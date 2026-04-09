# Sprint Contract

## Scope

Close a clean harness run that touches one real backend product file and proves the runner writes completion evidence into manifest.json.

## In Scope

- [x] Close one clean harness run whose touched paths are limited to this run directory and `apps/backend/build.gradle.kts`.
- [x] Add one non-functional clarification comment to `apps/backend/build.gradle.kts` after baseline capture.

## Out of Scope

- [x] Do not change backend runtime behavior, dependency versions, or compiler targets.
- [x] Do not modify any other `apps/backend/...` files.

## Touched Paths

- [x] tools/harness-runtime/artifacts/runs/sprint-010
- [x] apps/backend/build.gradle.kts

## Acceptance Criteria

- [x] `sprint-010` closes through `freeze-contract`, `gate-generator`, and `gate-close`, and `manifest.json` shows runner-authored completion evidence.
- [x] `apps/backend/build.gradle.kts` changes only by a clarification comment about the Java 25 toolchain and Kotlin JVM 23 bytecode target mismatch.

## Evidence Required

- [x] `tools/harness-runtime/artifacts/runs/sprint-010/manifest.json`
- [x] `python tools/harness-runtime/scripts/runner.py gate-close --run-id sprint-010`
- [x] `apps/backend/build.gradle.kts`
- [x] `git diff -- apps/backend/build.gradle.kts`

## Evaluator Checks

- [x] spec 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 밖 변경 없음
- [x] acceptance criteria 충족
