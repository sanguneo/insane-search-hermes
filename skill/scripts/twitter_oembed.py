#!/usr/bin/env python3
"""Fetch X/Twitter oEmbed for a single post URL."""
import argparse
import json
import urllib.parse
import urllib.request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tweet_url')
    args = parser.parse_args()
    api = 'https://publish.twitter.com/oembed?url=' + urllib.parse.quote(args.tweet_url, safe='')
    req = urllib.request.Request(api, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode('utf-8', 'ignore'))
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
