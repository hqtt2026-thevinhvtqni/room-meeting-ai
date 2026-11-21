"""OS process-tree containment primitives for Work 10.

Windows uses a Job Object with KILL_ON_JOB_CLOSE. The parent assigns the
worker while it is still waiting at an inert stdin gate; application work must
not be released before assignment succeeds.

POSIX process groups are provided as a limited fallback only. They are not
claimed to be equivalent to cgroup-v2 containment and must not be accepted as
the hardened Linux profile without a separate cgroup fixture.
"""
from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass


class ContainmentError(RuntimeError):
    pass


class ContainmentUnsupported(ContainmentError):
    pass


@dataclass(frozen=True)
class ContainmentIdentity:
    profile_id: str
    locator: str
    owner_pid: int
    worker_pid: int
    created_at: str
    assurance: str


if os.name == "nt":
    import ctypes
    from ctypes import wintypes

    JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
    JobObjectBasicAccountingInformation = 1
    JobObjectExtendedLimitInformation = 9
    WAIT_OBJECT_0 = 0x00000000
    WAIT_TIMEOUT = 0x00000102
    SYNCHRONIZE = 0x00100000

    class _BasicLimitInformation(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_longlong),
            ("PerJobUserTimeLimit", ctypes.c_longlong),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class _IoCounters(ctypes.Structure):
        _fields_ = [
            ("ReadOperationCount", ctypes.c_ulonglong),
            ("WriteOperationCount", ctypes.c_ulonglong),
            ("OtherOperationCount", ctypes.c_ulonglong),
            ("ReadTransferCount", ctypes.c_ulonglong),
            ("WriteTransferCount", ctypes.c_ulonglong),
            ("OtherTransferCount", ctypes.c_ulonglong),
        ]

    class _ExtendedLimitInformation(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", _BasicLimitInformation),
            ("IoInfo", _IoCounters),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        ]

    class _BasicAccountingInformation(ctypes.Structure):
        _fields_ = [
            ("TotalUserTime", ctypes.c_longlong),
            ("TotalKernelTime", ctypes.c_longlong),
            ("ThisPeriodTotalUserTime", ctypes.c_longlong),
            ("ThisPeriodTotalKernelTime", ctypes.c_longlong),
            ("TotalPageFaultCount", wintypes.DWORD),
            ("TotalProcesses", wintypes.DWORD),
            ("ActiveProcesses", wintypes.DWORD),
            ("TotalTerminatedProcesses", wintypes.DWORD),
        ]

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    _kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    _kernel32.SetInformationJobObject.argtypes = [
        wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD
    ]
    _kernel32.SetInformationJobObject.restype = wintypes.BOOL
    _kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    _kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    _kernel32.QueryInformationJobObject.argtypes = [
        wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD)
    ]
    _kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    _kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    _kernel32.TerminateJobObject.restype = wintypes.BOOL
    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    _kernel32.CloseHandle.restype = wintypes.BOOL
    _kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _kernel32.OpenProcess.restype = wintypes.HANDLE
    _kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    _kernel32.WaitForSingleObject.restype = wintypes.DWORD

    class WindowsJob:
        """Named Windows Job Object; closing the last handle kills all members."""

        profile_id = "windows-job-object-kill-on-close-v1"
        assurance = "OS_JOB_OBJECT"

        def __init__(self, run_id: str | None = None):
            self.run_id = run_id or str(uuid.uuid4())
            self.name = "Local\\Work10Job-" + self.run_id
            self.handle = _kernel32.CreateJobObjectW(None, self.name)
            if not self.handle:
                raise ContainmentError(
                    f"CreateJobObjectW failed: {ctypes.get_last_error()}"
                )
            info = _ExtendedLimitInformation()
            info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            ok = _kernel32.SetInformationJobObject(
                self.handle, JobObjectExtendedLimitInformation,
                ctypes.byref(info), ctypes.sizeof(info)
            )
            if not ok:
                code = ctypes.get_last_error()
                _kernel32.CloseHandle(self.handle)
                self.handle = None
                raise ContainmentError(f"SetInformationJobObject failed: {code}")

        def assign_process(self, process: subprocess.Popen) -> None:
            if self.handle is None:
                raise ContainmentError("job handle is closed")
            process_handle = wintypes.HANDLE(int(process._handle))
            if not _kernel32.AssignProcessToJobObject(self.handle, process_handle):
                raise ContainmentError(
                    f"AssignProcessToJobObject failed: {ctypes.get_last_error()}"
                )

        def active_processes(self) -> int:
            if self.handle is None:
                return 0
            info = _BasicAccountingInformation()
            ok = _kernel32.QueryInformationJobObject(
                self.handle, JobObjectBasicAccountingInformation,
                ctypes.byref(info), ctypes.sizeof(info), None
            )
            if not ok:
                raise ContainmentError(
                    f"QueryInformationJobObject failed: {ctypes.get_last_error()}"
                )
            return int(info.ActiveProcesses)

        def terminate(self, exit_code: int = 1) -> None:
            if self.handle is not None and not _kernel32.TerminateJobObject(self.handle, exit_code):
                raise ContainmentError(
                    f"TerminateJobObject failed: {ctypes.get_last_error()}"
                )

        def close(self) -> None:
            handle, self.handle = self.handle, None
            if handle:
                # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE is the crash/owner-loss fence.
                if not _kernel32.CloseHandle(handle):
                    raise ContainmentError(
                        f"CloseHandle(job) failed: {ctypes.get_last_error()}"
                    )

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            self.close()

    def wait_pid_exit(pid: int, timeout_seconds: float = 5.0) -> bool:
        handle = _kernel32.OpenProcess(SYNCHRONIZE, False, int(pid))
        if not handle:
            # ERROR_INVALID_PARAMETER means the process ID no longer exists.
            return ctypes.get_last_error() == 87
        try:
            milliseconds = max(0, int(timeout_seconds * 1000))
            return _kernel32.WaitForSingleObject(handle, milliseconds) == WAIT_OBJECT_0
        finally:
            _kernel32.CloseHandle(handle)

else:
    class WindowsJob:
        profile_id = "windows-job-object-kill-on-close-v1"
        assurance = "UNAVAILABLE"

        def __init__(self, *args, **kwargs):
            raise ContainmentUnsupported("Windows Job Objects are available only on Windows")

    def wait_pid_exit(pid: int, timeout_seconds: float = 5.0) -> bool:
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            try:
                os.kill(int(pid), 0)
            except ProcessLookupError:
                return True
            except PermissionError:
                return False
            time.sleep(0.05)
        try:
            os.kill(int(pid), 0)
            return False
        except ProcessLookupError:
            return True


def terminate_posix_process_group(process: subprocess.Popen, timeout_seconds: float = 5.0) -> bool:
    """Terminate a process group created with start_new_session=True.

    This is a limited fallback. It is not a substitute for a cgroup-v2
    controller where hostile descendants may create a new session.
    """
    if os.name == "nt":
        raise ContainmentUnsupported("POSIX process groups are unavailable on Windows")
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return True
    try:
        process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            return False
    try:
        os.killpg(process.pid, 0)
    except ProcessLookupError:
        return True
    except PermissionError:
        return False
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        return True
    try:
        process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        return False
    try:
        os.killpg(process.pid, 0)
        return False
    except ProcessLookupError:
        return True
