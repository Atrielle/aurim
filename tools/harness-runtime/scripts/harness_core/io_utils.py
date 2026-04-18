from __future__ import annotations

import hashlib
import json
from pathlib import Path


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f'missing file: {path}')
    return path.read_text(encoding='utf-8')


def read_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f'missing file: {path}')
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding='utf-8')


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
