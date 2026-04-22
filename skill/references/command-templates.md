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
python3 scripts/jina_fetch.py 'https://example.com/article'
```

## 8) Reddit JSON

```bash
python3 scripts/reddit_json.py 'https://www.reddit.com/r/LocalLLaMA/comments/abc123/example/'
```

## 9) Hacker News top/search

```bash
python3 scripts/hn_fetch.py --limit 10
python3 scripts/hn_fetch.py --query 'claude code'
```

## 10) Wayback lookup

```bash
python3 scripts/wayback_lookup.py 'https://example.com/article'
```

## 11) Bluesky profile/feed

```bash
python3 scripts/bluesky_fetch.py 'bsky.app'
python3 scripts/bluesky_fetch.py 'bsky.app' --feed --limit 5
```

## 12) Router

```bash
python3 scripts/insane_router.py 'https://example.com/article'
python3 scripts/insane_router.py '@openclaw'
python3 scripts/insane_router.py '클로드 코드 뉴스'
```
