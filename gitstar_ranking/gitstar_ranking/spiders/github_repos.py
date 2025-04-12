import scrapy
import re
from ..items import GitHubRepoItem
import logging
import os

class GitHubReposSpider(scrapy.Spider):
    name = 'github_repos'
    allowed_domains = ['gitstar-ranking.com']
    start_urls = ['https://gitstar-ranking.com/repositories']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1,  # Add delay between requests to be polite
        'CONCURRENT_REQUESTS': 8,  # Control concurrency
        'RETRY_TIMES': 3,  # Retry failed requests
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_LEVEL': 'DEBUG',  # Set to DEBUG for more detailed logging
        'FEEDS': {
            'output/github_repos.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'overwrite': True,
            },
            'output/github_repos.csv': {
                'format': 'csv',
                'encoding': 'utf8',
                'store_empty': False,
                'overwrite': True,
            },
        },
    }
    
    def __init__(self, *args, **kwargs):
        super(GitHubReposSpider, self).__init__(*args, **kwargs)
        self.repo_count = 0
        self.max_repos = 5000
        self.logger.setLevel(logging.DEBUG)
        
        # Ensure output directory exists
        output_dir = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def start_requests(self):
        """Override start_requests to add debugging"""
        self.logger.debug("Starting requests...")
        for url in self.start_urls:
            self.logger.debug(f"Requesting URL: {url}")
            yield scrapy.Request(url, callback=self.parse, errback=self.errback)
    
    def errback(self, failure):
        """Handle request errors"""
        self.logger.error(f"Request failed: {failure.value}")
    
    def parse(self, response):
        """Parse the repository listing page"""
        self.logger.debug(f"Processing response from: {response.url}")
        self.logger.debug(f"Response status: {response.status}")
        
        # Extract repositories from current page
        repo_items = response.css('.list-group-item.paginated_item')
        self.logger.debug(f"Found {len(repo_items)} repository items on page")
        
        if not repo_items:
            self.logger.warning("No repository items found on page")
            self.logger.debug(f"Response body: {response.body[:1000]}")  # Log first 1000 chars of response
            
        for item in repo_items:
            # Check if we've reached the limit
            if self.repo_count >= self.max_repos:
                self.logger.info(f"Reached maximum repository limit of {self.max_repos}")
                return
            
            repo = GitHubRepoItem()
            
            # Extract rank and name
            name_element = item.css('.name::text').getall()
            if name_element:
                # Get rank from the first part (e.g., "1.")
                rank_text = name_element[0].strip()
                try:
                    repo['rank'] = int(rank_text.rstrip('.'))
                except ValueError:
                    self.logger.warning(f"Could not parse rank from: {rank_text}")
                    continue
                
                # Get full repository name
                full_name = item.css('.name .hidden-xs.hidden-sm::text').get()
                if not full_name:
                    # Try alternate selector for mobile view
                    full_name = item.css('.name .hidden-md.hidden-lg::text').get()
                
                if full_name:
                    repo['name'] = full_name.strip()
                else:
                    # Fallback: Get link text which contains repo name
                    href = item.css('a::attr(href)').get()
                    if href and href.startswith('/'):
                        repo['name'] = href.lstrip('/')
            
            # Extract star count
            stars_text = item.css('.stargazers_count::text').getall()
            if stars_text:
                # Get the last text node which contains the star count
                stars_text = stars_text[-1].strip()
                try:
                    repo['stars'] = int(stars_text.replace(',', ''))
                except ValueError:
                    self.logger.warning(f"Could not parse stars from: {stars_text}")
                    repo['stars'] = 0
            else:
                repo['stars'] = 0
            
            # Extract description
            desc_element = item.css('.repo-description::attr(title)').get()
            if desc_element:
                repo['description'] = desc_element.strip()
            else:
                # Fallback to text content if title attribute is not available
                desc_text = item.css('.repo-description::text').get()
                if desc_text:
                    repo['description'] = desc_text.strip()
                else:
                    repo['description'] = "No description available"
            
            # Extract language
            lang_element = item.css('.repo-language span::text').get()
            repo['language'] = lang_element.strip() if lang_element else "No language available"
            
            self.repo_count += 1
            self.logger.debug(f"Processed repository {self.repo_count}: {repo['name']}")

            #Extract image url
            avatar_url = item.css('img.avatar_image_big::attr(src)').get()
            if avatar_url:
                repo['avatar_url'] = avatar_url
            else:
                # Fallback to any image within the item if specific class not found
                any_img = item.css('img::attr(src)').get()
                repo['avatar_url'] = any_img if any_img else "No avatar available"
            
            # Extract repository URL from the href of the main anchor
            repo_url = item.css('a::attr(href)').get()
            if repo_url:
            # If it's a relative URL, you might want to join it with the base URL
                repo['repo_url'] = response.urljoin(repo_url)
            else:
                repo['repo_url'] = "No URL available"
            
            self.logger.debug(f"Processed repository {self.repo_count}: {repo['name']}")
            yield repo
        
        # Follow pagination only if we haven't reached the limit
        if self.repo_count < self.max_repos:
            next_page = response.css('li.next a::attr(href)').get()
            if next_page:
                self.logger.info(f"Following next page: {next_page}")
                yield response.follow(next_page, self.parse)
            else:
                self.logger.info("Reached the last page of repositories")
        else:
            self.logger.info(f"Reached maximum repository limit of {self.max_repos}") 

    