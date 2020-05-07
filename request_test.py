import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup
import re


def get():
    url = 'https://twitter.com/search'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    params = (
        ('q', '맥도날드'.encode('utf-8')),
        ('f', 'live'),
    )
    response = requests.get(url=url, headers=headers, params=params)
    bs = BeautifulSoup(response.content, features='lxml')
    script_list = bs.find_all('script')
    js_list = []
    for script in script_list:
        src = script.get_attribute_list('src')[0]
        if src:
            js_list.append(src)
    # id_pattern = re.compile('"guestId":"(.*?)"')
    # guest_id = id_pattern.findall(script_list[0].string)[0] 스크립트에서 반환되는 guest_id를 정규식으로 가져옴
    # auth_token = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
    headers = {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'}
    response = requests.post('https://api.twitter.com/1.1/guest/activate.json', headers=headers)
    guest_token = json.loads(response.content)['guest_token']
    headers = {
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
        ('count', '100'),
        ('query_source', 'typed_query'),
        ('pc', '1'),
        ('spelling_corrections', '1'),
        ('ext', 'mediaStats,highlightedLabel,cameraMoment'),
    )
    response = requests.get('https://api.twitter.com/2/search/adaptive.json', headers=headers, params=params)
    print(response.content.decode('utf-8'))
    content = json.loads(response.content)
    #pprint(content['globalObjects']['tweets'])
    #print(len(content['globalObjects']['tweets']))
    #print(content)

get()

'''
headers = {
    'authority': 'api.twitter.com',
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'x-twitter-client-language': 'ko',
    'x-guest-token': '1254600316881784832',
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
    ('q', '\uB9E5\uB3C4\uB0A0\uB4DC'),
    ('count', '20'),
    ('tweet_search_mode', 'live'),
    #('cursor', 'refresh:thGAVUV0VFVBaAwKe9iN6F5CIWgsCjkYCepeQiEjUAFQAlABEViPl5FYCJehgETkVXUxUAFQAA')
)

response = requests.get('https://api.twitter.com/2/search/adaptive.json', headers=headers, params=params)
content = json.loads(response.content)
#pprint(content)
#pprint(content['globalObjects']['tweets'])

for each in content['globalObjects']['tweets']:
    print(content['globalObjects']['tweets'][each])
print(len(content['globalObjects']['tweets']))
'''
'''
#pprint()
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://api.twitter.com/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_composer_source=true&include_ext_alt_text=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweets=true&q=%EB%A7%A5%EB%8F%84%EB%82%A0%EB%93%9C&count=20&query_source=&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2CcameraMoment', headers=headers)
'''

