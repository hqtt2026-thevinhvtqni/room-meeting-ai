"""Process group helpers for Execution Host cleanup attestation.

Lifecycle rule: create processes only via spawn_managed() so session/group
membership is established at start. Wrapping an existing Popen cannot attach a
Windows Job Object retroactively — that path is labeled explicitly and never
claims isolation PASS.
"""
from __future__ import annotations

import os
import signal
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Sequence


@dataclass(frozen=True)
class CleanupResult:
    process_reaped: bool
    leader_pid: int | None = None
    members_before: int | None = None
    members_after: int | None = None
    terminate_sent: bool = False
    kill_sent: bool = False
    waited: bool = False
    platform: str = ""
    job_object: str = "NOT_ATTACHED"
    session_leader: bool = False
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _windows_kill_tree(pid: int) -> list[str]:
    """Best-effort kill process tree on Windows via taskkill /T.

    This is NOT a Job Object. Callers must keep job_object=NOT_ATTACHED.
    """
    notes: list[str] = []
    if pid <= 0:
        return notes
    try:
        completed = subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(pid)],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if completed.returncode != 0:
            notes.append(f"taskkill_rc={completed.returncode}")
        else:
            notes.append("taskkill_tree_attempted")
    except (OSError, subprocess.TimeoutExpired) as exc:
        notes.append(f"taskkill_failed:{type(exc).__name__}")
    return notes


def _posix_group_members(pgid: int) -> int:
    """Count processes in process group *pgid* (POSIX)."""
    if pgid <= 0:
        return 0
    try:
        completed = subprocess.run(
            ["ps", "-o", "pid=", "-g", str(pgid)],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return 0

    n = 0
    for line in (completed.stdout or "").splitlines():
        token = line.strip()
        if not token:
            continue
        if not token.isdigit():
            continue
        n += 1
    return n


@dataclass
class ManagedProcess:
    """Process started under spawn_managed (preferred) or explicitly wrapped.

    isolation is never PASS here — only reaping/attestation.
    """

    process: subprocess.Popen
    platform: str = field(default_factory=lambda: sys.platform)
    session_leader: bool = False
    created_via_spawn: bool = False
    job_object: str = "NOT_ATTACHED"

    @property
    def pid(self) -> int | None:
        return self.process.pid

    def poll(self) -> int | None:
        return self.process.poll()

    def members_count(self) -> int | None:
        if self.platform.startswith("win"):
            return 1 if self.poll() is None else 0
        try:
            pgid = os.getpgid(self.process.pid)
        except (OSError, ProcessLookupError, AttributeError):
            return 0 if self.poll() is not None else None
        return _posix_group_members(pgid)

    def cleanup(self, *, terminate_first: bool = True, wait_timeout: float = 5.0) -> CleanupResult:
        notes: list[str] = []
        if not self.created_via_spawn:
            notes.append("wrapped_existing_popen")
            notes.append("job_object_cannot_attach_retroactively")
        if self.job_object != "ATTACHED":
            notes.append("job_object_not_attached")

        leader = self.process.pid
        before = self.members_count()
        terminate_sent = False
        kill_sent = False
        waited = False

        if self.process.poll() is None:
            try:
                if self.platform.startswith("win"):
                    notes.extend(_windows_kill_tree(leader))
                    terminate_sent = terminate_first
                    kill_sent = True
                    try:
                        self.process.wait(timeout=wait_timeout)
                        waited = True
                    except subprocess.TimeoutExpired:
                        notes.append("wait_timeout_after_taskkill")
                        try:
                            self.process.kill()
                            self.process.wait(timeout=wait_timeout)
                            waited = True
                        except (subprocess.TimeoutExpired, OSError) as exc:
                            notes.append(f"force_kill_failed:{type(exc).__name__}")
                elif terminate_first:
                    # killpg only when we created a new session; otherwise we
                    # would signal the test runner's process group.
                    if self.session_leader:
                        try:
                            os.killpg(os.getpgid(leader), signal.SIGTERM)
                        except (OSError, ProcessLookupError):
                            self.process.terminate()
                    else:
                        self.process.terminate()
                    terminate_sent = True
                    try:
                        self.process.wait(timeout=wait_timeout)
                        waited = True
                    except subprocess.TimeoutExpired:
                        notes.append("wait_timeout_after_terminate")
                        if self.session_leader:
                            try:
                                os.killpg(os.getpgid(leader), signal.SIGKILL)
                            except (OSError, ProcessLookupError):
                                self.process.kill()
                        else:
                            self.process.kill()
                        kill_sent = True
                        try:
                            self.process.wait(timeout=wait_timeout)
                            waited = True
                        except (subprocess.TimeoutExpired, OSError) as exc:
                            notes.append(f"force_kill_failed:{type(exc).__name__}")
                else:
                    if self.session_leader:
                        try:
                            os.killpg(os.getpgid(leader), signal.SIGKILL)
                        except (OSError, ProcessLookupError):
                            self.process.kill()
                    else:
                        self.process.kill()
                    kill_sent = True
                    try:
                        self.process.wait(timeout=wait_timeout)
                        waited = True
                    except subprocess.TimeoutExpired:
                        notes.append("wait_timeout_after_kill")
                        try:
                            self.process.kill()
                            self.process.wait(timeout=wait_timeout)
                            waited = True
                        except (subprocess.TimeoutExpired, OSError) as exc:
                            notes.append(f"force_kill_failed:{type(exc).__name__}")
            except OSError as exc:
                notes.append(f"signal_failed:{type(exc).__name__}")

        try:
            self.process.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            try:
                self.process.kill()
                kill_sent = True
            except OSError:
                pass
            try:
                self.process.communicate(timeout=1)
            except subprocess.TimeoutExpired:
                notes.append("communicate_timeout")

        after = self.members_count()
        reaped = self.process.poll() is not None
        if before is not None and before > 0 and after is not None and after > 0 and reaped:
            notes.append("group_members_remain")
            reaped = False

        return CleanupResult(
            process_reaped=reaped,
            leader_pid=leader,
            members_before=before,
            members_after=after,
            terminate_sent=terminate_sent,
            kill_sent=kill_sent,
            waited=waited,
            platform=self.platform,
            job_object=self.job_object,
            session_leader=self.session_leader,
            notes=tuple(notes),
        )


def spawn_managed(
    args: Sequence[str],
    *,
    cwd: str | Path,
    env: dict[str, str],
    text: bool = True,
) -> ManagedProcess:
    """Create a process with session leadership on POSIX at spawn time.

    Windows Job Object is not attached in this build — job_object stays
    NOT_ATTACHED and callers must keep isolation at NOT_VERIFIED.
    """
    is_win = sys.platform.startswith("win")
    process = subprocess.Popen(
        list(args),
        cwd=str(cwd),
        env=env,
        text=text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=not is_win,
    )
    return ManagedProcess(
        process=process,
        platform=sys.platform,
        session_leader=not is_win,
        created_via_spawn=True,
        job_object="NOT_ATTACHED",
    )


def wrap_existing_popen(process: subprocess.Popen) -> ManagedProcess:
    """Explicit post-hoc wrap — does NOT claim Job Object or isolation."""
    return ManagedProcess(
        process=process,
        platform=sys.platform,
        session_leader=False,
        created_via_spawn=False,
        job_object="NOT_ATTACHED",
    )


ISOLATION_STATUS = "NOT_VERIFIED"

__all__ = [
    "CleanupResult",
    "ManagedProcess",
    "spawn_managed",
    "wrap_existing_popen",
    "_posix_group_members",
    "ISOLATION_STATUS",
]
