"""Process group / Job Object helpers for Execution Host cleanup attestation.

Lifecycle rule: create processes only via spawn_managed() so session/group
membership (POSIX) or Windows Job Object membership is established at start.

Wrapping an existing Popen cannot attach a Windows Job Object retroactively —
that path is labeled and never claims job_object=ATTACHED.

Isolation (OS sandbox) is separate from Job Object tree containment and remains
NOT_VERIFIED until independently proven.
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


class _WinJob:
    def __init__(self, handle: int):
        self.handle = handle

    def close(self) -> None:
        if self.handle:
            try:
                _kernel32.CloseHandle(self.handle)
            except Exception:
                pass
            self.handle = 0


def _load_kernel32():
    if not sys.platform.startswith("win"):
        return None
    import ctypes
    from ctypes import wintypes

    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
    k.CreateJobObjectW.restype = wintypes.HANDLE
    k.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    k.AssignProcessToJobObject.restype = wintypes.BOOL
    k.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    k.TerminateJobObject.restype = wintypes.BOOL
    k.CloseHandle.argtypes = [wintypes.HANDLE]
    k.CloseHandle.restype = wintypes.BOOL
    k.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD]
    k.SetInformationJobObject.restype = wintypes.BOOL
    k.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    k.OpenProcess.restype = wintypes.HANDLE
    return k


_kernel32 = _load_kernel32()
_JobObjectExtendedLimitInformation = 9
_JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
_PROCESS_SET_QUOTA = 0x0100
_PROCESS_TERMINATE = 0x0001


def _create_job_object() -> tuple:
    notes: list[str] = []
    if _kernel32 is None:
        notes.append("kernel32_unavailable")
        return None, notes
    import ctypes
    from ctypes import wintypes

    handle = _kernel32.CreateJobObjectW(None, None)
    if not handle:
        notes.append(f"CreateJobObjectW_failed_err={ctypes.get_last_error()}")
        return None, notes

    class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_int64),
            ("PerJobUserTimeLimit", ctypes.c_int64),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class IO_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("ReadOperationCount", ctypes.c_uint64),
            ("WriteOperationCount", ctypes.c_uint64),
            ("OtherOperationCount", ctypes.c_uint64),
            ("ReadTransferCount", ctypes.c_uint64),
            ("WriteTransferCount", ctypes.c_uint64),
            ("OtherTransferCount", ctypes.c_uint64),
        ]

    class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
            ("IoInfo", IO_COUNTERS),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        ]

    info = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
    info.BasicLimitInformation.LimitFlags = _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    ok = _kernel32.SetInformationJobObject(
        handle, _JobObjectExtendedLimitInformation, ctypes.byref(info), ctypes.sizeof(info)
    )
    if not ok:
        notes.append(f"SetInformationJobObject_failed_err={ctypes.get_last_error()}")
        _kernel32.CloseHandle(handle)
        return None, notes
    return _WinJob(handle), notes


def _assign_pid_to_job(job, pid: int) -> list:
    notes: list[str] = []
    if _kernel32 is None or not job.handle:
        notes.append("assign_skipped_no_job")
        return notes
    import ctypes
    PROCESS_ALL_ACCESS = 0x1F0FFF
    proc = _kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not proc:
        proc = _kernel32.OpenProcess(_PROCESS_SET_QUOTA | _PROCESS_TERMINATE | 0x1000, False, pid)
    if not proc:
        notes.append(f"OpenProcess_failed_err={ctypes.get_last_error()}")
        return notes
    try:
        ok = _kernel32.AssignProcessToJobObject(job.handle, proc)
        if not ok:
            notes.append(f"AssignProcessToJobObject_failed_err={ctypes.get_last_error()}")
        else:
            notes.append("job_object_assigned")
    finally:
        _kernel32.CloseHandle(proc)
    return notes


def _terminate_job(job, exit_code: int = 1) -> list:
    notes: list[str] = []
    if job is None or not job.handle or _kernel32 is None:
        notes.append("terminate_job_skipped")
        return notes
    import ctypes
    ok = _kernel32.TerminateJobObject(job.handle, exit_code)
    if not ok:
        notes.append(f"TerminateJobObject_failed_err={ctypes.get_last_error()}")
    else:
        notes.append("TerminateJobObject_ok")
    return notes


def _posix_group_members(pgid: int) -> int:
    if pgid <= 0:
        return 0
    try:
        completed = subprocess.run(
            ["ps", "-o", "pid=", "-g", str(pgid)],
            capture_output=True, text=True, timeout=5, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return 0
    n = 0
    for line in (completed.stdout or "").splitlines():
        token = line.strip()
        if not token or not token.isdigit():
            continue
        n += 1
    return n


@dataclass
class ManagedProcess:
    process: subprocess.Popen
    platform: str = field(default_factory=lambda: sys.platform)
    session_leader: bool = False
    created_via_spawn: bool = False
    job_object: str = "NOT_ATTACHED"
    _job: Any = field(default=None, repr=False, compare=False)

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
                if self.platform.startswith("win") and self.job_object == "ATTACHED" and self._job is not None:
                    notes.extend(_terminate_job(self._job))
                    kill_sent = True
                    terminate_sent = terminate_first
                    try:
                        self.process.wait(timeout=wait_timeout)
                        waited = True
                    except subprocess.TimeoutExpired:
                        notes.append("wait_timeout_after_TerminateJobObject")
                        try:
                            self.process.kill()
                            self.process.wait(timeout=wait_timeout)
                            waited = True
                        except (subprocess.TimeoutExpired, OSError) as exc:
                            notes.append(f"force_kill_failed:{type(exc).__name__}")
                elif self.platform.startswith("win"):
                    notes.append("job_object_fallback_process_kill")
                    try:
                        if terminate_first:
                            self.process.terminate()
                            terminate_sent = True
                        else:
                            self.process.kill()
                            kill_sent = True
                        self.process.wait(timeout=wait_timeout)
                        waited = True
                    except subprocess.TimeoutExpired:
                        notes.append("wait_timeout_fallback")
                        try:
                            self.process.kill()
                            kill_sent = True
                            self.process.wait(timeout=wait_timeout)
                            waited = True
                        except (subprocess.TimeoutExpired, OSError) as exc:
                            notes.append(f"force_kill_failed:{type(exc).__name__}")
                elif terminate_first:
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

        if self._job is not None:
            try:
                self._job.close()
            except Exception as exc:
                notes.append(f"job_close_failed:{type(exc).__name__}")
            self._job = None

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
    is_win = sys.platform.startswith("win")
    process = subprocess.Popen(
        list(args), cwd=str(cwd), env=env, text=text,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=not is_win,
    )
    job = None
    job_status = "NOT_ATTACHED"
    spawn_notes: list[str] = []
    if is_win and process.pid:
        job, create_notes = _create_job_object()
        spawn_notes.extend(create_notes)
        if job is not None:
            assign_notes = _assign_pid_to_job(job, process.pid)
            spawn_notes.extend(assign_notes)
            if "job_object_assigned" in assign_notes:
                job_status = "ATTACHED"
            else:
                job.close()
                job = None
                spawn_notes.append("job_object_attach_failed")
        else:
            spawn_notes.append("job_object_create_failed")
    managed = ManagedProcess(
        process=process, platform=sys.platform, session_leader=not is_win,
        created_via_spawn=True, job_object=job_status, _job=job,
    )
    managed._spawn_notes = tuple(spawn_notes)  # type: ignore[attr-defined]
    return managed


def spawn_managed_service(
    args: Sequence[str],
    *,
    cwd: str | Path,
    env: dict[str, str],
) -> ManagedProcess:
    """Long-lived service spawn: DEVNULL streams + Job Object / session at create."""
    is_win = sys.platform.startswith("win")
    process = subprocess.Popen(
        list(args), cwd=str(cwd), env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=not is_win,
    )
    job = None
    job_status = "NOT_ATTACHED"
    spawn_notes: list[str] = []
    if is_win and process.pid:
        job, create_notes = _create_job_object()
        spawn_notes.extend(create_notes)
        if job is not None:
            assign_notes = _assign_pid_to_job(job, process.pid)
            spawn_notes.extend(assign_notes)
            if "job_object_assigned" in assign_notes:
                job_status = "ATTACHED"
            else:
                job.close()
                job = None
                spawn_notes.append("job_object_attach_failed")
        else:
            spawn_notes.append("job_object_create_failed")
    managed = ManagedProcess(
        process=process, platform=sys.platform, session_leader=not is_win,
        created_via_spawn=True, job_object=job_status, _job=job,
    )
    managed._spawn_notes = tuple(spawn_notes)  # type: ignore[attr-defined]
    return managed


def wrap_existing_popen(process: subprocess.Popen) -> ManagedProcess:
    return ManagedProcess(
        process=process, platform=sys.platform, session_leader=False,
        created_via_spawn=False, job_object="NOT_ATTACHED", _job=None,
    )


def job_object_gate(managed: ManagedProcess) -> str | None:
    """Fail-closed Windows Job Object gate for execution paths (WP2).

    Returns a blocker string when process-tree containment is NOT
    guaranteed: on Windows an execution must NOT proceed when the Job
    Object could not be created or attached. POSIX uses the session
    process group established at spawn and passes. This gate NEVER claims
    OS isolation: ISOLATION_STATUS stays NOT_VERIFIED.
    """
    if managed.platform.startswith("win") and managed.job_object != "ATTACHED":
        return "job_object_attach_failed"
    return None


ISOLATION_STATUS = "NOT_VERIFIED"

__all__ = [
    "CleanupResult",
    "ManagedProcess",
    "spawn_managed",
    "spawn_managed_service",
    "wrap_existing_popen",
    "_posix_group_members",
    "ISOLATION_STATUS",
    "job_object_gate",
]
