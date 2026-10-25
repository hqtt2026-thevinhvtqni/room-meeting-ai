"""Fail-closed snapshot runner seam; not wired to HTTP."""
from __future__ import annotations
import hashlib
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from .work28_contract import SourceSnapshot, Work28ContractError

@dataclass(frozen=True)
class SnapshotRunResult:
    status: str
    operation: str
    work_id: str
    snapshot_ref: str
    source_sha256: str
    exit_code: int | None
    timed_out: bool
    cleanup_verified: bool
    stdout: str
    stderr: str

def run_snapshot(*, snapshot: SourceSnapshot, operation: str, timeout_seconds: int) -> SnapshotRunResult:
    if operation not in {"RUN_SCRIPT", "RUN_TESTS"}:
        raise Work28ContractError("unsupported_operation")
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, int) or not 1 <= timeout_seconds <= 300:
        raise Work28ContractError("timeout_out_of_range")
    path = Path(snapshot.snapshot_path)
    if not path.is_file():
        raise Work28ContractError("snapshot_missing")
    if hashlib.sha256(path.read_bytes()).hexdigest() != snapshot.source_sha256:
        raise Work28ContractError("snapshot_changed_after_validation")
    argv = [sys.executable, str(path)] if operation == "RUN_SCRIPT" else [sys.executable, "-m", "pytest", "-q", str(path)]
    try:
        result = subprocess.run(argv, cwd=str(path.parent), stdin=subprocess.DEVNULL, capture_output=True, text=True, shell=False, timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        return SnapshotRunResult("BLOCKED", operation, snapshot.work_id, snapshot.snapshot_ref, snapshot.source_sha256, None, True, False, stdout, stderr)
    except OSError as exc:
        return SnapshotRunResult("BLOCKED", operation, snapshot.work_id, snapshot.snapshot_ref, snapshot.source_sha256, None, False, True, "", str(exc))
    return SnapshotRunResult("PASS" if result.returncode == 0 else "FAILED", operation, snapshot.work_id, snapshot.snapshot_ref, snapshot.source_sha256, result.returncode, False, True, result.stdout, result.stderr)
