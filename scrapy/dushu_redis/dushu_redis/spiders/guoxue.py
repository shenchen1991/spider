# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.http import Response
from scrapy_redis.spiders import RedisSpider


class GuoxueSpider(RedisSpider):
    name = 'guoxue'
    allowed_domains = ['dushu.com']

    redis_key = 'gx_start_urls'

    def parse(self, response: Response):
        for url in response.css('.sub-catalog a::attr("href")').extract():
            yield Request('https://www.dushu.com' + url, callback=self.parse_item)

    def parse_item(self, response):
        divs = response.css('.book-info')
        for div in divs:
            item = {}
            item['name'] = div.xpath('./div//img/@alt').get()
            item['cover'] = div.xpath('./div//img/@src').get()
            item['detail_url'] = div.xpath('./div/a/@href').get()
            yield item
