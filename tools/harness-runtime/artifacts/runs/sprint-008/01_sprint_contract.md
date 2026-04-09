# Sprint Contract

## Scope

Prove that the runner itself owns manifest completion evidence on a clean artifact-only run.

## In Scope

- [x] Use only `tools/harness-runtime/artifacts/runs/sprint-008` as the touched path.
- [x] Run `freeze-contract`, `gate-generator`, and `gate-close` in order.
- [x] Verify that `manifest.json` reflects runner-authored gate completion.

## Out of Scope

- [x] Product code changes.
- [x] Harness changes outside `tools/harness-runtime/artifacts/runs/sprint-008`.
- [x] Manual edits to manifest completion fields.

## Touched Paths

- [x] tools/harness-runtime/artifacts/runs/sprint-008

## Acceptance Criteria

- [x] `freeze-contract` writes its own completion evidence into `manifest.json`.
- [x] `gate-generator` writes its own completion evidence into `manifest.json`.
- [x] `gate-close` writes `status: passed` and `completed_gates` into `manifest.json`.

## Evidence Required

- [x] `tools/harness-runtime/artifacts/runs/sprint-008/manifest.json`.
- [x] Command evidence from `python tools/harness-runtime/scripts/runner.py freeze-contract --run-id sprint-008`, `gate-generator --run-id sprint-008`, and `gate-close --run-id sprint-008`.

## Evaluator Checks

- [x] spec 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 밖 변경 없음
- [x] acceptance criteria 충족
