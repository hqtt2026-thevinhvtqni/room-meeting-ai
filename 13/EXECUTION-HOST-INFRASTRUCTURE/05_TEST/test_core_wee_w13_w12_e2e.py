from __future__ import annotations

import hashlib
import json
import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

W13_CODE = Path(__file__).resolve().parents[1] / "04_CODE"
if str(W13_CODE) in sys.path:
    sys.path.remove(str(W13_CODE))
sys.path.insert(0, str(W13_CODE))
for _name in tuple(sys.modules):
    if _name == "execution_host" or _name.startswith("execution_host."):
        del sys.modules[_name]
for _name in tuple(sys.modules):
    if _name == "wee" or _name.startswith("wee."):
        del sys.modules[_name]

from core.execution_authority import ExecutionAuthority
from room_hop_mcp.adapter.execution_authority_http import mount_execution_authority_routes
from execution_host.identity import RuntimeIdentity
from execution_host.server import CoreAuthorityError, Handler
from execution_host.source_snapshot import workspace_source_sha256
from execution_host.w12_adapter import W12ExecutionAdapter
from execution_host.wee_bridge import ExecutionHostBridge


class CoreHttpAdapter:
    """Routes Host introspection and run writes through the real Core FastAPI app."""

    def __init__(self, client):
        self.client = client

    def validate_grant(self, work_id, grant_id, token):
        response = self.client.get(
            f"/works/{work_id}/execution-grants/{grant_id}/validate",
            headers={"Authorization": "Bearer " + token},
        )
        if response.status_code != 200:
            raise CoreAuthorityError(response.status_code, "core_execution_grant_denied")
        return response.json()

    def record_run(self, work_id, grant_id, token, payload):
        response = self.client.post(
            f"/works/{work_id}/execution-grants/{grant_id}/runs",
            headers={"Authorization": "Bearer " + token},
            json=payload,
        )
        if response.status_code != 200:
            raise CoreAuthorityError(response.status_code, "core_run_record_failed")
        return response.json()


def test_full_core_wee_w13_w12_execution_and_core_run_record(tmp_path):
    workspace_root = tmp_path / "work-root"
    workspace = workspace_root / "W28"
    evidence = workspace_root / "W28-EVIDENCE"
    workspace.mkdir(parents=True)
    evidence.mkdir()
    (workspace / "test_sample.py").write_text(
        "def test_authorized_work_execution():\n    assert 7 * 6 == 42\n",
        encoding="utf-8",
    )
    source_hash = workspace_source_sha256(workspace)
    credential = "mcp-service-credential-with-high-entropy-test-value"
    authority = ExecutionAuthority(
        identity_credential_sha256={
            "mcp-8020": hashlib.sha256(credential.encode("utf-8")).hexdigest()
        },
        work_policies={
            "W28": {
                "work_name": "MCP-8020-TOOLING-PLATFORM",
                "allowed_identities": ["mcp-8020"],
                "workspace_root": str(workspace_root),
                "execution_workspace": str(workspace),
                "evidence_root": str(evidence),
                "source_sha256": source_hash,
                "allowed_purposes": ["pytest_run"],
            }
        },
        store_path=tmp_path / "core-authority.jsonl",
    )
    app = FastAPI()
    mount_execution_authority_routes(app, authority)

    with TestClient(app) as core_client:
        core_adapter = CoreHttpAdapter(core_client)
        identity = RuntimeIdentity(bind_address="127.0.0.1:0")
        Handler.runtime_identity = identity
        Handler.host = W12ExecutionAdapter(allow_processes=True, runtime_identity=identity)
        Handler.core = core_adapter
        host_server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        host_thread = threading.Thread(target=host_server.serve_forever, daemon=True)
        host_thread.start()

        def core_transport(url, body, timeout, headers):
            from urllib.parse import urlsplit
            response = core_client.post(urlsplit(url).path, content=body, headers=headers)
            return response.status_code, response.content

        try:
            bridge = ExecutionHostBridge(
                endpoint=f"http://127.0.0.1:{host_server.server_address[1]}",
                core_endpoint="http://127.0.0.1:8000",
                service_credential=credential,
                core_transport=core_transport,
            )
            result = bridge.invoke(
                {"work_id": "W28", "authorized": False, "workspace_root": "C:/caller-forged"},
                {
                    "command": ["python", "-m", "pytest", "-q"],
                    "timeout_seconds": 30.0,
                    "collect_artifacts": [],
                    "run_test": False,
                },
            )
        finally:
            host_server.shutdown()
            host_server.server_close()
            host_thread.join(timeout=3)
            Handler.host = None
            Handler.core = None
            Handler.runtime_identity = None

        assert result.status == "PASS"
        assert result.work_id == "W28"
        assert Path(result.evidence_ref).is_file()
        evidence_data = json.loads(Path(result.evidence_ref).read_text(encoding="utf-8"))
        assert evidence_data["source_sha256"] == source_hash
        assert evidence_data["process_tree_cleanup_verified"] is True
        events = authority.store.read_events()
        assert [event["event_type"] for event in events] == ["GRANT_ISSUED", "RUN_RECORDED"]
        assert events[-1]["source_sha256"] == source_hash
        assert events[-1]["exit_status"] == "PASS"
        assert credential not in (tmp_path / "core-authority.jsonl").read_text(encoding="utf-8")
