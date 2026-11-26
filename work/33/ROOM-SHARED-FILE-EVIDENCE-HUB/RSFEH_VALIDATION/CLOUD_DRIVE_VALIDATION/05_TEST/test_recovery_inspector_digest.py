"""Regression tests for COMMITTING provider verification after a crash."""
import hashlib
import sqlite3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from cloud_drive.storage.protocol import ObjectRef, StoredObject
from cloud_drive.uploads.recovery_inspector import RecoveryInspector

class FakeStorage:
    def __init__(self, payload: bytes):
        self.payload = payload
    def head(self, ref: ObjectRef):
        return StoredObject(ref, len(self.payload), hashlib.sha256(self.payload).hexdigest())

def make_db(path: Path, *, expected_sha256=None, commit_sha256=None, commit_size=None):
    db = sqlite3.connect(path)
    db.executescript("""
        CREATE TABLE upload_sessions(
            session_id TEXT PRIMARY KEY, scope_id TEXT NOT NULL, object_key TEXT NOT NULL,
            status TEXT NOT NULL, expires_at INTEGER NOT NULL, expected_size INTEGER NOT NULL,
            expected_sha256 TEXT, completed_size INTEGER, completed_sha256 TEXT,
            commit_sha256 TEXT, commit_size INTEGER, commit_manifest_version INTEGER
        );
        CREATE TABLE upload_parts(
            session_id TEXT NOT NULL, part_number INTEGER NOT NULL,
            size_bytes INTEGER NOT NULL, sha256 TEXT NOT NULL
        );
    """)
    db.execute(
        "INSERT INTO upload_sessions VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
        ("a" * 32, "scope-a", "scope-a/object-1", "COMMITTING", 9999999999, 7, expected_sha256, None, None, commit_sha256, commit_size, 1 if commit_sha256 else None),
    )
    db.commit(); db.close()

def test_committing_without_expected_digest_never_claims_provider_match(tmp_path):
    db_path = tmp_path / "upload.sqlite3"
    make_db(db_path, expected_sha256=None)
    staging = tmp_path / "staging"
    staging.mkdir()
    inspector = RecoveryInspector(str(db_path), str(staging), FakeStorage(b"WRONG!!"))
    before = db_path.read_bytes()
    findings = inspector.inspect(now=1)
    after = db_path.read_bytes()

    assert before == after, "recovery inspection must remain read-only"
    assert any(x["kind"] == "COMMITTING_COMMITMENT_MISSING_OR_INVALID" and x["severity"] == "CRITICAL" for x in findings)
    assert not any("MATCHES" in x["kind"] for x in findings)

def test_committing_with_digest_detects_provider_hash_mismatch(tmp_path):
    db_path = tmp_path / "upload.sqlite3"
    expected = hashlib.sha256(b"RIGHT!!").hexdigest()
    make_db(db_path, expected_sha256=None, commit_sha256=expected, commit_size=7)
    staging = tmp_path / "staging"
    staging.mkdir()
    inspector = RecoveryInspector(str(db_path), str(staging), FakeStorage(b"WRONG!!"))
    findings = inspector.inspect(now=1)

    assert any(x["kind"] == "COMMITTING_PROVIDER_OBJECT_MISMATCH" for x in findings)
    assert not any(x["kind"] == "COMMITTING_PROVIDER_OBJECT_MATCHES_EXPECTATION" for x in findings)


def test_committing_with_matching_persisted_commitment_is_only_match_case(tmp_path):
    db_path = tmp_path / "upload.sqlite3"
    expected = hashlib.sha256(b"RIGHT!!").hexdigest()
    make_db(db_path, commit_sha256=expected, commit_size=7)
    staging = tmp_path / "staging"
    staging.mkdir()
    inspector = RecoveryInspector(str(db_path), str(staging), FakeStorage(b"RIGHT!!"))
    findings = inspector.inspect(now=1)
    assert any(x["kind"] == "COMMITTING_PROVIDER_OBJECT_MATCHES_COMMITMENT" for x in findings)


def test_committing_provider_without_digest_is_unconfirmed(tmp_path):
    class NoDigestStorage:
        def head(self, ref):
            return type("Head", (), {"size_bytes": 7, "sha256": None})()
    db_path = tmp_path / "upload.sqlite3"
    expected = hashlib.sha256(b"RIGHT!!").hexdigest()
    make_db(db_path, commit_sha256=expected, commit_size=7)
    staging = tmp_path / "staging"
    staging.mkdir()
    findings = RecoveryInspector(str(db_path), str(staging), NoDigestStorage()).inspect(now=1)
    assert any(x["kind"] == "COMMITTING_PROVIDER_OBJECT_UNCONFIRMED" for x in findings)
    assert not any("MATCHES" in x["kind"] for x in findings)
