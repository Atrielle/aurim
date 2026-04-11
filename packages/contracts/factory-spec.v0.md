# Factory Spec Contract v0

## Contract ID

- Name: `factory-spec`
- Version: `v0`

## Canonical Ownership (PostgreSQL)

PostgreSQL owns spec metadata and lifecycle state.

### Canonical fields

- `spec_id`
- `workspace_id`
- `title`
- `version`
- `status`
- `snapshot_uri`

## API Surface (HTTP)

- `POST /api/v0/workspaces/{workspace_id}/factory/specs`
- `GET /api/v0/workspaces/{workspace_id}/factory/specs`
- `GET /api/v0/workspaces/{workspace_id}/factory/specs/{spec_id}`

## Invariants

- Runs must reference an approved spec snapshot.
- Spec version is immutable after approval.
