# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from csv import DictWriter

from qidian.items import *


class QidianPipeline(object):
    def __init__(self):
        self.book_csv = 'book.csv'
        self.juan_csv = 'juan.csv'
        self.seg_csv = 'seg.csv'

    def save_csv(self, item, filename):
        has_header = os.path.exists(filename);
        with open(filename, 'a', encoding='utf-8') as f:
            writer = DictWriter(f, fieldnames=item.keys())
            if not has_header:
                writer.writeheader()
            writer.writerow(item)

    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            self.save_csv(item, self.book_csv)
        elif isinstance(item, JuanItem):
            self.save_csv(item, self.juan_csv)
        return item
