from __future__ import annotations

import hashlib
import subprocess
import sys
from urllib.parse import urlsplit

from execution_host.core_authority_client import CoreAuthorityClient
from execution_host.granted_host import GrantedExecutionHost
from execution_host.source_snapshot import workspace_source_sha256
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.execution_authority import ExecutionAuthority
from room_hop_mcp.adapter.execution_authority_http import create_execution_authority_router


class AgentRegistryStub:
    def exists(self, principal_id):
        return principal_id == "agent-ka"


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def configured_authority(tmp_path):
    root = tmp_path / "root"
    workspace = root / "workspace"
    evidence = root / "evidence"
    workspace.mkdir(parents=True)
    evidence.mkdir()
    (workspace / "test_ok.py").write_text("def test_ok(): assert True\n", encoding="utf-8")
    return ExecutionAuthority(
        identities={
            "agent-service": {
                "kind": "agent",
                "principal_id": "agent-ka",
                "credential_sha256": digest("agent-secret-32-byte-minimum-credential"),
            },
            "host-service": {
                "kind": "host",
                "credential_sha256": digest("host-secret-32-byte-minimum-credential"),
            },
        },
        works={
            "W32": {
                "work_name": "ROOM-HOP-WORK-32",
                "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
                "allowed_branches": ["work/32-core-owned-execution-authority-20261112"],
                "allowed_identities": ["agent-service"],
                "allowed_host_identities": ["host-service"],
                "allowed_assignments": ["W32-A"],
                "allowed_tasks": ["W32-T1"],
                "workspace_root": str(root),
                "execution_workspace": str(workspace),
                "evidence_root": str(evidence),
                "environment_id": "w32-test",
                "test_entrypoint": ["python", "-m", "pytest", "-q"],
                "max_timeout_seconds": 30,
            }
        },
        store_path=tmp_path / "authority" / "events.jsonl",
        agent_registry=AgentRegistryStub(),
    )


def app_for(authority):
    app = FastAPI()
    app.include_router(create_execution_authority_router(authority))
    return TestClient(app)


def agent_headers():
    return {
        "X-ROOM-HOP-SERVICE-ID": "agent-service",
        "X-ROOM-HOP-SERVICE-CREDENTIAL": "agent-secret-32-byte-minimum-credential",
    }


def host_headers():
    return {
        "X-ROOM-HOP-SERVICE-ID": "host-service",
        "X-ROOM-HOP-SERVICE-CREDENTIAL": "host-secret-32-byte-minimum-credential",
    }


def issue_payload():
    return {
        "purpose": "pytest_run",
        "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
        "branch": "work/32-core-owned-execution-authority-20261112",
        "expected_head": "b" * 40,
        "assignment_id": "W32-A",
        "task_id": "W32-T1",
        "host_identity_id": "host-service",
        "source_sha256": "a" * 64,
        "environment_id": "w32-test",
        "test_entrypoint": ["python", "-m", "pytest", "-q"],
        "requested_timeout_seconds": 20,
    }


def test_unconfigured_authority_returns_503_before_request_validation():
    response = app_for(None).post(
        "/works/W32/execution-grants",
        json={"purpose": "pytest_run"},
    )
    assert response.status_code == 503
    assert response.json()["detail"] == "execution_authority_not_configured"


def test_http_issue_validate_revoke_lifecycle(tmp_path):
    client = app_for(configured_authority(tmp_path))
    issued = client.post(
        "/works/W32/execution-grants",
        json=issue_payload(),
        headers=agent_headers(),
    )
    assert issued.status_code == 200
    grant = issued.json()
    assert grant["grant_token"]

    validated = client.get(
        f"/works/W32/execution-grants/{grant['grant_id']}/validate",
        headers={
            **host_headers(),
            "Authorization": "Bearer " + grant["grant_token"],
        },
    )
    assert validated.status_code == 200
    assert validated.json()["principal_id"] == "agent-ka"

    status = client.get(
        f"/works/W32/execution-grants/{grant['grant_id']}",
        headers=agent_headers(),
    )
    assert status.status_code == 200
    assert status.json()["status"] == "active"

    revoked = client.post(
        f"/works/W32/execution-grants/{grant['grant_id']}/revoke",
        headers=agent_headers(),
    )
    assert revoked.status_code == 200
    assert revoked.json()["status"] == "revoked"

    denied = client.get(
        f"/works/W32/execution-grants/{grant['grant_id']}/validate",
        headers={
            **host_headers(),
            "Authorization": "Bearer " + grant["grant_token"],
        },
    )
    assert denied.status_code == 403
    assert denied.json()["detail"] == "grant_not_active"


def test_http_issue_rejects_bad_agent_credential_and_unknown_fields(tmp_path):
    client = app_for(configured_authority(tmp_path))
    bad_auth = client.post(
        "/works/W32/execution-grants",
        json=issue_payload(),
        headers={
            "X-ROOM-HOP-SERVICE-ID": "agent-service",
            "X-ROOM-HOP-SERVICE-CREDENTIAL": "wrong",
        },
    )
    assert bad_auth.status_code == 401
    assert bad_auth.json()["detail"] == "service_credential_invalid"

    invalid_body = dict(issue_payload(), authorized=True)
    invalid = client.post(
        "/works/W32/execution-grants",
        json=invalid_body,
        headers=agent_headers(),
    )
    assert invalid.status_code == 422
    assert invalid.json()["detail"] == "execution_grant_request_invalid"


