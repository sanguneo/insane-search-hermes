# 터미널 HTTP 프로브

웹 도구가 비거나 막히면 직접 확인한다.

## 기본 curl

```bash
curl -L --max-time 20 -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36' 'https://example.com'
```

## 모바일 UA

```bash
curl -L --max-time 20 -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15' 'https://example.com'
```

## Jina

```bash
curl -s 'https://r.jina.ai/https://example.com/path'
```

## curl_cffi

```bash
python3 -c "import curl_cffi" 2>/dev/null || pip install curl_cffi -q
```

## yt-dlp

```bash
which yt-dlp || python3 -m pip install -q yt-dlp
```

## feedparser

```bash
python3 -c "import feedparser" 2>/dev/null || pip install feedparser -q
```

## 원칙
- `python` 대신 `python3`
- 없으면 설치하고 계속
- 설치 실패 시 더 약한 단계로 후퇴하지 말고 browser까지 올린다
