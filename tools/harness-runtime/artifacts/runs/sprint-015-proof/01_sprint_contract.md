# Sprint Contract

## Scope

Create one current-main canonical proof run with latest `work_units` coverage, then use that run to drive backend first-slice request validation into line with the authoritative contracts.

## In Scope

- [x] Freeze a canonical proof contract for `sprint-015-proof`.
- [x] Exercise `plan-units`, `dispatch-unit`, `collect-unit`, `gate-units`, `gate-generator`, and `gate-close` on the latest runner schema.
- [x] Align backend request validation for representative first-slice endpoints.
- [x] Add backend regression tests for invalid request payloads.

## Out of Scope

- [x] Any stack change or domain-boundary change.
- [x] Any harness expansion toward autonomous long-running orchestration.
- [x] Any feature work outside the first vertical slice.

## Touched Paths

- [x] apps/backend/build.gradle.kts
- [x] apps/backend/src

## Acceptance Criteria

- [x] AC-001: canonical proof run completes on current main through freeze, unit planning/collection, baseline capture, and close gate using the latest `work_units` schema.
- [x] AC-002: backend request validation rejects contract-invalid payloads on representative first-slice endpoints before service logic proceeds.

## Evidence Required

- [x] `tools/harness-runtime/artifacts/runs/sprint-015-proof/04_unit_plan.json`
- [x] `tools/harness-runtime/artifacts/runs/sprint-015-proof/05_unit_reports/WU-001.dispatch.json`
- [x] `tools/harness-runtime/artifacts/runs/sprint-015-proof/05_unit_reports/WU-001.evidence.json`
- [x] `tools/harness-runtime/.runner-state/freeze-proofs/sprint-015-proof.json`
- [x] `tools/harness-runtime/.runner-state/baseline-proofs/sprint-015-proof.json`
- [x] `apps/backend/src/test/kotlin/io/atrielle/aurim/backend/api/ContractValidationTest.kt`
- [x] `apps/backend/gradlew.bat test`

## Work Units

- [x] WU-001 | 목적: canonical proof contract와 backend validation change set을 고정 | AC: AC-001 | 경로: apps/backend/build.gradle.kts, apps/backend/src | 선행: 없음 | 예산: input 12000 / output 3000
- [x] WU-002 | 목적: backend contract validation과 테스트 구현 | AC: AC-002 | 경로: apps/backend/build.gradle.kts, apps/backend/src | 선행: WU-001 | 예산: input 16000 / output 4000

## Unit Dependencies

- [x] WU-001 <- (none)
- [x] WU-002 <- WU-001

## Evaluator Checks

- [x] spec 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 밖 변경 없음
- [x] acceptance criteria 충족
