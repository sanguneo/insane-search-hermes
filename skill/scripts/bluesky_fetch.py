#!/usr/bin/env python3
"""Fetch Bluesky profile or author feed."""
import argparse
import json
import urllib.parse
import urllib.request


def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8', 'ignore'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('handle')
    parser.add_argument('--feed', action='store_true')
    parser.add_argument('--limit', type=int, default=10)
    args = parser.parse_args()

    if args.feed:
        url = 'https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=' + urllib.parse.quote(args.handle) + f'&limit={args.limit}'
    else:
        url = 'https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor=' + urllib.parse.quote(args.handle)
    data = get_json(url)
    print(json.dumps(data, ensure_ascii=False, indent=2)[:50000])


if __name__ == '__main__':
    main()
