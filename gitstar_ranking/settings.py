# Scrapy settings for gitstar_ranking project

BOT_NAME = 'gitstar_ranking'

SPIDER_MODULES = ['gitstar_ranking.spiders']
NEWSPIDER_MODULE = 'gitstar_ranking.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performing at the same time
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1.0
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 3.0
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 4.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0  # Never expire during the crawl
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Configure item pipelines
ITEM_PIPELINES = {
    'gitstar_ranking.pipelines.GitstarRankingPipeline': 300,
}

# Enable memory usage extension
MEMUSAGE_ENABLED = True
MEMUSAGE_LIMIT_MB = 512
MEMUSAGE_WARNING_MB = 384

# Configure logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/spider.log'

# Configure retry middleware
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

# Configure download timeout
DOWNLOAD_TIMEOUT = 30

# Enable cookies
COOKIES_ENABLED = True

# Configure maximum response size (2MB)
DOWNLOAD_MAXSIZE = 2097152

# Configure depth priority
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleLifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.LifoMemoryQueue'

# Configure priority settings
SCHEDULER_PRIORITY_QUEUE = 'scrapy.pqueues.DownloaderAwarePriorityQueue'

# Configure concurrent items in pipeline
CONCURRENT_ITEMS = 200

# Configure stats collection
STATS_CLASS = 'scrapy.statscollectors.MemoryStatsCollector'

# Configure request fingerprinting
DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'

# Configure DNS settings
DNS_TIMEOUT = 10
DNS_RESOLVER = 'scrapy.resolver.CachingThreadedResolver'

# Configure redirect middleware
REDIRECT_ENABLED = True
REDIRECT_MAX_TIMES = 5 