from __future__ import annotations

import argparse
import inspect
from typing import Callable


COMMAND_ARGUMENTS: dict[str, list[str]] = {
    'create-run': ['run_id'],
    'freeze-contract': ['run_id'],
    'validate-contract': ['run_id'],
    'gate-generator': ['run_id'],
    'gate-close': ['run_id'],
    'plan-units': ['run_id'],
    'collect-unit': ['run_id', 'unit_id', 'report'],
    'dispatch-unit': ['run_id', 'unit_id'],
    'gate-units': ['run_id'],
    'run-status': ['run_id'],
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Aurim harness runner')
    sub = parser.add_subparsers(dest='command', required=True)
    for command_name, args in COMMAND_ARGUMENTS.items():
        cmd_parser = sub.add_parser(command_name)
        for argument in args:
            cmd_parser.add_argument(f'--{argument.replace("_", "-")}', dest=argument, required=True)
    return parser


def dispatch_command(args: argparse.Namespace, handlers: dict[str, Callable[..., None]]) -> None:
    command = args.command
    handler = handlers.get(command)
    if handler is None:
        raise ValueError(f'unknown command: {command}')

    required_args = COMMAND_ARGUMENTS.get(command, [])
    params = [getattr(args, arg) for arg in required_args]
    handler(*params)


def validate_handlers(handlers: dict[str, Callable[..., None]]) -> None:
    missing = [command for command in COMMAND_ARGUMENTS if command not in handlers]
    if missing:
        raise ValueError(f'missing command handlers: {", ".join(sorted(missing))}')

    for command, handler in handlers.items():
        if command not in COMMAND_ARGUMENTS:
            raise ValueError(f'unsupported handler command: {command}')
        expected = len(COMMAND_ARGUMENTS[command])
        positional = [
            parameter
            for parameter in inspect.signature(handler).parameters.values()
            if parameter.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        ]
        if len(positional) != expected:
            raise ValueError(
                f'handler signature mismatch for {command}: expected {expected} positional args, got {len(positional)}'
            )


def run_cli(handlers: dict[str, Callable[..., None]]) -> None:
    validate_handlers(handlers)
    parser = build_parser()
    args = parser.parse_args()
    dispatch_command(args, handlers)
