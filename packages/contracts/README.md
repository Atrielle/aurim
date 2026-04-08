# Contracts Package Boundary

이 디렉터리는 Aurim 플랫폼의 계약 기준 원본을 둔다.

## Source Of Truth

- HTTP API: `OpenAPI`
- resource, event, artifact schemas: `JSON Schema`

## Goals

- PostgreSQL 소유 모델을 중심으로 계약을 먼저 고정한다.
- product core와 harness가 공유해야 하는 최소 계약만 노출한다.
- 구현 엔진은 계약 뒤에서 교체 가능하게 유지한다.
- frontend와 backend가 언어에 직접 종속되지 않도록 스키마 중심으로 정렬한다.

## Expected Contents

- `openapi/`
- `schemas/`
- versioned contract documents

## First Contracts To Define

- workspace
- git workspace
- factory spec
- factory run
- factory artifact
