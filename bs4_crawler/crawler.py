import logging
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List
from multiprocessing import Pool
from tqdm import tqdm

from .config import (
    RESULTS_FILE, CSV_FILE,
    NUM_WORKERS, TARGET_REPO_RANK
)
from .page_finder import PageFinder
from .repo_parser import RepoParser

logger = logging.getLogger(__name__)

class GitHubCrawler:
    def __init__(self):
        """Initialize the crawler"""
        self.page_finder = PageFinder()
    
    def _worker_task(self, page: int) -> List[Dict]:
        """Worker process task to fetch and parse a page
        
        Args:
            page (int): Page number to process
            
        Returns:
            List[Dict]: List of parsed repository data
        """
        logger.info(f"Worker processing page {page}")
        html = self.page_finder._fetch_page(page)
        return RepoParser.parse_page(html)
    
    def run(self) -> List[Dict]:
        """Run the crawler
        
        Returns:
            List[Dict]: List of crawled repository data
        """
        try:
            logger.info("Finding target page using binary search...")
            target_page, first_rank, last_rank = self.page_finder.find_target_page()
            
            if target_page == -1:
                logger.error("Could not find target page")
                return []
            
            logger.info(f"Found target page {target_page}. Now crawling all pages from 1 to 50...")
            
            # Create a list of all pages to crawl (1 to 50)
            pages_to_crawl = list(range(1, 51))
            
            # Process pages with worker pool
            all_repos = []
            with Pool(processes=NUM_WORKERS) as pool:
                with tqdm(total=len(pages_to_crawl), desc="Processing pages") as pbar:
                    for repos in pool.imap_unordered(self._worker_task, pages_to_crawl):
                        all_repos.extend(repos)
                        pbar.update()
            
            # Sort repositories by rank
            all_repos.sort(key=lambda x: x['rank'])
            
            # Save results
            logger.info(f"Saving {len(all_repos)} repositories to {RESULTS_FILE}")
            with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(all_repos, f, ensure_ascii=False, indent=2)
            
            # Save as CSV
            logger.info(f"Saving repositories to {CSV_FILE}")
            df = pd.DataFrame(all_repos)
            df.to_csv(CSV_FILE, index=False)
            
            return all_repos
            
        except Exception as e:
            logger.error(f"Error during crawling: {str(e)}")
            return [] 