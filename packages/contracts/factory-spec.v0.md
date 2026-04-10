# Factory Spec Contract v0

## Contract ID

- Name: `factory-spec`
- Version: `v0`
- Owner domain: Product Core (Factory App surface)

## Purpose

Represent a product spec snapshot used by harness runs.

## Canonical Ownership (PostgreSQL)

PostgreSQL owns spec metadata and lifecycle state.
Spec document body may be stored externally, but metadata remains canonical in PostgreSQL.

### Canonical fields

- `spec_id`
- `workspace_id`
- `title`
- `version`
- `status` (`draft` | `approved` | `superseded`)
- `snapshot_uri` (body location reference)
- `created_by`
- `created_at`
- `updated_at`

## API Surface (HTTP)

### Create spec

- `POST /api/v0/workspaces/{workspace_id}/factory/specs`

### List specs

- `GET /api/v0/workspaces/{workspace_id}/factory/specs`

### Get spec

- `GET /api/v0/workspaces/{workspace_id}/factory/specs/{spec_id}`

## Invariants

- Runs must reference an existing approved spec snapshot.
- Spec version is immutable once approved.

## Adapter Boundary

Document storage engine is replaceable behind storage contract.
Search indexing is replaceable behind search adapter contract.
