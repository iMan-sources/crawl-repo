import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict, Tuple
from pathlib import Path
from tqdm import tqdm
from retry import retry
from fake_useragent import UserAgent

from .config import (
    BASE_URL, MAX_REPOS, REPOS_PER_PAGE, 
    MAX_RETRIES, RETRY_DELAY, REQUEST_TIMEOUT
)
from .cache_manager import CacheManager

logger = logging.getLogger(__name__)

class PageFinder:
    def __init__(self, cache_file: Path):
        """Initialize page finder
        
        Args:
            cache_file (Path): Path to cache file for storing HTML content
        """
        self.cache = CacheManager(cache_file)
        self.session = requests.Session()
        self.pages_info: Dict[int, int] = {}  # page_number -> repo_count
    
    @retry(tries=MAX_RETRIES, delay=RETRY_DELAY, backoff=2)
    def _fetch_page(self, page: int) -> str:
        """Fetch page content with retries and caching
        
        Args:
            page (int): Page number to fetch
            
        Returns:
            str: HTML content of the page
        """
        url = f"{BASE_URL}?page={page}"
        
        # Try to get from cache first
        cached = self.cache.get(url)
        if cached:
            logger.debug(f"Cache hit for page {page}")
            return cached
        
        # Fetch from web if not in cache
        headers = {
            'User-Agent': UserAgent().random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        response = self.session.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        content = response.text
        
        # Cache the content
        self.cache.set(url, content)
        logger.debug(f"Cached content for page {page}")
        
        return content
    
    def _count_repos_on_page(self, html: str) -> int:
        """Count repositories on a page
        
        Args:
            html (str): HTML content of the page
            
        Returns:
            int: Number of repositories found on the page
        """
        soup = BeautifulSoup(html, 'html.parser')
        repos = soup.select('.list-group-item.paginated_item')
        return len(repos)
    
    def find_required_pages(self) -> Tuple[int, Dict[int, int]]:
        """Find and cache all pages needed to reach MAX_REPOS
        
        Returns:
            Tuple[int, Dict[int, int]]: Total pages needed and page info mapping
        """
        total_repos = 0
        current_page = 1
        
        with tqdm(total=MAX_REPOS, desc="Finding pages") as pbar:
            while total_repos < MAX_REPOS:
                try:
                    html = self._fetch_page(current_page)
                    repos_count = self._count_repos_on_page(html)
                    
                    if repos_count == 0:
                        logger.warning(f"No repositories found on page {current_page}")
                        break
                    
                    self.pages_info[current_page] = repos_count
                    total_repos += repos_count
                    pbar.update(min(repos_count, MAX_REPOS - (total_repos - repos_count)))
                    
                    logger.info(f"Page {current_page}: Found {repos_count} repositories "
                              f"(Total: {total_repos})")
                    
                    current_page += 1
                    
                except Exception as e:
                    logger.error(f"Error processing page {current_page}: {str(e)}")
                    break
        
        return current_page - 1, self.pages_info
    
    def get_cached_pages(self) -> Dict[int, str]:
        """Get all cached pages
        
        Returns:
            Dict[int, str]: Mapping of page numbers to HTML content
        """
        cached_pages = {}
        for page in self.pages_info.keys():
            url = f"{BASE_URL}?page={page}"
            content = self.cache.get(url)
            if content:
                cached_pages[page] = content
        return cached_pages 