# Governance Model

## Governance Goal

거버넌스의 목적은 의사결정을 느리게 만드는 것이 아니라, 제품과 하네스가 임의 확장되지 못하게 막는 것이다.
모든 중요한 변경은 다음 네 가지를 통과해야 한다.

1. 경계 일관성
2. 데이터 소유권 일관성
3. 교체 가능성 유지
4. 상업적 이용 안전성

## Decision Layers

### Layer 1. Immutable foundations

다음은 쉽게 바꾸지 않는다.

- PostgreSQL as system of record
- Product vs Harness boundary
- Platform-owned domain rules
- Contract-first adapter architecture
- Commercial-safe license policy

이 레이어를 바꾸려면 ADR과 명시적 승인 둘 다 필요하다.

### Layer 2. Versioned platform contracts

다음은 버전 관리하되 신중하게 변경한다.

- Resource ID rules
- Workspace boundary
- Permission relation types
- Work Item schema
- Document revision policy
- File metadata schema
- Storage provider contract
- Search adapter contract
- Git adapter contract
- Realtime adapter contract
- Event bus, queue, cache contracts
- Event schema
- Search document schema

이 레이어를 바꾸면 migration impact와 compatibility note가 반드시 필요하다.

### Layer 3. Replaceable engine decisions

다음은 교체 가능해야 한다.

- auth engine
- permission engine
- object storage implementation
- search engine
- git engine
- realtime transport
- queue or cache engine
- document editing wrapper details
- observability stack
- harness runtime implementation

이 레이어는 계약 호환성만 유지하면 교체 가능하다.

## Required Artifacts for Change

중요한 변경은 아래 산출물을 남긴다.

- one-page decision note
- impacted contracts list
- touched paths list
- risk list
- rollback plan
- evaluator criteria

제품 변경이든 하네스 변경이든, 위 산출물 없이 merge하지 않는다.

## ADR Rule

다음 변경은 ADR이 필요하다.

- PostgreSQL 외 다른 system of record 도입
- Product and Harness boundary 변경
- core license policy 변경
- platform-owned domain rule 변경
- contract breaking change
- runtime topology 변경

ADR 최소 항목은 아래와 같다.

- context
- decision
- alternatives considered
- consequences
- migration plan

## Ownership Model

### Product owner decisions

- user-facing workflows
- workspace semantics
- work item semantics
- document and file lifecycle
- mobile parity scope
- monetizable app boundaries

### Platform architect decisions

- adapter contracts
- data ownership boundaries
- migration compatibility
- pluggability rules
- integration safety

### Harness owner decisions

- sprint contract format
- run lifecycle
- evaluator gates
- artifact schema
- execution isolation policy

### Security and compliance decisions

- license approval
- data retention policy
- secret handling
- auditability requirements
- self-hosting boundary

## Non-Negotiable Rules

- 제품 코어에 planner, generator, evaluator 런타임을 직접 넣지 않는다.
- Git을 운영 메타데이터 저장소로 사용하지 않는다.
- OSS 제품을 제품 자체로 재포장하지 않는다.
- 계약 없이 특정 엔진에 도메인 로직을 박아 넣지 않는다.
- source-available 계열을 코어 경로에 두지 않는다.
- evaluator PASS 없이 run을 성공 처리하지 않는다.
- touched paths 밖의 코드 변경은 허용하지 않는다.

## Decision Checklist

변경 제안은 아래 질문에 모두 답해야 한다.

- 이것이 제품 코어 변경인가, factory app 변경인가, harness runtime 변경인가?
- platform-owned rule인가, engine choice인가?
- PostgreSQL ownership을 흐리게 만드는가?
- 특정 벤더나 엔진에 잠기게 만드는가?
- 라이선스 정책에 위배되는가?
- 웹과 모바일 공통 도메인 모델을 깨는가?
- Work Item 단일 모델 원칙을 깨는가?
- 롤백 가능한가?

## Release Gates

### Product gate

- contract compatibility confirmed
- migration reviewed
- permission implications reviewed
- audit and activity impact reviewed
- mobile and web API consistency checked

### Factory app gate

- run metadata schema valid
- git workspace linkage valid
- approval flow valid
- artifact visibility valid

### Harness gate

- spec snapshot exists
- sprint contract valid
- touched paths validated
- evaluator verdict is PASS
- compliance checklist complete

## Repository Implication

이 거버넌스는 저장소 구조에도 반영되어야 한다.

- product-facing code는 앱 경계 아래 둔다.
- harness runtime은 별도 도구 경계 아래 둔다.
- 공통 계약은 별도 contracts 경계로 뺀다.
- 문서 없는 구조 결정을 코드에 먼저 반영하지 않는다.
