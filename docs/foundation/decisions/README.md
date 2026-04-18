# Decision Records

이 디렉터리는 세션이 끊겨도 추적 가능한 거버넌스 결정을 파일시스템에 저장하는 공간이다.

## Rules

- 파일명: `DEC-YYYY-NNNN-<slug>.json`
- 스키마: `docs/foundation/decision-record.schema.json`
- 상태: `proposed`, `decided`, `superseded`, `rejected`
- 기존 결정을 대체하면 새 레코드의 `supersedes`에 이전 `decision_id`를 넣는다.

## Why Filesystem First

현재는 DB 없이도 Git 이력/PR과 함께 감사 추적이 가능하도록 파일시스템을 기준 원본으로 쓴다.
추후 레코드가 많아지면 DB 인덱스를 추가할 수 있지만, 원본 권위는 파일에 둔다.

## Suggested Flow

1. 변경 제안 작성 (`status=proposed`)
2. 사용자 승인 후 `status=decided` 전환
3. `docs/foundation/decision-status.md`의 Decided/Pending 갱신
4. `python tools/harness-runtime/scripts/governance_audit.py --run-regression` 실행
