from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from execution_host.core_authority_client import AuthorityClientError
from execution_host.granted_host import GrantedExecutionHost
from execution_host.process_control import run_bounded
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
        ["git", "remote", "add", "origin", f"https://github.com/{REPOSITORY}.git"],
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
    def __init__(self, binding, *, fail_validation_number=None, fail_start=False, fail_complete=False):
        self.binding = binding
        self.validation_calls = 0
        self.fail_validation_number = fail_validation_number
        self.fail_start = fail_start
        self.fail_complete = fail_complete
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
        if self.fail_complete:
            raise AuthorityClientError("run_completion_unavailable", 503)
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


def test_host_rejects_git_head_or_branch_mismatch(tmp_path):
    wrong_head_binding = make_binding(tmp_path / "wrong-head")
    wrong_head_binding["expected_head"] = "0" * 40
    wrong_head = GrantedExecutionHost(FakeAuthorityClient(wrong_head_binding)).execute_for_work(
        "W32", "grant-test", "secret-token"
    )
    assert wrong_head["status"] == "BLOCKED"
    assert wrong_head["blocker"] == "execution_git_head_mismatch"

    wrong_branch_binding = make_binding(tmp_path / "wrong-branch")
    wrong_branch_binding["branch"] = "main"
    wrong_branch = GrantedExecutionHost(FakeAuthorityClient(wrong_branch_binding)).execute_for_work(
        "W32", "grant-test", "secret-token"
    )
    assert wrong_branch["status"] == "BLOCKED"
    assert wrong_branch["blocker"] == "execution_git_branch_mismatch"


def test_host_rejects_wrong_git_origin_repository(tmp_path):
    binding = make_binding(tmp_path)
    subprocess.run(
        ["git", "remote", "set-url", "origin", "https://github.com/attacker/other.git"],
        cwd=binding["execution_workspace"],
        check=True,
        capture_output=True,
    )
    result = GrantedExecutionHost(FakeAuthorityClient(binding)).execute_for_work(
        "W32", "grant-test", "secret-token"
    )
    assert result["status"] == "BLOCKED"
    assert result["blocker"] == "execution_git_origin_mismatch"


def test_host_rejects_dirty_worktree_even_when_source_hash_matches(tmp_path):
    binding = make_binding(tmp_path)
    workspace = Path(binding["execution_workspace"])
    (workspace / "test_ok.py").write_text(
        "def test_ok():\n    assert 2 == 2\n",
        encoding="utf-8",
    )
    # The submitted source digest matches the modified bytes, but the Git
    # revision is no longer a clean checkout of the approved commit.
    binding["source_sha256"] = workspace_source_sha256(workspace)
    authority = FakeAuthorityClient(binding)
    result = GrantedExecutionHost(authority).execute_for_work(
        "W32", "grant-test", "secret-token"
    )
    assert result["status"] == "BLOCKED"
    assert result["blocker"] == "execution_git_worktree_dirty"
    assert authority.started == []


def test_host_rejects_evidence_directory_inside_git_repository(tmp_path):
    root = tmp_path / "repository-root"
    workspace = root / "workspace"
    evidence = root / "evidence"
    workspace.mkdir(parents=True)
    evidence.mkdir()
    (workspace / "test_ok.py").write_text("def test_ok(): assert True\n", encoding="utf-8")
    expected_head = init_git(root)
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
    result = GrantedExecutionHost(FakeAuthorityClient(binding)).execute_for_work(
        "W32", "grant-test", "secret-token"
    )
    assert result["status"] == "BLOCKED"
    assert result["blocker"] == "evidence_root_inside_git_repository"


def test_host_does_not_report_pass_when_run_completion_is_not_persisted(tmp_path):
    binding = make_binding(tmp_path)
    authority = FakeAuthorityClient(binding, fail_complete=True)
    result = GrantedExecutionHost(authority).execute_for_work(
        "W32", "grant-test", "secret-token"
    )
    assert result["execution_status"] == "PASS"
    assert result["status"] == "BLOCKED"
    assert result["run_record_started"] is True
    assert result["run_record_persisted"] is False
    assert result["blocker"] == "run_record_completion_failed:AuthorityClientError"


