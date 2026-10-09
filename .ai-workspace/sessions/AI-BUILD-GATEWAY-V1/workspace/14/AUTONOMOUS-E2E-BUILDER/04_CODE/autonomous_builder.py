from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


class BuilderError(ValueError):
    pass


def iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class WorkRequest:
    execution_id: str
    work_id: str
    requester: str
    workspace: str
    build_command: list[str]
    test_command: list[str]
    repair_command: list[str] | None = None
    max_repair_cycles: int = 1


class Evidence:
    def __init__(self, root: Path, execution_id: str):
        self.root = root / execution_id
        self.root.mkdir(parents=True, exist_ok=True)
        self.lifecycle: list[dict] = []

    def transition(self, stage: str, status: str, **data):
        self.lifecycle.append({"stage": stage, "status": status, "at": iso(), **data})

    def write(self, name: str, payload):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
        return str(target)


class AutonomousBuilder:
    ALLOWED_EXECUTABLES = {"python", "python3", "bash", "sh"}

    def __init__(self, evidence_root: Path, allowed_work_ids: set[str] | None = None, allowed_requesters: set[str] | None = None):
        self.evidence_root = Path(evidence_root)
        self.allowed_work_ids = allowed_work_ids or {"Work 14"}
        self.allowed_requesters = allowed_requesters or {"nu"}

    def build(self, request: WorkRequest) -> dict:
        ev = Evidence(self.evidence_root, request.execution_id)
        ev.write("request.json", asdict(request))
        ev.transition("DISCOVER", "PASS", work_id=request.work_id)
        try:
            self._validate(request)
        except BuilderError as exc:
            ev.transition("VALIDATE", "BLOCKED", reason=str(exc))
            return self._finish(ev, request, "BLOCKED", str(exc), None)
        ev.transition("REVIEW", "PASS", reuse=["Work 12 lifecycle/evidence semantics", "Work 13 security/process boundary"], adapt=["autonomous repair loop"])
        ev.transition("ARCHITECT", "PASS", provider="sandbox-real-process")
        ev.transition("IMPLEMENT", "PASS")
        ev.transition("START", "PASS", workspace=request.workspace)
        build = self._run(request.build_command, Path(request.workspace), ev, "runtime/build")
        ev.transition("E2E", "PASS" if build["status"] == "PASS" else "FAILED", runtime=build)
        if build["status"] != "PASS":
            return self._finish(ev, request, "FAILED", "build_failed", build)
        test = self._run(request.test_command, Path(request.workspace), ev, "runtime/test-1")
        ev.transition("VERIFY", "PASS" if test["status"] == "PASS" else "FAILED", cycle=0, runtime=test)
        cycle = 0
        while test["status"] != "PASS" and request.repair_command and cycle < request.max_repair_cycles:
            cycle += 1
            ev.transition("DETECT", "PASS", cycle=cycle, failure=test["stderr"] or test["stdout"])
            repair = self._run(request.repair_command, Path(request.workspace), ev, f"runtime/repair-{cycle}")
            ev.transition("FIX", "PASS" if repair["status"] == "PASS" else "FAILED", cycle=cycle, runtime=repair)
            if repair["status"] != "PASS":
                return self._finish(ev, request, "FAILED", "repair_failed", repair)
            test = self._run(request.test_command, Path(request.workspace), ev, f"runtime/test-{cycle + 1}")
            ev.transition("RETEST", "PASS" if test["status"] == "PASS" else "FAILED", cycle=cycle, runtime=test)
        final = "PASS" if test["status"] == "PASS" else "FAILED"
        return self._finish(ev, request, final, None if final == "PASS" else "verification_failed", {"build": build, "test": test, "repair_cycles": cycle})

    def _validate(self, request: WorkRequest):
        if not request.execution_id or request.work_id not in self.allowed_work_ids:
            raise BuilderError("work_boundary_invalid")
        if request.requester not in self.allowed_requesters:
            raise BuilderError("requester_not_authorized")
        workspace = Path(request.workspace).resolve()
        if not workspace.exists() or not workspace.is_dir():
            raise BuilderError("workspace_missing")
        for command in (request.build_command, request.test_command, request.repair_command or []):
            if not command or Path(command[0]).name not in self.ALLOWED_EXECUTABLES:
                raise BuilderError("executable_not_allowed")
            if any(token in command for token in ("&&", "||", ";", "|", ">", "<")):
                raise BuilderError("command_injection_rejected")

    def _run(self, command: list[str], workspace: Path, ev: Evidence, prefix: str) -> dict:
        started = iso()
        try:
            p = subprocess.run(command, cwd=workspace, text=True, capture_output=True, timeout=10)
            result = {"command": command, "status": "PASS" if p.returncode == 0 else "FAILED", "exit_code": p.returncode, "stdout": p.stdout[-4000:], "stderr": p.stderr[-4000:], "started": started, "ended": iso()}
        except subprocess.TimeoutExpired as exc:
            result = {"command": command, "status": "FAILED", "exit_code": None, "stdout": str(exc.stdout or ""), "stderr": "TIMEOUT", "started": started, "ended": iso()}
        ev.write(f"{prefix}.json", result)
        return result

    def _finish(self, ev: Evidence, request: WorkRequest, status: str, reason: str | None, result):
        payload = {"execution_id": request.execution_id, "work_id": request.work_id, "requester": request.requester, "status": status, "reason": reason, "result": result, "lifecycle": ev.lifecycle, "finished": iso()}
        ev.write("lifecycle.json", ev.lifecycle)
        evidence_path = ev.write("FINAL_RESULT.json", payload)
        return {"status": status, "execution_id": request.execution_id, "evidence": evidence_path, "reason": reason, "lifecycle": ev.lifecycle}
