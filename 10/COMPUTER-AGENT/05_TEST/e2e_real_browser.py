"""Cross-platform real-browser E2E through the actual HTTP API + OS supervisor.

This test does not instantiate AgentRuntime in the test process. It starts the
Agent API, submits the workflow over HTTP, and therefore exercises the worker
subprocess, Windows Job Object / limited POSIX process-group boundary, host
owner lease, durable run journal and real Chromium adapter.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


WORK_ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = WORK_ROOT / "04_CODE"
TEST_DIR = WORK_ROOT / "05_TEST"
EVIDENCE_DIR = WORK_ROOT / "06_EVIDENCE"
RESULT_PATH = EVIDENCE_DIR / "real-browser-e2e-result.json"
SCREENSHOT_PATH = EVIDENCE_DIR / "real-browser-e2e.png"
API_TOKEN = "work10-ci-real-browser-token"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return


def stop_process(proc: subprocess.Popen | None) -> None:
    if proc is None or proc.poll() is not None:
        return
    try:
        proc.send_signal(signal.CTRL_BREAK_EVENT if os.name == "nt" else signal.SIGINT)
        proc.wait(timeout=8)
    except (OSError, subprocess.TimeoutExpired):
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)


def start_api_server():
    env = dict(os.environ)
    env.update({
        "COMPUTER_AGENT_PORT": "0",
        "COMPUTER_AGENT_HOST": "127.0.0.1",
        "COMPUTER_AGENT_API_TOKEN": API_TOKEN,
        "COMPUTER_AGENT_ALLOWED_ORIGINS": "http://127.0.0.1:3000",
        "COMPUTER_AGENT_ALLOWED_DOMAINS": "127.0.0.1",
        "COMPUTER_AGENT_ALLOWED_PATHS": "06_EVIDENCE",
        "COMPUTER_AGENT_HEADLESS": "1",
        "COMPUTER_AGENT_ALLOW_DESTRUCTIVE": "1",
        "COMPUTER_AGENT_ACTION_TIMEOUT_SECONDS": "20",
        "COMPUTER_AGENT_OBSERVATION_TIMEOUT_SECONDS": "15",
        "COMPUTER_AGENT_WORKFLOW_TIMEOUT_SECONDS": "180",
        "COMPUTER_AGENT_WORK_ROOT": str(WORK_ROOT),
        "COMPUTER_AGENT_ALLOW_LIMITED_PROCESS_GROUP": "1",
        "PYTHONPATH": f"{CODE_DIR}{os.pathsep}{env.get('PYTHONPATH', '')}",
        "PYTHONUNBUFFERED": "1",
    })
    proc = subprocess.Popen(
        [sys.executable, str(CODE_DIR / "agent_api.py")],
        cwd=str(WORK_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        creationflags=(subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0),
        start_new_session=(os.name != "nt"),
    )
    deadline = time.monotonic() + 15
    port = None
    startup_lines = []
    while time.monotonic() < deadline:
        line = proc.stdout.readline()
        if line:
            startup_lines.append(line.rstrip())
            if "listening on" in line:
                port = int(line.strip().rsplit(":", 1)[1])
                break
        elif proc.poll() is not None:
            break
    if not port:
        stderr = proc.stderr.read() if proc.stderr else ""
        stop_process(proc)
        raise RuntimeError(
            "Agent API did not start. stdout=" + " | ".join(startup_lines)
            + " stderr=" + stderr[-4000:]
        )
    return proc, port


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    started_at = utc_now()
    target = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        partial(QuietHandler, directory=str(TEST_DIR)),
    )
    target_port = target.server_address[1]
    target_thread = threading.Thread(target=target.serve_forever, daemon=True)
    target_thread.start()

    api_proc = None
    result_payload = {
        "status": "FAIL",
        "started_at": started_at,
        "host": {
            "python": sys.version,
            "platform": sys.platform,
            "os_name": os.name,
            "release": __import__("platform").release(),
            "version": __import__("platform").version(),
            "machine": __import__("platform").machine(),
        },
        "commit_sha": os.getenv("GITHUB_SHA"),
        "api_mode": "HTTP + isolated worker process",
        "target_url": f"http://127.0.0.1:{target_port}/browser_e2e_target.html",
    }
    http_status = None
    body = {}
    try:
        api_proc, api_port = start_api_server()
        result_payload["api_port"] = api_port
        workflow = {
            "task": "Work 10 real browser end-to-end",
            "actions": [
                {"type": "navigate", "value": result_payload["target_url"]},
                {"type": "observe"},
                {"type": "click", "target": "Start task"},
                {"type": "type", "target": "Task name", "value": "Work 10 REAL E2E"},
                {"type": "key_press", "value": "TAB"},
                {"type": "scroll", "value": 500},
                {"type": "click", "target": "Submit task"},
                {"type": "wait", "value": 0.2},
                {"type": "observe"},
                {"type": "extract", "target": "#result"},
                {"type": "screenshot", "args": {"path": "06_EVIDENCE/real-browser-e2e.png"}},
                {"type": "download", "target": "Download evidence"},
                {"type": "observe"},
            ],
            "verification": {
                "checks": [
                    {"field": "text", "contains": "SUBMITTED"},
                    {"field": "text", "contains": "Work 10 REAL E2E"},
                ]
            },
        }
        request = urllib.request.Request(
            f"http://127.0.0.1:{api_port}/agent/execute",
            data=json.dumps(workflow).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Origin": "http://127.0.0.1:3000",
                "Authorization": f"Bearer {API_TOKEN}",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=210) as response:
                http_status = response.status
                body = json.loads(response.read() or b"{}")
        except urllib.error.HTTPError as exc:
            http_status = exc.code
            body = json.loads(exc.read() or b"{}")

        supervisor = next(
            (item for item in body.get("evidence", [])
             if item.get("action") == "process_supervisor"),
            {},
        )
        screenshot_ok = SCREENSHOT_PATH.exists() and SCREENSHOT_PATH.stat().st_size > 0
        result_payload.update({
            "http_status": http_status,
            "api_result": body,
            "state_trace": body.get("state_trace", []),
            "step_count": len(body.get("steps", [])),
            "evidence_count": len(body.get("evidence", [])),
            "process_supervisor_evidence": supervisor,
            "screenshot": {
                "path": str(SCREENSHOT_PATH.relative_to(WORK_ROOT)).replace("\\", "/"),
                "exists": screenshot_ok,
                "size_bytes": SCREENSHOT_PATH.stat().st_size if screenshot_ok else 0,
            },
        })
        passed = (
            http_status == 200
            and body.get("status") == "PASS"
            and body.get("state_trace", [None])[-1] == "PASS"
            and len(body.get("steps", [])) == 13
            and supervisor.get("containment_empty_verified") is True
            and supervisor.get("ok") is True
            and screenshot_ok
        )
        result_payload["status"] = "PASS" if passed else "FAIL"
        if not passed:
            result_payload["error"] = (
                body.get("error")
                or "API/browser/process-containment acceptance assertions failed"
            )
    except Exception as exc:
        result_payload["status"] = "FAIL"
        result_payload["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        stop_process(api_proc)
        target.shutdown()
        target.server_close()
        target_thread.join(timeout=3)
        result_payload["finished_at"] = utc_now()
        RESULT_PATH.write_text(
            json.dumps(result_payload, ensure_ascii=False, indent=2, default=str) + "\n",
            encoding="utf-8",
        )

    print(json.dumps({
        "status": result_payload["status"],
        "http_status": result_payload.get("http_status"),
        "state_trace": result_payload.get("state_trace"),
        "step_count": result_payload.get("step_count"),
        "evidence_count": result_payload.get("evidence_count"),
        "containment": result_payload.get("process_supervisor_evidence"),
        "screenshot": result_payload.get("screenshot"),
        "error": result_payload.get("error"),
    }, ensure_ascii=False, indent=2))
    return 0 if result_payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
