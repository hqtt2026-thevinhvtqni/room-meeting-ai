import importlib.util
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from execution_host import process_job as candidate_process_job

ManagedProcess = candidate_process_job.ManagedProcess
_wait_job_drained = candidate_process_job._wait_job_drained


class FakeProcess:
    pid = 12345

    def poll(self):
        return None


class FakeJob:
    handle = 1

    def close(self):
        self.handle = 0


def test_windows_job_membership_unavailable_remains_unknown():
    managed = ManagedProcess(
        process=FakeProcess(),
        platform="win32",
        created_via_spawn=True,
        job_object="ATTACHED",
        _job=object(),
    )
    with patch.object(candidate_process_job, "_job_active_processes", return_value=None):
        assert managed.members_count() is None


def test_job_drain_query_failure_is_not_success():
    notes = []
    with patch.object(candidate_process_job, "_job_active_processes", return_value=None):
        assert _wait_job_drained(object(), timeout=0.0, notes=notes) is False
    assert "job_member_count_unavailable_fail_closed" in notes


def test_windows_spawn_assigns_job_before_resuming_user_process():
    events = []
    job = FakeJob()
    process = FakeProcess()

    def fake_popen(args, **kwargs):
        events.append(("create", kwargs.get("creationflags")))
        return process

    def fake_assign(_job, pid):
        events.append(("assign", pid))
        return ["job_object_assigned"]

    def fake_resume(pid):
        events.append(("resume", pid))
        return ["resumed_threads=1"], True

    with (
        patch.object(candidate_process_job, "_is_windows", return_value=True),
        patch.object(candidate_process_job, "_create_job_object", return_value=(job, [])),
        patch.object(candidate_process_job.subprocess, "Popen", side_effect=fake_popen),
        patch.object(candidate_process_job, "_assign_pid_to_job", side_effect=fake_assign),
        patch.object(candidate_process_job, "_resume_suspended_process", side_effect=fake_resume),
    ):
        managed = candidate_process_job._spawn(
            ["candidate-child"],
            cwd=".",
            env={},
            text=True,
            stdout=None,
            stderr=None,
        )

    assert events == [
        ("create", candidate_process_job._CREATE_SUSPENDED),
        ("assign", process.pid),
        ("resume", process.pid),
    ]
    assert managed.job_object == "ATTACHED"
    assert managed._job is job


def test_windows_spawn_never_resumes_when_job_assignment_fails():
    events = []
    job = FakeJob()
    process = FakeProcess()

    def fake_popen(args, **kwargs):
        events.append(("create", kwargs.get("creationflags")))
        return process

    def fake_assign(_job, pid):
        events.append(("assign_failed", pid))
        return ["AssignProcessToJobObject_failed_err=5"]

    def fake_abort(_process, _job, notes, *, assigned):
        events.append(("abort", assigned))
        notes.append("suspended_process_terminated_never_resumed")
        return True

    def forbidden_resume(pid):
        events.append(("UNEXPECTED_RESUME", pid))
        return ["unexpected"], True

    with (
        patch.object(candidate_process_job, "_is_windows", return_value=True),
        patch.object(candidate_process_job, "_create_job_object", return_value=(job, [])),
        patch.object(candidate_process_job.subprocess, "Popen", side_effect=fake_popen),
        patch.object(candidate_process_job, "_assign_pid_to_job", side_effect=fake_assign),
        patch.object(candidate_process_job, "_abort_suspended", side_effect=fake_abort),
        patch.object(candidate_process_job, "_resume_suspended_process", side_effect=forbidden_resume),
    ):
        try:
            candidate_process_job._spawn(
                ["candidate-child"],
                cwd=".",
                env={},
                text=True,
                stdout=None,
                stderr=None,
            )
        except candidate_process_job.JobObjectUnavailable as exc:
            assert exc.process_reaped is True
        else:
            raise AssertionError("expected JobObjectUnavailable")

    assert events == [
        ("create", candidate_process_job._CREATE_SUSPENDED),
        ("assign_failed", process.pid),
        ("abort", False),
    ]
    assert not any(event[0] == "UNEXPECTED_RESUME" for event in events)


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="requires native Windows Job Object")
def test_native_windows_child_cannot_execute_before_job_assignment(tmp_path):
    marker = tmp_path / "child-started.txt"
    script = f"from pathlib import Path; Path({str(marker)!r}).write_text('started', encoding='utf-8')"
    events = []
    real_assign = candidate_process_job._assign_pid_to_job
    real_resume = candidate_process_job._resume_suspended_process

    def observed_assign(job, pid):
        assert not marker.exists(), "child code ran before Job Object assignment"
        events.append("assign_begin")
        notes = real_assign(job, pid)
        assert "job_object_assigned" in notes, notes
        events.append("assigned")
        assert not marker.exists(), "child code ran before ResumeThread"
        return notes

    def observed_resume(pid):
        assert events == ["assign_begin", "assigned"]
        assert not marker.exists(), "child code ran before ResumeThread"
        events.append("resume")
        return real_resume(pid)

    with (
        patch.object(candidate_process_job, "_assign_pid_to_job", side_effect=observed_assign),
        patch.object(candidate_process_job, "_resume_suspended_process", side_effect=observed_resume),
    ):
        managed = candidate_process_job.spawn_managed(
            [sys.executable, "-c", script],
            cwd=tmp_path,
            env=os.environ.copy(),
        )

    try:
        assert events == ["assign_begin", "assigned", "resume"]
        managed.process.wait(timeout=10)
        assert marker.is_file(), "child did not execute after successful resume"
    finally:
        managed.cleanup(terminate_first=True, wait_timeout=5.0)


