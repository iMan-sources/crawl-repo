import scrapy

class GitHubRepoItem(scrapy.Item):
    """Item for storing repository information"""
    rank = scrapy.Field()
    name = scrapy.Field()
    stars = scrapy.Field()
    description = scrapy.Field()
    language = scrapy.Field() 
    avatar_url = scrapy.Field()
    repo_url = scrapy.Field()
