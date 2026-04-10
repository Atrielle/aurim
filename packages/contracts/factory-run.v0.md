# Factory Run Contract v0

## Contract ID

- Name: `factory-run`
- Version: `v0`
- Owner domain: Product Core (Factory App surface) + Harness Runtime integration boundary

## Purpose

Represent a governed execution unit connected to spec snapshot and sprint contract.

## Canonical Ownership (PostgreSQL)

PostgreSQL owns run metadata and lifecycle state.

### Canonical fields

- `run_id`
- `workspace_id`
- `spec_id`
- `status` (`created` | `in_progress` | `blocked` | `passed` | `failed`)
- `started_at`
- `ended_at`
- `requested_by`
- `evaluator_verdict` (`PASS` | `FAIL` | `PENDING`)

## API Surface (HTTP)

### Create run request

- `POST /api/v0/workspaces/{workspace_id}/factory/runs`

### List runs

- `GET /api/v0/workspaces/{workspace_id}/factory/runs`

### Get run

- `GET /api/v0/workspaces/{workspace_id}/factory/runs/{run_id}`

## Invariants

- No run without valid spec snapshot.
- No successful close when evaluator verdict is not `PASS`.
- Touched paths are enforced by harness policy.

## Adapter Boundary

Planner/generator/evaluator runtime remains in `tools/harness-runtime`.
Product API exposes governed run metadata only.
