# Generator Report

## Changed Files

- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/api/PlatformController.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/api/WorkspaceController.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/api/GitWorkspaceController.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/api/FactorySpecController.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/api/FactoryRunController.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/api/FactoryArtifactController.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/model/Contracts.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/persistence/JsonListCodec.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/persistence/WorkspaceRepository.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/persistence/GitWorkspaceRepository.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/persistence/FactorySpecRepository.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/persistence/FactoryRunRepository.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/persistence/FactoryArtifactRepository.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/service/WorkspaceService.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/service/GitWorkspaceService.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/service/FactorySpecService.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/service/FactoryRunService.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/service/FactoryArtifactService.kt
- apps/backend/src/main/resources/db/migration/V2__first_slice_contracts.sql
- packages/contracts/openapi/aurim-first-slice.v0.yaml
- packages/contracts/schemas/workspace.schema.json
- packages/contracts/schemas/create-workspace-request.schema.json
- packages/contracts/schemas/update-workspace-request.schema.json
- packages/contracts/schemas/git-workspace.schema.json
- packages/contracts/schemas/create-git-workspace-request.schema.json
- packages/contracts/schemas/update-git-workspace-request.schema.json
- packages/contracts/schemas/factory-spec.schema.json
- packages/contracts/schemas/create-factory-spec-request.schema.json
- packages/contracts/schemas/update-factory-spec-request.schema.json
- packages/contracts/schemas/factory-run.schema.json
- packages/contracts/schemas/create-factory-run-request.schema.json
- packages/contracts/schemas/close-factory-run-request.schema.json
- packages/contracts/schemas/factory-artifact.schema.json
- packages/contracts/schemas/create-factory-artifact-request.schema.json
- tools/harness-runtime/artifacts/runs/sprint-002/00_spec_snapshot.md
- tools/harness-runtime/artifacts/runs/sprint-002/01_sprint_contract.md
- tools/harness-runtime/artifacts/runs/sprint-002/02_generator_report.md
- tools/harness-runtime/artifacts/runs/sprint-002/03_evaluator_report.md
- tools/harness-runtime/artifacts/runs/sprint-002/manifest.json

## Acceptance Mapping

- [x] AC-001 -> `packages/contracts/openapi/aurim-first-slice.v0.yaml` and `packages/contracts/schemas/*.json` exist.
- [x] AC-002 -> controllers, services, repositories, and DTOs were added under `apps/backend/src/main/kotlin/io/atrielle/aurim/backend/`.
- [x] AC-003 -> `apps/backend/src/main/resources/db/migration/V2__first_slice_contracts.sql` exists and `.\gradlew.bat test` completed successfully.
- [x] AC-004 -> this run directory contains completed contract, generator, and evaluator artifacts and the harness gates passed.

## Commands Run

- .\gradlew.bat test
- python tools/harness-runtime/scripts/runner.py create-run --run-id sprint-002
- python tools/harness-runtime/scripts/runner.py validate-contract --run-id sprint-002
- python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-002
- python tools/harness-runtime/scripts/runner.py gate-close --run-id sprint-002

## Open Risks

- Runtime API verification against a live PostgreSQL instance has not been executed yet.
- Kotlin bytecode target remains `JVM_23` while the Java toolchain is `25`.
