#!/usr/bin/env python3
"""Fetch a URL with curl_cffi impersonation, auto-installing curl_cffi if needed."""
import argparse
import json
import subprocess
import sys
from urllib.parse import urlparse


def ensure_curl_cffi():
    try:
        from curl_cffi import requests  # noqa: F401
    except Exception:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'curl_cffi'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--locale', default='ko-KR')
    parser.add_argument('--timeout', type=int, default=20)
    args = parser.parse_args()

    ensure_curl_cffi()
    from curl_cffi import requests

    parsed = urlparse(args.url)
    origin = f'{parsed.scheme}://{parsed.netloc}'
    targets = ['safari', 'chrome', 'firefox']
    last_error = None

    for target in targets:
        try:
            session = requests.Session(impersonate=target)
            session.headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': f'{args.locale},{args.locale.split("-")[0]};q=0.9,en-US;q=0.8',
                'Referer': 'https://www.google.com/',
                'User-Agent': 'Mozilla/5.0',
            })
            try:
                session.get(origin, timeout=min(args.timeout, 10))
            except Exception:
                pass
            session.headers['Referer'] = origin
            resp = session.get(args.url, timeout=args.timeout)
            payload = {
                'ok': resp.status_code == 200,
                'target': target,
                'status_code': resp.status_code,
                'headers': dict(resp.headers),
                'text': resp.text[:20000],
                'length': len(resp.text),
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return
        except Exception as exc:
            last_error = repr(exc)

    print(json.dumps({'ok': False, 'error': last_error or 'all targets failed'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
