# -*- coding: utf-8 -*-
import scrapy
from ..items import MaoyanTopItem


class MaoyantopSpider(scrapy.Spider):
    name = 'maoyantop'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/board/4']

    def parse(self, response):
        results = response.css('dl.board-wrapper dd')
        for result in results:
            movie = MaoyanTopItem()
            movie['index'] = result.css('i::text').extract_first()
            movie['title'] = result.css('.image-link::attr(title)').extract_first().strip()
            movie['actor'] = result.css('.star::text').extract_first().strip()[3:]
            movie['time'] = result.css('.releasetime::text').extract_first().strip()[5:]
            movie['score'] = ''.join(result.css('.score i::text').extract())
            movie['image'] = result.css('.board-img::attr(data-src)').extract_first()
            yield movie

        # try:
        #     results = response.css('.list-pager li a')
        #     for result in results:
        #         if result.css('a::text').extract_first() == '下一页':
        #             next_page_url = result.css('a::attr(href)').extract_first()
        #     if next_page_url:
        #         yield scrapy.Request(self.start_urls[0] + next_page_url)
        # except UnboundLocalError:
        #     pass
