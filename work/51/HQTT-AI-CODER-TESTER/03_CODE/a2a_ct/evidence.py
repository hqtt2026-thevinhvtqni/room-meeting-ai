"""Evidence: hashes + append-only JSONL event log.

Rule (charter §6): no PASS without verifiable evidence. Every pipeline
step is logged with task ids, states, artifact hashes and verdicts.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def utc_now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class EvidenceLog:
    """Append-only JSONL event log. One JSON object per line."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def log(self, event: str, **fields) -> dict:
        record = {"ts": utc_now_iso(), "event": event}
        record.update(fields)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    def read_all(self) -> list[dict]:
        records = []
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records
