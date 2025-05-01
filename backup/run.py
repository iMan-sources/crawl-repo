#!/usr/bin/env python3
import os
import sys
import logging
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from gitstar_ranking.spiders.scout_spider import ScoutSpider
from gitstar_ranking.spiders.github_repos import GitHubReposSpider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/crawler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def setup_directories():
    """Create necessary directories if they don't exist"""
    dirs = ['logs', 'output', 'httpcache']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            logger.info(f"Created directory: {d}")

@defer.inlineCallbacks
def crawl():
    """Run spiders in sequence"""
    try:
        setup_directories()
        settings = get_project_settings()
        runner = CrawlerRunner(settings)
        
        # Run scout spider first
        logger.info("Starting scout spider to map repository pages...")
        yield runner.crawl(ScoutSpider)
        
        # Check if page mapping was created
        if not os.path.exists('page_mapping.txt'):
            logger.error("Scout spider failed to create page mapping!")
            return
        
        # Run main spider
        logger.info("Starting main spider to collect repository data...")
        yield runner.crawl(GitHubReposSpider)
        
        # Verify output files exist
        output_files = ['output/github_repos.json', 'output/github_repos.csv']
        missing_files = [f for f in output_files if not os.path.exists(f)]
        
        if missing_files:
            logger.error(f"Missing output files: {missing_files}")
        else:
            logger.info("Crawling completed successfully!")
            
    except Exception as e:
        logger.error(f"Error during crawling: {str(e)}", exc_info=True)
    finally:
        reactor.stop()

def main():
    """Main entry point"""
    configure_logging()
    crawl()
    reactor.run()

if __name__ == '__main__':
    main() 