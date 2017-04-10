# -*- coding: utf-8 -*-
# flake8: noqa

# Scrapy settings for reviews_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:45.0) Gecko/20100101 Firefox/45.0'
CONCURRENT_REQUESTS_PER_DOMAIN = 100

DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.CustomCrawleraMiddleware': 610,
}

ITEM_PIPELINES = {
   'crawler.pipelines.SQSStorePipeline': 200
}

DOWNLOAD_DELAY = 2
#REACTOR_THREADPOOL_MAXSIZE = 20
#LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False
##RETRY_ENABLED = False
#DOWNLOAD_TIMEOUT = 60
##REDIRECT_ENABLED = False
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
RETRY_HTTP_CODES = range(400, 600)
RETRY_TIMES = 4

_LOCAL_DEV_ENVIRONMENT = os.getenv('LOCAL_DEV_ENVIRONMENT')

if _LOCAL_DEV_ENVIRONMENT:
    HTTPCACHE_ENABLED=False