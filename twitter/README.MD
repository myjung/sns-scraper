# twitter spider 개요

### 1. TOKEN 생성

#### 요청 URL >>> https://api.twitter.com/1.1/guest/activate.json

#### 요청 방식 : POST

#### 요청시 필요 정보
1. 헤더
```
{'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}
```

#### CURL 요청 정보
```
curl -X POST -H \
'authorization: Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA' \
-A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36' \
https://api.twitter.com/1.1/guest/activate.json
```

#### 응답 정보 : JSON
    {"guest_token" : "1258204706054127621"}

---
### 2. SEARCH
#### 요청 URL >>> https://api.twitter.com/2/search/adaptive.json
#### 요청 방식 : GET
#### 요청시 필요 정보
1. 헤더 (guest_token 주의)
```
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
```

2. URI PARAMETERS (q파라미터가 검색어, cursor가 페이지 기준)

queries의 경우 '(맥도날드 OR 맥날 OR 빅맥)'형태로 OR 및 AND 조건 사용 가능함
```
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
이후 페이지는 앞 페이지 데이터의 cursor위치를 삽입하면 됨
    (cursor, '#ASDASDASDASD')
```