# Generator Report

## Changed Files

- apps/backend/build.gradle.kts
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/api/FactoryArtifactController.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/api/FactoryRunController.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/api/FactorySpecController.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/api/GitWorkspaceController.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/api/WorkspaceController.kt
- apps/backend/src/main/kotlin/io/atrielle/aurim/backend/model/Contracts.kt
- apps/backend/src/test/kotlin/io/atrielle/aurim/backend/api/ContractValidationTest.kt

## Acceptance Mapping

- [x] AC-001 -> `sprint-015-proof` completed `plan-units`, `dispatch-unit`, `collect-unit`, `gate-units`, `freeze-contract`, and `gate-generator` on the latest `work_units` schema, with runner-owned proof files captured under `.runner-state`.
- [x] AC-002 -> backend request DTOs now carry contract-aligned validation constraints, controllers enforce `@Valid`, and `apps/backend/gradlew.bat test` passes with representative validation regression coverage.

## Commands Run

- python tools/harness-runtime/scripts/runner.py validate-contract --run-id sprint-015-proof
- python tools/harness-runtime/scripts/runner.py plan-units --run-id sprint-015-proof
- python tools/harness-runtime/scripts/runner.py dispatch-unit --run-id sprint-015-proof --unit-id WU-001
- python tools/harness-runtime/scripts/runner.py collect-unit --run-id sprint-015-proof --unit-id WU-001 --report tools/harness-runtime/artifacts/runs/sprint-015-proof/wu-001-source.md
- python tools/harness-runtime/scripts/runner.py dispatch-unit --run-id sprint-015-proof --unit-id WU-002
- python tools/harness-runtime/scripts/runner.py collect-unit --run-id sprint-015-proof --unit-id WU-002 --report tools/harness-runtime/artifacts/runs/sprint-015-proof/wu-002-source.md
- python tools/harness-runtime/scripts/runner.py gate-units --run-id sprint-015-proof
- python tools/harness-runtime/scripts/runner.py freeze-contract --run-id sprint-015-proof
- python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-015-proof
- apps/backend/gradlew.bat test

## Open Risks

- Gradle still warns that Kotlin emits JVM 23 bytecode under the Java 25 toolchain. This is the documented temporary state in the repo, not a new regression.
