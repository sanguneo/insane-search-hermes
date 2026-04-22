#!/usr/bin/env python3
"""Search Naver with curl_cffi, auto-installing curl_cffi if needed."""
import argparse
import json
import subprocess
import sys
from urllib.parse import quote


def ensure_curl_cffi():
    try:
        from curl_cffi import requests  # noqa: F401
    except Exception:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'curl_cffi'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query')
    parser.add_argument('--where', default='news', choices=['news', 'post', 'web', 'nexearch'])
    args = parser.parse_args()

    ensure_curl_cffi()
    from curl_cffi import requests

    session = requests.Session(impersonate='chrome')
    session.headers.update({
        'Accept-Language': 'ko-KR,ko;q=0.9',
        'Referer': 'https://www.google.com/',
        'User-Agent': 'Mozilla/5.0',
    })
    try:
        session.get('https://www.naver.com/', timeout=10)
    except Exception:
        pass
    session.headers['Referer'] = 'https://www.naver.com/'
    if args.where == 'nexearch':
        url = f'https://search.naver.com/search.naver?query={quote(args.query)}'
    else:
        url = f'https://search.naver.com/search.naver?where={args.where}&query={quote(args.query)}'
    resp = session.get(url, timeout=20)
    print(json.dumps({'url': url, 'status_code': resp.status_code, 'text': resp.text[:30000]}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
