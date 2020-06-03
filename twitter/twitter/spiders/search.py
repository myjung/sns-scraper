# -*- coding: utf-8 -*-
import urllib
import pprint
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
        'DOWNLOAD_DELAY': 3,
        'WAIT_FOR_SCALE': 1
    }
    handle_httpstatus_list = [400, 404]

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
        headers = {
            'authority': 'api.twitter.com',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'x-twitter-client-language': 'ko',
            'x-guest-token': json.loads(response.text)['guest_token'],
            'x-csrf-token': '',
            'accept': '*/*',
            'origin': 'https://twitter.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://twitter.com/search?q=%EB%A7%A5%EB%8F%84%EB%82%A0%EB%93%9C',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        params = (
            ('include_profile_interstitial_type', '1'),
            ('include_blocking', '1'),
            ('include_blocked_by', '1'),
            ('include_followed_by', '1'),
            ('include_want_retweets', '1'),
            ('include_mute_edge', '1'),
            ('include_can_dm', '1'),
            ('include_can_media_tag', '1'),
            ('skip_status', '1'),
            ('cards_platform', 'Web-12'),
            ('include_cards', '1'),
            ('include_composer_source', 'true'),
            ('include_ext_alt_text', 'true'),
            ('include_reply_count', '1'),
            ('tweet_mode', 'extended'),
            ('include_entities', 'true'),
            ('include_user_entities', 'true'),
            ('include_ext_media_color', 'true'),
            ('include_ext_media_availability', 'true'),
            ('send_error_codes', 'true'),
            ('simple_quoted_tweets', 'true'),
            ('q', '\uB9E5\uB3C4\uB0A0\uB4DC'),
            ('tweet_search_mode', 'live'),
            ('count', '20'),
            ('query_source', 'typed_query'),
            ('pc', '1'),
            ('spelling_corrections', '1'),
            ('ext', 'mediaStats,highlightedLabel,cameraMoment'),
        )
        url = "https://api.twitter.com/2/search/adaptive.json?"
        url = url + urllib.parse.urlencode(params)
        return scrapy.Request(url, headers=headers, callback=self.parse)

    def search(self, token, page):
        pass

    def parse(self, response):
        print(json.dumps(json.loads(response.text), indent=2))
