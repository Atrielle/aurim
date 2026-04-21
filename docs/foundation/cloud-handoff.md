# Cloud Handoff

## Identity

- Repository role: reusable harness engineering runtime
- Primary domain: harness runtime
- Product domain: out of scope for this repository baseline

## What This Repository Owns

이 저장소는 다른 프로젝트에 복사하거나 서브트리로 가져가서 사용할 수 있는 `AI harness engineering runtime`을 정의한다.

핵심 책임:

- run contract
- orchestration state machine
- planner / generator / evaluator executor contract
- budget / retry / evidence governance
- file-based artifact and state layout
- operator UI and control plane contract

## What This Repository Does Not Own

- 특정 제품의 domain model
- 제품 서버 request path 내부의 agent loop
- 특정 벤더 API에 종속된 executor 구현
- 제품 DB schema

## Target Runtime Shape

- modular runtime core
- replaceable executor adapters
- file-based default state store
- optional future DB-backed indexing layer
- operator-facing UI for run visibility and control

## Reuse Rule

다른 프로젝트는 이 저장소에서 아래를 가져가 사용할 수 있어야 한다.

- `docs/foundation/`
- `packages/contracts/`
- `tools/harness-runtime/`

프로젝트별 커스터마이징은 아래에 한정한다.

- spec inputs
- executor adapter wiring
- local policy defaults
- UI branding or embedding
