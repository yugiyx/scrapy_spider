# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import ExampleItem


class ExamplesSpider(scrapy.Spider):
    name = 'examples'
    allowed_domains = ['matplotlib.org']
    start_urls = ['https://matplotlib.org/examples/index.html']

    def parse(self, response):
        le = LinkExtractor(restrict_css='.toctree-wrapper .toctree-l2')
        links = le.extract_links(response)
        print(len(links))
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse_source)

    def parse_source(self, response):
        href = response.css('.reference::attr(href)').extract_first()
        url = response.urljoin(href)
        example = ExampleItem()
        example['file_urls'] = [url]
        return example
