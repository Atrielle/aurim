# Resume Context

## Read Order

내일이나 다음 세션에서 새 에이전트가 시작할 때는 아래 순서로 읽는다.

1. `README.md`
2. `docs/foundation/cloud-handoff.md`
3. `docs/foundation/product-philosophy.md`
4. `docs/foundation/governance-model.md`
5. `docs/foundation/ui-direction.md`
6. `docs/foundation/resume-context.md`
7. `docs/foundation/design-system.md`
8. `packages/contracts/*.v0.md`
9. `apps/backend/build.gradle.kts`

## Current State Summary

- repository: `Atrielle/aurim`
- monorepo shape is fixed
- frontend target: `React + TypeScript + Vite`
- backend target: `Kotlin + Spring Boot + WebFlux + Coroutines + R2DBC + Flyway`
- database: `PostgreSQL`
- contract source of truth: `OpenAPI + JSON Schema`
- harness runtime: `Python`
- first vertical slice target:
  - Workspace
  - Git Workspace binding
  - Factory Spec
  - Factory Run
  - Artifact Viewer

## What Was Completed Last

- backend Python bootstrap was removed
- backend Kotlin Spring skeleton was added
- Gradle wrapper was added
- backend `gradlew.bat test` was verified on Windows
- first-slice v0 contract draft documents were added under `packages/contracts/`
- core foundation docs were updated to the agreed stack and boundary rules

## Important Caveat

JDK is `25`, but Kotlin currently falls back to `JVM_23` bytecode target.
This is currently tolerated via `apps/backend/gradle.properties`.
Do not silently remove that detail without checking Kotlin support status.

## Immediate Next Step

Do not redesign the architecture.
Do not widen scope.
The next concrete task is:

- create actual `OpenAPI` and `JSON Schema` files under `packages/contracts/`
- then implement backend first-slice API skeleton against those contracts

## Prompt To Start Next Session

Use this as the first message if needed:

```text
Read these files first and treat them as authoritative:
- README.md
- docs/foundation/cloud-handoff.md
- docs/foundation/product-philosophy.md
- docs/foundation/governance-model.md
- docs/foundation/ui-direction.md
- docs/foundation/resume-context.md
- docs/foundation/design-system.md

Keep the current monorepo shape.
Do not reintroduce Python backend code.
Do not change the agreed stack.
Do not widen scope beyond the first vertical slice.

Start with packages/contracts as the source of truth.
Create actual OpenAPI and JSON Schema files for workspace, git workspace, factory spec, factory run, and factory artifact.
Then wire backend API skeletons to those contracts.
Before coding, summarize current repo state and the exact touched paths.
```
