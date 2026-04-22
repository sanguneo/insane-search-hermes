[한국어](README.ko.md) | English

# insane-search-hermes

Hermes-oriented blocked-site retrieval skill inspired by `fivetaku/insane-search`.
This repository reorganizes the original ideas around Hermes-native tools such as `web_search`, `web_extract`, `terminal`, `browser_*`, and `browser_cdp`.

## What it does

- Escalates from lightweight extraction to stronger fallback methods
- Handles blocked or brittle sites such as X, Reddit, YouTube, Naver, LinkedIn, Coupang, Medium, and Substack
- Adds Korean and English trigger phrases for skill loading consideration
- Includes references for RSS, metadata extraction, browser escalation, and terminal probes

## Contents

Runnable helper scripts are also included.
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

## Install

### Auto
```bash
hermes skills install sanguneo/insane-search-hermes:skill/SKILL.md
```

### Manual
```bash
git clone https://github.com/sanguneo/insane-search-hermes.git
cp -R ./insane-search-hermes/skill ~/.hermes/skills/research/insane-search-hermes/
```

## Attribution

This repository was created with strong inspiration from:

- `fivetaku/insane-search`
- https://github.com/fivetaku/insane-search

It does not aim to be a verbatim mirror of the original project.
Instead, it adapts the blocked-site retrieval strategy, fallback structure, and platform-specific handling approach for Hermes Agent workflows.

## Router

- `skill/scripts/insane_router.py` classifies URL/handle/query input and automatically executes the first extraction path, escalating until success. Use `--plan-only` for dry-run output and `--run-all` to execute every candidate.

## Ready-to-use templates

- See `skill/references/command-templates.md` for copy-paste command templates.

## Publish readiness

- See `skill/references/publish-checklist.md` for the final pre-publish checklist.

## License

- MIT License
- See [LICENSE](./LICENSE)
