"""Work 103 — Freeze the approved labeled evaluation set (QC tooling).

Purpose: after the labeled set is approved, produce an immutable freeze record
containing SHA-256 fingerprints of every frozen input and a canonical
content fingerprint that survives formatting-only changes.

Two kinds of hashes are recorded on purpose:
- file_sha256: byte-exact hash of the committed file. Use it to prove the
  frozen file was not modified at all (governance / tamper evidence).
- canonical_sha256: SHA-256 over the JSON document re-serialized with
  sort_keys=True, ensure_ascii=False, separators=(",", ":"). Use it to prove
  semantic equality across whitespace/key-order/formatting changes
  (evaluation reproducibility).

This tool NEVER edits the labeled set. It only reads, validates, and writes
the freeze manifest plus raw run artifacts next to it in 06_EVIDENCE/.

Usage:
    python freeze_eval_set.py [--out ../06_EVIDENCE/FROZEN_EVAL_SET_v2.json]
Exit codes:
    0 = freeze written; 1 = validation or gate failure (nothing written);
    2 = unexpected error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

VN_TZ = timezone(timedelta(hours=7))  # UTC+07:00 — hồ sơ Work dùng múi giờ Việt Nam

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from rag_eval import EVAL_SET_PATH, evaluate, gate_verdict, load_eval_set  # noqa: E402
from rag_retrieval import Document, RetrievalIndex, index_documents  # noqa: E402

WORK_ROOT = HERE.parent
DEFAULT_OUT = WORK_ROOT / "06_EVIDENCE" / "FROZEN_EVAL_SET_v2.json"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_json_sha256(data) -> str:
    """Format-independent content fingerprint of a JSON-serializable object."""
    canon = json.dumps(data, sort_keys=True, ensure_ascii=False,
                       separators=(",", ":")).encode("utf-8")
    return sha256_bytes(canon)


def git_info() -> dict:
    def _run(args: list[str]) -> str:
        try:
            proc = subprocess.run(["git", *args], cwd=str(WORK_ROOT),
                                  capture_output=True, text=True, timeout=20)
            return proc.stdout.strip() if proc.returncode == 0 else ""
        except Exception:
            return ""

    commit = _run(["rev-parse", "HEAD"])
    tree = ""
    if commit:
        tree = _run(["rev-parse", f"{commit}^{{tree}}"])
    return {
        "commit": commit or "UNAVAILABLE",
        "tree": tree or "UNAVAILABLE",
        "branch": _run(["rev-parse", "--abbrev-ref", "HEAD"]) or "UNAVAILABLE",
        "dirty_worktree_at_freeze": (_run(["status", "--porcelain"]) != ""),
    }


def build_index(data: dict):
    docs = [Document(d["source_id"], d["title"], d["text"]) for d in data["documents"]]
    chunks = index_documents(docs, **data["chunking"])
    return RetrievalIndex(chunks), len(chunks)


def rel_to_work(path: Path) -> str:
    try:
        return path.relative_to(WORK_ROOT).as_posix()
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT),
                        help="freeze manifest path (default 06_EVIDENCE/FROZEN_EVAL_SET_v2.json)")
    parser.add_argument("--force", action="store_true",
                        help="explicitly regenerate an existing freeze record; "
                             "without it, re-freezing over a valid manifest is refused")
    args = parser.parse_args()
    out_path = Path(args.out).resolve()
    artifacts_dir = out_path.parent / "frozen" / out_path.stem
    started_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    started_epoch = time.time()

    # 1. Strict schema validation (raises ValueError on any violation).
    try:
        data = load_eval_set(EVAL_SET_PATH)
    except ValueError as exc:
        print(f"FREEZE ABORTED — schema validation failed: {exc}")
        return 1

    # 2. Read current bytes (for fingerprints and the re-freeze guard below).
    raw = EVAL_SET_PATH.read_bytes()

    # 3. Refuse silent re-freeze: an approved, still-valid freeze record must
    # not be overwritten or replaced without an explicit force flag. Data that
    # changed against a valid manifest requires a new version + approval.
    if out_path.exists() and not args.force:
        try:
            existing = json.loads(out_path.read_text(encoding="utf-8"))
            existing_fp = existing.get("fingerprints", {})
        except Exception:
            existing_fp = {}
        current_file_hash = sha256_bytes(raw)
        current_canon = canonical_json_sha256(data)
        if (existing_fp.get("canonical_sha256") == current_canon
                and existing_fp.get("file_sha256") != current_file_hash):
            print("FREEZE ABORTED — data content unchanged but bytes differ from the "
                  "frozen record (formatting churn). Fix the file back to the frozen "
                  "bytes; do not re-freeze cosmetic changes.")
            return 2
        if existing_fp.get("canonical_sha256") and \
                existing_fp["canonical_sha256"] != current_canon:
            print("FREEZE ABORTED — an existing freeze record for this output path is "
                  "VALID but describes DIFFERENT content. Bump EVAL_SET version, get "
                  "approval, and write a NEW manifest (--out FROZEN_EVAL_SET_v<N>.json), "
                  "or pass --force intentionally.")
            return 2
        if existing_fp.get("canonical_sha256") == current_canon:
            print("FREEZE ABORTED — identical content already frozen at this path. "
                  "Use --force only to regenerate the record (e.g. new run metadata).")
            return 2

    # 4. Fingerprints of frozen inputs.
    corpus_ids = sorted(d["source_id"] for d in data["documents"])
    fingerprints = {
        "eval_set_path": EVAL_SET_PATH.name,
        "file_bytes": len(raw),
        "file_sha256": sha256_bytes(raw),
        "canonical_sha256": canonical_json_sha256(data),
        "version": data["version"],
        "corpus_source_ids": corpus_ids,
        "corpus_canonical_sha256": canonical_json_sha256(corpus_ids),
        "n_labeled_queries": len(data["labeled_queries"]),
        "n_no_answer_queries": len(data["no_answer_queries"]),
        "labeled_canonical_sha256": canonical_json_sha256(data["labeled_queries"]),
        "no_answer_canonical_sha256": canonical_json_sha256(data["no_answer_queries"]),
        "chunking": data["chunking"],
        "retrieval": data["retrieval"],
        "baseline_gate": data["baseline_gate"],
    }

    # 3. Run the approved evaluation procedure on the frozen set.
    index, n_chunks = build_index(data)
    top_k = data["retrieval"]["top_k"]
    op = data["retrieval"]["operating_min_score"]
    metrics = evaluate(index, data["labeled_queries"], data["no_answer_queries"], top_k, op)
    passed, failures = gate_verdict(metrics, data["baseline_gate"])
    verdict = "PASS" if passed else "FAIL"
    elapsed_ms = round((time.time() - started_epoch) * 1000.0, 1)

    # 4. Persist raw artifacts (stdout-equivalent JSON) beside the manifest.
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    art_metrics = artifacts_dir / "eval_operating_metrics.json"
    art_metrics.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")

    manifest = {
        "record_type": "WORK103_FROZEN_LABELED_EVAL_SET",
        "status": "FROZEN_IMMUTABLE" if passed else "FREEZE_BLOCKED_GATE_FAIL",
        "work": "103 ROOM-HOP-RAG-RETRIEVAL-CAPABILITY",
        "procedure_ref": "05_TEST/ACCEPTANCE_AND_E2E_PLAN.md + BIEN_BAN.md gate G3",
        "frozen_at_utc": started_utc,
        "frozen_at_vn": datetime.fromtimestamp(started_epoch, timezone.utc)
                        .astimezone(VN_TZ).isoformat(timespec="seconds"),
        "tool": "04_CODE/freeze_eval_set.py",
        "git": git_info(),
        "fingerprints": fingerprints,
        "index_summary": {"n_documents": len(data["documents"]), "n_chunks": n_chunks},
        "run_environment": {
            "python": sys.version.split()[0],
            "platform": sys.platform,
            "elapsed_ms": elapsed_ms,
        },
        "metrics_at_operating_threshold": {k: v for k, v in metrics.items()},
        "gate_verdict": verdict,
        "gate_failures": failures,
        "artifacts": {
            "eval_operating_metrics": {
                "path": rel_to_work(art_metrics),
                "file_sha256": sha256_bytes(art_metrics.read_bytes()),
            },
        },
        "policy": (
            "Any change to EVAL_SET.json requires a new version number and a new "
            "freeze record; this file must never be edited in place after freeze. "
            "Verify with: python 04_CODE/verify_frozen_eval_set.py"
        ),
    }
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(f"Freeze manifest: {out_path}")
    print(f"EVAL_SET file_sha256:      {fingerprints['file_sha256']}")
    print(f"EVAL_SET canonical_sha256: {fingerprints['canonical_sha256']}")
    print(f"Gate verdict: {verdict}" + ("" if passed else f" — failures: {failures}"))
    return 0 if passed else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # defensive: never write a partial freeze silently
        print(f"FREEZE ABORTED — unexpected error: {exc!r}")
        raise SystemExit(2)
