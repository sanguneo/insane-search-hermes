# 미디어 추출

`yt-dlp`는 영상/오디오/스트리밍 메타데이터 확보의 기본 경로다.

## 설치 확인
```bash
which yt-dlp || python3 -m yt_dlp --version
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
yt-dlp --dump-json "ytsearch5:검색어"
```

## 언제 우선하나
- YouTube 요약
- 자막 추출
- Vimeo/Twitch/TikTok/SoundCloud 등 미디어 URL
- 공식 사이트 HTML이 막히고 실제 영상 메타만 필요할 때
