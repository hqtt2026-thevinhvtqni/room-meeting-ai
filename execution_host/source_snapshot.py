from __future__ import annotations

import hashlib
from pathlib import Path


_EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
}


def workspace_source_sha256(workspace: str | Path) -> str:
    """Hash an immutable source workspace using sorted relative paths and bytes.

    Symlinks are rejected rather than followed so a workspace cannot smuggle
    files from outside its canonical root into the source identity.
    """
    root = Path(workspace).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("execution_workspace_not_directory")

    digest = hashlib.sha256()
    files: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in _EXCLUDED_PARTS for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError("execution_workspace_symlink_rejected")
        if path.is_file():
            files.append(path)

    for path in sorted(files, key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()
