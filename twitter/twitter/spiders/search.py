# -*- coding: utf-8 -*-
import urllib
import pprint
import scrapy
import orjson
import json
import re


def get_params(query: str, cursor=None) -> str:
    params = [('skip_status', '1'), ('cards_platform', 'Web-12'), ('include_cards', '1'),
              ('include_composer_source', 'true'), ('include_ext_alt_text', 'true'), ('include_reply_count', '1'),
              ('tweet_mode', 'extended'), ('include_entities', 'true'), ('include_user_entities', 'true'),
              ('include_ext_media_color', 'true'), ('include_ext_media_availability', 'true'),
              ('send_error_codes', 'true'), ('simple_quoted_tweets', 'true'), ('q', query),
              ('tweet_search_mode', 'live'), ('count', '100'), ('query_source', 'typed_query'), ('pc', '1'),
              ('ext', 'mediaStats,highlightedLabel,cameraMoment')]
    if cursor is not None:
        params.append(cursor)
    return urllib.parse.urlencode(params)


class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['twitter.com']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        },
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'DOWNLOAD_DELAY': 0,
        'WAIT_FOR_SCALE': 1
    }
    handle_httpstatus_list = [400, 404, 429]
    guest_token = ""
    links = []
    cursor_finder = re.compile(r'cursor":{"value":"(scroll.*?)","cursorType":"Bottom"')
    page = 1

    def start_requests(self):
        '''
        :return: token 생성하는 url로 접속
        '''
        return [scrapy.Request('https://api.twitter.com/1.1/guest/activate.json', method='POST',
                               callback=self.after_getting_token)]

    def after_getting_token(self, response):
        """
        token 생성 후 페이지를 순회하며 전체 데이터 다운로드함
        :param response: json {globalObjects:{broadcasts:{},cards{}
        :return:
        """
        self.guest_token = json.loads(response.text)['guest_token']
        headers = {
            'authority': 'api.twitter.com',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'x-twitter-client-language': 'ko',
            'x-guest-token': self.guest_token,
            'x-csrf-token': '',
            'accept': '*/*',
            'origin': 'https://twitter.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://twitter.com/search?q=%EB%A7%A5%EB%8F%84%EB%82%A0%EB%93%9C',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        url = "https://api.twitter.com/2/search/adaptive.json?"
        url = url + get_params("맥도날드")
        return scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        page = orjson.loads(response.text)
        try:
            self.page += 1
            bottom_cursor = self.cursor_finder.findall(response.text)[0]
            print("현재 작업중인 페이지는 ", self.page, "번째 페이지 입니다.")
            print("*" * 10, bottom_cursor, "*" * 10)
        except Exception as E:
            print(E)
            bottom_cursor = None
        tweets = page['globalObjects']['tweets']
        users = page['globalObjects']['users']
        for tweet_id, tweet in tweets.items():
            api_url = f"https://api.twitter.com/2/timeline/conversation/{tweet_id}.json"
            web_url = f"https://twitter.com/{users[str(tweet['user_id'])]['screen_name']}/status/{tweet_id}"
            self.links.append((api_url, web_url))
        print(len(self.links))
        headers = {
            'authority': 'api.twitter.com',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'x-twitter-client-language': 'ko',
            'x-guest-token': self.guest_token,
            'accept': '*/*',
            'origin': 'https://twitter.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty'
        }
        if self.page >= 180:
            bottom_cursor = None
        if bottom_cursor is not None:
            url = "https://api.twitter.com/2/search/adaptive.json?"
            url = url + get_params("맥도날드", ("cursor", bottom_cursor))
            print(self.guest_token, url)
            return scrapy.Request(url, headers=headers, callback=self.parse)
        else:
            print(self.links)
            # return [scrapy.Request(url, headers=headers, callback=self.detail_parse) for url in self.links]

        # pprint.pprint(users)
        # print(bottom_cursor)
        # each tweet has a user_id
        # users[user_id]
        # globalObjects.users[user_id].screen_name

    def detail_parse(self, response):
        print(orjson.loads(response.text))
