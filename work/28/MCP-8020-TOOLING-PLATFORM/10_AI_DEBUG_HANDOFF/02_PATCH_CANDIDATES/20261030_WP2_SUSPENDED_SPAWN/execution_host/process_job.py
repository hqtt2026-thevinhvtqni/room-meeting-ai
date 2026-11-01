"""Process group / Job Object helpers for Execution Host cleanup attestation.

Lifecycle rule: create processes only via spawn_managed() so session/group
membership (POSIX) or Windows Job Object membership is established BEFORE any
user code runs.

Windows spawn order (fail-closed, WP2):
  1. CreateJobObjectW + KILL_ON_JOB_CLOSE        (no process exists yet)
  2. Popen(..., creationflags=CREATE_SUSPENDED)  (process exists, runs nothing)
  3. AssignProcessToJobObject                    (membership before first instruction)
  4. ResumeThread on the suspended initial thread (user code starts only now)
If any step fails the suspended process is terminated, it is never resumed and
JobObjectUnavailable (an OSError) is raised so the caller reports BLOCKED. A
child created by the program can only be created after step 4, so it inherits
Job Object membership (breakaway is not permitted by the job limits).

Wrapping an existing Popen cannot attach a Windows Job Object retroactively -
that path is labeled and never claims job_object=ATTACHED.

Isolation (OS sandbox) is separate from Job Object tree containment and remains
NOT_VERIFIED until independently proven.
"""
from __future__ import annotations

import ctypes
import os
import signal
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Sequence


def _is_windows() -> bool:
    return sys.platform.startswith("win")


def _last_error() -> int:
    getter = getattr(ctypes, "get_last_error", None)
    return int(getter()) if getter else 0


class JobObjectUnavailable(OSError):
    """Windows process-tree containment could not be established at spawn.

    Subclass of OSError so existing ``except OSError`` -> BLOCKED paths keep
    working. The user program was never resumed (it executed no instruction).
    """

    blocker = "job_object_attach_failed"

    def __init__(self, notes: Sequence[str], *, process_reaped: bool = True):
        self.notes = tuple(notes)
        self.process_reaped = process_reaped
        super().__init__(f"{self.blocker}: {','.join(self.notes)}")


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


# ---------------------------------------------------------------------------
# Win32 structures (defined on every platform so their ABI size is testable)
# ---------------------------------------------------------------------------
try:
    # Fixed-width fields (DWORD=uint32, LONG=int32 on Windows) so the Win64 ABI
    # layout is identical, and unit-testable, on every platform.
    class _JobBasicLimit(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_int64),
            ("PerJobUserTimeLimit", ctypes.c_int64),
            ("LimitFlags", ctypes.c_uint32),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", ctypes.c_uint32),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", ctypes.c_uint32),
            ("SchedulingClass", ctypes.c_uint32),
        ]

    class _IoCounters(ctypes.Structure):
        _fields_ = [
            ("ReadOperationCount", ctypes.c_uint64),
            ("WriteOperationCount", ctypes.c_uint64),
            ("OtherOperationCount", ctypes.c_uint64),
            ("ReadTransferCount", ctypes.c_uint64),
            ("WriteTransferCount", ctypes.c_uint64),
            ("OtherTransferCount", ctypes.c_uint64),
        ]

    class _JobExtendedLimit(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", _JobBasicLimit),
            ("IoInfo", _IoCounters),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        ]

    class _JobBasicAccounting(ctypes.Structure):
        _fields_ = [
            ("TotalUserTime", ctypes.c_int64),
            ("TotalKernelTime", ctypes.c_int64),
            ("ThisPeriodTotalUserTime", ctypes.c_int64),
            ("ThisPeriodTotalKernelTime", ctypes.c_int64),
            ("TotalPageFaultCount", ctypes.c_uint32),
            ("TotalProcesses", ctypes.c_uint32),
            ("ActiveProcesses", ctypes.c_uint32),
            ("TotalTerminatedProcesses", ctypes.c_uint32),
        ]

    class _ThreadEntry32(ctypes.Structure):
        _fields_ = [
            ("dwSize", ctypes.c_uint32),
            ("cntUsage", ctypes.c_uint32),
            ("th32ThreadID", ctypes.c_uint32),
            ("th32OwnerProcessID", ctypes.c_uint32),
            ("tpBasePri", ctypes.c_int32),
            ("tpDeltaPri", ctypes.c_int32),
            ("dwFlags", ctypes.c_uint32),
        ]
