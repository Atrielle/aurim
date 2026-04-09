# Sprint Contract

## Scope

Make the harness measure changed files from a captured baseline and git-visible workspace state instead of trusting the generator report alone.

## In Scope

- [x] Capture a baseline snapshot for touched paths before coding begins.
- [x] Enforce generator changed-file reporting against measured changed files at close time.
- [x] Document the stricter baseline capture flow in the harness README.

## Out of Scope

- [x] Product backend or frontend feature changes.
- [x] Autonomous multi-agent runtime work beyond local harness gate enforcement.
- [x] Harness file changes outside the declared touched paths.

## Touched Paths

- [x] tools/harness-runtime/README.md
- [x] tools/harness-runtime/scripts/runner.py
- [x] tools/harness-runtime/artifacts/runs/sprint-004

## Acceptance Criteria

- [x] `gate-generator` captures a baseline snapshot for the declared touched paths before coding begins.
- [x] `gate-close` compares generator-reported changed files against actual changed files derived from baseline plus git-visible dirty state.
- [x] The README explains that `gate-generator` must run before coding to capture the baseline.
- [x] `sprint-004` passes the stricter harness gates.

## Evidence Required

- [x] `tools/harness-runtime/scripts/runner.py`.
- [x] `tools/harness-runtime/README.md`.
- [x] `tools/harness-runtime/artifacts/runs/sprint-004/manifest.json`.
- [x] Command evidence from `python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-004` and `gate-close --run-id sprint-004`.

## Evaluator Checks

- [x] spec 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 밖 변경 없음
- [x] acceptance criteria 충족
