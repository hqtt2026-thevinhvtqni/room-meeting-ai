from __future__ import annotations
import hashlib, os, platform, time, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def canonical_build_hash(source_root: Path | None = None) -> str:
    """Hash the canonical Python source tree deterministically; no time/random inputs."""
    root = (source_root or Path(__file__).resolve().parent).resolve()
    digest = hashlib.sha256()
    files = sorted(p for p in root.rglob('*.py') if '__pycache__' not in p.parts)
    for path in files:
        relative = path.relative_to(root).as_posix().encode('utf-8')
        digest.update(len(relative).to_bytes(8, 'big')); digest.update(relative)
        content = path.read_bytes()
        digest.update(len(content).to_bytes(8, 'big')); digest.update(content)
    return digest.hexdigest()

class RuntimeIdentity:
    """One immutable identity created once when the W13 process starts."""
    def __init__(self, *, bind_address: str = '127.0.0.1:8031', source_root: Path | None = None):
        self.instance_id = 'w13-' + uuid.uuid4().hex
        self.build_hash = canonical_build_hash(source_root)
        self.started_at = datetime.now(timezone.utc).isoformat()
        self.pid = os.getpid()
        self.platform = platform.platform()
        self.bind_address = bind_address
    def as_dict(self) -> dict[str, Any]:
        return {'instance_id': self.instance_id, 'build_hash': self.build_hash, 'started_at': self.started_at, 'pid': self.pid, 'platform': self.platform, 'bind_address': self.bind_address}
