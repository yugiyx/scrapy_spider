# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import BookItem


class ToscrapeBookSpider(scrapy.Spider):
    name = 'toscrape_book'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        le = LinkExtractor(restrict_css='.product_pod')
        links = le.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse_book)

        le = LinkExtractor(restrict_css='li.next')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url)

    def parse_book(self, response):
        book = BookItem()
        sel = response.css('.product_main')
        book['name'] = sel.css('h1::text').extract_first()
        book['price'] = sel.css('.price_color::text').extract_first()
        book['review_rating'] = sel.css(
            '.star-rating::attr(class)').re_first('star-rating (\w+)')
        sel = response.css('.table-striped td::text')
        book['upc'] = sel.extract()[0]
        book['stock'] = sel.re_first('In stock \((\d+) available\)')
        book['review_num'] = sel.extract()[6]
        yield book
