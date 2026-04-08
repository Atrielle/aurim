# Atrielle Aurim Monorepo

이 저장소는 `Atrielle` 브랜드의 `Aurim` 제품과 그 제품을 통제된 방식으로 개발하기 위한 하네스를 함께 담는 모노레포다.

## Repository Shape

- `apps/frontend/`: Aurim 사용자 제품 UI
- `apps/backend/`: Aurim 플랫폼 API
- `tools/harness-runtime/`: spec-driven AI harness runtime
- `packages/contracts/`: OpenAPI와 JSON Schema 기준 원본
- `packages/sdk/`: contracts에서 파생되는 SDK 경계
- `docs/foundation/`: 철학, 거버넌스, 핸드오프 문서

## Agreed Target Stack

- Frontend: `React + TypeScript + Vite`
- Backend: `Kotlin + Spring Boot + WebFlux + Coroutines + R2DBC`
- Database: `PostgreSQL`
- Database migration: `Flyway`
- Contracts source of truth: `OpenAPI + JSON Schema`
- Harness runtime: `Python`
- JDK: `Java 25`
- Build: `Gradle Kotlin DSL`

## Current Implementation Note

현재 `apps/backend/`에는 초기 부트스트랩 잔재가 남아 있을 수 있다.
하지만 기준 문서상 백엔드 목표 스택은 `Kotlin + Spring Boot + WebFlux + Coroutines + R2DBC + Flyway` 이며,
이 경계 밖으로 Python 백엔드를 확장하지 않는다.

## Non-Negotiable Rules

- Aurim 제품 코어와 AI harness runtime은 같은 저장소여도 별도 도메인이다.
- PostgreSQL만 초기 고정 system of record다.
- auth, search, storage, git, realtime 같은 엔진은 반드시 계약 뒤에서 교체 가능해야 한다.
- 완성형 OSS 제품을 그대로 제품으로 채택하지 않는다.
- 제품 서버 request path에 planner, generator, evaluator 런타임을 직접 넣지 않는다.

## Read First

1. `docs/foundation/product-philosophy.md`
2. `docs/foundation/governance-model.md`
3. `docs/foundation/cloud-handoff.md`
4. `docs/foundation/ui-direction.md`
5. `docs/foundation/resume-context.md`
6. `docs/foundation/design-system.md`

## Recommended First Vertical Slice

- Workspace
- Git Workspace binding
- Factory Spec
- Factory Run
- Artifact Viewer

## Harness Entry

1. `tools/harness-runtime/specs/product-spec.md`를 채운다.
2. `python tools/harness-runtime/scripts/runner.py create-run --run-id sprint-001`
3. run artifact를 기준으로 planner / generator / evaluator를 수행한다.
4. `gate-close`가 PASS되기 전에는 완료로 간주하지 않는다.
