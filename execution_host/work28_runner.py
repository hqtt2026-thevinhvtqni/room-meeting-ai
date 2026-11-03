"""Narrow Work 28 snapshot runner for the existing Work 13 host.

No caller-supplied command vector is accepted. This helper is staged and is not
wired to the HTTP endpoint; authenticated Core authorization and runtime
attestation remain separate mandatory gates.
"""
from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from .work28_contract import SourceSnapshot, Work28ContractError

_ALLOWED = {"RUN_SCRIPT", "RUN_TESTS"}


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


def _group_exists(pid: int) -> bool:
    try:
        os.killpg(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def _stop_process_tree(process: subprocess.Popen[str]) -> bool:
    """Stop the owned process group/tree and verify it is no longer present."""
    if os.name == "nt":
        # taskkill is an OS utility invoked with a fixed argument vector; no shell.
        try:
            result = subprocess.run(
                ["taskkill.exe", "/PID", str(process.pid), "/T", "/F"],
                capture_output=True, text=True, timeout=5, check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return False
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            return False
        # taskkill returns 128 when the process already exited. Verify root exit;
        # Windows does not expose a portable process-tree query through stdlib.
        return process.poll() is not None and result.returncode in (0, 128)
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return process.poll() is not None
    except OSError:
        return False
    deadline = time.monotonic() + 1.0
    while time.monotonic() < deadline:
        if not _group_exists(process.pid):
            try:
                process.wait(timeout=0.2)
            except subprocess.TimeoutExpired:
                pass
            return True
        time.sleep(0.025)
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except OSError:
        return False
    deadline = time.monotonic() + 1.0
    while time.monotonic() < deadline:
        if not _group_exists(process.pid):
            try:
                process.wait(timeout=0.2)
            except subprocess.TimeoutExpired:
                pass
            return True
        time.sleep(0.025)
    return False


def run_snapshot(
    *, snapshot: SourceSnapshot, operation: str, timeout_seconds: int,
) -> SnapshotRunResult:
    """Run only a previously validated snapshot with a fixed operation mapping."""
    if operation not in _ALLOWED:
        raise Work28ContractError("unsupported_operation")
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, int) or not 1 <= timeout_seconds <= 300:
        raise Work28ContractError("timeout_out_of_range")
    path = Path(snapshot.snapshot_path)
    if not path.is_file():
        raise Work28ContractError("snapshot_missing")
    import hashlib
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != snapshot.source_sha256:
        raise Work28ContractError("snapshot_changed_after_validation")
    if operation == "RUN_SCRIPT":
        argv = [sys.executable, str(path)]
    else:
        argv = [sys.executable, "-m", "pytest", "-q", str(path)]
    kwargs = {
        "cwd": str(path.parent),
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True,
        "shell": False,
    }
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
    try:
        process = subprocess.Popen(argv, **kwargs)
    except OSError as exc:
        return SnapshotRunResult(
            "BLOCKED", operation, snapshot.work_id, snapshot.snapshot_ref,
            snapshot.source_sha256, None, False, True, "", str(exc),
        )
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        cleanup = _stop_process_tree(process)
        try:
            stdout, stderr = process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            stdout, stderr = "", "process_output_collection_timeout"
            cleanup = False
    else:
        # Even after the leader exits, stop any child left in its owned group.
        cleanup = _stop_process_tree(process)
    code = process.returncode
    status = "PASS" if code == 0 and not timed_out and cleanup else "FAILED"
    if not cleanup:
        status = "BLOCKED"
    return SnapshotRunResult(
        status, operation, snapshot.work_id, snapshot.snapshot_ref,
        snapshot.source_sha256, code, timed_out, cleanup, stdout, stderr,
    )


__all__ = ["SnapshotRunResult", "run_snapshot"]
