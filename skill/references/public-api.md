# 공개 API 직접 호출

> 인증 없이 구조화 데이터를 주는 공개 API.

## Bluesky

```bash
curl -sL "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={handle}"
curl -sL "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor={handle}&limit=10"
```

## Mastodon

```bash
curl -sL "https://{instance}/api/v1/accounts/lookup?acct={username}"
curl -sL "https://{instance}/api/v1/accounts/{id}/statuses?limit=10"
```

## Stack Exchange

```bash
curl -sL "https://api.stackexchange.com/2.3/search?order=desc&sort=votes&intitle={query}&site=stackoverflow"
curl -sL "https://api.stackexchange.com/2.3/questions/{id}/answers?order=desc&sort=votes&site=stackoverflow&filter=withbody"
```

## arXiv

```bash
curl -sL "http://export.arxiv.org/api/query?search_query=ti:{query}&max_results=5&sortBy=submittedDate&sortOrder=descending"
```

## CrossRef

```bash
curl -sL "https://api.crossref.org/works?query={query}&rows=5&sort=relevance"
```

## OpenLibrary

```bash
curl -sL "https://openlibrary.org/search.json?q={query}&limit=5"
```

## Wayback Machine

```bash
curl -sL "https://archive.org/wayback/available?url={URL}"
curl -sL "https://web.archive.org/cdx/search/cdx?url={URL}&output=json&fl=timestamp,statuscode&limit=5"
```

## GitHub

gh가 있으면 우선 사용, 없으면 REST API.

```bash
curl -sL "https://api.github.com/search/repositories?q={query}&sort=stars&per_page=5"
```
