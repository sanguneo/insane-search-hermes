# 출처 메모

이 스킬은 다음 공개 저장소의 아이디어와 구조를 Hermes 도구 체계에 맞게 재구성한 것이다.
- https://github.com/fivetaku/insane-search

주요 차이점:
- Claude 전용 WebFetch/Playwright MCP 표기를 Hermes의 `web_extract`, `web_search`, `browser_*`, `browser_cdp`, `terminal` 기준으로 변경
- Hermes 세션에서 바로 쓸 수 있게 도구 선택 순서를 재정리
- 한국 사이트와 로컬 환경 보조 경로를 Hermes 관점으로 정리
