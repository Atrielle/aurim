# Harness

이 디렉터리는 AI planner / generator / evaluator를 하네스하는 강제 레이어다.

핵심 규칙:

- spec snapshot 없이 sprint를 시작하지 않는다
- sprint contract 없이 generator는 코드 작업에 들어가지 않는다
- evaluator PASS 없이 sprint는 닫히지 않는다
- touched paths 밖의 변경은 위반으로 간주한다

기본 흐름:

1. `harness/specs/product-spec.md`를 채운다
2. `python harness/scripts/runner.py create-run --run-id sprint-001`
3. 생성된 artifact를 기준으로 planner / generator / evaluator 프롬프트를 수동 입력한다
4. `python harness/scripts/runner.py gate-generator --run-id sprint-001`
5. 코드 작업 수행
6. `python harness/scripts/runner.py gate-close --run-id sprint-001`

`gate-close`가 실패하면 스프린트는 끝나지 않은 것이다.
