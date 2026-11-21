"""
Work 10 — HTTP API tests (Gate 2)

Runs the real agent_api.py in a subprocess against the deterministic adapter
double (no Chromium needed here), and proves:
  * /health reports service identity and the effective policy;\n  * bearer authentication and exact Origin/preflight boundaries reject hostile callers;
  * a valid workflow returns 200 PASS with evidence;
  * a failing post-condition returns 409 FAIL;
  * an omitted verification invokes the minimum observation check; explicit empty checks return 409 BLOCKED;
  * a destructive action returns 409 BLOCKED;
  * invalid payloads return 400;
  * the adapter is closed on every path (lifecycle, no leak).
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
        env = dict(os.environ)
        env.update({
            "COMPUTER_AGENT_PORT": "0",
            "COMPUTER_AGENT_ADAPTER_MODULE": "test_fake_adapter:FakeAdapter",
            "COMPUTER_AGENT_FAKE_LOG": str(self.log_path),
            "COMPUTER_AGENT_ALLOWED_DOMAINS": "127.0.0.1",
            "COMPUTER_AGENT_API_TOKEN": "test-token-work10",
            "COMPUTER_AGENT_ALLOWED_ORIGINS": "http://127.0.0.1:3000",
            "COMPUTER_AGENT_ACTION_TIMEOUT_SECONDS": "0.2",
            "COMPUTER_AGENT_FAKE_SLOW_CLICK_SECONDS": "1.5",
            "PYTHONPATH": f"{CODE}{os.pathsep}{TEST_DIR}{os.pathsep}{env.get('PYTHONPATH', '')}",
            "PYTHONUNBUFFERED": "1",
        })
        self.proc = subprocess.Popen(
            [sys.executable, str(CODE / "agent_api.py")],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env,
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
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        for stream in (self.proc.stdout, self.proc.stderr):
            try:
                stream.close()
            except Exception:
                pass


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
        check("/health exposes effective policy",
              lambda: health["policy"]["allow_destructive"] is False
              and health["policy"]["max_action_retries"] == 2)

        status, body = server.request("GET", "/nope")
        check("unknown GET -> 404", lambda: status == 404)

        status, body = server.request("POST", "/agent/execute", WORKFLOW,
                                      headers={"Authorization": ""})
        check("missing bearer token -> 401", lambda: status == 401 and body.get("error") == "unauthorized")

        status, body = server.request("POST", "/agent/execute", WORKFLOW,
                                      headers={"Authorization": "Bearer wrong-token"})
        check("invalid bearer token -> 401", lambda: status == 401 and body.get("error") == "unauthorized")

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
        check("valid workflow -> 200 PASS", lambda: status == 200 and body["status"] == "PASS")
        check("response carries state_trace PLANNED..PASS",
              lambda: body["state_trace"][0] == "PLANNED" and body["state_trace"][-1] == "PASS")
        check("response carries evidence with action_id and timestamp",
              lambda: all(e.get("action_id") and e.get("timestamp") for e in body["evidence"]))
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

        # Production-shaped regression: request A times out while its adapter
        # worker remains alive; request B must not construct/dispatch a new adapter.
        slow_workflow = {
            "task": "slow click timeout",
            "actions": [{"type": "click", "target": "slow"}],
            "verification": VERIFY,
        }
        close_before_slow = server.log().count("close")
        starts_before_slow = server.log().count("start")
        status, slow_body = server.request("POST", "/agent/execute", slow_workflow)
        check("timed-out workflow -> 409 BLOCKED",
              lambda: status == 409 and slow_body.get("status") == "BLOCKED"
              and "ActionTimeout" in (slow_body.get("error") or ""))
        check("timed-out adapter is not closed while worker remains active",
              lambda: "click-start:slow" in server.log()
              and "click-end:slow" not in server.log()
              and server.log().count("close") == close_before_slow)
        status, busy_health = server.request("GET", "/health")
        check("health reports execution_busy during orphan worker",
              lambda: status == 200 and busy_health.get("execution_busy") is True)

        status, busy_body = server.request("POST", "/agent/execute", WORKFLOW)
        check("cross-request dispatch blocked while orphan worker is active",
              lambda: status == 409 and busy_body.get("error") == "execution_busy")
        check("busy request does not construct another adapter",
              lambda: server.log().count("start") == starts_before_slow + 1)

        time.sleep(1.6)
        status, idle_health = server.request("GET", "/health")
        check("health clears execution_busy after deferred cleanup",
              lambda: status == 200 and idle_health.get("execution_busy") is False)
        event_log = server.log()
        check("deferred adapter close occurs only after timed-out worker exits",
              lambda: event_log.index("click-end:slow") < event_log.index("close", event_log.index("click-end:slow")))
        slow_start_index = event_log.index("click-start:slow")
        slow_end_index = event_log.index("click-end:slow")
        start_thread_ids = [
            line.split(":", 1)[1] for line in event_log[:slow_start_index]
            if line.startswith("start-thread:")
        ]
        slow_thread_ids = [
            line.split(":", 1)[1] for line in event_log[slow_start_index:slow_end_index + 2]
            if line.startswith(("click-start-thread:", "click-end-thread:"))
        ]
        close_thread_ids = [
            line.split(":", 1)[1] for line in event_log[slow_end_index + 1:]
            if line.startswith("close-thread:")
        ]
        same_owner_thread = (
            bool(start_thread_ids and close_thread_ids)
            and len(slow_thread_ids) == 2
            and len({start_thread_ids[-1], *slow_thread_ids, close_thread_ids[0]}) == 1
        )
        if not same_owner_thread:
            print("  DEBUG thread ownership:", {
                "start_thread_ids": start_thread_ids,
                "slow_thread_ids": slow_thread_ids,
                "close_thread_ids": close_thread_ids,
                "event_log": event_log,
            })
        check("adapter start, action and deferred close share one owner thread",
              lambda: same_owner_thread)
        status, body = server.request("POST", "/agent/execute", WORKFLOW)
        check("new workflow permitted after orphan worker cleanup",
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
