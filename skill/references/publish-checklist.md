# Publish readiness checklist

skills hub 배포 전 마지막 점검용 체크리스트.

## 구조
- [ ] `SKILL.md` 존재
- [ ] `references/` 링크 파일 모두 존재
- [ ] `scripts/` 실행 파일 모두 존재
- [ ] README.md / README.ko.md 분리됨
- [ ] LICENSE 포함

## 메타데이터
- [ ] `name` 고유함
- [ ] `description`이 충분히 구체적임
- [ ] `version` 갱신됨
- [ ] `metadata.hermes.tags` 정리됨
- [ ] upstream attribution 명시됨

## 실행성
- [ ] `insane_router.py --plan-only` 동작
- [ ] generic URL 입력으로 최소 1개 성공 경로 확인
- [ ] handle 입력으로 최소 1개 성공 경로 확인
- [ ] query 입력으로 최소 1개 성공 경로 확인
- [ ] PEP 668 환경에서 temp venv bootstrap 동작

## 배포 명령
```bash
hermes skills publish /home/sknah/work/insane-search-hermes/skill --to github --repo sanguneo/insane-search-hermes
hermes skills publish /home/sknah/work/insane-search-hermes/skill --to clawhub
```

## 배포 후 확인
```bash
hermes skills inspect insane-search-hermes
hermes skills search insane-search-hermes
```
