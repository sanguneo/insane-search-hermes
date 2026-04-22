# 한국 사이트 대응

## 네이버 블로그
데스크톱보다 모바일 URL이 잘 열린다.

```bash
curl -sL \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15" \
  -H "Accept-Language: ko-KR,ko;q=0.9" \
  -H "Referer: https://m.naver.com/" \
  "https://m.blog.naver.com/PostView.naver?blogId={ID}&logNo={NO}"
```

RSS:
```bash
curl -sL "https://rss.blog.naver.com/{BLOG_ID}.xml"
```

## 네이버 검색
한국어 최신 콘텐츠 탐색에 강하다.

`curl_cffi` 세션으로:
1. `https://www.naver.com/` 쿠키 워밍
2. `search.naver.com/search.naver?query=...`
3. `where=post`, `where=news` 탭 직접 접근

## 네이버 뉴스 / 증권
Jina로 먼저 확인하고, 안 되면 browser 단계로 올린다.

## 한국 커뮤니티
- 클리앙, 루리웹, 브런치, 일부 뉴스: Jina가 잘 먹힘
- 디시인사이드, 에펨코리아, 쿠팡: curl/Jina가 약하면 Phase 2로 바로 올린다
- 요즘IT, 일부 CloudFront 계열: Chrome UA나 browser가 더 잘 먹힐 수 있다

## 검색 전략 팁
- 한국어 최신 이슈: RSS 또는 네이버 검색 우선
- 이미 URL이 있으면 검색보다 직접 추출 우선
- 쇼핑/가격 비교는 JSON-LD가 있는지 먼저 본다
