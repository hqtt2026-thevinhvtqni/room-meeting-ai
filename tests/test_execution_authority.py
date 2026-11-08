from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone

import pytest

from core.execution_authority import (
    AppendOnlyExecutionStore,
    ExecutionAuthority,
    ExecutionAuthorityStoreError,
)


def make_authority(tmp_path, *, grant_seconds=120):
    credential = "service-credential-that-is-long-enough-123"
    digest = hashlib.sha256(credential.encode()).hexdigest()
    root = tmp_path / "work"
    workspace = root / "workspace"
    evidence = root / "evidence"
    workspace.mkdir(parents=True)
    evidence.mkdir()
    authority = ExecutionAuthority(
        identity_credential_sha256={"mcp-8020": digest},
        work_policies={
            "W28": {
                "work_name": "MCP-8020-TOOLING-PLATFORM",
                "allowed_identities": ["mcp-8020"],
                "workspace_root": str(root),
                "execution_workspace": str(workspace),
                "evidence_root": str(evidence),
                "source_sha256": "a" * 64,
                "allowed_purposes": ["pytest_run", "build"],
            }
        },
        store_path=tmp_path / "authority.jsonl",
        default_grant_seconds=grant_seconds,
    )
    return authority, credential, tmp_path / "authority.jsonl"


def test_authenticate_and_issue_work_scoped_grant(tmp_path):
    authority, credential, _ = make_authority(tmp_path)
    identity = authority.authenticate(credential)
    grant = authority.issue_grant(identity, "W28", "pytest_run")
    assert grant["authorized"] is True
    assert grant["work_id"] == "W28"
    assert authority.validate_grant_token(grant["grant_id"], grant["grant_token"])["status"] == "active"


def test_bad_credential_and_wrong_work_fail_closed(tmp_path):
    authority, credential, _ = make_authority(tmp_path)
    with pytest.raises(PermissionError, match="caller_authentication_failed"):
        authority.authenticate("not-the-service-credential")
    with pytest.raises(KeyError, match="unknown_work"):
        authority.issue_grant(authority.authenticate(credential), "W29", "pytest_run")


def test_wrong_purpose_and_invalid_work_id_rejected(tmp_path):
    authority, credential, _ = make_authority(tmp_path)
    identity = authority.authenticate(credential)
    with pytest.raises(PermissionError, match="execution_purpose_not_allowed"):
        authority.issue_grant(identity, "W28", "arbitrary_shell")


def test_wrong_token_and_wrong_grant_work_fail_closed(tmp_path):
    authority, credential, _ = make_authority(tmp_path)
    grant = authority.issue_grant(authority.authenticate(credential), "W28", "pytest_run")
    with pytest.raises(PermissionError, match="execution_grant_invalid"):
        authority.validate_grant_token(grant["grant_id"], "wrong-token")


def test_revocation_is_append_only_and_effective(tmp_path):
    authority, credential, path = make_authority(tmp_path)
    grant = authority.issue_grant(authority.authenticate(credential), "W28", "pytest_run")
    authority.revoke_grant(grant["grant_id"])
    assert authority.get_grant_status(grant["grant_id"])["status"] == "revoked"
    with pytest.raises(PermissionError, match="execution_grant_revoked"):
        authority.validate_grant_token(grant["grant_id"], grant["grant_token"])
    lines = path.read_text(encoding="utf-8").splitlines()
    assert [json.loads(x)["event_type"] for x in lines] == ["GRANT_ISSUED", "GRANT_REVOKED"]


def test_run_record_links_grant_source_exit_and_evidence(tmp_path):
    authority, credential, path = make_authority(tmp_path)
    grant = authority.issue_grant(authority.authenticate(credential), "W28", "pytest_run")
    record = authority.record_run(
        grant["grant_id"],
        grant_token=grant["grant_token"],
        source_sha256="a" * 64,
        exit_status="PASS",
        output_refs=["stdout:run-1", "stderr:run-1"],
        evidence_refs=["evidence:run-1"],
        handoff_ids=["handoff-1"],
    )
    assert record["grant_id"] == grant["grant_id"]
    assert record["source_sha256"] == "a" * 64
    events = AppendOnlyExecutionStore(path).read_events()
    assert [e["event_type"] for e in events] == ["GRANT_ISSUED", "RUN_RECORDED"]
    assert events[-1]["handoff_ids"] == ["handoff-1"]


