import requests
import json
import re
import logging

def get_token():
    headers = {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    response = requests.post('https://api.twitter.com/1.1/guest/activate.json', headers=headers)
    logging.info(response.content.decode('utf-8'))
    guest_token = json.loads(response.content)['guest_token']
    return guest_token


def create_params(queries, cursor=None):
    params = [
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
        ('q', queries),
        ('tweet_search_mode', 'live'),
        ('count', '100'),
        ('query_source', 'typed_query'),
        ('pc', '1'),
        ('spelling_corrections', '1'),
        ('ext', 'mediaStats,highlightedLabel,cameraMoment'),
    ]
    if cursor:
        params.append(('cursor', cursor))
    logging.info(params)
    return params


def twitter_search(queries, cursor=None):
    params = create_params(queries, cursor)
    guest_token = get_token()
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
    find_cursor = re.compile(r':"(scroll:.*?)"')
    response = requests.get('https://api.twitter.com/2/search/adaptive.json', headers=headers,
                            params=params)
    logging.info(params)
    dict_data = json.loads(response.content)
    current_cursor = find_cursor.findall(response.content.decode('utf-8'))[0]
    return (current_cursor, dict_data)


def recursive_search(queries, cursor=None):
    res = twitter_search(queries, cursor)
    print(res[1]['globalObjects']['tweets'])

    recursive_search(queries, res[0])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    recursive_search('(맥도날드 OR 맥날 OR 빅맥)')
