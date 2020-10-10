import json
import time

import requests
from bs4 import BeautifulSoup, Tag

from utils.header import get_ua

headers = {
    'User-Agent': get_ua()
}


def get(url):
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        parse(resp.text)


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
        print(item)

        # 加载下一页
    post('http://www.meinv.hk/wp-admin/admin-ajax.php')


page = 2


def post(url):
    time.sleep(1)
    global page
    print(page)
    resp = requests.post(url, data={
        'total': 36,
        'action': 'fa_load_postlist',
        'paged': page,
        'category': 1,
        'wowDelay': '0.3s',
    }, headers=headers)
    page += 1
    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        result = json.loads(resp.text)
        parse(result['postlist'])



def item_pipeline(item):
    pass


if __name__ == '__main__':
    get('http://www.meinv.hk/?cat=1')
