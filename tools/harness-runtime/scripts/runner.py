from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HARNESS = ROOT / 'tools' / 'harness-runtime'
RUNS = HARNESS / 'artifacts' / 'runs'
SPEC = HARNESS / 'specs' / 'product-spec.md'
SPRINT_TEMPLATE = HARNESS / 'contracts' / 'sprint-contract.template.md'
GENERATOR_TEMPLATE = HARNESS / 'contracts' / 'generator-report.template.md'
EVALUATOR_TEMPLATE = HARNESS / 'contracts' / 'evaluator-report.template.md'

REQUIRED_CONTRACT_HEADINGS = [
    '# Sprint Contract',
    '## Scope',
    '## In Scope',
    '## Out of Scope',
    '## Touched Paths',
    '## Acceptance Criteria',
    '## Evidence Required',
    '## Evaluator Checks',
]

REQUIRED_GENERATOR_HEADINGS = [
    '# Generator Report',
    '## Changed Files',
    '## Acceptance Mapping',
    '## Commands Run',
    '## Open Risks',
]

REQUIRED_EVALUATOR_HEADINGS = [
    '# Evaluator Report',
    '## Summary',
    '## Findings',
    '## Contract Compliance',
    '## Overall Verdict',
]


def fail(message: str) -> None:
    print(f'FAIL: {message}')
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f'OK: {message}')


def run_dir(run_id: str) -> Path:
    path = RUNS / run_id
    if not path.exists():
        fail(f'run not found: {path}')
    return path


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f'missing file: {path}')
    return path.read_text(encoding='utf-8')


def require_headings(text: str, headings: list[str], name: str) -> None:
    missing = [heading for heading in headings if heading not in text]
    if missing:
        fail(f'{name} missing headings: {", ".join(missing)}')


def require_no_placeholders(text: str, name: str) -> None:
    placeholders = ['TBD', '한 문장 요약', '구현 대상', '하지 않을 것', 'path/to/file', 'criterion 1 -> evidence']
    found = [item for item in placeholders if item in text]
    if found:
        fail(f'{name} still contains placeholders: {", ".join(found)}')


def extract_checked_items(section_text: str) -> list[str]:
    return re.findall(r'- \[x\] (.+)', section_text, flags=re.IGNORECASE)


def extract_paths(contract_text: str) -> list[str]:
    match = re.search(r'## Touched Paths\n(.*?)(?:\n## |\Z)', contract_text, flags=re.S)
    if not match:
        fail('could not find Touched Paths section')
    items = extract_checked_items(match.group(1))
    if not items:
        fail('Touched Paths must contain checked items')
    return items


def validate_paths(paths: list[str]) -> None:
    allowed_roots = ['apps/', 'tools/', 'packages/', 'docs/']
    for item in paths:
        normalized = item.replace('\\', '/')
        if not any(normalized.startswith(root) for root in allowed_roots):
            fail(f'touched path outside allowed roots: {item}')
        resolved = (ROOT / normalized).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            fail(f'touched path escapes workspace: {item}')


def extract_changed_files(generator_text: str) -> list[str]:
    match = re.search(r'## Changed Files\n(.*?)(?:\n## |\Z)', generator_text, flags=re.S)
    if not match:
        fail('could not find Changed Files section')
    items = re.findall(r'- (.+)', match.group(1))
    if not items:
        fail('Changed Files must list at least one file')
    return items


def ensure_changed_files_within_scope(changed_files: list[str], touched_paths: list[str]) -> None:
    touched = [path.replace('\\', '/') for path in touched_paths]
    for file in changed_files:
        normalized = file.replace('\\', '/')
        if not any(normalized == path.rstrip('/') or normalized.startswith(path.rstrip('/') + '/') for path in touched):
            fail(f'changed file outside touched paths: {file}')


