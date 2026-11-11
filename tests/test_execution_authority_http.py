from __future__ import annotations

import hashlib

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
                "allowed_identities": ["agent-service"],
                "allowed_host_identities": ["host-service"],
                "allowed_assignments": ["W32-A"],
                "allowed_tasks": ["W32-T1"],
                "workspace_root": str(root),
                "execution_workspace": str(workspace),
                "evidence_root": str(evidence),
                "source_sha256": "a" * 64,
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
            "exit_code": 0,
            "evidence_sha256": "c" * 64,
            "evidence_ref": "evidence/run-http-001/RUN_EVIDENCE.json",
        },
        headers=headers,
    )
    assert completed.status_code == 200
    assert completed.json()["status"] == "completed"
