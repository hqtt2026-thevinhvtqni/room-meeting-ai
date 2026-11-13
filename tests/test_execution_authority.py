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
            "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
            "allowed_branches": ["work/32-core-owned-execution-authority-20261112"],
            "allowed_identities": ["agent-ka-service"],
            "allowed_host_identities": ["host-8031"],
            "allowed_assignments": ["W32-EXECUTION-AUTHORITY"],
            "allowed_tasks": ["W32-P0-PYTEST"],
            "workspace_root": str(root),
            "execution_workspace": str(workspace),
            "evidence_root": str(evidence),
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
        "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
        "branch": "work/32-core-owned-execution-authority-20261112",
        "expected_head": "b" * 40,
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
        ("source_sha256", "bad", "source_sha256_invalid"),
        ("environment_id", "production", "execution_environment_not_authorized"),
        ("purpose", "shell", "execution_purpose_not_allowed"),
        ("repository", "attacker/other-repo", "repository_or_branch_not_authorized"),
        ("branch", "main", "repository_or_branch_not_authorized"),
        ("expected_head", "not-a-git-sha", "expected_git_head_invalid"),
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
            "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
            "branch": "work/32-core-owned-execution-authority-20261112",
            "expected_head": "b" * 40,
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
            "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
            "branch": "work/32-core-owned-execution-authority-20261112",
            "expected_head": "b" * 40,
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
            "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
            "branch": "work/32-core-owned-execution-authority-20261112",
            "expected_head": "b" * 40,
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
        "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
        "branch": "work/32-core-owned-execution-authority-20261112",
        "expected_head": "b" * 40,
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
        "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
        "branch": "work/32-core-owned-execution-authority-20261112",
        "expected_head": "b" * 40,
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



def test_revocation_blocks_new_run_but_allows_existing_run_completion(tmp_path):
    authority, request = make_authority(tmp_path)
    grant = issue(authority, request)
    start_record = {
        "run_id": "run-revoked-after-start",
        "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
        "branch": "work/32-core-owned-execution-authority-20261112",
        "expected_head": "b" * 40,
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
        record=start_record,
    )
    authority.revoke_grant(
        work_id="W32",
        grant_id=grant["grant_id"],
        service_id="agent-ka-service",
        credential="agent-secret-32-byte-minimum-credential",
    )
    with pytest.raises(AuthorityError, match="grant_not_active"):
        authority.start_run(
            work_id="W32",
            grant_id=grant["grant_id"],
            token=grant["grant_token"],
            host_service_id="host-8031",
            host_credential="host-secret-32-byte-minimum-credential",
            record={**start_record, "run_id": "run-after-revoke"},
        )

    completed = authority.complete_run(
        work_id="W32",
        grant_id=grant["grant_id"],
        token=grant["grant_token"],
        host_service_id="host-8031",
        host_credential="host-secret-32-byte-minimum-credential",
        record={
            "run_id": "run-revoked-after-start",
        "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
        "branch": "work/32-core-owned-execution-authority-20261112",
        "expected_head": "b" * 40,
            "finished_at": "2026-11-12T00:00:02+00:00",
            "status": "BLOCKED",
            "exit_code": None,
            "evidence_sha256": "d" * 64,
        },
    )
    assert completed["status"] == "completed"
    events = [
        json.loads(line)
        for line in authority.store_path.read_text(encoding="utf-8").splitlines()
    ]
    assert [event["event_type"] for event in events] == [
        "grant_issued", "run_started", "grant_revoked", "run_completed"
    ]
    assert events[-1]["payload"]["grant_status_at_completion"] == "revoked"



def test_concurrent_core_instances_append_valid_hash_chain(tmp_path):
    from concurrent.futures import ThreadPoolExecutor

    authority, request = make_authority(tmp_path)
    second = ExecutionAuthority(
        identities=authority.identities,
        works=authority.works,
        store_path=authority.store_path,
        agent_registry=AgentRegistryStub(),
    )
    services = [authority, second]

    def issue_one(index):
        return issue(services[index % 2], dict(request))

    with ThreadPoolExecutor(max_workers=8) as pool:
        grants = list(pool.map(issue_one, range(16)))

    ids = [grant["grant_id"] for grant in grants]
    assert len(set(ids)) == 16
    events = [
        json.loads(line)
        for line in authority.store_path.read_text(encoding="utf-8").splitlines()
    ]
    assert len(events) == 16
    assert all(event["event_type"] == "grant_issued" for event in events)
    for grant in grants:
        assert authority.grant_status(
            work_id="W32",
            grant_id=grant["grant_id"],
            service_id="agent-ka-service",
            credential="agent-secret-32-byte-minimum-credential",
        )["status"] == "active"



def test_work_policy_rejects_evidence_inside_source_workspace(tmp_path):
    authority, request = make_authority(tmp_path)
    evidence_inside = Path(authority.works["W32"]["execution_workspace"]) / "evidence"
    evidence_inside.mkdir()
    authority.works["W32"]["evidence_root"] = str(evidence_inside)
    with pytest.raises(AuthorityError, match="work_policy_paths_invalid"):
        issue(authority, request)


def test_journal_tampering_fails_closed(tmp_path):
    authority, request = make_authority(tmp_path)
    grant = issue(authority, request)
    raw = authority.store_path.read_text(encoding="utf-8")
    authority.store_path.write_text(raw.replace("grant_issued", "grant_issuEd"), encoding="utf-8")
    with pytest.raises(AuthorityError, match="authority_journal_hash_invalid"):
        validate(authority, grant)


