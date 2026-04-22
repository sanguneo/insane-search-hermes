# 메타데이터 추출

본문을 못 가져와도 다음은 꼭 본다.
- OGP
- JSON-LD
- Next.js payload (`__NEXT_DATA__`, `self.__next_f.push`)

## 터미널 예시

```bash
curl -sL 'https://example.com' > /tmp/example-page.html
python3 - <<'PY'
from pathlib import Path
import re, json
html = Path('/tmp/example-page.html').read_text(encoding='utf-8', errors='ignore')
for m in re.findall(r'<meta[^>]+property=["']og:([^"']+)["'][^>]+content=["']([^"']*)', html, re.I):
    print('og:%s = %s' % m)
for block in re.findall(r'<script[^>]+type=["']application/ld\+json["'][^>]*>(.*?)</script>', html, re.S|re.I):
    try:
        print(json.dumps(json.loads(block), ensure_ascii=False)[:3000])
    except Exception:
        pass
PY
```
