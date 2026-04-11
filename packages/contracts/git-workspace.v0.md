# Git Workspace Binding Contract v0

## Contract ID

- Name: `git-workspace-binding`
- Version: `v0`
- Owner domain: Product Core (`apps/backend`)

## Canonical Ownership (PostgreSQL)

PostgreSQL is the system of record for binding metadata.

### Canonical fields

- `binding_id`
- `workspace_id`
- `provider`
- `repository_ref`
- `default_branch`
- `status`

## API Surface (HTTP)

- `POST /api/v0/workspaces/{workspace_id}/git-bindings`
- `GET /api/v0/workspaces/{workspace_id}/git-bindings`

## Invariants

- Binding must reference an existing `workspace_id`.
- Repository content is not the product system of record.

## Adapter Boundary

Git provider integrations stay behind a replaceable adapter contract.
