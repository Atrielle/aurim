from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from harness_core import baseline_ops, cli_ops, contract_ops, gate_ops, io_utils, manifest_ops, path_policy, unit_ops, validators

ROOT = Path(__file__).resolve().parents[3]
HARNESS = ROOT / 'tools' / 'harness-runtime'
RUNS = HARNESS / 'artifacts' / 'runs'
RUNNER_STATE = HARNESS / '.runner-state'
FREEZE_PROOFS = RUNNER_STATE / 'freeze-proofs'
BASELINE_PROOFS = RUNNER_STATE / 'baseline-proofs'
SPEC = HARNESS / 'specs' / 'product-spec.md'
RUN_CONTRACT_TEMPLATE = HARNESS / 'contracts' / 'run-contract.template.json'
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

REQUIRED_UNIT_REPORT_HEADINGS = [
    '# Unit Report',
    '## Summary',
    '## Changed Files',
    '## Acceptance Mapping',
    '## Evidence',
]

REQUIRED_RUN_CONTRACT_KEYS = [
    'version',
    'run_id',
    'objective',
    'authoritative_inputs',
    'blocking_rule',
    'in_scope',
    'out_of_scope',
    'touched_paths',
    'acceptance_criteria',
    'work_units',
    'evaluator_checks',
]

RUN_MANIFEST_TEMPLATE_KEYS = [
    'run_id',
    'status',
    'required_sequence',
]

REQUIRED_WORK_UNIT_KEYS = [
    'id',
    'title',
    'objective',
    'touched_paths',
    'acceptance_criteria_ids',
    'required_evidence',
    'agent_budget',
]

