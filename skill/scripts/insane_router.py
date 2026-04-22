#!/usr/bin/env python3
"""Automatic best-effort router for insane-search-hermes.

Classifies input and tries increasingly stronger methods until one succeeds.
Outputs JSON containing the executed attempts, heuristic success judgement,
and the best result found so far.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote, urlparse

SCRIPT_DIR = Path(__file__).resolve().parent


def classify(text: str):
    if text.startswith('http://') or text.startswith('https://'):
        host = urlparse(text).netloc.lower()
        return {'kind': 'url', 'host': host}
    if text.startswith('@'):
        return {'kind': 'handle', 'host': None}
    return {'kind': 'query', 'host': None}


def run_command(command):
    proc = subprocess.run(command, capture_output=True, text=True)
    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()
    parsed = None
    if stdout:
        try:
            parsed = json.loads(stdout)
        except Exception:
            parsed = None
    return {
        'command': ' '.join(command),
        'exit_code': proc.returncode,
        'stdout': stdout[:50000],
        'stderr': stderr[:12000],
        'parsed': parsed,
    }


def text_has_success_signal(text: str):
    lowered = text.lower()
    bad_markers = [
        'captcha', 'verify you are human', 'enable javascript', 'checking your browser',
        'sign in', 'login', 'member-only', 'subscribe', 'access denied', 'forbidden',
    ]
    if any(marker in lowered for marker in bad_markers):
        return False
    return len(text.strip()) >= 200


def evaluate_attempt(label, result):
    parsed = result.get('parsed')
    stdout = result.get('stdout', '')
    exit_code = result.get('exit_code', 1)

    success = False
    reason = 'no useful output'
    summary = None

    if exit_code != 0:
        reason = 'command failed'
        return {'label': label, 'success': False, 'reason': reason, 'summary': summary, 'result': result}

    if parsed is not None:
        if label == 'fetch_with_cffi':
            text = str(parsed.get('text', ''))
            success = bool(parsed.get('ok')) and text_has_success_signal(text)
            reason = 'html body retrieved' if success else 'weak or blocked html body'
            summary = {'status_code': parsed.get('status_code'), 'target': parsed.get('target'), 'length': parsed.get('length')}
        elif label == 'jina_fetch':
            body = str(parsed.get('body', ''))
            success = text_has_success_signal(body)
            reason = 'jina body retrieved' if success else 'jina body too weak or blocked'
            summary = {'url': parsed.get('url'), 'length': len(body)}
        elif label == 'extract_metadata':
            og = parsed.get('og') or {}
            json_ld = parsed.get('json_ld') or []
            success = bool(og or json_ld or parsed.get('description') or parsed.get('next_data_excerpt'))
            reason = 'metadata found' if success else 'no useful metadata'
            summary = {'og_keys': list(og.keys())[:10], 'json_ld_count': len(json_ld)}
        elif label == 'wayback_lookup':
            available = parsed.get('available', {})
            snapshots = available.get('archived_snapshots', {}) if isinstance(available, dict) else {}
            success = bool(snapshots)
            reason = 'archived snapshot found' if success else 'no archive snapshot'
            summary = {'archived': bool(snapshots), 'cdx': parsed.get('cdx')}
        elif label == 'reddit_json':
            success = isinstance(parsed, (list, dict)) and len(json.dumps(parsed, ensure_ascii=False)) > 200
            reason = 'reddit json retrieved' if success else 'reddit json too weak'
            summary = {'type': type(parsed).__name__}
        elif label == 'twitter_oembed':
            html = str(parsed.get('html', ''))
            success = bool(html)
            reason = 'oEmbed html retrieved' if success else 'oEmbed empty'
            summary = {'author_name': parsed.get('author_name'), 'url': parsed.get('url')}
        elif label in {'hn_fetch', 'bluesky_fetch', 'naver_search', 'rss_discover', 'naver_search_news', 'naver_search_post'}:
            size = len(json.dumps(parsed, ensure_ascii=False))
            if label.startswith('hn_'):
                hits = parsed.get('hits') or []
                success = len(hits) > 0
                reason = 'hn results retrieved' if success else 'hn returned no hits'
                summary = {'size': size, 'hit_count': len(hits)}
            else:
                success = size > 150
                reason = f'{label} payload retrieved' if success else f'{label} payload too weak'
                summary = {'size': size}
        else:
            success = len(json.dumps(parsed, ensure_ascii=False)) > 200
            reason = 'json payload retrieved' if success else 'json payload too weak'
            summary = {'size': len(json.dumps(parsed, ensure_ascii=False))}
    else:
        success = text_has_success_signal(stdout)
        reason = 'text body retrieved' if success else 'text output too weak'
        summary = {'length': len(stdout)}

    return {'label': label, 'success': success, 'reason': reason, 'summary': summary, 'result': result}


def execute_step(label, command):
    return evaluate_attempt(label, run_command(command))


def candidate_steps_for_url(url: str, host: str):
    py = sys.executable
    steps = []
    if 'x.com' in host or 'twitter.com' in host:
        steps.append(('twitter_oembed', [py, str(SCRIPT_DIR / 'twitter_oembed.py'), url]))
        steps.append(('jina_fetch', [py, str(SCRIPT_DIR / 'jina_fetch.py'), url]))
        steps.append(('wayback_lookup', [py, str(SCRIPT_DIR / 'wayback_lookup.py'), url]))
        return steps
    if 'reddit.com' in host:
        steps.append(('reddit_json', [py, str(SCRIPT_DIR / 'reddit_json.py'), url]))
    elif 'youtube.com' in host or 'youtu.be' in host:
        steps.append(('yt_dlp', ['yt-dlp', '--dump-json', url]))
    elif 'news.ycombinator.com' in host or 'hn.algolia.com' in host:
        steps.append(('hn_fetch', [py, str(SCRIPT_DIR / 'hn_fetch.py'), '--limit', '10']))
    elif 'bsky.app' in host or 'bsky.social' in host:
        # URL parsing for individual posts is still weak; try Jina then metadata.
        steps.append(('jina_fetch', [py, str(SCRIPT_DIR / 'jina_fetch.py'), url]))
    elif 'naver.com' in host:
        steps.append(('fetch_with_cffi', [py, str(SCRIPT_DIR / 'fetch_with_cffi.py'), url]))
    else:
        steps.append(('jina_fetch', [py, str(SCRIPT_DIR / 'jina_fetch.py'), url]))
        steps.append(('fetch_with_cffi', [py, str(SCRIPT_DIR / 'fetch_with_cffi.py'), url]))

    steps.append(('extract_metadata', [py, str(SCRIPT_DIR / 'extract_metadata.py'), url]))
    steps.append(('wayback_lookup', [py, str(SCRIPT_DIR / 'wayback_lookup.py'), url]))
    return steps


def execute_url(url: str, host: str, stop_on_success: bool):
    attempts = []
    best = None
    for label, command in candidate_steps_for_url(url, host):
        attempt = execute_step(label, command)
        attempts.append(attempt)
        if attempt['success'] and best is None:
            best = attempt
            if stop_on_success and label != 'extract_metadata':
                break
    if best is None and attempts:
        best = attempts[-1]
    return attempts, best


def execute_handle(handle: str, stop_on_success: bool):
    normalized = handle.lstrip('@')
    py = sys.executable
    attempts = []
    for label, command in [
        ('bluesky_fetch', [py, str(SCRIPT_DIR / 'bluesky_fetch.py'), normalized]),
        ('twitter_timeline', ['curl', '-sL', f'https://syndication.twitter.com/srv/timeline-profile/screen-name/{normalized}']),
    ]:
        attempt = execute_step(label, command)
        attempts.append(attempt)
        if attempt['success'] and stop_on_success:
            return attempts, attempt
    return attempts, attempts[0] if attempts else None


def execute_query(query: str, stop_on_success: bool):
    py = sys.executable
    attempts = []
    steps = [
        ('naver_search_news', [py, str(SCRIPT_DIR / 'naver_search.py'), query, '--where', 'news']),
        ('naver_search_post', [py, str(SCRIPT_DIR / 'naver_search.py'), query, '--where', 'post']),
        ('hn_search', [py, str(SCRIPT_DIR / 'hn_fetch.py'), '--query', query]),
    ]
    if re.search(r'\b(arxiv|paper|논문)\b', query, re.I):
        steps.append(('arxiv_search', ['curl', '-sL', 'http://export.arxiv.org/api/query?search_query=all:' + quote(query) + '&max_results=5&sortBy=submittedDate&sortOrder=descending']))

    best = None
    for label, command in steps:
        attempt = execute_step(label, command)
        attempts.append(attempt)
        if attempt['success'] and best is None:
            best = attempt
            if stop_on_success:
                break
    if best is None and attempts:
        best = attempts[-1]
    return attempts, best


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--plan-only', action='store_true', help='Only print the classified route and candidate commands.')
    parser.add_argument('--run-all', action='store_true', help='Do not stop after the first successful attempt.')
    args = parser.parse_args()

    cls = classify(args.input)
    stop_on_success = not args.run_all

    if args.plan_only:
        if cls['kind'] == 'url':
            steps = [{'label': label, 'command': ' '.join(command)} for label, command in candidate_steps_for_url(args.input, cls['host'])]
        elif cls['kind'] == 'handle':
            py = sys.executable
            normalized = args.input.lstrip('@')
            steps = [
                {'label': 'bluesky_fetch', 'command': f"{py} {SCRIPT_DIR / 'bluesky_fetch.py'} {normalized}"},
                {'label': 'twitter_timeline', 'command': f"curl -sL https://syndication.twitter.com/srv/timeline-profile/screen-name/{normalized}"},
            ]
        else:
            py = sys.executable
            steps = [
                {'label': 'naver_search_news', 'command': f"{py} {SCRIPT_DIR / 'naver_search.py'} {args.input} --where news"},
                {'label': 'naver_search_post', 'command': f"{py} {SCRIPT_DIR / 'naver_search.py'} {args.input} --where post"},
                {'label': 'hn_search', 'command': f"{py} {SCRIPT_DIR / 'hn_fetch.py'} --query {args.input}"},
            ]
        print(json.dumps({'classification': cls, 'steps': steps}, ensure_ascii=False, indent=2))
        return

    if cls['kind'] == 'url':
        attempts, best = execute_url(args.input, cls['host'], stop_on_success)
    elif cls['kind'] == 'handle':
        attempts, best = execute_handle(args.input, stop_on_success)
    else:
        attempts, best = execute_query(args.input, stop_on_success)

    output = {
        'classification': cls,
        'stop_on_success': stop_on_success,
        'attempt_count': len(attempts),
        'best': best,
        'attempts': attempts,
        'next_hint': 'If all attempts are weak or blocked, escalate to Hermes browser/browser_cdp using the URL you discovered.',
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