def test_windows_job_creation_failure_starts_no_process():
    events = []

    def forbidden_popen(*args, **kwargs):
        events.append("UNEXPECTED_PROCESS_CREATE")
        raise AssertionError("Popen must not run when Job creation fails")

    with (
        patch.object(candidate_process_job, "_is_windows", return_value=True),
        patch.object(candidate_process_job, "_create_job_object", return_value=(None, ["CreateJobObjectW_failed_err=5"])),
        patch.object(candidate_process_job.subprocess, "Popen", side_effect=forbidden_popen),
    ):
        try:
            candidate_process_job._spawn(
                ["candidate-child"], cwd=".", env={}, text=True,
                stdout=None, stderr=None,
            )
        except candidate_process_job.JobObjectUnavailable as exc:
            assert exc.process_reaped is True
        else:
            raise AssertionError("expected JobObjectUnavailable")

    assert events == []


def test_windows_resume_failure_aborts_assigned_suspended_process():
    events = []
    job = FakeJob()
    process = FakeProcess()

    def fake_popen(args, **kwargs):
        events.append(("create", kwargs.get("creationflags")))
        return process

    def fake_assign(_job, pid):
        events.append(("assign", pid))
        return ["job_object_assigned"]

    def fake_resume(pid):
        events.append(("resume_failed", pid))
        return ["ResumeThread_failed_err=5"], False

    def fake_abort(_process, _job, notes, *, assigned):
        events.append(("abort", assigned))
        notes.append("suspended_process_terminated_never_resumed")
        return True

    with (
        patch.object(candidate_process_job, "_is_windows", return_value=True),
        patch.object(candidate_process_job, "_create_job_object", return_value=(job, [])),
        patch.object(candidate_process_job.subprocess, "Popen", side_effect=fake_popen),
        patch.object(candidate_process_job, "_assign_pid_to_job", side_effect=fake_assign),
        patch.object(candidate_process_job, "_resume_suspended_process", side_effect=fake_resume),
        patch.object(candidate_process_job, "_abort_suspended", side_effect=fake_abort),
    ):
        try:
            candidate_process_job._spawn(
                ["candidate-child"], cwd=".", env={}, text=True,
                stdout=None, stderr=None,
            )
        except candidate_process_job.JobObjectUnavailable as exc:
            assert exc.process_reaped is True
        else:
            raise AssertionError("expected JobObjectUnavailable")

    assert events == [
        ("create", candidate_process_job._CREATE_SUSPENDED),
        ("assign", process.pid),
        ("resume_failed", process.pid),
        ("abort", True),
    ]


