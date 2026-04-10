# Factory Artifact Contract v0

## Contract ID

- Name: `factory-artifact`
- Version: `v0`
- Owner domain: Product Core (Artifact Viewer surface)

## Purpose

Provide metadata and retrieval contract for run artifacts used in the Artifact Viewer.

## Canonical Ownership (PostgreSQL)

PostgreSQL owns artifact metadata and visibility policy.
Artifact body may live in replaceable object storage.

### Canonical fields

- `artifact_id`
- `run_id`
- `workspace_id`
- `artifact_type` (`spec_snapshot` | `sprint_contract` | `generator_report` | `evaluator_report` | `manifest`)
- `storage_uri`
- `checksum`
- `created_at`

## API Surface (HTTP)

### List artifacts for run

- `GET /api/v0/workspaces/{workspace_id}/factory/runs/{run_id}/artifacts`

### Get artifact metadata

- `GET /api/v0/workspaces/{workspace_id}/factory/artifacts/{artifact_id}`

## Invariants

- Artifact must belong to the same workspace as the run.
- Artifact type taxonomy is versioned by contract.
- Visibility is controlled by workspace membership/permissions.

## Adapter Boundary

Object storage provider is replaceable.
Artifact viewer consumes stable metadata contract, not storage vendor APIs.
