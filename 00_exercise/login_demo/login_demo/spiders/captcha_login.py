# -*- coding: utf-8 -*-
import json
from PIL import Image
from io import BytesIO
import pytesseract
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.log import logger


class CaptchaLoginSpider(scrapy.Spider):
    name = 'captcha_login'
    allowed_domains = ['xxx.com']
    start_urls = ['http://xxx.com/']

    def parse(self, response):
        pass
