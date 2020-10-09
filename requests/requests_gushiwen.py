import os
import time
from csv import DictWriter

import requests
from lxml import etree
from requests import Response

from utils import header

base_url = 'https://www.gushiwen.cn/'


def item_pipeline(item):
    print(item)


has_header = os.path.exists('dushuwang.csv')  # 是否第一次操作
header_fields = ('name', 'author', 'content', 'tags')


def item_pipeline_csv(item):
    global has_header
    with open('dushuwang.csv', 'a', encoding='utf-8') as f:
        writer = DictWriter(f, header_fields)
        if not has_header:
            writer.writeheader()
            has_header = True

        writer.writerow(item)


def parse(html):
    root = etree.HTML(html)
    divs = root.xpath('//div[@class="left"]/div[@class="sons"]')
    item = {}
    for div in divs:
        if len(div.xpath('.//div[@class="tool"]')) == 1:
            item['name'] = div.xpath('.//p[1]//text()')[0]
            item['author'] = ' '.join(div.xpath('.//p[2]/a/text()'))
            item['content'] = '<br>'.join(div.xpath('.//div[@class="contson"]/text()'))
            item['tags'] = '，'.join(div.xpath('./div[last()]/a/text()'))
            # item_pipeline(item)
            item_pipeline_csv(item)

    # 获取下一页的链接
    next_url = base_url + root.xpath('//a[@id="amore"]/@href')[0]
    print(next_url)
    time.sleep(0.5)
    get(next_url)


def get(url):
    resp: Response = requests.get(url,
                                  headers={'user-agent': header.get_ua()})
    if resp.status_code == 200:
        parse(resp.text)
    else:
        raise Exception('失败')


if __name__ == '__main__':
    get('https://www.gushiwen.cn/')
