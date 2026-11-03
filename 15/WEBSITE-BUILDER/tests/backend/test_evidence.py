"""Tests for the evidence system (issue #34, parts D + E)."""

from __future__ import annotations

import json

import pytest

from roomhop_builder.errors import ValidationError
from roomhop_builder.evidence import (
    EvidenceStore,
    REQUIRED_KINDS,
    compute_code_version,
)


def fill_all(store: EvidenceStore, job_id: str) -> None:
    for kind in REQUIRED_KINDS:
        store.add(job_id, kind, summary=f"{kind} recorded", code_version="git:abc123")


def test_empty_bundle_is_incomplete_and_lists_missing():
    store = EvidenceStore()
    assert store.is_complete("W15-x") is False
    assert store.missing_kinds("W15-x") == list(REQUIRED_KINDS)


def test_partial_bundle_still_incomplete():
    store = EvidenceStore()
    store.add("W15-a", "diff", summary="files changed", code_version="git:1")
    store.add("W15-a", "log", summary="build log", code_version="git:1")
    assert store.is_complete("W15-a") is False
    assert set(store.missing_kinds("W15-a")) == {"preview", "e2e", "runtime_status"}


def test_full_bundle_is_complete():
    store = EvidenceStore()
    fill_all(store, "W15-full")
    assert store.is_complete("W15-full")
    assert store.missing_kinds("W15-full") == []


def test_unknown_kind_rejected():
    store = EvidenceStore()
    with pytest.raises(ValidationError) as exc:
        store.add("W15-b", "vibes", summary="looks good to me", code_version="git:1")
    assert exc.value.details["allowed"]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"summary": "", "code_version": "git:1"},
        {"summary": "ok", "code_version": ""},
        {"summary": "   ", "code_version": "git:1"},
    ],
)
def test_blank_summary_or_version_rejected(kwargs):
    store = EvidenceStore()
    with pytest.raises(ValidationError):
        store.add("W15-c", "log", **kwargs)


def test_records_are_content_addressed_and_deterministic():
    store = EvidenceStore()
    a = store.add("W15-d", "e2e", summary="pass 12/12", code_version="git:1",
                  payload={"cases": 12})
    b = store.add("W15-d", "e2e", summary="pass 12/12", code_version="git:1",
                  payload={"cases": 12})
    c = store.add("W15-d", "e2e", summary="fail 1/12", code_version="git:1",
                  payload={"cases": 12})
    assert a.sha256 == b.sha256  # same content -> same fingerprint
    assert c.sha256 != a.sha256


def test_jsonl_mirror_written_to_disk(tmp_path):
    store = EvidenceStore(root=tmp_path / "evidence")
    store.add("W15-e", "preview", summary="http://127.0.0.1:8099", code_version="git:9",
              payload={"http_status": 200})
    lines = (tmp_path / "evidence" / "W15-e.jsonl").read_text(encoding="utf-8").strip()
    record = json.loads(lines)
    assert record["kind"] == "preview"
    assert record["code_version"] == "git:9"
    assert record["sha256"]


def test_manifest_reports_completeness_and_versions(tmp_path):
    store = EvidenceStore(root=tmp_path)
    fill_all(store, "W15-m")
    store.add("W15-m", "note", summary="extra context", code_version="git:1")
    manifest = store.manifest("W15-m")
    assert manifest["complete"] is True
    assert manifest["missing"] == []
    assert manifest["count"] == len(REQUIRED_KINDS) + 1
    assert all(r["code_version"] for r in manifest["records"])


def test_code_version_prefers_git_sha(tmp_path):
    version = compute_code_version(tmp_path)
    # In this repo it resolves to a git SHA; outside git it falls back to tree hash.
    assert version.startswith(("git:", "tree:"))


def test_success_gate_uses_evidence_store_end_to_end():
    """The state machine must consult the real store, not a boolean shortcut."""
    from roomhop_builder.jobs import JobStore, JobState
    from roomhop_builder.errors import EvidenceMissingError

    store = EvidenceStore()
    jobs = JobStore(evidence_checker=store.is_complete)
    job = jobs.create({"intent": "site", "site_name": "s", "created_by": "vinh"})
    jobs.transition(job.id, JobState.RUNNING, reason="start")

    with pytest.raises(EvidenceMissingError):
        jobs.transition(job.id, JobState.SUCCEEDED, reason="claims done")

    fill_all(store, job.id)
    done = jobs.transition(job.id, JobState.SUCCEEDED, reason="proof on disk")
    assert done.state is JobState.SUCCEEDED
