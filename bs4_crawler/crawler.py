import logging
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List
from multiprocessing import Pool, Manager
from tqdm import tqdm

from .config import (
    HTML_CACHE_FILE, RESULTS_FILE, CSV_FILE,
    NUM_WORKERS, MAX_REPOS
)
from .page_finder import PageFinder
from .repo_parser import RepoParser

logger = logging.getLogger(__name__)

class GitHubCrawler:
    def __init__(self):
        """Initialize the crawler"""
        self.page_finder = PageFinder(HTML_CACHE_FILE)
        self.total_pages = 0
        self.pages_info = {}
        self.cached_pages = {}
    
    def _worker_task(self, args: tuple) -> List[Dict]:
        """Worker process task to parse assigned pages
        
        Args:
            args (tuple): Tuple of (page_number, html_content)
            
        Returns:
            List[Dict]: List of parsed repository data
        """
        page_num, html = args
        logger.info(f"Worker processing page {page_num}")
        return RepoParser.parse_page(html)
    
    def run(self) -> List[Dict]:
        """Run the crawler
        
        Returns:
            List[Dict]: List of crawled repository data
        """
        try:
            logger.info("Finding and caching pages...")
            self.total_pages, self.pages_info = self.page_finder.find_required_pages()
            logger.info(f"Found {self.total_pages} pages with repositories")
            
            logger.info("Getting cached pages...")
            self.cached_pages = self.page_finder.get_cached_pages()
            logger.info(f"Retrieved {len(self.cached_pages)} cached pages")
            
            # Prepare work items
            work_items = [(page, html) for page, html in self.cached_pages.items()]
            
            # Process pages with worker pool
            all_repos = []
            with Pool(processes=NUM_WORKERS, maxtasksperchild=1) as pool:
                with tqdm(total=len(work_items), desc="Processing pages") as pbar:
                    for repos in pool.imap_unordered(self._worker_task, work_items):
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
            
        finally:
            # Clean up cache after finishing
            logger.info("Cleaning up temporary cache files...")
            self.page_finder.cache.cleanup() 