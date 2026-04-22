# 미디어 추출 — yt-dlp

> yt-dlp는 YouTube 전용이 아니라 1,858개 사이트를 지원하는 범용 미디어 추출 도구다.

## 없으면 설치하고 계속

```bash
which yt-dlp || python3 -m pip install -q yt-dlp
```

## 메타데이터

```bash
yt-dlp --dump-json "URL"
```

## 자막

```bash
yt-dlp --write-sub --write-auto-sub --sub-lang "ko,en" --skip-download -o "/tmp/%(id)s" "URL"
```

## 검색

```bash
yt-dlp --dump-json "ytsearch5:{검색어}"
yt-dlp --dump-json "scsearch5:{검색어}"
```

## 채널/플레이리스트

```bash
yt-dlp --flat-playlist --dump-json "채널_URL"
```