except Exception:  # pragma: no cover - ctypes unavailable
    _JobExtendedLimit = _JobBasicAccounting = _ThreadEntry32 = None  # type: ignore[assignment]


def _load_kernel32():
    if not _is_windows():
        return None
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
    k.QueryInformationJobObject.argtypes = [
        wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID,
    ]
    k.QueryInformationJobObject.restype = wintypes.BOOL
    k.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    k.OpenProcess.restype = wintypes.HANDLE
    k.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    k.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    k.Thread32First.argtypes = [wintypes.HANDLE, wintypes.LPVOID]
    k.Thread32First.restype = wintypes.BOOL
    k.Thread32Next.argtypes = [wintypes.HANDLE, wintypes.LPVOID]
    k.Thread32Next.restype = wintypes.BOOL
    k.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    k.OpenThread.restype = wintypes.HANDLE
    k.ResumeThread.argtypes = [wintypes.HANDLE]
    k.ResumeThread.restype = wintypes.DWORD
    return k


_kernel32 = _load_kernel32()
_CREATE_SUSPENDED = 0x00000004
_JobObjectBasicAccountingInformation = 1
_JobObjectExtendedLimitInformation = 9
_JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
_PROCESS_SET_QUOTA = 0x0100
_PROCESS_TERMINATE = 0x0001
_TH32CS_SNAPTHREAD = 0x00000004
_THREAD_SUSPEND_RESUME = 0x0002
_RESUME_FAILED = 0xFFFFFFFF


def _invalid_handle(handle) -> bool:
    return handle in (None, 0, ctypes.c_void_p(-1).value)


def _create_job_object() -> tuple:
    notes: list[str] = []
    if _kernel32 is None:
        notes.append("kernel32_unavailable")
        return None, notes

    handle = _kernel32.CreateJobObjectW(None, None)
    if not handle:
        notes.append(f"CreateJobObjectW_failed_err={_last_error()}")
        return None, notes

    # No JOB_OBJECT_LIMIT_BREAKAWAY_OK / SILENT_BREAKAWAY_OK: members cannot escape.
    info = _JobExtendedLimit()
    info.BasicLimitInformation.LimitFlags = _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    ok = _kernel32.SetInformationJobObject(
        handle, _JobObjectExtendedLimitInformation, ctypes.byref(info), ctypes.sizeof(info)
    )
    if not ok:
        notes.append(f"SetInformationJobObject_failed_err={_last_error()}")
        _kernel32.CloseHandle(handle)
        return None, notes
    return _WinJob(handle), notes


def _assign_pid_to_job(job, pid: int) -> list:
    notes: list[str] = []
    if _kernel32 is None or not job.handle:
        notes.append("assign_skipped_no_job")
        return notes
    PROCESS_ALL_ACCESS = 0x1F0FFF
    proc = _kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not proc:
        proc = _kernel32.OpenProcess(_PROCESS_SET_QUOTA | _PROCESS_TERMINATE | 0x1000, False, pid)
    if not proc:
        notes.append(f"OpenProcess_failed_err={_last_error()}")
        return notes
    try:
        ok = _kernel32.AssignProcessToJobObject(job.handle, proc)
        if not ok:
            notes.append(f"AssignProcessToJobObject_failed_err={_last_error()}")
        else:
            notes.append("job_object_assigned")
    finally:
        _kernel32.CloseHandle(proc)
    return notes


def _job_active_processes(job) -> int | None:
    """Real Job Object membership (ActiveProcesses); None if it cannot be read."""
    if _kernel32 is None or job is None or not job.handle or _JobBasicAccounting is None:
        return None
    info = _JobBasicAccounting()
    ok = _kernel32.QueryInformationJobObject(
        job.handle, _JobObjectBasicAccountingInformation,
        ctypes.byref(info), ctypes.sizeof(info), None,
    )
    if not ok:
        return None
    return int(info.ActiveProcesses)


