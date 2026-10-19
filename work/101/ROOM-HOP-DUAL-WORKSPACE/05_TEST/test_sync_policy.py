import sys
import unittest
from pathlib import Path

# Resolve the Work's declared code directory without requiring a caller-supplied
# PYTHONPATH. This is test discovery setup, not an execution sandbox.
CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
sys.path.insert(0, str(CODE_DIR))

from sync_policy import (
    ApprovalBinding, ChangeState, PolicyError, Snapshot, bind_approval,
    build_sync_plan, canonical_relative_path, classify_sync, enforce_idempotency, sha256_text,
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

    def test_rejects_windows_invalid_filename_characters(self):
        for path in ("04_CODE/a?.py", "04_CODE/a*.py", "04_CODE/a|b.txt", "04_CODE/a<b.txt"):
            with self.subTest(path=path), self.assertRaises(PolicyError):
                canonical_relative_path(path)

    def test_rejects_os_metadata_temp_files_and_private_key_material(self):
        for path in (
            "desktop.ini", "Thumbs.db", ".DS_Store", "tmp/cache.tmp",
            "backup/archive.bak", "secrets/private.pem", "certs/client.p12",
            "docs/~$draft.docx",
        ):
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

    def test_plan_is_dry_run_and_directional(self):
        base = snap("b1", {"04_CODE/a.py": "old", "05_TEST/t.py": "old"})
        source = snap("s1", {"04_CODE/a.py": "new", "05_TEST/t.py": "old"}, base_revision="b1")
        dest = snap("d1", {"04_CODE/a.py": "old", "05_TEST/t.py": "new"}, base_revision="b1")
        plan = build_sync_plan(
            operation_id="op-101-1", work_id="101", destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/", "05_TEST/"),
        )
        self.assertEqual(plan.mode, "DRY_RUN")
        self.assertEqual(plan.source_to_destination, ("04_CODE/a.py",))
        self.assertEqual(plan.destination_to_source, ("05_TEST/t.py",))
        self.assertEqual(len(plan.diff_digest), 64)

    def test_plan_blocks_conflicts_without_transfer(self):
        base = snap("b1", {"04_CODE/a.py": "old"})
        source = snap("s1", {"04_CODE/a.py": "source"}, base_revision="b1")
        dest = snap("d1", {"04_CODE/a.py": "destination"}, base_revision="b1")
        plan = build_sync_plan(
            operation_id="op-101-2", work_id="101", destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/",),
        )
        self.assertEqual(plan.state, ChangeState.CONFLICT_PENDING)
        self.assertEqual(plan.source_to_destination, ())
        self.assertEqual(plan.destination_to_source, ())
        self.assertEqual(plan.conflict_paths, ("04_CODE/a.py",))

    def test_plan_rejects_main_and_paths_outside_allowlist(self):
        base = snap("b1", {"04_CODE/a.py": "old"})
        source = snap("s1", {"04_CODE/a.py": "new"}, base_revision="b1")
        dest = snap("d1", {"04_CODE/a.py": "old"}, base_revision="b1")
        args = dict(operation_id="op-101-3", work_id="101", base_revision="b1", base=base,
                    source=source, destination=dest, permitted_path_roots=("04_CODE/",))
        with self.assertRaises(PolicyError):
            build_sync_plan(destination_branch="main", **args)
        outside = snap("s2", {"00_ROOT/config.yaml": "x"}, base_revision="b1")
        with self.assertRaises(PolicyError):
            build_sync_plan(destination_branch="work/101-room-hop-dual-workspace", **{**args, "source": outside})


    def test_plan_digest_binds_actual_content_hashes(self):
        base = snap("b1", {"04_CODE/a.py": "old"})
        source_a = snap("s1", {"04_CODE/a.py": "new-a"}, base_revision="b1")
        source_b = snap("s1", {"04_CODE/a.py": "new-b"}, base_revision="b1")
        dest = snap("d1", {"04_CODE/a.py": "old"}, base_revision="b1")
        common = dict(operation_id="op-101-digest", work_id="101",
                      destination_branch="work/101-room-hop-dual-workspace",
                      base_revision="b1", base=base, destination=dest,
                      permitted_path_roots=("04_CODE/",))
        plan_a = build_sync_plan(source=source_a, **common)
        plan_b = build_sync_plan(source=source_b, **common)
        self.assertNotEqual(plan_a.diff_digest, plan_b.diff_digest)

    def test_plan_requires_explicit_baseline_markers(self):
        base = snap("b1", {"04_CODE/a.py": "old"})
        source = snap("s1", {"04_CODE/a.py": "new"})
        dest = snap("d1", {"04_CODE/a.py": "old"}, base_revision="b1")
        with self.assertRaises(PolicyError):
            build_sync_plan(
                operation_id="op-101-missing-base", work_id="101",
                destination_branch="work/101-room-hop-dual-workspace",
                base_revision="b1", base=base, source=source, destination=dest,
                permitted_path_roots=("04_CODE/",),
            )


    def test_source_deletion_requires_review_and_blocks_all_transfers(self):
        base = snap("b1", {"04_CODE/a.py": "old", "05_TEST/t.py": "old"})
        source = snap("s1", {"05_TEST/t.py": "old"}, base_revision="b1")
        dest = snap("d1", {"04_CODE/a.py": "old", "05_TEST/t.py": "old"}, base_revision="b1")
        plan = build_sync_plan(
            operation_id="op-101-delete-source", work_id="101",
            destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/", "05_TEST/"),
        )
        self.assertEqual(plan.state, ChangeState.DELETION_PENDING)
        self.assertEqual(plan.conflict_paths, ("04_CODE/a.py",))
        self.assertEqual(plan.source_to_destination, ())
        self.assertEqual(plan.destination_to_source, ())

    def test_bilateral_deletion_still_requires_review(self):
        base = snap("b1", {"04_CODE/a.py": "old"})
        source = snap("s1", {}, base_revision="b1")
        dest = snap("d1", {}, base_revision="b1")
        plan = build_sync_plan(
            operation_id="op-101-delete-both", work_id="101",
            destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/",),
        )
        self.assertEqual(plan.state, ChangeState.DELETION_PENDING)
        self.assertEqual(plan.conflict_paths, ("04_CODE/a.py",))
        self.assertEqual(plan.destination_to_source, ())
        self.assertEqual(plan.source_to_destination, ())

    def test_destination_deletion_requires_review(self):
        base = snap("b1", {"04_CODE/a.py": "old"})
        source = snap("s1", {"04_CODE/a.py": "old"}, base_revision="b1")
        dest = snap("d1", {}, base_revision="b1")
        plan = build_sync_plan(
            operation_id="op-101-delete-destination", work_id="101",
            destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/",),
        )
        self.assertEqual(plan.state, ChangeState.DELETION_PENDING)
        self.assertEqual(plan.destination_to_source, ())
        self.assertEqual(plan.source_to_destination, ())

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

    def test_plan_digest_includes_all_binding_fields(self):
        base = snap("b1", {"04_CODE/a.py": "old"})
        source = snap("s1", {"04_CODE/a.py": "new"}, base_revision="b1")
        dest = snap("d1", {"04_CODE/a.py": "old"}, base_revision="b1")
        
        plan_a = build_sync_plan(
            operation_id="op-1", work_id="101",
            destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/",),
        )
        
        plan_b = build_sync_plan(
            operation_id="op-2", work_id="101",
            destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/",),
        )
        
        plan_c = build_sync_plan(
            operation_id="op-1", work_id="101",
            destination_branch="work/101-other-branch",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/",),
        )
        
        plan_d = build_sync_plan(
            operation_id="op-1", work_id="101",
            destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b2", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/",),
        )
        
        # Different operation_id = different digest
        self.assertNotEqual(plan_a.diff_digest, plan_b.diff_digest)
        # Different branch = different digest
        self.assertNotEqual(plan_a.diff_digest, plan_c.diff_digest)
        # Different base_revision = different digest
        self.assertNotEqual(plan_a.diff_digest, plan_d.diff_digest)

    def test_plan_rejects_empty_permitted_roots(self):
        base = snap("b1", {"04_CODE/a.py": "old"})
        source = snap("s1", {"04_CODE/a.py": "new"}, base_revision="b1")
        dest = snap("d1", {"04_CODE/a.py": "old"}, base_revision="b1")
        
        with self.assertRaises(PolicyError):
            build_sync_plan(
                operation_id="op-1", work_id="101",
                destination_branch="work/101-room-hop-dual-workspace",
                base_revision="b1", base=base, source=source, destination=dest,
                permitted_path_roots=[],
            )

    def test_plan_with_multiple_permitted_roots(self):
        base = snap("b1", {
            "04_CODE/a.py": "old",
            "05_TEST/t.py": "old",
            "06_EVIDENCE/report.md": "old"
        })
        source = snap("s1", {
            "04_CODE/a.py": "new",
            "05_TEST/t.py": "old",
            "06_EVIDENCE/report.md": "old"
        }, base_revision="b1")
        dest = snap("d1", {
            "04_CODE/a.py": "old",
            "05_TEST/t.py": "new",
            "06_EVIDENCE/report.md": "old"
        }, base_revision="b1")
        
        plan = build_sync_plan(
            operation_id="op-multi-root", work_id="101",
            destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/", "05_TEST/", "06_EVIDENCE/"),
        )
        
        self.assertEqual(plan.state, ChangeState.NON_OVERLAPPING)
        self.assertEqual(plan.source_to_destination, ("04_CODE/a.py",))
        self.assertEqual(plan.destination_to_source, ("05_TEST/t.py",))

    def test_path_outside_allowlist_rejected_in_snapshot(self):
        base = snap("b1", {"04_CODE/a.py": "old", "00_ROOT/secret.txt": "x"})
        source = snap("s1", {"04_CODE/a.py": "new"}, base_revision="b1")
        dest = snap("d1", {"04_CODE/a.py": "old"}, base_revision="b1")
        
        with self.assertRaises(PolicyError):
            build_sync_plan(
                operation_id="op-1", work_id="101",
                destination_branch="work/101-room-hop-dual-workspace",
                base_revision="b1", base=base, source=source, destination=dest,
                permitted_path_roots=("04_CODE/",),
            )

    def test_empty_snapshots_handled(self):
        base = snap("b1", {})
        source = snap("s1", {}, base_revision="b1")
        dest = snap("d1", {}, base_revision="b1")
        
        plan = build_sync_plan(
            operation_id="op-empty", work_id="101",
            destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/",),
        )
        
        self.assertEqual(plan.state, ChangeState.NO_CHANGE)
        self.assertEqual(plan.source_to_destination, ())
        self.assertEqual(plan.destination_to_source, ())

    def test_new_file_addition_in_source(self):
        base = snap("b1", {"04_CODE/a.py": "old"})
        source = snap("s1", {"04_CODE/a.py": "old", "04_CODE/b.py": "new"}, base_revision="b1")
        dest = snap("d1", {"04_CODE/a.py": "old"}, base_revision="b1")
        
        plan = build_sync_plan(
            operation_id="op-new-file", work_id="101",
            destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/",),
        )
        
        self.assertEqual(plan.state, ChangeState.SOURCE_ONLY)
        self.assertEqual(plan.source_to_destination, ("04_CODE/b.py",))

    def test_new_file_addition_in_destination(self):
        base = snap("b1", {"04_CODE/a.py": "old"})
        source = snap("s1", {"04_CODE/a.py": "old"}, base_revision="b1")
        dest = snap("d1", {"04_CODE/a.py": "old", "04_CODE/c.py": "new"}, base_revision="b1")
        
        plan = build_sync_plan(
            operation_id="op-new-file-dest", work_id="101",
            destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/",),
        )
        
        self.assertEqual(plan.state, ChangeState.DESTINATION_ONLY)
        self.assertEqual(plan.destination_to_source, ("04_CODE/c.py",))

    def test_plan_includes_work_id_in_digest(self):
        base = snap("b1", {"04_CODE/a.py": "old"})
        source = snap("s1", {"04_CODE/a.py": "new"}, base_revision="b1")
        dest = snap("d1", {"04_CODE/a.py": "old"}, base_revision="b1")
        
        plan_101 = build_sync_plan(
            operation_id="op-1", work_id="101",
            destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/",),
        )
        
        plan_102 = build_sync_plan(
            operation_id="op-1", work_id="102",
            destination_branch="work/101-room-hop-dual-workspace",
            base_revision="b1", base=base, source=source, destination=dest,
            permitted_path_roots=("04_CODE/",),
        )
        
        # Different work_id = different digest
        self.assertNotEqual(plan_101.diff_digest, plan_102.diff_digest)


if __name__ == "__main__":
    unittest.main()
