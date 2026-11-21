"""
Work 10 — HTTP API tests (Gate 2)

Runs the real agent_api.py and isolated execution worker in subprocesses
against the deterministic adapter double (no Chromium needed here), and proves:
  * /health reports service identity and the effective policy;\n  * bearer authentication and exact Origin/preflight boundaries reject hostile callers;
  * a valid workflow returns 200 PASS with evidence;
  * a failing post-condition returns 409 FAIL;
  * an omitted verification invokes the minimum observation check; explicit empty checks return 409 BLOCKED;
  * a destructive action returns 409 BLOCKED;
  * invalid payloads return 400;
  * a timed-out worker is terminated through OS containment before the lease is released.
"""
import hashlib
import json
import os
import platform
import signal
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timedelta, timezone
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def utc_iso(value=None):
    value = value or datetime.now(timezone.utc)
    return value.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def host_architecture():
    machine = platform.machine().casefold()
    return "arm64" if machine in {"arm64", "aarch64"} else "x86_64"
CODE = ROOT / "04_CODE"
TEST_DIR = ROOT / "05_TEST"
FAILED = []


def check(name, fn):
    try:
        outcome = fn()
        if outcome is False:
            raise AssertionError("check returned False")
        print(f"  PASS  {name}")
    except Exception as exc:  # noqa: BLE001
        FAILED.append(f"{name}: {exc}")
        print(f"  FAIL  {name}: {exc}")


class Server:
    def __init__(self):
        self.log_path = Path(tempfile.mkstemp(prefix="work10-fake-", suffix=".log")[1])
        self.host_root = Path(tempfile.mkdtemp(prefix="work10-host-root-"))
        (self.host_root / "sample.txt").write_text("W10_HOST_READ_OK", encoding="utf-8")
        (self.host_root / "test_sample.py").write_text(
            "def test_host_pytest_smoke():\n    assert 6 * 7 == 42\n", encoding="utf-8"
        )
        (self.host_root / "probe.ps1").write_text(
            "Write-Output 'W10_PS_OK'\n", encoding="utf-8"
        )
        env = dict(os.environ)
        validator_schema = ROOT / "06_EVIDENCE" / "W10_P0_ACCEPTANCE_MANIFEST_V8.schema.json"
        validator_policy = ROOT / "06_EVIDENCE" / "W10_P0_CATEGORY_OUTCOME_POLICY_V8.json"
        validator_source = ROOT / "04_CODE" / "acceptance_validator.py"
        self.source_commit = os.getenv("GITHUB_SHA") or ("a" * 40)
        env.update({
            "COMPUTER_AGENT_VALIDATOR_SHA256": sha256_bytes(validator_source.read_bytes()),
            "COMPUTER_AGENT_VALIDATOR_SCHEMA_SHA256": sha256_bytes(validator_schema.read_bytes()),
            "COMPUTER_AGENT_VALIDATOR_POLICY_SHA256": sha256_bytes(validator_policy.read_bytes()),
            "COMPUTER_AGENT_VALIDATOR_HMAC_KEY": "0123456789abcdef" * 4,
            "COMPUTER_AGENT_VALIDATOR_KEY_ID": "W10-CI-TEST-ONLY",
            "COMPUTER_AGENT_VALIDATOR_RUNNER_ID": platform.node(),
            "COMPUTER_AGENT_SOURCE_COMMIT": self.source_commit,
            "COMPUTER_AGENT_PORT": "0",
            "COMPUTER_AGENT_ADAPTER_MODULE": "test_fake_adapter:FakeAdapter",
            "COMPUTER_AGENT_FAKE_LOG": str(self.log_path),
            "COMPUTER_AGENT_ALLOWED_DOMAINS": "127.0.0.1",
            "COMPUTER_AGENT_API_TOKEN": "test-token-work10",
            "COMPUTER_AGENT_ALLOWED_ORIGINS": "http://127.0.0.1:3000",
            "COMPUTER_AGENT_ACTION_TIMEOUT_SECONDS": "0.2",
            "COMPUTER_AGENT_FAKE_SLOW_CLICK_SECONDS": "1.5",
            "COMPUTER_AGENT_ALLOW_LIMITED_PROCESS_GROUP": "1",
            "COMPUTER_AGENT_HOST_ALLOWED_ROOTS": str(self.host_root),
            "COMPUTER_AGENT_HOST_WRITABLE_ROOTS": str(self.host_root),
            "COMPUTER_AGENT_HOST_POWERSHELL_ROOTS": str(self.host_root),
            "COMPUTER_AGENT_HOST_COMMAND_TIMEOUT_SECONDS": "30",
            "PYTHONPATH": f"{CODE}{os.pathsep}{TEST_DIR}{os.pathsep}{env.get('PYTHONPATH', '')}",
            "PYTHONUNBUFFERED": "1",
        })
        self.proc = subprocess.Popen(
            [sys.executable, str(CODE / "agent_api.py")],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env,
            creationflags=(subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0),
        )
        self.port = None
        deadline = time.time() + 10
        while time.time() < deadline:
            line = self.proc.stdout.readline()
            if not line:
                break
            if "listening on" in line:
                self.port = int(line.strip().rsplit(":", 1)[1])
                break
        if not self.port:
            raise RuntimeError(f"server did not start: {self.proc.stdout.read()} "
                               f"{self.proc.stderr.read()}")

    def request(self, method, path, payload=None, headers=None):
        data = None if payload is None else json.dumps(payload).encode()
        request_headers = {"Content-Type": "application/json", "Origin": "http://127.0.0.1:3000",
                           "Authorization": "Bearer test-token-work10"}
        if headers:
            request_headers.update(headers)
        req = urllib.request.Request(f"http://127.0.0.1:{self.port}{path}",
                                     data=data, method=method, headers=request_headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.status, json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read() or b"{}")

    def log(self):
        return self.log_path.read_text(encoding="utf-8").split("\n")

    def stop(self):
        try:
            self.proc.send_signal(
                signal.CTRL_BREAK_EVENT if os.name == "nt" else signal.SIGINT
            )
            self.proc.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=5)
        try:
            server_stderr = self.proc.stderr.read() if self.proc.stderr else ""
            if server_stderr.strip():
                print("  DEBUG API server stderr:", server_stderr[-6000:])
        except Exception:
            pass
        for stream in (self.proc.stdout, self.proc.stderr):
            try:
                stream.close()
            except Exception:
                pass
        shutil.rmtree(self.host_root, ignore_errors=True)


