# Factory Run Contract v0

## Purpose

Factory Run represents one controlled execution of planner, generator, and evaluator against a spec and sprint contract.

## Canonical Ownership

- Owned by the platform
- Execution metadata is stored in PostgreSQL
- Runtime artifacts are file-backed or object-backed, but referenced by platform records

## Core Fields

- `factory_run_id`
- `workspace_id`
- `factory_spec_id`
- `status`
- `planner_prompt_ref`
- `generator_prompt_ref`
- `evaluator_prompt_ref`
- `contract_snapshot_ref`
- `artifact_root_ref`
- `created_at`
- `created_by`

## Rules

- A run must reference one spec snapshot.
- A run must reference one sprint contract snapshot.
- A run must record touched paths before generator execution.
- A run cannot be closed without evaluator `PASS`.
- Failed evaluation remains visible in evaluator artifacts and blocks close, but is not persisted as a terminal run status in v0.

## States

- `created`
- `planned`
- `running`
- `blocked`
- `closed`

## API Surface

- `POST /factory-runs`
- `GET /factory-runs/{factory_run_id}`
- `GET /workspaces/{workspace_id}/factory-runs`
- `POST /factory-runs/{factory_run_id}/start`
- `POST /factory-runs/{factory_run_id}/close`

## Events

- `factory_run.created`
- `factory_run.started`
- `factory_run.blocked`
- `factory_run.closed`

## Notes

- The run record is the coordination layer, not the executor itself.
