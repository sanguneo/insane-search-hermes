[English](README.md) | 한국어

# insane-search-hermes

Hermes Agent용 blocked-site retrieval 스킬입니다.
원본인 `fivetaku/insane-search`의 아이디어를 참고해서,
Hermes의 `web_search`, `web_extract`, `terminal`, `browser_*`, `browser_cdp` 흐름에 맞게 다시 정리한 버전입니다.

## 소개

> 웹이 막혀도 쉽게 포기하지 않는 Hermes용 검색/추출 스킬

`403`, WAF, CAPTCHA, 빈 SPA, 로그인 벽처럼 일반 추출이 자주 실패하는 상황에서,
Hermes가 단계적으로 더 강한 접근 방법을 고를 수 있게 정리한 스킬입니다.

## 주요 특징

- Hermes 네이티브 도구 우선 사용
  - `web_search`
  - `web_extract`
  - `terminal`
  - `browser_*`
  - `browser_cdp`
- 차단 신호 기반 Phase 에스컬레이션
- X, Reddit, YouTube, Naver, LinkedIn, Coupang, Medium, Substack 등 대응
- 한국어/영어 트리거 문구 추가
- 메타데이터(JSON-LD/OGP), RSS, 미디어 추출까지 포함

## 포함 내용

실행형 스크립트도 포함됩니다.
- `skill/scripts/fetch_with_cffi.py`
- `skill/scripts/extract_metadata.py`
- `skill/scripts/naver_search.py`
- `skill/scripts/twitter_oembed.py`
- `skill/scripts/rss_discover.py`
- `skill/scripts/jina_fetch.py`
- `skill/scripts/reddit_json.py`
- `skill/scripts/hn_fetch.py`
- `skill/scripts/wayback_lookup.py`
- `skill/scripts/bluesky_fetch.py`
- `skill/scripts/insane_router.py`


- `skill/SKILL.md`
- `skill/references/fallback.md`
- `skill/references/special-endpoints.md`
- `skill/references/korea.md`
- `skill/references/media.md`
- `skill/references/browser-escalation.md`
- `skill/references/metadata.md`
- `skill/references/terminal-http.md`
- `skill/references/source-note.md`

## 설치

```bash
mkdir -p ~/.hermes/skills/research/insane-search-hermes
cp -R skill/* ~/.hermes/skills/research/insane-search-hermes/
```

## 이 스킬이 다루는 문제 예시

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

## 원본 참고

이 저장소는 아래 원본 레포의 문제의식과 접근 방식을 많이 참고했습니다.

- `fivetaku/insane-search`
- https://github.com/fivetaku/insane-search

특히 아래 관점을 참고했습니다.

- 차단된 사이트를 미리 포기하지 않는 접근
- 공개 API / RSS / yt-dlp / Jina / TLS impersonation / 브라우저 fallback 계층화
- 한국 사이트와 특수 플랫폼을 따로 다루는 방식

이 저장소는 원본을 그대로 복제한 것이 아니라,
Hermes Agent 환경에 맞게 구조와 설명, 도구 선택 순서를 다시 구성한 adaptation입니다.

## Router

- `skill/scripts/insane_router.py`가 URL/핸들/키워드를 분류하고 실제 스크립트를 자동 실행합니다. `--plan-only`로 계획만, `--run-all`로 전체 후보를 순차 실행할 수 있습니다.

## 바로 쓰는 템플릿

- `skill/references/command-templates.md`에 복붙용 명령 템플릿을 추가했습니다.

## 배포 전 점검

- `skill/references/publish-checklist.md`에 배포 전 최종 체크리스트를 추가했습니다.

## 라이선스

이 저장소는 MIT License로 배포합니다.
자세한 내용은 [LICENSE](./LICENSE)를 참고하세요.
