from http.cookiejar import CookieJar
from urllib.parse import urlencode
from urllib.request import build_opener, HTTPHandler, HTTPCookieProcessor, ProxyHandler, Request

# 代理
opener = build_opener(HTTPHandler(),
                      HTTPCookieProcessor(CookieJar()),
                      ProxyHandler(proxies={
                          'http': 'http://118.190.199.163:8888'
                      }))
post_url = ''
data = {

}

headers = {

}

request = Request(post_url,
                  urlencode(data).encode('utf-8'),
                  headers)

resp = opener.open(request)
bytes_ = resp.read()
print(bytes_.decode())
