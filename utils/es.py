from urllib.parse import quote

import requests

INDEX_HOST = '127.0.0.1'
INDEX_PORT = 9200


class ESIndex:
    def __init__(self, index_name, doc_type):
        self.index_name = index_name
        self.doc_type = doc_type

    def create(self):  # 创建索引库
        url = f'http://{INDEX_HOST}:{INDEX_PORT}/{self.index_name}'
        json_data = {
            "settings": {
                "number_of_shards": 5,
                "number_of_replicas": 1
            }
        }
        resp = requests.put(url, json=json_data)
        if resp.status_code == 200:
            print('创建成功')
            print(resp.json())

    def delete(self):  # 删除索引库
        resp = requests.delete(f'http://{INDEX_HOST}:{INDEX_PORT}/{self.index_name}')
        if resp.status_code == 200:
            print('删除索引成功')

    def add_doc(self, item: dict):  # 向库增加文档
        doc_id = item.pop('id', None)
        url = f'http://{INDEX_HOST}:{INDEX_PORT}/{self.index_name}/{self.doc_type}/'
        if doc_id:
            url += str(doc_id)
        resp = requests.post(url, json=item)
        if resp.status_code == 200:
            print(f'{url} 文档新增成功')

    def remove_doc(self, doc_id):  # 删除库文档
        url = f'http://{INDEX_HOST}:{INDEX_PORT}/{self.index_name}/{self.doc_type}/{doc_id}'
        resp = requests.delete(url)
        if resp.status_code == 200:
            print(f'{url} 文档删除成功')

    def update_doc(self, item: dict):  # 向库增加文档
        doc_id = item.pop('id')
        url = f'http://{INDEX_HOST}:{INDEX_PORT}/{self.index_name}/{self.doc_type}/{doc_id}'
        resp = requests.put(url, json=item)
        if resp.status_code == 200:
            print(f'{url} 文档更新成功')

    def query(self, wd=None):  # 查询库
        q = quote(wd) if wd else ''
        url = f'http://{INDEX_HOST}:{INDEX_PORT}/{self.index_name}/_search?size=100'
        if q:
            url += f'&q={q}'
        print(url)
        resp = requests.get(url)
        datas = []
        if resp.status_code == 200:
            ret = resp.json()
            hits = ret['hits']['hits']
            if hits:
                for item in hits:
                    data = item['_source']
                    data['id'] = item['_id']
                    datas.append(data)
        return datas


if __name__ == '__main__':
    index = ESIndex('gushiwen', 'tuijian')
    index.create()
    index.add_doc({
        'id': 1,
        'name': 'disen',
        'price': 19.5
    })
    index.add_doc({
        'id': 2,
        'name': 'disen2',
        'price': 39.5
    })

    print(index.query())
