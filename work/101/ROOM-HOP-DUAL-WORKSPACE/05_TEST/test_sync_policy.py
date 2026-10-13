import sys
import unittest
from pathlib import Path

# Resolve the Work's declared code directory without requiring a caller-supplied
# PYTHONPATH. This is test discovery setup, not an execution sandbox.
CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
sys.path.insert(0, str(CODE_DIR))

from sync_policy import (
    ApprovalBinding, ChangeState, PolicyError, Snapshot, bind_approval,
    canonical_relative_path, classify_sync, enforce_idempotency, sha256_text,
)


def snap(revision, files, base_revision=None):
    return Snapshot(revision, {p: sha256_text(v) for p, v in files.items()}, base_revision)


class SyncPolicyTests(unittest.TestCase):
    def test_canonical_path_accepts_scoped_relative_path(self):
        self.assertEqual(canonical_relative_path("src/module.py"), "src/module.py")

    def test_rejects_traversal_absolute_drive_and_ads(self):
        for path in ("../secret.txt", "/etc/passwd", "\\rooted.txt", "src\\nested.txt", "C:/temp/a.py", "src/file.txt:secret"):
            with self.subTest(path=path), self.assertRaises(PolicyError):
                canonical_relative_path(path)

    def test_rejects_secrets_databases_logs_and_generated_files(self):
        for path in (".env", "data/app_workspace.db", "logs/app.log", "dist/app.js", "x/__pycache__/a.pyc"):
            with self.subTest(path=path), self.assertRaises(PolicyError):
                canonical_relative_path(path)

    def test_evidence_documents_are_allowed_but_evidence_logs_are_not(self):
        self.assertEqual(canonical_relative_path("06_EVIDENCE/report.md"), "06_EVIDENCE/report.md")
        with self.assertRaises(PolicyError):
            canonical_relative_path("06_EVIDENCE/runtime.log")

    def test_snapshot_rejects_case_insensitive_path_collisions(self):
        collision = Snapshot("s1", {"Config.json": sha256_text("a"), "config.json": sha256_text("b")})
        with self.assertRaises(PolicyError):
            classify_sync(snap("b1", {}), collision, snap("d1", {}))

    def test_stale_source_baseline_is_blocked(self):
        base = snap("b1", {"a.txt": "old"})
        source = snap("s1", {"a.txt": "new"}, base_revision="older-base")
        dest = snap("d1", {"a.txt": "old"}, base_revision="b1")
        result = classify_sync(base, source, dest)
        self.assertEqual(result.state, ChangeState.STALE_BASE)
        self.assertEqual(result.reason, "SOURCE_BASE_REVISION_MISMATCH")

    def test_source_only_change(self):
        base = snap("b1", {"a.txt": "old"})
        source = snap("s1", {"a.txt": "new"})
        dest = snap("d1", {"a.txt": "old"})
        self.assertEqual(classify_sync(base, source, dest).state, ChangeState.SOURCE_ONLY)

    def test_non_overlapping_changes(self):
        base = snap("b1", {"a.txt": "a", "b.txt": "b"})
        source = snap("s1", {"a.txt": "A", "b.txt": "b"})
        dest = snap("d1", {"a.txt": "a", "b.txt": "B"})
        self.assertEqual(classify_sync(base, source, dest).state, ChangeState.NON_OVERLAPPING)

    def test_same_path_different_content_is_conflict(self):
        base = snap("b1", {"a.txt": "old"})
        source = snap("s1", {"a.txt": "source"})
        dest = snap("d1", {"a.txt": "destination"})
        result = classify_sync(base, source, dest)
        self.assertEqual(result.state, ChangeState.CONFLICT_PENDING)
        self.assertEqual(result.conflict_paths, ("a.txt",))

    def test_same_path_same_content_is_not_conflict(self):
        base = snap("b1", {"a.txt": "old"})
        source = snap("s1", {"a.txt": "new"})
        dest = snap("d1", {"a.txt": "new"})
        self.assertEqual(classify_sync(base, source, dest).state, ChangeState.NON_OVERLAPPING)

    def test_approval_must_match_exact_binding(self):
        approved = ApprovalBinding("op-1", "a" * 64, "feature/sync", "base-sha")
        bind_approval(approved, approved)
        altered = ApprovalBinding("op-1", "b" * 64, "feature/sync", "base-sha")
        with self.assertRaises(PolicyError):
            bind_approval(approved, altered)

    def test_idempotency_same_payload_replays_same_fingerprint(self):
        first = enforce_idempotency(None, "op-1", {"digest": "a" * 64})
        self.assertEqual(enforce_idempotency(first, "op-1", {"digest": "a" * 64}), first)

    def test_idempotency_rejects_payload_mutation(self):
        first = enforce_idempotency(None, "op-1", {"digest": "a" * 64})
        with self.assertRaises(PolicyError):
            enforce_idempotency(first, "op-1", {"digest": "b" * 64})


if __name__ == "__main__":
    unittest.main()