def test_http_run_record_requires_grant_and_host_binding(tmp_path):
    client = app_for(configured_authority(tmp_path))
    grant = client.post(
        "/works/W32/execution-grants",
        json=issue_payload(),
        headers=agent_headers(),
    ).json()
    headers = {
        **host_headers(),
        "Authorization": "Bearer " + grant["grant_token"],
    }
    started = client.post(
        f"/works/W32/execution-grants/{grant['grant_id']}/runs",
        json={
            "run_id": "run-http-001",
            "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
            "branch": "work/32-core-owned-execution-authority-20261112",
            "expected_head": "b" * 40,
            "command": ["python", "-m", "pytest", "-q"],
            "source_sha256": "a" * 64,
            "environment_id": "w32-test",
            "started_at": "2026-11-12T00:00:00+00:00",
        },
        headers=headers,
    )
    assert started.status_code == 200
    assert started.json()["status"] == "started"

    completed = client.post(
        f"/works/W32/execution-grants/{grant['grant_id']}/runs/run-http-001/complete",
        json={
            "finished_at": "2026-11-12T00:00:01+00:00",
            "status": "PASS",
            "execution_status": "PASS",
            "exit_code": 0,
            "evidence_sha256": "c" * 64,
            "evidence_ref": "evidence/run-http-001/RUN_EVIDENCE.json",
            "evidence_persisted": True,
            "evidence_errors": [],
            "stdout_sha256": "d" * 64,
            "stderr_sha256": "e" * 64,
        },
        headers=headers,
    )
    assert completed.status_code == 200
    assert completed.json()["status"] == "completed"


def test_http_run_completion_rejects_invalid_evidence_metadata(tmp_path):
    client = app_for(configured_authority(tmp_path))
    grant = client.post(
        "/works/W32/execution-grants",
        json=issue_payload(),
        headers=agent_headers(),
    ).json()
    headers = {
        **host_headers(),
        "Authorization": "Bearer " + grant["grant_token"],
    }
    started = client.post(
        f"/works/W32/execution-grants/{grant['grant_id']}/runs",
        json={
            "run_id": "run-http-evidence-metadata",
            "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
            "branch": "work/32-core-owned-execution-authority-20261112",
            "expected_head": "b" * 40,
            "command": ["python", "-m", "pytest", "-q"],
            "source_sha256": "a" * 64,
            "environment_id": "w32-test",
            "started_at": "2026-11-12T00:00:00+00:00",
        },
        headers=headers,
    )
    assert started.status_code == 200

    invalid = client.post(
        f"/works/W32/execution-grants/{grant['grant_id']}/runs/run-http-evidence-metadata/complete",
        json={
            "finished_at": "2026-11-12T00:00:01+00:00",
            "status": "PASS",
            "execution_status": "PASS",
            "exit_code": 0,
            "evidence_sha256": "c" * 64,
            "evidence_persisted": False,
            "evidence_errors": [],
            "stdout_sha256": "bad",
            "stderr_sha256": "e" * 64,
        },
        headers=headers,
    )
    assert invalid.status_code == 422
    assert invalid.json()["detail"] == "execution_run_completion_invalid"

    completed = client.post(
        f"/works/W32/execution-grants/{grant['grant_id']}/runs/run-http-evidence-metadata/complete",
        json={
            "finished_at": "2026-11-12T00:00:02+00:00",
            "status": "BLOCKED",
            "execution_status": "PASS",
            "exit_code": 0,
            "evidence_sha256": "c" * 64,
            "evidence_ref": "evidence/run-http-evidence-metadata/RUN_EVIDENCE.json",
            "evidence_persisted": False,
            "evidence_errors": ["stdout.log:OSError"],
            "stdout_sha256": "d" * 64,
            "stderr_sha256": "e" * 64,
        },
        headers=headers,
    )
    assert completed.status_code == 200
    assert completed.json()["status"] == "completed"


