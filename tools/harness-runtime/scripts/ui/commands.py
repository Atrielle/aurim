from __future__ import annotations

import shlex
import subprocess
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
