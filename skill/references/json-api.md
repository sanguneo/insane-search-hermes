# JSON API 직접 호출

> URL 변형이나 공개 엔드포인트로 구조화된 JSON을 직접 가져오는 패턴.
> Jina보다 빠르고 구조가 좋아 우선 선택할 때가 많다.

## Reddit

Mobile User-Agent 필수.

```bash
UA="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"

curl -sL -H "User-Agent: $UA" "https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
curl -sL -H "User-Agent: $UA" "https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=1"
curl -sL -H "User-Agent: $UA" "https://www.reddit.com/r/{subreddit}/comments/{post_id}/{slug}/.json"
```

## Hacker News

```bash
curl -sL "https://hacker-news.firebaseio.com/v0/topstories.json?limitToFirst=10&orderBy=%22%24key%22"
curl -sL "https://hacker-news.firebaseio.com/v0/item/{id}.json"
curl -sL "https://hn.algolia.com/api/v1/search?query={query}"
```

## Lobste.rs

```bash
curl -sL "https://lobste.rs/hottest.json"
curl -sL "https://lobste.rs/t/ai.json"
curl -sL "https://lobste.rs/s/{short_id}.json"
```

## dev.to

```bash
curl -sL "https://dev.to/api/articles?tag=ai&per_page=5"
curl -sL "https://dev.to/api/articles?top=7&per_page=5"
```

## npm

```bash
curl -sL "https://registry.npmjs.org/{package}/latest"
curl -sL "https://registry.npmjs.org/-/v1/search?text={query}&size=5"
```

## PyPI

```bash
curl -sL "https://pypi.org/pypi/{package}/json"
```

## Wikipedia

```bash
curl -sL "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
curl -sL "https://ko.wikipedia.org/api/rest_v1/page/summary/{title}"
```

## V2EX

```bash
curl -sL "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: insane-search-hermes/1.0"
```
