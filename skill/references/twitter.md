# X/Twitter 접근 전략

> 일반 HTML 추출은 자주 막힌다. 공개 엔드포인트를 우선 사용한다.

## 키워드 검색

먼저 URL을 확보한다.
- `web_search(query="site:x.com {검색어}")`
- 필요시 일반 검색엔진 또는 네이버 검색과 조합

## 타임라인 — Syndication API

```bash
curl -sL "https://syndication.twitter.com/srv/timeline-profile/screen-name/{handle}"
```

핵심 데이터:
- `full_text`
- `favorite_count`
- `retweet_count`
- `created_at`
- `id_str`

## 개별 포스트 — oEmbed

```bash
curl -sL "https://publish.twitter.com/oembed?url=https://x.com/{user}/status/{tweet_id}"
```

## 조합 패턴
1. `web_search(site:x.com {query})`
2. 포스트 URL 확보
3. oEmbed로 전문 확보

## 실패 패턴
- SPA 셸만 나오는 200 OK
- `Sign in to X`만 보임
- `hasResults: false`

이 경우 타임라인/검색/oEmbed 조합으로 우회한다.
