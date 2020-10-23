# -*- coding: utf-8 -*-
import uuid

import scrapy
from scrapy import Request
from scrapy.http import Response

from qidian.items import *


# 创建项目命令
# scrapy startproject 项目名称
# 创建爬虫命令
# scrapy genspider 爬虫名 域名
# 启动爬虫命令
# scrapy crawl 爬虫名
# 调试爬虫命令
# scrapy shell url
# scrapy shell  + fetch(url)

# 样式选择器
# selector()

# css() 样式选择器，返回Selector选择器的课迭代对象
#       scrapy.selector.SelectorList
#       scrapy.selector.Selector
#   样式选择器提取属性或者文本
#       ::text 提取文本
#       ::attr("属性名") 提取属性


# xpath()


# 选择器常用方法
#       css()/xpath()/x()
#       extract() 提取选择中所有内容，返回list
#       extract_first()/get() 提取每个选择器中的内容，返回是文本


class WanbenSpider(scrapy.Spider):
    name = 'wanben'
    allowed_domains = ['qidian.com']
    start_urls = ['https://www.qidian.com/finish']

    def parse(self, response: Response):
        if response.status == 200:
            lis = response.css('.all-img-list li')
            print(f'------{len(lis)}-------------')
            for li in lis:
                item = BookItem()
                item['book_id'] = uuid.uuid4().hex
                a = li.xpath('./div[1]/a')
                item['book_url'] = a.xpath('./@href').get()
                item['book_cover'] = a.xpath('./img/@src').get()
                item['book_name'] = li.xpath('./div[2]/h4//text()').get()

                item['author'], *item['tags'] = li.css('.author a::text').extract()
                item['summary'] = li.css('.intro::text').get()

                # 请求小说的详情
                yield Request('https:' + item['book_url'],
                              callback=self.parse_info,
                              priority=1,
                              meta={'book_id': item['book_id']})

                yield item

            # 获取下一页
            next_url = response.css('.lbf-pagination-item-list ').xpath('./li[last()]/a/@href').get()
            if next_url.find('javascript') == -1:
                yield Request('https:' + next_url, priority=100)

    def parse_info(self, response: Response):
        print('---------详情完事儿了---------------', response.meta['book_id'])
