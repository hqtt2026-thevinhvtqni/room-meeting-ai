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
                }
            },
            store_path=tmp_path / "authority.jsonl",
        )
