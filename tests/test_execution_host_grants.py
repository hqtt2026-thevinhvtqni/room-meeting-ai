from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from execution_host.core_authority_client import AuthorityClientError
from execution_host.granted_host import GrantedExecutionHost
from execution_host.source_snapshot import workspace_source_sha256


REPOSITORY = "hqtt2026-thevinhvtqni/room-meeting-ai"
BRANCH = "work/32-core-execution-authority-20261112"


def init_git(workspace: Path) -> str:
    commands = [
        ["git", "init", "-b", BRANCH],
        ["git", "config", "user.email", "w32-tests@example.invalid"],
        ["git", "config", "user.name", "Work32 Test"],
        ["git", "add", "-A"],
        ["git", "commit", "-m", "test workspace snapshot"],
        ["git", "rev-parse", "HEAD"],
    ]
    output = ""
    for command in commands:
        result = subprocess.run(
            command, cwd=workspace, text=True, capture_output=True, check=True
        )
        output = result.stdout.strip()
    return output


class FakeAuthorityClient:
    def __init__(self, binding, *, fail_validation_number=None, fail_start=False):
        self.binding = binding
        self.validation_calls = 0
        self.fail_validation_number = fail_validation_number
        self.fail_start = fail_start
        self.records = []
        self.started = []

    def validate_grant(self, work_id, grant_id, token):
        self.validation_calls += 1
        if self.fail_validation_number == self.validation_calls:
            raise AuthorityClientError("grant_not_active", 403)
        assert work_id == self.binding["work_id"]
        assert grant_id == "grant-test"
        assert token == "secret-token"
        return dict(self.binding, status="active", grant_id=grant_id)

    def start_run(self, work_id, grant_id, token, record):
        if self.fail_start:
            raise AuthorityClientError("run_start_persistence_unavailable", 503)
        self.started.append(record)
        return {"run_id": record["run_id"], "grant_id": grant_id, "status": "started"}

    def complete_run(self, work_id, grant_id, token, run_id, record):
        self.records.append({"run_id": run_id, **record})
        return {"run_id": run_id, "grant_id": grant_id, "status": "completed"}


def make_binding(tmp_path: Path, command=None):
    root = tmp_path / "root"
    workspace = root / "workspace"
    evidence = root / "evidence"
    workspace.mkdir(parents=True)
    evidence.mkdir()
    (workspace / "test_ok.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    expected_head = init_git(workspace)
    return {
        "work_id": "W32",
        "work_name": "ROOM-HOP-WORK-32",
        "repository": REPOSITORY,
        "branch": BRANCH,
        "expected_head": expected_head,
        "purpose": "pytest_run",
        "assignment_id": "W32-EXECUTION-AUTHORITY",
        "task_id": "W32-P0-PYTEST",
        "principal_id": "agent-ka",
        "host_identity_id": "host-8031",
        "workspace_root": str(root),
        "execution_workspace": str(workspace),
        "evidence_root": str(evidence),
        "source_sha256": workspace_source_sha256(workspace),
        "environment_id": "w32-local-ci",
        "test_entrypoint": command or [sys.executable, "-m", "pytest", "-q"],
        "max_timeout_seconds": 30,
    }


def test_host_validates_twice_executes_canonical_pytest_and_records_run(tmp_path):
    binding = make_binding(tmp_path)
    authority = FakeAuthorityClient(binding)
    result = GrantedExecutionHost(authority).execute_for_work(
        "W32", "grant-test", "secret-token"
    )

    assert authority.validation_calls == 2
    assert result["status"] == "PASS"
    assert result["run_record_persisted"] is True
    assert len(authority.started) == 1
    assert len(authority.records) == 1
    assert authority.started[0]["command"] == binding["test_entrypoint"]
    assert Path(result["evidence_ref"]).exists()
    assert Path(result["stdout_ref"]).exists()


def test_host_revalidates_immediately_before_process_effect(tmp_path):
    root = tmp_path / "root"
    workspace = root / "workspace"
    workspace.mkdir(parents=True)
    marker = root / "must-not-exist.txt"
    test_file = workspace / "test_side_effect.py"
    test_file.write_text(
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('executed')\n"
        "def test_ok(): assert True\n",
        encoding="utf-8",
    )
    evidence = root / "evidence"
    evidence.mkdir()
    expected_head = init_git(workspace)
    binding = {
        "work_id": "W32",
        "work_name": "ROOM-HOP-WORK-32",
        "repository": REPOSITORY,
        "branch": BRANCH,
        "expected_head": expected_head,
        "purpose": "pytest_run",
        "assignment_id": "W32-EXECUTION-AUTHORITY",
        "task_id": "W32-P0-PYTEST",
        "principal_id": "agent-ka",
        "host_identity_id": "host-8031",
        "workspace_root": str(root),
        "execution_workspace": str(workspace),
        "evidence_root": str(evidence),
        "source_sha256": workspace_source_sha256(workspace),
        "environment_id": "w32-local-ci",
        "test_entrypoint": [sys.executable, "-m", "pytest", "-q"],
        "max_timeout_seconds": 30,
    }
    authority = FakeAuthorityClient(binding, fail_validation_number=2)
    result = GrantedExecutionHost(authority).execute_for_work(
        "W32", "grant-test", "secret-token"
    )

    assert authority.validation_calls == 2
    assert len(authority.started) == 1
    assert result["status"] == "BLOCKED"
    assert result["blocker"] == "grant_not_active"
    assert not marker.exists()


def test_host_refuses_non_pytest_command_from_core_binding(tmp_path):
    binding = make_binding(tmp_path, [sys.executable, "-c", "print('unsafe')"])
    authority = FakeAuthorityClient(binding)
    result = GrantedExecutionHost(authority).execute_for_work(
        "W32", "grant-test", "secret-token"
    )
    assert result["status"] == "BLOCKED"
    assert result["blocker"] == "canonical_command_not_pytest"


def test_host_does_not_spawn_when_core_cannot_persist_run_start(tmp_path):
    root = tmp_path / "root"
    workspace = root / "workspace"
    workspace.mkdir(parents=True)
    marker = root / "must-not-exist.txt"
    (workspace / "test_side_effect.py").write_text(
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('executed')\n"
        "def test_ok(): assert True\n",
        encoding="utf-8",
    )
    evidence = root / "evidence"
    evidence.mkdir()
    expected_head = init_git(workspace)
    binding = {
        "work_id": "W32",
        "work_name": "ROOM-HOP-WORK-32",
        "repository": REPOSITORY,
        "branch": BRANCH,
        "expected_head": expected_head,
        "purpose": "pytest_run",
        "assignment_id": "W32-EXECUTION-AUTHORITY",
        "task_id": "W32-P0-PYTEST",
        "principal_id": "agent-ka",
        "host_identity_id": "host-8031",
        "workspace_root": str(root),
        "execution_workspace": str(workspace),
        "evidence_root": str(evidence),
        "source_sha256": workspace_source_sha256(workspace),
        "environment_id": "w32-local-ci",
        "test_entrypoint": [sys.executable, "-m", "pytest", "-q"],
        "max_timeout_seconds": 30,
    }
    authority = FakeAuthorityClient(binding, fail_start=True)
    result = GrantedExecutionHost(authority).execute_for_work(
        "W32", "grant-test", "secret-token"
    )

    assert authority.validation_calls == 1
    assert result["status"] == "BLOCKED"
    assert result["run_record_started"] is False
    assert not marker.exists()
