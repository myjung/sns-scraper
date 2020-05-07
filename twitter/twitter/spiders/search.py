# -*- coding: utf-8 -*-
import scrapy
import json


class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['twitter.com']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        },
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'DOWNLOAD_DELAY': 2
    }
    handle_httpstatus_list = [400,404]
    def start_requests(self):
        '''
        :return: token 생성하는 url로 접속
        '''
        return [scrapy.FormRequest('https://api.twitter.com/1.1/guest/activate.json', method='POST', callback=self.after_getting_token)]

    def after_getting_token(self, response):
        '''
        token 생성 후 페이지를 순회하며 전체 데이터 다운로드함
        :param response: json {globalObjects:{broadcasts:{},cards{}
        :return:
        '''
        json_response = json.loads(response.body)
        token = json_response('guest_token')
        print(token)
        return
    def search(self, token, page):
        pass
    def parse(self, response):
        jsonresponse = json.loads(response.body)
        print("**********************")
        print("**********************")
        print("**********************")
        print(jsonresponse)
        print("**********************")
        print("**********************")
        print("**********************")
        print("**********************")
