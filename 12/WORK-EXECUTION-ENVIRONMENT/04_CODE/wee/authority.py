from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import json

REQUIRED = ('work_id','work_name','repository','repository_root','branch','execution_workspace','expected_head','runtime','browser','test_entrypoint','ci_target','evidence_root')

@dataclass(frozen=True)
class WorkBinding:
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
    def as_dict(self) -> dict[str, Any]: return asdict(self)

class CanonicalWorkAuthority:
    """The only resolver allowed to create a WorkContext.

    It reads a Work instance from the Work Sandbox; it never discovers or guesses
    a repository, branch, workspace, or HEAD from the ambient process.
    """
    def __init__(self, source: str | Path): self.source = Path(source)
    def resolve(self, work_id: str | None = None) -> WorkBinding:
        raw = json.loads(self.source.read_text(encoding='utf-8'))
        missing = [key for key in REQUIRED if key not in raw]
        if missing: raise ValueError('authority missing fields: ' + ', '.join(missing))
        if work_id is not None and str(raw['work_id']) != str(work_id):
            raise ValueError(f'authority work mismatch: expected {work_id}, got {raw["work_id"]}')
        if not raw.get('work_id') or not raw.get('work_name') or not raw.get('execution_workspace') or not raw.get('evidence_root'):
            raise ValueError('authority identity/scope fields must be non-empty')
        return WorkBinding(**{key: raw[key] for key in REQUIRED})
