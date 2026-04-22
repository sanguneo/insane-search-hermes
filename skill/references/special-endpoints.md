# 플랫폼별 우선 경로

## X / Twitter
- 키워드 검색: 검색으로 포스트 URL 확보 후 oEmbed
- 타임라인: `https://syndication.twitter.com/srv/timeline-profile/screen-name/{handle}`
- 개별 포스트: `https://publish.twitter.com/oembed?url=https://x.com/{user}/status/{id}`

## Reddit
모바일 UA로 `.json` 사용.

예시:
```bash
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15'
curl -sL -H "User-Agent: $UA" "https://www.reddit.com/r/LocalLLaMA/hot.json?limit=10"
```

## Hacker News
- `https://hacker-news.firebaseio.com/v0/topstories.json`
- `https://hacker-news.firebaseio.com/v0/item/{id}.json`
- 검색은 Algolia: `https://hn.algolia.com/api/v1/search?query=...`

## Bluesky / Mastodon / Stack Overflow
공개 API 우선. HTML보다 안정적이다.

## GitHub
- 가능하면 `gh` CLI
- 없으면 GitHub REST API

## arXiv / CrossRef / OpenLibrary / Wikipedia
공식 공개 API 우선.

## RSS / Atom
다음 후보를 빠르게 시도:
- `/rss`
- `/feed`
- `/atom.xml`
- `/rss.xml`
- `/index.xml`

## Jina Reader
공개 URL 본문 정리에 강하다.
- 기본: `curl -s "https://r.jina.ai/https://example.com"`
- JSON: `Accept: application/json`

## 아카이브
원문 실패 시만 보조 출처로 사용.
- Wayback Machine
- archive.today 계열
- AMP cache
