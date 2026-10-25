"""Negative and positive contract tests for the staged authorized adapter.

Mocks verify fail-closed policy ordering only; they are not live Core/runtime proof.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from mcp8020_authorized_execution_adapter_v1 import AuthorizedExecutionAdapterV1

HASH = "a" * 64
REQUEST = {
    "work_id": "work28",
    "entry_path": "04_CODE/smoke.py",
    "operation": "RUN_SCRIPT",
    "expected_source_sha256": HASH,
    "timeout_seconds": 30,
}


class Authorizer:
    def __init__(self, allowed=True):
        self.allowed = allowed
        self.calls = []

    def authorize(self, trusted_caller, work_id):
        self.calls.append((trusted_caller, work_id))
        return self.allowed


class Snapshots:
    def __init__(self, **overrides):
        self.overrides = overrides
        self.calls = []

    def create_immutable_snapshot(self, work_id, entry_path):
        self.calls.append((work_id, entry_path))
        result = {
            "work_id": work_id, "entry_path": entry_path,
            "immutable": True, "source_sha256": HASH,
            "snapshot_ref": "snapshot://work28/sha256",
        }
        result.update(self.overrides)
        return result


class Runtime:
    def __init__(self, **overrides):
        self.overrides = overrides
        self.calls = []

    def execute_snapshot(self, snapshot, operation, timeout_seconds):
        self.calls.append((snapshot, operation, timeout_seconds))
        result = {
            "status": "PASS", "work_id": "work28", "source_sha256": HASH,
            "snapshot_ref": "snapshot://work28/sha256",
            "runtime_identity": "approved-runtime-8031",
            "process_tree_cleanup_verified": True,
        }
        result.update(self.overrides)
        return result


class AuthorizedAdapterTests(unittest.TestCase):
    def make_adapter(self, *, allowed=True, snapshot_overrides=None, runtime_overrides=None):
        self.auth = Authorizer(allowed)
        self.snapshots = Snapshots(**(snapshot_overrides or {}))
        self.runtime = Runtime(**(runtime_overrides or {}))
        adapter = AuthorizedExecutionAdapterV1(
            authorizer=self.auth, snapshots=self.snapshots, runtime=self.runtime,
            approved_runtime_identity="approved-runtime-8031",
        )
        return adapter

    def test_valid_request_passes_all_gates(self):
        adapter = self.make_adapter()
        result = adapter.run(dict(REQUEST), trusted_caller={"id": "caller-from-auth-middleware"})
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(len(self.auth.calls), 1)
        self.assertEqual(len(self.snapshots.calls), 1)
        self.assertEqual(len(self.runtime.calls), 1)

    def test_missing_trusted_caller_is_denied_before_snapshot_or_runtime(self):
        adapter = self.make_adapter()
        with self.assertRaises(PermissionError):
            adapter.run(dict(REQUEST), trusted_caller=None)
        self.assertEqual(self.snapshots.calls, [])
        self.assertEqual(self.runtime.calls, [])

    def test_core_authorization_denial_stops_before_snapshot_or_runtime(self):
        adapter = self.make_adapter(allowed=False)
        with self.assertRaises(PermissionError):
            adapter.run(dict(REQUEST), trusted_caller=object())
        self.assertEqual(self.snapshots.calls, [])
        self.assertEqual(self.runtime.calls, [])

    def test_public_request_cannot_smuggle_authority_or_command(self):
        adapter = self.make_adapter()
        for extra in ({"authorized": True}, {"principal": "admin"}, {"command": ["sh"]}):
            with self.subTest(extra=extra):
                with self.assertRaises(ValueError):
                    adapter.run({**REQUEST, **extra}, trusted_caller=object())
        self.assertEqual(self.auth.calls, [])
        self.assertEqual(self.runtime.calls, [])

    def test_hash_mismatch_fails_before_runtime_dispatch(self):
        adapter = self.make_adapter(snapshot_overrides={"source_sha256": "b" * 64})
        with self.assertRaisesRegex(RuntimeError, "source hash mismatch"):
            adapter.run(dict(REQUEST), trusted_caller=object())
        self.assertEqual(self.runtime.calls, [])

    def test_non_immutable_snapshot_fails_before_runtime_dispatch(self):
        adapter = self.make_adapter(snapshot_overrides={"immutable": False})
        with self.assertRaisesRegex(RuntimeError, "not attested immutable"):
            adapter.run(dict(REQUEST), trusted_caller=object())
        self.assertEqual(self.runtime.calls, [])

    def test_runtime_identity_mismatch_is_rejected(self):
        adapter = self.make_adapter(runtime_overrides={"runtime_identity": "unapproved"})
        with self.assertRaisesRegex(RuntimeError, "runtime identity mismatch"):
            adapter.run(dict(REQUEST), trusted_caller=object())

    def test_runtime_must_attest_same_snapshot(self):
        adapter = self.make_adapter(runtime_overrides={"snapshot_ref": "snapshot://other"})
        with self.assertRaisesRegex(RuntimeError, "exact immutable snapshot"):
            adapter.run(dict(REQUEST), trusted_caller=object())

    def test_failed_process_tree_cleanup_is_rejected(self):
        adapter = self.make_adapter(runtime_overrides={"process_tree_cleanup_verified": False})
        with self.assertRaisesRegex(RuntimeError, "cleanup is not verified"):
            adapter.run(dict(REQUEST), trusted_caller=object())

    def test_test_run_requires_nonempty_clean_test_summary(self):
        request = {**REQUEST, "operation": "RUN_TESTS"}
        for summary in (
            {"total": 0, "failed": 0, "errors": 0},
            {"total": 1, "failed": 1, "errors": 0},
            {"total": 1, "failed": 0, "errors": 1},
            {"total": True, "failed": 0, "errors": 0},
        ):
            with self.subTest(summary=summary):
                adapter = self.make_adapter(runtime_overrides={"test_summary": summary})
                with self.assertRaisesRegex(RuntimeError, "non-empty clean test summary"):
                    adapter.run(request, trusted_caller=object())

    def test_snapshot_work_or_path_mismatch_is_rejected(self):
        for overrides in (
            {"work_id": "other-work"},
            {"entry_path": "other.py"},
            {"snapshot_ref": ""},
        ):
            with self.subTest(overrides=overrides):
                adapter = self.make_adapter(snapshot_overrides=overrides)
                with self.assertRaises(RuntimeError):
                    adapter.run(dict(REQUEST), trusted_caller=object())
                self.assertEqual(self.runtime.calls, [])

    def test_constructor_requires_explicit_pinned_runtime_identity(self):
        with self.assertRaises(ValueError):
            AuthorizedExecutionAdapterV1(
                authorizer=Authorizer(), snapshots=Snapshots(), runtime=Runtime(),
                approved_runtime_identity="",
            )


if __name__ == "__main__":
    unittest.main()
