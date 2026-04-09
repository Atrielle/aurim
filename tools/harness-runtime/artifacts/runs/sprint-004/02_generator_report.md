# Generator Report

## Changed Files

- tools/harness-runtime/README.md
- tools/harness-runtime/scripts/runner.py
- tools/harness-runtime/artifacts/runs/sprint-004/02_generator_report.md

## Acceptance Mapping

- [x] AC-001 -> `gate-generator` now records `baseline_snapshot` and `baseline_git_dirty_files` in `tools/harness-runtime/artifacts/runs/sprint-004/manifest.json`.
- [x] AC-002 -> `tools/harness-runtime/scripts/runner.py` now measures changed files from baseline and rejects generator reports that diverge from measured changes or current git-visible dirty files.
- [x] AC-003 -> `tools/harness-runtime/README.md` now states that `gate-generator` must run before coding so the baseline is captured.
- [x] AC-004 -> `sprint-004` reached `validate-contract` and `gate-generator` successfully before close evaluation.

## Commands Run

- python tools/harness-runtime/scripts/runner.py validate-contract --run-id sprint-004
- python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-004
- python tools/harness-runtime/scripts/runner.py gate-close --run-id sprint-004

## Open Risks

- The harness still relies on the operator to run `gate-generator` before editing any touched file.
