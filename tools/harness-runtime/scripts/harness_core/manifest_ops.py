from __future__ import annotations


def record_gate_completion(manifest: dict, gate_name: str, status: str) -> dict:
    completed_gates = manifest.get('completed_gates')
    if not isinstance(completed_gates, list):
        completed_gates = []
    if gate_name not in completed_gates:
        completed_gates.append(gate_name)
    manifest['completed_gates'] = completed_gates
    manifest['status'] = status
    return manifest


def ensure_gate_completed(manifest: dict, gate_name: str, *, context: str) -> None:
    completed_gates = manifest.get('completed_gates', [])
    if not isinstance(completed_gates, list) or gate_name not in completed_gates:
        raise ValueError(f'{gate_name} must pass before {context}')


def append_collected_unit(manifest: dict, unit_id: str) -> dict:
    collected = manifest.get('collected_units', [])
    if not isinstance(collected, list):
        collected = []
    if unit_id not in collected:
        collected.append(unit_id)
    manifest['collected_units'] = sorted(collected)
    return manifest
