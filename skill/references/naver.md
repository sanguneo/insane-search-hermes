# 네이버 계열 접근 전략

## 네이버 블로그

모바일 URL + iPhone UA 우선.

```bash
curl -sL   -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"   -H "Accept-Language: ko-KR,ko;q=0.9"   -H "Referer: https://m.naver.com/"   "https://m.blog.naver.com/PostView.naver?blogId={ID}&logNo={NO}"
```

RSS:
```bash
curl -sL "https://rss.blog.naver.com/{BLOG_ID}.xml"
```

## 네이버 검색

curl_cffi 세션으로 쿠키 워밍 후 접근.

```python
from curl_cffi import requests
from urllib.parse import quote
s = requests.Session(impersonate='chrome')
s.headers.update({'Accept-Language':'ko-KR,ko;q=0.9','Referer':'https://www.google.com/'})
s.get('https://www.naver.com/', timeout=10)
s.headers['Referer'] = 'https://www.naver.com/'
r = s.get(f"https://search.naver.com/search.naver?where=news&query={quote('검색어')}")
```

핵심 탭:
- 통합 검색
- `where=post`
- `where=news`

## 네이버 뉴스 / 증권

Jina로 먼저 시도, 실패하면 browser로.

```bash
curl -s "https://r.jina.ai/https://n.news.naver.com/article/{press_id}/{article_id}"
curl -s "https://r.jina.ai/https://finance.naver.com/item/main.naver?code=005930"
```

## 네이버 금융 시세

```bash
curl -sL "https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20240101&endTime=20241231&timeframe=day"
```

## 네이버 카페

로그인+iframe 장벽이 강해 인증 필요로 끝날 가능성이 높다.
