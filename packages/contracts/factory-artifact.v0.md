# Factory Artifact Contract v0

## Contract ID

- Name: `factory-artifact`
- Version: `v0`

## Canonical Ownership (PostgreSQL)

PostgreSQL owns artifact metadata and visibility policy.

### Canonical fields

- `artifact_id`
- `run_id`
- `workspace_id`
- `artifact_type`
- `storage_uri`

## API Surface (HTTP)

- `GET /api/v0/workspaces/{workspace_id}/factory/runs/{run_id}/artifacts`
- `GET /api/v0/workspaces/{workspace_id}/factory/artifacts/{artifact_id}`

## Invariants

- Artifact must belong to the same workspace as the run.
- Artifact type taxonomy is versioned by contract.
