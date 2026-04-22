#!/usr/bin/env python3
"""Fetch Reddit JSON with mobile UA."""
import argparse
import json
import urllib.request

UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Reddit JSON-capable URL or subreddit URL')
    args = parser.parse_args()
    url = args.url
    if not url.endswith('.json'):
        if url.endswith('/'):
            url = url[:-1]
        url += '.json'
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode('utf-8', 'ignore'))
    print(json.dumps(payload, ensure_ascii=False, indent=2)[:50000])


if __name__ == '__main__':
    main()
