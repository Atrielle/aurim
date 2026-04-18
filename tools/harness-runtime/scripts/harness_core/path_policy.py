from __future__ import annotations

from pathlib import Path


def validate_paths(paths: list[str], root: Path) -> list[str]:
    errors: list[str] = []
    allowed_roots = ['apps/', 'tools/', 'packages/', 'docs/']
    for item in paths:
        normalized = item.replace('\\', '/')
        if not any(normalized.startswith(prefix) for prefix in allowed_roots):
            errors.append(f'touched path outside allowed roots: {item}')
            continue
        if normalized == 'tools/harness-runtime/.runner-state' or normalized.startswith('tools/harness-runtime/.runner-state/'):
            errors.append(f'touched path cannot include runner-owned state: {item}')
            continue
        resolved = (root / normalized).resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            errors.append(f'touched path escapes workspace: {item}')
    return errors


def is_within_touched_paths(path: str, touched_paths: list[str]) -> bool:
    normalized = path.replace('\\', '/')
    return any(
        normalized == touched.rstrip('/') or normalized.startswith(touched.rstrip('/') + '/')
        for touched in (item.replace('\\', '/') for item in touched_paths)
    )


def iter_touched_files(root: Path, touched_paths: list[str]) -> list[str]:
    files: set[str] = set()
    for item in touched_paths:
        resolved = root / item
        if resolved.is_file():
            files.add(resolved.relative_to(root).as_posix())
        elif resolved.is_dir():
            for child in resolved.rglob('*'):
                if child.is_file():
                    files.add(child.relative_to(root).as_posix())
    return sorted(files)
