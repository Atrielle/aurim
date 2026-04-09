# Sprint Contract

## Scope

Contract-first first slice for Aurim: materialize OpenAPI and JSON Schema, then align the Kotlin backend to the workspace, git workspace, factory spec, factory run, and factory artifact boundaries.

## In Scope

- [x] Create concrete OpenAPI and JSON Schema files under `packages/contracts/` for the first vertical slice.
- [x] Replace backend fixture responses with controller, service, repository, and Flyway persistence skeletons that match the contracts.
- [x] Capture this sprint in harness artifacts and verify the run with local harness gates.

## Out of Scope

- [x] Frontend implementation for Factory App or Artifact Viewer UI.
- [x] Auth, search, realtime, or storage engine selection beyond current contract placeholders.
- [x] Running planner, generator, or evaluator inside the product request path.

## Touched Paths

- [x] apps/backend/src/main/kotlin/io/atrielle/aurim/backend/api
- [x] apps/backend/src/main/kotlin/io/atrielle/aurim/backend/model
- [x] apps/backend/src/main/kotlin/io/atrielle/aurim/backend/persistence
- [x] apps/backend/src/main/kotlin/io/atrielle/aurim/backend/service
- [x] apps/backend/src/main/resources/db/migration
- [x] packages/contracts/openapi
- [x] packages/contracts/schemas
- [x] tools/harness-runtime/artifacts/runs/sprint-002

## Acceptance Criteria

- [x] `packages/contracts/` contains concrete OpenAPI and JSON Schema files for workspace, git workspace, factory spec, factory run, and factory artifact.
- [x] Backend exposes the first-slice endpoints through contract-aligned controllers backed by service and R2DBC repository skeletons.
- [x] Flyway includes first-slice persistence tables and `apps/backend/gradlew.bat test` completes successfully.
- [x] Harness run artifacts for this sprint are complete enough to pass local gate validation.

## Evidence Required

- [x] OpenAPI file at `packages/contracts/openapi/aurim-first-slice.v0.yaml`.
- [x] JSON Schema files under `packages/contracts/schemas/`.
- [x] Backend Kotlin changes under `apps/backend/src/main/kotlin/io/atrielle/aurim/backend/`.
- [x] Flyway migration at `apps/backend/src/main/resources/db/migration/V2__first_slice_contracts.sql`.
- [x] Command evidence from `apps/backend/gradlew.bat test`, `python tools/harness-runtime/scripts/runner.py validate-contract --run-id sprint-002`, `python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-002`, and `python tools/harness-runtime/scripts/runner.py gate-close --run-id sprint-002`.

## Evaluator Checks

- [x] spec 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 밖 변경 없음
- [x] acceptance criteria 충족
