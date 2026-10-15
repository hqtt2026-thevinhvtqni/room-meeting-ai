"""CLA PROPOSED RED TESTS — Work 28 — 2026-10-15

Status: PROPOSED / NOT RUN. Written statically by Cla; no interpreter, runner or PC
was used. Kept in 06_EVIDENCE on purpose so the canonical command
(python -m unittest discover -s 05_TEST -t . -v) is NOT affected. Ka decides if/when
to move them into 05_TEST once an approved runner exists.

Companion record: CLA_TRUST_BOUNDARY_F1_F3_REVIEW_20261015.md

Expectation on CURRENT source (contract 1.3.0 / collector 0.2.0 / verifier 0.1.0):
  RED (must fail now, proving the finding):  TB1, TB2, TB3, TB4, TB5, F1-1, F3-2..F3-6
  GREEN (regression guards, should pass):     G_* tests
A RED test turning green is only meaningful after the matching fix; do not edit a
test to make it pass. Where a test fixes an API name (e.g. AuthorizedExecutionRequest)
that name is a proposal: Ka/Nu may rename it, but the behaviour asserted must stay.

All fixtures are in-memory or tempfile directories. Nothing touches the PC, the
network, a real repository or a live MCP/Core service.
"""
from __future__ import annotations

import hashlib
import io
import os
import sys
import tempfile
import types
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import tool_contracts as tc  # noqa: E402
import source_snapshot_contract as ssc  # noqa: E402
import source_snapshot_import_verifier as siv  # noqa: E402
import pc_readonly_source_collector as col  # noqa: E402


# ---------------------------------------------------------------------------
# Trust boundary (TB-1 .. TB-5)
# ---------------------------------------------------------------------------
class TB1_PrincipalForgery(unittest.TestCase):
    def test_arbitrary_source_label_rejected(self):
        # Any label outside a transport allowlist must be refused.
        for label in ("request", "header", "body", "param", "anything"):
            with self.subTest(label=label):
                with self.assertRaises(ValueError):
                    tc.TrustedPrincipal(principal_id="admin", source=label)

    def test_code_outside_adapter_cannot_mint_trusted_principal(self):
        # Even a plausible trusted label must not be mintable by arbitrary code.
        with self.assertRaises((ValueError, PermissionError, TypeError)):
            tc.TrustedPrincipal(principal_id="admin", source="core-session")

    def test_G_caller_labels_still_rejected(self):
        for label in ("caller", "Client", " user-supplied ", "identity_id"):
            with self.subTest(label=label):
                with self.assertRaises(ValueError):
                    tc.TrustedPrincipal(principal_id="p1", source=label)


class TB2_WorkContextSelfAuthorization(unittest.TestCase):
    def _principal(self):
        # Built through whatever path currently works; TB1 fix may change this helper.
        return tc.TrustedPrincipal(principal_id="p1", source="core-session")

    def test_allowed_operations_must_be_known_operations(self):
        for ops in (("FORMAT_DISK",), ("READ", "*"), ("read",), ("READ", "EXECUTE_ANYTHING")):
            with self.subTest(ops=ops):
                with self.assertRaises(ValueError):
                    tc.WorkContext(work_id="28", principal=self._principal(), allowed_operations=ops)

    def test_context_must_be_bound_to_core_grant(self):
        # A context built by the caller (no Core-issued grant) must not authorize anything.
        ctx = tc.WorkContext(work_id="28", principal=self._principal(), allowed_operations=("READ",))
        grant = getattr(ctx, "core_grant", None)
        self.assertIsNotNone(grant, "WorkContext carries no Core-issued grant/attestation")

    def test_G_operation_outside_context_rejected(self):
        ctx = tc.WorkContext(work_id="28", principal=self._principal(), allowed_operations=("READ",))
        with self.assertRaises(ValueError):
            tc.AuthorizedSandboxRequest(
                request_id="req-1", work_context=ctx,
                operation=tc.SandboxOperation.DELETE, relative_path="a.txt")


