import os
import sys
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from gitstar_ranking.spiders.github_repos import GitHubReposSpider

def ensure_directory(path):
    """Create directory if it doesn't exist and ensure it's writable"""
    if not os.path.exists(path):
        os.makedirs(path)
    elif not os.access(path, os.W_OK):
        os.chmod(path, 0o755)  # Make directory writable

def main():
    """Run the GitHub repository crawler"""
    print("Starting GitStar Ranking crawler...")
    
    # Get absolute paths
    base_dir = os.getcwd()
    output_dir = os.path.join(base_dir, 'output')
    logs_dir = os.path.join(base_dir, 'logs')
    
    # Ensure directories exist and are writable
    ensure_directory(output_dir)
    ensure_directory(logs_dir)
    
    # Create timestamp for this run
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    
    # Configure settings
    settings = get_project_settings()
    settings['LOG_FILE'] = os.path.join(logs_dir, f'gitstar_crawler_{timestamp}.log')
    settings['LOG_LEVEL'] = 'DEBUG'
    
    # Print current working directory and settings
    print(f"Current working directory: {base_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Log file: {settings['LOG_FILE']}")
    
    try:
        # Run the crawler
        process = CrawlerProcess(settings)
        process.crawl(GitHubReposSpider)
        process.start()  # This will block until crawling is finished
        
        # Check if output files were created
        json_output = os.path.join(output_dir, 'github_repos.json')
        csv_output = os.path.join(output_dir, 'github_repos.csv')
        
        if os.path.exists(json_output):
            print(f"JSON output file created: {json_output}")
            print(f"File size: {os.path.getsize(json_output)} bytes")
        else:
            print("Warning: JSON output file was not created")
            
        if os.path.exists(csv_output):
            print(f"CSV output file created: {csv_output}")
            print(f"File size: {os.path.getsize(csv_output)} bytes")
        else:
            print("Warning: CSV output file was not created")
            
    except Exception as e:
        print(f"Error running crawler: {str(e)}")
        sys.exit(1)
    
    print("Crawler finished successfully")
    sys.exit(0)

if __name__ == "__main__":
    main() 