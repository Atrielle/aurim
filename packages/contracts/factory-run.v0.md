# Factory Run Contract v0

## Contract ID

- Name: `factory-run`
- Version: `v0`

## Canonical Ownership (PostgreSQL)

PostgreSQL owns run metadata and lifecycle state.

### Canonical fields

- `run_id`
- `workspace_id`
- `spec_id`
- `status`
- `evaluator_verdict`

## API Surface (HTTP)

- `POST /api/v0/workspaces/{workspace_id}/factory/runs`
- `GET /api/v0/workspaces/{workspace_id}/factory/runs`
- `GET /api/v0/workspaces/{workspace_id}/factory/runs/{run_id}`

## Invariants

- No run without valid spec snapshot.
- No successful close when evaluator verdict is not `PASS`.

## Boundary

Planner/generator/evaluator runtime remains in `tools/harness-runtime`.
