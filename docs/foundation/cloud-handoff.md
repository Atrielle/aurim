# Cloud Handoff

## Identity

- Group or organization: `Atrielle`
- Product name: `Aurim`
- Korean product rendering: `아우림`
- Repository: `Atrielle/aurim`

`Atrielle` is the brand layer.
`Aurim` is the collaboration platform product layer.

## What This Repository Is

This repository is a monorepo for two distinct but related systems.

1. The collaboration product itself
2. The AI harness system that helps build and govern the product

They may live in one repository, but they are not the same domain.

## Non-Negotiable Product Position

- We are not adopting a complete OSS product as the product itself.
- We may use OSS engines, protocols, storage systems, and infrastructure behind our own platform.
- The platform owns domain rules, data ownership, APIs, and UI or UX.
- PostgreSQL is the only initial fixed system-of-record decision.
- Other engines must remain replaceable behind contracts.
- Web and mobile must run on the same domain model and API.
- Calendar, kanban, WBS, and gantt must project from a single Work Item model.
- Git is not the primary operational database.
- Git is an optional revision backend and developer workspace capability.

## Agreed Technical Baseline

- Frontend: `React + TypeScript + Vite`
- Backend target: `Kotlin + Spring Boot + WebFlux + Coroutines + R2DBC`
- Database: `PostgreSQL`
- Database migration: `Flyway`
- Contracts source of truth: `OpenAPI + JSON Schema`
- Harness runtime: `Python`
- JDK: `Java 25`
- Build: `Gradle Kotlin DSL`

## Architecture Direction

- Modular monolith first
- Platform core plus replaceable engines
- Split later only when operationally necessary
- Fix contracts and ownership boundaries before distributed topology

## Product vs Harness Boundary

### Product owns

- Workspace
- Membership
- Role and permission relationships
- Work Item model
- Document metadata and revision policy
- File metadata and storage mapping
- Link graph
- Activity and audit schema
- Search document schema
- Git workspace linkage
- End-user collaboration UI
- Developer-facing Factory App UI inside the collaboration product

### Harness owns

- Spec snapshot
- Sprint contract
- Prompt sets
- Run manifest
- Planner, generator, evaluator flow
- Artifact validation
- Gate enforcement
- Evaluator close criteria

### Product must not own

- Direct long-running planner or generator execution in the request path
- Evaluator runtime internals
- Long-running code generation worker internals

## Recommended Product Structure

```text
apps/
  frontend/
  backend/
tools/
  harness-runtime/
packages/
  contracts/
  sdk/
docs/
  foundation/
  adr/
```

Current local workspace now follows the recommended monorepo shape.

## Current Repository Status

- `apps/frontend/`: React + TypeScript baseline
- `apps/backend/`: backend boundary exists, but implementation may still contain temporary bootstrap code before Kotlin migration is complete
- `tools/harness-runtime/`: Python run gates and prompt templates
- `packages/contracts/`: contract package boundary scaffold
- `packages/sdk/`: SDK package boundary scaffold
- `docs/foundation/`: philosophy, governance, and handoff

The repository direction is authoritative even when implementation scaffolding lags behind it.

## Harness Meaning

Harness here means an AI engineering control system, not just a UI mock environment.

The purpose of the harness is to prevent drift from spec by forcing execution through:

- spec snapshot
- sprint contract
- touched paths
- generator report
- evaluator report
- pass or fail close gate

Manual prompt entry is allowed.
Unconstrained execution is not allowed.

## Existing Harness Gate Logic

The local harness assumes these controls:

- no run without spec snapshot
- no run without sprint contract
- no code changes outside touched paths
- no successful close without evaluator `PASS`
- no quiet bypass of placeholders in artifacts

## Product Vision

Aurim is a next-generation enterprise B2B collaboration platform.

Core product themes:

- workspace-centric collaboration
- shared documents
- file and asset management
- work tracking
- schedule and timeline views
- chat and activity linkage
- developer workspace support with Git integration

Aurim should be able to host a developer-oriented Factory App as one application capability,
but the actual harness runtime should remain operationally separated.

## Factory App Vision

Inside the collaboration product, provide a developer-facing application that manages:

- specs
- sprint contracts
- run requests
- approvals
- artifacts
- evaluator results
- Git workspace binding

This is part of the product experience.
It is not the same thing as embedding the full harness runtime into the product core.

## UI Memory

The original local UI before the reset had a strong dashboard and widget-workbench feel.
That implementation is gone, but the intended feel must remain.
Read `docs/foundation/ui-direction.md` before doing meaningful frontend design work.

## Recommended First Real Scope

Do not begin with the whole collaboration suite.
Start with one vertical slice:

- Workspace
- Git Workspace binding
- Factory Spec
- Factory Run
- Artifact Viewer

## Immediate Next Steps

1. Define v0 contracts in `packages/contracts/`
2. Replace temporary backend bootstrap with the agreed Kotlin Spring stack
3. Keep harness gates under `tools/harness-runtime/`
4. Build only the first vertical slice before broader product surface area

## What Not To Do

- Do not split into multiple repositories yet
- Do not make the product server run the full planner or generator loop inline
- Do not let Git become the operational metadata database
- Do not lock core behavior into one engine implementation
- Do not treat complete OSS products as the product
- Do not treat source-available licenses as safe defaults

## Read First

Before continuing, read these files first:

- [product-philosophy.md](/C:/syszone_project/ui_design/docs/foundation/product-philosophy.md)
- [governance-model.md](/C:/syszone_project/ui_design/docs/foundation/governance-model.md)
- [cloud-handoff.md](/C:/syszone_project/ui_design/docs/foundation/cloud-handoff.md)
- [ui-direction.md](/C:/syszone_project/ui_design/docs/foundation/ui-direction.md)
- [resume-context.md](/C:/syszone_project/ui_design/docs/foundation/resume-context.md)
