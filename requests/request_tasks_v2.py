"""
多任务
"""
import uuid

from threading import Thread
from multiprocessing import Queue, Process
from queue import Queue as TQueue
import requests
from lxml import etree

from utils.header import get_ua

headers = {
    'User-Agent': get_ua()
}


class DownloadThread(Thread):
    def __init__(self, task_queue, result_queue):
        super().__init__()
        self.task_queue: TQueue = task_queue
        self.result_queue: Queue = result_queue

    def run(self):
        while True:
            try:
                url = self.task_queue.get(timeout=10)
                content = self.get(url)
                self.result_queue.put((url, content))
            except:
                break

    def get(self, url):
        print('开始下载', url)
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
        print('完成下载', url)
        return resp.text


class DownloadProcess(Process):
    def __init__(self, url_q, html_q):
        super(DownloadProcess, self).__init__()
        self.url_q: Queue = url_q
        self.html_q: Queue = html_q
        self.task_queue = None

    def run(self):
        self.task_queue = TQueue()
        ts = [DownloadThread(self.task_queue, self.html_q)
              for i in range(2)]
        for t in ts:
            t.start()
        while True:
            try:
                url = self.url_q.get(timeout=30)
                # 启动子线程下载任务
                self.task_queue.put(url)
            except:
                print('异常')
                break
        for t in ts:
            t.join()
        print('下载进程over')


class ParseThread(Thread):
    def __init__(self, html, url_q, parent_url):
        super(ParseThread, self).__init__()
        self.html = html
        self.url_q: Queue = url_q
        self.parent_url = parent_url

    def run(self):
        root = etree.HTML(self.html)
        images = root.xpath('//div[contains(@class,"picblock")]//img')

        item = {}
        for image in images:
            item['id'] = uuid.uuid4().hex
            item['name'] = image.xpath('./@alt')[0]
            try:
                item['cover'] = image.xpath('./@src2')[0]
            except:
                item['cover'] = image.xpath('./@src')[0]
            print(item)

        # 获取下一页的链接
        next_page = root.xpath('//a[@class="nextpage"]/@href')
        if next_page:
            next_url = self.parent_url + next_page[0]
            self.url_q.put(next_url)


class ParseProcess(Process):
    def __init__(self, url_q, html_q):
        super(ParseProcess, self).__init__()
        self.url_q: Queue = url_q
        self.html_q: Queue = html_q

    def run(self):
        while True:
            try:
                url, html = self.html_q.get(timeout=30)
                # 启动子线程下载任务
                parent_url = url[:url.rindex('/') + 1]
                ParseThread(html, self.url_q, parent_url).start()

            except:
                print('异常')
                break
        print('解析进程over')


if __name__ == '__main__':
    task1 = Queue()  # 下载任务队列
    task2 = Queue()  # 解析任务队列

    task1.put('http://sc.chinaz.com/tupian/cixiutuan.html')
    p1 = DownloadProcess(task1, task2)
    p2 = ParseProcess(task1, task2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
