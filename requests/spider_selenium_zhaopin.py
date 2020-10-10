import json
import re

import requests

from utils.header import get_ua

headers = {
    'User-Agent': get_ua()
}


def get_all_city():
    url = 'https://www.zhaopin.com/citymap'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        html = resp.text
        s = re.search(r'<script>__INITIAL_STATE__=(.*?)</script>', html)
        json_data = s.group()[0]
        print(s.group())
        data = json.loads(json_data)
        city_map_list = data['cityList']
        for letter, cities in city_map_list.items():
            print(f'---{letter}-----')
            for city in cities:
                yield city

        # with open('city.html', 'w', encoding='utf-8') as f:
        #     f.write(html)


if __name__ == '__main__':
    for city in get_all_city():
        print(city)
