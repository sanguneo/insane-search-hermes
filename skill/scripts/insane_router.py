#!/usr/bin/env python3
"""Best-effort router for insane-search-hermes.

Classifies input and prints a plan: which method to try first, next fallbacks,
and runnable commands using the bundled scripts.
"""
import argparse
import json
import re
from urllib.parse import urlparse


def classify(text: str):
    if text.startswith('http://') or text.startswith('https://'):
        host = urlparse(text).netloc.lower()
        return {'kind': 'url', 'host': host}
    if text.startswith('@'):
        return {'kind': 'handle', 'host': None}
    return {'kind': 'query', 'host': None}


def plan_for_url(url: str, host: str):
    cmds = []
    notes = []
    if 'x.com' in host or 'twitter.com' in host:
        cmds.append(f"python3 scripts/twitter_oembed.py '{url}'")
        notes.append('If this is not a single post or oEmbed fails, search for related post URLs first.')
    elif 'reddit.com' in host:
        cmds.append(f"python3 scripts/reddit_json.py '{url}'")
    elif 'youtube.com' in host or 'youtu.be' in host:
        cmds.append(f"yt-dlp --dump-json '{url}'")
    elif 'news.ycombinator.com' in host or 'hn.algolia.com' in host:
        cmds.append("python3 scripts/hn_fetch.py --limit 10")
    elif 'naver.com' in host:
        cmds.append(f"python3 scripts/fetch_with_cffi.py '{url}'")
        cmds.append(f"python3 scripts/extract_metadata.py '{url}'")
    else:
        cmds.append(f"python3 scripts/jina_fetch.py '{url}'")
        cmds.append(f"python3 scripts/fetch_with_cffi.py '{url}'")
        cmds.append(f"python3 scripts/extract_metadata.py '{url}'")
        cmds.append(f"python3 scripts/wayback_lookup.py '{url}'")
    return cmds, notes


def plan_for_handle(handle: str):
    normalized = handle.lstrip('@')
    cmds = [
        f"python3 scripts/bluesky_fetch.py '{normalized}'",
        f"curl -sL 'https://syndication.twitter.com/srv/timeline-profile/screen-name/{normalized}'",
    ]
    notes = ['Decide platform from context. X/Twitter handle and Bluesky handle may differ.']
    return cmds, notes


def plan_for_query(query: str):
    cmds = [
        f"python3 scripts/naver_search.py '{query}' --where news",
        f"python3 scripts/naver_search.py '{query}' --where post",
        f"python3 scripts/hn_fetch.py --query '{query}'",
    ]
    if re.search(r'\b(arxiv|paper|논문)\b', query, re.I):
        cmds.append(f"curl -sL 'http://export.arxiv.org/api/query?search_query=all:{query}&max_results=5&sortBy=submittedDate&sortOrder=descending'")
    notes = ['Use search to discover URLs, then rerun insane_router.py with a concrete URL for deeper extraction.']
    return cmds, notes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    cls = classify(args.input)
    if cls['kind'] == 'url':
        commands, notes = plan_for_url(args.input, cls['host'])
    elif cls['kind'] == 'handle':
        commands, notes = plan_for_handle(args.input)
    else:
        commands, notes = plan_for_query(args.input)
    print(json.dumps({'classification': cls, 'commands': commands, 'notes': notes}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
