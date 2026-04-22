# 메타데이터 추출

본문을 못 가져와도 아래는 꼭 확인한다.
- OGP: title, description, image
- JSON-LD: Product, NewsArticle, Person, ItemList
- Next.js payload: `__NEXT_DATA__`, `self.__next_f.push`

## 터미널 예시
```bash
curl -sL 'https://example.com' > /tmp/example-page.html
python3 - <<'PY'
from pathlib import Path
import re, json
html = Path('/tmp/example-page.html').read_text(encoding='utf-8', errors='ignore')
for m in re.findall(r'<meta[^>]+property=["\']og:([^"\']+)["\'][^>]+content=["\']([^"\']*)', html, re.I):
    print('og:%s = %s' % m)
for block in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.S|re.I):
    try:
        print(json.dumps(json.loads(block), ensure_ascii=False)[:3000])
    except Exception:
        pass
PY
```

## 브라우저 예시
`browser_console(expression='[...document.querySelectorAll("script[type=\"application/ld+json\"]")].map(x=>x.textContent)')`

## 특히 유용한 경우
- 쇼핑몰 가격/상품 리스트
- 뉴스 기사 요약/작성일
- 프로필 페이지
- 본문이 비어 있는 SPA
