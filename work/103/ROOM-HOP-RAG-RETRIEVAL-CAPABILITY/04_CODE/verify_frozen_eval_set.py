"""Work 103 — Verify a frozen labeled evaluation set against its freeze record.

Recomputes SHA-256 fingerprints of the current EVAL_SET.json and compares them
with the committed freeze manifest (FROZEN_EVAL_SET_v2.json). Then re-runs the
approved evaluation procedure on the frozen set and checks that every gate
metric matches the recorded values exactly (ranking metrics are deterministic;
latency is excluded from comparison by design).

Usage:
    python verify_frozen_eval_set.py [--manifest ../06_EVIDENCE/FROZEN_EVAL_SET_v2.json]
Exit codes:
    0 = FROZEN SET INTACT + results reproduce;
    1 = mismatch (data changed, or gate result differs from the record);
    2 = manifest/eval set missing or unreadable.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from freeze_eval_set import canonical_json_sha256, sha256_bytes  # noqa: E402
from rag_eval import EVAL_SET_PATH, evaluate, gate_verdict, load_eval_set  # noqa: E402
from rag_retrieval import Document, RetrievalIndex, index_documents  # noqa: E402

WORK_ROOT = HERE.parent
DEFAULT_MANIFEST = WORK_ROOT / "06_EVIDENCE" / "FROZEN_EVAL_SET_v2.json"

# Metrics compared for exact equality between the freeze run and this run.
COMPARED_METRICS = (
    "hit_at_5", "precision_at_5", "recall_at_5", "mrr", "answered_rate",
    "no_answer_accuracy", "easy_leaks", "near_miss_leaks", "ranked_misses",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    args = parser.parse_args()
    manifest_path = Path(args.manifest)
    if not manifest_path.is_file():
        print(f"VERIFY FAILED — freeze manifest not found: {manifest_path}")
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    fp = manifest["fingerprints"]

    # 1. Byte-exact tamper check.
    raw = EVAL_SET_PATH.read_bytes()
    file_hash = sha256_bytes(raw)
    problems: list[str] = []
    if file_hash != fp["file_sha256"]:
        problems.append(
            f"file_sha256 MISMATCH: current={file_hash} frozen={fp['file_sha256']}")
    if len(raw) != fp["file_bytes"]:
        problems.append(f"file_bytes MISMATCH: current={len(raw)} frozen={fp['file_bytes']}")

    # 2. Content (format-independent) check.
    try:
        data = load_eval_set(EVAL_SET_PATH)
    except ValueError as exc:
        print(f"VERIFY FAILED — schema validation failed: {exc}")
        return 1
    canon = canonical_json_sha256(data)
    if canon != fp["canonical_sha256"]:
        problems.append(
            f"canonical_sha256 MISMATCH: current={canon} frozen={fp['canonical_sha256']}")
    for key, cur in (
        ("corpus_canonical_sha256", canonical_json_sha256(
            sorted(d["source_id"] for d in data["documents"]))),
        ("labeled_canonical_sha256", canonical_json_sha256(data["labeled_queries"])),
        ("no_answer_canonical_sha256", canonical_json_sha256(data["no_answer_queries"])),
    ):
        if cur != fp[key]:
            problems.append(f"{key} MISMATCH: current={cur} frozen={fp[key]}")

    # 3. Reproduce the approved evaluation run.
    docs = [Document(d["source_id"], d["title"], d["text"]) for d in data["documents"]]
    index = RetrievalIndex(index_documents(docs, **data["chunking"]))
    top_k = data["retrieval"]["top_k"]
    op = data["retrieval"]["operating_min_score"]
    metrics = evaluate(index, data["labeled_queries"], data["no_answer_queries"], top_k, op)
    recorded = manifest["metrics_at_operating_threshold"]
    for key in COMPARED_METRICS:
        if metrics.get(key) != recorded.get(key):
            problems.append(f"metric {key}: current={metrics.get(key)!r} "
                            f"frozen-record={recorded.get(key)!r}")
    passed, failures = gate_verdict(metrics, manifest["fingerprints"]["baseline_gate"])
    verdict = "PASS" if passed else "FAIL"
    if verdict != manifest["gate_verdict"]:
        problems.append(f"gate_verdict: current={verdict} frozen-record={manifest['gate_verdict']}")

    print(f"EVAL_SET file_sha256:      {file_hash}")
    print(f"EVAL_SET canonical_sha256: {canon}")
    print(f"Gate verdict now:          {verdict}")
    if problems:
        print("VERIFY RESULT: ❌ FROZEN SET OR RESULTS CHANGED")
        for p in problems:
            print("  -", p)
        return 1
    print("VERIFY RESULT: ✅ FROZEN SET INTACT — hashes match, results reproduce exactly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
