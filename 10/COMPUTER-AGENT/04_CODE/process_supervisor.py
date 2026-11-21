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
    _kernel32.OpenJobObjectW = ctypes.WinDLL("kernel32", use_last_error=True).OpenJobObjectW
    _kernel32.OpenJobObjectW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
    _kernel32.OpenJobObjectW.restype = wintypes.HANDLE
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

        @classmethod
        def open_existing(cls, name: str):
            handle = _kernel32.OpenJobObjectW(0x0004 | 0x0008, False, name)
            if not handle:
                error = ctypes.get_last_error()
                if error == 2:
                    return None
                raise ContainmentError(f"OpenJobObjectW failed: {error}")
            obj = cls.__new__(cls)
            obj.run_id = "recovered"
            obj.name = name
            obj.handle = handle
            return obj

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

        def spawn_worker(self, command, cwd):
            if self.handle is None:
                raise ContainmentError("job handle is closed")
            return _spawn_process_in_job(self.handle, command, cwd)

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

    # Resume a CREATE_SUSPENDED process only after it has been assigned to
    # its Job Object. Popen closes the original thread handle, so locate the
    # worker's primary thread by owner PID through Toolhelp.
    THREAD_SUSPEND_RESUME = 0x0002
    TH32CS_SNAPTHREAD = 0x00000004

    class _ThreadEntry32(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ThreadID", wintypes.DWORD),
            ("th32OwnerProcessID", wintypes.DWORD),
            ("tpBasePri", wintypes.LONG),
            ("tpDeltaPri", wintypes.LONG),
            ("dwFlags", wintypes.DWORD),
        ]

    _kernel32.CreateToolhelp32Snapshot = ctypes.WinDLL("kernel32", use_last_error=True).CreateToolhelp32Snapshot
    _kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    _kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    _kernel32.Thread32First = ctypes.WinDLL("kernel32", use_last_error=True).Thread32First
    _kernel32.Thread32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(_ThreadEntry32)]
    _kernel32.Thread32First.restype = wintypes.BOOL
    _kernel32.Thread32Next = ctypes.WinDLL("kernel32", use_last_error=True).Thread32Next
    _kernel32.Thread32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(_ThreadEntry32)]
    _kernel32.Thread32Next.restype = wintypes.BOOL
    _kernel32.OpenThread = ctypes.WinDLL("kernel32", use_last_error=True).OpenThread
    _kernel32.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _kernel32.OpenThread.restype = wintypes.HANDLE
    _kernel32.ResumeThread = ctypes.WinDLL("kernel32", use_last_error=True).ResumeThread
    _kernel32.ResumeThread.argtypes = [wintypes.HANDLE]
    _kernel32.ResumeThread.restype = wintypes.DWORD

    def resume_suspended_process(pid: int) -> None:
        snapshot = _kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
        invalid = ctypes.c_void_p(-1).value
        if not snapshot or snapshot == invalid:
            raise ContainmentError(
                f"CreateToolhelp32Snapshot failed: {ctypes.get_last_error()}"
            )
        try:
            entry = _ThreadEntry32()
            entry.dwSize = ctypes.sizeof(entry)
            found = False
            ok = _kernel32.Thread32First(snapshot, ctypes.byref(entry))
            while ok:
                if entry.th32OwnerProcessID == int(pid):
                    thread = _kernel32.OpenThread(
                        THREAD_SUSPEND_RESUME, False, entry.th32ThreadID
                    )
                    if not thread:
                        raise ContainmentError(
                            f"OpenThread failed: {ctypes.get_last_error()}"
                        )
                    try:
                        previous = _kernel32.ResumeThread(thread)
                        if previous == 0xFFFFFFFF:
                            raise ContainmentError(
                                f"ResumeThread failed: {ctypes.get_last_error()}"
                            )
                        if previous != 1:
                            raise ContainmentError(
                                f"unexpected suspend count while resuming PID {pid}: {previous}"
                            )
                        found = True
                        break
                    finally:
                        _kernel32.CloseHandle(thread)
                ok = _kernel32.Thread32Next(snapshot, ctypes.byref(entry))
            if not found:
                raise ContainmentError(f"no suspended primary thread found for PID {pid}")
        finally:
            _kernel32.CloseHandle(snapshot)

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


    class _SecurityAttributes(ctypes.Structure):
        _fields_ = [
            ("nLength", wintypes.DWORD),
            ("lpSecurityDescriptor", ctypes.c_void_p),
            ("bInheritHandle", wintypes.BOOL),
        ]

    class _StartupInfo(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD), ("lpReserved", wintypes.LPWSTR),
            ("lpDesktop", wintypes.LPWSTR), ("lpTitle", wintypes.LPWSTR),
            ("dwX", wintypes.DWORD), ("dwY", wintypes.DWORD),
            ("dwXSize", wintypes.DWORD), ("dwYSize", wintypes.DWORD),
            ("dwXCountChars", wintypes.DWORD), ("dwYCountChars", wintypes.DWORD),
            ("dwFillAttribute", wintypes.DWORD), ("dwFlags", wintypes.DWORD),
            ("wShowWindow", wintypes.WORD), ("cbReserved2", wintypes.WORD),
            ("lpReserved2", ctypes.POINTER(wintypes.BYTE)),
            ("hStdInput", wintypes.HANDLE), ("hStdOutput", wintypes.HANDLE),
            ("hStdError", wintypes.HANDLE),
        ]

    class _StartupInfoEx(ctypes.Structure):
        _fields_ = [("StartupInfo", _StartupInfo), ("lpAttributeList", ctypes.c_void_p)]

    class _ProcessInformation(ctypes.Structure):
        _fields_ = [
            ("hProcess", wintypes.HANDLE), ("hThread", wintypes.HANDLE),
            ("dwProcessId", wintypes.DWORD), ("dwThreadId", wintypes.DWORD),
        ]

    _kernel32.CreatePipe.argtypes = [
        ctypes.POINTER(wintypes.HANDLE), ctypes.POINTER(wintypes.HANDLE),
        ctypes.POINTER(_SecurityAttributes), wintypes.DWORD
    ]
    _kernel32.CreatePipe.restype = wintypes.BOOL
    _kernel32.SetHandleInformation.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD]
    _kernel32.SetHandleInformation.restype = wintypes.BOOL
    _kernel32.InitializeProcThreadAttributeList.argtypes = [
        ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.c_size_t)
    ]
    _kernel32.InitializeProcThreadAttributeList.restype = wintypes.BOOL
    _kernel32.UpdateProcThreadAttribute.argtypes = [
        ctypes.c_void_p, wintypes.DWORD, ctypes.c_size_t, ctypes.c_void_p,
        ctypes.c_size_t, ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)
    ]
    _kernel32.UpdateProcThreadAttribute.restype = wintypes.BOOL
    _kernel32.DeleteProcThreadAttributeList.argtypes = [ctypes.c_void_p]
    _kernel32.DeleteProcThreadAttributeList.restype = None
    _kernel32.CreateProcessW.argtypes = [
        wintypes.LPCWSTR, wintypes.LPWSTR, ctypes.c_void_p, ctypes.c_void_p,
        wintypes.BOOL, wintypes.DWORD, ctypes.c_void_p, wintypes.LPCWSTR,
        ctypes.POINTER(_StartupInfoEx), ctypes.POINTER(_ProcessInformation)
    ]
    _kernel32.CreateProcessW.restype = wintypes.BOOL
    _kernel32.ReadFile.argtypes = [
        wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p
    ]
    _kernel32.ReadFile.restype = wintypes.BOOL
    _kernel32.WriteFile.argtypes = [
        wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p
    ]
    _kernel32.WriteFile.restype = wintypes.BOOL
    _kernel32.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    _kernel32.GetExitCodeProcess.restype = wintypes.BOOL
    _kernel32.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
    _kernel32.TerminateProcess.restype = wintypes.BOOL

    PROC_THREAD_ATTRIBUTE_HANDLE_LIST = 0x00020002
    PROC_THREAD_ATTRIBUTE_JOB_LIST = 0x0002000D
    EXTENDED_STARTUPINFO_PRESENT = 0x00080000
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    CREATE_NO_WINDOW = 0x08000000
    STARTF_USESTDHANDLES = 0x00000100
    HANDLE_FLAG_INHERIT = 0x00000001
    ERROR_BROKEN_PIPE = 109
    ERROR_NO_DATA = 232

    class WindowsContainedProcess:
        """Process created atomically inside a Job Object via JOB_LIST attribute."""

        def __init__(self, process_handle, stdout_handle, stdin_handle, pid):
            self.process_handle = process_handle
            self.stdout_handle = stdout_handle
            self.stdin_handle = stdin_handle
            self.pid = int(pid)
            self.returncode = None
            self.forced_cleanup = False

        def communicate(self, input_text, timeout_seconds, job, cleanup_timeout_seconds, on_gate_released=None):
            import threading
            output = bytearray()
            read_errors = []
            reader_done = threading.Event()

            def read_output():
                try:
                    while True:
                        buffer = ctypes.create_string_buffer(65536)
                        count = wintypes.DWORD(0)
                        ok = _kernel32.ReadFile(
                            self.stdout_handle, buffer, len(buffer), ctypes.byref(count), None
                        )
                        if not ok:
                            error = ctypes.get_last_error()
                            if error in (ERROR_BROKEN_PIPE, ERROR_NO_DATA):
                                break
                            read_errors.append(f"ReadFile failed: {error}")
                            break
                        if count.value == 0:
                            break
                        output.extend(buffer.raw[:count.value])
                        if len(output) > 2 * 1024 * 1024:
                            read_errors.append("worker output exceeded 2 MiB limit")
                            try:
                                job.terminate()
                            except Exception:
                                pass
                            break
                finally:
                    reader_done.set()

            reader = threading.Thread(target=read_output, name="w10-worker-output", daemon=True)
            reader.start()
            timed_out = False
            try:
                payload = input_text.encode("utf-8")
                offset = 0
                while offset < len(payload):
                    chunk = payload[offset:]
                    buffer = ctypes.create_string_buffer(chunk)
                    written = wintypes.DWORD(0)
                    ok = _kernel32.WriteFile(
                        self.stdin_handle, buffer, len(chunk), ctypes.byref(written), None
                    )
                    if not ok or written.value == 0:
                        raise ContainmentError(
                            f"WriteFile(worker stdin) failed: {ctypes.get_last_error()}"
                        )
                    offset += written.value
            finally:
                if self.stdin_handle:
                    _kernel32.CloseHandle(self.stdin_handle)
                    self.stdin_handle = None
            if on_gate_released is not None:
                on_gate_released()

            wait_ms = max(0, int(float(timeout_seconds) * 1000))
            wait_result = _kernel32.WaitForSingleObject(self.process_handle, wait_ms)
            if wait_result == WAIT_TIMEOUT:
                timed_out = True
                job.terminate()
                cleanup_wait = _kernel32.WaitForSingleObject(
                    self.process_handle, max(0, int(float(cleanup_timeout_seconds) * 1000))
                )
                if cleanup_wait == WAIT_TIMEOUT:
                    _kernel32.TerminateProcess(self.process_handle, 1)
                    _kernel32.WaitForSingleObject(
                        self.process_handle, max(0, int(float(cleanup_timeout_seconds) * 1000))
                    )
            elif wait_result != WAIT_OBJECT_0:
                raise ContainmentError(
                    f"WaitForSingleObject(worker) failed: {ctypes.get_last_error()}"
                )

            # Give the OS a short grace period to retire the signaled worker
            # from Job Object accounting. If stdout remains open, a descendant
            # may still hold the pipe; then fail closed and terminate the job.
            reader.join(min(1.0, float(cleanup_timeout_seconds)))
            if reader.is_alive():
                self.forced_cleanup = True
                job.terminate()
                reader.join(float(cleanup_timeout_seconds) + 2.0)
            if reader.is_alive():
                raise ContainmentError("worker output pipe did not close after Job Object termination")
            exit_code = wintypes.DWORD(0)
            if not _kernel32.GetExitCodeProcess(self.process_handle, ctypes.byref(exit_code)):
                raise ContainmentError(
                    f"GetExitCodeProcess failed: {ctypes.get_last_error()}"
                )
            self.returncode = int(exit_code.value)
            if read_errors:
                raise ContainmentError("; ".join(read_errors))
            return bytes(output).decode("utf-8", errors="replace"), timed_out, self.returncode

        def wait(self, timeout_seconds=5.0):
            result = _kernel32.WaitForSingleObject(
                self.process_handle, max(0, int(float(timeout_seconds) * 1000))
            )
            if result != WAIT_OBJECT_0:
                raise ContainmentError("worker process did not exit within cleanup deadline")
            code = wintypes.DWORD(0)
            if not _kernel32.GetExitCodeProcess(self.process_handle, ctypes.byref(code)):
                raise ContainmentError(f"GetExitCodeProcess failed: {ctypes.get_last_error()}")
            self.returncode = int(code.value)
            return self.returncode

        def close(self):
            for attr in ("stdin_handle", "stdout_handle", "process_handle"):
                handle = getattr(self, attr)
                if handle:
                    _kernel32.CloseHandle(handle)
                    setattr(self, attr, None)

    def _spawn_process_in_job(job_handle, command, cwd):
        import subprocess
        if not command:
            raise ContainmentError("worker command is empty")
        sa = _SecurityAttributes()
        sa.nLength = ctypes.sizeof(sa)
        sa.lpSecurityDescriptor = None
        sa.bInheritHandle = True
        stdin_read = wintypes.HANDLE()
        stdin_write = wintypes.HANDLE()
        stdout_read = wintypes.HANDLE()
        stdout_write = wintypes.HANDLE()
        attr_buffer = None
        attr_list = None
        process_info = _ProcessInformation()
        try:
            if not _kernel32.CreatePipe(ctypes.byref(stdin_read), ctypes.byref(stdin_write), ctypes.byref(sa), 0):
                raise ContainmentError(f"CreatePipe(stdin) failed: {ctypes.get_last_error()}")
            if not _kernel32.CreatePipe(ctypes.byref(stdout_read), ctypes.byref(stdout_write), ctypes.byref(sa), 0):
                raise ContainmentError(f"CreatePipe(stdout) failed: {ctypes.get_last_error()}")
            if not _kernel32.SetHandleInformation(stdin_write, HANDLE_FLAG_INHERIT, 0):
                raise ContainmentError(f"SetHandleInformation(stdin) failed: {ctypes.get_last_error()}")
            if not _kernel32.SetHandleInformation(stdout_read, HANDLE_FLAG_INHERIT, 0):
                raise ContainmentError(f"SetHandleInformation(stdout) failed: {ctypes.get_last_error()}")

            size = ctypes.c_size_t(0)
            _kernel32.InitializeProcThreadAttributeList(None, 2, 0, ctypes.byref(size))
            attr_buffer = ctypes.create_string_buffer(size.value)
            attr_list = ctypes.cast(attr_buffer, ctypes.c_void_p)
            if not _kernel32.InitializeProcThreadAttributeList(attr_list, 2, 0, ctypes.byref(size)):
                raise ContainmentError(
                    f"InitializeProcThreadAttributeList failed: {ctypes.get_last_error()}"
                )

            job_handles = (wintypes.HANDLE * 1)(job_handle)
            inherited_handles = (wintypes.HANDLE * 2)(stdin_read, stdout_write)
            if not _kernel32.UpdateProcThreadAttribute(
                attr_list, 0, PROC_THREAD_ATTRIBUTE_JOB_LIST,
                ctypes.cast(job_handles, ctypes.c_void_p), ctypes.sizeof(job_handles), None, None
            ):
                raise ContainmentError(
                    f"UpdateProcThreadAttribute(JOB_LIST) failed: {ctypes.get_last_error()}"
                )
            if not _kernel32.UpdateProcThreadAttribute(
                attr_list, 0, PROC_THREAD_ATTRIBUTE_HANDLE_LIST,
                ctypes.cast(inherited_handles, ctypes.c_void_p), ctypes.sizeof(inherited_handles), None, None
            ):
                raise ContainmentError(
                    f"UpdateProcThreadAttribute(HANDLE_LIST) failed: {ctypes.get_last_error()}"
                )

            startup = _StartupInfoEx()
            startup.StartupInfo.cb = ctypes.sizeof(_StartupInfoEx)
            startup.StartupInfo.dwFlags = STARTF_USESTDHANDLES
            startup.StartupInfo.hStdInput = stdin_read
            startup.StartupInfo.hStdOutput = stdout_write
            startup.StartupInfo.hStdError = stdout_write
            startup.lpAttributeList = attr_list
            command_line = ctypes.create_unicode_buffer(subprocess.list2cmdline(command))
            flags = EXTENDED_STARTUPINFO_PRESENT | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW
            ok = _kernel32.CreateProcessW(
                command[0], command_line, None, None, True, flags, None, str(cwd),
                ctypes.byref(startup), ctypes.byref(process_info)
            )
            if not ok:
                raise ContainmentError(f"CreateProcessW in Job Object failed: {ctypes.get_last_error()}")

            # Parent closes child-side handles; the worker owns its inherited copies.
            _kernel32.CloseHandle(stdin_read)
            stdin_read = None
            _kernel32.CloseHandle(stdout_write)
            stdout_write = None
            _kernel32.CloseHandle(process_info.hThread)
            process_info.hThread = None
            process = WindowsContainedProcess(
                process_info.hProcess, stdout_read, stdin_write, process_info.dwProcessId
            )
            process_info.hProcess = None
            stdout_read = stdin_write = None
            return process
        finally:
            if attr_list:
                _kernel32.DeleteProcThreadAttributeList(attr_list)
            for handle in (stdin_read, stdin_write, stdout_read, stdout_write,
                           process_info.hThread, process_info.hProcess):
                if handle:
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

    The leader may exit before an orphaned descendant has been reaped by init.
    Therefore, after SIGKILL, poll the process-group identity until the bounded
    deadline instead of treating the first post-kill killpg(0) probe as final.
    This remains a limited fallback, not a cgroup-v2 containment guarantee.
    """
    if os.name == "nt":
        raise ContainmentUnsupported("POSIX process groups are unavailable on Windows")
    pgid = process.pid
    deadline = time.monotonic() + max(0.1, float(timeout_seconds))

    def group_exists() -> bool | None:
        try:
            os.killpg(pgid, 0)
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            return None

    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        try:
            process.wait(timeout=max(0.0, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            return False
        return True

    # Give cooperative members a short bounded grace period. The group may
    # outlive its leader, so leader exit alone is never treated as empty.
    grace_deadline = min(deadline, time.monotonic() + 0.25)
    while time.monotonic() < grace_deadline:
        try:
            process.wait(timeout=min(0.05, max(0.001, grace_deadline - time.monotonic())))
        except subprocess.TimeoutExpired:
            pass
        exists = group_exists()
        if exists is False:
            return process.poll() is not None
        if exists is None:
            return False
        time.sleep(0.02)

    # Kill any remaining descendants, including a group whose leader already
    # exited. Keep checking until the group disappears or the deadline expires.
    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except PermissionError:
        return False

    try:
        process.wait(timeout=max(0.0, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        return False

    while time.monotonic() < deadline:
        exists = group_exists()
        if exists is False:
            return True
        if exists is None:
            return False
        try:
            os.killpg(pgid, signal.SIGKILL)
        except ProcessLookupError:
            return True
        except PermissionError:
            return False
        time.sleep(0.05)

    return group_exists() is False

def _utc_now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _atomic_json(path, payload) -> None:
    import json
    from pathlib import Path
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


class HostOwnerLease:
    """Exclusive host owner lock with monotonically increasing generation."""

    def __init__(self, work_root):
        from pathlib import Path
        self.work_root = Path(work_root).resolve()
        self.evidence_dir = self.work_root / "06_EVIDENCE"
        self.lock_path = self.evidence_dir / ".computer-agent-owner.lock"
        self.state_path = self.evidence_dir / "computer-agent-owner-state.json"
        self._file = None
        self.generation = 0
        self.previous_owner = None

    @staticmethod
    def _pid_alive(pid: int) -> bool:
        if not pid:
            return False
        if os.name == "nt":
            return not wait_pid_exit(pid, timeout_seconds=0)
        try:
            os.kill(int(pid), 0)
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            return True

    def acquire(self):
        import json
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self._file = open(self.lock_path, "a+b")
        self._file.seek(0, os.SEEK_END)
        if self._file.tell() == 0:
            self._file.write(b"\0")
            self._file.flush()
        self._file.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self._file.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self._file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            self._file.close()
            self._file = None
            raise ContainmentError("another Computer Agent owner still holds the host lease") from exc

        previous = {}
        if self.state_path.exists():
            try:
                previous = json.loads(self.state_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                self._unlock_only()
                raise ContainmentError("host owner state is unreadable; refusing to take ownership")
        previous_pid = int(previous.get("pid") or 0)
        if previous.get("state") == "ACTIVE" and self._pid_alive(previous_pid):
            self._unlock_only()
            raise ContainmentError(
                f"previous owner PID {previous_pid} is still alive; fencing is not proven"
            )
        self.previous_owner = previous or None
        self.generation = int(previous.get("owner_generation", 0)) + 1
        try:
            self._recover_stale_runs()
        except Exception:
            self._unlock_only()
            raise
        self._write_state("ACTIVE")
        return self

    def _recover_stale_runs(self):
        import json
        runs_dir = self.evidence_dir / "process-runs"
        if not runs_dir.exists():
            return
        for journal_path in sorted(runs_dir.glob("*.json")):
            try:
                record = json.loads(journal_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise ContainmentError(f"unreadable process journal {journal_path.name}") from exc
            detail = record.get("detail") or {}
            if record.get("state") == "RECONCILED_EMPTY" or detail.get("containment_empty_verified") is True:
                continue
            profile = record.get("profile_id", "")
            locator = record.get("containment_locator", "")
            worker_pid = int(record.get("worker_pid") or 0)
            empty = False
            if profile.startswith("windows-job-object"):
                job = WindowsJob.open_existing(locator) if os.name == "nt" and locator else None
                if job is not None:
                    try:
                        job.terminate()
                        deadline = time.monotonic() + 5.0
                        while time.monotonic() < deadline and job.active_processes():
                            time.sleep(0.05)
                        empty = job.active_processes() == 0
                    finally:
                        job.close()
                else:
                    # A missing named job means its last handle closed. With
                    # KILL_ON_JOB_CLOSE, members are terminated. A live worker
                    # PID without its job locator is an unresolved spawn race.
                    if worker_pid and self._pid_alive(worker_pid):
                        raise ContainmentError(
                            f"orphan worker PID {worker_pid} is alive but its Job Object is absent"
                        )
                    empty = True
            elif profile.startswith("posix-process-group"):
                if os.name == "nt":
                    raise ContainmentError("POSIX process journal found on Windows host")
                if worker_pid:
                    try:
                        os.killpg(worker_pid, 0)
                    except ProcessLookupError:
                        empty = True
                    else:
                        # PID/PGID alone is insufficient to prove identity after
                        # a broker crash; do not risk killing a reused process group.
                        raise ContainmentError(
                            f"stale POSIX process group {worker_pid} still exists; "
                            "PID-only identity is insufficient for safe recovery"
                        )
                else:
                    empty = True
            else:
                raise ContainmentError(
                    f"unknown containment profile in stale journal {journal_path.name}: {profile}"
                )
            if not empty:
                raise ContainmentError(
                    f"stale process containment could not be reconciled: {journal_path.name}"
                )
            record["state"] = "RECOVERED_EMPTY"
            record["recovered_by_owner_generation"] = self.generation
            record["recovered_at"] = _utc_now()
            _atomic_json(journal_path, record)

    def _write_state(self, state: str):
        payload = {
            "work_id": "10",
            "owner_generation": self.generation,
            "pid": os.getpid(),
            "state": state,
            "updated_at": _utc_now(),
            "previous_owner": self.previous_owner,
        }
        if state == "ACTIVE":
            payload["started_at"] = payload["updated_at"]
        else:
            payload["ended_at"] = payload["updated_at"]
        _atomic_json(self.state_path, payload)

    def _unlock_only(self):
        if self._file is None:
            return
        try:
            if os.name == "nt":
                import msvcrt
                self._file.seek(0)
                msvcrt.locking(self._file.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self._file.fileno(), fcntl.LOCK_UN)
        finally:
            self._file.close()
            self._file = None

    def release(self):
        if self._file is None:
            return
        try:
            self._write_state("RELEASED")
        finally:
            self._unlock_only()


class ProcessSupervisor:
    """Run one workflow in an OS-contained worker process.

    Windows is accepted only when CreateProcessW atomically places the worker
    in a named Job Object through PROC_THREAD_ATTRIBUTE_JOB_LIST. POSIX process groups are
    a limited test/development profile; production Linux remains fail-closed
    unless an explicit limited-profile override is supplied.
    """

    def __init__(self, work_root, owner_generation: int = 0, cleanup_timeout_seconds: float = 5.0):
        from pathlib import Path
        self.work_root = Path(work_root).resolve()
        self.owner_generation = int(owner_generation)
        self.cleanup_timeout_seconds = float(cleanup_timeout_seconds)
        self.worker_path = Path(__file__).with_name("execution_worker.py")

    def execute(self, request: dict, timeout_seconds: float) -> dict:
        if os.name == "nt":
            return self._execute_windows(request, timeout_seconds)
        if os.name == "posix":
            if os.getenv("COMPUTER_AGENT_ALLOW_LIMITED_PROCESS_GROUP") != "1":
                return self._blocked(request, "linux_cgroup_v2_required",
                                     "Linux hardened profile requires cgroup-v2; limited process-group mode is disabled")
            return self._execute_posix(request, timeout_seconds)
        return self._blocked(request, "containment_unsupported",
                             f"unsupported OS family: {os.name}")

    def _journal_path(self, run_id: str):
        return self.work_root / "06_EVIDENCE" / "process-runs" / f"{run_id}.json"

    def _journal(self, path, run_id, state, profile, locator, pid=None, detail=None):
        payload = {
            "work_id": "10",
            "run_id": run_id,
            "owner_generation": self.owner_generation,
            "owner_pid": os.getpid(),
            "worker_pid": pid,
            "profile_id": profile,
            "containment_locator": locator,
            "state": state,
            "updated_at": _utc_now(),
            "detail": detail,
        }
        _atomic_json(path, payload)

    def _blocked(self, request, code: str, detail: str) -> dict:
        now = _utc_now()
        return {
            "status": "BLOCKED",
            "task": request.get("task", ""),
            "steps": [],
            "evidence": [{
                "action": "process_supervisor",
                "status": "blocked",
                "ok": False,
                "error_code": code,
                "detail": detail,
                "timestamp": now,
                "owner_generation": self.owner_generation,
            }],
            "error": f"{code}: {detail}",
            "state_trace": ["PLANNED", "RUNNING", "VERIFYING", "BLOCKED"],
            "work_id": request.get("work_id", "10"),
            "started_at": now,
            "finished_at": now,
            "policy": request.get("policy"),
        }

    @staticmethod
    def _add_supervisor_evidence(result, evidence):
        if not isinstance(result, dict):
            return
        result.setdefault("evidence", []).append(evidence)

    @staticmethod
    def _worker_result(stdout: str, request_id: str):
        import json
        try:
            response = json.loads((stdout or "").strip().splitlines()[-1])
        except (IndexError, json.JSONDecodeError):
            return None, "worker_response_invalid"
        if response.get("request_id") != request_id:
            return None, "worker_request_id_mismatch"
        if not isinstance(response.get("result"), dict):
            return None, response.get("error") or "worker_result_missing"
        return response, None

    def _execute_windows(self, request: dict, timeout_seconds: float) -> dict:
        import json
        import uuid
        run_id = str(uuid.uuid4())
        profile = "windows-job-object-kill-on-close-v1"
        job = None
        proc = None
        journal = self._journal_path(run_id)
        locator = "Local\\Work10Job-" + run_id
        active_after = None
        empty_verified = False
        cleanup_action = "none"
        forced_cleanup = False
        stdout = ""
        request_id = str(uuid.uuid4())
        envelope = dict(request)
        envelope["request_id"] = request_id
        try:
            job = WindowsJob(run_id)
            locator = job.name
            self._journal(journal, run_id, "CONTAINMENT_CREATED", profile, locator)
            self._journal(journal, run_id, "SPAWN_INTENT_DURABLE", profile, locator)
            # PROC_THREAD_ATTRIBUTE_JOB_LIST places the worker in the Job Object
            # atomically at process creation, before its first instruction.
            proc = job.spawn_worker([sys.executable, str(self.worker_path)], self.work_root)
            self._journal(journal, run_id, "PROCESS_IDENTITY_DURABLE", profile, locator, proc.pid)
            self._journal(journal, run_id, "GATE_RELEASE_INTENT_DURABLE", profile, locator, proc.pid)
            def mark_gate_released():
                self._journal(journal, run_id, "GATE_RELEASED", profile, locator, proc.pid)
                self._journal(journal, run_id, "RUNNING_DURABLE", profile, locator, proc.pid)
            stdout, timed_out, exit_code = proc.communicate(
                json.dumps(envelope, ensure_ascii=False) + "\n",
                float(timeout_seconds), job, self.cleanup_timeout_seconds,
                on_gate_released=mark_gate_released,
            )
            forced_cleanup = bool(proc.forced_cleanup)
            if timed_out:
                cleanup_action = "TERMINATE_JOB_ON_WORKFLOW_TIMEOUT"
                forced_cleanup = True
                result = self._blocked(
                    request, "workflow_timeout_contained",
                    "parent deadline expired; Job Object termination completed"
                )
            else:
                response, parse_error = self._worker_result(stdout, request_id)
                if parse_error:
                    cleanup_action = "TERMINATE_JOB_ON_INVALID_WORKER_RESULT"
                    forced_cleanup = True
                    job.terminate()
                    result = self._blocked(request, parse_error, "")
                else:
                    result = response["result"]
                    if response.get("cleanup_pending"):
                        cleanup_action = "TERMINATE_JOB_ON_UNCERTAIN_WORKER"
                        forced_cleanup = True
                        job.terminate()
                    if exit_code != 0 and result.get("status") != "BLOCKED":
                        forced_cleanup = True
                        result["status"] = "BLOCKED"
                        result["error"] = (result.get("error") or "") + "; worker exited nonzero"

            active_after = job.active_processes()
            if active_after:
                # Allow a short OS accounting grace after worker exit before
                # deciding that a descendant leaked from an otherwise clean run.
                grace_deadline = time.monotonic() + min(0.75, self.cleanup_timeout_seconds)
                while active_after and time.monotonic() < grace_deadline:
                    time.sleep(0.05)
                    active_after = job.active_processes()
            if active_after:
                forced_cleanup = True
                if cleanup_action == "none":
                    cleanup_action = "TERMINATE_REMAINING_JOB_MEMBERS"
                job.terminate()
                deadline = time.monotonic() + self.cleanup_timeout_seconds
                while time.monotonic() < deadline and job.active_processes():
                    time.sleep(0.05)
                active_after = job.active_processes()
            empty_verified = active_after == 0
            if not empty_verified or forced_cleanup:
                result["status"] = "BLOCKED"
                reason = (
                    "Job Object containment not empty after cleanup" if not empty_verified
                    else "forced termination was required to reconcile the Job Object"
                )
                result["error"] = (result.get("error") or "") + "; " + reason
                if not result.get("state_trace") or result["state_trace"][-1] != "BLOCKED":
                    result.setdefault("state_trace", []).append("BLOCKED")

            evidence = {
                "action": "process_supervisor",
                "status": "success" if empty_verified and not forced_cleanup else "blocked",
                "ok": empty_verified and not forced_cleanup,
                "profile_id": profile,
                "assurance": "OS_JOB_OBJECT_ATOMIC_JOB_LIST",
                "run_id": run_id,
                "worker_pid": proc.pid if proc else None,
                "containment_locator": locator,
                "owner_generation": self.owner_generation,
                "cleanup_action": cleanup_action,
                "forced_cleanup": forced_cleanup,
                "active_processes_after_cleanup": active_after,
                "containment_empty_verified": empty_verified,
                "timestamp": _utc_now(),
            }
            self._add_supervisor_evidence(result, evidence)
            self._journal(
                journal, run_id,
                "RECONCILED_EMPTY" if empty_verified and not forced_cleanup else "BLOCKED",
                profile, locator, proc.pid if proc else None, evidence
            )
            return result
        except Exception as exc:
            cleanup_action = "TERMINATE_JOB_ON_SUPERVISOR_ERROR"
            if job is not None:
                try:
                    job.terminate()
                except Exception:
                    pass
            if proc is not None:
                try:
                    proc.wait(timeout_seconds=self.cleanup_timeout_seconds)
                except Exception:
                    pass
            result = self._blocked(request, "supervisor_error", f"{type(exc).__name__}: {exc}")
            evidence = {
                "action": "process_supervisor", "status": "blocked", "ok": False,
                "profile_id": profile, "run_id": run_id, "containment_locator": locator,
                "worker_pid": proc.pid if proc else None, "cleanup_action": cleanup_action,
                "containment_empty_verified": False, "timestamp": _utc_now(),
            }
            self._add_supervisor_evidence(result, evidence)
            try:
                self._journal(journal, run_id, "BLOCKED", profile, locator,
                              proc.pid if proc else None, evidence)
            except Exception:
                pass
            return result
        finally:
            if proc is not None:
                try:
                    proc.close()
                except Exception:
                    pass
            if job is not None:
                try:
                    job.close()
                except Exception:
                    pass

    def _execute_posix(self, request: dict, timeout_seconds: float) -> dict:
        import json
        import subprocess
        import uuid
        run_id = str(uuid.uuid4())
        profile = "posix-process-group-limited-v1"
        proc = None
        journal = self._journal_path(run_id)
        locator = f"pgid:{run_id}"
        cleanup_action = "none"
        forced_cleanup = False
        stdout = stderr = ""
        request_id = str(uuid.uuid4())
        envelope = dict(request)
        envelope["request_id"] = request_id
        try:
            self._journal(journal, run_id, "SPAWN_INTENT_DURABLE", profile, locator)
            proc = subprocess.Popen(
                [sys.executable, str(self.worker_path)],
                cwd=str(self.work_root), stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding="utf-8", errors="replace",
                start_new_session=True,
            )
            locator = f"pgid:{proc.pid}"
            self._journal(journal, run_id, "PROCESS_IDENTITY_DURABLE", profile, locator, proc.pid)
            self._journal(journal, run_id, "GATE_RELEASE_INTENT_DURABLE", profile, locator, proc.pid)
            proc.stdin.write(json.dumps(envelope, ensure_ascii=False) + "\n")
            proc.stdin.flush()
            self._journal(journal, run_id, "GATE_RELEASED", profile, locator, proc.pid)
            self._journal(journal, run_id, "RUNNING_DURABLE", profile, locator, proc.pid)
            try:
                stdout, stderr = proc.communicate(timeout=float(timeout_seconds))
            except subprocess.TimeoutExpired:
                cleanup_action = "KILL_PROCESS_GROUP_ON_WORKFLOW_TIMEOUT"
                forced_cleanup = True
                empty_verified = terminate_posix_process_group(proc, self.cleanup_timeout_seconds)
                result = self._blocked(request, "workflow_timeout_contained",
                                       "parent deadline expired; process-group termination requested")
                response = None
            else:
                response, parse_error = self._worker_result(stdout, request_id)
                if parse_error:
                    cleanup_action = "KILL_PROCESS_GROUP_ON_INVALID_WORKER_RESULT"
                    forced_cleanup = True
                    empty_verified = terminate_posix_process_group(proc, self.cleanup_timeout_seconds)
                    result = self._blocked(request, parse_error, (stderr or "")[-2000:])
                else:
                    result = response["result"]
                    if response.get("cleanup_pending"):
                        cleanup_action = "KILL_PROCESS_GROUP_ON_UNCERTAIN_WORKER"
                        forced_cleanup = True
                        empty_verified = terminate_posix_process_group(proc, self.cleanup_timeout_seconds)
                    else:
                        try:
                            os.killpg(proc.pid, 0)
                            cleanup_action = "KILL_REMAINING_PROCESS_GROUP_MEMBERS"
                            forced_cleanup = True
                            empty_verified = terminate_posix_process_group(proc, self.cleanup_timeout_seconds)
                        except ProcessLookupError:
                            empty_verified = True
                        except PermissionError:
                            empty_verified = False
            if not empty_verified or forced_cleanup:
                result["status"] = "BLOCKED"
                reason = ("process group not proven empty" if not empty_verified
                          else "forced process-group termination was required")
                result["error"] = (result.get("error") or "") + "; " + reason
                if not result.get("state_trace") or result["state_trace"][-1] != "BLOCKED":
                    result.setdefault("state_trace", []).append("BLOCKED")
            evidence = {
                "action": "process_supervisor", "status": "success" if empty_verified else "blocked",
                "ok": empty_verified, "profile_id": profile,
                "assurance": "LIMITED_NOT_CGROUP_V2", "run_id": run_id,
                "worker_pid": proc.pid, "containment_locator": locator,
                "owner_generation": self.owner_generation, "cleanup_action": cleanup_action,
                "forced_cleanup": forced_cleanup,
                "containment_empty_verified": empty_verified, "stderr_tail": (stderr or "")[-1000:],
                "timestamp": _utc_now(),
            }
            self._add_supervisor_evidence(result, evidence)
            self._journal(journal, run_id, "RECONCILED_EMPTY" if empty_verified else "BLOCKED",
                          profile, locator, proc.pid, evidence)
            return result
        except Exception as exc:
            if proc is not None:
                try:
                    terminate_posix_process_group(proc, self.cleanup_timeout_seconds)
                except Exception:
                    pass
            result = self._blocked(request, "supervisor_error", f"{type(exc).__name__}: {exc}")
            self._add_supervisor_evidence(result, {
                "action": "process_supervisor", "status": "blocked", "ok": False,
                "profile_id": profile, "run_id": run_id, "containment_locator": locator,
                "worker_pid": proc.pid if proc else None, "assurance": "LIMITED_NOT_CGROUP_V2",
                "containment_empty_verified": False, "timestamp": _utc_now(),
            })
            try:
                self._journal(journal, run_id, "BLOCKED", profile, locator,
                              proc.pid if proc else None, result["evidence"][-1])
            except Exception:
                pass
            return result
        finally:
            if proc is not None:
                for stream in (proc.stdin, proc.stdout, proc.stderr):
                    try:
                        if stream:
                            stream.close()
                    except Exception:
                        pass
