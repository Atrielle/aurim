# Atrielle Aurim Monorepo

이 저장소는 Atrielle 브랜드의 Aurim 제품을 위한 모노레포다.

핵심 구조:

- `apps/`: Aurim product core 애플리케이션 도메인
  - `apps/frontend/`: 사용자 협업 UI
  - `apps/backend/`: 플랫폼 API 및 도메인 서비스
- `tools/`: 제품 외부의 운영 도구 도메인
  - `tools/harness-runtime/`: spec-driven AI harness runtime
- `packages/`: 교체 가능한 계약/SDK 패키지
  - `packages/contracts/`: 플랫폼 및 어댑터 계약 초안 경계
  - `packages/sdk/`: 클라이언트/내부 SDK 경계
- `docs/`: foundation 및 ADR 문서

비가역 원칙:

- Aurim 제품 코어와 AI harness는 같은 저장소여도 별도 도메인이다.
- PostgreSQL만 초기 고정 system of record다.
- 그 외 엔진(auth/search/storage/git/realtime 등)은 반드시 계약 뒤에서 교체 가능해야 한다.
- 완성형 OSS 제품을 그대로 제품으로 채택하지 않는다.

권장 시작:

1. `docs/foundation/product-philosophy.md`
2. `docs/foundation/governance-model.md`
3. `docs/foundation/cloud-handoff.md`
4. `python tools/harness-runtime/scripts/runner.py create-run --run-id sprint-001`
