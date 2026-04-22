# Source note

이 스킬은 다음 공개 저장소의 문제의식과 커버리지를 Hermes 도구 체계에 맞게 재구성한 것이다.
- https://github.com/fivetaku/insane-search

차이점:
- Claude Code 전용 WebFetch/Playwright MCP 표기를 Hermes `web_search`, `web_extract`, `terminal`, `browser_*`, `browser_cdp` 기준으로 변경
- Hermes 세션에서 바로 쓸 수 있게 도구 우선순위와 fallback 흐름을 재정리
- 원본의 “없으면 설치하고 계속 간다” 원칙을 Hermes 문서에도 반영
