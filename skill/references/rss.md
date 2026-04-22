# RSS / Atom 피드

> 인증 불필요. 뉴스/블로그/커뮤니티에서 가장 안정적인 보조 경로다.

## 없으면 설치하고 계속

```bash
python3 -c "import feedparser" 2>/dev/null || pip install feedparser -q
```

## 자동 발견

```bash
curl -sH "Accept: application/json" "https://r.jina.ai/https://example.com" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'].get('external',{}).get('alternate',[]))"
```

## URL 변형 탐색

```bash
curl -sL "{origin}/rss"
curl -sL "{origin}/feed"
curl -sL "{origin}/atom.xml"
curl -sL "{origin}/rss.xml"
curl -sL "{origin}/index.xml"
```

## Google News RSS

```bash
curl -sL "https://news.google.com/rss/search?q={검색어}&hl=ko&gl=KR&ceid=KR:ko"
```

## 한국 언론 RSS 예시

```bash
curl -sL "https://news.sbs.co.kr/news/rss.do"
curl -sL "https://www.hankyung.com/feed/all-news"
curl -sL "https://www.yonhapnewsagency.com/RSS/headline.xml"
```

## 블로그/플랫폼 RSS

```bash
curl -sL "https://rss.blog.naver.com/{BLOG_ID}.xml"
curl -sL "https://{blogname}.tistory.com/rss"
curl -sL "https://{publication}.substack.com/feed"
```
