import logging
from scrapy_crawlera import CrawleraMiddleware


logger = logging.getLogger(__name__)


class CustomCrawleraMiddleware(CrawleraMiddleware):
    """
    Customization of Crawlera Middleware to enable only
    when a request is being retried.
    """
    def open_spider(self, spider):
        persona = getattr(spider, 'place', {}).get('persona', {})
        proxy = persona.get('proxy', persona.get('Proxy'))
        if proxy:
            user, _, self.crawlera_url = self._parse_crawlera_info(proxy)
            self.apikey = user
            logger.debug('Using crawlera ({}...@{})'.format(self.apikey[:7],
                                                            self.crawlera_url))
            spider.crawlera_enabled = True
        super(CustomCrawleraMiddleware, self).open_spider(spider)

    def _parse_crawlera_info(self, proxy):
        if '@' in proxy:
            userpass, url = proxy.split('@')
        else:
            userpass, url = ':', proxy
        user, password = userpass.split(':')
        return user, password, url

    def _setup_proxy_for_request(self, request):
        """
        Only use proxy if retrying a request for the second time.
        """
        request.meta.setdefault('dont_proxy', True)
        should_use_proxy = request.meta.get('retry_times', 0) > 1
        if self.enabled and should_use_proxy or request.meta.get('force_proxy', False):
            logger.debug('Enabling proxy for %s' % request)
            request.meta.pop('dont_proxy')

    def process_request(self, request, spider):
        self._setup_proxy_for_request(request)
        super(CustomCrawleraMiddleware, self).process_request(request, spider)
