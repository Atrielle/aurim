from __future__ import annotations

import re
from typing import Callable


def validate_reported_vs_measured_changes(reported: list[str], measured: list[str]) -> None:
    if reported == measured:
        return
    missing = sorted(set(measured) - set(reported))
    extra = sorted(set(reported) - set(measured))
    raise ValueError(
        'generator report changed files do not match measured changes'
        + (f'; missing: {", ".join(missing)}' if missing else '')
        + (f'; extra: {", ".join(extra)}' if extra else '')
    )


def ensure_measured_files_visible_in_git(measured: list[str], git_dirty: set[str]) -> None:
    invisible = sorted(path for path in measured if path not in git_dirty)
    if invisible:
        raise ValueError(f'measured changed files are not visible in git status: {", ".join(invisible)}')


def validate_evaluator_pass(evaluator_text: str, extract_checked_items: Callable[[str], list[str]]) -> None:
    verdict_match = re.search(r'## Overall Verdict\n(.*?)(?:\n## |\Z)', evaluator_text, flags=re.S)
    if not verdict_match or 'PASS' not in verdict_match.group(1):
        raise ValueError('evaluator report is not PASS')

    compliance_section = re.search(r'## Contract Compliance\n(.*?)(?:\n## |\Z)', evaluator_text, flags=re.S)
    if not compliance_section:
        raise ValueError('missing Contract Compliance section')

    checked = extract_checked_items(compliance_section.group(1))
    if len(checked) < 4:
        raise ValueError('not all contract compliance checks are marked complete')
