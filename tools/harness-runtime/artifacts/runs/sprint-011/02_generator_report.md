# Generator Report

## Changed Files

- apps/backend/src/main/resources/application.yml
- tools/harness-runtime/artifacts/runs/sprint-011/02_generator_report.md

## Acceptance Mapping

- [x] AC-001 -> `freeze-contract`, `gate-generator`, and `gate-close` ran in order; `tools/harness-runtime/.runner-state/freeze-proofs/sprint-011.json` and `manifest.json` are runner-authored evidence for freeze provenance and completion.
- [x] AC-002 -> Only `apps/backend/src/main/resources/application.yml` was changed as the product file after baseline capture; no other product path was touched.

## Commands Run

- `python tools/harness-runtime/scripts/runner.py validate-contract --run-id sprint-011`
- `python tools/harness-runtime/scripts/runner.py freeze-contract --run-id sprint-011`
- `python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-011`
- `apps/backend/gradlew.bat test`

## Open Risks

- `apps/backend` as a directory is still dirty in the wider worktree, so this proof run intentionally scoped itself to the single clean file `apps/backend/src/main/resources/application.yml`.
