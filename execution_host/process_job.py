"""Process group / job helpers for Execution Host cleanup attestation.

Fail-closed counting: never report zero members when the leader still exists
and is observable. Isolation is NOT claimed here — only process-tree reaping.
"""
from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
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
    notes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _posix_group_members(pgid: int) -> int:
    """Count processes in process group *pgid* (POSIX).

    Uses ``ps -o pid= -g <pgid>``. Empty/invalid lines are skipped with
    ``continue``; the counter is incremented only for valid PID lines
    (must not sit under the ``continue`` branch).
    """
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
        # Valid PID token only — increment is NOT under continue.
        if not token.isdigit():
            continue
        n += 1
    return n


@dataclass
class ManagedProcess:
    """Wrap a Popen with attested cleanup (no OS sandbox claim)."""

    process: subprocess.Popen
    platform: str = field(default_factory=lambda: sys.platform)

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
        leader = self.process.pid
        before = self.members_count()
        terminate_sent = False
        kill_sent = False
        waited = False

        if self.process.poll() is None:
            try:
                if terminate_first:
                    if self.platform.startswith("win"):
                        self.process.terminate()
                    else:
                        try:
                            os.killpg(os.getpgid(leader), signal.SIGTERM)
                        except (OSError, ProcessLookupError):
                            self.process.terminate()
                    terminate_sent = True
                else:
                    if self.platform.startswith("win"):
                        self.process.kill()
                    else:
                        try:
                            os.killpg(os.getpgid(leader), signal.SIGKILL)
                        except (OSError, ProcessLookupError):
                            self.process.kill()
                    kill_sent = True
                try:
                    self.process.wait(timeout=wait_timeout)
                    waited = True
                except subprocess.TimeoutExpired:
                    notes.append("wait_timeout_after_terminate")
                    try:
                        if self.platform.startswith("win"):
                            self.process.kill()
                        else:
                            try:
                                os.killpg(os.getpgid(leader), signal.SIGKILL)
                            except (OSError, ProcessLookupError):
                                self.process.kill()
                        kill_sent = True
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
            notes=tuple(notes),
        )


def spawn_managed(
    args: Sequence[str],
    *,
    cwd: str | Path,
    env: dict[str, str],
    text: bool = True,
) -> ManagedProcess:
    process = subprocess.Popen(
        list(args),
        cwd=str(cwd),
        env=env,
        text=text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=not sys.platform.startswith("win"),
    )
    return ManagedProcess(process=process)


__all__ = [
    "CleanupResult",
    "ManagedProcess",
    "spawn_managed",
    "_posix_group_members",
]
