from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import time
import logging

class CustomRetryMiddleware(RetryMiddleware):
    def __init__(self, settings):
        super().__init__(settings)
        self.logger = logging.getLogger(__name__)
    
    def process_response(self, request, response, spider):
        if response.status in self.retry_http_codes:
            self.logger.warning(f'Retrying {request} due to status {response.status}')
            reason = response_status_message(response.status)
            # Add exponential backoff
            retry_count = request.meta.get('retry_times', 0)
            delay = 2 ** retry_count
            self.logger.info(f"Waiting {delay} seconds before retrying...")
            time.sleep(delay)
            return self._retry(request, reason, spider) or response
        return response 