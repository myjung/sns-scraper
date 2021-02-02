import requests
import json

cookies = {
    'PHPSESSID': '0cc9c3a18f6fb42a8d567fd418000c10',
    'ci_c': '350963c2b37003cd4a41b1bb5cc5d27e',
    '__utma': '118540316.110983585.1588138745.1588138745.1588138745.1',
    '__utmc': '118540316',
    '__utmz': '118540316.1588138745.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '__utmt': '1',
    'alarm_popup': '1',
    'ck_lately_gall': '3b',
    'trc_cookie_storage': 'taboola%2520global%253Auser-id%3D6b0c21d4-797f-4bf1-b2fa-4312c28b048f-tuct5a298ab',
    'gallRecom': 'MjAyMC0wNC0yOSAxNDo0MDoyNS9mMGMzOTIxMGViOTBlZGRjZWJjYmZkMTU3ODBlYmEyMjA2MTJjM2Q0YjBiZmExZjkzNjI0M2E2ZDU2MjI3Yjlh',
    'service_code': '21ac6d96ad152e8f15a05b7350a2475909d19bcedeba9d4face8115e9bc2f74283d44d8d37a28f2620857c758a4e146d74a56c2e1c66ae73d5a14fc58fe88991d5171f1d4f422d6228669754704c5f84d3fc825c015fb3e01745d48cfaf78208af6f929a8acc1ce3e9c11b525a26497806ff51c7aa4d631a2b2aa3d1350d7f0501065f2f965d9f14f76d0e1045fcbf20b06f665bfdd3c11acf2aa5756ad4c3058babc27bafae5ff50b8697749477119a9fcb7412e74b2715b133cbd49b0c9f177f09656f245494c6',
    'wcs_bt': 'f92eaecbc22aac:1588138826',
    '__utmb': '118540316.14.10.1588138745',
    'last_alarm': '1588138827',
    'movie26342225_Firstcheck': 'Y',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://gall.dcinside.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://gall.dcinside.com/board/view/?id=movie2&no=6342225&page=1',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

data = {
  'ci_t': '350963c2b37003cd4a41b1bb5cc5d27e',
  'id': 'movie2',
  'no': '6342225',
  'mode': 'U',
  'code_recommend': 'undefined'
}

response = requests.post('https://gall.dcinside.com/board/recommend/vote', headers=headers, data=data, cookies=cookies)
print(response.content.decode('utf-8'))