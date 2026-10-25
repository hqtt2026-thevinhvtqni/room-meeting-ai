"""Gate 3 preparation: live boot probe for the Core execution authority.

Boots `core.execution_authority.http_server` as a REAL subprocess with
fail-loud environment configuration, waits for it to arm (port answers on
TCP), then exercises the LIVE boundary over a real socket: 401 missing and
wrong credential, 403 enrolled-but-unauthorized, 404 unknown work, 200
grant issue, 409 duplicate active grant, 403 forged grant token, 200 valid
run recording, fail-closed boot on missing env, and non-leakage of
credentials in process output.

Evidence level: this is CI-runtime evidence (real process + real socket on
the CI runner). It is NOT a trusted-Sandbox deployment and does NOT claim
production PASS, Sandbox runtime verification, or Gate 3 completion.
"""
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

SERVICE_IDENTITY_HEADER = "X-Room-Hop-Service-Identity"


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class BootProbeTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.port = _free_port()
        works_path = Path(self._tmp.name) / "works.json"
        works_path.write_text(json.dumps({
            "W13": {
                "work_name": "SANDBOX",
                "workspace_root": "/w/13",
                "execution_workspace": "/w/13/run",
                "evidence_root": "/w/13/evidence",
                "allowed_identities": ["boot-identity"],
            }
        }), encoding="utf-8")
        env = dict(os.environ)
        env["EXECUTION_AUTHORITY_ENROLLED_IDENTITIES"] = (
            "boot-identity=boot-credential-alpha,other-identity=boot-credential-beta")
        env["EXECUTION_AUTHORITY_WORKS_FILE"] = str(works_path)
        env["EXECUTION_AUTHORITY_DATA_DIR"] = str(Path(self._tmp.name) / "records")
        env["EXECUTION_AUTHORITY_PORT"] = str(self.port)
        env["EXECUTION_AUTHORITY_HOST"] = "127.0.0.1"
        self._proc = subprocess.Popen(
            [sys.executable, "-m", "core.execution_authority.http_server"],
            cwd=str(REPO_ROOT), env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        )
        self.addCleanup(self._stop)
        armed = False
        deadline = time.time() + 15
        while time.time() < deadline:
            if self._proc.poll() is not None:
                break
            try:
                with socket.create_connection(("127.0.0.1", self.port), timeout=0.25):
                    armed = True
                    break
            except OSError:
                time.sleep(0.2)
        if not armed:
            self._proc.kill()
            self._proc.wait(timeout=5)
            out = self._proc.stdout.read() if self._proc.stdout else ""
            self.fail("authority process did not arm within 15s; output: " + out)

    def _stop(self):
        self._proc.terminate()
        try:
            self._proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self._proc.kill()
            self._proc.wait(timeout=5)

    def request(self, path, body=None, credential="boot-credential-alpha", method="POST"):
        url = "http://127.0.0.1:" + str(self.port) + path
        data = json.dumps(body or {}).encode("utf-8")
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")
        if credential is not None:
            req.add_header(SERVICE_IDENTITY_HEADER, credential)
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read().decode("utf-8"))

    def test_boot_armed_and_fail_closed_on_missing_env(self):
        self.assertIsNone(self._proc.poll())
        env = dict(os.environ)
        env.pop("EXECUTION_AUTHORITY_ENROLLED_IDENTITIES", None)
        env.pop("EXECUTION_AUTHORITY_WORKS_FILE", None)
        env.pop("EXECUTION_AUTHORITY_DATA_DIR", None)
        proc = subprocess.Popen(
            [sys.executable, "-m", "core.execution_authority.http_server"],
            cwd=str(REPO_ROOT), env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        )
        try:
            proc.wait(timeout=10)
            self.assertNotEqual(proc.returncode, 0)
            out = proc.stdout.read() if proc.stdout else ""
            self.assertIn("no enrolled service identities", out)
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=5)

    def test_live_probe_boundary(self):
        code, _ = self.request("/works/W13/execution-grants", {"purpose": "gate3_probe"}, credential=None)
        self.assertEqual(code, 401)
        code, _ = self.request("/works/W13/execution-grants", {"purpose": "gate3_probe"}, credential="wrong-credential")
        self.assertEqual(code, 401)
        code, payload = self.request("/works/W13/execution-grants", {"purpose": "gate3_probe"}, credential="boot-credential-beta")
        self.assertEqual(code, 403)
        self.assertEqual(payload["error"], "caller_not_authorized_for_work")
        code, payload = self.request("/works/W99/execution-grants", {"purpose": "gate3_probe"})
        self.assertEqual(code, 404)
        self.assertEqual(payload["error"], "unknown_work")
        code, payload = self.request("/works/W13/execution-grants", {"purpose": "gate3_probe"})
        self.assertEqual(code, 200)
        grant = payload["grant"]
        self.assertTrue(grant["grant_token"])
        self.assertIn("grant_id", grant)
        code, payload = self.request("/works/W13/execution-grants", {"purpose": "gate3_probe"})
        self.assertEqual(code, 409)
        self.assertEqual(payload["error"], "grant_already_active")
        body = {"grant_id": grant["grant_id"], "grant_token": "forged",
                "source_sha256": "b" * 64, "exit_status": "PASS",
                "output_refs": [], "evidence_refs": ["boot-ev-1"], "handoff_ids": []}
        code, payload = self.request("/works/W13/execution-runs", body)
        self.assertEqual(code, 403)
        self.assertEqual(payload["error"], "grant_token_mismatch")
        body["grant_token"] = grant["grant_token"]
        code, payload = self.request("/works/W13/execution-runs", body)
        self.assertEqual(code, 200)
        self.assertEqual(payload["run"]["exit_status"], "PASS")
        self.assertEqual(payload["run"]["work_id"], "W13")

    def test_process_output_never_leaks_credentials(self):
        code, _ = self.request("/works/W13/execution-grants", {"purpose": "gate3_probe"})
        self.assertEqual(code, 200)
        self._stop()
        out = self._proc.stdout.read() if self._proc.stdout else ""
        self.assertNotIn("boot-credential-alpha", out)
        self.assertNotIn("boot-credential-beta", out)
        self.assertIn("execution-authority: armed", out)


if __name__ == "__main__":
    unittest.main()
