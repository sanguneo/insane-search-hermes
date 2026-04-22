# 플랫폼별 우선 경로

## X / Twitter
- timeline: syndication
- single post: oEmbed
- keyword search: 검색 → 포스트 URL → oEmbed

## Reddit
- `.json` + Mobile UA

## Hacker News
- Firebase API
- Algolia Search

## Bluesky / Mastodon / Stack Overflow
- 공개 API 우선

## GitHub / arXiv / CrossRef / OpenLibrary / Wikipedia
- 공개 API 우선

## RSS / Atom
- `/rss`, `/feed`, `/atom.xml`, `/rss.xml`, `/index.xml`

## Jina Reader
- 본문 정리용 우선 fallback

## archive / wayback / AMP
- 원문 실패 시에만 채택
