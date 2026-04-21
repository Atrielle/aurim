# Decision Status

이 문서는 최대버전 하네스의 현재 결정을 `decided / pending / proposed` 상태로 고정 관리한다.

## Decided

| Area | Decision | Status |
|---|---|---|
| Repository Role | 이 저장소는 reusable harness engineering runtime을 우선한다 | decided |
| Runtime Shape | planner / generator / evaluator orchestration을 core shape로 둔다 | decided |
| Contract Source | governance and runtime source of truth는 문서 + JSON Schema다 | decided |
| Default State Store | 초기 기본 저장은 file system이다 | decided |
| Executor Model | executor는 adapter contract 뒤에서 교체 가능해야 한다 | decided |
| Completion Rule | evaluator verdict와 evidence 없이 run 성공 처리를 하지 않는다 | decided |
| Policy Control | budget / retry / timeout은 정책 계약으로 외부화한다 | decided |
| UI Requirement | operator UI는 최대버전 범위에 포함된다 | decided |

## Pending

| Area | Question | Status |
|---|---|---|
| UI Framework | 어떤 UI stack으로 operator console을 구현할지 | pending |
| Indexed Store | file system 위에 SQLite 등 보조 인덱스를 둘지 | pending |
| Parallelism | unit-level 병렬 실행의 기본 정책 | pending |
| Approval Gates | human approval을 어느 stage에 넣을지 | pending |
| Vendor Executors | 어떤 실제 모델 provider adapter를 1순위로 붙일지 | pending |

## Proposed

| Area | Proposal | Status |
|---|---|---|
| Maximum Harness | state machine, retry, budget, evidence, UI를 포함한 maximum harness baseline 정의 | proposed |

## Session Notes

- 2026-04-21: 제품 코드 대신 reusable harness engineering runtime을 저장소의 중심 목표로 재정의.
- 2026-04-21: 최대버전 하네스를 위한 governance / contract-first 문서 작성 시작.

## Last Updated

- 2026-04-21 (UTC)
