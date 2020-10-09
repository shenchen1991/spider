import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

url = 'https://fanyi.baidu.com/sug'
headers = {
    'Cookies': 'REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BIDUPSID=3932C875425346E1184747ACDFD4220D; PSTM=1592296886; BAIDUID=3932C875425346E156F6E8AE2A87985B:FG=1; H_WISE_SIDS=154758_152477_151997_152353_150686_150076_147089_150087_148855_153684_147280_153629_153425_153438_152410_153243_153756_151017_153566_146574_127969_154413_153227_152902_146652_146732_131423_154563_154037_151148_107312_154190_152716_152408_153077_153502_144966_154167_154436_154212_154118_154903_153060_154146_147546_148868_153447_154361_151945_110085; MCITY=-%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=3vLOJeC62rVSKlcrqejEhrRkLkJtxwbTH6aokg__5p8DDaiv0U12EG0Pox8g0KubtwtCogKKKgOTHICF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJkfoIDhfIvbfP0khtnDMtA85h5Ka4CXa5rMVbbmHl7ketn4hUt50PKEhp5Datoy2TrNBhRjWhk2ep72QhrdQJtb2HbHJpKtQj5T-qu22bopsIJM557B-6KzyecBbPvqaKviaKJjBMb1MlvDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6o-jaAqt5ksbTrK3bvH-jrVHtoYhRbVq4tehHRe-lR9WDTm_Do52f5ZhI54KtooK-kX0xRrK5DtXbvq-pPKKRA5sR3XXno8MbkeqH33Qtkf3mkjbn7Gfn02OPKzBT0M544syPRiKMRnWg5mKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJDJCFhhItCjTtben-W5gTq24oQaPo2WbCQBpQv8pcNLTDK06ttKqCebJo-3N63QfooBpToVM5ahpO1j4_eXN0JJ-RbXK62BRohaqbDMp5jDh3r3jksD-Rtelvd55by0hvcWb3cShnVLUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDG08t6LDJJksLRrVabuVHnRY-P4_M43H-UnLq5JqBgOZ0l8Ktto4Vpv1-n5abtIkMh5NaM7WWjnOLbomWIQHDnvTBpPhK5kvQMQ0-jOPtRr4KKJxa-PWeIJo5t5M5n0dhUJiBMnMBan7alOIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TFMe5cy3D; delPer=0; PSINO=5; ZD_ENTRY=baidu; H_PS_PSSID=32809_32617_1456_32791_7545_32706_32230_7517_32116_26350_22159; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1599632114,1599699766,1600840619,1602055288; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1602055288; __yjsv5_shitong=1.0_7_3996623ca112eae82293288bd80e858b4549_300_1602055289466_115.236.71.68_573969e3; yjs_js_security_passport=c61572971e43bb00b9ead8cf7f93b5422706c6c3_1602055290_js',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}


def translate(kw):
    data = {
        'kw': kw
    }
    # data不为空则为post请求
    req = Request(url,
                  data=urlencode(data).encode('utf-8'))
    resp = urlopen(req)
    assert resp.code == 200

    json_data = resp.read()
    content_encode = resp.getheader('Content-type')
    content_encode = 'utf-8' if content_encode is None else content_encode.split('=')[-1]
    # print(content_encode)
    return json.loads(json_data.decode('utf-8'))


if __name__ == '__main__':
    print(translate('apple'))
