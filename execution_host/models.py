from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any
import uuid

@dataclass(frozen=True)
class WorkContext:
    work_id: str
    work_name: str
    workspace_root: str
    execution_workspace: str
    evidence_root: str
    authorized: bool
    execution_id: str | None = None
    repository: str | None = None
    repository_root: str | None = None
    branch: str | None = None
    expected_head: str | None = None
    test_entrypoint: tuple[str, ...] | None = None
    browser_target: str | None = None
    github_target: str | None = None
    ci_target: dict[str, Any] = field(default_factory=dict)
    def as_dict(self): return asdict(self)

@dataclass
class ExecutionRequest:
    command: tuple[str, ...] | None = None
    timeout_seconds: float = 30.0
    collect_artifacts: tuple[str, ...] = ()
    run_test: bool = False
    def as_dict(self): return asdict(self)

@dataclass
class ExecutionResult:
    execution_id: str
    work_id: str
    status: str
    exit_code: int | None = None
    stdout: str = ''
    stderr: str = ''
    artifacts: list[str] = field(default_factory=list)
    evidence_ref: str | None = None
    blocker: str | None = None
    cleanup: dict[str, Any] = field(default_factory=dict)
    runtime_instance_id: str | None = None
    runtime_build_hash: str | None = None
    runtime_started_at: str | None = None
    runtime_pid: int | None = None
    runtime_platform: str | None = None
    runtime_bind_address: str | None = None
    def as_dict(self): return asdict(self)

def new_execution_id() -> str: return uuid.uuid4().hex