class TB3_PassGateIsSelfAttested(unittest.TestCase):
    def test_fabricated_execution_pass_rejected(self):
        # Shape-perfect but fabricated evidence must not yield an accepted PASS.
        with self.assertRaises(ValueError):
            tc.ToolResult(
                request_id="req-1", status=tc.ToolStatus.PASS, message="fabricated",
                operation_kind=tc.OperationKind.EXECUTION,
                execution_operation=tc.ExecutionOperation.RUN_TESTS,
                run_id="run-" + "a" * 32, exit_code=0,
                evidence_ref="evidence/does-not-exist.log",
                source_sha256="b" * 64,
                test_summary={"tests_run": 1, "failures": 0, "errors": 0, "skipped": 0})

    def test_G_pass_without_counters_rejected(self):
        with self.assertRaises(ValueError):
            tc.ToolResult(
                request_id="req-1", status=tc.ToolStatus.PASS, message="x",
                operation_kind=tc.OperationKind.EXECUTION,
                execution_operation=tc.ExecutionOperation.RUN_TESTS,
                run_id="run-" + "a" * 32, exit_code=0, evidence_ref="e",
                source_sha256="b" * 64, test_summary={"tests_run": 0, "failures": 0,
                                                       "errors": 0, "skipped": 0})


class TB4_ExecutionAuthorizationSurface(unittest.TestCase):
    def test_execution_requests_have_their_own_authorization_type(self):
        self.assertTrue(hasattr(tc, "AuthorizedExecutionRequest"),
                        "no authorization request type for RUN_SCRIPT/RUN_TESTS")


class TB5_DeniedIsNotCollapsedIntoNotFound(unittest.TestCase):
    def test_permission_error_keeps_denied_status(self):
        res = tc.result_from_exception("req-1", PermissionError("x"))
        self.assertEqual(res.status, tc.ToolStatus.DENIED)


class G_PathValidationGuards(unittest.TestCase):
    def test_G_rejects_traversal_and_platform_tricks(self):
        bad = ["../x", "a/../b", "/abs", "C:/x", "a\\b", "a//b", "a/./b", "CON", "nul.txt",
               "a/.git/config", ".env", "a/desktop.ini", "x~1/y", "a b ", "a.", "-opt",
               "a:stream", "a\u2215b", "a\u0000b"]
        for value in bad:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    tc.validate_relative_work_path(value)

    def test_G_accepts_plain_relative_path(self):
        self.assertEqual(tc.validate_relative_work_path("a/b/c.txt"), "a/b/c.txt")


# ---------------------------------------------------------------------------
# F1 — collector race / link handling (disposable temp directories only)
# ---------------------------------------------------------------------------
def _can_symlink(tmp: Path) -> bool:
    try:
        (tmp / "_probe_t").write_text("x")
        os.symlink(tmp / "_probe_t", tmp / "_probe_l")
        return True
    except (OSError, NotImplementedError):
        return False


