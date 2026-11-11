from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from core.execution_authority import AuthorityError, ExecutionAuthority


class AgentRegistryStub:
    def __init__(self, ids=("agent-ka",)):
        self.ids = set(ids)

    def exists(self, principal_id):
        return principal_id in self.ids


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def make_authority(tmp_path: Path) -> tuple[ExecutionAuthority, dict]:
    root = tmp_path / "work-root"
    workspace = root / "workspace"
    evidence = root / "evidence"
    workspace.mkdir(parents=True)
    evidence.mkdir()
    (workspace / "test_sample.py").write_text("def test_ok(): assert True\n", encoding="utf-8")
    source_hash = "a" * 64
    identities = {
        "agent-ka-service": {
            "kind": "agent",
            "principal_id": "agent-ka",
            "credential_sha256": _digest("agent-secret-32-byte-minimum-credential"),
        },
        "host-8031": {
            "kind": "host",
            "credential_sha256": _digest("host-secret-32-byte-minimum-credential"),
        },
    }
    works = {
        "W32": {
            "work_name": "ROOM-HOP-WORK-32",
            "allowed_identities": ["agent-ka-service"],
            "allowed_host_identities": ["host-8031"],
            "allowed_assignments": ["W32-EXECUTION-AUTHORITY"],
            "allowed_tasks": ["W32-P0-PYTEST"],
            "workspace_root": str(root),
            "execution_workspace": str(workspace),
            "evidence_root": str(evidence),
            "source_sha256": source_hash,
            "environment_id": "w32-local-ci",
            "test_entrypoint": ["python", "-m", "pytest", "-q"],
            "max_timeout_seconds": 120,
            "grant_ttl_seconds": 120,
            "policy_version": "W32-EXEC-AUTH-1",
        }
    }
    authority = ExecutionAuthority(
        identities=identities,
        works=works,
        store_path=tmp_path / "authority" / "events.jsonl",
        agent_registry=AgentRegistryStub(),
    )
    request = {
        "purpose": "pytest_run",
        "assignment_id": "W32-EXECUTION-AUTHORITY",
        "task_id": "W32-P0-PYTEST",
        "host_identity_id": "host-8031",
        "source_sha256": source_hash,
        "environment_id": "w32-local-ci",
        "test_entrypoint": ["python", "-m", "pytest", "-q"],
        "requested_timeout_seconds": 60,
    }
    return authority, request


def issue(authority, request):
    return authority.issue_grant(
        work_id="W32",
        service_id="agent-ka-service",
        credential="agent-secret-32-byte-minimum-credential",
        request=request,
    )


def validate(authority, grant):
    return authority.validate_grant(
        work_id="W32",
        grant_id=grant["grant_id"],
        token=grant["grant_token"],
        host_service_id="host-8031",
        host_credential="host-secret-32-byte-minimum-credential",
    )


def test_issue_and_validate_grant_binds_agent_work_task_host_and_source(tmp_path):
    authority, request = make_authority(tmp_path)
    grant = issue(authority, request)
    binding = validate(authority, grant)

    assert binding["work_id"] == "W32"
    assert binding["principal_id"] == "agent-ka"
    assert binding["assignment_id"] == "W32-EXECUTION-AUTHORITY"
    assert binding["task_id"] == "W32-P0-PYTEST"
    assert binding["host_identity_id"] == "host-8031"
    assert binding["source_sha256"] == "a" * 64
    assert binding["test_entrypoint"] == ["python", "-m", "pytest", "-q"]
    assert "token_sha256" not in binding


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        ("assignment_id", "W99-OTHER", "assignment_not_authorized"),
        ("task_id", "UNRELATED-TASK", "task_not_authorized"),
        ("host_identity_id", "untrusted-host", "execution_host_not_authorized"),
        ("source_sha256", "b" * 64, "source_revision_not_authorized"),
        ("environment_id", "production", "execution_environment_not_authorized"),
        ("purpose", "shell", "execution_purpose_not_allowed"),
        ("test_entrypoint", ["python", "-c", "print(1)"], "test_entrypoint_not_authorized"),
    ],
)
def test_issue_denies_out_of_scope_grants(tmp_path, field, value, expected):
    authority, request = make_authority(tmp_path)
    request[field] = value
    with pytest.raises(AuthorityError) as caught:
        issue(authority, request)
    assert caught.value.code == expected


def test_invalid_agent_credential_and_unresolved_principal_are_denied(tmp_path):
    authority, request = make_authority(tmp_path)
    with pytest.raises(AuthorityError, match="service_credential_invalid"):
        authority.issue_grant(
            work_id="W32",
            service_id="agent-ka-service",
            credential="wrong",
            request=request,
        )

    authority.agent_registry = AgentRegistryStub(ids=())
    with pytest.raises(AuthorityError, match="agent_principal_unresolved"):
        issue(authority, request)


def test_wrong_host_identity_and_token_are_denied(tmp_path):
    authority, request = make_authority(tmp_path)
    grant = issue(authority, request)
    with pytest.raises(AuthorityError, match="service_identity_not_enrolled"):
        authority.validate_grant(
            work_id="W32",
            grant_id=grant["grant_id"],
            token=grant["grant_token"],
            host_service_id="other-host",
            host_credential="host-secret-32-byte-minimum-credential",
        )
    with pytest.raises(AuthorityError, match="grant_token_invalid"):
        authority.validate_grant(
            work_id="W32",
            grant_id=grant["grant_id"],
            token="wrong-token",
            host_service_id="host-8031",
            host_credential="host-secret-32-byte-minimum-credential",
        )


