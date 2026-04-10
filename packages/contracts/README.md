# Contracts Package Boundary

이 디렉터리는 플랫폼 소유 계약(도메인/어댑터/API) 버전 경계를 둔다.

목표:

- PostgreSQL 소유 모델을 중심으로 계약을 먼저 고정
- 엔진 구현체는 계약 뒤에서 교체 가능 유지
- product core와 harness가 공유해야 하는 최소 계약만 노출

## v0 First Vertical Slice Contracts

- `workspace.v0.md`
- `git-workspace.v0.md`
- `factory-spec.v0.md`
- `factory-run.v0.md`
- `factory-artifact.v0.md`
