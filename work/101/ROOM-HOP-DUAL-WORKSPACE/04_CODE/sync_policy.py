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
    # Optional common-base marker captured when the snapshot was collected.
    base_revision: str | None = None


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
    p = path.replace("\\", "/").lower()
    parts = p.split("/")
    name = parts[-1]
    if name == ".env" or name.startswith(".env.") or name in {
        "id_rsa", "id_ed25519", "credentials.json", "secrets.json",
        "app_workspace.db", "sqlite.db", "runtime.db",
    }:
        return True
    if name.endswith((".db", ".sqlite", ".sqlite3", ".log", ".zip", ".7z", ".tar", ".gz", ".pyc")):
        return True
    if any(part in {"__pycache__", "node_modules", ".git", "dist", "build"} for part in parts):
        return True
    return False


def validate_snapshot(snapshot: Snapshot) -> None:
    if not isinstance(snapshot.revision, str) or not snapshot.revision.strip():
        raise PolicyError("REVISION_REQUIRED")
    if snapshot.base_revision is not None and (
        not isinstance(snapshot.base_revision, str) or not snapshot.base_revision.strip()
    ):
        raise PolicyError("BASE_REVISION_INVALID")
    if not isinstance(snapshot.files, dict):
        raise PolicyError("SNAPSHOT_FILES_INVALID")
    seen_casefolded: dict[str, str] = {}
    for path, digest in snapshot.files.items():
        if canonical_relative_path(path) != path:
            raise PolicyError("PATH_NOT_CANONICAL")
        collision_key = unicodedata.normalize("NFC", path).casefold()
        previous = seen_casefolded.get(collision_key)
        if previous is not None and previous != path:
            raise PolicyError("PATH_CASE_COLLISION")
        seen_casefolded[collision_key] = path
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise PolicyError("CONTENT_DIGEST_INVALID")


def classify_sync(base: Snapshot, source: Snapshot, destination: Snapshot) -> SyncDecision:
    """Compare two sides against the same baseline. Never applies writes."""
    for snap in (base, source, destination):
        validate_snapshot(snap)
    # If either side reports the baseline it was collected against, fail closed
    # when it does not match the baseline selected for this comparison.
    if source.base_revision is not None and source.base_revision != base.revision:
        return SyncDecision(ChangeState.STALE_BASE, reason="SOURCE_BASE_REVISION_MISMATCH")
    if destination.base_revision is not None and destination.base_revision != base.revision:
        return SyncDecision(ChangeState.STALE_BASE, reason="DESTINATION_BASE_REVISION_MISMATCH")
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



@dataclass(frozen=True)
class SyncPlan:
    """Read-only synchronization plan; it never performs transfer or writes."""
    operation_id: str
    work_id: str
    destination_branch: str
    base_revision: str
    source_revision: str
    destination_revision: str
    state: ChangeState
    source_to_destination: tuple[str, ...]
    destination_to_source: tuple[str, ...]
    conflict_paths: tuple[str, ...]
    mode: str
    diff_digest: str
    reason: str = ""


def build_sync_plan(
    *,
    operation_id: str,
    work_id: str,
    destination_branch: str,
    base_revision: str,
    base: Snapshot,
    source: Snapshot,
    destination: Snapshot,
    permitted_path_roots: Iterable[str],
) -> SyncPlan:
    """Build a deterministic DRY_RUN plan. This function performs no I/O."""
    if not isinstance(operation_id, str) or not operation_id.strip():
        raise PolicyError("OPERATION_ID_REQUIRED")
    if not isinstance(work_id, str) or not work_id.strip():
        raise PolicyError("WORK_ID_REQUIRED")
    if not isinstance(destination_branch, str) or not destination_branch.strip():
        raise PolicyError("DESTINATION_BRANCH_REQUIRED")
    if destination_branch.strip().casefold() in {"main", "master"}:
        raise PolicyError("PROTECTED_BRANCH_NOT_ALLOWED")
    if not isinstance(base_revision, str) or not base_revision.strip():
        raise PolicyError("BASE_REVISION_REQUIRED")
    if base.revision != base_revision:
        raise PolicyError("PLAN_BASE_REVISION_MISMATCH")

    roots = tuple(canonical_relative_path(r.rstrip("/")) for r in permitted_path_roots)
    if not roots:
        raise PolicyError("PATH_ALLOWLIST_REQUIRED")

    for snap in (base, source, destination):
        validate_snapshot(snap)
        for path in snap.files:
            if not any(path == root or path.startswith(root + "/") for root in roots):
                raise PolicyError("PATH_OUTSIDE_ALLOWLIST")

    decision = classify_sync(base, source, destination)
    source_to_destination: tuple[str, ...] = ()
    destination_to_source: tuple[str, ...] = ()
    if decision.state not in {ChangeState.CONFLICT_PENDING, ChangeState.STALE_BASE}:
        paths = set(base.files) | set(source.files) | set(destination.files)
        to_destination = []
        to_source = []
        for path in sorted(paths):
            base_digest = base.files.get(path)
            source_digest = source.files.get(path)
            destination_digest = destination.files.get(path)
            source_changed = source_digest != base_digest
            destination_changed = destination_digest != base_digest
            if source_digest == destination_digest:
                continue
            if source_changed and not destination_changed:
                to_destination.append(path)
            elif destination_changed and not source_changed:
                to_source.append(path)
            # A divergent same-path edit is already CONFLICT_PENDING and blocks
            # the entire plan. This branch is defensive and must never auto-pick.
        source_to_destination = tuple(to_destination)
        destination_to_source = tuple(to_source)

    payload = {
        "operation_id": operation_id,
        "work_id": work_id,
        "destination_branch": destination_branch,
        "base_revision": base_revision,
        "source_revision": source.revision,
        "destination_revision": destination.revision,
        "state": decision.state.value,
        "source_to_destination": source_to_destination,
        "destination_to_source": destination_to_source,
        "conflict_paths": decision.conflict_paths,
        "mode": "DRY_RUN",
    }
    return SyncPlan(
        operation_id=operation_id,
        work_id=work_id,
        destination_branch=destination_branch,
        base_revision=base_revision,
        source_revision=source.revision,
        destination_revision=destination.revision,
        state=decision.state,
        source_to_destination=source_to_destination,
        destination_to_source=destination_to_source,
        conflict_paths=decision.conflict_paths,
        mode="DRY_RUN",
        diff_digest=digest_payload(payload),
        reason=decision.reason,
    )


def enforce_idempotency(existing_fingerprint: str | None, operation_id: str, payload: object) -> str:
    current = idempotency_fingerprint(operation_id, payload)
    if existing_fingerprint is not None and existing_fingerprint != current:
        raise PolicyError("OPERATION_ID_REPLAY_WITH_DIFFERENT_PAYLOAD")
    return current
