# Sprint Contract

## Scope

Prove the hardened harness flow against a real backend file by freezing the contract first, then changing only `apps/backend/build.gradle.kts` after baseline capture.

## In Scope

- [x] Freeze a contract that allows exactly one backend product file plus this run directory.
- [x] Capture baseline through `gate-generator` before editing the backend file.
- [x] Add one non-behavioral clarification comment to `apps/backend/build.gradle.kts`.

## Out of Scope

- [x] Changing dependency versions, JVM targets, or runtime behavior.
- [x] Editing any other product file outside `apps/backend/build.gradle.kts`.
- [x] Editing harness core files in `tools/harness-runtime/scripts` or `tools/harness-runtime/README.md`.

## Touched Paths

- [x] apps/backend/build.gradle.kts
- [x] tools/harness-runtime/artifacts/runs/sprint-009

## Acceptance Criteria

- [x] AC-001: The run closes successfully through `gate-close` with manifest completion evidence written by the runner.
- [x] AC-002: The only product change after baseline capture is `apps/backend/build.gradle.kts`.

## Evidence Required

- [x] `tools/harness-runtime/artifacts/runs/sprint-009/manifest.json` shows `completed_gates` and `status` after `gate-close`.
- [x] `tools/harness-runtime/artifacts/runs/sprint-009/02_generator_report.md` lists only `apps/backend/build.gradle.kts` as the product file changed after baseline.
- [x] `python tools/harness-runtime/scripts/runner.py gate-close --run-id sprint-009` returns success.

## Evaluator Checks

- [x] spec snapshot 기준 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 밖 변경 없음
- [x] acceptance criteria 충족
