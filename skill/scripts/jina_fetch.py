#!/usr/bin/env python3
"""Fetch a page through Jina Reader."""
import argparse
import json
import urllib.request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--json-mode', action='store_true')
    args = parser.parse_args()

    reader_url = 'https://r.jina.ai/' + args.url
    headers = {'User-Agent': 'Mozilla/5.0'}
    if args.json_mode:
        headers['Accept'] = 'application/json'
    req = urllib.request.Request(reader_url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode('utf-8', 'ignore')
    print(json.dumps({'url': reader_url, 'body': body[:50000]}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
