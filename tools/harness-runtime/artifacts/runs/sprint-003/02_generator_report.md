# Generator Report

## Changed Files

- tools/harness-runtime/README.md
- tools/harness-runtime/contracts/generator-report.template.md
- tools/harness-runtime/contracts/run-contract.template.json
- tools/harness-runtime/prompts/planner.system.md
- tools/harness-runtime/prompts/generator.system.md
- tools/harness-runtime/prompts/evaluator.system.md
- tools/harness-runtime/scripts/runner.py
- tools/harness-runtime/artifacts/runs/sprint-002/01_run_contract.json
- tools/harness-runtime/artifacts/runs/sprint-002/02_generator_report.md
- tools/harness-runtime/artifacts/runs/sprint-002/manifest.json
- tools/harness-runtime/artifacts/runs/sprint-003/00_spec_snapshot.md
- tools/harness-runtime/artifacts/runs/sprint-003/01_run_contract.json
- tools/harness-runtime/artifacts/runs/sprint-003/01_sprint_contract.md
- tools/harness-runtime/artifacts/runs/sprint-003/02_generator_report.md
- tools/harness-runtime/artifacts/runs/sprint-003/03_evaluator_report.md
- tools/harness-runtime/artifacts/runs/sprint-003/manifest.json

## Acceptance Mapping

- [x] AC-001 -> `tools/harness-runtime/contracts/run-contract.template.json` exists and defines objective, authoritative inputs, touched paths, and acceptance criteria.
- [x] AC-002 -> prompts and `tools/harness-runtime/scripts/runner.py` now read and validate `01_run_contract.json` as the authoritative execution contract.
- [x] AC-003 -> `tools/harness-runtime/artifacts/runs/sprint-002/01_run_contract.json` was added and `sprint-002` still passes harness gates.

## Commands Run

- python tools/harness-runtime/scripts/runner.py create-run --run-id sprint-003
- python tools/harness-runtime/scripts/runner.py validate-contract --run-id sprint-002
- python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-002
- python tools/harness-runtime/scripts/runner.py gate-close --run-id sprint-002
- python tools/harness-runtime/scripts/runner.py validate-contract --run-id sprint-003
- python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-003
- python tools/harness-runtime/scripts/runner.py gate-close --run-id sprint-003

## Open Risks

- The harness still trusts self-reported changed files; it does not yet compute them from git diff automatically.