def test_expired_grant_can_be_revoked_and_revocation_is_idempotent(tmp_path):
    from datetime import datetime, timedelta

    authority, request = make_authority(tmp_path)
    grant = issue(authority, request)
    expiry = datetime.fromisoformat(grant["expires_at"])
    authority.clock = lambda: expiry + timedelta(seconds=1)

    revoked = authority.revoke_grant(
        work_id="W32",
        grant_id=grant["grant_id"],
        service_id="agent-ka-service",
        credential="agent-secret-32-byte-minimum-credential",
    )
    assert revoked["status"] == "revoked"

    repeated = authority.revoke_grant(
        work_id="W32",
        grant_id=grant["grant_id"],
        service_id="agent-ka-service",
        credential="agent-secret-32-byte-minimum-credential",
    )
    assert repeated == revoked

    events = [
        json.loads(line)
        for line in authority.store_path.read_text(encoding="utf-8").splitlines()
    ]
    assert [event["event_type"] for event in events] == [
        "grant_issued", "grant_revoked"
    ]


def test_authority_store_must_be_outside_work_scope(tmp_path):
    authority, _ = make_authority(tmp_path)
    work_root = Path(authority.works["W32"]["workspace_root"])

    with pytest.raises(AuthorityError, match="authority_store_inside_work_scope"):
        ExecutionAuthority(
            identities=authority.identities,
            works=authority.works,
            store_path=work_root / "authority" / "events.jsonl",
            agent_registry=AgentRegistryStub(),
        )


def test_authority_store_path_must_be_absolute(tmp_path):
    authority, _ = make_authority(tmp_path)

    with pytest.raises(AuthorityError, match="authority_store_path_must_be_absolute"):
        ExecutionAuthority(
            identities=authority.identities,
            works=authority.works,
            store_path="relative-authority/events.jsonl",
            agent_registry=AgentRegistryStub(),
        )


def _start_completion_validation_run(authority, grant, run_id="run-completion-validation"):
    authority.start_run(
        work_id="W32",
        grant_id=grant["grant_id"],
        token=grant["grant_token"],
        host_service_id="host-8031",
        host_credential="host-secret-32-byte-minimum-credential",
        record={
            "run_id": run_id,
            "repository": "hqtt2026-thevinhvtqni/room-meeting-ai",
            "branch": "work/32-core-owned-execution-authority-20261112",
            "expected_head": "b" * 40,
            "command": ["python", "-m", "pytest", "-q"],
            "source_sha256": "a" * 64,
            "environment_id": "w32-local-ci",
            "started_at": "2026-11-12T00:00:00+00:00",
        },
    )


def _complete_validation_run(authority, grant, run_id="run-completion-validation", **overrides):
    record = {
        "run_id": run_id,
        "finished_at": "2026-11-12T00:00:01+00:00",
        "status": "PASS",
        "exit_code": 0,
        "evidence_sha256": "c" * 64,
    }
    record.update(overrides)
    return authority.complete_run(
        work_id="W32",
        grant_id=grant["grant_id"],
        token=grant["grant_token"],
        host_service_id="host-8031",
        host_credential="host-secret-32-byte-minimum-credential",
        record=record,
    )


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        ("status", "UNKNOWN", "run_completion_status_invalid"),
        ("status", [], "run_completion_status_invalid"),
        ("execution_status", "UNKNOWN", "run_execution_status_invalid"),
        ("execution_status", {}, "run_execution_status_invalid"),
        ("finished_at", "not-a-date", "run_finished_at_invalid"),
        ("finished_at", "2026-11-12T00:00:01", "run_finished_at_timezone_required"),
        ("exit_code", True, "run_exit_code_invalid"),
        ("exit_code", "0", "run_exit_code_invalid"),
        ("evidence_sha256", "A" * 64, "run_evidence_sha256_invalid"),
        ("evidence_sha256", "bad", "run_evidence_sha256_invalid"),
        ("stdout_sha256", "bad", "run_stdout_sha256_invalid"),
        ("stderr_sha256", "A" * 64, "run_stderr_sha256_invalid"),
        ("evidence_ref", "", "run_evidence_ref_invalid"),
        ("evidence_persisted", "false", "run_evidence_persisted_invalid"),
        ("evidence_errors", "disk_full", "run_evidence_errors_invalid"),
        ("evidence_errors", ["x" * 257], "run_evidence_errors_invalid"),
        ("evidence_errors", ["disk_full"], "run_evidence_persistence_metadata_invalid"),
        ("evidence_persisted", False, "run_evidence_persistence_metadata_invalid"),
    ],
)
def test_complete_run_rejects_invalid_completion_fields(
    tmp_path, field, value, expected
):
    authority, request = make_authority(tmp_path)
    grant = issue(authority, request)
    _start_completion_validation_run(authority, grant)

    with pytest.raises(AuthorityError) as caught:
        _complete_validation_run(authority, grant, **{field: value})

    assert caught.value.code == expected


@pytest.mark.parametrize(
    ("status", "execution_status"),
    [
        ("BLOCKED", "BLOCKED"),
        ("TIMEOUT", "TIMEOUT"),
    ],
)
def test_complete_run_accepts_nonzero_or_unavailable_exit_code_states(
    tmp_path, status, execution_status
):
    authority, request = make_authority(tmp_path)
    grant = issue(authority, request)
    _start_completion_validation_run(authority, grant)

    result = _complete_validation_run(
        authority,
        grant,
        status=status,
        execution_status=execution_status,
        exit_code=None,
    )

    assert result["status"] == "completed"
