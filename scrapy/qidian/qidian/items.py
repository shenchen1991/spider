# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    book_id = scrapy.Field
    book_url = scrapy.Field()
    book_cover = scrapy.Field()
    book_name = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    summary = scrapy.Field()


class JuanItem(scrapy.Item):
    juan_id = scrapy.Field
    title = scrapy.Field


class QidianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
