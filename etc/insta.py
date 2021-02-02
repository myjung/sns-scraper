import requests
import json
import re
import logging
import urllib
from pprint import pprint


def get_query_hash(query='인스타'):
    headers = {
        'authority': 'www.instagram.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    hash_pattern = re.compile(r'byTag.*?queryId:"(.*?)"')
    script_pattern = re.compile(r'href="(.*?\/TagPageContainer\.js.*?)"')
    base_url = 'https://www.instagram.com/explore/tags/'
    search_url = base_url + query + '/'
    logging.info(search_url)
    response = requests.get(search_url, headers=headers)
    script_url = "https://www.instagram.com" + script_pattern.findall(response.content.decode('utf-8'))[0]
    logging.info(script_url)
    response = requests.get(script_url, headers=headers)
    return hash_pattern.findall(response.content.decode('utf-8'))[0]


def create_params(query, query_hash, page=12, cursor=None):
    variables = {
        'tag_name': query,
        'first': page
    }
    if cursor:
        variables['after'] = cursor
    params = {
        'query_hash': query_hash,
        'variables': json.dumps(variables, ensure_ascii=False)
    }
    logging.info(params)
    return params


def get_first_page(query):
    base_url = 'https://www.instagram.com/explore/tags/'
    cursor_pattern = re.compile(r'.{0,2}end_cursor.{0,2}:(.*?)}')
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    }
    url = base_url + query + '/?__a=1'
    logging.info('search url is :\t' + url)
    response = requests.get(url, headers=headers)
    dict_data = json.loads(response.content)
    page_info = dict_data['graphql']['hashtag']['edge_hashtag_to_media']['page_info']
    if page_info['has_next_page'] is True:
        current_cursor = page_info['end_cursor']
    else:
        current_cursor = None
    return (current_cursor, dict_data)


def search_insta(query, query_hash, page=12, cursor=None):
    headers = {
        "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    }
    base_url = 'https://www.instagram.com/graphql/query/'
    params = create_params(query, query_hash, page, cursor)
    response = requests.get(base_url, headers=headers, params=params)
    logging.info(response.headers)
    dict_data = json.loads(response.content)
    page_info = dict_data['data']['hashtag']['edge_hashtag_to_media']['page_info']
    logging.info(page_info)
    if page_info['has_next_page'] is True:
        current_cursor = page_info['end_cursor']
    else:
        current_cursor = None
    return (current_cursor, dict_data)

def recursive_search(query, query_hash, page, cursor=None):
    res = search_insta(query, query_hash, page, cursor)
    print(res[1])
    logging.info(res[0])
    recursive_search(query, query_hash, page, res[0])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # print(get_query_hash('상수'))
    # print(get_query_hash('맥날'))
    # print(get_first_page('부산'))
    # print(create_params('맥날', 'asdasdasdasd', 'asdasdasdasd'))
    #print(search_insta('버거킹', get_query_hash()))
    recursive_search('맥도날드', get_query_hash(), 12)