VERIFY = {"checks": [{"field": "text", "contains": "SUBMITTED"}]}
WORKFLOW = {
    "task": "http smoke",
    "actions": [
        {"type": "navigate", "value": "http://127.0.0.1/fake"},
        {"type": "observe"},
        {"type": "click", "target": "Start task"},
        {"type": "type", "target": "Task name", "value": "Work 10 REAL E2E"},
        {"type": "observe"},
    ],
    "verification": VERIFY,
}


def main():
    print("Work 10 — HTTP API Tests")
    print("=" * 58)
    server = Server()
    try:
        status, health = server.request("GET", "/health")
        check("/health -> 200", lambda: status == 200)
        check("/health identifies the service",
              lambda: health.get("service") == "computer-agent" and health.get("status") == "ok")
        check("/health exposes OS containment profile and owner generation",
              lambda: health.get("process_containment_profile") in (
                  "windows-job-object-kill-on-close-v1", "posix-process-group-limited-v1"
              ) and int(health.get("owner_generation") or 0) >= 1)
        check("/health exposes effective policy",
              lambda: health["policy"]["allow_destructive"] is False
              and health["policy"]["max_action_retries"] == 2)
        check("/health reports host capability enablement separately",
              lambda: "run_pytest" in health["host_capabilities"]["supported_operations"]
              and health["host_capabilities"]["write_enabled"] is True
              and health["host_capabilities"]["powershell_enabled"] is (os.name == "nt")
              and "validate_acceptance_manifest" in health["host_capabilities"]["supported_operations"]
              and health["host_capabilities"]["validator_ready"] is True)

        status, body = server.request("GET", "/nope")
        check("unknown GET -> 404", lambda: status == 404)

        status, body = server.request("POST", "/agent/execute", WORKFLOW,
                                      headers={"Authorization": ""})
        check("missing bearer token -> 401", lambda: status == 401 and body.get("error") == "unauthorized")

        status, body = server.request("POST", "/agent/execute", WORKFLOW,
                                      headers={"Authorization": "Bearer wrong-token"})
        check("invalid bearer token -> 401", lambda: status == 401 and body.get("error") == "unauthorized")

        status, body = server.request("POST", "/agent/host/execute",
                                      {"operation": "list_directory", "arguments": {"path": "."}},
                                      headers={"Authorization": ""})
        check("host capability endpoint requires bearer token",
              lambda: status == 401 and body.get("error") == "unauthorized")

        status, body = server.request("POST", "/agent/execute", WORKFLOW,
                                      headers={"Origin": "https://attacker.invalid"})
        check("hostile Origin -> 403", lambda: status == 403 and body.get("error") == "origin_not_allowed")

        status, body = server.request("POST", "/agent/execute", WORKFLOW,
                                      headers={"Origin": ""})
        check("missing Origin -> 403", lambda: status == 403 and body.get("error") == "origin_not_allowed")

        status, body = server.request("POST", "/agent/execute", WORKFLOW,
                                      headers={"Content-Type": "text/plain"})
        check("non-JSON content type -> 415", lambda: status == 415
              and body.get("error") == "content_type_must_be_application_json")

        status, body = server.request("POST", "/agent/execute", WORKFLOW,
                                      headers={"Transfer-Encoding": "chunked"})
        check("chunked transfer encoding rejected -> 400",
              lambda: status == 400 and body.get("error") == "transfer_encoding_not_supported")
        check("unauthorized/hostile requests never start adapter", lambda: not any(server.log()))

        status, body = server.request("OPTIONS", "/agent/execute",
                                      headers={"Access-Control-Request-Method": "POST",
                                               "Access-Control-Request-Headers": "authorization, content-type"})
        check("approved Origin preflight -> 204", lambda: status == 204)

        status, body = server.request("OPTIONS", "/agent/host/execute",
                                      headers={"Access-Control-Request-Method": "POST",
                                               "Access-Control-Request-Headers": "authorization, content-type"})
        check("host capability preflight -> 204", lambda: status == 204)

        status, body = server.request("OPTIONS", "/agent/execute",
                                      headers={"Origin": "https://attacker.invalid",
                                               "Access-Control-Request-Method": "POST",
                                               "Access-Control-Request-Headers": "authorization, content-type"})
        check("hostile Origin preflight -> 403", lambda: status == 403)

        status, body = server.request("OPTIONS", "/agent/execute",
                                      headers={"Access-Control-Request-Method": "GET",
                                               "Access-Control-Request-Headers": "authorization, content-type"})
        check("wrong preflight method -> 403", lambda: status == 403)

        status, body = server.request("OPTIONS", "/other",
                                      headers={"Access-Control-Request-Method": "POST",
                                               "Access-Control-Request-Headers": "authorization, content-type"})
        check("preflight on non-execute path -> 404", lambda: status == 404)

        status, body = server.request("POST", "/agent/execute", [1, 2, 3])
        check("non-object JSON body -> 400", lambda: status == 400 and body.get("error") == "request_body_must_be_object")

        status, body = server.request("POST", "/agent/execute", {"padding": "x" * (1024 * 1024 + 10)})
        check("request body over 1 MiB -> 413", lambda: status == 413 and body.get("error") == "request_body_too_large")

        status, body = server.request("POST", "/agent/execute", {"task": "", "actions": []})
        check("empty task -> 400", lambda: status == 400)

        status, body = server.request("POST", "/agent/execute",
                                      {"task": "t", "actions": [{"type": "do_magic"}]})
        check("unknown action over HTTP -> 400", lambda: status == 400 and "invalid_action" in body["error"])

        status, body = server.request("POST", "/agent/execute", WORKFLOW)
        if status != 200 or body.get("status") != "PASS":
            print("  DEBUG first workflow response:", status, json.dumps(body, ensure_ascii=False, default=str))
            print("  DEBUG fake adapter log:", server.log())
        check("valid workflow -> 200 PASS", lambda: status == 200 and body["status"] == "PASS")
        check("response carries state_trace PLANNED..PASS",
              lambda: body["state_trace"][0] == "PLANNED" and body["state_trace"][-1] == "PASS")
        check("response carries evidence with action_id and timestamp",
              lambda: all(e.get("action_id") and e.get("timestamp")
                          for e in body["evidence"] if e.get("action") != "process_supervisor"))
        check("valid workflow includes verified process-containment evidence",
              lambda: any(e.get("action") == "process_supervisor"
                          and e.get("containment_empty_verified") is True
                          and e.get("ok") is True for e in body.get("evidence", [])))
        check("response carries work_id and timestamps",
              lambda: body["work_id"] == "10" and body["started_at"] and body["finished_at"])
        check("adapter closed after success (no leak)",
              lambda: "start" in server.log() and "close" in server.log())

        before = server.log().count("close")
        mismatch = dict(WORKFLOW, verification={"checks": [{"field": "text", "contains": "ABSENT"}]})
        status, body = server.request("POST", "/agent/execute", mismatch)
        check("failing post-condition -> 409 FAIL",
              lambda: status == 409 and body["status"] == "FAIL")
        check("adapter closed after failure too",
              lambda: server.log().count("close") == before + 1)

        no_verify = dict(WORKFLOW)
        no_verify.pop("verification")
        status, body = server.request("POST", "/agent/execute", no_verify)
        check("omitted verification -> minimum observation check -> 200 PASS",
              lambda: status == 200 and body["status"] == "PASS"
              and any(e.get("verification") == "PASS"
                      and e.get("checks") == [{"kind": "observation_exists"}]
                      for e in body["evidence"]))

        explicit_empty = dict(WORKFLOW, verification={"checks": []})
        starts_before_invalid_verification = server.log().count("start")
        status, body = server.request("POST", "/agent/execute", explicit_empty)
        check("explicit empty verification -> 409 BLOCKED",
              lambda: status == 409 and body["status"] == "BLOCKED"
              and "verification_invalid" in body["error"])
        check("invalid verification rejected before adapter construction",
              lambda: server.log().count("start") == starts_before_invalid_verification)

        destructive = {
            "task": "download",
            "actions": [{"type": "download", "target": "Download evidence"}],
            "verification": VERIFY,
        }
        status, body = server.request("POST", "/agent/execute", destructive)
        check("destructive action -> 409 BLOCKED",
              lambda: status == 409 and "destructive_not_allowed" in body["error"])

        # Separate host capability contract: filesystem and pytest operations
        # are allowlisted and use the same ProcessSupervisor boundary.
        host_list = {"operation": "list_directory", "arguments": {"path": "."}}
        status, host_body = server.request("POST", "/agent/host/execute", host_list)
        check("host list_directory -> 200 PASS",
              lambda: status == 200 and host_body.get("status") == "PASS"
              and any(x.get("name") == "sample.txt" for x in host_body["result"]["entries"]))
        host_read = {"operation": "read_file", "arguments": {"path": "sample.txt"}}
        status, host_body = server.request("POST", "/agent/host/execute", host_read)
        check("host read_file -> 200 PASS with SHA-256",
              lambda: status == 200 and host_body.get("status") == "PASS"
              and host_body["result"].get("content") == "W10_HOST_READ_OK"
              and len(host_body["result"].get("sha256", "")) == 64)
        host_write = {"operation": "write_file", "arguments": {
            "path": "created.txt", "content": "W10_HOST_WRITE_OK"
        }}
        status, host_body = server.request("POST", "/agent/host/execute", host_write)
        check("host write_file -> 200 PASS with read-back",
              lambda: status == 200 and host_body.get("status") == "PASS"
              and host_body["result"].get("readback_verified") is True)
        status, overwrite_body = server.request("POST", "/agent/host/execute", host_write)
        check("host write_file refuses implicit overwrite",
              lambda: status == 409 and overwrite_body.get("status") == "BLOCKED")
        overwrite = {"operation": "write_file", "arguments": {
            "path": "created.txt", "content": "W10_HOST_WRITE_V2", "overwrite": True
        }}
        status, overwrite_body = server.request("POST", "/agent/host/execute", overwrite)
        check("host write_file requires explicit overwrite=true",
              lambda: status == 200 and overwrite_body.get("status") == "PASS"
              and overwrite_body["result"].get("overwritten") is True)
        traversal = {"operation": "read_file", "arguments": {"path": "../outside.txt"}}
        status, traversal_body = server.request("POST", "/agent/host/execute", traversal)
        check("host file traversal outside allowlisted root -> BLOCKED",
              lambda: status == 409 and traversal_body.get("status") == "BLOCKED")
        pytest_request = {"operation": "run_pytest", "arguments": {
            "cwd": str(server.host_root), "paths": ["test_sample.py"]
        }}
        status, pytest_body = server.request("POST", "/agent/host/execute", pytest_request)
        if status != 200 or pytest_body.get("status") != "PASS":
            print("  DEBUG host pytest response:", status, json.dumps(pytest_body, ensure_ascii=False, default=str))
        check("host run_pytest -> 200 PASS",
              lambda: status == 200 and pytest_body.get("status") == "PASS"
              and pytest_body["result"].get("exit_code") == 0)
        # V8 semantic acceptance validator: caller flags are absent; trusted
        # runner recomputes state equality, policy outcomes and artifact hashes.
        fixture_bytes = b'{"fixture":"W10 V8 API fixture"}'
        oracle_bytes = b"W10 V8 API oracle"
        (server.host_root / "fixture.json").write_bytes(fixture_bytes)
        (server.host_root / "oracle.log").write_bytes(oracle_bytes)
        now = datetime.now(timezone.utc)
        v8_state = {
            "outcome": "REJECTED", "admission": "CLOSED", "gate": "CLOSED",
            "process_state": "EXITED", "containment_state": "EMPTY",
            "lease_state": "RELEASED", "owner_state": "CURRENT",
        }
        v8_manifest = {
            "schema_version": "1.2.0", "work_id": "10",
            "profile": {
                "profile_id": "w10-v8-http-test",
                "os_family": "windows" if os.name == "nt" else "linux",
                "support_status": "SUPPORTED",
                "fixture_sha256": sha256_bytes(fixture_bytes),
                "host_build": platform.version(),
                "architecture": host_architecture(),
                "fixture_manifest_ref": "fixture.json",
            },
            "test": {"test_id": "W10-V8-HTTP-001", "category": "SAFETY",
                     "review_revision": "V8"},
            "stimulus": {"injection_point": "host-api-test",
                         "description": "Forbidden host operation is rejected."},
            "expected": dict(v8_state),
            "observed": {**v8_state, "oracle_evidence": [{
                "oracle_id": "HTTP-ORACLE-001", "source": "test_runner",
                "result": "The forbidden operation was rejected.",
                "artifact_ref": "oracle.log",
            }]},
            "artifacts": [
                {"name": "fixture.json", "status": "PRESENT",
                 "sha256": sha256_bytes(fixture_bytes)},
                {"name": "oracle.log", "status": "PRESENT",
                 "sha256": sha256_bytes(oracle_bytes)},
            ],
            "verdict": "PASS", "reviewer": "Co", "recorded_at": utc_iso(now),
            "run_context": {
                "execution_id": str(uuid.uuid4()), "runner_id": platform.node(),
                "source_commit": server.source_commit,
                "started_at": utc_iso(now - timedelta(seconds=2)),
                "finished_at": utc_iso(now - timedelta(seconds=1)),
            },
        }
        (server.host_root / "manifest.json").write_text(
            json.dumps(v8_manifest, ensure_ascii=False), encoding="utf-8"
        )
        validator_request = {"operation": "validate_acceptance_manifest", "arguments": {
            "manifest_path": "manifest.json",
            "evidence_root": str(server.host_root),
            "attestation_path": "attestation.json",
        }}
        status, validator_body = server.request(
            "POST", "/agent/host/execute", validator_request
        )
        check("V8 validator API -> 200 PASS with acceptance eligibility",
              lambda: status == 200 and validator_body.get("status") == "PASS"
              and validator_body["result"].get("acceptance_eligible") is True)
        check("V8 validator writes HMAC-signed attestation",
              lambda: (server.host_root / "attestation.json").is_file()
              and validator_body["result"]["attestation"]["signature"]["algorithm"] == "HMAC-SHA256")
        disallowed_manifest = dict(v8_manifest)
        disallowed_manifest["expected"] = {**v8_state, "outcome": "PASS"}
        disallowed_manifest["observed"] = {
            **v8_state, "outcome": "PASS", "oracle_evidence": v8_manifest["observed"]["oracle_evidence"]
        }
        (server.host_root / "manifest.json").write_text(
            json.dumps(disallowed_manifest, ensure_ascii=False), encoding="utf-8"
        )
        status, validator_bad = server.request(
            "POST", "/agent/host/execute", validator_request
        )
        check("V8 category policy rejects PASS with disallowed SAFETY outcome",
              lambda: status == 409 and validator_bad.get("status") == "FAIL"
              and validator_bad["result"].get("acceptance_eligible") is False)

        powershell_request = {"operation": "run_powershell_script", "arguments": {
            "script": "probe.ps1"
        }}
        status, powershell_body = server.request("POST", "/agent/host/execute", powershell_request)
        if os.name == "nt":
            check("host run_powershell_script -> 200 PASS on Windows",
                  lambda: status == 200 and powershell_body.get("status") == "PASS"
                  and "W10_PS_OK" in powershell_body["result"].get("stdout", ""))
        else:
            check("host run_powershell_script blocked on non-Windows",
                  lambda: status == 409 and powershell_body.get("status") == "BLOCKED")
        check("host operation response includes process-containment evidence",
              lambda: any(e.get("action") == "process_supervisor"
                          and e.get("containment_empty_verified") is True
                          for e in host_body.get("evidence", [])))

        # A timed-out action is executed inside an OS containment. The
        # parent kills the worker tree before returning BLOCKED and releases
        # the request lease only after the containment-empty oracle succeeds.
        slow_workflow = {
            "task": "slow click timeout",
            "actions": [{"type": "click", "target": "slow"}],
            "verification": VERIFY,
        }
        close_before_slow = server.log().count("close")
        status, slow_body = server.request("POST", "/agent/execute", slow_workflow)
        check("timed-out workflow -> 409 BLOCKED",
              lambda: status == 409 and slow_body.get("status") == "BLOCKED"
              and "ActionTimeout" in (slow_body.get("error") or ""))
        slow_supervisor = next(
            (e for e in slow_body.get("evidence", [])
             if e.get("action") == "process_supervisor"), {}
        )
        check("parent verifies contained worker tree empty before response",
              lambda: slow_supervisor.get("containment_empty_verified") is True
              and slow_supervisor.get("forced_cleanup") is True)
        check("timeout terminates worker before late action/close",
              lambda: "click-start:slow" in server.log()
              and "click-end:slow" not in server.log()
              and server.log().count("close") == close_before_slow)
        status, idle_health = server.request("GET", "/health")
        check("health reports execution lease released after containment cleanup",
              lambda: status == 200 and idle_health.get("execution_busy") is False)
        status, body = server.request("POST", "/agent/execute", WORKFLOW)
        check("new workflow permitted after containment cleanup",
              lambda: status == 200 and body.get("status") == "PASS")
    finally:
        server.stop()

    print("\n" + "=" * 58)
    if FAILED:
        print(f"HTTP API tests: {len(FAILED)} FAILED")
        for item in FAILED:
            print(f"  - {item}")
        raise SystemExit(1)
    print("HTTP API tests: ALL PASSED")


if __name__ == "__main__":
    main()
