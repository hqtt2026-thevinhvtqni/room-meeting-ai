import sys
from pathlib import Path
from unittest.mock import patch

PATCH_ROOT = (
    Path(__file__).resolve().parents[1]
    / "02_PATCH_CANDIDATES"
    / "20261030_WP2_SUSPENDED_SPAWN"
)
sys.path.insert(0, str(PATCH_ROOT))

from execution_host.process_job import ManagedProcess, _wait_job_drained


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
    with patch("execution_host.process_job._job_active_processes", return_value=None):
        assert managed.members_count() is None


def test_job_drain_query_failure_is_not_success():
    notes = []
    with patch("execution_host.process_job._job_active_processes", return_value=None):
        assert _wait_job_drained(object(), timeout=0.0, notes=notes) is False
    assert "job_member_count_unavailable_fail_closed" in notes