def test_http_run_completion_rejects_body_run_id_mismatch(tmp_path):
    client = app_for(configured_authority(tmp_path))
    grant = client.post(
        "/works/W32/execution-grants",
        json=issue_payload(),
        headers=agent_headers(),
    ).json()
    headers = {
        **host_headers(),
        "Authorization": "Bearer " + grant["grant_token"],
    }
    started = client.post(
        f"/works/W32/execution-grants/{grant['grant_id']}/runs",
        json={
            "run_id": "run-http-path-bound",
            "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
            "branch": "work/32-core-owned-execution-authority-20261112",
            "expected_head": "b" * 40,
            "command": ["python", "-m", "pytest", "-q"],
            "source_sha256": "a" * 64,
            "environment_id": "w32-test",
            "started_at": "2026-11-12T00:00:00+00:00",
        },
        headers=headers,
    )
    assert started.status_code == 200

    mismatch = client.post(
        f"/works/W32/execution-grants/{grant['grant_id']}/runs/run-http-path-bound/complete",
        json={
            "run_id": "run-http-other",
            "finished_at": "2026-11-12T00:00:01+00:00",
            "status": "PASS",
            "exit_code": 0,
            "evidence_sha256": "c" * 64,
        },
        headers=headers,
    )
    assert mismatch.status_code == 422
    assert mismatch.json()["detail"] == "execution_run_id_mismatch"

    completed = client.post(
        f"/works/W32/execution-grants/{grant['grant_id']}/runs/run-http-path-bound/complete",
        json={
            "finished_at": "2026-11-12T00:00:02+00:00",
            "status": "PASS",
            "exit_code": 0,
            "evidence_sha256": "d" * 64,
        },
        headers=headers,
    )
    assert completed.status_code == 200
    assert completed.json()["status"] == "completed"



def test_granted_host_completes_through_real_core_http_contract(tmp_path):
    root = tmp_path / "host-root"
    workspace = root / "workspace"
    evidence = root / "evidence"
    workspace.mkdir(parents=True)
    evidence.mkdir()
    (workspace / "test_ok.py").write_text(
        "def test_ok():\n    assert True\n",
        encoding="utf-8",
    )

    branch = "work/32-core-owned-execution-authority-20261112"
    commands = [
        ["git", "init", "-b", branch],
        ["git", "config", "user.email", "w32-tests@example.invalid"],
        ["git", "config", "user.name", "Work32 Test"],
        ["git", "add", "-A"],
        ["git", "commit", "-m", "test Host Core completion contract"],
        [
            "git",
            "remote",
            "add",
            "origin",
            "https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai.git",
        ],
        ["git", "rev-parse", "HEAD"],
    ]
    head = ""
    for command in commands:
        result = subprocess.run(
            command,
            cwd=workspace,
            text=True,
            capture_output=True,
            check=True,
        )
        head = result.stdout.strip()
    source_sha256 = workspace_source_sha256(workspace)
    command = [sys.executable, "-m", "pytest", "-q"]

    authority = ExecutionAuthority(
        identities={
            "agent-service": {
                "kind": "agent",
                "principal_id": "agent-ka",
                "credential_sha256": digest("agent-secret-32-byte-minimum-credential"),
            },
            "host-service": {
                "kind": "host",
                "credential_sha256": digest("host-secret-32-byte-minimum-credential"),
            },
        },
        works={
            "W32": {
                "work_name": "ROOM-HOP-WORK-32",
                "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
                "allowed_branches": [branch],
                "allowed_identities": ["agent-service"],
                "allowed_host_identities": ["host-service"],
                "allowed_assignments": ["W32-A"],
                "allowed_tasks": ["W32-T1"],
                "workspace_root": str(root),
                "execution_workspace": str(workspace),
                "evidence_root": str(evidence),
                "environment_id": "w32-test",
                "test_entrypoint": command,
                "max_timeout_seconds": 30,
            }
        },
        store_path=tmp_path / "authority" / "events.jsonl",
        agent_registry=AgentRegistryStub(),
    )
    client = app_for(authority)
    issued = client.post(
        "/works/W32/execution-grants",
        json={
            "purpose": "pytest_run",
            "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
            "branch": branch,
            "expected_head": head,
            "assignment_id": "W32-A",
            "task_id": "W32-T1",
            "host_identity_id": "host-service",
            "source_sha256": source_sha256,
            "environment_id": "w32-test",
            "test_entrypoint": command,
            "requested_timeout_seconds": 20,
        },
        headers=agent_headers(),
    )
    assert issued.status_code == 200
    grant = issued.json()

    def transport(url, method, request_body, headers, timeout):
        response = client.request(
            method,
            urlsplit(url).path,
            content=request_body,
            headers=headers,
        )
        return response.status_code, response.content

    core_client = CoreAuthorityClient(
        base_url="http://127.0.0.1:8000",
        service_id="host-service",
        credential="host-secret-32-byte-minimum-credential",
        transport=transport,
    )
    result = GrantedExecutionHost(core_client).execute_for_work(
        "W32",
        grant["grant_id"],
        grant["grant_token"],
    )

    assert result["status"] == "PASS"
    assert result["run_record_persisted"] is True
    assert result["evidence_persisted"] is True
    assert result["evidence_errors"] == []
    assert len(result["stdout_sha256"]) == 64
    assert len(result["stderr_sha256"]) == 64

    events = [
        json.loads(line)
        for line in (tmp_path / "authority" / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    completed = next(event for event in events if event["event_type"] == "run_completed")
    payload = completed["payload"]
    assert payload["status"] == "PASS"
    assert payload["evidence_persisted"] is True
    assert payload["evidence_errors"] == []
    assert len(payload["stdout_sha256"]) == 64
    assert len(payload["stderr_sha256"]) == 64
