from __future__ import annotations

import json
import sys
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

W13_CODE = Path(__file__).resolve().parents[1] / "04_CODE"
if str(W13_CODE) not in sys.path:
    sys.path.insert(0, str(W13_CODE))

from execution_host.identity import RuntimeIdentity
from execution_host.models import ExecutionRequest
from execution_host.server import CoreAuthorityError, Handler
from execution_host.source_snapshot import workspace_source_sha256
from execution_host.w12_adapter import W12ExecutionAdapter


class FakeCore:
    def __init__(self, grant):
        self.grant = grant
        self.runs = []
        self.validations = []

    def validate_grant(self, work_id, grant_id, token):
        self.validations.append((work_id, grant_id, token))
        if token != "test-grant-token":
            raise CoreAuthorityError(403, "core_execution_grant_denied")
        return dict(self.grant)

    def record_run(self, work_id, grant_id, token, payload):
        assert token == "test-grant-token"
        self.runs.append((work_id, grant_id, dict(payload)))
        return {"event_type": "RUN_RECORDED"}


def post(server, body, token="test-grant-token"):
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        f"http://127.0.0.1:{server.server_address[1]}/execute",
        data=data,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + token},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))


def test_core_grant_to_w12_real_host_and_append_only_run_record(tmp_path):
    work_root = tmp_path / "W28"
    workspace = work_root / "workspace"
    evidence = work_root / "evidence"
    workspace.mkdir(parents=True)
    evidence.mkdir()
    (workspace / "test_sample.py").write_text(
        "def test_core_grant_reaches_real_w12_host():\n    assert 2 + 2 == 4\n",
        encoding="utf-8",
    )
    source_hash = workspace_source_sha256(workspace)
    grant = {
        "status": "active",
        "grant_id": "GRANT-test",
        "work_id": "W28",
        "work_name": "MCP-8020-TOOLING-PLATFORM",
        "purpose": "pytest_run",
        "max_timeout_seconds": 30,
        "workspace_root": str(work_root),
        "execution_workspace": str(workspace),
        "evidence_root": str(evidence),
        "source_sha256": source_hash,
    }
    core = FakeCore(grant)
    identity = RuntimeIdentity(bind_address="127.0.0.1:0")
    Handler.runtime_identity = identity
    Handler.host = W12ExecutionAdapter(allow_processes=True, runtime_identity=identity)
    Handler.core = core
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        status, result = post(server, {
            "work_id": "W28",
            "grant_id": "GRANT-test",
            "purpose": "pytest_run",
            "execution_request": {
                "command": ["python", "-m", "pytest", "-q"],
                "timeout_seconds": 30.0,
                "collect_artifacts": [],
                "run_test": False,
            },
        })
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
        Handler.host = None
        Handler.core = None
        Handler.runtime_identity = None

    assert status == 200
    assert result["status"] == "PASS"
    assert Path(result["evidence_ref"]).is_file()
    evidence_data = json.loads(Path(result["evidence_ref"]).read_text(encoding="utf-8"))
    assert evidence_data["source_sha256"] == source_hash
    assert core.validations == [("W28", "GRANT-test", "test-grant-token")]
    assert len(core.runs) == 1
    run = core.runs[0][2]
    assert run["source_sha256"] == source_hash
    assert run["exit_status"] == "PASS"
    assert run["evidence_refs"] == [result["evidence_ref"]]


def test_old_caller_supplied_work_context_is_rejected(tmp_path):
    identity = RuntimeIdentity(bind_address="127.0.0.1:0")
    Handler.runtime_identity = identity
    Handler.host = W12ExecutionAdapter(allow_processes=True, runtime_identity=identity)
    Handler.core = FakeCore({})
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        status, result = post(server, {
            "work_context": {
                "work_id": "W28",
                "work_name": "forged",
                "workspace_root": str(tmp_path),
                "execution_workspace": str(tmp_path),
                "evidence_root": str(tmp_path),
                "authorized": True,
            },
            "execution_request": {"command": ["python", "-m", "pytest", "-q"]},
        })
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
        Handler.host = None
        Handler.core = None
        Handler.runtime_identity = None
    assert status == 400
    assert result["reason"] == "request_contract_invalid"


def test_wrong_bearer_grant_is_denied_before_execution(tmp_path):
    work_root = tmp_path / "W28"
    workspace = work_root / "workspace"
    evidence = work_root / "evidence"
    workspace.mkdir(parents=True)
    evidence.mkdir()
    grant = {
        "status": "active", "work_id": "W28", "work_name": "W28",
        "purpose": "pytest_run", "max_timeout_seconds": 30,
        "workspace_root": str(work_root), "execution_workspace": str(workspace),
        "evidence_root": str(evidence), "source_sha256": workspace_source_sha256(workspace),
    }
    core = FakeCore(grant)
    identity = RuntimeIdentity(bind_address="127.0.0.1:0")
    Handler.runtime_identity = identity
    Handler.host = W12ExecutionAdapter(allow_processes=True, runtime_identity=identity)
    Handler.core = core
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        status, result = post(server, {
            "work_id": "W28", "grant_id": "GRANT-test", "purpose": "pytest_run",
            "execution_request": {
                "command": ["python", "-m", "pytest", "-q"],
                "timeout_seconds": 30.0, "collect_artifacts": [], "run_test": False,
            },
        }, token="invalid-token")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
        Handler.host = None
        Handler.core = None
        Handler.runtime_identity = None
    assert status == 403
    assert result["reason"] == "core_execution_grant_denied"
    assert core.runs == []
