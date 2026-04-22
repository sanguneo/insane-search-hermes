#!/usr/bin/env python3
"""Try common RSS/Atom feed paths and parse them, auto-installing feedparser if needed."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


def ensure_feedparser():
    try:
        import feedparser  # noqa: F401
        return
    except Exception:
        pass

    if os.environ.get('INSANE_FEEDPARSER_BOOTSTRAPPED') == '1':
        raise RuntimeError('feedparser bootstrap already attempted and still unavailable')

    venv_dir = Path('/tmp/insane-search-hermes-venvs/feedparser')
    venv_python = venv_dir / 'bin' / 'python'
    if not venv_python.exists():
        subprocess.check_call([sys.executable, '-m', 'venv', str(venv_dir)])
        subprocess.check_call([str(venv_python), '-m', 'pip', 'install', '-q', 'feedparser'])

    env = dict(os.environ)
    env['INSANE_FEEDPARSER_BOOTSTRAPPED'] = '1'
    raise SystemExit(subprocess.call([str(venv_python), __file__, *sys.argv[1:]], env=env))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()
    ensure_feedparser()
    import feedparser

    parsed = urlparse(args.url)
    origin = f'{parsed.scheme}://{parsed.netloc}'
    candidates = [f'{origin}/rss', f'{origin}/feed', f'{origin}/atom.xml', f'{origin}/rss.xml', f'{origin}/index.xml']
    results = []
    for candidate in candidates:
        feed = feedparser.parse(candidate)
        if getattr(feed, 'entries', None):
            results.append({
                'url': candidate,
                'title': getattr(feed.feed, 'title', ''),
                'entries': [{'title': getattr(e, 'title', ''), 'link': getattr(e, 'link', '')} for e in feed.entries[:5]],
            })
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
