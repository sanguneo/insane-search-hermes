#!/usr/bin/env python3
"""Check Wayback availability and CDX snapshots."""
import argparse
import json
import urllib.parse
import urllib.request


def get_text(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8', 'ignore')


def get_json(url):
    return json.loads(get_text(url))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()
    target = urllib.parse.quote(args.url, safe='')

    try:
        available = get_json('https://archive.org/wayback/available?url=' + target)
    except Exception as exc:
        available = {'error': repr(exc)}

    try:
        cdx_raw = get_text('https://web.archive.org/cdx/search/cdx?url=' + target + '&output=json&fl=timestamp,statuscode&limit=5')
        try:
            cdx = json.loads(cdx_raw)
        except Exception:
            cdx = cdx_raw
    except Exception as exc:
        cdx = {'error': repr(exc)}

    print(json.dumps({'available': available, 'cdx': cdx}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
