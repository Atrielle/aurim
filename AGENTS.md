# AGENTS Operating Lock for Aurim

이 파일은 `/workspace/aurim` 전체 트리에 적용되는 강제 운영 규칙이다.

## 목적
- 세션이 바뀌거나 대화가 중단되어도, 에이전트가 아키텍처/거버넌스 합의에서 벗어나지 않게 고정한다.

## Mandatory Startup Protocol (반드시 순서대로)
에이전트는 코드 작성/수정 전에 아래 파일을 이 순서로 읽고, 요약을 먼저 제시해야 한다.

1. `README.md`
2. `docs/foundation/cloud-handoff.md`
3. `docs/foundation/product-philosophy.md`
4. `docs/foundation/governance-model.md`
5. `docs/foundation/ui-direction.md`
6. `docs/foundation/resume-context.md`
7. `docs/foundation/design-system.md`
8. `docs/foundation/decision-status.md`

## Non-Negotiable Guardrails
- Product domain과 Harness runtime domain을 혼합하지 않는다.
- PostgreSQL을 초기 system of record로 유지한다.
- Contract source of truth는 `packages/contracts/`의 OpenAPI + JSON Schema다.
- planner/generator/evaluator 런타임을 제품 request path에 직접 넣지 않는다.
- first vertical slice 범위(Workspace/Git Workspace/Factory Spec/Factory Run/Artifact Viewer) 밖으로 임의 확장하지 않는다.

## Scope Control
- 작업 시작 전 `docs/foundation/decision-status.md`의 **Decided / Pending**을 확인한다.
- 요청이 Pending 항목을 변경하려는 경우, 먼저 "결정 제안"으로 올리고 사용자 확인 전 코드 변경 금지.

## Session Handoff Rule
- 세션 종료 전 반드시 `docs/foundation/decision-status.md`의 `Session Notes`와 `Last Updated`를 갱신한다.
- 다음 세션은 `docs/foundation/resume-context.md`의 시작 프롬프트를 그대로 사용한다.

## Refusal Policy
아래 요청은 사용자 명시 승인 없이는 수행하지 않는다.
- 합의 스택 변경
- 도메인 경계 변경(Product vs Harness)
- first vertical slice 밖 기능 확장
- 계약 우회(코드 우선)
