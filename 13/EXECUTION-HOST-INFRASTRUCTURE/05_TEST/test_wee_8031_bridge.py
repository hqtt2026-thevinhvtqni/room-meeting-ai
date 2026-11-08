import sys
from pathlib import Path
W13_CODE = Path(__file__).resolve().parents[1] / '04_CODE'
if str(W13_CODE) not in sys.path:
    sys.path.insert(0, str(W13_CODE))

import json
from urllib.error import URLError

from execution_host.wee_bridge import ExecutionHostBridge


class FakeTransport:
    def __init__(self, code=200, payload=None, error=None):
        self.code = code
        self.payload = payload or {}
        self.error = error
        self.calls = []

    def __call__(self, url, body, timeout, headers):
        self.calls.append((url, json.loads(body), timeout, dict(headers)))
        if self.error:
            raise self.error
        return self.code, json.dumps(self.payload).encode()


class FakeCoreTransport:
    def __init__(self, code=200, payload=None, error=None):
        self.code = code
        self.payload = payload or {
            "grant_id": "GRANT-test-1",
            "grant_token": "opaque-test-token",
            "work_id": "W28",
            "purpose": "pytest_run",
        }
        self.error = error
        self.calls = []

    def __call__(self, url, body, timeout, headers):
        self.calls.append((url, json.loads(body), timeout, dict(headers)))
        if self.error:
            raise self.error
        return self.code, json.dumps(self.payload).encode()


def context(**overrides):
    value = {"work_id": "W28"}
    value.update(overrides)
    return value


def request_body():
    return {
        "command": ["python3", "-m", "pytest", "-q"],
        "timeout_seconds": 30,
        "collect_artifacts": [],
        "run_test": False,
    }


def bridge(host, core=None, **kwargs):
    return ExecutionHostBridge(
        "http://host:8031",
        transport=host,
        core_endpoint="http://127.0.0.1:8000",
        service_credential="service-credential-test-123456789",
        core_transport=core or FakeCoreTransport(),
        **kwargs,
    )


def test_core_grant_is_obtained_before_host_and_workcontext_is_not_forwarded():
    host = FakeTransport(payload={
        "execution_id": "e-1",
        "work_id": "W28",
        "status": "PASS",
        "exit_code": 0,
        "evidence_ref": "/w/evidence/e-1/FINAL_RESULT.json",
        "stdout": "/w/evidence/e-1/runtime/stdout.log",
        "stderr": "/w/evidence/e-1/runtime/stderr.log",
        "cleanup": {"process_reaped": True},
    })
    core = FakeCoreTransport()
    result = bridge(host, core).invoke(context(authorized=False, workspace_root="/attacker/path"), request_body())
    assert result.status == "PASS"
    assert core.calls[0][0].endswith("/works/W28/execution-grants")
    assert core.calls[0][1] == {"purpose": "pytest_run", "max_timeout_seconds": 30}
    assert host.calls[0][0] == "http://host:8031/execute"
    assert host.calls[0][3]["Authorization"] == "Bearer opaque-test-token"
    assert "work_context" not in host.calls[0][1]
    assert host.calls[0][1]["grant_id"] == "GRANT-test-1"
    assert result.evidence_ref.endswith("FINAL_RESULT.json")


def test_core_denial_prevents_host_network_call():
    host = FakeTransport()
    core = FakeCoreTransport(code=403, payload={"detail": "caller_not_authorized_for_work"})
    result = bridge(host, core).invoke(context(), request_body())
    assert result.status == "BLOCKED"
    assert result.blocker == "core_execution_grant_denied"
    assert not host.calls


def test_missing_service_credential_blocks_without_network():
    host = FakeTransport()
    core = FakeCoreTransport()
    adapter = ExecutionHostBridge(
        "http://host:8031",
        transport=host,
        core_endpoint="http://127.0.0.1:8000",
        service_credential="",
        core_transport=core,
    )
    result = adapter.invoke(context(), request_body())
    assert result.status == "BLOCKED"
    assert result.blocker == "core_service_identity_not_configured"
    assert not host.calls and not core.calls


def test_blocked_host_response_is_not_promoted():
    host = FakeTransport(code=403, payload={"status": "BLOCKED", "reason": "execution_grant_invalid"})
    result = bridge(host).invoke(context(), request_body())
    assert result.status == "BLOCKED"
    assert result.blocker == "execution_host_http_403"


def test_core_network_error_blocks_before_host():
    host = FakeTransport()
    core = FakeCoreTransport(error=TimeoutError("down"))
    result = bridge(host, core).invoke(context(), request_body())
    assert result.status == "BLOCKED"
    assert result.blocker == "core_authority_unreachable"
    assert not host.calls


def test_host_network_error_blocks():
    host = FakeTransport(error=URLError("down"))
    result = bridge(host).invoke(context(), request_body())
    assert result.status == "BLOCKED"
    assert result.blocker == "execution_host_unreachable"


def test_noncanonical_work_and_non_pytest_operation_blocked():
    host = FakeTransport()
    core = FakeCoreTransport()
    result = bridge(host, core).invoke(context(work_id="W-any"), request_body())
    assert result.status == "BLOCKED"
    assert result.blocker == "canonical_work_id_required"
    assert not core.calls and not host.calls

    result = bridge(host, core).invoke(
        context(),
        {"command": ["python3", "-c", "print(1)"], "timeout_seconds": 30},
    )
    assert result.status == "BLOCKED"
    assert result.blocker == "pytest_grant_requires_pytest_command"
    assert not core.calls and not host.calls
