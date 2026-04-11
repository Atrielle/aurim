from __future__ import annotations

import json
import shlex
import subprocess
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RUNNER = ROOT / 'tools' / 'harness-runtime' / 'scripts' / 'runner.py'
REGRESSION = ROOT / 'tools' / 'harness-runtime' / 'scripts' / 'unit_gate_regression.py'
RUNS = ROOT / 'tools' / 'harness-runtime' / 'artifacts' / 'runs'


@dataclass(frozen=True)
class CommandSpec:
    name: str
    requires_run_id: bool = False
    requires_unit_id: bool = False
    requires_report: bool = False


RUNNER_COMMANDS: dict[str, CommandSpec] = {
    'create-run': CommandSpec('create-run', requires_run_id=True),
    'freeze-contract': CommandSpec('freeze-contract', requires_run_id=True),
    'validate-contract': CommandSpec('validate-contract', requires_run_id=True),
    'gate-generator': CommandSpec('gate-generator', requires_run_id=True),
    'gate-close': CommandSpec('gate-close', requires_run_id=True),
    'plan-units': CommandSpec('plan-units', requires_run_id=True),
    'dispatch-unit': CommandSpec('dispatch-unit', requires_run_id=True, requires_unit_id=True),
    'collect-unit': CommandSpec('collect-unit', requires_run_id=True, requires_unit_id=True, requires_report=True),
    'gate-units': CommandSpec('gate-units', requires_run_id=True),
    'run-status': CommandSpec('run-status', requires_run_id=True),
}


def known_runs() -> list[str]:
    if not RUNS.exists():
        return []
    return sorted(item.name for item in RUNS.iterdir() if item.is_dir())


def _run_subprocess(command: list[str]) -> dict:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    output = (result.stdout + '\n' + result.stderr).strip()
    return {
        'exit_code': result.returncode,
        'command_line': shlex.join(command),
        'output': output,
    }


def run_regression() -> dict:
    return _run_subprocess(['python', str(REGRESSION)])


def run_runner_command(command_name: str, run_id: str, unit_id: str, report_path: str) -> dict:
    spec = RUNNER_COMMANDS.get(command_name)
    if spec is None:
        raise ValueError(f'unsupported command: {command_name}')

    args = [spec.name]
    if spec.requires_run_id:
        if not run_id:
            raise ValueError('run_id is required for this command')
        args.extend(['--run-id', run_id])

    if spec.requires_unit_id:
        if not unit_id:
            raise ValueError('unit_id is required for this command')
        args.extend(['--unit-id', unit_id])

    if spec.requires_report:
        if not report_path:
            raise ValueError('report path is required for collect-unit')
        args.extend(['--report', report_path])

    return _run_subprocess(['python', str(RUNNER), *args])


SEQUENCE_PRESETS: dict[str, list[str]] = {
    'bootstrap': ['create-run', 'run-status'],
    'validate_plan': ['validate-contract', 'plan-units', 'run-status'],
    'unit_gate_ready': ['gate-units', 'run-status'],
}


def sequence_names() -> list[str]:
    return sorted(SEQUENCE_PRESETS.keys())


def resolve_sequence(preset: str | None, sequence: list[str] | None = None) -> list[str]:
    if sequence:
        return sequence
    chosen = (preset or 'bootstrap').strip()
    resolved = SEQUENCE_PRESETS.get(chosen)
    if resolved is None:
        raise ValueError(f'unknown sequence preset: {chosen}')
    return resolved


def update_manifest_sequence_refs(run_dir: Path, report_ref: str) -> None:
    manifest_path = run_dir / 'manifest.json'
    if not manifest_path.exists():
        return
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    reports = manifest.get('sequence_reports', [])
    if not isinstance(reports, list):
        reports = []
    if report_ref not in reports:
        reports.append(report_ref)
    manifest['sequence_reports'] = reports
    manifest['last_sequence_report_ref'] = report_ref
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')


def write_sequence_report(run_id: str, report: dict) -> str | None:
    run_dir = RUNS / run_id
    if not run_dir.exists() or not run_dir.is_dir():
        return None

    reports_dir = run_dir / '06_sequence_reports'
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    target = reports_dir / f'{timestamp}.json'
    target.write_text(json.dumps(report, indent=2), encoding='utf-8')
    report_ref = target.relative_to(ROOT).as_posix()
    update_manifest_sequence_refs(run_dir, report_ref)
    return report_ref


def read_run_status(run_id: str) -> dict:
    if not run_id:
        raise ValueError('run_id is required')
    result = run_runner_command('run-status', run_id=run_id, unit_id='', report_path='')
    if result.get('exit_code') != 0:
        raise ValueError(result.get('output') or 'failed to read run status')
    try:
        return json.loads(result.get('output', '{}'))
    except json.JSONDecodeError as exc:
        raise ValueError('run-status output is not valid json') from exc


def read_sequence_report(report_ref: str) -> dict:
    if not report_ref:
        raise ValueError('report_ref is required')
    target = (ROOT / report_ref).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError('report_ref escapes workspace') from exc
    if not target.exists() or not target.is_file():
        raise ValueError(f'report file not found: {report_ref}')
    runs_root = RUNS.resolve()
    try:
        target.relative_to(runs_root)
    except ValueError as exc:
        raise ValueError('report_ref must be under harness runs') from exc
    return json.loads(target.read_text(encoding='utf-8'))


def run_sequence(run_id: str, preset: str | None = None, sequence: list[str] | None = None) -> dict:
    if not run_id:
        raise ValueError('run_id is required for sequence execution')

    selected = resolve_sequence(preset=preset, sequence=sequence)
    steps: list[dict] = []
    for command_name in selected:
        result = run_runner_command(command_name, run_id=run_id, unit_id='', report_path='')
        steps.append({
            'command': command_name,
            **result,
        })
        if result['exit_code'] != 0:
            payload = {
                'run_id': run_id,
                'sequence': selected,
                'steps': steps,
                'success': False,
            }
            payload['sequence_report_ref'] = write_sequence_report(run_id, payload)
            return payload

    payload = {
        'run_id': run_id,
        'sequence': selected,
        'steps': steps,
        'success': True,
    }
    payload['sequence_report_ref'] = write_sequence_report(run_id, payload)
    return payload
