BOT_NAME = 'gitstar_ranking'

SPIDER_MODULES = ['gitstar_ranking.spiders']
NEWSPIDER_MODULE = 'gitstar_ranking.spiders'

# Configure item pipelines
ITEM_PIPELINES = {
    'gitstar_ranking.pipelines.JsonWriterPipeline': 300,
    'gitstar_ranking.pipelines.CsvWriterPipeline': 400,
}

# Enable and configure the AutoThrottle extension
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 3
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Enable middleware
DOWNLOADER_MIDDLEWARES = {
    'gitstar_ranking.middlewares.CustomRetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,  # Disable default retry middleware
}

# Enable logging
LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'

# Configure a delay for requests for the same website
DOWNLOAD_DELAY = 1

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 8

# Configure retry times
RETRY_TIMES = 3

# Configure user agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Ensure UTF-8 encoding
FEED_EXPORT_ENCODING = 'utf-8'

# Configure output files
FEEDS = {
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
} 