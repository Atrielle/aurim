from __future__ import annotations

from typing import Callable


def validate_freeze_proof(
    proof: dict,
    *,
    run_id: str,
    expected_contracts: set[str],
    hash_for_path: Callable[[str], str],
    require_prebaseline_state: bool,
    current_run_artifact_snapshot: dict[str, str],
    current_manifest_hash: str,
) -> tuple[dict[str, str], str]:
    if proof.get('run_id') != run_id:
        raise ValueError('freeze proof run_id mismatch')
    if proof.get('captured_via') != 'freeze-contract':
        raise ValueError('freeze proof captured_via mismatch')

    frozen_snapshot = proof.get('run_artifact_snapshot')
    if not isinstance(frozen_snapshot, dict):
        raise ValueError('freeze proof run_artifact_snapshot is invalid')

    manifest_hash = proof.get('manifest_hash')
    if not isinstance(manifest_hash, str) or not manifest_hash:
        raise ValueError('freeze proof manifest_hash is invalid')

    contract_hashes = proof.get('contract_hashes')
    if not isinstance(contract_hashes, dict):
        raise ValueError('freeze proof contract_hashes is invalid')

    if set(contract_hashes) != expected_contracts:
        raise ValueError('freeze proof contract_hashes do not match authored contract files')

    for relative_path, frozen_hash in contract_hashes.items():
        if hash_for_path(relative_path) != frozen_hash:
            raise ValueError(f'freeze proof no longer matches authored contract file: {relative_path}')

    if require_prebaseline_state:
        if current_run_artifact_snapshot != frozen_snapshot:
            raise ValueError('run artifacts changed after freeze-contract and before baseline capture')
        if current_manifest_hash != manifest_hash:
            raise ValueError('manifest was edited after freeze-contract')

    return frozen_snapshot, manifest_hash


def validate_baseline_proof(proof: dict, *, run_id: str) -> dict[str, str]:
    if proof.get('run_id') != run_id:
        raise ValueError('baseline proof run_id mismatch')
    if proof.get('captured_via') != 'gate-generator':
        raise ValueError('baseline proof captured_via mismatch')
    baseline_snapshot = proof.get('baseline_snapshot')
    if not isinstance(baseline_snapshot, dict):
        raise ValueError('baseline proof baseline_snapshot is invalid')
    return baseline_snapshot


def split_dirty_files(
    *,
    dirty_files: set[str],
    run_manifest_path: str,
    frozen_manifest_hash: str,
    frozen_snapshot: dict[str, str],
    hash_for_path: Callable[[str], str],
) -> tuple[set[str], set[str]]:
    exemptable_files: set[str] = set()
    for path in sorted(dirty_files):
        if path == run_manifest_path:
            if hash_for_path(path) == frozen_manifest_hash:
                exemptable_files.add(path)
            continue
        if path in frozen_snapshot and hash_for_path(path) == frozen_snapshot[path]:
            exemptable_files.add(path)
    unresolved = set(dirty_files) - exemptable_files
    return unresolved, exemptable_files


def actual_changed_files(
    baseline_snapshot: dict[str, str],
    current_snapshot: dict[str, str],
    ignored_paths: set[str],
) -> list[str]:
    changed = {
        path
        for path in sorted(set(baseline_snapshot) | set(current_snapshot))
        if baseline_snapshot.get(path) != current_snapshot.get(path)
    }
    changed -= ignored_paths
    return sorted(changed)
