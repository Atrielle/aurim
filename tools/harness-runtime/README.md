# Harness Runtime (Factory Domain)

이 디렉터리는 AI planner, generator, evaluator를 통제하는 하네스 런타임 경계다.

## Runtime Stack

- `Python`
- file-based artifacts
- gate-driven run lifecycle

## Hard Rules

- spec snapshot 없이 sprint를 시작하지 않는다.
- sprint contract 없이 generator는 코드 작업에 들어가지 않는다.
- evaluator PASS 없이 sprint는 닫히지 않는다.
- touched paths 밖의 변경은 위반으로 간주한다.
- 제품 코어 request path에 장시간 planner, generator, evaluator 런타임을 직접 넣지 않는다.

## Relationship To Product

- 제품은 Factory App UI와 run metadata를 소유할 수 있다.
- 실제 planner, generator, evaluator 실행은 이 runtime 경계가 담당한다.
- 제품 코어와 하네스 런타임은 같은 저장소에 있어도 별도 도메인이다.

## Basic Flow

1. `tools/harness-runtime/specs/product-spec.md`를 채운다.
2. `python tools/harness-runtime/scripts/runner.py create-run --run-id sprint-001`
3. 생성된 `01_run_contract.json`을 먼저 채운다. 이 파일이 실행 계약의 기준점이다.
4. `01_sprint_contract.md`를 사람이 읽기 쉬운 요약으로 채우되, 범위와 touched paths는 JSON contract와 충돌하면 안 된다.
5. `python tools/harness-runtime/scripts/runner.py freeze-contract --run-id sprint-001`
6. `freeze-contract`가 authored contract state를 잠그지 못한 run은 다음 단계로 넘어가지 않는다.
7. `python tools/harness-runtime/scripts/runner.py plan-units --run-id sprint-001`
8. `plan-units`는 run contract의 `work_units`를 의존성 순서로 정렬해 `04_unit_plan.json`을 생성한다.
9. `python tools/harness-runtime/scripts/runner.py dispatch-unit --run-id sprint-001 --unit-id WU-001`
10. `dispatch-unit`은 해당 unit의 AC, touched paths, 증거 요구사항, 토큰 예산을 담은 payload(`05_unit_reports/WU-001.dispatch.json`)를 생성한다.
11. 각 unit 작업 보고서를 작성한다. (필수 heading: `# Unit Report`, `## Summary`, `## Changed Files`, `## Acceptance Mapping`, `## Evidence`)
12. `python tools/harness-runtime/scripts/runner.py collect-unit --run-id sprint-001 --unit-id WU-001 --report docs/path/to/unit-report.md`
13. `collect-unit`은 보고서 수집과 함께 changed files 해시 증거(`05_unit_reports/WU-001.evidence.json`)를 자동 생성한다.
14. 모든 unit 보고서를 수집한 뒤 `python tools/harness-runtime/scripts/runner.py gate-units --run-id sprint-001`
15. 현재 진행 상태를 확인할 때 `python tools/harness-runtime/scripts/runner.py run-status --run-id sprint-001`를 사용한다.
16. `gate-units`를 통과하지 못한 run은 generator/evaluator close 단계로 진행하지 않는다.
17. 생성 artifact를 기준으로 planner, generator, evaluator 프롬프트를 수동 또는 반자동으로 입력한다.
18. `python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-001`
19. `freeze-contract`는 현재 run 디렉터리 밖의 runner-owned proof(`tools/harness-runtime/.runner-state/...`)도 남긴다. 이 proof가 없으면 `gate-generator`는 진행되지 않는다.
20. `gate-generator` 전에 선언된 touched paths는 깨끗해야 한다. 현재 run 디렉터리 안의 artifact 파일들과 `manifest.json`은 runner-owned freeze proof와 현재 내용이 정확히 같을 때만 예외로 인정한다.
21. `tools/harness-runtime/.runner-state/...`는 touched paths에 넣을 수 없고, generator가 수정 대상으로 선언할 수도 없다.
22. `gate-generator`는 runner-owned baseline proof도 남긴다. 이 proof가 없으면 `gate-close`는 진행되지 않는다.
23. 코드 작업 수행
24. `python tools/harness-runtime/scripts/runner.py gate-close --run-id sprint-001`

`gate-close`가 실패하면 스프린트는 끝나지 않은 것이다.
`gate-generator` 전에 코드를 바꾸면 changed-files enforcement의 신뢰성이 떨어진다.
수동 시드 baseline은 허용하지 않는다.
`freeze-contract` 없이 작성된 run artifact는 baseline 예외가 적용되지 않는다.
`manifest.json` 단독 self-report는 freeze/baseline evidence로 인정하지 않는다.

## Regression Check

unit-level 실패 시나리오를 한 번에 점검하려면 아래 명령을 사용한다.

`python tools/harness-runtime/scripts/unit_gate_regression.py`

## Harness UI Console

자동화 흐름을 터미널 대신 UI에서 실행하려면 아래 명령으로 로컬 콘솔을 띄운다.

`python tools/harness-runtime/scripts/ui_server.py`

브라우저에서 `http://127.0.0.1:8787`에 접속하면 run lifecycle 명령(create/validate/freeze/plan/dispatch/collect/gate/status)과 regression 실행을 버튼으로 수행할 수 있다.

- UI는 내부적으로 기존 `runner.py`를 그대로 호출하므로 gate 규칙은 동일하게 적용된다.
- `collect-unit`은 `unit-id`와 `report path`를 반드시 입력해야 한다.
- UI 출력에는 실행 명령과 stdout/stderr가 함께 표시되어 증거 추적에 사용할 수 있다.

