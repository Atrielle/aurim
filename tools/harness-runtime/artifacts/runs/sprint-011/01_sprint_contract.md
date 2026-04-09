# Sprint Contract

## Scope

Prove the hardened harness flow against a real backend config file by freezing the contract first, then changing only `apps/backend/src/main/resources/application.yml` after baseline capture.

## In Scope

- [x] Freeze a contract that allows exactly one backend product file plus this run directory.
- [x] Capture baseline through `gate-generator` before editing the backend file.
- [x] Add one non-behavioral clarification comment to `apps/backend/src/main/resources/application.yml`.

## Out of Scope

- [x] Changing ports, credentials, dependency versions, or runtime behavior.
- [x] Editing any other product file outside `apps/backend/src/main/resources/application.yml`.
- [x] Editing harness core files in `tools/harness-runtime/scripts` or `tools/harness-runtime/README.md`.

## Touched Paths

- [x] apps/backend/src/main/resources/application.yml
- [x] tools/harness-runtime/artifacts/runs/sprint-011

## Acceptance Criteria

- [x] AC-001: The run closes successfully with runner-owned freeze proof and runner-authored manifest completion evidence.
- [x] AC-002: The only product change after baseline capture is `apps/backend/src/main/resources/application.yml`.

## Evidence Required

- [x] `tools/harness-runtime/.runner-state/freeze-proofs/sprint-011.json` exists and matches the frozen contract state.
- [x] `tools/harness-runtime/artifacts/runs/sprint-011/manifest.json` shows `completed_gates` and `status` after `gate-close`.
- [x] `tools/harness-runtime/artifacts/runs/sprint-011/02_generator_report.md` lists only `apps/backend/src/main/resources/application.yml` as the product file changed after baseline.
- [x] `python tools/harness-runtime/scripts/runner.py gate-close --run-id sprint-011` returns success.

## Evaluator Checks

- [x] spec snapshot 기준 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 준수
- [x] acceptance criteria 충족
