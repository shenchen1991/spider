import ssl
from urllib.parse import quote
from urllib.request import urlopen, Request, urlretrieve


def search_baidu(wd='千峰'):
    url = 'https://www.baidu.com/s?wd=%s'

    request = Request(url % quote(wd),
                      headers={
                          'Cookies': 'BD_UPN=12314753; BIDUPSID=3932C875425346E1184747ACDFD4220D; PSTM=1592296886; BAIDUID=3932C875425346E156F6E8AE2A87985B:FG=1; H_WISE_SIDS=154758_152477_151997_152353_150686_150076_147089_150087_148855_153684_147280_153629_153425_153438_152410_153243_153756_151017_153566_146574_127969_154413_153227_152902_146652_146732_131423_154563_154037_151148_107312_154190_152716_152408_153077_153502_144966_154167_154436_154212_154118_154903_153060_154146_147546_148868_153447_154361_151945_110085; ispeed_lsm=0; MCITY=-%3A; sug=3; sugstore=0; ORIGIN=0; bdime=0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; BD_CK_SAM=1; PSINO=5; BD_HOME=1; H_PS_PSSID=32809_32617_1456_32791_7545_32706_32230_7517_32116_26350_22159; H_PS_645EC=d7dbyl0FuZ9Lfg%2Fzmizmm%2B18T%2FhpN1YPnURtP0EkOsbc6RKgrswXGv9HHgw; BDSVRTM=126; COOKIE_SESSION=853_0_9_9_22_31_1_4_9_5_11_0_0_0_4_0_1601773602_0_1602033649%7C9%232159880_6_1601259138%7C3; WWW_ST=1602034379129',
                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                        'like Gecko) Chrome/85.0.4183.121 Safari/537.36'
                      })
    response = urlopen(request)
    assert response.code == 200
    print('请求成功')

    # 读取响应数据
    bytes_ = response.read()
    with open('%s.html' % wd, 'wb') as file:
        file.write(bytes_)


def download_img(url):
    filename = url[url.rfind('/') + 1:]
    urlretrieve(url, filename)


if __name__ == '__main__':
    search_baidu()
    download_img('https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=570576571,581499736&fm=26&gp=0.jpg')
