# Git Workspace Contract v0

## Purpose

Git Workspace binds an external Git repository to a platform workspace without making Git the system of record.

## Canonical Ownership

- Owned by the platform
- Repository metadata is stored in PostgreSQL
- Git provider implementation is pluggable

## Core Fields

- `git_workspace_id`
- `workspace_id`
- `provider`
- `repository_url`
- `default_branch`
- `connection_status`
- `created_at`
- `created_by`

## Rules

- One Git workspace belongs to one platform workspace.
- Provider details stay behind an adapter contract.
- Repository identity must be stable even if the provider implementation changes.
- Git is a revision backend and collaboration bridge, not the primary operational store.

## States

- `connected`
- `disconnected`
- `error`
- `archived`

## API Surface

- `POST /workspaces/{workspace_id}/git-workspaces`
- `GET /workspaces/{workspace_id}/git-workspaces`
- `GET /git-workspaces/{git_workspace_id}`
- `PATCH /git-workspaces/{git_workspace_id}`
- `DELETE /git-workspaces/{git_workspace_id}`

## Events

- `git_workspace.connected`
- `git_workspace.updated`
- `git_workspace.disconnected`
- `git_workspace.archived`

## Notes

- Branch, commit, and pull request references may be modeled later as linked resources.
