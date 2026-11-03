"""Staged Work 28 contract boundary for the canonical W13 host.

This module is deliberately not wired to the HTTP endpoint yet. It provides
strict request validation and a Work-bound immutable snapshot primitive. Live
activation still requires trusted Core authorization, pinned runtime identity,
and verified process-tree containment/cleanup at the host boundary.
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_WORK_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ALLOWED_OPERATIONS = {"RUN_SCRIPT", "RUN_TESTS"}
_ALLOWED_FIELDS = {
    "work_id", "entry_path", "operation",
    "expected_source_sha256", "timeout_seconds",
}


class Work28ContractError(ValueError):
    """The public Work 28 execution contract is invalid."""


@dataclass(frozen=True)
class Work28RunRequest:
    work_id: str
    entry_path: str
    operation: str
    expected_source_sha256: str
    timeout_seconds: int


@dataclass(frozen=True)
class SourceSnapshot:
    work_id: str
    entry_path: str
    source_sha256: str
    snapshot_ref: str
    snapshot_path: Path


def validate_request(payload: Any) -> Work28RunRequest:
    if not isinstance(payload, dict):
        raise Work28ContractError("request_must_be_object")
    extra = set(payload) - _ALLOWED_FIELDS
    missing = {"work_id", "entry_path", "operation", "expected_source_sha256"} - set(payload)
    if extra:
        raise Work28ContractError("unsupported_fields:" + ",".join(sorted(extra)))
    if missing:
        raise Work28ContractError("missing_fields:" + ",".join(sorted(missing)))

    work_id = payload["work_id"]
    if not isinstance(work_id, str) or not _WORK_ID.fullmatch(work_id):
        raise Work28ContractError("invalid_work_id")

    entry = payload["entry_path"]
    if not isinstance(entry, str) or not entry or any(ord(c) < 32 or ord(c) == 127 for c in entry):
        raise Work28ContractError("invalid_entry_path")
    normalized = entry.replace("\\", "/")
    parts = normalized.split("/")
    if normalized.startswith("/") or ":" in normalized or any(p in ("", ".", "..") for p in parts):
        raise Work28ContractError("entry_path_must_be_safe_work_relative_path")
    if any(p.endswith((" ", ".")) for p in parts):
        raise Work28ContractError("windows_ambiguous_path")
    if any(p.startswith(".") and p in {".git", ".hg", ".svn"} for p in parts):
        raise Work28ContractError("vcs_metadata_path_rejected")

    operation = payload["operation"]
    if not isinstance(operation, str) or operation not in _ALLOWED_OPERATIONS:
        raise Work28ContractError("unsupported_operation")

    expected = payload["expected_source_sha256"]
    if not isinstance(expected, str) or not _SHA256.fullmatch(expected):
        raise Work28ContractError("invalid_expected_source_sha256")

    timeout = payload.get("timeout_seconds", 30)
    if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 300:
        raise Work28ContractError("timeout_out_of_range")

    return Work28RunRequest(work_id, "/".join(parts), operation, expected, timeout)


def create_source_snapshot(
    *,
    request: Work28RunRequest,
    authoritative_work_id: str,
    work_root: str | Path,
    snapshot_root: str | Path,
) -> SourceSnapshot:
    """Copy and hash the exact regular file to a private snapshot directory.

    The caller must obtain authoritative_work_id/work_root from trusted Core,
    not from the public request. This function intentionally does not authorize
    a caller and does not claim OS-level immutable storage.
    """
    if authoritative_work_id != request.work_id:
        raise PermissionError("work_binding_mismatch")

    root = Path(work_root).resolve(strict=True)
    if not root.is_dir():
        raise Work28ContractError("work_root_not_directory")

    candidate = root.joinpath(*request.entry_path.split("/"))
    # Resolve strict and prove containment; reject any symlink in the path.
    current = root
    for part in request.entry_path.split("/"):
        current = current / part
        if current.is_symlink():
            raise Work28ContractError("symlink_component_rejected")
    source = candidate.resolve(strict=True)
    try:
        source.relative_to(root)
    except ValueError as exc:
        raise Work28ContractError("entry_path_escape") from exc
    if not source.is_file():
        raise Work28ContractError("entry_path_not_regular_file")
    mode = source.stat().st_mode
    if not stat.S_ISREG(mode):
        raise Work28ContractError("entry_path_not_regular_file")

    # Read once; hash and snapshot are derived from the same byte sequence.
    data = source.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != request.expected_source_sha256:
        raise Work28ContractError("source_hash_mismatch")

    parent = Path(snapshot_root).resolve()
    parent.mkdir(parents=True, exist_ok=True)
    snapshot_dir = Path(tempfile.mkdtemp(prefix="w28-snapshot-", dir=parent))
    snapshot_path = snapshot_dir / Path(request.entry_path).name
    try:
        with snapshot_path.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        # Read-only permissions are a defense-in-depth measure, not a claim
        # of kernel-enforced immutability against the same OS account.
        snapshot_path.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        if hashlib.sha256(snapshot_path.read_bytes()).hexdigest() != digest:
            raise Work28ContractError("snapshot_hash_verification_failed")
    except Exception:
        try:
            snapshot_path.chmod(stat.S_IWUSR | stat.S_IRUSR)
            snapshot_path.unlink(missing_ok=True)
            shutil.rmtree(snapshot_dir, ignore_errors=True)
        finally:
            raise

    return SourceSnapshot(
        work_id=request.work_id,
        entry_path=request.entry_path,
        source_sha256=digest,
        snapshot_ref=f"sha256:{digest}:{snapshot_dir.name}/{snapshot_path.name}",
        snapshot_path=snapshot_path,
    )


__all__ = [
    "SourceSnapshot",
    "Work28ContractError",
    "Work28RunRequest",
    "create_source_snapshot",
    "validate_request",
]
