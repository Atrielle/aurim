# Git Workspace Binding Contract v0

## Contract ID

- Name: `git-workspace-binding`
- Version: `v0`
- Owner domain: Product Core (`apps/backend`)

## Purpose

Define how a workspace is linked to one or more Git repositories for developer workflows.

## Canonical Ownership (PostgreSQL)

PostgreSQL is the system of record for binding metadata.

### Canonical fields

- `binding_id`
- `workspace_id`
- `provider` (`github` | `gitlab` | `bitbucket` | `custom`)
- `repository_ref` (provider-specific identifier)
- `default_branch`
- `status` (`connected` | `disconnected`)
- `created_at`
- `updated_at`

## API Surface (HTTP)

### Create binding

- `POST /api/v0/workspaces/{workspace_id}/git-bindings`
- Request:
  - `provider`
  - `repository_ref`
  - `default_branch`
- Response: binding resource

### List bindings

- `GET /api/v0/workspaces/{workspace_id}/git-bindings`
- Response: binding array

## Invariants

- Binding must reference an existing `workspace_id`.
- Provider access tokens/secrets are never returned by this contract.
- Repository content is not the product system of record.

## Adapter Boundary

Git provider SDK/API calls are behind a git adapter contract.
Domain services consume adapter interfaces, not vendor SDK directly.
