import scrapy
from scrapy.http import JsonRequest
from scrapy.http import Response

'''
2020-05-07 10:20
description : 
https://api.twitter.com/1.1/guest/activate.json 로 post 메시지에 header에 authorization 토큰을 포함하여 보내면 
게스트 토큰을 반환함
-----------REQUEST---------------
curl -x localhost:8888 -X POST -H \
'authorization: Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA' \
-A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36' \
https://api.twitter.com/1.1/guest/activate.json
-----------RESPONSE-------------- 
response : json object {"guest_token" : "1258204706054127621"}
'''
'''
token 생성 이후 다음 내용을 헤더에 담아 uri에 param을 담아 get 방식으로 요청하면 json타입의 트위터 본문 데이터가 전송됨
        'authority': 'api.twitter.com',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'x-twitter-client-language': 'ko',
        'x-guest-token': guest_token,
        'x-csrf-token': '',
        'accept': '*/*',
        'origin': 'https://twitter.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://twitter.com/search?q=%EB%A7%A5%EB%8F%84%EB%82%A0%EB%93%9C',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
response : json object {}
'''


class SearchSpider(scrapy.Spider):
    name = 'Twitter Search'
    start_urls = ['https://api.twitter.com/1.1/guest/activate.json']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
        }
    }

    def parse(self, response):
        print(response)
        return

    def get_token(self):
        headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
        }
        url = 'https://api.twitter.com/1.1/guest/activate.json'
        yield JsonRequest(url=url, method='POST', headers=headers, callback=self.parse_token)

    def parse_token(self, response):
        print(response)


'''
        headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
        }
        url = 'https://api.twitter.com/1.1/guest/activate.json'
        JsonRequest(url=url, method='POST', headers=headers)
'''


def get_token():
    headers = {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    url = 'https://api.twitter.com/1.1/guest/activate.json'
    JsonRequest(url=url, method='POST', headers=headers)
    print(Response.status)
    print(Response)


def main():
    get_token()
