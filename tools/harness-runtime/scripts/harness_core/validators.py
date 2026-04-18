from __future__ import annotations

import re


def require_headings(text: str, headings: list[str], name: str) -> list[str]:
    return [heading for heading in headings if heading not in text]


def require_no_placeholders(text: str, snippets: list[str]) -> list[str]:
    return [item for item in snippets if item in text]


def extract_checked_items(section_text: str) -> list[str]:
    return re.findall(r'- \[x\] (.+)', section_text, flags=re.IGNORECASE)


def extract_paths(contract_text: str) -> list[str]:
    match = re.search(r'## Touched Paths\n(.*?)(?:\n## |\Z)', contract_text, flags=re.S)
    if not match:
        return []
    return extract_checked_items(match.group(1))
