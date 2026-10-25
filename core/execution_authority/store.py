"""Append-only durable record store for the Core execution authority (DR-3).

Proof obligations of the contract (section 5, DR-3):
* durability: every append is flushed and fsync-ed before returning;
* restart recovery: a new store instance over the same directory reloads
  every record and remains queryable by id;
* append-only: the store exposes no mutation or deletion path. History can
  only grow; corrections are new records, never edits.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class AppendOnlyRecordStore:
    """JSONL-backed append-only record store. No update, no delete."""

    def __init__(self, data_dir: str | os.PathLike[str]) -> None:
        self._dir = Path(data_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._file = self._dir / "execution_authority_records.jsonl"
        self._records: list[dict[str, Any]] = []
        self._by_id: dict[str, dict[str, Any]] = {}
        self._reload()

    def _reload(self) -> None:
        self._records = []
        self._by_id = {}
        if not self._file.exists():
            return
        with open(self._file, "r", encoding="utf-8") as handle:
            for line in handle:
                stripped = line.strip()
                if not stripped:
                    continue
                record = json.loads(stripped)
                self._records.append(record)
                self._by_id[record["record_id"]] = record

    def append(self, record: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(record, dict):
            raise ValueError("record must be a mapping")
        record_id = record.get("record_id")
        if not isinstance(record_id, str) or not record_id.strip():
            raise ValueError("record must carry a non-empty record_id")
        if record_id in self._by_id:
            raise ValueError("append-only store refuses duplicate record_id")
        line = json.dumps(record, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        with open(self._file, "a", encoding="utf-8") as handle:
            handle.write(line)
            handle.write(chr(10))
            handle.flush()
            os.fsync(handle.fileno())
        stored = dict(record)
        self._records.append(stored)
        self._by_id[record_id] = stored
        return dict(stored)

    def get(self, record_id: str) -> dict[str, Any] | None:
        return self._by_id.get(record_id)

    def records(self, record_type: str | None = None) -> list[dict[str, Any]]:
        if record_type is None:
            return [dict(r) for r in self._records]
        return [dict(r) for r in self._records if r.get("record_type") == record_type]
