"""Tests for the Core execution authority (contract V1.2, Gate 2).

Locks the approved decision requests as testable proof obligations: DR-1
service identity enrolled by Core, port-agnostic, wrong credential denied
fail-closed; DR-2 grant token returned once, only its SHA-256 stored,
server-side validation of rights/Work/expiry/token, secrets never in stored
records or error paths; DR-3 append-only store persists across restart,
refuses duplicate ids, exposes no mutation path, and run records verifiably
link grant, source hash, exit status, output/evidence refs, handoff ids;
DR-4 the HTTP mount answers with the stable error codes of the contract
(401/403/404/409) and never echoes secrets. No test touches a real Core
deployment; stores use temp directories and the HTTP boundary runs on an
ephemeral local port with an in-test authority.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.execution_authority.authority import (
    ExecutionAuthority,
    ExecutionAuthorityConfigError,
    load_enrolled_identities,
    load_works_registry,
)
from core.execution_authority.http_server import SERVICE_IDENTITY_HEADER, ExecutionAuthorityHandler
from core.execution_authority.store import AppendOnlyRecordStore


def build_authority(tmpdir, seconds=300):
    identities = load_enrolled_identities("mcp8020=secret-a,mcp8030=secret-b")
    works = {
        "W28": {
            "work_name": "MCP-TOOLING-PLATFORM",
            "workspace_root": "/w/28",
            "execution_workspace": "/w/28/run",
            "evidence_root": "/w/28/evidence",
            "allowed_identities": ["mcp8020"],
        }
    }
    store = AppendOnlyRecordStore(str(Path(tmpdir) / "records"))
    return ExecutionAuthority(store=store, enrolled_identities=identities, works=works, default_grant_seconds=seconds)


class StoreTests(unittest.TestCase):
    def test_append_persists_and_survives_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = AppendOnlyRecordStore(tmp)
            store.append({"record_id": "R-1", "record_type": "grant", "value": "a"})
            reopened = AppendOnlyRecordStore(tmp)
            self.assertEqual(reopened.get("R-1")["value"], "a")
            self.assertEqual(len(reopened.records()), 1)

    def test_duplicate_record_id_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = AppendOnlyRecordStore(tmp)
            store.append({"record_id": "R-1", "record_type": "grant"})
            with self.assertRaises(ValueError):
                store.append({"record_id": "R-1", "record_type": "grant"})

    def test_no_mutation_or_deletion_path_exists(self):
        exposed = {name for name in dir(AppendOnlyRecordStore) if not name.startswith("_") and not name.startswith("__")}
        self.assertEqual(exposed, {"append", "get", "records"})


class ConfigTests(unittest.TestCase):
    def test_empty_identities_fail_loud(self):
        with self.assertRaises(ExecutionAuthorityConfigError):
            load_enrolled_identities("")
        with self.assertRaises(ExecutionAuthorityConfigError):
            load_enrolled_identities(None)

    def test_malformed_identity_entry_fail_loud(self):
        with self.assertRaises(ExecutionAuthorityConfigError):
            load_enrolled_identities("nocredential")

    def test_works_registry_requires_canonical_work_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "works.json"
            path.write_text(json.dumps({"28": {"work_name": "x"}}), encoding="utf-8")
            with self.assertRaises(ExecutionAuthorityConfigError):
                load_works_registry(str(path))
            path.write_text(json.dumps({"W28": {"work_name": "x"}}), encoding="utf-8")
            with self.assertRaises(ExecutionAuthorityConfigError):
                load_works_registry(str(path))


class AuthorityTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.authority = build_authority(self._tmp.name)

    def test_authenticate_right_and_wrong_credential(self):
        self.assertEqual(self.authority.authenticate("secret-a"), "mcp8020")
        self.assertEqual(self.authority.authenticate("secret-b"), "mcp8030")
        with self.assertRaises(PermissionError):
            self.authority.authenticate("wrong")
        with self.assertRaises(PermissionError):
            self.authority.authenticate(None)

    def test_issue_grant_returns_token_once_and_stores_only_hash(self):
        grant = self.authority.issue_grant("mcp8020", "W28", "pytest_run")
        self.assertTrue(grant["grant_token"])
        stored = self.authority._store.get(grant["grant_id"])
        self.assertNotIn("grant_token", stored)
        self.assertNotIn(grant["grant_token"], json.dumps(stored))
        self.assertTrue(stored["token_sha256"])

    def test_grant_status_active_then_revoked(self):
        grant = self.authority.issue_grant("mcp8020", "W28", "pytest_run")
        self.assertEqual(self.authority.grant_status(grant["grant_id"])["status"], "active")
        revoked = self.authority.revoke_grant(grant["grant_id"])
        self.assertEqual(revoked["status"], "revoked")

    def test_expired_grant_detected(self):
        grant = self.authority.issue_grant("mcp8020", "W28", "pytest_run")
        stored = self.authority._store.get(grant["grant_id"])
        stored["expires_at_unix"] = 0
        self.assertEqual(self.authority.grant_status(grant["grant_id"])["status"], "expired")

    def test_second_active_grant_refused(self):
        self.authority.issue_grant("mcp8020", "W28", "pytest_run")
        with self.assertRaises(FileExistsError):
            self.authority.issue_grant("mcp8020", "W28", "pytest_run")

    def test_validate_grant_token_server_side(self):
        grant = self.authority.issue_grant("mcp8020", "W28", "pytest_run")
        ok = self.authority.validate_grant_token(grant["grant_id"], grant["grant_token"])
        self.assertEqual(ok["status"], "active")
        with self.assertRaises(PermissionError):
            self.authority.validate_grant_token(grant["grant_id"], "forged")
        with self.assertRaises(PermissionError):
            self.authority.validate_grant_token(grant["grant_id"], "")

    def test_record_run_full_linkage(self):
        grant = self.authority.issue_grant("mcp8020", "W28", "pytest_run")
        run = self.authority.record_run(
            grant["grant_id"], source_sha256="a" * 64, exit_status="PASS",
            output_refs=["stdout://1"], evidence_refs=["ev-1"], handoff_ids=["H-1"])
        self.assertEqual(run["grant_id"], grant["grant_id"])
        self.assertEqual(run["source_sha256"], "a" * 64)
        self.assertEqual(run["exit_status"], "PASS")
        self.assertEqual(run["evidence_refs"], ["ev-1"])
        self.assertEqual(run["handoff_ids"], ["H-1"])
        self.assertEqual(run["work_id"], "W28")

    def test_record_run_requires_evidence_refs(self):
        grant = self.authority.issue_grant("mcp8020", "W28", "pytest_run")
        with self.assertRaises(ValueError):
            self.authority.record_run(grant["grant_id"], source_sha256="a", exit_status="PASS",
                                      output_refs=[], evidence_refs=[], handoff_ids=[])

    def test_record_run_rejected_for_revoked_or_unknown_grant(self):
        grant = self.authority.issue_grant("mcp8020", "W28", "pytest_run")
        self.authority.revoke_grant(grant["grant_id"])
        with self.assertRaises(PermissionError):
            self.authority.record_run(grant["grant_id"], source_sha256="a", exit_status="PASS",
                                      output_refs=[], evidence_refs=["e"], handoff_ids=[])
        with self.assertRaises(LookupError):
            self.authority.record_run("GRANT-nope", source_sha256="a", exit_status="PASS",
                                      output_refs=[], evidence_refs=["e"], handoff_ids=[])

    def test_state_survives_authority_restart(self):
        grant = self.authority.issue_grant("mcp8020", "W28", "pytest_run")
        self.authority.record_run(grant["grant_id"], source_sha256="a", exit_status="PASS",
                                  output_refs=[], evidence_refs=["e"], handoff_ids=[])
        restarted = build_authority(self._tmp.name)
        self.assertEqual(restarted.grant_status(grant["grant_id"])["status"], "active")
        self.assertEqual(len(restarted._store.records("run")), 1)


class HttpBoundaryTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.authority = build_authority(self._tmp.name)
        bound = type("BoundHandler", (ExecutionAuthorityHandler,), {"authority": self.authority})
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), bound)
        self.port = self._server.server_address[1]
        Thread(target=self._server.serve_forever, daemon=True).start()
        self.addCleanup(self._server.shutdown)

    def request(self, path, body=None, credential="secret-a", method="POST"):
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

    def test_missing_or_wrong_identity_401(self):
        code, payload = self.request("/works/W28/execution-grants", {"purpose": "pytest_run"}, credential=None)
        self.assertEqual(code, 401)
        self.assertEqual(payload["error"], "caller_authentication_failed")
        code, _ = self.request("/works/W28/execution-grants", {"purpose": "pytest_run"}, credential="wrong")
        self.assertEqual(code, 401)

    def test_enrolled_but_unauthorized_identity_403(self):
        code, payload = self.request("/works/W28/execution-grants", {"purpose": "pytest_run"}, credential="secret-b")
        self.assertEqual(code, 403)
        self.assertEqual(payload["error"], "caller_not_authorized_for_work")

    def test_unknown_work_404_and_duplicate_grant_409(self):
        code, payload = self.request("/works/W99/execution-grants", {"purpose": "pytest_run"})
        self.assertEqual(code, 404)
        self.assertEqual(payload["error"], "unknown_work")
        code, payload = self.request("/works/W28/execution-grants", {"purpose": "pytest_run"})
        self.assertEqual(code, 200)
        code, payload = self.request("/works/W28/execution-grants", {"purpose": "pytest_run"})
        self.assertEqual(code, 409)
        self.assertEqual(payload["error"], "grant_already_active")

    def test_grant_issue_and_status_roundtrip(self):
        code, payload = self.request("/works/W28/execution-grants", {"purpose": "pytest_run"})
        self.assertEqual(code, 200)
        grant = payload["grant"]
        self.assertTrue(grant["grant_token"])
        code, payload = self.request("/works/W28/execution-grants/" + grant["grant_id"], method="GET")
        self.assertEqual(code, 200)
        self.assertEqual(payload["grant"]["status"], "active")
        self.assertNotIn("token_sha256", payload["grant"])
        self.assertNotIn("grant_token", payload["grant"])

    def test_run_recording_via_http_with_server_side_token_check(self):
        code, payload = self.request("/works/W28/execution-grants", {"purpose": "pytest_run"})
        grant = payload["grant"]
        body = {"grant_id": grant["grant_id"], "grant_token": "forged",
                "source_sha256": "a" * 64, "exit_status": "PASS",
                "output_refs": [], "evidence_refs": ["ev-1"], "handoff_ids": []}
        code, payload = self.request("/works/W28/execution-runs", body)
        self.assertEqual(code, 403)
        self.assertEqual(payload["error"], "grant_token_mismatch")
        body["grant_token"] = grant["grant_token"]
        code, payload = self.request("/works/W28/execution-runs", body)
        self.assertEqual(code, 200)
        self.assertEqual(payload["run"]["exit_status"], "PASS")
        self.assertEqual(payload["run"]["evidence_refs"], ["ev-1"])

    def test_credential_and_token_never_leak(self):
        code, payload = self.request("/works/W28/execution-grants", {"purpose": "pytest_run"})
        grant = payload["grant"]
        code, payload = self.request("/works/W28/execution-runs", {"grant_id": grant["grant_id"], "grant_token": "x",
                                                                   "source_sha256": "a", "exit_status": "PASS",
                                                                   "evidence_refs": ["e"]})
        blob = json.dumps(payload) + json.dumps(self.authority._store.records())
        self.assertNotIn("secret-a", blob)
        self.assertNotIn("secret-b", blob)
        self.assertNotIn(grant["grant_token"], json.dumps(self.authority._store.records()))


if __name__ == "__main__":
    unittest.main()
