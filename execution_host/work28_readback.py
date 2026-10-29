"""WP19 — Authenticated evidence readback (verify seal on read).

Does not open MCP tools. Paths are constrained under a configured evidence_root.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .work28_evidence import EvidenceError, verify_evidence_seal

_EXEC_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class ReadbackError(ValueError):
    """Readback refused or path invalid."""


def load_sealed_result(
    *,
    evidence_root: Path | str,
    execution_id: str,
) -> dict[str, Any]:
    if not isinstance(execution_id, str) or not _EXEC_ID.fullmatch(execution_id):
        raise ReadbackError("execution_id_invalid")
    root = Path(evidence_root).resolve()
    result_path = (root / execution_id / "FINAL_RESULT.json").resolve()
    try:
        result_path.relative_to(root)
    except ValueError as exc:
        raise ReadbackError("evidence_path_escape") from exc
    if not result_path.is_file():
        raise ReadbackError("evidence_not_found")
    digest = verify_evidence_seal(result_path)
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise EvidenceError("evidence_payload_invalid")
    return {
        "status": "PASS",
        "execution_id": execution_id,
        "evidence_ref": str(result_path),
        "evidence_sha256": digest,
        "result": payload,
    }


__all__ = ["ReadbackError", "load_sealed_result"]
