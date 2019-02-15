# -*- coding: utf-8 -*-
import json
import hashlib
import scrapy
from ..items import ImageItem


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/kuleko/']
    url = 'https://www.instagram.com/graphql/query/?query_hash=a5164aed103f24b03e7b7747a2d94e3c&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'
    page_count = 1
    user_id = ''
    rhx_gis = ''

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    def parse(self, response):
        images = ImageItem()
        if response.css('script'):
            self.user_id = response.css('script').re_first('filePage_(.*?)"')
            self.rhx_gis = response.css('script').re_first('rhx_gis":"(.*?)"')
            json_data = json.loads(response.css('script')[3].extract()[52:-10])
            items = json_data['entry_data']['ProfilePage'][0]['graphql']
        else:
            json_data = json.loads(response.text)
            items = json_data['data']
        page_info = items['user']['edge_owner_to_timeline_media']['page_info']
        cursor = page_info['end_cursor']
        has_next_page = page_info['has_next_page']
        edges = items['user']['edge_owner_to_timeline_media']['edges']
        images['title'] = edges[0]['node']['owner']['username']
        images['image_urls'] = [item['node']['display_url']
                                for item in edges
                                if not item['node']['is_video']]
        images['page'] = self.page_count
        self.page_count += 1
        yield images

        if has_next_page:
            next_url = self.url.format(user_id=self.user_id, cursor=cursor)
            queryVariables = '{"id":"' + self.user_id + \
                '","first":12,"after":"' + cursor + '"}'
            self.headers['X-Instagram-GIS'] = self.hash_str(
                self.rhx_gis + ":" + queryVariables)
            yield scrapy.Request(next_url, headers=self.headers)

    def hash_str(self, strInfo):
        h = hashlib.md5()
        h.update(strInfo.encode("utf-8"))
        return h.hexdigest()
