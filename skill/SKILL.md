---
name: insane-search-hermes
description: >
  Auto-bypass for blocked websites in Hermes — tries every method until one works.
  Use when web_extract/web_search fail, when pages return 403/429/blocked/login shells,
  or when accessing X/Twitter, Reddit, YouTube, GitHub, Mastodon, Medium, Substack,
  Stack Overflow, Threads, Naver, Coupang, LinkedIn, or other WAF/bot-protected sites.
  Leverages yt-dlp (1,858 media sites), Jina Reader, public APIs (HN, Bluesky, arXiv),
  RSS/Atom, curl_cffi TLS impersonation with auto-install guidance, and Hermes browser/CDP fallback.
  Korean triggers: 트위터/X 못 열어, 레딧 안 읽혀, 유튜브 자막 뽑아줘, 깃헙 검색,
  사이트 차단됨, 스레드 안 열려, 마스토돈, 미디엄, 서브스택, 스택오버플로우,
  네이버 블로그, 디시인사이드, 에펨코리아, 요즘IT, 긱뉴스, 클리앙, 쿠팡, 링크드인,
  당근마켓. English triggers: twitter access, reddit blocked, youtube subtitles,
  github search, arxiv papers, threads, mastodon, medium, substack, stackoverflow,
  naver blog, dcinside, fmkorea, coupang, linkedin, yozm, wishket.
  Do NOT trigger for simple web searches that web_search can handle directly.
version: 1.5.0
metadata:
  hermes:
    tags: [research, web, scraping, blocked-sites, jina, curl_cffi, browser, naver, reddit, twitter, rss]
    homepage: https://github.com/fivetaku/insane-search
    source_adaptation: Adapted for Hermes Agent from fivetaku/insane-search
---

# Insane Search for Hermes

> URL 접근이 차단될 때, 플랫폼별 최적 방법을 Hermes 도구 체계로 공격적으로 안내한다.

원본 `fivetaku/insane-search`의 의도와 커버리지를 최대한 유지하되,
Claude Code 전용 표기를 Hermes의 `web_search`, `web_extract`, `terminal`, `browser_*`, `browser_cdp` 기준으로 치환했다.

## 의도 분류 (Phase 0 진입 전)

| 사용자 입력 | 경로 |
|------------|------|
| URL 제공 (`https://...`) | → Phase 0~3 직접 접근 |
| 핸들 제공 (`@username`) | → Phase 0 syndication/API |
| 키워드만 (`X에서 AI 검색`) | → `web_search(site:{domain} {keyword})` 또는 네이버/RSS 검색 → URL 확보 후 Phase 0~3 |

> 한국어 신규 콘텐츠는 일반 웹검색 인덱싱이 느릴 수 있다. URL을 직접 받으면 가장 강하고, 키워드만 있으면 네이버 검색/RSS를 적극 고려한다.

## 원칙

1. 어떤 방법도 미리 제외하지 않는다.
2. 의존성이 없으면 설치하고 계속 간다.
3. 실패 신호 기반으로 더 강한 단계로 즉시 올린다.
4. HTML을 얻으면 OGP/JSON-LD/구조화 데이터도 같이 본다.
5. 원본 성공본이 있으면 캐시/아카이브는 참고만 쓴다.
6. login/paywall은 우회 성공처럼 말하지 않는다.

## Phase 0 — 특수 엔드포인트 인덱스

범용 체인으로 자동 발견하기 어려운 전용 API/CLI만 둔다.
없는 사이트는 Phase 1부터 자동 시도한다.

### 소셜/커뮤니티 전용 API

| 플랫폼 | 방법 | 상세 |
|--------|------|------|
| X/Twitter | syndication + oEmbed + 키워드 검색은 검색→oEmbed | [twitter.md](references/twitter.md) |
| Reddit | URL + `.json` + Mobile UA | [json-api.md](references/json-api.md) |
| Bluesky | AT Protocol | [public-api.md](references/public-api.md) |
| Mastodon | 인스턴스별 공개 API | [public-api.md](references/public-api.md) |
| Hacker News | Firebase API + Algolia Search | [json-api.md](references/json-api.md) |
| Stack Overflow | Stack Exchange API v2.3 | [public-api.md](references/public-api.md) |
| Lobste.rs / V2EX / dev.to | 공개 JSON API | [json-api.md](references/json-api.md) |

### 미디어

| 플랫폼 | 방법 | 상세 |
|--------|------|------|
| YouTube/Vimeo/Twitch/TikTok/SoundCloud 등 | `yt-dlp --dump-json` | [media.md](references/media.md) |

### 학술/레지스트리

| 플랫폼 | 방법 | 상세 |
|--------|------|------|
| arXiv | Atom API | [public-api.md](references/public-api.md) |
| CrossRef | REST API | [public-api.md](references/public-api.md) |
| Wikipedia | REST API | [json-api.md](references/json-api.md) |
| OpenLibrary | JSON API | [public-api.md](references/public-api.md) |
| GitHub | REST API / gh CLI | [public-api.md](references/public-api.md) |
| npm / PyPI | Registry API | [json-api.md](references/json-api.md) |
| Wayback Machine | CDX API | [public-api.md](references/public-api.md) |

