# Decision Status (Filesystem-Locked)

이 문서는 Aurim의 현재 거버넌스 결정을 **결정됨(Decided) / 미결정(Pending)** 으로 고정 관리한다.

- Status 값: `decided` | `pending` | `proposed`
- 이 문서에 없는 내용은 기본적으로 `pending`으로 취급한다.

## Decided

| Area | Decision | Status | Source |
|---|---|---|---|
| Domain Boundary | Product와 Harness는 같은 저장소여도 별도 도메인으로 분리 | decided | `docs/foundation/product-philosophy.md` |
| Product Position | 완성형 OSS 제품을 그대로 제품으로 채택하지 않음 | decided | `docs/foundation/product-philosophy.md` |
| System of Record | 초기 고정 SoR은 PostgreSQL | decided | `README.md`, `docs/foundation/product-philosophy.md` |
| Contract Source | OpenAPI + JSON Schema를 계약 기준 원본으로 사용 | decided | `README.md`, `packages/contracts/README.md` |
| Backend Target | Kotlin + Spring Boot + WebFlux + Coroutines + R2DBC + Flyway | decided | `README.md`, `apps/backend/README.md` |
| Frontend Target | React + TypeScript + Vite | decided | `README.md`, `apps/frontend/README.md` |
| Harness Runtime | Python 기반 gate-driven runtime 유지 | decided | `README.md`, `tools/harness-runtime/README.md` |
| Delivery Scope | first vertical slice 5개(Workspace/Git Workspace/Factory Spec/Factory Run/Artifact Viewer) 우선 | decided | `README.md`, `docs/foundation/cloud-handoff.md` |
| Gate Policy | evaluator PASS 없이는 run close 불가 | decided | `tools/harness-runtime/README.md` |
| Change Scope | touched paths 밖 변경 불가 | decided | `tools/harness-runtime/README.md`, `docs/foundation/governance-model.md` |
| Session Lock | 루트 `AGENTS.md` + 본 문서를 기준으로 세션 재개 시 컨텍스트를 강제 | decided | `AGENTS.md`, `docs/foundation/resume-context.md` |
| Decision Storage | 의사결정 기록은 당분간 파일시스템(JSON) 원본을 기준으로 유지하고, DB는 후속 인덱싱 용도로 검토 | decided | `docs/foundation/decisions/DEC-2026-0002-decision-storage-strategy.json` |

## Pending

| Area | Question | Current Status | Notes |
|---|---|---|---|
| Engine Choices | auth/search/storage/git/realtime/queue/cache/observability 구체 엔진 확정 | pending | 계약 호환이 우선이며 엔진은 교체 가능해야 함 |
| ADR Catalog | ADR 파일 체계(`docs/adr/`) 운영 기준 확정 | pending | 변경 정책은 있으나 실제 ADR 축적은 진행 필요 |
| Contract Maturity | v0 계약의 호환성/브레이킹 정책 자동 검증 체계 | pending | 수동 점검 중심에서 자동 검증으로 강화 필요 |

## Harness Readiness Check

아래 항목은 하네스가 앞으로 아우림 협업툴 개발에 사용 가능한지 점검한 최신 실행 기록이다.

| Date (UTC) | Command | Result | Meaning |
|---|---|---|---|
| 2026-04-18 | `python tools/harness-runtime/scripts/unit_gate_regression.py` | pass | unit-level gate 실패 시나리오 회귀 점검 통과 |
| 2026-04-18 | `python -m py_compile ...` (runner/ui/regression scripts) | pass | 하네스 핵심 스크립트 문법/로딩 이상 없음 |

## Proposed

| Date (UTC) | Proposal | Owner | Status |
|---|---|---|---|
| 2026-04-18 | 세션 단절 대응용 filesystem lock(AGENTS + decision-status) 도입 | Codex agent | decided |

## Session Notes

- 2026-04-18: Root `AGENTS.md`와 본 `decision-status.md`를 추가해 세션 재개 시 문서 기반 강제 컨텍스트를 고정.
- 2026-04-18: 하네스 회귀/컴파일 체크를 실행해 런타임 기본 건전성을 확인.
- 2026-04-18: 거버넌스 감사 스크립트(`governance_audit.py`)와 결정 레코드 스키마/샘플을 추가해 추적 가능성을 강화.
- 2026-04-18: 하네스 리팩토링 Phase 0(모듈 경계 정의 및 skeleton 생성) 착수.
- 2026-04-18: 하네스 리팩토링 Phase 1(공통 IO/Validation/Path helper를 harness_core로 위임) 완료.
- 2026-04-18: 하네스 리팩토링 Phase 2-A(unit report parsing/validation 로직 분리) 완료.
- 2026-04-18: 하네스 리팩토링 Phase 2-B1(gate-close 검증 로직 분리) 완료.
- 2026-04-18: 하네스 리팩토링 Phase 2-B2(contract 검증/정렬 로직 분리) 완료, Phase 3 진입 준비.
- 2026-04-18: 하네스 리팩토링 Phase 3-A(freeze/baseline 검증 로직 분리) 완료.
- 2026-04-18: 하네스 리팩토링 Phase 3-B(manifest 상태 전이 helper 분리) 완료.
- 2026-04-18: 하네스 리팩토링 Phase 4-A(CLI parser/dispatch 분리) 완료.
- 2026-04-18: 하네스 리팩토링 Phase 4-B(handler registry 검증/CLI 진입점 통합) 완료.
- 2026-04-18: 하네스 리팩토링 Phase 0~4 범위 완료, refactor program 종료.

## Last Updated

- 2026-04-18 (UTC)
