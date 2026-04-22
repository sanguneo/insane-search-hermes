# 브라우저 에스컬레이션

## Hermes browser 우선 흐름
1. `browser_navigate(URL)`
2. `browser_snapshot(full=true)`
3. `browser_console(expression='document.body.innerText.slice(0,4000)')`
4. JSON-LD 추출
5. 필요시 `browser_cdp`로 탭/쿠키/런타임 평가

## 적극 탐색 포인트
- `document.querySelectorAll('script[type="application/ld+json"]')`
- `window.__NEXT_DATA__`
- `self.__next_f`
- XHR/fetch 응답
- 로그인폼 / paywall / challenge DOM 흔적

## 브라우저로도 안 되면
- 인증 필요 / CAPTCHA / 지역 차단을 명시
- archive/RSS/public API가 있으면 보조 경로로 전환
