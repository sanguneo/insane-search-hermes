#!/usr/bin/env python3
"""Fetch top stories or search Hacker News."""
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
    parser.add_argument('--query')
    parser.add_argument('--limit', type=int, default=10)
    args = parser.parse_args()

    if args.query:
        data = get_json('https://hn.algolia.com/api/v1/search?query=' + urllib.parse.quote(args.query))
        print(json.dumps(data, ensure_ascii=False, indent=2)[:50000])
        return

    ids = get_json('https://hacker-news.firebaseio.com/v0/topstories.json')[:args.limit]
    items = [get_json(f'https://hacker-news.firebaseio.com/v0/item/{id}.json') for id in ids]
    print(json.dumps(items, ensure_ascii=False, indent=2)[:50000])


if __name__ == '__main__':
    main()
