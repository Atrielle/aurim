from __future__ import annotations

from typing import Callable


def validate_sprint_contract(
    contract_text: str,
    *,
    required_headings: list[str],
    require_headings: Callable[[str, list[str], str], None],
    require_no_placeholders: Callable[[str, str], None],
    extract_paths: Callable[[str], list[str]],
    expected_touched_paths: list[str],
) -> None:
    require_headings(contract_text, required_headings, 'sprint contract')
    require_no_placeholders(contract_text, 'sprint contract')
    touched_paths = extract_paths(contract_text)
    if touched_paths != expected_touched_paths:
        raise ValueError('sprint contract Touched Paths do not match 01_run_contract.json')


def topological_work_units(work_units: list[dict]) -> list[dict]:
    by_id = {unit['id']: unit for unit in work_units}
    dependency_counts = {unit['id']: len(unit['agent_budget']['depends_on']) for unit in work_units}
    reverse_edges: dict[str, list[str]] = {unit['id']: [] for unit in work_units}
    for unit in work_units:
        for dependency in unit['agent_budget']['depends_on']:
            reverse_edges[dependency].append(unit['id'])

    ready = [unit_id for unit_id, count in dependency_counts.items() if count == 0]
    ordered: list[str] = []
    while ready:
        current = sorted(ready)[0]
        ready.remove(current)
        ordered.append(current)
        for child in reverse_edges[current]:
            dependency_counts[child] -= 1
            if dependency_counts[child] == 0:
                ready.append(child)

    if len(ordered) != len(work_units):
        raise ValueError('work unit dependency graph contains a cycle')
    return [by_id[unit_id] for unit_id in ordered]