def create_run(run_id: str) -> None:
    if not SPEC.exists():
        fail(f'spec not found: {SPEC}')
    target = RUNS / run_id
    if target.exists():
        fail(f'run already exists: {target}')

    target.mkdir(parents=True)
    shutil.copyfile(SPEC, target / '00_spec_snapshot.md')
    shutil.copyfile(SPRINT_TEMPLATE, target / '01_sprint_contract.md')
    shutil.copyfile(GENERATOR_TEMPLATE, target / '02_generator_report.md')
    shutil.copyfile(EVALUATOR_TEMPLATE, target / '03_evaluator_report.md')

    manifest = {
        'run_id': run_id,
        'status': 'created',
        'required_sequence': [
            '00_spec_snapshot.md',
            '01_sprint_contract.md',
            '02_generator_report.md',
            '03_evaluator_report.md',
        ],
    }
    (target / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    ok(f'created run: {target}')


def validate_contract(run_id: str) -> None:
    target = run_dir(run_id)
    contract = read_text(target / '01_sprint_contract.md')
    require_headings(contract, REQUIRED_CONTRACT_HEADINGS, 'sprint contract')
    require_no_placeholders(contract, 'sprint contract')
    touched_paths = extract_paths(contract)
    validate_paths(touched_paths)
    ok('sprint contract is structurally valid')


def gate_generator(run_id: str) -> None:
    target = run_dir(run_id)
    validate_contract(run_id)
    contract = read_text(target / '01_sprint_contract.md')
    touched_paths = extract_paths(contract)
    for touched_path in touched_paths:
        resolved = ROOT / touched_path
        if not resolved.exists():
            fail(f'touched path does not exist yet: {touched_path}')
    ok('generator gate passed')


def gate_close(run_id: str) -> None:
    target = run_dir(run_id)
    validate_contract(run_id)
    contract = read_text(target / '01_sprint_contract.md')
    generator = read_text(target / '02_generator_report.md')
    evaluator = read_text(target / '03_evaluator_report.md')

    require_headings(generator, REQUIRED_GENERATOR_HEADINGS, 'generator report')
    require_headings(evaluator, REQUIRED_EVALUATOR_HEADINGS, 'evaluator report')
    require_no_placeholders(generator, 'generator report')
    require_no_placeholders(evaluator, 'evaluator report')

    touched_paths = extract_paths(contract)
    changed_files = extract_changed_files(generator)
    ensure_changed_files_within_scope(changed_files, touched_paths)

    if 'PASS' not in re.search(r'## Overall Verdict\n(.*?)(?:\n## |\Z)', evaluator, flags=re.S).group(1):
        fail('evaluator report is not PASS')

    compliance_section = re.search(r'## Contract Compliance\n(.*?)(?:\n## |\Z)', evaluator, flags=re.S)
    if not compliance_section:
        fail('missing Contract Compliance section')
    checked = extract_checked_items(compliance_section.group(1))
    if len(checked) < 4:
        fail('not all contract compliance checks are marked complete')

    ok('close gate passed: sprint may be treated as complete')


def main() -> None:
    parser = argparse.ArgumentParser(description='Aurim harness runner')
    sub = parser.add_subparsers(dest='command', required=True)

    create = sub.add_parser('create-run')
    create.add_argument('--run-id', required=True)

    validate = sub.add_parser('validate-contract')
    validate.add_argument('--run-id', required=True)

    gate_gen = sub.add_parser('gate-generator')
    gate_gen.add_argument('--run-id', required=True)

    gate_close_parser = sub.add_parser('gate-close')
    gate_close_parser.add_argument('--run-id', required=True)

    args = parser.parse_args()

    if args.command == 'create-run':
        create_run(args.run_id)
    elif args.command == 'validate-contract':
        validate_contract(args.run_id)
    elif args.command == 'gate-generator':
        gate_generator(args.run_id)
    elif args.command == 'gate-close':
        gate_close(args.run_id)
    else:
        fail(f'unknown command: {args.command}')


if __name__ == '__main__':
    main()

