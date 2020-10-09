import requests
from requests import Response

url = 'https://hangzhou.anjuke.com/community/'


def download(url: str) -> str:
    resp: Response = requests.get(url, params={'from': 'esf_list_navigation'})
    if resp.status_code == 200:
        return resp.text
    return '下载失败'


def get_douban_json():
    url = 'https://movie.douban.com/j/chart/top_list'
    data = {
        'start': 0,
        'limit': 20,
        'type': 5,
        'interval_id': '100:90'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }

    resp: Response = requests.get(url, params=data, headers=headers)
    assert resp.status_code == 200
    if 'application/json' in resp.headers['Content-Type']:
        return resp.json()
    return resp.text


# result = download(url)
result = get_douban_json()
print(result)

