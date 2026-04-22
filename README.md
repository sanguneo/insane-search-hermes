# insane-search-hermes

Hermes Agent skill adapted from fivetaku/insane-search.

Purpose
- Improve blocked-site retrieval in Hermes
- Add trigger phrases for automatic skill loading consideration
- Prefer Hermes-native tools first: web_search, web_extract, terminal, browser_*, browser_cdp

Contents
- `skill/SKILL.md`
- `skill/references/*.md`

Install
```bash
mkdir -p ~/.hermes/skills/research/insane-search-hermes
cp -R skill/* ~/.hermes/skills/research/insane-search-hermes/
```

Source inspiration
- https://github.com/fivetaku/insane-search

Notes
- This repository is an adaptation for Hermes workflows, not a verbatim mirror.
