"""Gate 4 prep: E2E from the staged MCP client seam to a live authority process.

This is the strongest end-to-end evidence reachable from the repo side: the
STAGED `W13CoreExecutionClientV1` (unwired, no v54 registration) is driven
through a REAL HTTP bridge against a REAL `core.execution_authority.http_server`
subprocess booted in-test with fail-loud env. The seven client methods are
exercised, run linkage is verified on-disk in the append-only JSONL store,
and live security probes cover malformed JSON (400), unknown routes (404),
and missing identity on GET (401).

Evidence level: repo-side CI E2E (client seam -> live authority process).
It does NOT include the real MCP gateway registration, the W13 execution
host, or a trusted-Sandbox deployment. v54 stays NOT_IMPLEMENTED.
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
sys.path.insert(0, str(REPO_ROOT))

from mcp8020_catalog_v54 import ToolCallError
from mcp8020_w13_core_client_v1 import W13CoreExecutionClientV1

SERVICE_IDENTITY_HEADER = "X-Room-Hop-Service-Identity"


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class LiveAuthorityBridge:
    """HTTP bridge: grants + run recording against the live authority."""

    def __init__(self, port, credential):
        self._port = port
        self._credential = credential

    def _call(self, path, body):
        url = "http://127.0.0.1:" + str(self._port) + path
        data = json.dumps(body or {}).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header(SERVICE_IDENTITY_HEADER, self._credential)
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read().decode("utf-8"))
        except OSError as exc:
            raise ToolCallError("BLOCKED", "authority_unreachable: " + type(exc).__name__) from exc

    def invoke(self, work_context, execution_request):
        work_id = execution_request["work_id"]
        purpose = execution_request["purpose"]
        code, payload = self._call("/works/" + work_id + "/execution-grants", {"purpose": purpose})
        if code != 200:
            raise ToolCallError("BLOCKED", "authority_denied_grant: " + str(payload.get("error")))
        grant = payload["grant"]
        run_body = {
            "grant_id": grant["grant_id"],
            "grant_token": grant["grant_token"],
            "source_sha256": execution_request["source_sha256"],
            "exit_status": "PASS",
            "output_refs": ["stdout://" + grant["grant_id"]],
            "evidence_refs": [execution_request["evidence_ref"]],
            "handoff_ids": [],
        }
        code, payload = self._call("/works/" + work_id + "/execution-runs", run_body)
        if code != 200:
            raise ToolCallError("BLOCKED", "authority_denied_run: " + str(payload.get("error")))
        run = payload["run"]
        return {
            "execution_id": run["record_id"],
            "status": run["exit_status"],
            "work_id": run["work_id"],
            "exit_code": 0,
            "stdout_ref": run["output_refs"][0],
            "stderr_ref": None,
            "evidence_ref": run["evidence_refs"][0],
            "artifacts": list(run["output_refs"]),
        }


def _work_context_provider(work_id):
    if work_id not in ("W13", "W12"):
        raise ToolCallError("BLOCKED", "work_not_authorized_for_service")
    return {"work_id": work_id, "authorized": True}


def _request_builder(request):
    return {
        "work_id": request["work_id"],
        "purpose": request["purpose"],
        "source_sha256": request["source_sha256"],
        "evidence_ref": request["evidence_ref"],
    }


class ClientLiveAuthorityE2ETests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.port = _free_port()
        works_path = Path(self._tmp.name) / "works.json"
        works_path.write_text(json.dumps({
            "W12": {
                "work_name": "BRIDGE", "workspace_root": "/w/12",
                "execution_workspace": "/w/12/run", "evidence_root": "/w/12/evidence",
                "allowed_identities": ["boot-identity"],
            },
            "W13": {
                "work_name": "SANDBOX", "workspace_root": "/w/13",
                "execution_workspace": "/w/13/run", "evidence_root": "/w/13/evidence",
                "allowed_identities": ["boot-identity"],
            }
        }), encoding="utf-8")
        env = dict(os.environ)
        env["EXECUTION_AUTHORITY_ENROLLED_IDENTITIES"] = "boot-identity=boot-credential-e2e"
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
        deadline = time.time() + 15
        armed = False
        while time.time() < deadline:
            if self._proc.poll() is not None:
                self.fail("authority process died before arming")
            try:
                with socket.create_connection(("127.0.0.1", self.port), timeout=0.25):
                    armed = True
                    break
            except OSError:
                time.sleep(0.2)
        if not armed:
            self.fail("authority did not arm within 15s")

    def _stop(self):
        self._proc.terminate()
        try:
            self._proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self._proc.kill()
            self._proc.wait(timeout=5)

    def _client(self):
        bridge = LiveAuthorityBridge(self.port, "boot-credential-e2e")
        return W13CoreExecutionClientV1(
            bridge=bridge,
            work_context_provider=_work_context_provider,
            request_builder=_request_builder,
        )

    def _store_lines(self):
        path = Path(self._tmp.name) / "records" / "execution_authority_records.jsonl"
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_submit_records_run_with_full_linkage_on_disk(self):
        client = self._client()
        result = client.submit({
            "work_id": "W13", "purpose": "gate4_prep_e2e",
            "source_sha256": "c" * 64, "evidence_ref": "e2e-ev-1",
        })
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["work_id"], "W13")
        self.assertTrue(result["run_id"])
        runs = [r for r in self._store_lines() if r.get("record_type") == "run"]
        self.assertEqual(len(runs), 1)
        run = runs[0]
        self.assertEqual(run["work_id"], "W13")
        self.assertEqual(run["source_sha256"], "c" * 64)
        self.assertEqual(run["evidence_refs"], ["e2e-ev-1"])
        self.assertEqual(run["record_id"], result["run_id"])
        grants = [r for r in self._store_lines() if r.get("record_type") == "grant"]
        self.assertEqual(len(grants), 1)
        self.assertEqual(run["grant_id"], grants[0]["record_id"])
        self.assertIn("token_sha256", grants[0])
        blob = json.dumps(self._store_lines())
        self.assertNotIn("boot-credential-e2e", blob)

    def test_seven_method_surface_over_live_authority(self):
        client = self._client()
        result = client.submit({
            "work_id": "W12", "purpose": "gate4_prep_e2e",
            "source_sha256": "d" * 64, "evidence_ref": "e2e-ev-2",
        })
        run_id = result["run_id"]
        self.assertEqual(client.get_status(run_id)["status"], "PASS")
        detail = client.get_result(run_id)
        self.assertEqual(detail["exit_code"], 0)
        self.assertTrue(detail["evidence_ref"])
        artifact = detail["stdout_ref"]
        collected = client.collect_artifact(run_id, artifact)
        self.assertEqual(collected["artifact_path"], artifact)
        evidence = client.generate_evidence(run_id, "ci_e2e", ["ref-1"])
        self.assertEqual(evidence["evidence_ref"], "e2e-ev-2")
        handoff = client.create_handoff("W12", "PASS", ["e2e-ev-2"], "next: gate4 live probes")
        self.assertEqual(handoff["status"], "PASS")
        with self.assertRaises(ToolCallError):
            client.cancel(run_id)
        with self.assertRaises(ToolCallError):
            client.get_status("RUN-unknown")

    def test_wrong_credential_fails_closed_at_the_boundary(self):
        bridge = LiveAuthorityBridge(self.port, "wrong-credential-e2e")
        client = W13CoreExecutionClientV1(
            bridge=bridge,
            work_context_provider=_work_context_provider,
            request_builder=_request_builder,
        )
        with self.assertRaises(ToolCallError):
            client.submit({
                "work_id": "W13", "purpose": "gate4_prep_e2e",
                "source_sha256": "e" * 64, "evidence_ref": "e2e-ev-3",
            })
        self.assertEqual(self._store_lines(), [])

    def test_live_security_probes(self):
        url = "http://127.0.0.1:" + str(self.port)
        req = urllib.request.Request(url + "/works/W13/execution-grants", data=b"not-json-payload", method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header(SERVICE_IDENTITY_HEADER, "boot-credential-e2e")
        try:
            urllib.request.urlopen(req, timeout=10)
            self.fail("malformed json must not be accepted")
        except urllib.error.HTTPError as exc:
            self.assertEqual(exc.code, 400)
        req = urllib.request.Request(url + "/works/W13/not-a-route", data=b" ", method="POST")
        req.add_header(SERVICE_IDENTITY_HEADER, "boot-credential-e2e")
        try:
            urllib.request.urlopen(req, timeout=10)
            self.fail("unknown route must not be accepted")
        except urllib.error.HTTPError as exc:
            self.assertEqual(exc.code, 404)
        req = urllib.request.Request(url + "/works/W13/execution-grants/GRANT-none", method="GET")
        try:
            urllib.request.urlopen(req, timeout=10)
            self.fail("GET without identity must not be accepted")
        except urllib.error.HTTPError as exc:
            self.assertEqual(exc.code, 401)


if __name__ == "__main__":
    unittest.main()
