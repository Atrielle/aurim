# Backend

이 디렉터리는 플랫폼 API 코드베이스다.

원칙:

- backend는 플랫폼이 직접 소유하는 도메인 규칙과 메타데이터 계약을 노출한다
- auth, search, storage, git, realtime은 adapter 경계 뒤에 둔다
- 하네스 artifact 없이 scope를 늘리지 않는다

예상 시작 명령:

`uvicorn app.main:app --reload --app-dir backend`