PLACEHOLDER_SNIPPETS = [
    'TBD',
    '한 문장 요약',
    '구현 대상',
    '하지 않을 것',
    'path/to/file',
    'criterion 1 -> evidence',
    'Replace with',
    'replace-run-id',
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
    try:
        return io_utils.read_text(path)
    except FileNotFoundError:
        fail(f'missing file: {path}')


def read_json(path: Path) -> dict:
    try:
        return io_utils.read_json(path)
    except FileNotFoundError:
        fail(f'missing file: {path}')
    except json.JSONDecodeError as exc:
        fail(f'invalid json in {path}: {exc}')
    raise AssertionError('unreachable')


def write_json(path: Path, payload: dict) -> None:
    io_utils.write_json(path, payload)


def hash_text(text: str) -> str:
    return io_utils.hash_text(text)


def require_headings(text: str, headings: list[str], name: str) -> None:
    missing = validators.require_headings(text, headings, name)
    if missing:
        fail(f'{name} missing headings: {", ".join(missing)}')


def require_no_placeholders(text: str, name: str) -> None:
    found = validators.require_no_placeholders(text, PLACEHOLDER_SNIPPETS)
    if found:
        fail(f'{name} still contains placeholders: {", ".join(found)}')


def extract_checked_items(section_text: str) -> list[str]:
    return validators.extract_checked_items(section_text)


def extract_paths(contract_text: str) -> list[str]:
    items = validators.extract_paths(contract_text)
    if not items and '## Touched Paths' not in contract_text:
        fail('could not find Touched Paths section')
    if not items:
        fail('Touched Paths must contain checked items')
    return items


def validate_paths(paths: list[str]) -> None:
    errors = path_policy.validate_paths(paths, ROOT)
    if errors:
        fail(errors[0])


def is_within_touched_paths(path: str, touched_paths: list[str]) -> bool:
    return path_policy.is_within_touched_paths(path, touched_paths)


def iter_touched_files(touched_paths: list[str]) -> list[str]:
    return path_policy.iter_touched_files(ROOT, touched_paths)


def hash_file(path: Path) -> str:
    return io_utils.hash_file(path)


def build_snapshot(touched_paths: list[str]) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for relative_path in iter_touched_files(touched_paths):
        snapshot[relative_path] = hash_file(ROOT / relative_path)
    return snapshot


def build_run_artifact_snapshot(run_id: str) -> dict[str, str]:
    snapshot = build_snapshot([run_relative_dir(run_id)])
    snapshot.pop(run_manifest_path(run_id), None)
    return snapshot


def manifest_template_hash(manifest: dict) -> str:
    payload = {key: manifest[key] for key in RUN_MANIFEST_TEMPLATE_KEYS}
    return hash_text(json.dumps(payload, sort_keys=True, separators=(',', ':')))


def build_template_snapshot(run_id: str, manifest: dict, touched_paths: list[str]) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for relative_path in iter_touched_files(touched_paths):
        if relative_path == run_manifest_path(run_id):
            snapshot[relative_path] = manifest_template_hash(manifest)
        else:
            snapshot[relative_path] = hash_file(ROOT / relative_path)
    return snapshot


def current_template_hash(relative_path: str, run_id: str) -> str:
    if relative_path == run_manifest_path(run_id):
        manifest = read_manifest(run_id)
        return manifest_template_hash(manifest)
    return hash_file(ROOT / relative_path)


def git_status_files() -> list[str]:
    result = subprocess.run(
        ['git', '-C', str(ROOT), 'status', '--short', '--untracked-files=all'],
        capture_output=True,
        text=True,
        check=True,
    )
    files: list[str] = []
    for line in result.stdout.splitlines():
        raw_path = line[3:].strip()
        if not raw_path:
            continue
        if ' -> ' in raw_path:
            raw_path = raw_path.split(' -> ', 1)[1]
        files.append(raw_path.replace('\\', '/'))
    return sorted(set(files))


def run_relative_dir(run_id: str) -> str:
    return f'tools/harness-runtime/artifacts/runs/{run_id}'


def run_manifest_path(run_id: str) -> str:
    return f'{run_relative_dir(run_id)}/manifest.json'


def freeze_proof_path(run_id: str) -> Path:
    return FREEZE_PROOFS / f'{run_id}.json'


def freeze_proof_relative_path(run_id: str) -> str:
    return freeze_proof_path(run_id).relative_to(ROOT).as_posix()


def baseline_proof_path(run_id: str) -> Path:
    return BASELINE_PROOFS / f'{run_id}.json'


def generator_ignored_paths(run_id: str) -> set[str]:
    run_dir_relative = run_relative_dir(run_id)
    return {
        f'{run_dir_relative}/03_evaluator_report.md',
        f'{run_dir_relative}/manifest.json',
    }


def require_non_empty_string(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f'{name} must be a non-empty string')
    if any(snippet in value for snippet in PLACEHOLDER_SNIPPETS):
        fail(f'{name} still contains placeholders')
    return value.strip()


def require_string_list(value: object, name: str) -> list[str]:
    if not isinstance(value, list) or not value:
        fail(f'{name} must be a non-empty list')
    result: list[str] = []
    for index, item in enumerate(value):
        result.append(require_non_empty_string(item, f'{name}[{index}]'))
    return result


def read_run_contract(run_id: str) -> dict:
    target = run_dir(run_id)
    path = target / '01_run_contract.json'
    contract = read_json(path)

    missing_keys = [key for key in REQUIRED_RUN_CONTRACT_KEYS if key not in contract]
    if missing_keys:
        fail(f'run contract missing keys: {", ".join(missing_keys)}')

    if contract['run_id'] != run_id:
        fail(f'run contract run_id mismatch: expected {run_id}, got {contract["run_id"]}')

    require_non_empty_string(contract['version'], 'run contract version')
    require_non_empty_string(contract['objective'], 'run contract objective')
    require_non_empty_string(contract['blocking_rule'], 'run contract blocking_rule')

    authoritative_inputs = require_string_list(contract['authoritative_inputs'], 'run contract authoritative_inputs')
    for item in authoritative_inputs:
        resolved = (ROOT / item).resolve()
        if not resolved.exists():
            fail(f'authoritative input does not exist: {item}')
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            fail(f'authoritative input escapes workspace: {item}')

    require_string_list(contract['in_scope'], 'run contract in_scope')
    require_string_list(contract['out_of_scope'], 'run contract out_of_scope')

    touched_paths = require_string_list(contract['touched_paths'], 'run contract touched_paths')
    validate_paths(touched_paths)

    acceptance_criteria = contract['acceptance_criteria']
    if not isinstance(acceptance_criteria, list) or not acceptance_criteria:
        fail('run contract acceptance_criteria must be a non-empty list')

    criterion_ids: list[str] = []
    for index, item in enumerate(acceptance_criteria):
        if not isinstance(item, dict):
            fail(f'acceptance_criteria[{index}] must be an object')
        criterion_id = require_non_empty_string(item.get('id'), f'acceptance_criteria[{index}].id')
        if criterion_id in criterion_ids:
            fail(f'duplicate acceptance criterion id: {criterion_id}')
        criterion_ids.append(criterion_id)
        require_non_empty_string(item.get('statement'), f'acceptance_criteria[{index}].statement')
        require_string_list(item.get('required_evidence'), f'acceptance_criteria[{index}].required_evidence')

    require_string_list(contract['evaluator_checks'], 'run contract evaluator_checks')
    work_units = contract['work_units']
    if not isinstance(work_units, list) or not work_units:
        fail('run contract work_units must be a non-empty list')

    unit_ids: list[str] = []
    for index, unit in enumerate(work_units):
        if not isinstance(unit, dict):
            fail(f'work_units[{index}] must be an object')
        missing_unit_keys = [key for key in REQUIRED_WORK_UNIT_KEYS if key not in unit]
        if missing_unit_keys:
            fail(f'work_units[{index}] missing keys: {", ".join(missing_unit_keys)}')

        unit_id = require_non_empty_string(unit['id'], f'work_units[{index}].id')
        if unit_id in unit_ids:
            fail(f'duplicate work unit id: {unit_id}')
        unit_ids.append(unit_id)

        require_non_empty_string(unit['title'], f'work_units[{index}].title')
        require_non_empty_string(unit['objective'], f'work_units[{index}].objective')
        unit_paths = require_string_list(unit['touched_paths'], f'work_units[{index}].touched_paths')
        validate_paths(unit_paths)
        for unit_path in unit_paths:
            if not is_within_touched_paths(unit_path, touched_paths):
                fail(f'work_units[{index}] touched path outside run touched_paths: {unit_path}')

        mapped_criteria = require_string_list(
            unit['acceptance_criteria_ids'],
            f'work_units[{index}].acceptance_criteria_ids',
        )
        unknown_criteria = [criterion for criterion in mapped_criteria if criterion not in criterion_ids]
        if unknown_criteria:
            fail(f'work_units[{index}] has unknown acceptance_criteria_ids: {", ".join(unknown_criteria)}')

        require_string_list(unit['required_evidence'], f'work_units[{index}].required_evidence')
        budget = unit['agent_budget']
        if not isinstance(budget, dict):
            fail(f'work_units[{index}].agent_budget must be an object')
        max_input_tokens = budget.get('max_input_tokens')
        max_output_tokens = budget.get('max_output_tokens')
        if not isinstance(max_input_tokens, int) or max_input_tokens <= 0:
            fail(f'work_units[{index}].agent_budget.max_input_tokens must be a positive integer')
        if not isinstance(max_output_tokens, int) or max_output_tokens <= 0:
            fail(f'work_units[{index}].agent_budget.max_output_tokens must be a positive integer')
        depends_on = budget.get('depends_on', [])
        if depends_on is None:
            depends_on = []
        if not isinstance(depends_on, list):
            fail(f'work_units[{index}].agent_budget.depends_on must be a list when provided')
        unit['agent_budget']['depends_on'] = [
            require_non_empty_string(dep, f'work_units[{index}].agent_budget.depends_on')
            for dep in depends_on
        ]

    for unit in work_units:
        for dependency in unit['agent_budget']['depends_on']:
            if dependency not in unit_ids:
                fail(f'unknown work unit dependency: {dependency}')
            if dependency == unit['id']:
                fail(f'work unit cannot depend on itself: {dependency}')

    contract['_criterion_ids'] = criterion_ids
    contract['_touched_paths'] = touched_paths
    contract['_work_unit_ids'] = unit_ids
    return contract


def read_manifest(run_id: str) -> dict:
    return read_json(run_dir(run_id) / 'manifest.json')


def write_manifest(run_id: str, manifest: dict) -> None:
    write_json(run_dir(run_id) / 'manifest.json', manifest)


def write_freeze_proof(run_id: str, payload: dict) -> None:
    FREEZE_PROOFS.mkdir(parents=True, exist_ok=True)
    write_json(freeze_proof_path(run_id), payload)


def read_freeze_proof(run_id: str) -> dict:
    return read_json(freeze_proof_path(run_id))


def write_baseline_proof(run_id: str, payload: dict) -> None:
    BASELINE_PROOFS.mkdir(parents=True, exist_ok=True)
    write_json(baseline_proof_path(run_id), payload)


def read_baseline_proof(run_id: str) -> dict:
    return read_json(baseline_proof_path(run_id))


def record_gate_completion(run_id: str, gate_name: str, status: str) -> None:
    manifest = read_manifest(run_id)
    manifest = manifest_ops.record_gate_completion(manifest, gate_name, status)
    write_manifest(run_id, manifest)


def ensure_gate_completed(manifest: dict, gate_name: str, *, context: str) -> None:
    try:
        manifest_ops.ensure_gate_completed(manifest, gate_name, context=context)
    except ValueError as exc:
        fail(str(exc))


def extract_changed_files(generator_text: str) -> list[str]:
    try:
        return unit_ops.extract_changed_files(generator_text)
    except ValueError as exc:
        fail(str(exc))


def extract_acceptance_mapping_ids(generator_text: str) -> list[str]:
    try:
        return unit_ops.extract_acceptance_mapping_ids(generator_text)
    except ValueError as exc:
        fail(str(exc))


def extract_acceptance_mapping_ids_generic(text: str) -> list[str]:
    return extract_acceptance_mapping_ids(text)


def ensure_changed_files_within_scope(changed_files: list[str], touched_paths: list[str]) -> None:
    try:
        unit_ops.ensure_changed_files_within_scope(changed_files, touched_paths, is_within_touched_paths)
    except ValueError as exc:
        fail(str(exc))


def validate_freeze_proof(run_id: str, *, require_prebaseline_state: bool) -> dict:
    proof = read_freeze_proof(run_id)
    expected_contracts = {
        f'{run_relative_dir(run_id)}/01_run_contract.json',
        f'{run_relative_dir(run_id)}/01_sprint_contract.md',
    }
    try:
        baseline_ops.validate_freeze_proof(
            proof,
            run_id=run_id,
            expected_contracts=expected_contracts,
            hash_for_path=lambda relative_path: hash_file(ROOT / relative_path),
            require_prebaseline_state=require_prebaseline_state,
            current_run_artifact_snapshot=build_run_artifact_snapshot(run_id),
            current_manifest_hash=hash_file(run_dir(run_id) / 'manifest.json'),
        )
    except ValueError as exc:
        fail(str(exc))

    return proof


def validate_baseline_proof(run_id: str) -> dict:
    proof = read_baseline_proof(run_id)
    try:
        baseline_ops.validate_baseline_proof(proof, run_id=run_id)
    except ValueError as exc:
        fail(str(exc))
    return proof


def capture_baseline(run_id: str, touched_paths: list[str], freeze_proof: dict) -> None:
    manifest = read_manifest(run_id)
    if baseline_proof_path(run_id).exists():
        return
    frozen_snapshot = freeze_proof['run_artifact_snapshot']
    frozen_manifest_hash = freeze_proof['manifest_hash']

    dirty_files = {
        path for path in git_status_files() if is_within_touched_paths(path, touched_paths)
    }
    dirty_files, exemptable_files = baseline_ops.split_dirty_files(
        dirty_files=dirty_files,
        run_manifest_path=run_manifest_path(run_id),
        frozen_manifest_hash=frozen_manifest_hash,
        frozen_snapshot=frozen_snapshot,
        hash_for_path=lambda relative_path: hash_file(ROOT / relative_path),
    )
    if dirty_files:
        fail(f'touched paths are already dirty before baseline capture: {", ".join(sorted(dirty_files))}')

    baseline_snapshot = build_snapshot(touched_paths)
    write_baseline_proof(
        run_id,
        {
            'run_id': run_id,
            'captured_via': 'gate-generator',
            'baseline_snapshot': baseline_snapshot,
            'baseline_git_dirty_files': sorted(exemptable_files),
        },
    )
    manifest['baseline_snapshot'] = baseline_snapshot
    manifest['baseline_git_dirty_files'] = sorted(exemptable_files)
    manifest['baseline_captured_via'] = 'gate-generator'
    write_manifest(run_id, manifest)


def actual_changed_files(run_id: str, touched_paths: list[str]) -> list[str]:
    baseline_snapshot = validate_baseline_proof(run_id)['baseline_snapshot']
    current_snapshot = build_snapshot(touched_paths)
    return baseline_ops.actual_changed_files(
        baseline_snapshot,
        current_snapshot,
        generator_ignored_paths(run_id),
    )


def create_run(run_id: str) -> None:
    if not SPEC.exists():
        fail(f'spec not found: {SPEC}')
    target = RUNS / run_id
    if target.exists():
        fail(f'run already exists: {target}')
    if freeze_proof_path(run_id).exists():
        fail(f'runner-owned freeze proof already exists: {freeze_proof_path(run_id)}')
    if baseline_proof_path(run_id).exists():
        fail(f'runner-owned baseline proof already exists: {baseline_proof_path(run_id)}')

    target.mkdir(parents=True)
    shutil.copyfile(SPEC, target / '00_spec_snapshot.md')
    contract_text = read_text(RUN_CONTRACT_TEMPLATE).replace('replace-run-id', run_id)
    (target / '01_run_contract.json').write_text(contract_text, encoding='utf-8')
    shutil.copyfile(SPRINT_TEMPLATE, target / '01_sprint_contract.md')
    shutil.copyfile(GENERATOR_TEMPLATE, target / '02_generator_report.md')
    shutil.copyfile(EVALUATOR_TEMPLATE, target / '03_evaluator_report.md')

    manifest = {
        'run_id': run_id,
        'status': 'created',
        'required_sequence': [
            '00_spec_snapshot.md',
            '01_run_contract.json',
            '01_sprint_contract.md',
            '02_generator_report.md',
            '03_evaluator_report.md',
        ],
        'completed_gates': [],
    }
    (target / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    manifest['template_snapshot'] = build_template_snapshot(run_id, manifest, touched_paths=[f'{run_relative_dir(run_id)}'])
    (target / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    ok(f'created run: {target}')


def validate_contract(run_id: str) -> None:
    target = run_dir(run_id)
    run_contract = read_run_contract(run_id)
    contract = read_text(target / '01_sprint_contract.md')
    try:
        contract_ops.validate_sprint_contract(
            contract,
            required_headings=REQUIRED_CONTRACT_HEADINGS,
            require_headings=require_headings,
            require_no_placeholders=require_no_placeholders,
            extract_paths=extract_paths,
            expected_touched_paths=run_contract['_touched_paths'],
        )
    except ValueError as exc:
        fail(str(exc))
    ok('sprint contract is structurally valid')


def freeze_contract(run_id: str) -> None:
    validate_contract(run_id)
    run_contract = read_run_contract(run_id)
    manifest = read_manifest(run_id)
    template_snapshot = manifest.get('template_snapshot')
    if not isinstance(template_snapshot, dict):
        fail('template snapshot is missing; rerun create-run')
    if manifest.get('frozen_contract_captured_via') == 'freeze-contract':
        fail('contract is already frozen')
    if freeze_proof_path(run_id).exists():
        fail('runner-owned freeze proof already exists')

    current_snapshot = build_run_artifact_snapshot(run_id)
    expected_template_files = {
        f'{run_relative_dir(run_id)}/00_spec_snapshot.md',
        f'{run_relative_dir(run_id)}/02_generator_report.md',
        f'{run_relative_dir(run_id)}/03_evaluator_report.md',
    }
    authored_contract_files = {
        f'{run_relative_dir(run_id)}/01_run_contract.json',
        f'{run_relative_dir(run_id)}/01_sprint_contract.md',
    }

    for path in expected_template_files:
        if current_snapshot.get(path) != template_snapshot.get(path):
            fail(f'non-contract artifact was edited before freeze: {path}')

    for path in authored_contract_files:
        if current_snapshot.get(path) == template_snapshot.get(path):
            fail(f'authored contract file was not updated before freeze: {path}')

    manifest['frozen_snapshot'] = current_snapshot
    manifest['frozen_contract_captured_via'] = 'freeze-contract'
    manifest['frozen_contract_fields'] = sorted(authored_contract_files)
    write_manifest(run_id, manifest)
    record_gate_completion(run_id, 'freeze-contract', 'contract_frozen')
    write_freeze_proof(
        run_id,
        {
            'run_id': run_id,
            'captured_via': 'freeze-contract',
            'contract_hashes': {
                relative_path: hash_file(ROOT / relative_path)
                for relative_path in sorted(authored_contract_files)
            },
            'run_artifact_snapshot': build_run_artifact_snapshot(run_id),
            'manifest_hash': hash_file(run_dir(run_id) / 'manifest.json'),
        },
    )
    ok('contract frozen')


def gate_generator(run_id: str) -> None:
    validate_contract(run_id)
    run_contract = read_run_contract(run_id)
    manifest = read_manifest(run_id)
    ensure_gate_completed(manifest, 'gate-units', context='gate-generator')
    touched_paths = run_contract['_touched_paths']
    for touched_path in touched_paths:
        resolved = ROOT / touched_path
        if not resolved.exists():
            fail(f'touched path does not exist yet: {touched_path}')
    freeze_proof = validate_freeze_proof(run_id, require_prebaseline_state=True)
    capture_baseline(run_id, touched_paths, freeze_proof)
    record_gate_completion(run_id, 'gate-generator', 'baseline_captured')
    ok('generator gate passed and baseline captured')


def gate_close(run_id: str) -> None:
    target = run_dir(run_id)
    validate_contract(run_id)
    run_contract = read_run_contract(run_id)
    manifest = read_manifest(run_id)
    ensure_gate_completed(manifest, 'gate-units', context='gate-close')
    validate_freeze_proof(run_id, require_prebaseline_state=False)
    validate_baseline_proof(run_id)
    generator = read_text(target / '02_generator_report.md')
    evaluator = read_text(target / '03_evaluator_report.md')

    require_headings(generator, REQUIRED_GENERATOR_HEADINGS, 'generator report')
    require_headings(evaluator, REQUIRED_EVALUATOR_HEADINGS, 'evaluator report')
    require_no_placeholders(generator, 'generator report')
    require_no_placeholders(evaluator, 'evaluator report')

    touched_paths = run_contract['_touched_paths']
    reported_changed_files = sorted(file.replace('\\', '/') for file in extract_changed_files(generator))
    ensure_changed_files_within_scope(reported_changed_files, touched_paths)
    measured_changed_files = actual_changed_files(run_id, touched_paths)
    current_git_dirty = {
        path for path in git_status_files() if is_within_touched_paths(path, touched_paths)
    }

    try:
        gate_ops.validate_reported_vs_measured_changes(reported_changed_files, measured_changed_files)
        gate_ops.ensure_measured_files_visible_in_git(measured_changed_files, current_git_dirty)
    except ValueError as exc:
        fail(str(exc))

    mapped_ids = extract_acceptance_mapping_ids(generator)

    missing_ids = [item for item in run_contract['_criterion_ids'] if item not in mapped_ids]
    if missing_ids:
        fail(f'generator report is missing acceptance mappings for: {", ".join(missing_ids)}')

    try:
        gate_ops.validate_evaluator_pass(evaluator, extract_checked_items)
    except ValueError as exc:
        fail(str(exc))

    record_gate_completion(run_id, 'gate-close', 'passed')
    ok('close gate passed: sprint may be treated as complete')


def topological_work_units(work_units: list[dict]) -> list[dict]:
    try:
        return contract_ops.topological_work_units(work_units)
    except ValueError as exc:
        fail(str(exc))
    raise AssertionError('unreachable')


def read_unit_plan(run_id: str) -> dict:
    target = run_dir(run_id) / '04_unit_plan.json'
    if not target.exists():
        fail('unit plan missing; run plan-units first')
    payload = read_json(target)
    if payload.get('run_id') != run_id:
        fail('unit plan run_id mismatch')
    units = payload.get('units')
    if not isinstance(units, list) or not units:
        fail('unit plan units is invalid')
    return payload


def write_unit_plan(run_id: str, payload: dict) -> None:
    write_json(run_dir(run_id) / '04_unit_plan.json', payload)


def unit_reports_dir(run_id: str) -> Path:
    path = run_dir(run_id) / '05_unit_reports'
    path.mkdir(parents=True, exist_ok=True)
    return path


def unit_report_path(run_id: str, unit_id: str) -> Path:
    return unit_reports_dir(run_id) / f'{unit_id}.md'


def unit_evidence_path(run_id: str, unit_id: str) -> Path:
    return unit_reports_dir(run_id) / f'{unit_id}.evidence.json'


def find_unit(plan: dict, unit_id: str) -> dict:
    for unit in plan['units']:
        if unit.get('id') == unit_id:
            return unit
    fail(f'unit not found in plan: {unit_id}')
    raise AssertionError('unreachable')


def ensure_unit_dependencies_satisfied(plan: dict, unit: dict) -> None:
    by_id = {item['id']: item for item in plan['units']}
    for dependency in unit.get('depends_on', []):
        dependency_unit = by_id.get(dependency)
        if dependency_unit is None:
            fail(f'unit dependency missing from plan: {dependency}')
        if dependency_unit.get('status') != 'collected':
            fail(f'unit dependency not collected yet: {dependency}')


def validate_unit_report_text(report_text: str, unit: dict) -> tuple[list[str], list[str]]:
    try:
        return unit_ops.validate_unit_report_text(
            report_text,
            required_headings=REQUIRED_UNIT_REPORT_HEADINGS,
            placeholder_snippets=PLACEHOLDER_SNIPPETS,
            require_headings=require_headings,
            require_no_placeholders=require_no_placeholders,
            acceptance_criteria_ids=unit['acceptance_criteria_ids'],
            touched_paths=unit['touched_paths'],
            in_scope=is_within_touched_paths,
        )
    except ValueError as exc:
        fail(str(exc))
    raise AssertionError('unreachable')


def build_file_hash_snapshot(files: list[str]) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for relative_path in files:
        resolved = (ROOT / relative_path).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            fail(f'changed file escapes workspace: {relative_path}')
        if not resolved.exists() or not resolved.is_file():
            fail(f'changed file does not exist for evidence snapshot: {relative_path}')
        snapshot[relative_path] = hash_file(resolved)
    return snapshot


def plan_units(run_id: str) -> None:
    validate_contract(run_id)
    contract = read_run_contract(run_id)
    ordered_units = topological_work_units(contract['work_units'])
    unit_plan = {
        'run_id': run_id,
        'status': 'planned',
        'units': [
            {
                'id': unit['id'],
                'title': unit['title'],
                'objective': unit['objective'],
                'depends_on': unit['agent_budget']['depends_on'],
                'touched_paths': unit['touched_paths'],
                'acceptance_criteria_ids': unit['acceptance_criteria_ids'],
                'required_evidence': unit['required_evidence'],
                'agent_budget': {
                    'max_input_tokens': unit['agent_budget']['max_input_tokens'],
                    'max_output_tokens': unit['agent_budget']['max_output_tokens'],
                },
                'status': 'pending',
            }
            for unit in ordered_units
        ],
    }
    target = run_dir(run_id) / '04_unit_plan.json'
    write_json(target, unit_plan)
    manifest = read_manifest(run_id)
    manifest['unit_plan_ref'] = f'{run_relative_dir(run_id)}/04_unit_plan.json'
    manifest['planned_units'] = [unit['id'] for unit in ordered_units]
    write_manifest(run_id, manifest)
    ok(f'unit plan written: {target}')


def collect_unit(run_id: str, unit_id: str, report: str) -> None:
    plan = read_unit_plan(run_id)
    unit = find_unit(plan, unit_id)
    ensure_unit_dependencies_satisfied(plan, unit)
    report_path = (ROOT / report).resolve()
    if not report_path.exists():
        fail(f'unit report source file not found: {report}')
    try:
        report_path.relative_to(ROOT)
    except ValueError:
        fail(f'unit report source escapes workspace: {report}')

    report_text = report_path.read_text(encoding='utf-8')
    mapped_ids, changed_files = validate_unit_report_text(report_text, unit)

    target = unit_report_path(run_id, unit_id)
    target.write_text(report_text, encoding='utf-8')
    evidence_snapshot = build_file_hash_snapshot(changed_files)
    evidence_target = unit_evidence_path(run_id, unit_id)
    write_json(
        evidence_target,
        {
            'run_id': run_id,
            'unit_id': unit_id,
            'captured_via': 'collect-unit',
            'reported_changed_files': changed_files,
            'file_hashes': evidence_snapshot,
        },
    )
    unit['status'] = 'collected'
    unit['report_ref'] = target.relative_to(ROOT).as_posix()
    unit['evidence_ref'] = evidence_target.relative_to(ROOT).as_posix()
    unit['mapped_acceptance_criteria_ids'] = sorted(set(mapped_ids))
    unit['reported_changed_files'] = changed_files
    write_unit_plan(run_id, plan)

    manifest = read_manifest(run_id)
    manifest = manifest_ops.append_collected_unit(manifest, unit_id)
    write_manifest(run_id, manifest)
    ok(f'collected unit report: {target}')


def dispatch_unit(run_id: str, unit_id: str) -> None:
    contract = read_run_contract(run_id)
    plan = read_unit_plan(run_id)
    unit = find_unit(plan, unit_id)
    ensure_unit_dependencies_satisfied(plan, unit)
    if unit.get('status') == 'collected':
        fail(f'unit already collected: {unit_id}')

    acceptance = {
        item['id']: item
        for item in contract['acceptance_criteria']
        if item['id'] in unit['acceptance_criteria_ids']
    }
    payload = {
        'run_id': run_id,
        'unit_id': unit['id'],
        'title': unit['title'],
        'objective': unit['objective'],
        'touched_paths': unit['touched_paths'],
        'acceptance_criteria': [
            {
                'id': criterion_id,
                'statement': acceptance[criterion_id]['statement'],
                'required_evidence': acceptance[criterion_id]['required_evidence'],
            }
            for criterion_id in unit['acceptance_criteria_ids']
        ],
        'required_evidence': unit['required_evidence'],
        'agent_budget': unit['agent_budget'],
        'report_template': 'tools/harness-runtime/contracts/unit-report.template.md',
    }

    target = unit_reports_dir(run_id) / f'{unit_id}.dispatch.json'
    write_json(target, payload)
    if unit.get('status') == 'pending':
        unit['status'] = 'dispatched'
    unit['dispatch_ref'] = target.relative_to(ROOT).as_posix()
    write_unit_plan(run_id, plan)
    manifest = read_manifest(run_id)
    dispatched = manifest.get('dispatched_units', [])
    if not isinstance(dispatched, list):
        dispatched = []
    if unit_id not in dispatched:
        dispatched.append(unit_id)
    manifest['dispatched_units'] = sorted(dispatched)
    write_manifest(run_id, manifest)
    ok(f'dispatch payload written: {target}')


def gate_units(run_id: str) -> None:
    plan = read_unit_plan(run_id)
    for unit in plan['units']:
        unit_id = unit['id']
        report_ref = unit.get('report_ref')
        if unit.get('status') != 'collected' or not isinstance(report_ref, str):
            fail(f'unit is not collected: {unit_id}')
        report_path = (ROOT / report_ref).resolve()
        if not report_path.exists():
            fail(f'unit report missing for {unit_id}: {report_ref}')
        report_text = report_path.read_text(encoding='utf-8')
        _, changed_files = validate_unit_report_text(report_text, unit)
        evidence_ref = unit.get('evidence_ref')
        if not isinstance(evidence_ref, str):
            fail(f'unit evidence missing for {unit_id}')
        evidence_path = (ROOT / evidence_ref).resolve()
        if not evidence_path.exists():
            fail(f'unit evidence file missing for {unit_id}: {evidence_ref}')
        evidence = read_json(evidence_path)
        if evidence.get('run_id') != run_id or evidence.get('unit_id') != unit_id:
            fail(f'unit evidence identity mismatch for {unit_id}')
        hashes = evidence.get('file_hashes')
        if not isinstance(hashes, dict):
            fail(f'unit evidence hashes are invalid for {unit_id}')
        expected_files = sorted(changed_files)
        if sorted(hashes.keys()) != expected_files:
            fail(f'unit evidence file list mismatch for {unit_id}')
        current_hashes = build_file_hash_snapshot(expected_files)
        if current_hashes != hashes:
            fail(f'unit evidence hashes changed after collection for {unit_id}')

    manifest = read_manifest(run_id)
    manifest['unit_gate'] = 'passed'
    write_manifest(run_id, manifest)
    record_gate_completion(run_id, 'gate-units', 'units_ready')
    ok('unit gate passed')


def run_status(run_id: str) -> None:
    manifest = read_manifest(run_id)
    payload: dict = {
        'run_id': run_id,
        'status': manifest.get('status', 'unknown'),
        'completed_gates': manifest.get('completed_gates', []),
        'planned_units': manifest.get('planned_units', []),
        'dispatched_units': manifest.get('dispatched_units', []),
        'collected_units': manifest.get('collected_units', []),
        'unit_gate': manifest.get('unit_gate', 'pending'),
        'last_sequence_report_ref': manifest.get('last_sequence_report_ref'),
        'sequence_reports': manifest.get('sequence_reports', []),
    }
    unit_plan_path = run_dir(run_id) / '04_unit_plan.json'
    if unit_plan_path.exists():
        plan = read_unit_plan(run_id)
        payload['unit_status'] = [
            {
                'id': unit.get('id'),
                'status': unit.get('status', 'unknown'),
                'depends_on': unit.get('depends_on', []),
                'dispatch_ref': unit.get('dispatch_ref'),
                'report_ref': unit.get('report_ref'),
            }
            for unit in plan['units']
        ]
    print(json.dumps(payload, indent=2))


def main() -> None:
    handlers = {
        'create-run': create_run,
        'freeze-contract': freeze_contract,
        'validate-contract': validate_contract,
        'gate-generator': gate_generator,
        'gate-close': gate_close,
        'plan-units': plan_units,
        'collect-unit': collect_unit,
        'dispatch-unit': dispatch_unit,
        'gate-units': gate_units,
        'run-status': run_status,
    }
    try:
        cli_ops.run_cli(handlers)
    except ValueError as exc:
        fail(str(exc))


if __name__ == '__main__':
    main()
