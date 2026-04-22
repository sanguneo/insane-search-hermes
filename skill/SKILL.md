---
name: insane-search-hermes
description: Adaptive blocked-site retrieval workflow for Hermes. Use when web_search/web_extract fail, pages return 403/429/WAF/login shells, or when retrieving content from X, Reddit, YouTube, Naver, LinkedIn, Coupang, Medium, Substack, or other heavily scripted sites. Prefers Hermes web tools first, then terminal HTTP probes, public endpoints, TLS impersonation with curl_cffi, and finally browser/CDP escalation.
version: 1.0.0
metadata:
  hermes:
    tags: [research, web, scraping, blocked-sites, jina, curl_cffi, browser, naver]
    homepage: https://github.com/fivetaku/insane-search
    source_adaptation: Adapted for Hermes Agent from fivetaku/insane-search
---

# Insane Search for Hermes

웹 접근이 막히거나 기본 웹 도구가 빈약한 결과를 줄 때 쓰는 Hermes용 검색/추출 스킬입니다.

원본 아이디어는 fivetaku/insane-search이고, 여기서는 Claude 전용 흐름을 Hermes 도구 기준으로 다시 정리했습니다.

## 언제 쓰나
- `web_extract`가 실패하거나 빈 요약만 반환할 때
- `web_search`/`web_extract`만으로 최신 콘텐츠를 못 찾을 때
- 403, 429, Cloudflare, Akamai, DataDome, CAPTCHA, JS shell, login wall에 걸릴 때
- X, Reddit, YouTube, Medium, Substack, LinkedIn, Naver, Coupang, 한국 커뮤니티처럼 일반 추출이 자주 깨지는 사이트를 다룰 때
- URL 직접 접근뿐 아니라 키워드 검색 후 본문 추출까지 이어져야 할 때

## 트리거 문구
다음 표현이 들어오면 이 스킬을 우선 고려한다.

### 한국어
- 사이트 차단됨
- 접근이 안 됨
- 본문이 안 열림
- 403 / 429 / 캡차 / 로그인벽
- X 못 읽음 / 트위터 못 봄
- 레딧 본문 가져와줘
- 유튜브 자막 뽑아줘
- 네이버 블로그 읽어줘
- 쿠팡 상품 정보 긁어와줘
- 링크드인 글 내용 보여줘
- 한국 뉴스 최신 글 찾아줘

### English
- blocked site
- 403 forbidden
- captcha wall
- login wall
- read this X post
- fetch reddit comments
- extract youtube transcript
- scrape coupang
- read linkedin article
- summarize medium post

## 핵심 원칙
1. 쉬운 방법을 먼저 쓴다.
2. 사이트를 미리 포기하지 않는다.
3. 실패 신호가 보이면 더 강한 방법으로 바로 올린다.
4. HTML을 얻으면 항상 메타데이터도 같이 확인한다.
5. 로그인/유료벽이면 우회 가능 여부를 솔직하게 구분한다.

## 기본 라우팅
- URL이 이미 있으면: Phase 0~3 직접 접근
- 핸들만 있으면: 플랫폼 전용 공개 엔드포인트 우선
- 키워드만 있으면: `web_search` 또는 로컬/터미널 검색으로 URL 확보 후 접근
- 한국어 최신 콘텐츠면: 일반 검색보다 네이버 검색/RSS를 우선 고려

## Phase 개요
- Phase 0: 특수 엔드포인트 / 공개 API / RSS / yt-dlp
- Phase 1: Hermes 웹 도구 + Jina + curl UA/URL 변형
- Phase 2: `curl_cffi` TLS 임퍼소네이션 + 신원 위장
- Phase 3: Hermes browser/CDP로 실제 브라우저 렌더링 및 숨은 API 탐색

## 빠른 선택표
- 기사/블로그: `web_extract` → Jina → curl HTML + JSON-LD → browser
- SNS/X/Reddit: 공개 엔드포인트나 JSON API 우선
- 영상/오디오: `yt-dlp --dump-json` 또는 자막 추출
- 한국 뉴스/블로그: 네이버 검색, 모바일 URL, RSS, Jina 우선
- 쇼핑/프로필/SPA: JSON-LD와 browser 네트워크 관찰 우선

## 반드시 확인할 실패 신호
- 403 / 430 / 429 / 503
- `cf-ray`, `__cf_bm`, `_abck`, `datadome`
- `captcha`, `verify you are human`, `enable javascript`
- 본문 없이 앱 셸만 있는 SPA
- `sign in`, `login`, `구독`, `member-only`

## 실행 순서
1. `web_extract` 또는 `web_search`로 먼저 확인한다.
2. 실패하면 [special-endpoints.md](references/special-endpoints.md)에서 플랫폼별 우선 경로를 본다.
3. 그래도 안 되면 [fallback.md](references/fallback.md) 순서대로 올린다.
4. HTML을 얻는 모든 단계에서 [metadata.md](references/metadata.md)도 같이 적용한다.
5. 한국 사이트면 [korea.md](references/korea.md)를 먼저 참고한다.
6. 미디어면 [media.md](references/media.md)로 바로 간다.
7. JS/WAF면 [browser-escalation.md](references/browser-escalation.md)로 올린다.

## Hermes 맞춤 포인트
- `web_extract` / `web_search`가 되면 가장 먼저 쓴다.
- 웹 도구가 막히면 `terminal`로 `curl`, `python3`, `yt-dlp`를 사용한다.
- 브라우저가 필요하면 `browser_navigate`, `browser_snapshot`, `browser_console`을 우선 사용한다.
- CDP가 연결돼 있으면 `browser_cdp`로 탭/쿠키/런타임 평가를 보강한다.
- 이 환경처럼 로컬 SearxNG나 Chrome CDP가 있으면 보조 경로로 활용 가능하다.

## 출력 규칙
- 어떤 경로로 얻었는지 명시한다: 공식 API / 본문 추출 / 메타데이터 / 아카이브 / 브라우저 렌더링
- 부분 성공이면 본문인지 메타데이터만인지 구분한다.
- 인증 필요/지역 차단은 우회 성공처럼 말하지 않는다.
