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
- Flyway는 JDBC datasource를 사용하고, 앱 런타임은 R2DBC를 사용한다.

## Current Status

이 디렉터리는 현재 Kotlin/Spring Boot 스켈레톤으로 전환되었다.
`/health`와 `/platform-contract` 엔드포인트가 동작하는 최소 구조를 제공한다.

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