def test_host_blocks_when_core_is_unreachable_before_grant_validation(tmp_path):
    binding = make_binding(tmp_path)
    authority = FakeAuthorityClient(binding, fail_validation_number=1)
    result = GrantedExecutionHost(authority).execute_for_work(
        "W32", "grant-test", "secret-token"
    )
    assert result["status"] == "BLOCKED"
    assert authority.started == []
    assert authority.records == []


def test_host_completes_blocked_run_record_when_local_evidence_write_fails(
    tmp_path, monkeypatch
):
    binding = make_binding(tmp_path)
    authority = FakeAuthorityClient(binding)
    original_write_text = Path.write_text

    def fail_stdout(path, content, *args, **kwargs):
        if path.name == "stdout.log":
            raise OSError("disk_full")
        return original_write_text(path, content, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", fail_stdout)
    result = GrantedExecutionHost(authority).execute_for_work(
        "W32", "grant-test", "secret-token"
    )

    assert result["status"] == "BLOCKED"
    assert result["execution_status"] == "PASS"
    assert result["blocker"].startswith("run_evidence_persistence_failed")
    assert result["run_record_started"] is True
    assert result["run_record_persisted"] is True
    assert result["evidence_persisted"] is False
    assert len(authority.records) == 1
    assert authority.records[0]["status"] == "BLOCKED"
    assert authority.records[0]["execution_status"] == "PASS"
    assert authority.records[0]["evidence_persisted"] is False



def test_safe_env_uses_per_run_isolated_home_and_temp(monkeypatch, tmp_path):
    from execution_host.security import safe_env

    monkeypatch.setenv("HOME", str(tmp_path / "operator-home"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "operator-profile"))
    monkeypatch.setenv("APPDATA", str(tmp_path / "operator-appdata"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "operator-localappdata"))
    monkeypatch.setenv("OPENAI_API_KEY", "operator-secret-value")
    monkeypatch.setenv("ROOM_HOP_EXECUTION_HOST_CREDENTIAL", "operator-host-secret")

    isolated = tmp_path / "run" / "home"
    env = safe_env(isolated_home=isolated)

    assert env["HOME"] == str(isolated.resolve())
    assert env["TMP"] == str((isolated / "tmp").resolve())
    assert env["TEMP"] == str((isolated / "tmp").resolve())
    assert "OPENAI_API_KEY" not in env
    assert "ROOM_HOP_EXECUTION_HOST_CREDENTIAL" not in env
    assert str(tmp_path / "operator-home") not in env.values()
    assert str(tmp_path / "operator-profile") not in env.values()
    assert (isolated / "tmp").is_dir()
    if os.name == "nt":
        assert env["USERPROFILE"] == str(isolated.resolve())
        assert env["APPDATA"].startswith(str(isolated.resolve()))
        assert env["LOCALAPPDATA"].startswith(str(isolated.resolve()))
    else:
        assert env["TMPDIR"] == str((isolated / "tmp").resolve())
        assert env["XDG_CACHE_HOME"] == str((isolated / ".cache").resolve())



def test_run_bounded_caps_combined_output(tmp_path):
    code = "import sys,time; sys.stdout.write('x' * (2 * 1024 * 1024)); sys.stdout.flush(); time.sleep(5)"
    result = run_bounded(
        [sys.executable, "-c", code],
        cwd=tmp_path,
        env=os.environ.copy(),
        timeout=5,
        max_output_bytes=4096,
    )
    assert result.output_limit_exceeded is True
    assert len(result.stdout) + len(result.stderr) <= 4096
    assert result.tree_termination_confirmed is True


def test_run_bounded_terminates_process_tree_on_timeout(tmp_path):
    marker = tmp_path / "orphan-survived.txt"
    child_code = (
        "import time; from pathlib import Path; time.sleep(1.5); "
        f"Path({str(marker)!r}).write_text('survived', encoding='utf-8')"
    )
    parent_code = (
        "import subprocess,sys,time; "
        "subprocess.Popen([sys.executable, '-c', sys.argv[1]]); "
        "time.sleep(30)"
    )
    result = run_bounded(
        [sys.executable, "-c", parent_code, child_code],
        cwd=tmp_path,
        env=os.environ.copy(),
        timeout=0.4,
    )
    assert result.timed_out is True
    assert result.tree_termination_confirmed is True
    time.sleep(1.8)
    assert not marker.exists()
