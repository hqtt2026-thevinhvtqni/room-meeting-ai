"""Deterministic hash of the exact Work execution workspace snapshot."""
from __future__ import annotations

import hashlib
from pathlib import Path

_EXCLUDED = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "node_modules", "dist", "build",
}


class SourceSnapshotError(ValueError):
    pass


def workspace_source_sha256(workspace: str | Path) -> str:
    root = Path(workspace).resolve()
    if not root.exists() or not root.is_dir():
        raise SourceSnapshotError("execution_workspace_missing")
    digest = hashlib.sha256()
    files: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in _EXCLUDED for part in relative.parts):
            continue
        if path.is_symlink():
            raise SourceSnapshotError("source_snapshot_symlink_rejected")
        if path.is_file():
            files.append(path)
        elif not path.is_dir():
            raise SourceSnapshotError("source_snapshot_special_file_rejected")
    for path in sorted(files, key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


__all__ = ["SourceSnapshotError", "workspace_source_sha256"]
