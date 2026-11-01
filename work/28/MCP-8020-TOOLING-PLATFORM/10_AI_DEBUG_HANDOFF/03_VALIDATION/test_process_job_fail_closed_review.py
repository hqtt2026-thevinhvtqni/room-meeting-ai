import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch

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
