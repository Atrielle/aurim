# Sprint Contract

## Scope

Validate the explicit freeze-contract flow by authoring the run contract, freezing it, then running baseline capture and close under the frozen snapshot.

## In Scope

- [x] Author the run contract files in `tools/harness-runtime/artifacts/runs/sprint-007`.
- [x] Run `freeze-contract` before `gate-generator`.
- [x] Pass `gate-close` after frozen-contract and baseline capture.

## Out of Scope

- [x] Product code changes.
- [x] Manual baseline seeding.
- [x] Harness changes outside the sprint-007 run directory.

## Touched Paths

- [x] tools/harness-runtime/artifacts/runs/sprint-007

## Acceptance Criteria

- [x] The authored run contract can be frozen with `freeze-contract` before baseline capture.
- [x] `gate-generator` only accepts the frozen contract state and captures a baseline automatically.
- [x] `gate-close` succeeds after the `freeze-contract` step.

## Evidence Required

- [x] `tools/harness-runtime/artifacts/runs/sprint-007/manifest.json`.
- [x] `python tools/harness-runtime/scripts/runner.py freeze-contract --run-id sprint-007`.
- [x] `python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-007`.
- [x] `python tools/harness-runtime/scripts/runner.py gate-close --run-id sprint-007`.

## Evaluator Checks

- [x] spec 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 밖 변경 없음
- [x] acceptance criteria 충족
