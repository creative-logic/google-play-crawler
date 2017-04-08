import scrapy

from ..utils.serialize import deserialize_arg

class BaseReviewsSpider(scrapy.Spider):
    def __init__(self, place):
        self.place = deserialize_arg(place)
        self.logger.debug('Using place: %r' % self.place)
        self.last_review_hashes = self.place.get('last_review_hashes')
        self.profile_key = self.place.get('profile_key')
        self.start_cookiejars = self.place.get('persona', {}).get('cookies', {})
        credentials = self.place.get('persona', {}).get('credentials', {})
        self.persona_username = credentials.get('username')
        self.persona_password = credentials.get('password')

    def start_requests(self):
        req = self.profile_request(self.profile_key) if self.profile_key else None
        if req:
            self.logger.debug('Build request {} from profile key: {}'.format(req, self.profile_key))
            yield req
        else:
            for req in self.search_requests():
                yield req

    def profile_request(self, profile_key):
        return scrapy.Request('https://play.google.com/store/apps/details?id='+profile_key, self.parseApp)

    def search_requests(self):
        raise NotImplementedError("Missing implementation for {}.search_requests".format(
            self.__class__.__name__))

    def parseApp(self, response):
        raise NotImplementedError("Missing implementation for {}.parseApp".format(
            self.__class__.__name__))
