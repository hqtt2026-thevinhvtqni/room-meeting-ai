"""Tests for the real immutable source snapshot provider.

Runs against a REAL filesystem (CI runner): containment, symlink refusal,
per-run immutable copies, hash from actual content, refusal on drift, and
the full slice with the real Core authority (session -> adapter -> run
recorded against the live grant with on-disk linkage).
"""
from __future__ import annotations

import hashlib
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
from mcp8020_core_authority_authorizer_v1 import CoreAuthorityAuthorizer
from mcp8020_core_execution_session_v1 import CoreGrantExecutionSession
from mcp8020_source_snapshot_provider_v1 import (
    ImmutableSourceSnapshotProvider,
    SourceSnapshotError,
)

CONTENT = "print('work28-snapshot-ok')" 
HASH = hashlib.sha256(CONTENT.encode("utf-8")).hexdigest()
OTHER_HASH = "b" * 64


def build_authority(tmpdir):
    identities = load_enrolled_identities("mcp8020=secret-snap")
    works = {
        "W28": {
            "work_name": "TOOLING", "workspace_root": "/w/28",
            "execution_workspace": "/w/28/run", "evidence_root": "/w/28/evidence",
            "allowed_identities": ["mcp8020"],
        }
    }
    store = AppendOnlyRecordStore(str(Path(tmpdir) / "records"))
    return ExecutionAuthority(store=store, enrolled_identities=identities, works=works)


def make_workspace(root, work_id="W28", content=CONTENT):
    ws = Path(root) / "workspaces" / work_id / "04_CODE"
    ws.mkdir(parents=True, exist_ok=True)
    entry = ws / "smoke.py"
    entry.write_text(content, encoding="utf-8")
    return entry


class RecordingRuntime:
    def __init__(self):
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
            "request_id": "req-snap-1",
            "run_id": "run-snap-1",
            "evidence_ref": "evidence://run-snap-1",
            "process_tree_cleanup_verified": True,
        }


def valid_request():
    return {
        "work_id": "W28",
        "entry_path": "04_CODE/smoke.py",
        "operation": "RUN_SCRIPT",
        "expected_source_sha256": HASH,
        "timeout_seconds": 30,
    }


class SnapshotProviderTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.entry = make_workspace(self.root)
        self.provider = ImmutableSourceSnapshotProvider(
            workspaces_root=self.root / "workspaces",
            snapshots_root=self.root / "snapshots",
        )

    def test_snapshot_hash_from_actual_content(self):
        snap = self.provider.create_immutable_snapshot("W28", "04_CODE/smoke.py")
        self.assertTrue(snap["immutable"])
        self.assertEqual(snap["source_sha256"], HASH)
        self.assertTrue(snap["snapshot_ref"].startswith("snapshot://"))
        copy = self.root / "snapshots" / "W28" / snap["run_id"] / "source"
        self.assertEqual(copy.read_text(encoding="utf-8"), CONTENT)
        metadata = json.loads((copy.parent / "metadata.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["source_sha256"], HASH)
        self.assertEqual(metadata["work_id"], "W28")
        self.assertEqual(metadata["entry_path"], "04_CODE/smoke.py")

    def test_per_run_copy_is_immutable(self):
        snap = self.provider.create_immutable_snapshot("W28", "04_CODE/smoke.py")
        self.entry.write_text("print('tampered')", encoding="utf-8")
        copy = self.root / "snapshots" / "W28" / snap["run_id"] / "source"
        self.assertEqual(copy.read_text(encoding="utf-8"), CONTENT)
        drifted = self.provider.create_immutable_snapshot("W28", "04_CODE/smoke.py")
        self.assertNotEqual(drifted["source_sha256"], HASH)
        self.assertNotEqual(drifted["run_id"], snap["run_id"])

    def test_unsafe_paths_and_unknown_work_refused(self):
        cases = ["/abs/path.py", "../escape.py", "a/../b.py", "a//b.py", "folder /x.py", "folder./x.py", "C:/x.py"]
        for entry_path in cases:
            with self.subTest(entry_path=entry_path):
                with self.assertRaises(SourceSnapshotError):
                    self.provider.create_immutable_snapshot("W28", entry_path)
        with self.assertRaises(SourceSnapshotError):
            self.provider.create_immutable_snapshot("W99", "04_CODE/smoke.py")
        with self.assertRaises(Exception):
            self.provider.create_immutable_snapshot("work28", "04_CODE/smoke.py")

    def test_symlink_component_refused(self):
        real = Path(self._tmp.name) / "realdir"
        real.mkdir()
        (real / "smoke.py").write_text(CONTENT, encoding="utf-8")
        ws = self.root / "workspaces" / "W28" / "04_CODE"
        link = ws / "linkdir"
        link.symlink_to(real)
        with self.assertRaises(SourceSnapshotError):
            self.provider.create_immutable_snapshot("W28", "04_CODE/linkdir/smoke.py")


class FullSliceWithRealSnapshotTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.entry = make_workspace(self.root)
        self.authority = build_authority(self._tmp.name)
        self.provider = ImmutableSourceSnapshotProvider(
            workspaces_root=self.root / "workspaces",
            snapshots_root=self.root / "snapshots",
        )
        self.runtime = RecordingRuntime()

    def _adapter(self):
        return AuthorizedExecutionAdapterV1(
            authorizer=CoreAuthorityAuthorizer(authority=self.authority),
            snapshots=self.provider,
            runtime=self.runtime,
            approved_runtime_identity="w13-approved-build",
        )

    def test_full_slice_real_snapshot_real_core(self):
        session = CoreGrantExecutionSession(authority=self.authority, work_id="W28",
                                            credential="secret-snap", purpose="snapshot-slice")
        result = self._adapter().run(valid_request(), trusted_caller={"credential": "secret-snap"})
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(len(self.runtime.calls), 1)
        run = session.record_run(source_sha256=HASH, exit_status="PASS",
                                 output_refs=["stdout://run-snap-1"],
                                 evidence_refs=[result["evidence_ref"]], handoff_ids=[])
        self.assertEqual(run["grant_id"], session.grant_id)
        self.assertEqual(run["source_sha256"], HASH)
        stored_runs = self.authority._store.records("run")
        self.assertEqual(len(stored_runs), 1)
        blob = json.dumps(self.authority._store.records())
        self.assertNotIn("secret-snap", blob)

    def test_hash_drift_refuses_dispatch(self):
        request = valid_request()
        request["expected_source_sha256"] = OTHER_HASH
        with self.assertRaises(RuntimeError):
            self._adapter().run(request, trusted_caller={"credential": "secret-snap"})
        self.assertEqual(self.runtime.calls, [])
        self.assertEqual(self.authority._store.records("run"), [])

    def test_tampered_source_refuses_dispatch(self):
        self.entry.write_text("print('tampered')", encoding="utf-8")
        with self.assertRaises(RuntimeError):
            self._adapter().run(valid_request(), trusted_caller={"credential": "secret-snap"})
        self.assertEqual(self.runtime.calls, [])
        self.assertEqual(self.authority._store.records("run"), [])


if __name__ == "__main__":
    unittest.main()
