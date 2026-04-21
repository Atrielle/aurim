# Unit Report

## Summary

Locked the canonical proof-run scope and backend validation file set against the first-slice contracts.

## Changed Files

- apps/backend/build.gradle.kts
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/model/Contracts.kt

## Acceptance Mapping

- [x] AC-001 -> The proof contract fixes the backend touched paths and runner evidence flow on the latest `work_units` schema.

## Evidence

- `tools/harness-runtime/artifacts/runs/sprint-014-proof/01_run_contract.json`
- `tools/harness-runtime/artifacts/runs/sprint-014-proof/01_sprint_contract.md`
