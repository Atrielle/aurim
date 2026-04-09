# Sprint Contract

## Scope

Attempt to bypass `freeze-contract` by editing only run artifacts and manifest metadata before `gate-generator`.

## In Scope

- [x] Fill the contract files.
- [x] Forge manifest freeze metadata without calling `freeze-contract`.

## Out of Scope

- [x] Calling `freeze-contract`.
- [x] Editing runner-owned proof files.

## Touched Paths

- [x] tools/harness-runtime/artifacts/runs/sprint-011-bypass

## Acceptance Criteria

- [x] AC-001: `gate-generator` fails because no runner-owned freeze proof exists.

## Evidence Required

- [x] `python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-011-bypass` fails.

## Evaluator Checks

- [x] spec 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 밖 변경 없음
- [x] acceptance criteria 충족
