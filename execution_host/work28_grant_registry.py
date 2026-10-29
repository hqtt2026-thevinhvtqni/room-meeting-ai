"""WP17 — Load grants only from trusted deployment config (not client body).

Supported source: JSON file path via ROOM_HOP_GRANT_REGISTRY_PATH.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from .work28_grant import ExecutionGrant, GrantError

GRANT_REGISTRY_PATH_ENV = "ROOM_HOP_GRANT_REGISTRY_PATH"


def load_grant_registry(environ=None, path: str | Path | None = None) -> dict[str, ExecutionGrant]:
    env = os.environ if environ is None else environ
    raw_path = path if path is not None else env.get(GRANT_REGISTRY_PATH_ENV)
    if not raw_path:
        return {}
    p = Path(str(raw_path))
    if not p.is_file():
        raise GrantError("grant_registry_path_missing")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise GrantError("grant_registry_must_be_list")
    out: dict[str, ExecutionGrant] = {}
    for item in data:
        if not isinstance(item, dict):
            raise GrantError("grant_registry_entry_invalid")
        gid = item.get("grant_id")
        if not isinstance(gid, str) or not gid:
            raise GrantError("grant_registry_entry_missing_id")
        grant = ExecutionGrant(
            grant_id=gid,
            work_id=str(item["work_id"]),
            entry_path=str(item["entry_path"]),
            operation=str(item["operation"]),
            expected_source_sha256=str(item["expected_source_sha256"]),
            expires_at_unix=item.get("expires_at_unix"),
        )
        if gid in out:
            raise GrantError("grant_registry_duplicate_id")
        out[gid] = grant
    return out


__all__ = ["GRANT_REGISTRY_PATH_ENV", "load_grant_registry"]
