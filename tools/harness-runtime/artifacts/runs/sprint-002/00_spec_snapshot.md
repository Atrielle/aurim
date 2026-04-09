# Product Spec

## Product Name

Aurim

## Problem Statement

협업 제품과 개발 생산 시스템이 분리되지 않으면 제품 도메인과 내부 공장 도메인이 서로 오염된다.
Aurim은 문서, 파일, 작업, 일정, 활동, Git 연계를 한 플랫폼에 모으되,
AI 기반 개발 자동화는 별도 harness runtime으로 통제해야 한다.
우리는 상업적으로 안전하고 교체 가능한 OSS 엔진 위에서 제품 규칙과 데이터 소유권을 직접 가져야 한다.

## Product Goal

기업용 협업 플랫폼 코어와 개발자용 Factory App을 같은 제품 안에서 제공하되,
실제 planner, generator, evaluator 실행은 별도 하네스 런타임으로 관리한다.

## Non-Negotiable Constraints

- PostgreSQL is the metadata system of record.
- Frontend and backend are separate product codebases inside one monorepo.
- UI and domain rules are product-owned.
- Engines must stay replaceable behind contracts.
- Contract source of truth is OpenAPI plus JSON Schema.
- Frontend stack is React plus TypeScript.
- Backend target stack is Kotlin plus Spring Boot plus WebFlux plus Coroutines plus R2DBC.
- Database migration uses Flyway.
- Harness runtime uses Python.
- Product core and harness runtime remain separate domains.

## Core Domain Rules

- Workspace boundary
- Permission relationship model
- Work Item single model
- Document revision policy
- File revision policy
- Event schema ownership
- Git workspace linkage rule
- Factory App metadata ownership

## Initial Scope

이번 러닝에서 반드시 만들 범위만 적는다.
기본 권장 범위는 Workspace, Git Workspace, Factory Spec, Factory Run, Artifact Viewer다.

## Excluded Scope

이번 러닝에서 만들지 않을 범위를 적는다.
채팅, 일정, 고급 문서 편집, 실시간 협업 엔진 세부 구현은 초기 범위 밖에 둘 수 있다.

## Acceptance Standard

최종적으로 무엇이 되면 성공인지 적는다.
기준은 제품 철학, 거버넌스, 스프린트 계약, evaluator PASS 네 가지를 동시에 만족하는 것이다.
