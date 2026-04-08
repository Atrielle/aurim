# Frontend (Product Core)

이 디렉터리는 Aurim 제품 코어의 사용자 UI 코드베이스다.

## Target Stack

- `React`
- `TypeScript`
- `Vite`

## Rules

- 프런트는 하네스 artifact 없이 임의 구현하지 않는다.
- `tools/harness-runtime/artifacts/runs/<run-id>/01_sprint_contract.md`의 acceptance criteria와 touched paths를 먼저 확인한다.
- 프런트에서 임의로 도메인 모델을 새로 정의하지 않는다.
- API와 리소스 구조의 기준 원본은 `packages/contracts/`의 `OpenAPI + JSON Schema`다.

## Expected Inputs

- backend API contracts
- `tools/harness-runtime/artifacts/runs/<run-id>/00_spec_snapshot.md`
- `tools/harness-runtime/artifacts/runs/<run-id>/01_sprint_contract.md`
- evaluator feedback

## First Slice Focus

- Workspace shell
- Git Workspace binding UI
- Factory Spec editor or viewer
- Factory Run detail
- Artifact Viewer