def _wait_job_drained(job, timeout: float, notes: list) -> bool:
    """Wait until the Job reports zero active processes after TerminateJobObject."""
    deadline = time.monotonic() + max(timeout, 0.0)
    while True:
        active = _job_active_processes(job)
        if active is None:
            notes.append("job_member_count_unavailable_fail_closed")
            return False
        if active == 0:
            return True
        if time.monotonic() >= deadline:
            notes.append(f"job_members_remain_after_terminate={active}")
            return False
        time.sleep(0.02)


def _resume_suspended_process(pid: int) -> tuple:
    """Resume the initial thread of a CREATE_SUSPENDED process.

    Succeeds only if a thread of ``pid`` reported previous suspend count == 1
    (it really was suspended and is now running). Returns (notes, ok).
    """
    notes: list[str] = []
    if _kernel32 is None or _ThreadEntry32 is None:
        notes.append("resume_skipped_no_kernel32")
        return notes, False
    snap = _kernel32.CreateToolhelp32Snapshot(_TH32CS_SNAPTHREAD, 0)
    if _invalid_handle(snap):
        notes.append(f"CreateToolhelp32Snapshot_failed_err={_last_error()}")
        return notes, False
    resumed = 0
    try:
        entry = _ThreadEntry32()
        entry.dwSize = ctypes.sizeof(entry)
        ok = _kernel32.Thread32First(snap, ctypes.byref(entry))
        while ok:
            if entry.th32OwnerProcessID == pid:
                thread = _kernel32.OpenThread(_THREAD_SUSPEND_RESUME, False, entry.th32ThreadID)
                if not thread:
                    notes.append(f"OpenThread_failed_err={_last_error()}")
                else:
                    try:
                        previous = _kernel32.ResumeThread(thread)
                        if previous == _RESUME_FAILED:
                            notes.append(f"ResumeThread_failed_err={_last_error()}")
                        elif previous == 1:
                            resumed += 1
                        elif previous == 0:
                            notes.append("thread_was_not_suspended")
                        else:
                            notes.append(f"thread_still_suspended_count={previous - 1}")
                    finally:
                        _kernel32.CloseHandle(thread)
            entry.dwSize = ctypes.sizeof(entry)
            ok = _kernel32.Thread32Next(snap, ctypes.byref(entry))
    finally:
        _kernel32.CloseHandle(snap)
    if resumed < 1:
        notes.append("resume_failed_no_suspended_thread")
        return notes, False
    notes.append(f"resumed_threads={resumed}")
    return notes, True


def _terminate_job(job, exit_code: int = 1) -> list:
    notes: list[str] = []
    if job is None or not job.handle or _kernel32 is None:
        notes.append("terminate_job_skipped")
        return notes
    ok = _kernel32.TerminateJobObject(job.handle, exit_code)
    if not ok:
        notes.append(f"TerminateJobObject_failed_err={_last_error()}")
    else:
        notes.append("TerminateJobObject_ok")
    return notes


