# Factory Spec Contract v0

## Purpose

Factory Spec captures the instructions, constraints, and acceptance intent for a harness-driven development run.

## Canonical Ownership

- Owned by the platform
- Stored in PostgreSQL as the system of record
- Referenced by harness runtime, but not owned by it

## Core Fields

- `factory_spec_id`
- `workspace_id`
- `title`
- `summary`
- `problem_statement`
- `goal`
- `non_negotiable_constraints`
- `initial_scope`
- `excluded_scope`
- `acceptance_standard`
- `created_at`
- `created_by`

## Rules

- A spec belongs to exactly one workspace.
- A spec must be versioned when materially changed.
- The spec is the source input for sprint planning and evaluation.
- Contract text must remain concise enough to be read by both humans and agents.

## States

- `draft`
- `reviewed`
- `approved`
- `superseded`

## API Surface

- `POST /workspaces/{workspace_id}/factory-specs`
- `GET /workspaces/{workspace_id}/factory-specs`
- `GET /factory-specs/{factory_spec_id}`
- `PATCH /factory-specs/{factory_spec_id}`
- `POST /factory-specs/{factory_spec_id}/approve`

## Events

- `factory_spec.created`
- `factory_spec.updated`
- `factory_spec.approved`
- `factory_spec.superseded`

## Notes

- Harness runtime reads the spec snapshot, but product owns the canonical spec record.
