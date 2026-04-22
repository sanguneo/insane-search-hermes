# 접근 실패 시 — 적응형 스케줄러

> 인덱스 방법이 실패하거나 인덱스에 없는 사이트일 때 실행.
> Phase 0 → 1 → 2 → 3 순서로 에스컬레이션한다. 각 단계에서 성공하면 즉시 종료한다.

## 원칙

1. 어떤 방법도 미리 제외하지 않는다.
2. 의존성이 없으면 설치하고 시도한다.
3. Phase 전환은 실패 신호 기반으로 한다.
4. 결과 채택 기준: 정확성/신뢰도 > 신선도 > 완전성 > 구조화 > 비용.

## Phase 1: 경량 프로브 (병렬)

먼저 시도:
- `web_extract(URL)`
- Jina Reader 기본/JSON 모드
- `curl -L` + Chrome Desktop UA

추가 시도:
- 모바일 UA + 모바일 URL `m.{domain}`
- Googlebot UA
- URL 변형: `.json`, `/rss`, `/feed`
- archive.today / Wayback / AMP cache는 sidecar

모든 HTML 응답에서 메타데이터도 추출한다.

## 에스컬레이션 신호

Phase 1 → Phase 2:
- HTTP 403 / 430 / 429 / 503
- `cf-ray`, `server: cloudflare`, `x-datadome`
- `__cf_bm`, `_abck`, `datadome`
- `captcha`, `verify`, `enable javascript`, `check your browser`
- 200인데 본문 없이 SPA shell만 있음
- redirect loop 3회 이상

즉시 종료:
- `login`, `sign in`, `로그인`, `subscribe`, `member-only`, `구독`
- paywall이 명확하면 Phase 3까지 올려도 해결 안 될 수 있다

## Phase 2: TLS 임퍼소네이션

없으면 설치하고 계속:
```bash
python3 -c "import curl_cffi" 2>/dev/null || pip install curl_cffi -q
```

시도 순서:
- safari
- chrome
- firefox

추가 규칙:
- origin 홈으로 먼저 요청해 쿠키 워밍
- `Accept-Language`, `Referer`를 사이트/국가에 맞춤
- HTML을 얻으면 JSON-LD/OGP 즉시 추출
- `behavioral-content`, `sec-if-cpt` 같은 JS behavioral challenge면 Phase 3 직행

## Phase 3: Hermes browser/CDP

기본 순서:
1. `browser_navigate(URL)`
2. `browser_snapshot(full=true)` 또는 기본 snapshot
3. `browser_console(expression='document.body.innerText.slice(0,4000)')`
4. JSON-LD, `__NEXT_DATA__`, 네트워크 API 확인
5. CDP가 가능하면 `Target.getTargets`, `Runtime.evaluate` 보강

브라우저 단계의 목표:
- 실제 렌더링 본문 확보
- 숨은 XHR/fetch API 발견
- 로그인벽인지 실제 차단인지 판정

## 응답 검증

성공:
- 기사/블로그: 주제 관련 본문 500자 이상이거나 구조화 데이터 충분
- 상품: JSON-LD Product / ItemList 확보
- 짧은 포스트: 100자 이상 또는 전용 API 응답 확보
- 프로필: Person/Article/Feed 구조화 데이터 확보

부분 성공:
- OGP/JSON-LD만 확보
- 원문은 없지만 제목/요약/가격/프로필은 확보

실패:
- 인증 필요
- CAPTCHA 수동 개입 필요
- 지역 차단
- 챌린지/빈 쉘만 반복

## Sidecar 채택 규칙

원본 성공 응답이 있으면 sidecar는 참고만 한다.
원본 전부 실패 시에만 archive/wayback/AMP를 채택하고 provenance를 명시한다.