def _posix_group_members(pgid: int) -> int:
    if pgid <= 0:
        return 0
    try:
        completed = subprocess.run(
            ["ps", "-o", "pid=,pgid=,stat=", "-g", str(pgid)],
            capture_output=True, text=True, timeout=5, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return 0
    n = 0
    for line in (completed.stdout or "").splitlines():
        tokens = line.split()
        if not tokens or not tokens[0].isdigit():
            continue
        if len(tokens) >= 3:
            if tokens[1] != str(pgid):
                continue  # `ps -g` also matches by effective group id: not membership
            if tokens[2].startswith("Z"):
                continue  # zombie = already dead (init-less containers never reap it)
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
    _spawn_notes: tuple = field(default=(), repr=False, compare=False)
    # POSIX: pgid == leader pid (start_new_session). Needed because getpgid(leader)
    # fails once the leader is reaped, which made members_after always 0.
    _pgid: int | None = field(default=None, repr=False, compare=False)

    @property
    def pid(self) -> int | None:
        return self.process.pid

    def poll(self) -> int | None:
        return self.process.poll()

    def members_count(self) -> int | None:
        if self.platform.startswith("win"):
            if self._job is not None:
                # Unknown Job membership is not equivalent to zero members.
                # Preserve None so cleanup cannot report a false drained state.
                return _job_active_processes(self._job)
            return 1 if self.poll() is None else 0
        if self._pgid is not None:
            return _posix_group_members(self._pgid)
        try:
            pgid = os.getpgid(self.process.pid)
        except (OSError, ProcessLookupError, AttributeError):
            return 0 if self.poll() is not None else None
        return _posix_group_members(pgid)

    def _drain_posix_group(self, terminate_first: bool, timeout: float, notes: list) -> tuple:
        """Wait until the session process group has no live member; SIGKILL stragglers.

        SIGTERM/SIGKILL delivery is asynchronous: the leader can be reaped while a
        child is still runnable. Also covers orphans left by a leader that already
        exited. Returns (drained, escalated).
        """
        pgid = self._pgid
        start = time.monotonic()
        limit = max(timeout, 0.0)
        grace = min(0.5, limit / 2) if terminate_first else 0.0
        escalated = False
        while True:
            remaining = _posix_group_members(pgid)
            if remaining == 0:
                return True, escalated
            elapsed = time.monotonic() - start
            if not escalated and elapsed >= grace:
                try:
                    os.killpg(pgid, signal.SIGKILL)
                    escalated = True
                    notes.append("group_sigkill_stragglers")
                except ProcessLookupError:
                    return True, escalated
                except OSError as exc:
                    notes.append(f"group_sigkill_failed:{type(exc).__name__}")
                    return False, escalated
            if elapsed >= limit:
                notes.append(f"group_members_remain_after_drain={remaining}")
                return False, escalated
            time.sleep(0.02)

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
        drained = True
        win_job = (
            self.platform.startswith("win")
            and self.job_object == "ATTACHED"
            and self._job is not None
        )

        if win_job:
            # Job members can outlive the leader (orphans): terminate whenever the
            # leader is alive OR the Job still reports active processes.
            try:
                if self.process.poll() is None or before is None or before > 0:
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
                    drained = _wait_job_drained(self._job, wait_timeout, notes)
            except OSError as exc:
                notes.append(f"signal_failed:{type(exc).__name__}")
        elif self.process.poll() is None:
            try:
                if self.platform.startswith("win"):
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

        if self.session_leader and self._pgid is not None and not self.platform.startswith("win"):
            drained, escalated = self._drain_posix_group(terminate_first, wait_timeout, notes)
            kill_sent = kill_sent or escalated

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

        # Read membership BEFORE closing the Job handle (a closed handle cannot be queried).
        after = self.members_count()
        if self._job is not None:
            try:
                self._job.close()
            except Exception as exc:
                notes.append(f"job_close_failed:{type(exc).__name__}")
            self._job = None

        reaped = self.process.poll() is not None
        if before is not None and before > 0 and after is not None and after > 0 and reaped:
            notes.append("group_members_remain")
            reaped = False
        if not drained:
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


def _abort_suspended(process: subprocess.Popen, job, notes: list, *, assigned: bool,
                     timeout: float = 5.0) -> bool:
    """Kill a never-resumed process; returns True when it is confirmed dead."""
    if assigned and job is not None:
        notes.extend(_terminate_job(job))
    try:
        process.kill()
    except OSError as exc:
        notes.append(f"abort_kill_failed:{type(exc).__name__}")
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        notes.append("abort_wait_timeout")
    for stream in (getattr(process, "stdout", None), getattr(process, "stderr", None)):
        try:
            if stream is not None:
                stream.close()
        except Exception:
            pass
    if job is not None:
        job.close()
    reaped = process.poll() is not None
    notes.append("suspended_process_terminated_never_resumed" if reaped else "abort_process_not_reaped")
    return reaped


def _spawn(
    args: Sequence[str],
    *,
    cwd: str | Path,
    env: dict[str, str],
    text: bool | None,
    stdout: Any,
    stderr: Any,
) -> ManagedProcess:
    kwargs: dict[str, Any] = dict(cwd=str(cwd), env=env, stdout=stdout, stderr=stderr)
    if text is not None:
        kwargs["text"] = text

    if not _is_windows():
        process = subprocess.Popen(list(args), start_new_session=True, **kwargs)
        return ManagedProcess(
            process=process, platform=sys.platform, session_leader=True,
            created_via_spawn=True, job_object="NOT_ATTACHED", _job=None,
            _pgid=process.pid,
        )

    notes: list[str] = []
    job, create_notes = _create_job_object()
    notes.extend(create_notes)
    if job is None:
        notes.append("job_object_create_failed")
        raise JobObjectUnavailable(notes, process_reaped=True)  # nothing was started

    try:
        process = subprocess.Popen(list(args), creationflags=_CREATE_SUSPENDED, **kwargs)
    except BaseException:
        job.close()
        raise
    notes.append("created_suspended")

    assigned = False
    try:
        assign_notes = _assign_pid_to_job(job, process.pid)
        notes.extend(assign_notes)
        if "job_object_assigned" not in assign_notes:
            notes.append("job_object_attach_failed")
            reaped = _abort_suspended(process, job, notes, assigned=False)
            raise JobObjectUnavailable(notes, process_reaped=reaped)
        assigned = True

        resume_notes, resumed = _resume_suspended_process(process.pid)
        notes.extend(resume_notes)
        if not resumed:
            notes.append("job_object_resume_failed")
            reaped = _abort_suspended(process, job, notes, assigned=True)
            raise JobObjectUnavailable(notes, process_reaped=reaped)
    except JobObjectUnavailable:
        raise
    except BaseException:
        _abort_suspended(process, job, notes, assigned=assigned)
        raise

    notes.append("resumed_after_job_attach")
    return ManagedProcess(
        process=process, platform=sys.platform, session_leader=False,
        created_via_spawn=True, job_object="ATTACHED", _job=job,
        _spawn_notes=tuple(notes),
    )


def spawn_managed(
    args: Sequence[str],
    *,
    cwd: str | Path,
    env: dict[str, str],
    text: bool = True,
) -> ManagedProcess:
    return _spawn(
        args, cwd=cwd, env=env, text=text,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )


def spawn_managed_service(
    args: Sequence[str],
    *,
    cwd: str | Path,
    env: dict[str, str],
) -> ManagedProcess:
    """Long-lived service spawn: DEVNULL streams + Job Object / session at create."""
    return _spawn(
        args, cwd=cwd, env=env, text=None,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def wrap_existing_popen(process: subprocess.Popen) -> ManagedProcess:
    return ManagedProcess(
        process=process, platform=sys.platform, session_leader=False,
        created_via_spawn=False, job_object="NOT_ATTACHED", _job=None,
    )


def job_object_gate(managed: ManagedProcess) -> str | None:
    """Fail-closed Windows Job Object gate for execution paths (WP2).

    Defense in depth: spawn_managed() already raises JobObjectUnavailable on
    Windows when containment cannot be established, so a returned ManagedProcess
    on Windows is ATTACHED. This gate still returns a blocker string for any
    synthetic or wrapped process that is not ATTACHED. POSIX uses the session
    process group established at spawn and passes. This gate NEVER claims OS
    isolation: ISOLATION_STATUS stays NOT_VERIFIED.
    """
    if managed.platform.startswith("win") and managed.job_object != "ATTACHED":
        return "job_object_attach_failed"
    return None


ISOLATION_STATUS = "NOT_VERIFIED"

__all__ = [
    "CleanupResult",
    "JobObjectUnavailable",
    "ManagedProcess",
    "spawn_managed",
    "spawn_managed_service",
    "wrap_existing_popen",
    "_posix_group_members",
    "ISOLATION_STATUS",
    "job_object_gate",
]
