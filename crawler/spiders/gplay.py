import scrapy
import string
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from crawler.items import AppCategoryItem,AppItem
from .base import BaseReviewsSpider

class GPLAYSpider(BaseReviewsSpider):
    
    name = "gplay"
    allowed_domains = ["play.google.com"]
    
    #start_urls = [
    #    "https://play.google.com/store/apps"
    #]
   
    #rules = (
    #    Rule(LinkExtractor(allow=('/store/apps$', )), callback='parseCategoryGroup',follow=True),
    #    Rule(LinkExtractor(allow=('/store/apps/category/.*', )), callback='parseCategory',follow=True),
    #    Rule(LinkExtractor(allow=('/store/search\?.*', )), callback='parseSearch',follow=True),
    #)
    
    def search_requests(self):
        self.logger.debug('search_requests ============================================')
        url = 'https://play.google.com/store/apps'
        yield scrapy.Request(url, self.parseCategoryGroup)

    def parseCategoryGroup(self, response):
        self.logger.debug('parseCategoryGroup ============================================')
        hxs = Selector(response)

        categories = hxs.xpath('//ul/li/a[contains(@href,"/store/apps/category")]')
        self.logger.debug('This many categories %s' % len(categories));
        for category in categories:
            categoryName = category.xpath('text()').extract_first().strip()
            categoryURL = category.xpath('@href').extract_first().strip()
            self.logger.debug('This is the category name %s and category URL %s' % (categoryName,categoryURL))
            yield Request('https://play.google.com'+categoryURL,callback=self.parseCollectionGroup)

        #yield Request('https://play.google.com/store/apps/category/ART_AND_DESIGN',callback=self.parseCollectionGroup)
        return

    def parseCollectionGroup(self, response):
        self.logger.debug('parseCollectionGroup ============================================')
        hxs = Selector(response)

        collections = hxs.xpath('//h2[@class="single-title-link"]/a[contains(@href,"/collection/")]')
        self.logger.debug('This many collections %s' % len(collections));
        for collection in collections:
            collectionName = collection.xpath('text()').extract_first()
            collectionURL = collection.xpath('@href').extract_first()
            self.logger.debug('This is the collection name %s and collection URL %s' % (collectionName,collectionURL))
            yield Request('https://play.google.com'+collectionURL,callback=self.parseCollection)

        #yield Request('https://play.google.com/store/apps/category/AUTO_AND_VEHICLES/collection/topselling_paid',callback=self.parseCollection)
        return
   
    def parseCollection(self,response):
        self.logger.debug('parseCollection ============================================')
        basePath = response.url.split('?')[0]   
       
        if '/collection/' in response.url:
            self.logger.debug('The response url is: %s' % response.url)
            hxs = Selector(response)
            apps = hxs.xpath('//a[@class="title"]')
            hasApp = False
            for app in apps:
                hasApp = True
                appName = app.xpath('text()').extract()
                appURL = app.xpath('@href').extract()
                self.logger.debug('App name %s and App URL %s' % (appName,appURL))
                yield Request('https://play.google.com'+appURL[0] ,callback=self.parseApp)
                 
            if hasApp :
                import re
                m = re.match(r'(.*)\?start=(\d+)&num=24',response.url)
                if m is None :
                    startNumber = 24                  
                else:
                    startNumber = int(m.group(2))+24
                    self.logger.debug('The group is: %s' % m.group())
                self.logger.debug('This is the start number: %s' % startNumber)
                yield Request(basePath+'?start='+str(startNumber)+'&num=24',callback=self.parseCollection)

        return
   
    def parseSearch(self,response):
        self.logger.debug('parseSearch ============================================')
        import re
        m = re.match(r'(.*)&start=(\d+)&num=24',response.url)
        if m is None :
            basePath = response.url
            startNumber = 24                  
        else:
            startNumber = int(m.group(2))+24
            basePath = m.group(1)
       
        hxs = Selector(response)
        apps = hxs.xpath('//a[contains(@href,"/store/apps/details")]')
        hasApp = False
        for app in apps:
            hasApp = True
            appURL = app.xpath('@href').extract()
            yield Request('https://play.google.com'+appURL[0] ,callback=self.parseApp)
            
        if hasApp :
            self.logger.debug('next search -----')
            yield Request(basePath+'&start='+str(startNumber)+'&num=24',callback=self.parseSearch)

        return
   
    def parseApp(self,response):
        self.logger.debug('parseApp ============================================')
        hxs = Selector(response)
 
        apps = hxs.xpath('//a[@class="common-snippet-title"]')
        for app in apps:
            appURL = app.xpath('@href').extract()
            yield Request('https://play.google.com'+appURL[0] ,callback=self.parseApp)
            
        screens = hxs.css('div[class="thumbnails-wrapper"] img')
        screenShots=[]
        for screen in screens:
            screenShots.append(screen.xpath('@src').extract_first())
       
        metadata = hxs.xpath('//div[@class="main-content"]')
        
        app = {}
        app['url'] = response.url
        app['screenshots'] = screenShots
        app['name'] = metadata.css('div[itemprop="author"] span[itemprop="name"]::text').extract_first()
        app['author'] = metadata.css('div[itemprop="author"] span[itemprop="name"]::text').extract_first()
        app['genre'] = metadata.css('div[itemprop="author"] span[itemprop="genre"]::text').extract_first()
        app['badges'] = metadata.css('span[class="badge-title"]::text').extract()
        app['content_rating'] = metadata.css('span[class="document-subtitle content-rating-title"]::text').extract_first()
        app['rating_count'] = metadata.xpath('//meta[@itemprop="ratingCount"]/@content').extract_first()
        app['rating_value'] = metadata.xpath('//meta[@itemprop="ratingValue"]/@content').extract_first()
        app['description'] = metadata.css('div[itemprop="description"] > div').extract_first()
        app['individual_ratings'] = metadata.css('span[class="bar-number"]::text').extract()
        
        app['reviews'] = []
        reviews = metadata.css('div[data-load-more-section-id="reviews"] div.featured-review')
        self.logger.debug('Number of featured reviews found %s' % len(reviews))
        for r in reviews:
            review = {}
            review['author'] = r.css('span[class="author-name"]::text').extract_first().strip()
            review['text'] = r.css('div[class="review-text"]').extract_first()
            review['title'] = r.css('span[class="review-title"]::text').extract_first()
            review['author_img'] = r.css('span[class="responsive-img-hdpi"] > span::attr(style)').extract_first()[21:-1]
            app['reviews'].append(review)
        
        reviews = metadata.css('div[data-load-more-section-id="reviews"] div.single-review')
        self.logger.debug('Number of single reviews found %s' % len(reviews))
        for r in reviews:
            review = {}
            review['author'] = r.css('span[class="author-name"]::text').extract_first().strip()
            review['text'] = r.css('div[class="review-text"]').extract_first()
            review['title'] = r.css('span[class="review-title"]::text').extract_first()
            review['author_img'] = r.css('span[class="responsive-img-hdpi"] > span::attr(style)').extract_first()[21:-1]
            app['reviews'].append(review)
        
        app['recent_changes'] = metadata.css('div[class="recent-change"]::text').extract()
        app['updated'] = metadata.xpath('//div[@itemprop="datePublished"]/text()').extract_first().strip()
        app['number_of_downloads'] = metadata.xpath('//div[@itemprop="numDownloads"]/text()').extract_first().strip()
        app['software_version'] = metadata.xpath('//div[@itemprop="softwareVersion"]/text()').extract_first().strip()
        
        yield app