class F1_SafeRead(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.repo = Path(self._td.name).resolve()
        (self.repo / "core").mkdir()
        self.f = self.repo / "core" / "a.py"
        self.f.write_bytes(b"print(1)\n" * 50)

    def tearDown(self):
        self._td.cleanup()

    def test_G_reads_plain_file(self):
        data = col.safe_read(self.repo, "core/a.py", self.f)
        self.assertEqual(data, b"print(1)\n" * 50)

    def test_G_rejects_final_component_symlink(self):
        if not _can_symlink(self.repo):
            self.skipTest("symlink creation not permitted here")
        link = self.repo / "core" / "link.py"
        os.symlink(self.f, link)
        with self.assertRaises(SystemExit):
            col.safe_read(self.repo, "core/link.py", link)

    def test_G_rejects_parent_symlink(self):
        if not _can_symlink(self.repo):
            self.skipTest("symlink creation not permitted here")
        outside = Path(self._td.name) / "outside"
        outside.mkdir()
        (outside / "x.py").write_bytes(b"secret\n")
        os.symlink(outside, self.repo / "tests")
        with self.assertRaises(SystemExit):
            col.safe_read(self.repo, "tests/x.py", self.repo / "tests" / "x.py")

    def test_G_file_changed_during_read_rejected(self):
        real_read = os.read
        state = {"n": 0}

        def swapping_read(fd, n):
            state["n"] += 1
            if state["n"] == 1:
                with open(self.f, "ab") as h:
                    h.write(b"# tamper\n")
            return real_read(fd, n)

        with mock.patch.object(col.os, "read", swapping_read):
            with self.assertRaises(SystemExit):
                col.safe_read(self.repo, "core/a.py", self.f)

    def test_F1_1_identity_unavailable_must_fail_closed(self):
        # If the platform cannot give st_ino (reported 0, as on some Windows builds),
        # the identity check must fail closed, not be silently skipped.
        real_fstat = os.fstat

        def zero_ino(fd):
            st = real_fstat(fd)
            return types.SimpleNamespace(st_mode=st.st_mode, st_dev=st.st_dev, st_ino=0,
                                         st_size=st.st_size, st_mtime_ns=st.st_mtime_ns)

        with mock.patch.object(col.os, "fstat", zero_ino):
            with self.assertRaises(SystemExit):
                col.safe_read(self.repo, "core/a.py", self.f)

    def test_F1_3_post_read_identity_includes_device_and_inode(self):
        # Post-read check must detect a different file object even if size/mtime match.
        real_fstat = os.fstat
        calls = {"n": 0}

        def second_call_other_inode(fd):
            st = real_fstat(fd)
            calls["n"] += 1
            ino = st.st_ino if calls["n"] == 1 else st.st_ino + 1
            return types.SimpleNamespace(st_mode=st.st_mode, st_dev=st.st_dev, st_ino=ino,
                                         st_size=st.st_size, st_mtime_ns=st.st_mtime_ns)

        with mock.patch.object(col.os, "fstat", second_call_other_inode):
            with self.assertRaises(SystemExit):
                col.safe_read(self.repo, "core/a.py", self.f)


class F1_Enumerate(unittest.TestCase):
    def test_G_denied_names_and_suffixes_excluded(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td).resolve()
            (repo / "core").mkdir()
            for name in ("ok.py", "secrets.json", "x.pem", "a.log", ".env"):
                (repo / "core" / name).write_bytes(b"x\n")
            selected, _ = col.enumerate_files(repo)
            self.assertEqual([rel for rel, _ in selected], ["core/ok.py"])


# ---------------------------------------------------------------------------
# F3 — receipt / verifier / rule consistency (in-memory only)
# ---------------------------------------------------------------------------
def _build(files: dict[str, bytes], *, receipt_over: dict | None = None, with_receipt=True):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in sorted(files):
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, files[rel])
    archive = buf.getvalue()
    archive_hash = hashlib.sha256(archive).hexdigest()
    included = [{"path": rel, "size_bytes": len(files[rel]),
                 "sha256": hashlib.sha256(files[rel]).hexdigest()} for rel in sorted(files)]
    manifest = {
        "schema_version": ssc.CONTRACT_VERSION, "collector_version": "test/0",
        "provenance_status": "UNAUTHENTICATED_LOCAL_OBSERVATION",
        "created_at_utc": "2026-10-15T00:00:00Z", "repo_root": "/r", "branch": "main",
        "head": "a" * 40, "dirty": False, "status_short": [], "included_files": included,
        "excluded_paths": [], "file_count": len(included),
        "total_bytes": sum(len(v) for v in files.values()), "archive_sha256": archive_hash,
    }
    mbytes = ssc.canonical_manifest_bytes(manifest)
    receipt = None
    if with_receipt:
        receipt = {
            "receipt_version": "0.1.0", "source_identity": "pc-main", "approved_channel": "approved-readonly",
            "archive_sha256": archive_hash, "manifest_sha256": hashlib.sha256(mbytes).hexdigest(),
            "destination_work_id": "28",
            "transferred_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "nonce": "n" * 24, "issuer": "issuer-x", "issuer_signature": "sig-x",
            "verifier_result": "TRUSTED_RECEIPT_PENDING_EXTERNAL_AUTH",
        }
        if receipt_over:
            receipt.update(receipt_over)
    return archive, mbytes, receipt


GOOD = {"core/a.py": b"print(1)\n" * 20}


def _verify(files=None, **kw):
    archive, mbytes, receipt = _build(files or GOOD, **{k: v for k, v in kw.items()
                                                       if k in ("receipt_over", "with_receipt")})
    return siv.verify_archive_in_memory(
        archive, mbytes, allowlist=["core"], destination_work_id="28", receipt=receipt)


