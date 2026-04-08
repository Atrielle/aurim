# Dual Codebase Workspace

이 워크스페이스는 세 부분으로 구성된다.

- `frontend/`: 사용자 제품 UI 코드베이스
- `backend/`: API 및 도메인 서비스 코드베이스
- `harness/`: AI planner / generator / evaluator를 강제하는 하네스

핵심 원칙:

- 프런트와 백은 분리된 코드베이스다
- 하네스가 스펙, 스프린트 계약, 평가 보고서 없이 다음 단계로 넘어가지 못하게 막는다
- 수동 프롬프트 입력은 허용하지만, artifact와 gate를 통과하지 못하면 스프린트는 종료되지 않는다

권장 시작 순서:

1. `harness/specs/product-spec.md`를 채운다
2. `python harness/scripts/runner.py create-run --run-id sprint-001` 실행
3. 생성된 run artifact를 기준으로 planner / generator / evaluator 프롬프트를 수동 입력한다
4. `python harness/scripts/runner.py gate-generator --run-id sprint-001`
5. `python harness/scripts/runner.py gate-close --run-id sprint-001`

`gate-close`가 통과하기 전에는 스프린트 완료로 간주하지 않는다.

aurim