"""Work 101 pure sync-policy primitives.

This module is deliberately offline: no filesystem writes, GitHub API, credentials,
Core calls, or execution. Runtime adapters must enforce realpath/symlink containment
and Core authorization before any transfer.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import json
import re
import unicodedata
from typing import Iterable


class PolicyError(ValueError):
    """Input violates a fail-closed sync policy."""


class ChangeState(str, Enum):
    NO_CHANGE = "NO_CHANGE"
    SOURCE_ONLY = "SOURCE_ONLY"
    DESTINATION_ONLY = "DESTINATION_ONLY"
    NON_OVERLAPPING = "NON_OVERLAPPING"
    CONFLICT_PENDING = "CONFLICT_PENDING"
    STALE_BASE = "STALE_BASE"


@dataclass(frozen=True)
class Snapshot:
    revision: str
    files: dict[str, str]  # canonical relative path -> SHA-256 hex digest


@dataclass(frozen=True)
class SyncDecision:
    state: ChangeState
    source_changed: tuple[str, ...] = ()
    destination_changed: tuple[str, ...] = ()
    conflict_paths: tuple[str, ...] = ()
    reason: str = ""


@dataclass(frozen=True)
class ApprovalBinding:
    operation_id: str
    diff_digest: str
    destination_branch: str
    base_revision: str


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def digest_payload(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def canonical_relative_path(path: str) -> str:
    """Validate a relative path string; adapters must additionally verify realpath containment."""
    if not isinstance(path, str) or not path:
        raise PolicyError("PATH_EMPTY_OR_INVALID")
    if path != unicodedata.normalize("NFC", path):
        raise PolicyError("PATH_UNICODE_NOT_NFC")
    if any(unicodedata.category(ch) in {"Cc", "Cf", "Cs", "Co", "Cn"} for ch in path):
        raise PolicyError("PATH_CONTROL_OR_FORMAT_CHARACTER")
    if path.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", path):
        raise PolicyError("PATH_ABSOLUTE_OR_DRIVE")
    if "\\" in path:
        raise PolicyError("PATH_BACKSLASH_NOT_CANONICAL")
    parts = path.split("/")
    if any(p in {"", ".", ".."} for p in parts):
        raise PolicyError("PATH_TRAVERSAL_OR_AMBIGUOUS_COMPONENT")
    if any(p.startswith("-") for p in parts):
        raise PolicyError("PATH_OPTION_LIKE_COMPONENT")
    for part in parts:
        if part.endswith((".", " ")):
            raise PolicyError("PATH_WINDOWS_TRAILING_DOT_SPACE")
        if ":" in part:
            raise PolicyError("PATH_ALTERNATE_DATA_STREAM")
        stem = part.split(".", 1)[0].upper()
        if stem in {"CON", "PRN", "AUX", "NUL"} or re.fullmatch(r"(COM|LPT)[1-9¹²³]", stem):
            raise PolicyError("PATH_WINDOWS_RESERVED_NAME")
    normalized = "/".join(parts)
    if is_excluded_path(normalized):
        raise PolicyError("PATH_POLICY_EXCLUDED")
    return normalized


def is_excluded_path(path: str) -> bool:
    """Conservative denylist for credentials, runtime state, generated artifacts and logs."""
    p = path.replace("\\\\", "/").lower()
    parts = p.split("/")
    name = parts[-1]
    if name == ".env" or name.startswith(".env.") or name in {
        "id_rsa", "id_ed25519", "credentials.json", "secrets.json",
        "app_workspace.db", "sqlite.db", "runtime.db",
    }:
        return True
    if name.endswith((".db", ".sqlite", ".sqlite3", ".log", ".zip", ".7z", ".tar", ".gz", ".pyc")):
        return True
    if any(part in {"__pycache__", "node_modules", ".git", "dist", "build", "evidence", "06_evidence"} for part in parts):
        return True
    return False


def validate_snapshot(snapshot: Snapshot) -> None:
    if not snapshot.revision or not isinstance(snapshot.revision, str):
        raise PolicyError("REVISION_REQUIRED")
    for path, digest in snapshot.files.items():
        if canonical_relative_path(path) != path:
            raise PolicyError("PATH_NOT_CANONICAL")
        if not re.fullmatch(r"[0-9a-f]{64}", digest or ""):
            raise PolicyError("CONTENT_DIGEST_INVALID")


def classify_sync(base: Snapshot, source: Snapshot, destination: Snapshot) -> SyncDecision:
    """Compare two sides against the same baseline. Never applies writes."""
    for snap in (base, source, destination):
        validate_snapshot(snap)
    if not base.revision:
        return SyncDecision(ChangeState.STALE_BASE, reason="BASE_REVISION_MISSING")
    paths = set(base.files) | set(source.files) | set(destination.files)
    src_changed = {p for p in paths if source.files.get(p) != base.files.get(p)}
    dst_changed = {p for p in paths if destination.files.get(p) != base.files.get(p)}
    if not src_changed and not dst_changed:
        return SyncDecision(ChangeState.NO_CHANGE)
    overlap = src_changed & dst_changed
    # Same-path changes are only conflict-free when both sides independently reached
    # exactly the same content digest (including both deletions).
    conflicts = {p for p in overlap if source.files.get(p) != destination.files.get(p)}
    if conflicts:
        return SyncDecision(
            ChangeState.CONFLICT_PENDING,
            tuple(sorted(src_changed)),
            tuple(sorted(dst_changed)),
            tuple(sorted(conflicts)),
            "CONCURRENT_EDIT_REQUIRES_EXPLICIT_RESOLUTION",
        )
    if src_changed and dst_changed:
        return SyncDecision(
            ChangeState.NON_OVERLAPPING,
            tuple(sorted(src_changed)),
            tuple(sorted(dst_changed)),
            (),
            "CHANGES_ARE_NON_OVERLAPPING_OR_IDENTICAL",
        )
    if src_changed:
        return SyncDecision(ChangeState.SOURCE_ONLY, tuple(sorted(src_changed)), (), ())
    return SyncDecision(ChangeState.DESTINATION_ONLY, (), tuple(sorted(dst_changed)), ())


def bind_approval(binding: ApprovalBinding, requested: ApprovalBinding) -> None:
    """Exact equality check: any operation/diff/branch/base change invalidates approval."""
    if binding != requested:
        raise PolicyError("APPROVAL_BINDING_MISMATCH")


def idempotency_fingerprint(operation_id: str, payload: object) -> str:
    if not operation_id or not operation_id.strip():
        raise PolicyError("OPERATION_ID_REQUIRED")
    return digest_payload({"operation_id": operation_id, "payload": payload})


def enforce_idempotency(existing_fingerprint: str | None, operation_id: str, payload: object) -> str:
    current = idempotency_fingerprint(operation_id, payload)
    if existing_fingerprint is not None and existing_fingerprint != current:
        raise PolicyError("OPERATION_ID_REPLAY_WITH_DIFFERENT_PAYLOAD")
    return current
