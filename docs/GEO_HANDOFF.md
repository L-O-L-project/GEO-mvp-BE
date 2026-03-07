# GEO Handoff (2026-03-07)

## Scope
- QA 혼합 기능을 제거하고 GEO 전용 백엔드로 정리
- GEO 감사(`geo_audit`) 및 GEO 디스커버리(`discovery`) 유지
- 고도화 재사용을 위해 `analyze.py`, `llm.py` 유지

## Files Changed
- `app/main.py`
- `app/routers/geo.py`
- `app/routers/discovery.py`
- `app/services/geo_audit.py`
- `app/services/analyze.py` (유지)
- `app/services/llm.py` (유지)
- `app/static/geo-test.html`
- `tests/test_geo_test_page.py`
- `tests/test_geo_audit_details.py`
- `tests/test_geo_discovery_api.py`
- `requirements.txt`
- `README.md`
- `docs/GEO_SCOPE_AUDIT_2026-03-07.md`

## API Changes
- 유지:
  - `GET /`
  - `GET /health`
  - `GET /geo-test`
  - `POST /api/geo-audit`
  - `POST /api/geo-discovery`
- 제거:
  - QA 전용 API 전체 (체크리스트/플로우/OAuth/시트 연동 등)

## Validation Output
- `python3 -m pytest -q` 통과
- 런타임 스모크 통과:
  - `GET /health`
  - `GET /geo-test`
  - `POST /api/geo-audit`
  - `POST /api/geo-discovery`
- `https://optiflow.kr/geo` 기준 점검:
  - `geo_score` 92
  - `json_ld_summary` 10/10 유효
  - `recommendations` 없음

## Current Runtime / Ops
- 기본 실행:
  - `uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`
- 포트 8000 충돌 시:
  - 기존 PID 확인: `lsof -iTCP:8000 -sTCP:LISTEN -n -P`
  - 기존 PID 종료 후 재기동
- 로그 파일 예시:
  - `/tmp/geo_latest_8000.log`

## Environment Variables
- `QA_WEB_ORIGIN`: CORS 허용 origin (`*` 기본)
- `QA_HTTP_VERIFY_TLS`: 크롤링 TLS 검증 (`false` 기본)
- `QA_GEO_DYNAMIC`: Playwright 동적 경로 수집 (`false` 기본)

## Repo Hygiene
- `.gitignore` 적용:
  - `__pycache__/`, `*.pyc`, `.venv/`, `.pytest_cache/`, `out/`, `*.log` 등 제외
- 구 QA hook 제거:
  - `.githooks/pre-push` 삭제

## Rollback Plan
- 이전 QA 통합 구조가 필요하면 Git 히스토리에서 복구
- 빠른 복구 순서:
  - `app/main.py` 이전 버전 복원
  - 제거된 QA 서비스/라우터 복원
  - `requirements.txt` QA 의존성 복원
  - API smoke 재검증
