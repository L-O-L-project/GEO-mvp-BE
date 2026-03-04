# QA 고도화 실행 계획서 (BE)

작성일: 2026-03-04
대상: `qa-mvp-BE`
목표: FE가 신뢰 가능한 결과를 소비하도록 API/판정/운영성을 강화

---

## 1. 우선순위 로드맵

## P1
1) 진행률 표준 스키마 제공
2) 최종 판정 요약(의사결정 카드용) 제공
3) 오류 분류 코드 표준화
4) deprecation 경고 정리(lifespan)

## P2
5) 탐색 커버리지 계산 신뢰도 보강
6) 실행 이력 조회/비교 API

---

## 2. 이슈 티켓 단위 계획

## BE-001: Progress API 확장
- 목적: FE에서 단계별 상태를 안정적으로 렌더
- 응답 필드 추가:
  - `phase`: discovery|checklist|flow|report
  - `percent`: 0~100
  - `elapsed_ms`
  - `eta_ms`
  - `last_message`
- 수용 기준:
  - oneclick/run 실행 중 주기적으로 값 갱신

## BE-002: Final Summary 표준화
- 목적: FE의 릴리즈 판단 카드 생성 근거 제공
- 필드:
  - `critical_fail_count`
  - `warning_count`
  - `blockers_top` (최대 5)
  - `action_items` (최대 3)
  - `decision_hint` (ship|ship_with_caution|hold)
- 수용 기준:
  - `/api/report/finalize` 및 oneclick 응답에 포함

## BE-003: Error Taxonomy 도입
- 목적: 사용자 친화적 실패 안내
- 에러 구조:
  - `error_code`
  - `error_category` (network/auth/config/discovery_limit/server)
  - `user_message`
  - `debug_detail`
- 수용 기준:
  - 주요 엔드포인트에서 일관된 에러 형식 반환

## BE-004: FastAPI startup deprecation 제거
- 목적: 향후 Python/FastAPI 업그레이드 리스크 축소
- 작업:
  - `@app.on_event("startup")` -> lifespan 전환
- 수용 기준:
  - pytest 경고 감소 확인

## BE-005: Discovery Coverage 보강
- 목적: PASS 신뢰도 향상
- 작업:
  - 제한 조건(depth/page/origin) 명시
  - 커버리지 산정 근거 필드 추가
- 수용 기준:
  - analyze 결과에 커버리지 근거 포함

## BE-006: Run History API
- 목적: FE 이력 비교 기능 지원
- API:
  - 최근 N개 실행 결과 조회
  - 동일 URL 기준 비교 데이터 제공
- 수용 기준:
  - runId 기준 상태/경고/실패/소요시간 반환

---

## 3. 테스트 계획

1) 단위 테스트
- 에러 매핑 함수
- decision_hint 계산 함수

2) 통합 테스트
- oneclick 전체 실행에서 progress/final summary 확인
- 오류 분류 케이스별 응답 스키마 검증

3) 회귀 테스트
- 기존 `/api/analyze`, `/api/checklist/auto`, `/api/flow/transition-check` 동작 보장

---

## 4. 예상 작업 순서

1. BE-004 (lifespan 전환) -> 0.5d
2. BE-003 (error taxonomy) -> 1.0d
3. BE-001 (progress 확장) -> 1.0d
4. BE-002 (final summary) -> 1.0d
5. BE-005 (coverage 보강) -> 0.5d
6. BE-006 (history API) -> 1.0d

총 5.0d
