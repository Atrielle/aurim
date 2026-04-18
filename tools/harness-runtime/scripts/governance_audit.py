from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CONTRACTS = ROOT / 'packages' / 'contracts'
DECISIONS_DIR = ROOT / 'docs' / 'foundation' / 'decisions'
DECISION_STATUS = ROOT / 'docs' / 'foundation' / 'decision-status.md'
AGENTS = ROOT / 'AGENTS.md'
RESUME_CONTEXT = ROOT / 'docs' / 'foundation' / 'resume-context.md'
REPORT_DIR = ROOT / 'tools' / 'harness-runtime' / 'artifacts' / 'governance-reports'

REQUIRED_CONTRACT_FILES = [
    'openapi/aurim-first-slice.v0.yaml',
    'workspace.v0.md',
    'git-workspace.v0.md',
    'factory-spec.v0.md',
    'factory-run.v0.md',
    'factory-artifact.v0.md',
    'schemas/workspace.schema.json',
    'schemas/git-workspace.schema.json',
    'schemas/factory-spec.schema.json',
    'schemas/factory-run.schema.json',
    'schemas/factory-artifact.schema.json',
]

REQUIRED_DECISION_KEYS = {
    'decision_id',
    'title',
    'status',
    'layer',
    'date',
    'context',
    'decision',
    'consequences',
    'owner',
    'related_paths',
}


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str


def file_exists_check(path: Path, label: str) -> CheckResult:
    if path.exists():
        return CheckResult(label, True, f'found: {path.relative_to(ROOT)}')
    return CheckResult(label, False, f'missing: {path.relative_to(ROOT)}')


def check_contract_presence() -> list[CheckResult]:
    results: list[CheckResult] = []
    for rel in REQUIRED_CONTRACT_FILES:
        path = CONTRACTS / rel
        results.append(file_exists_check(path, f'contract::{rel}'))
    return results


def check_decision_records() -> list[CheckResult]:
    results: list[CheckResult] = []
    if not DECISIONS_DIR.exists():
        return [CheckResult('decision_records_dir', False, 'missing docs/foundation/decisions directory')]

    records = sorted(DECISIONS_DIR.glob('DEC-*.json'))
    if not records:
        return [CheckResult('decision_records_present', False, 'no decision record files found')]

    results.append(CheckResult('decision_records_present', True, f'{len(records)} records found'))

    for record in records:
        try:
            payload = json.loads(record.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            results.append(CheckResult(f'decision_record::{record.name}', False, f'invalid json: {exc}'))
            continue

        missing = sorted(REQUIRED_DECISION_KEYS - payload.keys())
        if missing:
            results.append(
                CheckResult(
                    f'decision_record::{record.name}',
                    False,
                    f'missing required keys: {", ".join(missing)}',
                )
            )
            continue

        if not isinstance(payload.get('consequences'), list) or not payload['consequences']:
            results.append(
                CheckResult(
                    f'decision_record::{record.name}',
                    False,
                    'consequences must be a non-empty list',
                )
            )
            continue

        results.append(CheckResult(f'decision_record::{record.name}', True, 'schema-minimum keys present'))

    return results


def run_regression_if_requested(run_regression: bool) -> CheckResult:
    if not run_regression:
        return CheckResult('harness_regression', True, 'skipped (use --run-regression to execute)')

    cmd = ['python', 'tools/harness-runtime/scripts/unit_gate_regression.py']
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    output = (result.stdout + '\n' + result.stderr).strip()
    if result.returncode == 0:
        return CheckResult('harness_regression', True, output or 'passed')
    return CheckResult('harness_regression', False, output or f'failed with code {result.returncode}')


def write_report(results: list[CheckResult]) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    target = REPORT_DIR / f'governance-audit-{ts}.md'

    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed

    lines = [
        '# Governance Audit Report',
        '',
        f'- generated_at_utc: {datetime.now(timezone.utc).isoformat()}',
        f'- passed: {passed}',
        f'- failed: {failed}',
        '',
        '## Results',
        '',
        '| Check | Status | Detail |',
        '|---|---|---|',
    ]

    for item in results:
        status = 'PASS' if item.passed else 'FAIL'
        detail = item.detail.replace('|', '\\|').replace('\n', '<br>')
        lines.append(f'| {item.name} | {status} | {detail} |')

    target.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description='Audit governance and contract readiness for Aurim harness workflow.')
    parser.add_argument('--run-regression', action='store_true', help='run unit_gate_regression.py as part of audit')
    args = parser.parse_args()

    checks: list[CheckResult] = [
        file_exists_check(AGENTS, 'agents_file'),
        file_exists_check(DECISION_STATUS, 'decision_status_file'),
        file_exists_check(RESUME_CONTEXT, 'resume_context_file'),
    ]
    checks.extend(check_contract_presence())
    checks.extend(check_decision_records())
    checks.append(run_regression_if_requested(args.run_regression))

    report = write_report(checks)

    failures = [c for c in checks if not c.passed]
    print(f'governance audit report: {report.relative_to(ROOT)}')
    print(f'passed={len(checks) - len(failures)} failed={len(failures)}')

    if failures:
        for failure in failures:
            print(f'FAIL: {failure.name} -> {failure.detail}')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
