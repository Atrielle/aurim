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
7. 생성 artifact를 기준으로 planner, generator, evaluator 프롬프트를 수동 또는 반자동으로 입력한다.
8. `python tools/harness-runtime/scripts/runner.py gate-generator --run-id sprint-001`
9. `freeze-contract`는 현재 run 디렉터리 밖의 runner-owned proof(`tools/harness-runtime/.runner-state/...`)도 남긴다. 이 proof가 없으면 `gate-generator`는 진행되지 않는다.
10. `gate-generator` 전에 선언된 touched paths는 깨끗해야 한다. 현재 run 디렉터리 안의 artifact 파일들과 `manifest.json`은 runner-owned freeze proof와 현재 내용이 정확히 같을 때만 예외로 인정한다.
11. `tools/harness-runtime/.runner-state/...`는 touched paths에 넣을 수 없고, generator가 수정 대상으로 선언할 수도 없다.
12. `gate-generator`는 runner-owned baseline proof도 남긴다. 이 proof가 없으면 `gate-close`는 진행되지 않는다.
13. 코드 작업 수행
14. `python tools/harness-runtime/scripts/runner.py gate-close --run-id sprint-001`

`gate-close`가 실패하면 스프린트는 끝나지 않은 것이다.
`gate-generator` 전에 코드를 바꾸면 changed-files enforcement의 신뢰성이 떨어진다.
수동 시드 baseline은 허용하지 않는다.
`freeze-contract` 없이 작성된 run artifact는 baseline 예외가 적용되지 않는다.
`manifest.json` 단독 self-report는 freeze/baseline evidence로 인정하지 않는다.
