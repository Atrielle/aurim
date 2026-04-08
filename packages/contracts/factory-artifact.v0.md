# Factory Artifact Contract v0

## Purpose

Factory Artifact stores the files and records produced by a factory run.

## Canonical Ownership

- Owned by the platform
- Metadata is stored in PostgreSQL
- Artifact bodies may live in object storage, file storage, or the repo filesystem during bootstrap

## Core Fields

- `factory_artifact_id`
- `factory_run_id`
- `workspace_id`
- `artifact_type`
- `name`
- `content_ref`
- `checksum`
- `created_at`
- `created_by`

## Rules

- Every artifact must be traceable to exactly one run.
- Artifacts must be immutable once attached to a closed run.
- Artifact metadata remains visible even if the body is relocated.
- Artifact types must be versioned when semantics change.

## Types

- `spec_snapshot`
- `sprint_contract`
- `planner_report`
- `generator_report`
- `evaluator_report`
- `diff`
- `log`
- `trace`

## API Surface

- `POST /factory-runs/{factory_run_id}/artifacts`
- `GET /factory-runs/{factory_run_id}/artifacts`
- `GET /factory-artifacts/{factory_artifact_id}`

## Events

- `factory_artifact.created`
- `factory_artifact.updated`
- `factory_artifact.attached`

## Notes

- Artifacts are the audit trail for harness-driven development.
