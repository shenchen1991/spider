import os
import re

import requests

from utils.header import get_ua

base_url = 'http://sc.chinaz.com/tupian/'
url = 'http://sc.chinaz.com/tupian/'

if os.path.exists('mn.html'):
    with open('mn.html', encoding='utf-8') as f:
        html = f.read()
else:
    resp = requests.get(url, headers={
        'User_Agent': get_ua()
    })
    resp.encoding = 'utf-8'
    assert resp.status_code == 200
    html = resp.text
    with open('mn.html', 'w', encoding=resp.encoding) as f:
        f.write(html)

compile = re.compile(r'<img src2="(.*?) alt="(.*?)">')
images = compile.findall(html)
# print(images)
next_url = re.findall(r'<b>2221</b></a><a href="(.*?)" class="nextpage', html,re.S)
print(base_url + next_url[0])


