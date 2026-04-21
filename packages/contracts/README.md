# Contracts

이 디렉터리는 최대버전 하네스의 계약 기준 원본을 둔다.

## Source Of Truth

- governance documents in `docs/foundation/`
- JSON Schema in `packages/contracts/schemas/`

## Contract Set

- `run-contract.schema.json`
- `state-machine.schema.json`
- `executor-config.schema.json`
- `budget-policy.schema.json`
- `retry-policy.schema.json`
- `evidence-record.schema.json`
- `ui-run-view.schema.json`

## Intent

코드 구현은 이 계약에 종속되어야 하고, 반대로 계약은 특정 구현 세부사항에 종속되면 안 된다.
