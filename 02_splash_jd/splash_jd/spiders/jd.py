# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest

lua_script = '''
function main(splash, args)
    splash:set_viewport_size(1028, 10000)
    splash.images_enabled = false
    splash:go(args.url)
    splash:wait(10)
    splash.scroll_position = {0,5000}
--    splash:runjs("window.scrollTo(0, document.body.scrollHeight)")
--    splash:runjs("document.getElementsByClassName('page')[0].scrollIntoView(true)")
    splash:wait(10)
    return splash:html()
end
'''


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['https://search.jd.com/Search?keyword=python']

    def parse(self, response):
        total_page = int(response.css('.fp-text i::text').extract_first())
        for i in range(10):
            url = '%s&page=%s' % (self.start_urls[0], 2 * i + 1)
            print('下载页数', i + 1)
            yield SplashRequest(url, self.parse_books, endpoint='execute',
                                args={'lua_source': lua_script},
                                cache_args=['lua_source'])

    def parse_books(self, response):
        sels = response.css('.clearfix .gl-item')
        print(response.url)
        print('本页书数量', len(sels))
        for sel in sels:
            yield{
                'name': sel.css('.p-name').xpath(
                    'string(.//em)').extract_first(),
                'price': sel.css('.p-price i::text').extract_first(),
            }
