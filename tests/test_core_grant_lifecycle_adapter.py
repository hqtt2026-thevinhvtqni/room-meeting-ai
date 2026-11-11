from __future__ import annotations

import json
from pathlib import Path

import pytest

from wee.bridge.core_grant_host import CoreGrantExecutionError, CoreGrantExecutionHost
from wee.models import WorkContext


def make_context(tmp_path):
    root = tmp_path / "root"
    workspace = root / "workspace"
    evidence = root / "evidence"
    workspace.mkdir(parents=True)
    evidence.mkdir()
    (workspace / "test_ok.py").write_text("def test_ok(): assert True\n", encoding="utf-8")
    return WorkContext(
        work_id="W32",
        work_name="ROOM-HOP-WORK-32",
        repository="hqtt2026-thevinhvtqni/room-meeting-ai",
        repository_root=str(root),
        branch="work/32-core-owned-execution-authority-20261112",
        execution_workspace=str(workspace),
        expected_head="a" * 40,
        runtime={},
        browser={},
        test_entrypoint=["python", "-m", "pytest", "-q"],
        ci_target={},
        evidence_root=str(evidence),
        execution_id="lifecycle-run-1",
        assignment_id="W32-EXECUTION-AUTHORITY",
        task_id="W32-P0-PYTEST",
        environment_id="w32-local-ci",
        host_identity_id="host-8031",
        requested_timeout_seconds=60,
    )


def test_lifecycle_adapter_issues_executes_and_revokes_grant(tmp_path):
    calls = []

    def transport(url, method, body, headers, timeout):
        calls.append((url, method, json.loads(body) if body else None, headers, timeout))
        if url.endswith("/works/W32/execution-grants") and method == "POST":
            return 200, json.dumps({
                "grant_id": "grant-123",
                "grant_token": "one-time-secret",
            }).encode()
        if url.endswith("/health") and method == "GET":
            return 200, json.dumps({
                "status": "PASS",
                "provider_type": "CORE_AUTHORIZED_PYTEST",
                "authority": "CORE_ONLINE",
                "grant_cache": False,
            }).encode()
        if url.endswith("/execute-granted") and method == "POST":
            return 200, json.dumps({
                "status": "PASS",
                "work_id": "W32",
                "run_id": "run-123",
                "run_record_persisted": True,
                "exit_code": 0,
            }).encode()
        if url.endswith("/grant-123/revoke") and method == "POST":
            return 200, json.dumps({"status": "revoked"}).encode()
        raise AssertionError((url, method))

    host = CoreGrantExecutionHost(
        core_url="http://127.0.0.1:8000",
        host_url="http://127.0.0.1:8031",
        agent_id="agent-ka-service",
        agent_credential="agent-secret",
        transport=transport,
    )
    context = make_context(tmp_path)
    discovery = host.discover(context)
    result = host.execute_authorized(context)

    assert discovery["authority"] == "CORE_ONLINE"
    assert result["status"] == "PASS"
    assert result["grant_revoked_after_run"] is True
    assert [call[1] for call in calls] == ["GET", "POST", "POST", "POST"]
    issue = calls[1]
    assert issue[2]["assignment_id"] == "W32-EXECUTION-AUTHORITY"
    assert issue[2]["task_id"] == "W32-P0-PYTEST"
    assert issue[2]["test_entrypoint"] == ["python", "-m", "pytest", "-q"]
    assert "one-time-secret" not in json.dumps(result)
    assert calls[2][4] >= 3630


def test_lifecycle_adapter_rejects_non_tls_remote_http():
    with pytest.raises(CoreGrantExecutionError, match="must_use_https_or_loopback_http"):
        CoreGrantExecutionHost(
            core_url="http://core.internal:8000",
            host_url="http://127.0.0.1:8031",
            agent_id="agent-ka-service",
            agent_credential="agent-secret",
            transport=lambda *args: (200, b"{}"),
        )
