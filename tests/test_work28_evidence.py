"""WP18: sealed evidence + Core grant client fail-closed."""
from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from execution_host.work28_evidence import (
    EvidenceError,
    seal_evidence,
    verify_evidence_seal,
)
from execution_host.work28_core_grant_client import (
    CORE_AUTHORITY_URL_ENV,
    CORE_SERVICE_IDENTITY_ENV,
    CORE_SERVICE_CREDENTIAL_ENV,
    HttpCoreGrantSource,
    build_grant_source,
)
from execution_host.work28_grant import GrantError


class SealEvidenceTests(unittest.TestCase):
    def test_seal_and_verify(self):
        with tempfile.TemporaryDirectory() as td:
            sealed = seal_evidence(
                evidence_root=td,
                execution_id="run1",
                payload={"grant_id": "g1", "status": "PASS"},
            )
            self.assertTrue(Path(sealed["evidence_ref"]).is_file())
            live = verify_evidence_seal(sealed["evidence_ref"])
            self.assertEqual(live, sealed["evidence_sha256"])

    def test_tamper_detected(self):
        with tempfile.TemporaryDirectory() as td:
            sealed = seal_evidence(
                evidence_root=td,
                execution_id="run2",
                payload={"x": 1},
            )
            path = Path(sealed["evidence_ref"])
            path.write_text('{"x": 2}\n', encoding="utf-8")
            with self.assertRaises(EvidenceError) as ctx:
                verify_evidence_seal(path)
            self.assertIn("tampered", str(ctx.exception))


class CoreGrantClientTests(unittest.TestCase):
    def test_http_unreachable_fail_closed(self):
        src = HttpCoreGrantSource("http://127.0.0.1:1/core", "mcp8020", "credential", timeout=0.2)
        with self.assertRaises(GrantError) as ctx:
            src.fetch_grant("W28", "GRANT-12345678-1234-1234-1234-123456789abc", "grant-token")
        self.assertIn("unreachable", str(ctx.exception))

    def test_build_requires_all_core_authority_configuration(self):
        with self.assertRaisesRegex(GrantError, "core_authority_url_required"):
            build_grant_source({})
        env = {
            CORE_AUTHORITY_URL_ENV: "https://core.example/authority",
            CORE_SERVICE_IDENTITY_ENV: "mcp8020",
            CORE_SERVICE_CREDENTIAL_ENV: "service-credential",
        }
        self.assertIsInstance(build_grant_source(env), HttpCoreGrantSource)



class DispatchSealsEvidenceTests(unittest.TestCase):
    def test_dispatch_writes_seal(self):
        from execution_host.host import ExecutionHost
        from execution_host.work28_dispatch import dispatch_execute
        from execution_host.work28_grant import issue_grant_for_tests

        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            host_root = base / "root"
            host_root.mkdir()
            body = b'print("wp18")\n'
            (host_root / "job.py").write_bytes(body)
            ws = host_root / "workspace"
            ev = host_root / "evidence"
            ws.mkdir()
            ev.mkdir()
            digest = hashlib.sha256(body).hexdigest()
            grant = issue_grant_for_tests(
                grant_id="g18",
                work_id="28",
                entry_path="job.py",
                operation="RUN_SCRIPT",
                expected_source_sha256=digest,
            )
            result = dispatch_execute(
                ExecutionHost(),
                work_context={
                    "work_id": "28",
                    "work_name": "W",
                    "workspace_root": str(host_root),
                    "execution_workspace": str(ws),
                    "evidence_root": str(ev),
                    "authorized": True,
                    "execution_id": "wp18-run",
                },
                body={
                    "mode": "work28_snapshot",
                    "execution_grant_id": "g18",
                    "work28_request": {
                        "work_id": "28",
                        "entry_path": "job.py",
                        "operation": "RUN_SCRIPT",
                        "expected_source_sha256": digest,
                        "timeout_seconds": 15,
                    },
                },
                grant_registry={"g18": grant},
            )
            self.assertIn("evidence_sha256", result)
            self.assertEqual(result.get("grant_id"), "g18")
            verify_evidence_seal(result["evidence_ref"])


if __name__ == "__main__":
    unittest.main()
