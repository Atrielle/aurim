# Governance Model

## Governance Goal

거버넌스의 목적은 구현 자유도를 빼앗는 것이 아니라, 하네스가 시간이 지나도 통제 가능한 시스템으로 남게 하는 것이다.

## Governance Layers

### Layer 1. Immutable Foundations

- planner / generator / evaluator 분리
- contract-first runtime
- policy-controlled execution
- evidence-preserving completion
- replaceable executor architecture

이 레이어를 바꾸려면 명시 승인과 decision record가 필요하다.

### Layer 2. Versioned Contracts

- run contract schema
- state machine schema
- executor config schema
- budget policy schema
- retry policy schema
- evidence record schema
- UI view-model contract

이 레이어 변경 시 breaking impact와 migration note가 필요하다.

### Layer 3. Replaceable Implementations

- mock executor
- subprocess executor
- vendor API executor
- file-based state backend
- optional indexed state backend
- operator UI framework

이 레이어는 계약 호환성을 유지하면 교체 가능하다.

## Required Decision Questions

모든 중요한 변경은 아래에 답해야 한다.

- 이것이 foundation인가, contract인가, implementation인가?
- run lifecycle를 흐리게 만드는가?
- retry / fail-stop 규칙을 무너뜨리는가?
- budget 통제 없이 실행하게 만드는가?
- evidence 없는 성공을 허용하는가?
- 특정 vendor나 transport에 고정되는가?
- resume 가능성을 해치는가?

## Release Gates

### Contract Gate

- schema valid
- examples valid
- compatibility note present

### Runtime Gate

- orchestration regression passes
- state transition audit passes
- retry policy tests pass

### UI Gate

- run summary visibility exists
- unit timeline visibility exists
- failure / retry reason visibility exists
- budget / executor configuration visibility exists

## Refusal Rules

아래는 명시 승인 없이는 수행하지 않는다.

- planner / generator / evaluator boundary 제거
- budget ceiling 제거
- evidence contract 우회
- run state machine 무력화
- executor-specific fields를 core contract에 직접 박아 넣기
