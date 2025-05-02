import os
from pathlib import Path

# Base configuration
BASE_DIR = Path(__file__).parent
CACHE_DIR = BASE_DIR / 'cache'
OUTPUT_DIR = BASE_DIR / 'output'
LOGS_DIR = BASE_DIR / 'logs'

# Ensure directories exist
for directory in [CACHE_DIR, OUTPUT_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Crawler settings
BASE_URL = 'https://gitstar-ranking.com/repositories'
MAX_REPOS = 5000
REPOS_PER_PAGE = 100
NUM_WORKERS = 4
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 1

# Cache settings
CACHE_ENABLED = True
CACHE_TTL = 3600  # 1 hour
HTML_CACHE_FILE = CACHE_DIR / 'pages_cache.json'
RESULTS_FILE = OUTPUT_DIR / 'github_repos.json'
CSV_FILE = OUTPUT_DIR / 'github_repos.csv'

# Request headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
} 