def test_spawn_managed_service_uses_same_fail_closed_spawn_path():
    sentinel = object()
    with patch.object(candidate_process_job, "_spawn", return_value=sentinel) as spawn:
        result = candidate_process_job.spawn_managed_service(
            ["service"], cwd=".", env={},
        )
    assert result is sentinel
    kwargs = spawn.call_args.kwargs
    assert kwargs["text"] is None
    assert kwargs["stdout"] == candidate_process_job.subprocess.DEVNULL
    assert kwargs["stderr"] == candidate_process_job.subprocess.DEVNULL


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="requires native Windows Job Object")
def test_native_windows_service_child_cannot_execute_before_job_assignment(tmp_path):
    marker = tmp_path / "service-started.txt"
    script = f"from pathlib import Path; Path({str(marker)!r}).write_text('started', encoding='utf-8')"
    events = []
    real_assign = candidate_process_job._assign_pid_to_job
    real_resume = candidate_process_job._resume_suspended_process

    def observed_assign(job, pid):
        assert not marker.exists(), "service code ran before Job Object assignment"
        events.append("assign_begin")
        notes = real_assign(job, pid)
        assert "job_object_assigned" in notes, notes
        events.append("assigned")
        assert not marker.exists(), "service code ran before ResumeThread"
        return notes

    def observed_resume(pid):
        assert events == ["assign_begin", "assigned"]
        assert not marker.exists(), "service code ran before ResumeThread"
        events.append("resume")
        return real_resume(pid)

    with (
        patch.object(candidate_process_job, "_assign_pid_to_job", side_effect=observed_assign),
        patch.object(candidate_process_job, "_resume_suspended_process", side_effect=observed_resume),
    ):
        managed = candidate_process_job.spawn_managed_service(
            [sys.executable, "-c", script],
            cwd=tmp_path,
            env=os.environ.copy(),
        )

    try:
        assert events == ["assign_begin", "assigned", "resume"]
        managed.process.wait(timeout=10)
        assert marker.is_file(), "service child did not execute after successful resume"
    finally:
        managed.cleanup(terminate_first=True, wait_timeout=5.0)


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="requires native Windows Job Object")
def test_native_windows_assignment_failure_never_executes_target(tmp_path):
    marker = tmp_path / "assignment-failure-marker.txt"
    script = f"from pathlib import Path; Path({str(marker)!r}).write_text('started', encoding='utf-8')"

    with (
        patch.object(candidate_process_job, "_assign_pid_to_job", return_value=["AssignProcessToJobObject_failed_err=5"]),
    ):
        try:
            candidate_process_job.spawn_managed(
                [sys.executable, "-c", script],
                cwd=tmp_path,
                env=os.environ.copy(),
            )
        except candidate_process_job.JobObjectUnavailable as exc:
            assert exc.process_reaped is True
        else:
            raise AssertionError("assignment failure must block spawn")

    assert not marker.exists(), "target code executed despite Job assignment failure"


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="requires native Windows Job Object")
def test_native_windows_resume_failure_never_executes_target(tmp_path):
    marker = tmp_path / "resume-failure-marker.txt"
    script = f"from pathlib import Path; Path({str(marker)!r}).write_text('started', encoding='utf-8')"

    with (
        patch.object(candidate_process_job, "_resume_suspended_process", return_value=(["ResumeThread_failed_err=5"], False)),
    ):
        try:
            candidate_process_job.spawn_managed(
                [sys.executable, "-c", script],
                cwd=tmp_path,
                env=os.environ.copy(),
            )
        except candidate_process_job.JobObjectUnavailable as exc:
            assert exc.process_reaped is True
        else:
            raise AssertionError("resume failure must block spawn")

    assert not marker.exists(), "target code executed despite ResumeThread failure"


def test_job_configuration_failure_closes_handle_before_any_spawn():
    class FakeKernel:
        def __init__(self):
            self.closed = []

        def CreateJobObjectW(self, *_args):
            return 77

        def SetInformationJobObject(self, *_args):
            return 0

        def CloseHandle(self, handle):
            self.closed.append(handle)
            return 1

    kernel = FakeKernel()
    with (
        patch.object(candidate_process_job, "_kernel32", kernel),
        patch.object(candidate_process_job, "_last_error", return_value=5),
    ):
        job, notes = candidate_process_job._create_job_object()

    assert job is None
    assert kernel.closed == [77]
    assert any(note.startswith("SetInformationJobObject_failed_err=") for note in notes)


