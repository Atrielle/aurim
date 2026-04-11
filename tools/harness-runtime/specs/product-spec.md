# Product Spec

## Product Name

Aurim

## Problem Statement

협업 제품과 AI factory capability를 한 저장소에서 운영할 때 경계가 무너지면
도메인 규칙 소유권과 시스템 운영 책임이 뒤섞인다.

## Product Goal

첫 vertical slice에서 Workspace, Git Workspace binding, Factory Spec, Factory Run,
Artifact Viewer를 계약 기반으로 연결한다.

## Non-Negotiable Constraints

- PostgreSQL is the metadata system of record.
- Frontend and backend are separate codebases.
- UI and domain rules are product-owned.
- Engines must stay replaceable behind contracts.

## Initial Scope

- Workspace metadata API
- Git workspace binding metadata API
- Factory spec/run metadata API
- Artifact viewer metadata API

## Excluded Scope

- Full collaboration suite beyond first slice
- Embedding planner/generator/evaluator runtime inside product request path

## Acceptance Standard

- Contract documents for first slice are versioned in `packages/contracts`.
- Product API exposes first-slice resources through workspace-scoped endpoints.
