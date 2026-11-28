from __future__ import annotations

from typing import Any

from .models import WorkContext, EvidenceStore
from .bridge.local_host import LocalExecutionHost


class LifecycleController:
    """Canonical Work lifecycle; protected execution requires a Core grant adapter."""

    def __init__(
        self,
        context: WorkContext,
        evidence: EvidenceStore,
        host=None,
        max_repair_cycles: int = 2,
    ):
        self.ctx, self.ev = context, evidence
        self.host = host or LocalExecutionHost(context.evidence_root)
        self.max_repair_cycles = max_repair_cycles
        self.states: list[dict[str, Any]] = []

    def stage(self, name: str, status: str, **data: Any) -> None:
        item = {
            "stage": name,
            "status": status,
            "execution_id": self.ctx.execution_id,
            **data,
        }
        self.states.append(item)
        self.ev.record(name, status, **data)

    def run(self) -> dict[str, Any]:
        self.ev.write(
            "authority.json",
            {
                "work_id": self.ctx.work_id,
                "work_name": self.ctx.work_name,
                "source": "canonical authority",
            },
        )
        self.stage("RESOLVE", "PASS", work_id=self.ctx.work_id, work_name=self.ctx.work_name)
        self.ev.write("context.json", self.ctx.as_dict())
        self.stage("BIND", "PASS", context=self.ctx.as_dict())

        blockers = self._validate_binding()
        if blockers:
            self.stage("VALIDATE", "BLOCKED", blockers=blockers)
            return self._finish("BLOCKED", blockers[0]["reason"], blockers)
        self.stage("VALIDATE", "PASS")
        self.stage("PREPARE", "PASS", workspace=self.ctx.execution_workspace)

        if not self.ctx.test_entrypoint:
            blocker = {"reason": "test_entrypoint_missing"}
            self.stage("EXECUTE", "BLOCKED", blockers=[blocker])
            self.stage("TEST", "BLOCKED", blockers=[blocker])
            return self._finish("BLOCKED", blocker["reason"], [blocker])

        if not callable(getattr(self.host, "execute_authorized", None)):
            blocker = {
                "reason": "core_grant_execution_adapter_not_configured",
                "detail": "capability discovery is not execution authority",
            }
            try:
                report = self.host.discover(self.ctx)
                self.ev.write("runtime/discovery.json", report)
            except Exception as exc:
                blocker["discovery_error"] = type(exc).__name__
            self.stage("EXECUTE", "BLOCKED", blockers=[blocker])
            self.stage("TEST", "BLOCKED", blockers=[blocker])
            return self._finish("BLOCKED", blocker["reason"], [blocker])

        try:
            report = self.host.discover(self.ctx)
            self.ev.write("runtime/discovery.json", report)
            execution = self.host.execute_authorized(self.ctx)
        except Exception as exc:
            blocker = {
                "reason": "core_grant_execution_failed",
                "detail": type(exc).__name__ + ":" + str(exc),
            }
            self.ev.write("runtime/granted-execution.json", {
                "status": "BLOCKED",
                "work_id": self.ctx.work_id,
                "execution_id": self.ctx.execution_id,
                **blocker,
            })
            self.stage("EXECUTE", "BLOCKED", blockers=[blocker])
            self.stage("TEST", "BLOCKED", blockers=[blocker])
            return self._finish("BLOCKED", blocker["reason"], [blocker])

        self.ev.write("runtime/granted-execution.json", execution)
        run_record_persisted = execution.get("run_record_persisted") is True
        execution_status = execution.get("status", "BLOCKED")
        if not run_record_persisted:
            blocker = {
                "reason": "execution_run_record_not_persisted",
                "execution_status": execution_status,
                "host_blocker": execution.get("blocker"),
            }
            self.stage("EXECUTE", "BLOCKED", blockers=[blocker])
            self.stage("TEST", "BLOCKED", blockers=[blocker])
            return self._finish("BLOCKED", blocker["reason"], [blocker])

        self.stage(
            "EXECUTE",
            "PASS",
            run_id=execution.get("run_id"),
            grant_id=execution.get("grant_id"),
            run_record_persisted=True,
        )
        if execution_status == "PASS":
            self.stage("TEST", "PASS", exit_code=execution.get("exit_code"))
            return self._finish("PASS", "", [])
        if execution_status in {"FAILED", "TIMEOUT"}:
            self.stage(
                "TEST",
                "FAILED",
                execution_status=execution_status,
                exit_code=execution.get("exit_code"),
                blocker=execution.get("blocker"),
            )
            return self._finish(
                "FAILED",
                execution.get("blocker") or "test_execution_failed",
                [],
            )

        blocker = {
            "reason": execution.get("blocker") or "test_execution_blocked",
            "execution_status": execution_status,
        }
        self.stage("TEST", "BLOCKED", blockers=[blocker])
        return self._finish("BLOCKED", blocker["reason"], [blocker])

    def _validate_binding(self):
        required = {
            "repository": self.ctx.repository,
            "repository_root": self.ctx.repository_root,
            "branch": self.ctx.branch,
            "expected_head": self.ctx.expected_head,
        }
        if callable(getattr(self.host, "execute_authorized", None)):
            required.update({
                "assignment_id": self.ctx.assignment_id,
                "task_id": self.ctx.task_id,
                "environment_id": self.ctx.environment_id,
                "host_identity_id": self.ctx.host_identity_id,
            })
        return [
            {"field": key, "reason": f"authority_field_not_configured:{key}"}
            for key, value in required.items()
            if not value
        ]

    def _finish(self, status: str, reason: str, blockers: list[dict[str, Any]]) -> dict[str, Any]:
        stage_names = (
            "RESOLVE", "BIND", "VALIDATE", "PREPARE", "EXECUTE",
            "TEST", "COMMIT", "PUSH", "CI", "VERIFY",
        )
        gates = {}
        for name in stage_names:
            matches = [item["status"] for item in self.states if item["stage"] == name]
            gates[name] = matches[-1] if matches else "BLOCKED"
        payload = {
            "work_id": self.ctx.work_id,
            "execution_id": self.ctx.execution_id,
            "status": status,
            "initial_head": self.ctx.expected_head,
            "final_head": None,
            "github_head": None,
            "tests": gates["TEST"],
            "ci": gates["CI"],
            "evidence_root": str(self.ev.path),
            "failure_reason": reason,
            "gates": gates,
            "lifecycle": self.states,
            "blockers": blockers,
            "no_fake_pass": True,
        }
        self.ev.write("FINAL_RESULT.json", payload)
        return {
            "status": status,
            "work_id": self.ctx.work_id,
            "execution_id": self.ctx.execution_id,
            "evidence": str(self.ev.path),
            "blocker": reason or None,
        }
