# Harness Core Refactor Plan (Phase 0)

이 디렉터리는 `runner.py`의 책임을 점진적으로 분리하기 위한 모듈 경계를 정의한다.

## Target Modules

- `types.py`
  - 런타임 공용 데이터 구조(CheckResult 등)
- `io_utils.py`
  - 파일/JSON read-write, 해시 유틸
- `validators.py`
  - heading/placeholder/contract-key 검증
- `path_policy.py`
  - touched path 정책 검사 및 경로 정규화

## Migration Rules

1. 기능 변경 금지: Phase 0~1에서는 동작 동일성을 유지한다.
2. 함수 단위 추출: runner의 기존 함수를 그대로 옮기고, 이후 호출부만 교체한다.
3. 회귀 기준: `unit_gate_regression.py`, `governance_audit.py --run-regression`가 PASS여야 한다.
4. `runner.py`는 최종적으로 CLI orchestration만 담당한다.

## Migration Status

- Phase 0: 완료 (모듈 경계 + skeleton)
- Phase 1: 완료 (runner의 공통 helper를 harness_core 모듈 위임)
- Phase 2-A: 완료 (unit report parsing/validation 도메인 로직을 `unit_ops.py`로 분리)
- Phase 2-B1: 완료 (gate-close 변화 검증/평가판정 로직을 `gate_ops.py`로 분리)
- Phase 2-B2: 완료 (sprint contract 검증 + work-unit 정렬 로직을 `contract_ops.py`로 분리)
- Phase 3-A: 완료 (freeze/baseline 검증 및 변경파일 계산 로직을 `baseline_ops.py`로 분리)
- Phase 3-B: 완료 (manifest 상태 전이/게이트 기록 helper를 `manifest_ops.py`로 분리)
- Phase 4-A: 완료 (CLI parser/dispatch를 `cli_ops.py`로 분리)
- Phase 4-B: 완료 (handler registry 검증 및 CLI 진입점 `run_cli` 통합)
- Refactor Program: 완료 (Phase 0~4 종료)

## Source Mapping (initial)

- IO 후보
  - `read_text`, `read_json`, `write_json`, `hash_text`, `hash_file`
- Validation 후보
  - `require_headings`, `require_no_placeholders`, `extract_checked_items`, `extract_paths`
- Path Policy 후보
  - `validate_paths`, `is_within_touched_paths`, `iter_touched_files`

## Non-Goals

- run contract format 변경
- artifact 디렉터리 구조 변경
- gate 판정 규칙 변경
