"""Evidence system (issue #34, part D).

An evidence bundle answers one question: *what actually happened?* Each
record is append-only, content-addressed by SHA-256, and tied to a code
version so a report can be checked against the real repository state.

Required kinds for a job to be eligible for ``SUCCEEDED``:

    diff | log | preview | e2e | runtime_status

The store never fabricates entries; ``is_complete()`` only reports what was
actually recorded. This module is the technical enforcement of the room
rule "Không được báo thành công nếu chưa có bằng chứng chạy thật."
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .errors import ValidationError

REQUIRED_KINDS = ("diff", "log", "preview", "e2e", "runtime_status")
ALLOWED_KINDS = REQUIRED_KINDS + ("note",)


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class EvidenceRecord:
    id: str
    job_id: str
    kind: str
    summary: str
    sha256: str
    code_version: str
    created_at: str
    payload: dict = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compute_code_version(root: Path) -> str:
    """Return a deterministic version string for the current tree.

    Prefers ``git rev-parse HEAD`` when available (authoritative), falls
    back to a hash over tracked source files so environments without git
    still produce a stable, verifiable fingerprint.
    """
    try:
        import subprocess

        out = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if out.returncode == 0 and out.stdout.strip():
            return f"git:{out.stdout.strip()}"
    except (OSError, ValueError):
        pass

    digest = hashlib.sha256()
    files = sorted(
        p for p in root.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and p.suffix in {".py", ".ts", ".js", ".json", ".html", ".css"}
    )
    for path in files:
        digest.update(str(path.relative_to(root)).encode("utf-8"))
        digest.update(path.read_bytes())
    return f"tree:{digest.hexdigest()[:16]}"


class EvidenceStore:
    """Append-only evidence records, mirrored to JSONL on disk."""

    def __init__(self, root: Optional[Path] = None) -> None:
        self._records: dict[str, list[EvidenceRecord]] = {}
        self._lock = threading.RLock()
        self._root = Path(root) if root else None
        if self._root:
            self._root.mkdir(parents=True, exist_ok=True)

    # -- write --------------------------------------------------------------

    def add(
        self,
        job_id: str,
        kind: str,
        *,
        summary: str,
        code_version: str,
        payload: Optional[dict] = None,
    ) -> EvidenceRecord:
        if kind not in ALLOWED_KINDS:
            raise ValidationError(
                f"unknown evidence kind {kind!r}",
                details={"allowed": list(ALLOWED_KINDS)},
            )
        if not isinstance(summary, str) or not summary.strip():
            raise ValidationError("evidence requires a non-empty summary")
        if not isinstance(code_version, str) or not code_version.strip():
            raise ValidationError("evidence requires the code_version it was produced on")

        blob = json.dumps({"kind": kind, "summary": summary, "payload": payload or {}},
                          sort_keys=True, ensure_ascii=False)
        record = EvidenceRecord(
            id=f"EVD-{uuid.uuid4().hex[:10]}",
            job_id=job_id,
            kind=kind,
            summary=summary.strip(),
            sha256=hashlib.sha256(blob.encode("utf-8")).hexdigest(),
            code_version=code_version.strip(),
            created_at=_utcnow(),
            payload=payload or {},
        )
        with self._lock:
            self._records.setdefault(job_id, []).append(record)
            if self._root:
                path = self._root / f"{job_id}.jsonl"
                with path.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
        return record

    # -- read ---------------------------------------------------------------

    def list(self, job_id: str) -> list[EvidenceRecord]:
        with self._lock:
            return list(self._records.get(job_id, []))

    def kinds_present(self, job_id: str) -> set[str]:
        return {r.kind for r in self.list(job_id)}

    def missing_kinds(self, job_id: str) -> list[str]:
        present = self.kinds_present(job_id)
        return [k for k in REQUIRED_KINDS if k not in present]

    def is_complete(self, job_id: str) -> bool:
        """True only when every required kind has a real recorded artifact."""
        return not self.missing_kinds(job_id)

    def manifest(self, job_id: str) -> dict[str, Any]:
        records = self.list(job_id)
        return {
            "job_id": job_id,
            "complete": self.is_complete(job_id),
            "missing": self.missing_kinds(job_id),
            "count": len(records),
            "records": [
                {
                    "id": r.id,
                    "kind": r.kind,
                    "sha256": r.sha256,
                    "code_version": r.code_version,
                    "created_at": r.created_at,
                    "file": os.path.join(str(self._root), f"{job_id}.jsonl")
                    if self._root
                    else None,
                }
                for r in records
            ],
        }
