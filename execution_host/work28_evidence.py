"""WP18 — Sealed execution evidence for Work 28 snapshot runs.

Writes FINAL_RESULT.json under evidence_root/<execution_id>/ and a SHA-256
sidecar so readback can detect silent mutation. Does not claim OS isolation.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class EvidenceError(ValueError):
    """Evidence write or seal verification failed."""


def seal_evidence(
    *,
    evidence_root: Path | str,
    execution_id: str,
    payload: dict[str, Any],
) -> dict[str, str]:
    if not execution_id or not isinstance(execution_id, str):
        raise EvidenceError("execution_id_required")
    root = Path(evidence_root).resolve()
    dest_dir = root / execution_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    body = json.dumps(payload, indent=2, ensure_ascii=False, default=str, sort_keys=True) + "\n"
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    result_path = dest_dir / "FINAL_RESULT.json"
    seal_path = dest_dir / "FINAL_RESULT.sha256"
    result_path.write_text(body, encoding="utf-8")
    seal_path.write_text(digest + "\n", encoding="utf-8")
    return {
        "evidence_ref": str(result_path),
        "evidence_seal": str(seal_path),
        "evidence_sha256": digest,
    }


def verify_evidence_seal(evidence_ref: str | Path) -> str:
    path = Path(evidence_ref)
    if not path.is_file():
        raise EvidenceError("evidence_missing")
    seal = path.with_name("FINAL_RESULT.sha256")
    if not seal.is_file():
        raise EvidenceError("evidence_seal_missing")
    live = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = seal.read_text(encoding="utf-8").strip()
    if live != expected:
        raise EvidenceError("evidence_tampered")
    return live


__all__ = ["EvidenceError", "seal_evidence", "verify_evidence_seal"]
