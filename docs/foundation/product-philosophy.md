# Product Philosophy

## Purpose

이 저장소는 두 가지를 함께 다룬다.

1. 협업 플랫폼 제품
2. 그 제품을 spec-driven 방식으로 만들기 위한 AI harness

둘은 같은 저장소에 있을 수 있지만, 같은 도메인은 아니다.
제품은 고객이 쓰는 시스템이고, harness는 제품을 설계·구현·평가하는 내부 공장이다.

## Core Position

- 우리는 완성형 OSS 제품을 도입하지 않는다.
- 우리는 OSS 엔진, 프로토콜, 인프라를 가져와 우리 제품에 통합한다.
- 플랫폼의 도메인 규칙, 데이터 소유권, API, UI/UX는 우리가 가진다.
- PostgreSQL만 초기 고정 대상이다.
- 그 외 엔진은 계약 뒤에 숨기고 교체 가능하게 설계한다.
- 웹과 모바일은 같은 도메인 모델과 API 위에서 동작한다.
- 일정, 달력, 칸반, WBS, 간트는 하나의 Work Item 모델에서 파생된다.
- Git은 플랫폼 DB 대체재가 아니라 선택적 revision backend다.
- 하네스는 제품 코어가 아니라 별도 factory capability다.

## Product Principles

- 직접 구현은 최소화한다.
- 상업적 이용 안전성이 불명확한 기술은 코어 선택지에서 제외한다.
- 플랫폼이 소유해야 하는 규칙은 반드시 내부 모델로 명시한다.
- 엔진 선택보다 계약 설계를 먼저 고정한다.
- 초기 구조는 모듈러 모놀리식 우선으로 간다.
- 먼저 데이터 소유권과 경계를 고정하고, 분산은 나중에 한다.
- 제품은 운영 데이터의 system of record를 PostgreSQL에 둔다.
- 파일 바디, 검색 인덱스, Git 저장소, 실시간 전달은 모두 pluggable 해야 한다.

## Harness Principles

- 하네스는 AI를 더 똑똑하게 보이게 하는 장식이 아니라, spec 이탈을 막는 통제 시스템이다.
- planner, generator, evaluator는 자유 실행이 아니라 artifact와 gate를 통해 움직여야 한다.
- 수동 프롬프트 입력은 허용하지만, spec snapshot과 sprint contract 없이 실행되면 안 된다.
- evaluator가 PASS하지 않으면 스프린트를 닫지 않는다.
- 코드 변경 가능 범위는 sprint contract의 touched paths로 제한한다.
- 제품 코드와 하네스 코드는 같은 저장소에 둘 수 있지만 런타임 책임은 분리한다.

## Product and Harness Boundary

### Product owns

- Workspace
- Membership
- Role and permission relationships
- Work Item model
- Document metadata and revision policy
- File metadata and storage contract mapping
- Link graph
- Activity and audit schema
- Search document schema
- Git workspace and repository linkage
- Developer-facing Factory App UI

### Harness owns

- Spec snapshot
- Sprint contract
- Prompt set and run manifest
- Planner, generator, evaluator execution flow
- Artifact validation
- Gate enforcement
- Run scoring and close conditions

### Product does not own

- Direct agent execution loop in request path
- Long-running code generation worker internals
- Evaluator runtime implementation details

## Commercial Safety

### Default allowed

- Apache-2.0
- MIT
- BSD
- PostgreSQL License

### Conditional review

- MPL-2.0
- LGPL
- dual license
- open core

### Default excluded from core path

- GPLv3
- AGPLv3
- SSPL
- Elastic License
- BSL
- FSL and source-available family

## Success Criteria

우리는 다음 상태를 목표로 한다.

- 제품 코어와 factory capability가 명확히 분리되어 있다.
- 어떤 엔진도 계약 밖으로 새지 않는다.
- 개발자는 협업툴 안에서 spec, run, approval, artifact를 다룰 수 있다.
- 실제 AI 실행은 별도 runtime에서 통제된다.
- 라이선스, 데이터 소유권, 운영 경계가 문서와 코드 구조에 동시에 반영된다.
