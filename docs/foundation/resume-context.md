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
8. `docs/foundation/decision-status.md`
9. `packages/contracts/*.v0.md`
10. `apps/backend/build.gradle.kts`

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

## Harness Assessment (Latest)

- 현재 `tools/harness-runtime/`는 예전 단순 `runner.py` 한 파일 상태가 아니다.
- 최신 `main` 기준 하네스는 `harness_core/`로 모듈 분리되어 있고, `freeze-contract`, `plan-units`, `dispatch-unit`, `collect-unit`, `gate-units`, `gate-generator`, `gate-close` 흐름을 가진다.
- `unit_gate_regression.py`와 `governance_audit.py --run-regression`는 현재 통과한다.
- 예전 리뷰에서 반복되던 `manifest self-report`, `freeze-contract bypass`, `contract authoring deadlock` 지적은 최신 코드에 그대로 적용되지 않는다.
- 다만 이것을 Anthropic의 long-running application harness 수준으로 과장하면 안 된다.
- 현재 상태는 `governance-heavy harness runtime shell`에 가깝고, 완전한 `planner / generator / evaluator autonomous loop`는 아직 아니다.
- 즉 지금 하네스는 `AI 실행 통제와 증빙` 쪽은 강하지만, `장시간 자율 실행 오케스트레이션`은 아직 비어 있다.

## Harness vs Anthropic

- Anthropic 글 기준의 핵심은:
  - planner / generator / evaluator 3-agent 실행 구조
  - sprint contract 협상
  - evaluator의 실제 앱 검증
  - generator가 evaluator 피드백으로 iteration
  - 장시간 세션 orchestration
- 현재 Aurim 하네스는 위 중에서:
  - artifact handoff
  - sprint/run contract
  - gate enforcement
  - evidence/proof separation
  - touched paths control
  를 구현한 상태다.
- 아직 부족한 것은:
  - 실제 agent loop orchestration
  - evaluator-driven retry loop
  - long-running worker/session management
  - canonical end-to-end proof run의 최신 schema 정렬

## What Was Completed Last

- backend Python bootstrap was removed
- backend Kotlin Spring skeleton was added
- Gradle wrapper was added
- backend `gradlew.bat test` was verified on Windows
- first-slice v0 contract draft documents were added under `packages/contracts/`
- core foundation docs were updated to the agreed stack and boundary rules
- harness runtime was modularized into `tools/harness-runtime/scripts/harness_core/`
- governance audit script and UI console flow were added
- harness refactor roadmap Phase 0~4 was closed

## Important Caveat

JDK is `25`, but Kotlin currently falls back to `JVM_23` bytecode target.
This is currently tolerated via `apps/backend/gradle.properties`.
Do not silently remove that detail without checking Kotlin support status.

## Immediate Next Step

Do not redesign the architecture.
Do not widen scope.
The next concrete task is:

- do not relitigate old harness review findings unless they reproduce on current `main`
- create one canonical proof run that matches the latest runner schema, including `work_units`
- if the harness proof run is green, move focus back to backend/frontend first-slice implementation
- verify existing `OpenAPI` and `JSON Schema` are kept authoritative and compatible
- implement/align backend first-slice API behavior against those contracts

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
- docs/foundation/decision-status.md

Keep the current monorepo shape.
Do not reintroduce Python backend code.
Do not change the agreed stack.
Do not widen scope beyond the first vertical slice.

Start with packages/contracts as the source of truth.
Keep OpenAPI and JSON Schema for workspace, git workspace, factory spec, factory run, and factory artifact as the source of truth.
Then wire/align backend API skeletons and behavior to those contracts.
Before coding, summarize current repo state, decision-status(Decided/Pending), the exact touched paths, and whether you are working on harness governance or product implementation.
```