class F3_Receipt(unittest.TestCase):
    def test_G_happy_path_stays_not_imported(self):
        res = _verify()
        self.assertEqual(res["status"], "VERIFIED_IN_MEMORY_NOT_IMPORTED")
        self.assertIs(res["imported"], False)

    def test_F3_2_missing_receipt_is_not_reported_as_verified(self):
        res = _verify(with_receipt=False)
        self.assertNotEqual(res["status"], "VERIFIED_IN_MEMORY_NOT_IMPORTED")

    def test_F3_1_unverifiable_signature_fails_closed(self):
        # No trust anchor configured => an arbitrary signature string must not pass.
        with self.assertRaises(siv.ImportVerificationError):
            _verify(receipt_over={"issuer_signature": "not-a-real-signature"})

    def test_F3_3_unlisted_channel_rejected(self):
        with self.assertRaises(siv.ImportVerificationError):
            _verify(receipt_over={"approved_channel": "attacker-channel", "source_identity": "unknown"})

    def test_F3_3_stale_receipt_rejected(self):
        with self.assertRaises(siv.ImportVerificationError):
            _verify(receipt_over={"transferred_at_utc": "2000-01-01T00:00:00Z"})

    def test_F3_3_replayed_nonce_rejected(self):
        _verify()
        with self.assertRaises(siv.ImportVerificationError):
            _verify()  # identical receipt/nonce presented twice

    def test_G_receipt_hash_mismatch_rejected(self):
        with self.assertRaises(siv.ImportVerificationError):
            _verify(receipt_over={"archive_sha256": "0" * 64})

    def test_G_wrong_destination_rejected(self):
        with self.assertRaises(siv.ImportVerificationError):
            _verify(receipt_over={"destination_work_id": "29"})


class F3_RuleConsistency(unittest.TestCase):
    def test_F3_5_collector_denied_names_also_denied_by_verifier(self):
        for rel in ("core/secrets.json", "core/old.bak", "core/x.dump", "core/coverage/a.py",
                    "core/htmlcov/a.py"):
            with self.subTest(rel=rel):
                with self.assertRaises(siv.ImportVerificationError):
                    _verify(files={rel: b"x = 1\n" * 10})

    def test_F3_5_verifier_enforces_suffix_allowlist(self):
        for rel in ("core/tool.exe", "core/lib.dll", "core/data.bin"):
            with self.subTest(rel=rel):
                with self.assertRaises(siv.ImportVerificationError):
                    _verify(files={rel: b"MZ" * 40})

    def test_F3_6_case_insensitive_duplicate_paths_rejected(self):
        with self.assertRaises(siv.ImportVerificationError):
            _verify(files={"core/a.py": b"x = 1\n" * 10, "core/A.py": b"x = 2\n" * 10})

    def test_F3_6_zip_symlink_mode_rejected(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            info = zipfile.ZipInfo("core/a.py", date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (0o120777 & 0xFFFF) << 16  # S_IFLNK
            zf.writestr(info, b"target\n" * 10)
        archive = buf.getvalue()
        data = b"target\n" * 10
        manifest = {
            "schema_version": ssc.CONTRACT_VERSION, "collector_version": "test/0",
            "provenance_status": "UNAUTHENTICATED_LOCAL_OBSERVATION",
            "created_at_utc": "2026-10-15T00:00:00Z", "repo_root": "/r", "branch": "main",
            "head": "a" * 40, "dirty": False, "status_short": [],
            "included_files": [{"path": "core/a.py", "size_bytes": len(data),
                                "sha256": hashlib.sha256(data).hexdigest()}],
            "excluded_paths": [], "file_count": 1, "total_bytes": len(data),
            "archive_sha256": hashlib.sha256(archive).hexdigest(),
        }
        with self.assertRaises(siv.ImportVerificationError):
            siv.verify_archive_in_memory(archive, ssc.canonical_manifest_bytes(manifest),
                                         allowlist=["core"], destination_work_id="28")

    def test_G_tampered_member_rejected(self):
        archive, mbytes, receipt = _build(GOOD)
        tampered_files = {"core/a.py": b"print(2)\n" * 20}
        t_archive, _t_m, _r = _build(tampered_files)
        with self.assertRaises(siv.ImportVerificationError):
            siv.verify_archive_in_memory(t_archive, mbytes, allowlist=["core"],
                                         destination_work_id="28", receipt=None)

    def test_G_path_traversal_rejected_by_contract(self):
        for rel in ("../core/a.py", "/core/a.py", "core/../a.py", "C:/core/a.py"):
            with self.subTest(rel=rel):
                with self.assertRaises(ssc.SnapshotValidationError):
                    ssc.validate_relative_path(rel, allowlist=["core"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
