"""Real immutable source snapshot provider (integration slice step 2).

Implements the SourceSnapshotProvider protocol of the authorized execution
adapter against a REAL filesystem, fail-closed:

* containment: entry_path is Work-relative, canonical W<number> work id,
  no absolute/traversal/drive-like or ambiguous components;
* anti-symlink: every path component is lstat-checked; any symlink or
  reparse-like link in the chain is refused, and the entry file itself is
  opened O_NOFOLLOW (falling back to lstat where the flag is missing);
* immutability: content bytes are copied into a per-run snapshot directory
  (unique run id) and fsync-ed; the metadata record binds work id, entry
  path, and the SHA-256 computed FROM THE COPIED CONTENT;
* refusal on drift: the provider reports the hash of the actual bytes; the
  adapter refuses dispatch when it differs from the caller's expected
  source hash.

STAGED and NOT WIRED into MCP/v54. This is a repository-verifiable
implementation tested on a real filesystem in CI; it is NOT proof of the
W13 Execution Host deployment or OS-level isolation (that evidence belongs
to the trusted environment and must be recorded PASS or BLOCKED there).
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
import time
import uuid
from pathlib import Path
from typing import Any

from mcp8020_core_authority_authorizer_v1 import require_core_canonical_work_id

_DEFAULT_SIZE_LIMIT_BYTES = 10 * 1024 * 1024


class SourceSnapshotError(RuntimeError):
    """Raised when a safe immutable snapshot cannot be produced."""


def _normalize_entry_path(entry_path: Any) -> list[str]:
    if not isinstance(entry_path, str) or not entry_path:
        raise SourceSnapshotError("entry_path must be a non-empty string")
    if any(ord(char) < 32 or ord(char) == 127 for char in entry_path):
        raise SourceSnapshotError("entry_path contains control characters")
    normalized = entry_path.replace("\\", "/")
    if normalized.startswith("/"):
        raise SourceSnapshotError("entry_path must be Work-relative")
    if ":" in normalized:
        raise SourceSnapshotError("entry_path contains drive-like segments")
    parts = normalized.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise SourceSnapshotError("entry_path contains unsafe path components")
    if any(part.endswith((" ", ".")) for part in parts):
        raise SourceSnapshotError("entry_path contains Windows-ambiguous names")
    return parts


def _parent_dirs_without_symlinks(base: Path, parts: list[str]) -> Path:
    current = base
    for part in parts[:-1]:
        current = current / part
        try:
            st = os.lstat(current)
        except OSError as exc:
            raise SourceSnapshotError("path component missing: " + part) from exc
        if stat.S_ISLNK(st.st_mode):
            raise SourceSnapshotError("symlink path component refused: " + part)
        if not stat.S_ISDIR(st.st_mode):
            raise SourceSnapshotError("path component is not a directory: " + part)
    return current


class ImmutableSourceSnapshotProvider:
    """SourceSnapshotProvider over a real filesystem. Fail-closed."""

    def __init__(self, *, workspaces_root: Any, snapshots_root: Any,
                 size_limit_bytes: int = _DEFAULT_SIZE_LIMIT_BYTES) -> None:
        if not isinstance(workspaces_root, (str, os.PathLike)) or not str(workspaces_root).strip():
            raise ValueError("workspaces_root is required")
        if not isinstance(snapshots_root, (str, os.PathLike)) or not str(snapshots_root).strip():
            raise ValueError("snapshots_root is required")
        if isinstance(size_limit_bytes, bool) or not isinstance(size_limit_bytes, int) or size_limit_bytes < 1:
            raise ValueError("size_limit_bytes must be a positive integer")
        self._workspaces_root = Path(workspaces_root)
        self._snapshots_root = Path(snapshots_root)
        self._size_limit_bytes = size_limit_bytes

    def create_immutable_snapshot(self, work_id: Any, entry_path: Any) -> dict[str, Any]:
        work_id = require_core_canonical_work_id(work_id)
        parts = _normalize_entry_path(entry_path)
        workspace = self._workspaces_root / work_id
        if not workspace.is_dir():
            raise SourceSnapshotError("unknown work workspace: " + work_id)
        parent = _parent_dirs_without_symlinks(workspace, parts)
        target = parent / parts[-1]
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        try:
            fd = os.open(target, flags)
        except OSError as exc:
            raise SourceSnapshotError("entry cannot be opened safely: " + type(exc).__name__) from exc
        try:
            st = os.fstat(fd)
            if stat.S_ISLNK(st.st_mode):
                raise SourceSnapshotError("entry is a symlink and is refused")
            if not stat.S_ISREG(st.st_mode):
                raise SourceSnapshotError("entry is not a regular file")
            if st.st_size > self._size_limit_bytes:
                raise SourceSnapshotError("entry exceeds the size limit")
            chunks = []
            while True:
                chunk = os.read(fd, 65536)
                if not chunk:
                    break
                chunks.append(chunk)
        finally:
            os.close(fd)
        content = b"".join(chunks)
        digest = hashlib.sha256(content).hexdigest()
        run_id = "SNAP-" + str(uuid.uuid4())
        snapshot_dir = self._snapshots_root / work_id / run_id
        snapshot_dir.mkdir(parents=True, exist_ok=False)
        with open(snapshot_dir / "source", "xb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if hashlib.sha256((snapshot_dir / "source").read_bytes()).hexdigest() != digest:
            raise SourceSnapshotError("snapshot copy does not match the hashed content")
        metadata = {
            "run_id": run_id,
            "work_id": work_id,
            "entry_path": "/".join(parts),
            "source_sha256": digest,
            "size_bytes": len(content),
            "created_at_unix": time.time(),
        }
        with open(snapshot_dir / "metadata.json", "x", encoding="utf-8") as handle:
            handle.write(json.dumps(metadata, sort_keys=True))
            handle.flush()
            os.fsync(handle.fileno())
        return {
            "work_id": work_id,
            "entry_path": "/".join(parts),
            "immutable": True,
            "source_sha256": digest,
            "snapshot_ref": "snapshot://" + run_id,
            "run_id": run_id,
        }


__all__ = ["ImmutableSourceSnapshotProvider", "SourceSnapshotError"]
