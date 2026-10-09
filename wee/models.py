from __future__ import annotations
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json, uuid
from .authority import WorkBinding

LIFECYCLE = ('RESOLVE','BIND','VALIDATE','PREPARE','EXECUTE','TEST','REPAIR','RETEST','COMMIT','PUSH','CI','VERIFY')
TERMINAL = ('PASS','BLOCKED','FAILED')

@dataclass(frozen=True)
class WorkContext:
    work_id: str
    work_name: str
    repository: str | None
    repository_root: str | None
    branch: str | None
    execution_workspace: str
    expected_head: str | None
    runtime: dict[str, Any]
    browser: dict[str, Any]
    test_entrypoint: list[str] | None
    ci_target: dict[str, Any]
    evidence_root: str
    execution_id: str
    @classmethod
    def from_binding(cls, binding: WorkBinding, execution_id: str | None = None) -> 'WorkContext':
        return cls(**binding.as_dict(), execution_id=execution_id or uuid.uuid4().hex)
    def as_dict(self) -> dict[str, Any]: return asdict(self)

@dataclass
class EvidenceStore:
    root: Path
    execution_id: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
    def __post_init__(self):
        self.path = self.root / self.execution_id
        for child in ('runtime','tests','browser','git','github','ci'):
            (self.path / child).mkdir(parents=True, exist_ok=True)
    def write(self, name: str, payload: dict[str, Any]) -> None:
        payload = {'execution_id': self.execution_id, **payload}
        target = self.path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str)+'\n', encoding='utf-8')
    def record(self, stage: str, status: str, **data: Any) -> None:
        self.write(f'lifecycle.json' if stage == 'LIFECYCLE' else f'{stage.lower()}/{stage.upper()}.json', {'stage': stage, 'status': status, 'timestamp': datetime.now(timezone.utc).isoformat(), **data})
