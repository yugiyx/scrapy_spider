# -*- coding: utf-8 -*-
import json
import scrapy
from ..items import ImageItem


class MeituSpider(scrapy.Spider):

    BASE_URL = 'https://www.toutiao.com/search_content/?offset=%s&format=json&keyword=%s&autoload=true&count=20&cur_tab=3&from=gallery'
    START_PAGE = 0
    KEYWORD = '街拍'

    name = 'images'
    allowed_domains = ['toutiao.com']
    start_urls = [BASE_URL % (START_PAGE, KEYWORD)]

    def parse(self, response):
        infos = json.loads(response.text)
        items = infos['data']
        for item in items:
            if 'open_url' in item:
                url = response.urljoin(item['open_url'].replace('group/', 'a'))
            yield scrapy.Request(url, self.parse_images)

        # if infos['has_more']:
        #     self.START_PAGE += 20
        #     next_url = self.BASE_URL % (self.START_PAGE, self.KEYWORD)
        #     yield scrapy.Request(next_url, self.parse)

    def parse_images(self, response):
        images = ImageItem()
        images['title'] = response.css('title::text').extract_first()
        infos = response.css('script').re_first(
            'sub_images\\\\":(.*?),\\\\"max').replace('\\', '')
        items = json.loads(infos)
        images['image_urls'] = [item['url'] for item in items]
        return images