def test_snapshot_failure_does_not_claim_suspended_thread_resumed():
    class FakeKernel:
        def __init__(self):
            self.closed = []

        def CreateToolhelp32Snapshot(self, *_args):
            return 0

        def CloseHandle(self, handle):
            self.closed.append(handle)
            return 1

    kernel = FakeKernel()
    with (
        patch.object(candidate_process_job, "_kernel32", kernel),
        patch.object(candidate_process_job, "_last_error", return_value=5),
    ):
        notes, resumed = candidate_process_job._resume_suspended_process(12345)

    assert resumed is False
    assert any(note.startswith("CreateToolhelp32Snapshot_failed_err=") for note in notes)
    assert kernel.closed == []


def test_open_thread_failure_does_not_claim_suspended_thread_resumed():
    class FakeKernel:
        def __init__(self):
            self.closed = []

        def CreateToolhelp32Snapshot(self, *_args):
            return 88

        def Thread32First(self, _snapshot, entry_ptr):
            entry = candidate_process_job.ctypes.cast(
                entry_ptr,
                candidate_process_job.ctypes.POINTER(candidate_process_job._ThreadEntry32),
            ).contents
            entry.th32OwnerProcessID = 12345
            entry.th32ThreadID = 67890
            return 1

        def Thread32Next(self, *_args):
            return 0

        def OpenThread(self, *_args):
            return 0

        def CloseHandle(self, handle):
            self.closed.append(handle)
            return 1

    kernel = FakeKernel()
    with (
        patch.object(candidate_process_job, "_kernel32", kernel),
        patch.object(candidate_process_job, "_last_error", return_value=5),
    ):
        notes, resumed = candidate_process_job._resume_suspended_process(12345)

    assert resumed is False
    assert any(note.startswith("OpenThread_failed_err=") for note in notes)
    assert kernel.closed == [88]


def test_popen_failure_closes_precreated_job_handle():
    job = FakeJob()
    with (
        patch.object(candidate_process_job, "_is_windows", return_value=True),
        patch.object(candidate_process_job, "_create_job_object", return_value=(job, [])),
        patch.object(candidate_process_job.subprocess, "Popen", side_effect=OSError("injected create failure")),
    ):
        try:
            candidate_process_job._spawn(
                ["candidate-child"], cwd=".", env={}, text=True,
                stdout=None, stderr=None,
            )
        except OSError as exc:
            assert "injected create failure" in str(exc)
        else:
            raise AssertionError("expected Popen failure")

    assert job.handle == 0


def test_abort_reports_unreaped_process_when_kill_and_wait_fail():
    class UnreapedProcess:
        pid = 12345
        stdout = None
        stderr = None

        def kill(self):
            raise OSError("injected kill failure")

        def wait(self, timeout=None):
            raise candidate_process_job.subprocess.TimeoutExpired("candidate-child", timeout)

        def poll(self):
            return None

    job = FakeJob()
    notes = []
    reaped = candidate_process_job._abort_suspended(
        UnreapedProcess(), job, notes, assigned=False, timeout=0.01,
    )

    assert reaped is False
    assert job.handle == 0
    assert any(note.startswith("abort_kill_failed:") for note in notes)
    assert "abort_wait_timeout" in notes
    assert "abort_process_not_reaped" in notes


def test_create_job_object_failure_does_not_configure_or_return_handle():
    class FakeKernel:
        def __init__(self):
            self.configured = False
            self.closed = []

        def CreateJobObjectW(self, *_args):
            return 0

        def SetInformationJobObject(self, *_args):
            self.configured = True
            return 1

        def CloseHandle(self, handle):
            self.closed.append(handle)
            return 1

    kernel = FakeKernel()
    with (
        patch.object(candidate_process_job, "_kernel32", kernel),
        patch.object(candidate_process_job, "_last_error", return_value=5),
    ):
        job, notes = candidate_process_job._create_job_object()

    assert job is None
    assert kernel.configured is False
    assert kernel.closed == []
    assert any(note.startswith("CreateJobObjectW_failed_err=") for note in notes)
