# Backend (Product Core)

이 디렉터리는 Aurim 플랫폼 API 코드베이스 경계다.

## Target Stack

- `Kotlin`
- `Spring Boot`
- `Spring WebFlux`
- `Kotlin Coroutines`
- `Spring Data R2DBC`
- `PostgreSQL`
- `Flyway`
- `Java 25`
- `Gradle Kotlin DSL`

## Why This Stack

- Web and mobile share one product-owned API and domain model.
- Backend remains modular-monolith first.
- WebFlux를 유지하므로 DB 접근도 `R2DBC`로 맞춘다.
- 코루틴을 사용해 reactive 코드를 직접 다루는 복잡도를 낮춘다.
- PostgreSQL은 운영 메타데이터의 system of record다.
- Flyway는 DB 스키마 변경 이력을 버전 관리하기 위한 기본 도구다.

## Current Status

현재 이 디렉터리의 구현은 목표 스택으로 완전히 이행되기 전의 임시 부트스트랩일 수 있다.
이 경계에서는 Python/FastAPI 방향으로 기능을 확장하지 않는다.
다음 실제 작업은 Kotlin Spring 기반으로 재정렬하는 것이다.

## Contract Rules

- backend는 플랫폼이 직접 소유하는 도메인 규칙과 메타데이터 계약을 노출한다.
- auth/search/storage/git/realtime은 adapter 경계 뒤에 둔다.
- contract source of truth는 `packages/contracts/` 아래 `OpenAPI + JSON Schema`다.
- 하네스 artifact 없이 scope를 늘리지 않는다.

## First Slice Focus

- Workspace
- Git Workspace binding
- Factory Spec
- Factory Run
- Artifact Viewer
