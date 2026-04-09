# Sprint Contract

## Scope

Prove the stricter pre-baseline rule by requiring run artifact files to match their create-run template hashes before they are exempted.

## In Scope

- [x] Use only `tools/harness-runtime/artifacts/runs/sprint-006` as the touched path.
- [x] Keep pre-baseline artifact files identical to their create-run template hashes.
- [x] Pass `gate-close` under the stricter template-hash exemption rule.

## Out of Scope

- [x] Product code changes.
- [x] Harness changes outside `tools/harness-runtime/artifacts/runs/sprint-006`.
- [x] Manual baseline seeding.

## Touched Paths

- [x] tools/harness-runtime/artifacts/runs/sprint-006

## Acceptance Criteria

- [x] `gate-generator` captures the baseline automatically for `sprint-006`.
- [x] Pre-baseline run artifact files are only exempt when they still match the create-run template hashes.
- [x] `sprint-006` passes `gate-close` without manual baseline seeding.

## Evidence Required

- [x] `tools/harness-runtime/artifacts/runs/sprint-006/manifest.json`.
- [x] `tools/harness-runtime/scripts/runner.py`.
- [x] Command evidence from `python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-006` and `gate-close --run-id sprint-006`.

## Evaluator Checks

- [x] spec 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 밖 변경 없음
- [x] acceptance criteria 충족
