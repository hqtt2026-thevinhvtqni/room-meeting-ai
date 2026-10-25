"""Integration slice tests: Core authority - adapter - grant session.

The Core boundary uses the REAL ExecutionAuthority (append-only JSONL
store, no mocks at that boundary). Snapshot provider and runtime remain
injected test doubles BY DESIGN: no verified runtime implementation exists
yet, and that is exactly what Gate 3/4 must still evidence.

Proves, in order: from-chore denial BEFORE any side effect, snapshot/hash
checked BEFORE runtime dispatch, dispatch only on a fully attested result,
and the run recorded against the live grant with on-disk linkage.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.execution_authority.authority import (
    ExecutionAuthority,
    load_enrolled_identities,
)
from core.execution_authority.store import AppendOnlyRecordStore
from mcp8020_authorized_execution_adapter_v1 import AuthorizedExecutionAdapterV1
from mcp8020_core_authority_authorizer_v1 import (
    CoreAuthorityAuthorizer,
    CoreWorkIdError,
)
from mcp8020_core_execution_session_v1 import CoreGrantExecutionSession

HASH = "a" * 64
OTHER_HASH = "b" * 64


def build_authority(tmpdir):
    identities = load_enrolled_identities("mcp8020=secret-slice,other=secret-other")
    works = {
        "W28": {
            "work_name": "TOOLING", "workspace_root": "/w/28",
            "execution_workspace": "/w/28/run", "evidence_root": "/w/28/evidence",
            "allowed_identities": ["mcp8020"],
        }
    }
    store = AppendOnlyRecordStore(str(Path(tmpdir) / "records"))
    return ExecutionAuthority(store=store, enrolled_identities=identities, works=works)


class RecordingSnapshotProvider:
    def __init__(self, source_sha256):
        self._source_sha256 = source_sha256
        self.calls = []

    def create_immutable_snapshot(self, work_id, entry_path):
        self.calls.append((work_id, entry_path))
        return {
            "work_id": work_id,
            "entry_path": entry_path,
            "immutable": True,
            "source_sha256": self._source_sha256,
            "snapshot_ref": "snapshot://" + self._source_sha256[:12],
        }


class RecordingRuntime:
    def __init__(self, snapshot_provider):
        self._snapshot_provider = snapshot_provider
        self.calls = []

    def execute_snapshot(self, snapshot, operation, timeout_seconds):
        self.calls.append((snapshot["snapshot_ref"], operation, timeout_seconds))
        return {
            "status": "PASS",
            "exit_code": 0,
            "runtime_identity": "w13-approved-build",
            "work_id": snapshot["work_id"],
            "source_sha256": snapshot["source_sha256"],
            "snapshot_ref": snapshot["snapshot_ref"],
            "request_id": "req-slice-1",
            "run_id": "run-slice-1",
            "evidence_ref": "evidence://run-slice-1",
            "process_tree_cleanup_verified": True,
        }


def valid_request(work_id="W28"):
    return {
        "work_id": work_id,
        "entry_path": "04_CODE/smoke.py",
        "operation": "RUN_SCRIPT",
        "expected_source_sha256": HASH,
        "timeout_seconds": 30,
    }


class CoreAuthorizationSurfaceTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.authority = build_authority(self._tmp.name)

    def test_public_surface_semantics(self):
        self.assertIs(self.authority.is_identity_allowed_for_work("mcp8020", "W28"), True)
        self.assertIs(self.authority.is_identity_allowed_for_work("other", "W28"), False)
        self.assertIs(self.authority.is_identity_allowed_for_work("mcp8020", "W99"), False)
        self.assertIs(self.authority.is_identity_allowed_for_work(None, "W28"), False)
        self.assertIs(self.authority.is_identity_allowed_for_work("mcp8020", None), False)


class GrantSessionTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.authority = build_authority(self._tmp.name)

    def _store(self):
        return self.authority._store

    def test_denial_happens_before_any_side_effect(self):
        with self.assertRaises(PermissionError):
            CoreGrantExecutionSession(authority=self.authority, work_id="W28",
                                      credential="wrong", purpose="slice")
        with self.assertRaises(PermissionError):
            CoreGrantExecutionSession(authority=self.authority, work_id="W28",
                                      credential="secret-other", purpose="slice")
        with self.assertRaises(CoreWorkIdError):
            CoreGrantExecutionSession(authority=self.authority, work_id="work28",
                                      credential="secret-slice", purpose="slice")
        with self.assertRaises(TypeError):
            CoreGrantExecutionSession(authority=object(), work_id="W28",
                                      credential="secret-slice", purpose="slice")
        self.assertEqual(self._store().records(), [])

    def test_grant_lifecycle_closed_loop(self):
        session = CoreGrantExecutionSession(authority=self.authority, work_id="W28",
                                            credential="secret-slice", purpose="slice")
        self.assertEqual(session.validate_for_run()["status"], "active")
        run = session.record_run(source_sha256=HASH, exit_status="PASS",
                                output_refs=[], evidence_refs=["evidence://run-slice-1"],
                                handoff_ids=[])
        self.assertEqual(run["grant_id"], session.grant_id)
        self.assertEqual(len(self._store().records("run")), 1)
        session.revoke()
        with self.assertRaises(PermissionError):
            session.validate_for_run()
        with self.assertRaises(PermissionError):
            session.record_run(source_sha256=HASH, exit_status="PASS",
                               output_refs=[], evidence_refs=["evidence://x"], handoff_ids=[])
        self.assertEqual(len(self._store().records("run")), 1)


class AdapterWithRealCoreTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.authority = build_authority(self._tmp.name)
        self.snapshots = RecordingSnapshotProvider(HASH)
        self.runtime = RecordingRuntime(self.snapshots)
        self.adapter = AuthorizedExecutionAdapterV1(
            authorizer=CoreAuthorityAuthorizer(authority=self.authority),
            snapshots=self.snapshots,
            runtime=self.runtime,
            approved_runtime_identity="w13-approved-build",
        )

    def _store(self):
        return self.authority._store

    def test_full_slice_run_recorded_against_live_grant(self):
        session = CoreGrantExecutionSession(authority=self.authority, work_id="W28",
                                            credential="secret-slice", purpose="slice")
        result = self.adapter.run(valid_request(), trusted_caller={"credential": "secret-slice"})
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(len(self.snapshots.calls), 1)
        self.assertEqual(len(self.runtime.calls), 1)
        run = session.record_run(source_sha256=HASH, exit_status="PASS",
                                 output_refs=["stdout://run-slice-1"],
                                 evidence_refs=[result["evidence_ref"]],
                                 handoff_ids=[])
        self.assertEqual(run["grant_id"], session.grant_id)
        self.assertEqual(run["source_sha256"], HASH)
        self.assertEqual(run["evidence_refs"], ["evidence://run-slice-1"])
        stored = self._store().records()
        self.assertEqual(len([r for r in stored if r["record_type"] == "grant"]), 1)
        self.assertEqual(len([r for r in stored if r["record_type"] == "run"]), 1)
        blob = json.dumps(stored)
        self.assertNotIn("secret-slice", blob)
        self.assertNotIn("secret-other", blob)

    def test_authorization_denied_before_snapshot_and_runtime(self):
        with self.assertRaises(PermissionError):
            self.adapter.run(valid_request(), trusted_caller={"credential": "secret-other"})
        self.assertEqual(self.snapshots.calls, [])
        self.assertEqual(self.runtime.calls, [])

    def test_snapshot_hash_mismatch_refuses_dispatch(self):
        bad_provider = RecordingSnapshotProvider(OTHER_HASH)
        bad_runtime = RecordingRuntime(bad_provider)
        adapter = AuthorizedExecutionAdapterV1(
            authorizer=CoreAuthorityAuthorizer(authority=self.authority),
            snapshots=bad_provider,
            runtime=bad_runtime,
            approved_runtime_identity="w13-approved-build",
        )
        with self.assertRaises(RuntimeError):
            adapter.run(valid_request(), trusted_caller={"credential": "secret-slice"})
        self.assertEqual(len(bad_provider.calls), 1)
        self.assertEqual(bad_runtime.calls, [])


if __name__ == "__main__":
    unittest.main()
