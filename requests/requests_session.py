import requests
from requests import Response

from utils.chaojiying import rec_code
from utils.header import get_ua

session = requests.session()


def down_code():
    resp = session.get('https://so.gushiwen.cn/RandCode.ashx',
                       headers={'User-Agent': get_ua()})
    with open('code.png', 'wb') as f:
        f.write(resp.content)


def get_code_str():
    down_code()
    return rec_code('code.png')


def login():
    resp: Response = session.post('https://so.gushiwen.cn/user/login.aspx',
                                  data={
                                      'email': '',
                                      'pwd': '',
                                      'code': get_code_str(),
                                  })
    if resp.status_code == 200:
        collect()
    else:
        print('-' * 30)
        print(resp.text)


def collect():
    resp: Response = session.get('http://so.gushiwen.cn/user/collect.aspx')
    print(resp.text)
    return resp.text


if __name__ == '__main__':
    login()
