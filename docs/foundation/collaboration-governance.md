# Collaboration Governance (Harness Tooling)

## Goal

이 문서는 하네스 협업 툴의 운영 원칙을 정의한다.
핵심 목표는 다음 세 가지다.

1. 누가 어떤 run을 맡고 승인하는지 명확히 한다.
2. 변경 이력과 승인 이력을 감사 가능하게 남긴다.
3. 제품 코어와 하네스 런타임 경계를 유지한다.

## Scope

적용 대상:

- `tools/harness-runtime/**`
- 하네스 run metadata / artifacts
- 하네스 협업 UI (운영용)

비적용 대상:

- 제품 사용자-facing 도메인 규칙
- backend request path에서의 planner/generator/evaluator 실행

## Collaboration Object Model

협업 툴에서 run은 아래 필드를 최소로 가져야 한다.

- `run_id`
- `status` (`created`, `planned`, `in_progress`, `review_requested`, `approved`, `rejected`, `closed`)
- `owner`
- `assignee`
- `reviewer`
- `last_sequence_report_ref`
- `sequence_reports[]`
- `updated_at`

선택 필드:

- `handoff_note`
- `risk_level`
- `blocked_reason`

## Role Responsibilities

### Owner

- run 목표 정의
- in/out scope 최종 확인
- reviewer 지정

### Assignee

- unit 실행/수집
- evidence 품질 보장
- handoff note 작성

### Reviewer

- contract compliance 검토
- evidence 재현성 확인
- approve / reject 결정

### Harness Operator

- 런타임 안정성 유지
- CI 회귀 실패 triage
- 운영 정책 위반 시 run 차단

## Workflow States and Rules

기본 상태 전이는 아래를 따른다.

- `created -> planned -> in_progress -> review_requested -> approved -> closed`
- `review_requested -> rejected -> in_progress`

강제 규칙:

- `review_requested`로 올리기 전 `gate-units`는 PASS여야 한다.
- `closed` 전 `gate-close`는 PASS여야 한다.
- `approved` 전 reviewer identity는 비어 있으면 안 된다.
- reject 시 `blocked_reason` 또는 코멘트가 필수다.

## Approval Policy

- 단일 reviewer 모델로 시작한다.
- Layer 1/2(immutable/contracts) 변경은 owner + reviewer 둘 다 승인 필요.
- Layer 3(replaceable engine) 변경은 reviewer 승인 1회로 충분하다.

## Audit and Retention

아래 이벤트는 반드시 로그로 남긴다.

- status 변경
- owner/assignee/reviewer 변경
- sequence 실행
- approve/reject 결정

보관 정책:

- run artifact: 최소 90일
- approval/rejection event: 최소 180일

## Minimal UI Requirements

협업 UI는 최소한 다음을 지원해야 한다.

1. run 목록에서 `owner/assignee/reviewer/status` 표시
2. run 상세에서 최근 `sequence_report` 바로 열기
3. status 변경 시 변경 이력 자동 기록
4. reviewer의 approve/reject 액션

## Governance Checks Before Merge

협업 관련 변경 PR은 아래를 만족해야 한다.

- policy 문서 변경 여부 확인
- touched paths가 하네스 경계를 벗어나지 않음
- regression check 통과
- run-status / report 연결 경로 검증

## Change Management

다음 변경은 ADR 필요:

- 상태 머신 변경
- 승인 권한 모델 변경
- 감사 보관 기간 변경
- run metadata 필수 필드 제거

