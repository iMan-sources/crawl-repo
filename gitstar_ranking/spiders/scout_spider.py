import scrapy
import logging
from collections import defaultdict

class ScoutSpider(scrapy.Spider):
    name = 'scout'
    allowed_domains = ['gitstar-ranking.com']
    start_urls = ['https://gitstar-ranking.com/repositories']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 4,
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_LEVEL': 'INFO',
        # Disable unnecessary pipeline and middleware
        'ITEM_PIPELINES': {},
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        },
        'STATS_DUMP': True,  # Enable stats printing
    }
    
    def __init__(self, *args, **kwargs):
        super(ScoutSpider, self).__init__(*args, **kwargs)
        self.cumulative_count = 0
        self.page_repo_counts = defaultdict(int)
        self.target_count = 5000
        self.found_target = False
        self.total_pages_needed = 0
        self.repos_per_page = []
    
    def parse(self, response):
        page_number = int(response.url.split('page=')[-1]) if 'page=' in response.url else 1
        repo_items = response.css('.list-group-item.paginated_item')
        page_count = len(repo_items)
        
        self.page_repo_counts[page_number] = page_count
        self.cumulative_count += page_count
        self.repos_per_page.append(page_count)
        
        # Calculate average repos per page
        avg_repos = sum(self.repos_per_page) / len(self.repos_per_page)
        estimated_total_pages = round(self.target_count / avg_repos)
        
        self.logger.info(
            f"\nProgress Update:"
            f"\n- Page {page_number}: Found {page_count} repos"
            f"\n- Cumulative repos: {self.cumulative_count}"
            f"\n- Average repos per page: {avg_repos:.1f}"
            f"\n- Estimated total pages needed: {estimated_total_pages}"
            f"\n- Progress: {(self.cumulative_count/self.target_count*100):.1f}% of target"
        )
        
        if self.cumulative_count >= self.target_count and not self.found_target:
            self.found_target = True
            self.total_pages_needed = page_number
            self.logger.info(
                f"\nTarget Found!"
                f"\n- Final page number: {page_number}"
                f"\n- Total pages needed: {self.total_pages_needed}"
                f"\n- Total repositories found: {self.cumulative_count}"
                f"\n- Average repos per page: {avg_repos:.1f}"
            )
            
            # Save the page mapping for the main spider
            with open('page_mapping.txt', 'w') as f:
                for p, count in sorted(self.page_repo_counts.items()):
                    f.write(f"{p},{count}\n")
            
            # Save detailed statistics
            with open('scout_stats.txt', 'w') as f:
                f.write(f"Total pages needed: {self.total_pages_needed}\n")
                f.write(f"Total repositories: {self.cumulative_count}\n")
                f.write(f"Average repos per page: {avg_repos:.1f}\n")
                f.write("\nPage-by-page breakdown:\n")
                for p, count in sorted(self.page_repo_counts.items()):
                    f.write(f"Page {p}: {count} repos\n")
            return
        
        if not self.found_target:
            next_page = response.css('li.next a::attr(href)').get()
            if next_page:
                yield response.follow(next_page, self.parse)
            else:
                self.logger.error("Reached last page without finding target count") 