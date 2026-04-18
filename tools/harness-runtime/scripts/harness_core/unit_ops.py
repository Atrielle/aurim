from __future__ import annotations

import re
from typing import Callable


def extract_changed_files(text: str) -> list[str]:
    match = re.search(r'## Changed Files\n(.*?)(?:\n## |\Z)', text, flags=re.S)
    if not match:
        raise ValueError('could not find Changed Files section')
    items = re.findall(r'- (.+)', match.group(1))
    if not items:
        raise ValueError('Changed Files must list at least one file')
    return items


def extract_acceptance_mapping_ids(text: str) -> list[str]:
    match = re.search(r'## Acceptance Mapping\n(.*?)(?:\n## |\Z)', text, flags=re.S)
    if not match:
        raise ValueError('could not find Acceptance Mapping section')
    items = re.findall(r'- \[(?:x|X)\] ([A-Z]{2}-\d{3}) -> .+', match.group(1))
    if not items:
        raise ValueError('Acceptance Mapping must contain checked criterion IDs')
    return items


def ensure_changed_files_within_scope(
    changed_files: list[str],
    touched_paths: list[str],
    in_scope: Callable[[str, list[str]], bool],
) -> None:
    for file in changed_files:
        if not in_scope(file, touched_paths):
            raise ValueError(f'changed file outside touched paths: {file}')


def validate_unit_report_text(
    report_text: str,
    *,
    required_headings: list[str],
    placeholder_snippets: list[str],
    require_headings: Callable[[str, list[str], str], None],
    require_no_placeholders: Callable[[str, str], None],
    acceptance_criteria_ids: list[str],
    touched_paths: list[str],
    in_scope: Callable[[str, list[str]], bool],
) -> tuple[list[str], list[str]]:
    require_headings(report_text, required_headings, 'unit report')
    require_no_placeholders(report_text, 'unit report')

    mapped_ids = extract_acceptance_mapping_ids(report_text)
    missing_ids = [item for item in acceptance_criteria_ids if item not in mapped_ids]
    if missing_ids:
        raise ValueError(f'unit report is missing acceptance mappings for: {", ".join(missing_ids)}')

    changed_files = sorted(file.replace('\\', '/') for file in extract_changed_files(report_text))
    ensure_changed_files_within_scope(changed_files, touched_paths, in_scope)
    return mapped_ids, changed_files
