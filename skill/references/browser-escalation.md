# 브라우저 에스컬레이션

## Hermes browser 우선 흐름
1. `browser_navigate(URL)`
2. `browser_snapshot(full=true)` 또는 기본 스냅샷
3. `browser_console(expression='document.body.innerText.slice(0,4000)')`
4. JSON-LD 추출:
   `browser_console(expression='[...document.querySelectorAll("script[type=\"application/ld+json\"]")].map(x=>x.textContent)')`

## CDP 보강
CDP가 연결되어 있으면:
- `Target.getTargets` 로 탭 찾기
- `Runtime.evaluate` 로 더 긴 JS 실행
- `Network.getAllCookies` 로 세션 상태 확인

## 브라우저 단계에서 확인할 것
- 본문이 실제 렌더링되는가
- 내부 XHR/fetch API가 있는가
- 로그인/유료벽인가
- 클라이언트 렌더링 데이터(`__NEXT_DATA__`, `__NUXT__`, JSON-LD)가 있는가

## 브라우저로도 안 되면
- 인증 필요면 그대로 보고
- CAPTCHA면 수동 개입 없이는 제한적이라고 알린다
- 이미 아카이브나 RSS가 있으면 보조 출처로 사용한다
