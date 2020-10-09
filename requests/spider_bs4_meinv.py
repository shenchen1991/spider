import requests

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
    print(html)
    with open('meinv.html', 'w', encoding='utf-8') as file:
        file.write(html)


def item_pipeline(item):
    pass
