# Command templates

실전에서 바로 복붙할 수 있는 명령 템플릿 모음.

## 1) curl_cffi로 URL 본문 시도

```bash
python3 scripts/fetch_with_cffi.py 'https://example.com/article'
```

## 2) HTML에서 OGP / JSON-LD 추출

```bash
python3 scripts/extract_metadata.py /tmp/example-page.html
python3 scripts/extract_metadata.py 'https://example.com/article'
```

## 3) 네이버 뉴스 / 블로그 검색

```bash
python3 scripts/naver_search.py '클로드 코드' --where news
python3 scripts/naver_search.py '클로드 코드' --where post
```

## 4) X 포스트 oEmbed

```bash
python3 scripts/twitter_oembed.py 'https://x.com/openclaw/status/1234567890'
```

## 5) RSS/Atom 자동 탐색

```bash
python3 scripts/rss_discover.py 'https://example.com'
```

## 6) yt-dlp 메타데이터

```bash
yt-dlp --dump-json 'https://www.youtube.com/watch?v=VIDEO_ID'
```

## 7) Jina Reader

```bash
curl -s 'https://r.jina.ai/https://example.com/article'
```

## 8) Reddit JSON

```bash
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15'
curl -sL -H "User-Agent: $UA" 'https://www.reddit.com/r/LocalLLaMA/hot.json?limit=10'
```
