from __future__ import annotations

import json
import shutil
import subprocess
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUNNER = ROOT / 'tools' / 'harness-runtime' / 'scripts' / 'runner.py'
RUNS = ROOT / 'tools' / 'harness-runtime' / 'artifacts' / 'runs'


def run_cmd(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ['python', str(RUNNER), *args],
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )


def assert_ok(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode != 0:
        raise RuntimeError(f'{label} expected success, got {result.returncode}: {result.stdout}\n{result.stderr}')


def assert_fail_contains(result: subprocess.CompletedProcess[str], label: str, expected: str) -> None:
    if result.returncode == 0:
        raise RuntimeError(f'{label} expected failure, got success')
    output = f'{result.stdout}\n{result.stderr}'
    if expected not in output:
        raise RuntimeError(f'{label} missing expected message "{expected}"\nActual:\n{output}')


def write_contracts(run_id: str, *, dependency: bool = False) -> None:
    base = RUNS / run_id
    contract = {
        'version': '1.0',
        'run_id': run_id,
        'objective': 'regression run',
        'authoritative_inputs': [
            'tools/harness-runtime/specs/product-spec.md',
            'docs/foundation/product-philosophy.md',
            'docs/foundation/governance-model.md',
            'docs/foundation/cloud-handoff.md',
        ],
        'blocking_rule': 'stop if blocked',
        'in_scope': ['harness regression'],
        'out_of_scope': ['product changes'],
        'touched_paths': ['tools/harness-runtime/contracts'],
        'acceptance_criteria': [
            {
                'id': 'AC-001',
                'statement': 'first unit complete',
                'required_evidence': ['unit report'],
            },
            {
                'id': 'AC-002',
                'statement': 'second unit complete',
                'required_evidence': ['unit report'],
            },
        ],
        'work_units': [
            {
                'id': 'WU-001',
                'title': 'first',
                'objective': 'first unit',
                'touched_paths': ['tools/harness-runtime/contracts'],
                'acceptance_criteria_ids': ['AC-001'],
                'required_evidence': ['unit report'],
                'agent_budget': {
                    'max_input_tokens': 1000,
                    'max_output_tokens': 500,
                    'depends_on': [],
                },
            },
            {
                'id': 'WU-002',
                'title': 'second',
                'objective': 'second unit',
                'touched_paths': ['tools/harness-runtime/contracts'],
                'acceptance_criteria_ids': ['AC-002'],
                'required_evidence': ['unit report'],
                'agent_budget': {
                    'max_input_tokens': 1000,
                    'max_output_tokens': 500,
                    'depends_on': ['WU-001'] if dependency else [],
                },
            },
        ],
        'evaluator_checks': [
            'Spec was not reinterpreted.',
            'Out-of-scope work was not added.',
            'Changed files stayed within touched paths.',
            'Every acceptance criterion has concrete evidence.',
        ],
    }
    (base / '01_run_contract.json').write_text(json.dumps(contract, indent=2), encoding='utf-8')
    (base / '01_sprint_contract.md').write_text(
        """# Sprint Contract

## Scope

Regression checks.

## In Scope

- [x] harness regression

## Out of Scope

- [x] product changes

## Touched Paths

- [x] tools/harness-runtime/contracts

## Acceptance Criteria

- [x] unit checks

## Evidence Required

- [x] unit evidence

## Work Units

- [x] WU-001 | 목적: first | AC: AC-001 | 경로: tools/harness-runtime/contracts | 선행: 없음 | 예산: input 1000 / output 500
- [x] WU-002 | 목적: second | AC: AC-002 | 경로: tools/harness-runtime/contracts | 선행: WU-001 | 예산: input 1000 / output 500

## Unit Dependencies

- [x] WU-002 <- WU-001

## Evaluator Checks

- [x] spec 위반 없음
- [x] out-of-scope 침범 없음
- [x] touched paths 밖 변경 없음
- [x] acceptance criteria 충족
""",
        encoding='utf-8',
    )


def write_unit_report(run_id: str, unit_id: str, ac_id: str, changed_file: str) -> Path:
    base = RUNS / run_id
    report = base / f'{unit_id.lower()}-report.md'
    report.write_text(
        f"""# Unit Report

## Summary

Regression unit.

## Changed Files

- {changed_file}

## Acceptance Mapping

- [x] {ac_id} -> mapped

## Evidence

- regression evidence
""",
        encoding='utf-8',
    )
    return report


def prepare_run(run_id: str, *, dependency: bool = False) -> None:
    assert_ok(run_cmd(['create-run', '--run-id', run_id]), 'create-run')
    write_contracts(run_id, dependency=dependency)
    assert_ok(run_cmd(['validate-contract', '--run-id', run_id]), 'validate-contract')
    assert_ok(run_cmd(['plan-units', '--run-id', run_id]), 'plan-units')


def cleanup_run(run_id: str) -> None:
    path = RUNS / run_id
    if path.exists():
        shutil.rmtree(path)


def scenario_dependency_violation(prefix: str) -> None:
    run_id = f'{prefix}-dep'
    try:
        prepare_run(run_id, dependency=True)
        report = write_unit_report(run_id, 'WU-002', 'AC-002', 'tools/harness-runtime/contracts/run-contract.template.json')
        result = run_cmd(['collect-unit', '--run-id', run_id, '--unit-id', 'WU-002', '--report', report.relative_to(ROOT).as_posix()])
        assert_fail_contains(result, 'dependency_violation', 'unit dependency not collected yet: WU-001')
    finally:
        cleanup_run(run_id)


def scenario_acceptance_mapping_violation(prefix: str) -> None:
    run_id = f'{prefix}-ac'
    try:
        prepare_run(run_id)
        report = write_unit_report(run_id, 'WU-001', 'AC-002', 'tools/harness-runtime/contracts/run-contract.template.json')
        result = run_cmd(['collect-unit', '--run-id', run_id, '--unit-id', 'WU-001', '--report', report.relative_to(ROOT).as_posix()])
        assert_fail_contains(result, 'acceptance_mapping_violation', 'unit report is missing acceptance mappings for: AC-001')
    finally:
        cleanup_run(run_id)


def scenario_touched_path_violation(prefix: str) -> None:
    run_id = f'{prefix}-path'
    try:
        prepare_run(run_id)
        report = write_unit_report(run_id, 'WU-001', 'AC-001', 'apps/backend/README.md')
        result = run_cmd(['collect-unit', '--run-id', run_id, '--unit-id', 'WU-001', '--report', report.relative_to(ROOT).as_posix()])
        assert_fail_contains(result, 'touched_path_violation', 'changed file outside touched paths: apps/backend/README.md')
    finally:
        cleanup_run(run_id)


def scenario_evidence_hash_tamper(prefix: str) -> None:
    run_id = f'{prefix}-hash'
    try:
        prepare_run(run_id)
        report = write_unit_report(run_id, 'WU-001', 'AC-001', 'tools/harness-runtime/contracts/run-contract.template.json')
        assert_ok(
            run_cmd(['collect-unit', '--run-id', run_id, '--unit-id', 'WU-001', '--report', report.relative_to(ROOT).as_posix()]),
            'collect-unit',
        )
        evidence = RUNS / run_id / '05_unit_reports' / 'WU-001.evidence.json'
        payload = json.loads(evidence.read_text(encoding='utf-8'))
        payload['file_hashes']['tools/harness-runtime/contracts/run-contract.template.json'] = 'tampered'
        evidence.write_text(json.dumps(payload, indent=2), encoding='utf-8')
        result = run_cmd(['gate-units', '--run-id', run_id])
        assert_fail_contains(result, 'evidence_hash_tamper', 'unit evidence hashes changed after collection for WU-001')
    finally:
        cleanup_run(run_id)


def main() -> None:
    prefix = f'regression-{uuid.uuid4().hex[:8]}'
    scenario_dependency_violation(prefix)
    scenario_acceptance_mapping_violation(prefix)
    scenario_touched_path_violation(prefix)
    scenario_evidence_hash_tamper(prefix)
    print('OK: unit gate regression scenarios passed')


if __name__ == '__main__':
    main()
