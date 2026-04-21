# Product Philosophy

## Purpose

이 저장소의 목적은 “AI가 뭔가 해주는 스크립트 묶음”이 아니라, 장시간 실행 가능한 개발 하네스를 통제 가능한 시스템으로 정의하는 것이다.

## Core Position

- 하네스는 오케스트레이션, 통제, 증빙을 함께 가져야 한다.
- planner / generator / evaluator는 느슨한 관습이 아니라 계약 기반 stage여야 한다.
- 실행보다 중요한 것은 재개 가능성, 실패 처리, budget 통제, evidence 보존이다.
- 특정 모델 벤더는 교체 가능해야 한다.
- 기본 저장은 파일 시스템으로 시작하되, 구조는 확장 가능해야 한다.

## Design Principles

- contract first
- policy driven
- state machine enforced
- executor replaceable
- operator visible
- evidence preserving
- reusable across projects

## Long-Running Harness Principle

최대버전 하네스는 아래 성질을 가진다.

- run lifecycle가 명시적이다
- unit dependency가 명시적이다
- evaluator 결과가 retry / replan / fail-stop으로 연결된다
- 중단 후 resume 가능하다
- budget과 usage가 stage별, run별로 추적된다
- UI에서 상태와 판단 근거를 확인할 수 있다

## Non-Negotiable Rules

- run contract 없는 orchestration 금지
- 상태 전이 기록 없는 silent transition 금지
- evaluator verdict 없는 run close 금지
- budget policy 없는 무제한 실행 금지
- evidence 없는 성공 처리 금지
- 특정 executor에 런타임 핵심 계약을 묶는 것 금지
