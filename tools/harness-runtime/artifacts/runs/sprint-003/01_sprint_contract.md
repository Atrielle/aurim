# Sprint Contract

## Scope

Tighten the harness so subagents execute against a machine-readable run contract rather than only a markdown summary.

## In Scope

- [x] Add a JSON run contract template with explicit objective, authoritative inputs, touched paths, and acceptance criteria.
- [x] Update harness prompts and runner validation to treat the JSON run contract as authoritative.
- [x] Backfill `sprint-002` to the new format and prove the stricter flow still passes local gates.

## Out of Scope

- [x] Product backend or frontend feature expansion beyond the current first slice.
- [x] Replacing the harness with a fully autonomous planner-generator-evaluator runtime.
- [x] Any harness file changes outside the declared touched paths.

## Touched Paths

- [x] tools/harness-runtime/README.md
- [x] tools/harness-runtime/contracts/generator-report.template.md
- [x] tools/harness-runtime/contracts/run-contract.template.json
- [x] tools/harness-runtime/prompts/planner.system.md
- [x] tools/harness-runtime/prompts/generator.system.md
- [x] tools/harness-runtime/prompts/evaluator.system.md
- [x] tools/harness-runtime/scripts/runner.py
- [x] tools/harness-runtime/artifacts/runs/sprint-002
- [x] tools/harness-runtime/artifacts/runs/sprint-003

## Acceptance Criteria

- [x] Harness runs have a machine-readable JSON execution contract template.
- [x] Harness prompts and runner enforce the JSON run contract as the authoritative scope and evidence contract.
- [x] Completed runs can be backfilled to the stricter contract format and still pass local gates.

## Evidence Required

- [x] `tools/harness-runtime/contracts/run-contract.template.json`.
- [x] `tools/harness-runtime/prompts/planner.system.md`, `generator.system.md`, and `evaluator.system.md`.
- [x] `tools/harness-runtime/scripts/runner.py`.
- [x] `tools/harness-runtime/artifacts/runs/sprint-002/01_run_contract.json`.
- [x] Command evidence from `python tools/harness-runtime/scripts/runner.py validate-contract --run-id sprint-002`, `gate-generator --run-id sprint-002`, `gate-close --run-id sprint-002`, and the same gate sequence for `sprint-003`.

## Evaluator Checks

- [x] spec 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 밖 변경 없음
- [x] acceptance criteria 충족
