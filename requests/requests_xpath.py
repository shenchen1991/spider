from lxml import etree

import requests
from requests import Response


class RequestError(Exception):
    pass


def get(url):
    resp: Response = requests.get(url,
                                  headers={
                                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'},
                                  proxies={'http': 'http://36.248.133.209:9999'})
    if resp.status_code == 200:
        print(resp.text)
        parse(resp.text)
    else:
        raise RequestError('失败')


def parse(html):
    root = etree.HTML(html)
    divs = root.xpath('//div[@class="li-itemmod"]')
    for div in divs:
        cover_url = div.xpath('.//img/@src')[0]
        title = div.xpath('.//h3/a/text()')[0]
        print(cover_url, title)


if __name__ == '__main__':
    get('https://hangzhou.anjuke.com/community/?from=esf_list_navigation')
