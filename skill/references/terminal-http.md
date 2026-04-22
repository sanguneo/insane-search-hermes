# 터미널 HTTP 프로브

Hermes 웹 도구가 비거나 막히면 `terminal`로 직접 확인한다.

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

## `curl_cffi` 확인
```bash
python3 -c "import curl_cffi; print('curl_cffi ok')"
```

없으면 설치가 필요하다고만 판단하고, 실제 설치는 현재 작업 범위에 맞게 별도 실행한다.

## Python3 one-liner 원칙
이 환경에서는 `python` 대신 `python3`를 쓴다.
