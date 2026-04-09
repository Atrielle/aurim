# Generator Report

## Changed Files

- tools/harness-runtime/artifacts/runs/sprint-005/02_generator_report.md

## Acceptance Mapping

- [x] AC-001 -> `manifest.json` was updated by `gate-generator` with an automatic baseline capture.
- [x] AC-002 -> the only measured post-baseline changed file is this generator report, and it is the only file listed here.
- [x] AC-003 -> the run is prepared for `gate-close` without any manual baseline seed.

## Commands Run

- python tools/harness-runtime/scripts/runner.py validate-contract --run-id sprint-005
- python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-005
- python tools/harness-runtime/scripts/runner.py gate-close --run-id sprint-005

## Open Risks

- The run proves the automatic path on artifact-only scope, not on product code paths.
