import json
import re
import time

import requests
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions

from utils.header import get_ua

headers = {
    'User-Agent': get_ua()
}

chrome = Chrome(executable_path='chromedriver.exe')


def get_all_city():
    url = 'https://www.zhaopin.com/citymap'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        html = resp.text
        s = re.search(r'<script>__INITIAL_STATE__=(.*?)</script>', html)
        json_data = s.groups()[0]
        data = json.loads(json_data)
        city_map_list = data['cityList']['cityMapList']
        for letter, cities in city_map_list.items():
            print(f'---{letter}-----')
            for city in cities:
                yield city

        # with open('city.html', 'w', encoding='utf-8') as f:
        #     f.write(html)


def get_city_jobs(url):
    chrome.get(url)

    # 查找警告信息的button
    # btn = chrome.find_element_by_css_selector('.risk-waring_content button')
    # btn.click()

    input_search: WebElement = chrome.find_element_by_class_name('zp-search__input')
    input_search.send_keys('Python')

    chrome.find_element_by_class_name('zp-search__btn').click()
    time.sleep(0.5)
    # 切换到浏览器第二个页签
    chrome.switch_to.window(chrome.window_handles[1])
    chrome.execute_script('var q=window.document.documentElement.scrollTop=1000')
    time.sleep(2)
    chrome.execute_script('var q=window.document.documentElement.scrollTop=2000')
    time.sleep(0.2)

    ui.WebDriverWait(chrome, 60).until(
        expected_conditions.visibility_of_all_elements_located((By.CLASS_NAME, 'contentpile__content')))

    no_content = chrome.find_element_by_class_name('contentpile__jobcontent__noimg')

    if not no_content:
        print('当前城市未找到python岗位')
    else:
        divs = chrome.find_elements_by_class_name('contentpile__content__wrapper')
        for div in divs:
            job_info_url = div.find_element(By.XPATH, './/a/@herf')


def get_city_jobs2(url):
    chrome.get(url)

    chrome.find_element_by_class_name('zp-search__btn').click()
    time.sleep(0.5)

    ui.WebDriverWait(chrome, 60).until(
        expected_conditions.visibility_of_all_elements_located((By.CLASS_NAME, 'contentpile__content')))

    no_content = chrome.find_element_by_class_name('contentpile__jobcontent__noimg')

    if not no_content:
        print('当前城市未找到python岗位')
    else:
        divs = chrome.find_elements_by_class_name('contentpile__content__wrapper')
        for div in divs:
            job_info_url = div.find_element(By.XPATH, './/a/@herf')
            print(job_info_url)


if __name__ == '__main__':
    query_cities = ('北京', '西安', '上海')
    for city in get_all_city():
        if city['name'] in query_cities:
            print(city)
            get_city_jobs('https:' + city['url'])
            # get_city_jobs2(f'https://sou.zhaopin.com/?jl={city["code"]}&kw=Python&kt=3')