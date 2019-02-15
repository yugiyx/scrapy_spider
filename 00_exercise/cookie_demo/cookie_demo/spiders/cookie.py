# -*- coding: utf-8 -*-
import scrapy


class CookieSpider(scrapy.Spider):
    name = 'cookie'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/setting/profile']

    def parse(self, response):
        pass
