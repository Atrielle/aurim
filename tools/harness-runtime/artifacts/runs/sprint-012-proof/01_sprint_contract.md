# Sprint Contract

## Scope

Prove the runner-owned freeze and baseline proof flow against a real backend file by changing only `apps/backend/gradle.properties` after baseline capture.

## In Scope

- [x] Freeze a contract for one backend file plus this run directory.
- [x] Capture baseline through `gate-generator`.
- [x] Add one explanatory comment to `apps/backend/gradle.properties` after baseline capture.

## Out of Scope

- [x] Changing runtime behavior or dependency versions.
- [x] Editing any product file other than `apps/backend/gradle.properties`.
- [x] Editing `tools/harness-runtime/.runner-state/...`.

## Touched Paths

- [x] apps/backend/gradle.properties
- [x] tools/harness-runtime/artifacts/runs/sprint-012-proof

## Acceptance Criteria

- [x] AC-001: `freeze-contract`, `gate-generator`, and `gate-close` complete with runner-owned proof files present.
- [x] AC-002: The only product change after baseline capture is `apps/backend/gradle.properties`.

## Evidence Required

- [x] `tools/harness-runtime/.runner-state/freeze-proofs/sprint-012-proof.json`
- [x] `tools/harness-runtime/.runner-state/baseline-proofs/sprint-012-proof.json`
- [x] `python tools/harness-runtime/scripts/runner.py gate-close --run-id sprint-012-proof`

## Evaluator Checks

- [x] spec 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 밖 변경 없음
- [x] acceptance criteria 충족
