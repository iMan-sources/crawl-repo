from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from urllib.parse import urljoin
import logging
import re

from .config import BASE_URL

logger = logging.getLogger(__name__)

class RepoParser:
    @staticmethod
    def parse_repository(item_html: str) -> Optional[Dict]:
        """Parse a single repository item from its HTML
        
        Args:
            item_html (str): HTML content of the repository item
            
        Returns:
            Optional[Dict]: Repository data if successfully parsed, None otherwise
        """
        try:
            soup = BeautifulSoup(item_html, 'html.parser')
            
            # Extract rank and name
            name_container = soup.select_one('.name')
            if not name_container:
                logger.warning("No name container found")
                return None
            
            # Extract rank from the first text node
            rank_text = next((text.strip() for text in name_container.stripped_strings), None)
            if not rank_text:
                logger.warning("No rank text found")
                return None
            
            rank_match = re.match(r'^(\d+)\.', rank_text)
            if not rank_match:
                logger.warning(f"Could not parse rank from: {rank_text}")
                return None
            rank = int(rank_match.group(1))
            
            # Try multiple strategies to extract the name
            name = None
            
            # Strategy 1: Try to get name from specific class selectors
            for selector in ['.hidden-xs.hidden-sm', '.hidden-md.hidden-lg']:
                name_elem = name_container.select_one(selector)
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    break
            
            # Strategy 2: If no name found, try to get from href
            if not name:
                link = name_container.find('a')
                if link and 'href' in link.attrs:
                    href = link['href']
                    if href.startswith('/'):
                        name = href[1:]  # Remove leading slash
            
            # Strategy 3: If still no name, try to get the last non-rank text
            if not name:
                text_parts = [text.strip() for text in name_container.stripped_strings]
                name = next((part for part in reversed(text_parts) 
                           if part and not part.endswith('.') and not re.match(r'^\d+\.', part)), None)
            
            if not name:
                logger.warning(f"No valid name found for repository rank {rank}")
                return None
            
            # Clean up the name by removing duplicates and extra whitespace
            name = re.sub(r'(.+?)\1+$', r'\1', name)
            name = re.sub(r'\s+', ' ', name).strip()
            
            # Extract stars
            stars_elems = soup.select('.stargazers_count')
            if stars_elems:
                # Get the last text node which contains the star count
                stars_text = stars_elems[-1].get_text(strip=True)
                try:
                    stars = int(stars_text.replace(',', ''))
                except ValueError:
                    logger.warning(f"Could not parse stars from: {stars_text}")
                    stars = 0
            else:
                stars = 0
            
            # Extract description
            desc_elem = soup.select_one('.repo-description')
            description = desc_elem.get('title', '') if desc_elem else None
            if not description:
                description = desc_elem.get_text(strip=True) if desc_elem else "No description available"
            
            # Extract language
            lang_elem = soup.select_one('.repo-language span')
            language = lang_elem.get_text(strip=True) if lang_elem else "No language available"
            
            # Extract avatar URL
            avatar_url = None
            # Try multiple selectors
            for selector in ['img.avatar_image_big', '.avatar_image_big img', '.list-group-item img']:
                img = soup.select_one(selector)
                if img and 'src' in img.attrs:
                    avatar_url = img['src']
                    break
            
            # Extract repo URL
            repo_url = None
            link = soup.select_one('a')
            if link and 'href' in link.attrs:
                repo_url = urljoin(BASE_URL, link['href'])
            
            return {
                'rank': rank,
                'name': name,
                'stars': stars,
                'description': description,
                'language': language,
                'avatar_url': avatar_url,
                'repo_url': repo_url
            }
            
        except Exception as e:
            logger.error(f"Error parsing repository: {str(e)}")
            return None
    
    @classmethod
    def parse_page(cls, html: str) -> List[Dict]:
        """Parse all repositories from a page
        
        Args:
            html (str): HTML content of the page
            
        Returns:
            List[Dict]: List of parsed repository data
        """
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.select('.list-group-item.paginated_item')
        
        repos = []
        for item in items:
            repo_data = cls.parse_repository(str(item))
            if repo_data:
                repos.append(repo_data)
        
        return repos 