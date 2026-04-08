# SDK Package Boundary

이 디렉터리는 웹, 모바일, 내부 도구가 공통 도메인 API를 소비하기 위한 SDK 경계다.

## Principles

- SDK는 `packages/contracts/`의 `OpenAPI + JSON Schema`에 종속된다.
- product core 계약 버전을 우선한다.
- 구현 엔진 세부사항은 노출하지 않는다.
- 교체 가능한 어댑터 구조를 깨지 않는 인터페이스만 제공한다.

## Intended Outputs

- frontend API client
- internal product SDK
- harness-facing schema helpers

수동 구현보다 계약 기반 생성 또는 얇은 래퍼를 우선한다.
