# Frontend

이 디렉터리는 실제 제품 UI 코드베이스다.

원칙:

- 프런트는 하네스 artifact 없이 임의 구현하지 않는다
- 하네스의 `01_sprint_contract.md`에 적힌 acceptance criteria와 touched paths를 먼저 확인한다
- 프런트에서 임의로 도메인 모델을 새로 정의하지 않는다

예상 입력:

- backend API contract
- `harness/artifacts/runs/<run-id>/00_spec_snapshot.md`
- `harness/artifacts/runs/<run-id>/01_sprint_contract.md`
- evaluator feedback
