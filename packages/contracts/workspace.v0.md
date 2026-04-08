# Workspace Contract v0

## Purpose

Workspace is the top-level tenancy and permission boundary for all product-owned resources.

## Canonical Ownership

- Owned by the platform
- Stored in PostgreSQL as the system of record
- All workspace-scoped resources must carry `workspace_id`

## Core Fields

- `workspace_id`
- `slug`
- `name`
- `status`
- `created_at`
- `created_by`
- `updated_at`

## Rules

- `workspace_id` is immutable.
- `slug` is unique within the platform.
- Soft delete or archival state must preserve historical references.
- Every product resource must resolve to exactly one workspace boundary.

## States

- `active`
- `archived`
- `deleted`

## API Surface

- `POST /workspaces`
- `GET /workspaces/{workspace_id}`
- `PATCH /workspaces/{workspace_id}`
- `GET /workspaces`

## Events

- `workspace.created`
- `workspace.updated`
- `workspace.archived`
- `workspace.deleted`

## Notes

- Workspace is the root contract for permissions, work items, documents, files, and Git linkage.
