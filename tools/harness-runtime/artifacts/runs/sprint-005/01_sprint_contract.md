# Sprint Contract

## Scope

Prove the pure automatic harness path by using only the sprint-005 run directory, capturing the baseline through gate-generator, and closing the run without any manual baseline seed.

## In Scope

- [x] Use only `tools/harness-runtime/artifacts/runs/sprint-005` as the touched path.
- [x] Run `gate-generator` before editing generator and evaluator artifacts.
- [x] Pass `gate-close` under measured changed-file enforcement.

## Out of Scope

- [x] Product code changes.
- [x] Harness changes outside `tools/harness-runtime/artifacts/runs/sprint-005`.
- [x] Manual baseline seeding.

## Touched Paths

- [x] tools/harness-runtime/artifacts/runs/sprint-005

## Acceptance Criteria

- [x] `gate-generator` captures the baseline automatically for `sprint-005`.
- [x] The generator report lists only measured post-baseline changed files.
- [x] `sprint-005` passes `gate-close` without manual baseline seeding.

## Evidence Required

- [x] `tools/harness-runtime/artifacts/runs/sprint-005/manifest.json`.
- [x] `tools/harness-runtime/artifacts/runs/sprint-005/02_generator_report.md`.
- [x] Command evidence from `python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-005` and `gate-close --run-id sprint-005`.

## Evaluator Checks

- [x] spec 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 밖 변경 없음
- [x] acceptance criteria 충족
