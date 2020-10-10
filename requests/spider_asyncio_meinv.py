import asyncio
import csv
import json
import os
import sys

import requests
from bs4 import BeautifulSoup, Tag

from utils.header import get_ua

headers = {
    'User-Agent': get_ua()
}


@asyncio.coroutine
def get(url):
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        yield from parse(resp.text)


@asyncio.coroutine
def post(url, page=2):
    yield from asyncio.sleep(0.5)
    print('正在下载', page, '页面')
    resp = requests.post(url, data={
        'total': 36,
        'action': 'fa_load_postlist',
        'paged': page,
        'category': 1,
        'wowDelay': '0.3s',
    }, headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        result = json.loads(resp.text)
        yield from parse(result['postlist'])
    yield from post(url, page + 1)


@asyncio.coroutine
def parse(html):
    root = BeautifulSoup(html, 'lxml')
    content_boxes = root.select('.content-box')

    for content_box in content_boxes:
        item = {}
        image: Tag = content_box.find('img')
        item['name'] = image.attrs.get('alt')
        item['cover'] = image.attrs.get('src')
        try:
            info = content_box.select('.posts-text')[0].get_text()
            _, birthday, city = [txt.strip() for txt in info.split('/')]
            item['birthday'], item['city'] = birthday[2:].strip(), city[2:].strip()
        except:
            item['birthday'], item['city'] = ('', '')
        # print(item)
        yield from item_pipeline(item)


@asyncio.coroutine
def item_pipeline(item):
    yield from sava_csv(item)
    yield from save_img(item['cover'], item['name'], )


@asyncio.coroutine
def sava_csv(item):
    print('保存文件')
    has_header = os.path.exists(csv_filepath)
    with open(csv_filepath, 'a', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=item.keys())
        if not has_header:
            writer.writeheader()

        writer.writerow(item)


@asyncio.coroutine
def save_img(url, name):
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        ext_name = '.jpg'
        type_ = resp.headers['content-type']
        ext_name = 'png' if type_.startswith('img/png') else '.jpg'
        with open(f'images/{name}{ext_name}', 'wb') as f:
            f.write(resp.content)


if __name__ == '__main__':
    # csv_filepath = sys.argv[1]
    csv_filepath = 'meinv.csv'

    loop = asyncio.get_event_loop()
    # 起始协程是单个
    # loop.run_until_complete(get(''))

    # 起始多个协程
    loop.run_until_complete(asyncio.wait((
        get('http://www.meinv.hk/?cat=1'),
        post('http://www.meinv.hk/wp-admin/admin-ajax.php'))
    ))
