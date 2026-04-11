# Workspace Contract v0

## Contract ID

- Name: `workspace`
- Version: `v0`
- Owner domain: Product Core (`apps/backend`)

## Purpose

Workspace is the top-level tenant boundary for all product resources.

## Canonical Ownership (PostgreSQL)

PostgreSQL is the system of record for workspace metadata.

### Canonical fields

- `workspace_id` (stable resource id)
- `name`
- `slug`
- `status` (`active` | `archived`)
- `created_at`
- `updated_at`

## API Surface (HTTP)

- `POST /api/v0/workspaces`
- `GET /api/v0/workspaces`
- `GET /api/v0/workspaces/{workspace_id}`

## Invariants

- Every domain resource must be scoped by `workspace_id`.
- `workspace_id` is immutable after creation.
- `slug` must be unique.

## Adapter Boundary

No external engine may own workspace truth.
