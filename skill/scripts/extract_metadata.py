#!/usr/bin/env python3
"""Extract OGP and JSON-LD metadata from a local HTML file or URL."""
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path


def load_text(source: str) -> str:
    if source.startswith('http://') or source.startswith('https://'):
        req = urllib.request.Request(source, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode('utf-8', 'ignore')
    return Path(source).read_text(encoding='utf-8', errors='ignore')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    args = parser.parse_args()
    html = load_text(args.source)

    og = {}
    for key, value in re.findall(r'<meta[^>]+property=["\']og:([^"\']+)["\'][^>]+content=["\']([^"\']*)', html, re.I):
        og[key] = value

    desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', html, re.I)
    description = desc_match.group(1) if desc_match else None

    json_ld = []
    for block in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            json_ld.append(json.loads(block))
        except Exception:
            continue

    next_data = None
    next_match = re.search(r'<script[^>]+id=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>', html, re.S | re.I)
    if next_match:
        next_data = next_match.group(1)[:5000]

    print(json.dumps({
        'og': og,
        'description': description,
        'json_ld': json_ld[:10],
        'next_data_excerpt': next_data,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