def test_revocation_is_online_and_blocks_next_validation(tmp_path):
    authority, request = make_authority(tmp_path)
    grant = issue(authority, request)
    validate(authority, grant)
    revoked = authority.revoke_grant(
        work_id="W32",
        grant_id=grant["grant_id"],
        service_id="agent-ka-service",
        credential="agent-secret-32-byte-minimum-credential",
    )
    assert revoked["status"] == "revoked"
    with pytest.raises(AuthorityError, match="grant_not_active"):
        validate(authority, grant)


def test_run_record_is_bound_to_grant_and_persisted(tmp_path):
    authority, request = make_authority(tmp_path)
    grant = issue(authority, request)
    validate(authority, grant)
    record = {
        "run_id": "run-001",
        "command": ["python", "-m", "pytest", "-q"],
        "source_sha256": "a" * 64,
        "environment_id": "w32-local-ci",
        "started_at": "2026-11-12T00:00:00+00:00",
        "finished_at": "2026-11-12T00:00:01+00:00",
        "status": "PASS",
        "exit_code": 0,
        "evidence_sha256": "c" * 64,
        "evidence_ref": "evidence/run-001/RUN_EVIDENCE.json",
    }
    authority.start_run(
        work_id="W32",
        grant_id=grant["grant_id"],
        token=grant["grant_token"],
        host_service_id="host-8031",
        host_credential="host-secret-32-byte-minimum-credential",
        record={
            "run_id": "run-001",
            "command": ["python", "-m", "pytest", "-q"],
            "source_sha256": "a" * 64,
            "environment_id": "w32-local-ci",
            "started_at": "2026-11-12T00:00:00+00:00",
        },
    )
    result = authority.complete_run(
        work_id="W32",
        grant_id=grant["grant_id"],
        token=grant["grant_token"],
        host_service_id="host-8031",
        host_credential="host-secret-32-byte-minimum-credential",
        record={
            "run_id": "run-001",
            "finished_at": "2026-11-12T00:00:01+00:00",
            "status": "PASS",
            "exit_code": 0,
            "evidence_sha256": "c" * 64,
            "evidence_ref": "evidence/run-001/RUN_EVIDENCE.json",
        },
    )
    assert result == {
        "run_id": "run-001",
        "grant_id": grant["grant_id"],
        "status": "completed",
    }
    events = [
        json.loads(line)
        for line in authority.store_path.read_text(encoding="utf-8").splitlines()
    ]
    assert [event["event_type"] for event in events] == ["grant_issued", "run_started", "run_completed"]
    assert events[-1]["payload"]["principal_id"] == "agent-ka"
    assert events[-1]["payload"]["task_id"] == "W32-P0-PYTEST"


def test_run_start_rejects_command_or_source_mismatch(tmp_path):
    authority, request = make_authority(tmp_path)
    grant = issue(authority, request)
    record = {
        "run_id": "run-bad",
        "command": ["python", "-c", "print(1)"],
        "source_sha256": "b" * 64,
        "environment_id": "w32-local-ci",
        "started_at": "2026-11-12T00:00:00+00:00",
    }
    with pytest.raises(AuthorityError, match="run_source_binding_mismatch"):
        authority.start_run(
            work_id="W32",
            grant_id=grant["grant_id"],
            token=grant["grant_token"],
            host_service_id="host-8031",
            host_credential="host-secret-32-byte-minimum-credential",
            record=record,
        )



def test_grant_is_single_use_after_run_start(tmp_path):
    authority, request = make_authority(tmp_path)
    grant = issue(authority, request)
    start = {
        "run_id": "run-single-1",
        "command": ["python", "-m", "pytest", "-q"],
        "source_sha256": "a" * 64,
        "environment_id": "w32-local-ci",
        "started_at": "2026-11-12T00:00:00+00:00",
    }
    authority.start_run(
        work_id="W32",
        grant_id=grant["grant_id"],
        token=grant["grant_token"],
        host_service_id="host-8031",
        host_credential="host-secret-32-byte-minimum-credential",
        record=start,
    )
    with pytest.raises(AuthorityError, match="grant_already_used"):
        authority.start_run(
            work_id="W32",
            grant_id=grant["grant_id"],
            token=grant["grant_token"],
            host_service_id="host-8031",
            host_credential="host-secret-32-byte-minimum-credential",
            record={**start, "run_id": "run-single-2"},
        )


def test_work_policy_rejects_workspace_symlink_escape(tmp_path):
    authority, request = make_authority(tmp_path)
    root = tmp_path / "work-root"
    workspace = root / "workspace"
    for child in workspace.iterdir():
        if child.is_file():
            child.unlink()
    outside = tmp_path / "outside-workspace"
    outside.mkdir()
    workspace.rmdir()
    try:
        workspace.symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("directory symlink creation is unavailable on this runner")
    with pytest.raises(AuthorityError, match="work_policy_paths_invalid"):
        issue(authority, request)


def test_journal_tampering_fails_closed(tmp_path):
    authority, request = make_authority(tmp_path)
    grant = issue(authority, request)
    raw = authority.store_path.read_text(encoding="utf-8")
    authority.store_path.write_text(raw.replace("grant_issued", "grant_issuEd"), encoding="utf-8")
    with pytest.raises(AuthorityError, match="authority_journal_hash_invalid"):
        validate(authority, grant)
