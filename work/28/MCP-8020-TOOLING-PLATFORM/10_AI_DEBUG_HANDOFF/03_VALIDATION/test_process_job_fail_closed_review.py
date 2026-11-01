import importlib.util
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

PATCH_ROOT = (
    Path(__file__).resolve().parents[1]
    / "02_PATCH_CANDIDATES"
    / "20261030_WP2_SUSPENDED_SPAWN"
)
MODULE_PATH = PATCH_ROOT / "execution_host" / "process_job.py"
SPEC = importlib.util.spec_from_file_location("work28_wp2_candidate_process_job", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
candidate_process_job = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = candidate_process_job
SPEC.loader.exec_module(candidate_process_job)

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
