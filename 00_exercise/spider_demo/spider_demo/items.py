# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanTopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    index = scrapy.Field()
    title = scrapy.Field()
    actor = scrapy.Field()
    time = scrapy.Field()
    score = scrapy.Field()
    image = scrapy.Field()


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    review_rating = scrapy.Field()
    review_num = scrapy.Field()
    upc = scrapy.Field()
    stock = scrapy.Field()
