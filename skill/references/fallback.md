# 적응형 접근 순서

## Phase 0 — 특수 엔드포인트 우선
범용 HTML 추출보다 정확하고 싸다.

우선 대상:
- X/Twitter: syndication, oEmbed
- Reddit: `.json` + 모바일 UA
- Hacker News: Firebase API / Algolia
- Bluesky, Mastodon, Stack Exchange, arXiv, CrossRef, OpenLibrary, GitHub API
- RSS/Atom
- YouTube/미디어: `yt-dlp --dump-json`
- 네이버 검색/금융/블로그 모바일 URL

성공하면 종료.

## Phase 1 — 가벼운 프로브
1. `web_extract(URL)`
2. Jina Reader: `https://r.jina.ai/http://...` 또는 `https://r.jina.ai/https://...`
3. `curl -L` + Chrome 데스크톱 UA
4. 모바일 UA / `m.` 서브도메인 / `.json` / `/rss` / `/feed`
5. 아카이브/캐시를 참고 소스로만 확인

### Phase 1에서 바로 다음으로 올리는 신호
- 403 / 430 / 429 / 503
- `cf-ray`, `_abck`, `datadome`, `__cf_bm`
- `captcha`, `verify you are human`, `checking your browser`
- `sign in`, `subscribe`, `member-only`, `로그인`
- HTML은 왔지만 본문 없이 SPA 셸뿐

## Phase 2 — TLS 임퍼소네이션
`curl_cffi`를 설치해 실제 브라우저 TLS 핑거프린트를 흉내 낸다.

기본 순서:
- `safari`
- `chrome`
- `firefox`

추가 원칙:
- 첫 요청은 origin 홈으로 보내 쿠키 워밍
- `Accept-Language`, `Referer`를 지역/사이트에 맞춘다
- HTML을 얻으면 JSON-LD/OG 메타를 바로 추출한다

## Phase 3 — 브라우저/네트워크 관찰
Hermes browser 도구 사용:
- `browser_navigate`
- `browser_snapshot`
- `browser_console(expression=...)`
- 필요시 `browser_cdp(Target.getTargets / Runtime.evaluate / Network.getAllCookies)`

브라우저 단계에서 해야 할 것:
1. 실제 렌더링 본문 확인
2. 숨은 XHR/fetch API 찾기
3. JSON-LD / Next.js payload 추출
4. 로그인벽인지 진짜 차단인지 판정

## 판정 기준
- 성공: 주제 관련 본문이나 구조화 데이터 확보
- 부분 성공: OGP/JSON-LD만 확보
- 실패: 인증 필요 / CAPTCHA / 지역 차단 / 완전 차단

## 보고 방식
최종 답변에는 다음을 짧게 적는다.
- 어떤 경로가 먹혔는지
- 본문인지 메타데이터인지
- 한계가 무엇인지
