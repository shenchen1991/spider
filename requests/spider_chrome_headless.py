import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions

from selenium import webdriver


def parse_data(flag=False):
    chrome.execute_script('var q=window.document.documentElement.scrollTop=5000')
    posts = chrome.find_elements(By.CLASS_NAME, 's_post')
    if flag:
        posts = posts[1:]
    for post in posts:
        a = post.find_element(By.CSS_SELECTOR, '.p_title a')
        url = a.get_attribute('href')
        title = a.text
        print(url, title)
    chrome.find_element(By.CLASS_NAME, 'next').click()
    time.sleep(1)
    parse_data()


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # options.binary_location = r'D:\pyWorkSpace\spider\requests\chromedriver.exe'
    # chrome = webdriver.Chrome(chrome_options=options, executable_path=r'D:\pyWorkSpace\spider\requests\chromedriver.exe')
    chrome = Chrome(chrome_options=options, executable_path=r'D:\pyWorkSpace\spider\requests\chromedriver.exe')
    chrome.get('https://tieba.baidu.com/')
    chrome.maximize_window()
    chrome.find_element(By.ID, 'wd1').send_keys('Python')
    chrome.find_element(By.CLASS_NAME, 'j_search_post').click()
    time.sleep(1)
    parse_data(True)
    chrome.save_screenshot('tieba.png')
    chrome.close()