### 한국 전용

| 플랫폼 | 방법 | 상세 |
|--------|------|------|
| 네이버 검색 | curl_cffi 신원위장 + `search.naver.com` | [naver.md](references/naver.md) |
| 네이버 금융 시세 | `api.finance.naver.com/siseJson.naver` | [naver.md](references/naver.md) |
| 한국 언론/블로그 | RSS/Atom, Jina, 모바일 URL | [rss.md](references/rss.md), [naver.md](references/naver.md) |

## 접근 순서 — 적응형 스케줄러

```
Phase 0: 특수 엔드포인트 — 있으면 먼저 시도
  ↓ 실패 또는 인덱스에 없음
Phase 1: 경량 프로브 — web_extract + Jina + curl UA/URL 변형
  ↓ 403/WAF/챌린지/빈 SPA 감지
Phase 2: TLS 임퍼소네이션 — curl_cffi (설치 후 safari→chrome→firefox)
  ↓ TLS 우회도 실패 또는 JS 챌린지
Phase 3: Hermes browser/CDP — 실제 브라우저 + 숨은 API 탐색
  ↓ login/paywall 감지
종료: 인증 필요 / 지역 차단 / CAPTCHA 수동개입 필요

사이드카: 캐시/아카이브 (원본이 실패할 때만 채택)
```

상세:
- [fallback.md](references/fallback.md)
- [terminal-http.md](references/terminal-http.md)
- [browser-escalation.md](references/browser-escalation.md)

## 빠른 참조

```bash
# Jina Reader
curl -s "https://r.jina.ai/https://example.com"

# 미디어 메타데이터
yt-dlp --dump-json "URL"

# Reddit
curl -sL -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15" "https://www.reddit.com/r/{sub}/hot.json?limit=10"

# X/Twitter timeline
curl -sL "https://syndication.twitter.com/srv/timeline-profile/screen-name/{handle}"

# Hacker News
curl -sL "https://hacker-news.firebaseio.com/v0/topstories.json?limitToFirst=10&orderBy=%22%24key%22"

# YouTube subtitles
yt-dlp --write-sub --write-auto-sub --sub-lang "en,ko" --skip-download -o "/tmp/%(id)s" "URL"
```

## 트리거 문구

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
- 스레드 안 열려
- 디시인사이드 / 에펨코리아 / 요즘IT / 긱뉴스 / 클리앙 긁어줘

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
- naver blog blocked
- read threads post

## 핵심 레퍼런스
- [fallback.md](references/fallback.md)
- [json-api.md](references/json-api.md)
- [public-api.md](references/public-api.md)
- [twitter.md](references/twitter.md)
- [naver.md](references/naver.md)
- [rss.md](references/rss.md)
- [media.md](references/media.md)
- [metadata.md](references/metadata.md)
- [browser-escalation.md](references/browser-escalation.md)
- [terminal-http.md](references/terminal-http.md)


## 실행 스크립트

다음 스크립트는 실전 재사용을 위한 실행형 보조 도구다.

- `scripts/fetch_with_cffi.py` — curl_cffi 자동설치 후 TLS impersonation 시도
- `scripts/extract_metadata.py` — OGP/JSON-LD/Next.js payload 추출
- `scripts/naver_search.py` — 네이버 검색 결과 HTML 확보
- `scripts/twitter_oembed.py` — X 개별 포스트 oEmbed 추출
- `scripts/rss_discover.py` — RSS/Atom 후보 자동 탐색 및 파싱
- `scripts/jina_fetch.py` — Jina Reader 본문 추출
- `scripts/reddit_json.py` — Reddit JSON 접근
- `scripts/hn_fetch.py` — Hacker News top/search
- `scripts/wayback_lookup.py` — Wayback snapshot 탐색
- `scripts/bluesky_fetch.py` — Bluesky profile/feed 접근
- `scripts/insane_router.py` — 입력 유형별 자동 실행/자동 승격 라우터

## 명령 템플릿

바로 복붙해서 쓸 템플릿은 [command-templates.md](references/command-templates.md)를 본다.

## 배포 전 점검

skills hub 배포 전 마지막 점검은 [publish-checklist.md](references/publish-checklist.md)를 본다.


## Router 설계

`insane_router.py`는 입력(URL/핸들/키워드)을 분류한 뒤 실제 스크립트를 자동 실행하고, 첫 성공까지 단계적으로 승격한다. `--plan-only`로 계획만 볼 수 있고, `--run-all`로 모든 후보를 순차 실행할 수 있다. 브라우저 단계는 외부 스크립트 안에서 직접 제어하지 않고, JSON 출력에 browser escalation plan을 포함해 Hermes browser/browser_cdp 에스컬레이션을 바로 이어서 쓸 수 있게 한다.
