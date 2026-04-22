[English](#english) | [한국어](#한국어)

# insane-search-hermes

Hermes Agent용 blocked-site retrieval 스킬입니다.
원본인 fivetaku/insane-search의 아이디어를 참고해서, Hermes의 `web_search`, `web_extract`, `terminal`, `browser_*`, `browser_cdp` 흐름에 맞게 다시 정리한 버전입니다.

## 한국어

> 웹이 막혀도 쉽게 포기하지 않는 Hermes용 검색/추출 스킬

`403`, WAF, CAPTCHA, 빈 SPA, 로그인 벽처럼 일반 추출이 자주 실패하는 상황에서,
Hermes가 단계적으로 더 강한 접근 방법을 고를 수 있게 정리한 스킬입니다.

주요 특징
- Hermes 네이티브 도구 우선 사용
  - `web_search`
  - `web_extract`
  - `terminal`
  - `browser_*`
  - `browser_cdp`
- 차단 신호 기반 Phase 에스컬레이션
- X, Reddit, YouTube, Naver, LinkedIn, Coupang, Medium, Substack 등 대응
- 한국어 트리거 문구 추가
- 메타데이터(JSON-LD/OGP), RSS, 미디어 추출까지 포함

포함 내용
- `skill/SKILL.md`
- `skill/references/fallback.md`
- `skill/references/special-endpoints.md`
- `skill/references/korea.md`
- `skill/references/media.md`
- `skill/references/browser-escalation.md`
- `skill/references/metadata.md`
- `skill/references/terminal-http.md`
- `skill/references/source-note.md`

설치
```bash
mkdir -p ~/.hermes/skills/research/insane-search-hermes
cp -R skill/* ~/.hermes/skills/research/insane-search-hermes/
```

이 스킬이 다루는 문제 예시
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

## 샤라웃 / Attribution

큰 방향과 문제 정의는 아래 원본 레포에서 많은 영감을 받았습니다.

- fivetaku/insane-search
- https://github.com/fivetaku/insane-search

특히 아래 관점을 참고했습니다.
- 차단된 사이트를 미리 포기하지 않는 접근
- 공개 API / RSS / yt-dlp / Jina / TLS impersonation / 브라우저 fallback 계층화
- 한국 사이트와 특수 플랫폼을 따로 다루는 방식

이 저장소는 원본을 그대로 복제한 것이 아니라,
Hermes Agent 환경에 맞게 구조와 설명, 도구 선택 순서를 다시 구성한 adaptation입니다.

## 라이선스

이 저장소는 MIT License로 배포합니다.
자세한 내용은 [LICENSE](./LICENSE)를 참고하세요.

원본 레포인 `fivetaku/insane-search` 역시 MIT License를 사용하며,
원본 아이디어와 참고 출처는 위 Attribution 섹션에 명시했습니다.

---

## English

Hermes-oriented blocked-site retrieval skill inspired by `fivetaku/insane-search`.
It reorganizes the original idea around Hermes-native tools such as `web_search`, `web_extract`, `terminal`, `browser_*`, and `browser_cdp`.

What it does
- Escalates from lightweight extraction to stronger fallback methods
- Handles blocked or brittle sites such as X, Reddit, YouTube, Naver, LinkedIn, Coupang, Medium, and Substack
- Adds Korean and English trigger phrases
- Includes references for RSS, metadata extraction, browser escalation, and terminal probes

Install
```bash
mkdir -p ~/.hermes/skills/research/insane-search-hermes
cp -R skill/* ~/.hermes/skills/research/insane-search-hermes/
```

Attribution
- Inspired by `fivetaku/insane-search`
- Source: https://github.com/fivetaku/insane-search

This repository is an adaptation for Hermes workflows, not a verbatim mirror of the original project.

License
- MIT License
- See [LICENSE](./LICENSE)