def test_hash_chain_detects_tampering(tmp_path):
    _, _, path = make_authority(tmp_path)
    store = AppendOnlyExecutionStore(path)
    store.append("TEST_EVENT", {"value": "original"})
    path.write_text(path.read_text(encoding="utf-8").replace("original", "tampered"), encoding="utf-8")
    with pytest.raises(ExecutionAuthorityStoreError, match="execution_store_chain_invalid"):
        store.read_events()


def test_work_paths_cannot_escape_work_root(tmp_path):
    credential = "service-credential-that-is-long-enough-123"
    digest = hashlib.sha256(credential.encode()).hexdigest()
    root = tmp_path / "work"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    with pytest.raises(Exception, match="work_path_outside_root"):
        ExecutionAuthority(
            identity_credential_sha256={"mcp-8020": digest},
            work_policies={
                "W28": {
                    "work_name": "W28",
                    "allowed_identities": ["mcp-8020"],
                    "workspace_root": str(root),
                    "execution_workspace": str(outside),
                    "evidence_root": str(root / "evidence"),
                    "source_sha256": "a" * 64,
                }
            },
            store_path=tmp_path / "authority.jsonl",
        )


def test_http_grant_flow_is_authenticated_and_work_scoped(tmp_path):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from room_hop_mcp.adapter.execution_authority_http import mount_execution_authority_routes

    authority, credential, _ = make_authority(tmp_path)
    app = FastAPI()
    mount_execution_authority_routes(app, authority)
    client = TestClient(app)

    denied = client.post("/works/W28/execution-grants", json={"purpose": "pytest_run"})
    assert denied.status_code == 401

    issued = client.post(
        "/works/W28/execution-grants",
        headers={"X-ROOM-HOP-SERVICE-CREDENTIAL": credential},
        json={"purpose": "pytest_run", "max_timeout_seconds": 60},
    )
    assert issued.status_code == 200
    grant = issued.json()
    assert grant["grant_token"]
    assert grant["work_id"] == "W28"

    wrong_work = client.get(
        f"/works/W29/execution-grants/{grant['grant_id']}",
        headers={"X-ROOM-HOP-SERVICE-CREDENTIAL": credential},
    )
    assert wrong_work.status_code == 403

    status = client.get(
        f"/works/W28/execution-grants/{grant['grant_id']}",
        headers={"X-ROOM-HOP-SERVICE-CREDENTIAL": credential},
    )
    assert status.status_code == 200
    assert status.json()["status"] == "active"

    validated = client.get(
        f"/works/W28/execution-grants/{grant['grant_id']}/validate",
        headers={"Authorization": "Bearer " + grant["grant_token"]},
    )
    assert validated.status_code == 200
    assert validated.json()["status"] == "active"

    recorded = client.post(
        f"/works/W28/execution-grants/{grant['grant_id']}/runs",
        headers={"Authorization": "Bearer " + grant["grant_token"]},
        json={
            "source_sha256": "b" * 64,
            "exit_status": "PASS",
            "output_refs": ["stdout:1"],
            "evidence_refs": ["evidence:1"],
            "handoff_ids": ["handoff:1"],
        },
    )
    assert recorded.status_code == 200
    assert recorded.json()["source_sha256"] == "b" * 64

    revoked = client.post(
        f"/works/W28/execution-grants/{grant['grant_id']}/revoke",
        headers={"Authorization": "Bearer " + grant["grant_token"]},
    )
    assert revoked.status_code == 200
    assert revoked.json()["status"] == "revoked"

    revoked_status = client.get(
        f"/works/W28/execution-grants/{grant['grant_id']}",
        headers={"X-ROOM-HOP-SERVICE-CREDENTIAL": credential},
    )
    assert revoked_status.status_code == 200
    assert revoked_status.json()["status"] == "revoked"

    after_revoke = client.get(
        f"/works/W28/execution-grants/{grant['grant_id']}/validate",
        headers={"Authorization": "Bearer " + grant["grant_token"]},
    )
    assert after_revoke.status_code == 403


def test_unconfigured_authority_returns_503():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from room_hop_mcp.adapter.execution_authority_http import mount_execution_authority_routes

    app = FastAPI()
    mount_execution_authority_routes(app, None)
    response = TestClient(app).post(
        "/works/W28/execution-grants",
        json={"purpose": "pytest_run"},
    )
    assert response.status_code == 503
    assert response.json()["detail"] == "execution_authority_not_configured"
