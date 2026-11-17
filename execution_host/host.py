from __future__ import annotations

import json
import shutil
import subprocess
import threading
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import (
    WorkContext,
    ExecutionRequest,
    ExecutionResult,
    new_execution_id,
)
from .security import (
    HostError,
    redact,
    validate_context,
    validate_command,
    validate_cwd,
    safe_env,
    executable_capabilities,
)
from .adapters import unavailable
from .git_adapter import GitAdapter
from .identity import RuntimeIdentity
from .process_job import JobObjectUnavailable, ManagedProcess, spawn_managed_service


class ExecutionHost:
    provider_type = "SANDBOX_REAL_PROCESS"

    def __init__(
        self,
        *,
        browser=None,
        github=None,
        ci=None,
        runtime_identity: RuntimeIdentity | None = None,
    ):
        self.browser = browser
        self.github = github
        self.ci = ci
        self.runtime_identity = runtime_identity or RuntimeIdentity()
        self.processes: dict[str, ManagedProcess] = {}
        # Serialize registry transitions so same-name starts/stops cannot orphan a process.
        self._processes_lock = threading.RLock()
        self._service_cleanup_blocked: set[str] = set()

    def identity(self) -> dict[str, Any]:
        return self.runtime_identity.as_dict()

    def _evidence(
        self,
        evidence_root: Path,
        execution_id: str,
        payload: dict[str, Any],
    ) -> str:
        target = (
            evidence_root
            / execution_id
            / "FINAL_RESULT.json"
        )

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        target.write_text(
            json.dumps(
                payload,
                indent=2,
                ensure_ascii=False,
                default=str,
            )
            + "\n",
            encoding="utf-8",
        )

        return str(target)

    def discover(
        self,
        ctx: WorkContext,
    ) -> dict[str, Any]:
        validate_context(ctx)

        return {
            "status": "PASS",
            "provider": self.provider_type,
            "execution_id": ctx.execution_id,
            "work_id": ctx.work_id,
            "capabilities": executable_capabilities(),
            "browser": (
                "AVAILABLE"
                if self.browser
                else "NOT_CONFIGURED"
            ),
            "github": (
                "AVAILABLE"
                if self.github
                else "NOT_CONFIGURED"
            ),
            "ci": (
                "AVAILABLE"
                if self.ci
                else "NOT_CONFIGURED"
            ),
            **self.identity(),
        }

    def _artifact(
        self,
        source: str,
        workspace: Path,
        evidence: Path,
        execution_id: str,
    ) -> str:
        src = Path(source)

        if not src.is_absolute():
            src = workspace / src

        src = src.resolve()

        validate_cwd(src.parent, workspace)

        if not src.exists() or not src.is_file():
            return ""

        dest = (
            evidence
            / execution_id
            / "artifacts"
            / src.name
        ).resolve()

        dest.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(src, dest)

        return str(dest)

    @staticmethod
    def _cleanup_process(
        process: subprocess.Popen,
        *,
        terminate_first: bool = False,
    ) -> tuple[str, str]:
        """Windows-safe process cleanup for long-lived services."""

        if process.poll() is None:
            try:
                if terminate_first:
                    process.terminate()
                else:
                    process.kill()

                process.wait(timeout=5)

            except (subprocess.TimeoutExpired, OSError):
                try:
                    process.kill()
                except OSError:
                    pass

                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass

        try:
            out, err = process.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except OSError:
                pass

            out, err = process.communicate()

        return out or "", err or ""

    def execute_command(
        self,
        ctx: WorkContext,
        command: list[str],
        timeout_seconds: float = 30.0,
    ) -> dict[str, Any]:
        # Delegate to host_run: spawn_managed at creation; isolation NOT_VERIFIED.
        from .host_run import run_execute_command
        return run_execute_command(self, ctx, command, timeout_seconds)

    def execute_work(
        self,
        ctx: WorkContext,
        request: ExecutionRequest,
    ) -> ExecutionResult:

        execution_id = (
            ctx.execution_id
            or new_execution_id()
        )

        execution_ctx = replace(
            ctx,
            execution_id=execution_id,
        )

        result = self.execute_command(
            execution_ctx,
            list(request.command or ()),
            request.timeout_seconds,
        )

        if request.run_test:
            if not execution_ctx.test_entrypoint:
                result["test"] = {
                    "status": "BLOCKED",
                    "reason": "test_entrypoint_not_bound",
                }
            else:
                result["test"] = (
                    self.execute_command(
                        execution_ctx,
                        list(
                            execution_ctx.test_entrypoint
                        ),
                        request.timeout_seconds,
                    )
                )

        _, workspace, evidence = validate_context(
            execution_ctx
        )

        result["artifacts"] = [
            artifact
            for artifact in (
                self._artifact(
                    source,
                    workspace,
                    evidence,
                    execution_id,
                )
                for source in request.collect_artifacts
            )
            if artifact
        ]

        result["evidence_ref"] = self._evidence(
            evidence,
            execution_id,
            result,
        )

        return ExecutionResult(
            execution_id=execution_id,
            work_id=ctx.work_id,
            status=result["status"],
            exit_code=result["exit_code"],
            stdout=result.get(
                "stdout_summary",
                "",
            ),
            stderr=result.get(
                "stderr_summary",
                "",
            ),
            artifacts=result["artifacts"],
            evidence_ref=result["evidence_ref"],
            blocker=result.get("blocker"),
            cleanup=result["cleanup"],
            runtime_instance_id=(
                self.runtime_identity.instance_id
            ),
            runtime_build_hash=(
                self.runtime_identity.build_hash
            ),
            runtime_started_at=(
                self.runtime_identity.started_at
            ),
            runtime_pid=self.runtime_identity.pid,
            runtime_platform=self.runtime_identity.platform,
            runtime_bind_address=(
                self.runtime_identity.bind_address
            ),
        )

    def _cleanup_service_entry(self, managed: Any) -> tuple[bool, dict[str, Any], int | None]:
        """Clean a registry entry without discarding its handle on uncertainty."""
        if isinstance(managed, ManagedProcess):
            result = managed.cleanup(terminate_first=True, wait_timeout=5.0)
            return result.process_reaped, result.as_dict(), managed.process.returncode

        process = managed
        if process.poll() is None:
            self._cleanup_process(process, terminate_first=True)
        reaped = process.poll() is not None
        return reaped, {
            "process_reaped": reaped,
            "job_object": "NOT_ATTACHED",
            "notes": ["legacy_unmanaged_process_cleanup"],
        }, process.returncode

    def start_service(
        self,
        name: str,
        command: list[str],
        ctx: WorkContext,
    ) -> dict[str, Any]:

        _, workspace, _ = validate_context(ctx)
        args = validate_command(command)

        env = safe_env()
        env.update(
            {
                "ROOM_HOP_EXECUTION_ID": ctx.execution_id,
                "ROOM_HOP_WORK_ID": ctx.work_id,
            }
        )

        # Hold the registry lock across inspect -> stale cleanup -> spawn -> register.
        # This deliberately serializes service starts/stops to prevent same-name races.
        with self._processes_lock:
            existing = self.processes.get(name)
            if existing and existing.poll() is None and name not in self._service_cleanup_blocked:
                return {
                    **self.identity(),
                    "status": "PASS",
                    "name": name,
                    "pid": existing.pid,
                    "already_running": True,
                    "execution_id": ctx.execution_id,
                    "job_object": getattr(existing, "job_object", "NOT_ATTACHED"),
                }

            if existing is not None:
                try:
                    reaped, cleanup, returncode = self._cleanup_service_entry(existing)
                except Exception as exc:
                    reaped = False
                    cleanup = {
                        "process_reaped": False,
                        "notes": [f"cleanup_exception:{type(exc).__name__}"],
                    }
                    returncode = getattr(getattr(existing, "process", existing), "returncode", None)
                if not reaped:
                    self._service_cleanup_blocked.add(name)
                    return {
                        **self.identity(),
                        "status": "BLOCKED",
                        "name": name,
                        "blocker": "existing_service_cleanup_unverified",
                        "cleanup": cleanup,
                        "returncode": returncode,
                        "pid": getattr(existing, "pid", None),
                        "execution_id": ctx.execution_id,
                    }
                # Only release the old handle after the entire process tree is reaped.
                if self.processes.get(name) is existing:
                    self.processes.pop(name, None)
                self._service_cleanup_blocked.discard(name)

            # Job Object (Windows) / session leader (POSIX) is established at spawn.
            # Containment failure is returned as structured BLOCKED; no registry entry.
            try:
                managed = spawn_managed_service(args, cwd=workspace, env=env)
            except JobObjectUnavailable as exc:
                return {
                    **self.identity(),
                    "status": "BLOCKED",
                    "name": name,
                    "blocker": getattr(exc, "blocker", "job_object_attach_failed"),
                    "notes": list(getattr(exc, "notes", ())),
                    "process_reaped": bool(getattr(exc, "process_reaped", False)),
                    "pid": None,
                    "execution_id": ctx.execution_id,
                    "job_object": "NOT_ATTACHED",
                }
            except OSError as exc:
                # Preserve generic spawn failures as structured BLOCKED results.
                # Unknown reap state remains None; never manufacture a cleanup PASS.
                process_reaped = getattr(exc, "process_reaped", None)
                return {
                    **self.identity(),
                    "status": "BLOCKED",
                    "name": name,
                    "blocker": "service_spawn_failed",
                    "spawn_error_type": type(exc).__name__,
                    "notes": list(getattr(exc, "notes", ())),
                    "process_reaped": process_reaped if isinstance(process_reaped, bool) else None,
                    "pid": None,
                    "execution_id": ctx.execution_id,
                    "job_object": "NOT_ATTACHED",
                }
            self.processes[name] = managed

            return {
                **self.identity(),
                "status": "PASS",
                "name": name,
                "pid": managed.pid,
                "execution_id": ctx.execution_id,
                "job_object": managed.job_object,
            }

    def service_status(
        self,
        name: str,
        ctx: WorkContext,
    ) -> dict[str, Any]:

        with self._processes_lock:
            process = self.processes.get(name)
            if process is None:
                status = "STOPPED"
                pid = None
                returncode = None
                members = 0
            else:
                pid = process.pid
                returncode = process.poll()
                if name in self._service_cleanup_blocked:
                    status = "BLOCKED"
                    try:
                        members = process.members_count() if isinstance(process, ManagedProcess) else None
                    except Exception:
                        members = None
                elif returncode is None:
                    status = "PASS"
                    members = process.members_count() if isinstance(process, ManagedProcess) else None
                elif isinstance(process, ManagedProcess):
                    try:
                        members = process.members_count()
                    except Exception:
                        members = None
                    # A dead leader is not STOPPED while descendants remain or
                    # membership cannot be proven empty.
                    status = "STOPPED" if members == 0 else "BLOCKED"
                else:
                    members = 0
                    status = "STOPPED"

            return {
                **self.identity(),
                "status": status,
                "name": name,
                "pid": pid,
                "returncode": returncode,
                "members": members,
                "readiness": "NOT_CHECKED",
                "execution_id": ctx.execution_id,
            }

    def stop_service(
        self,
        name: str,
        ctx: WorkContext,
    ) -> dict[str, Any]:

        with self._processes_lock:
            managed = self.processes.get(name)
            if managed is None:
                return {
                    **self.identity(),
                    "status": "STOPPED",
                    "name": name,
                    "execution_id": ctx.execution_id,
                }

            try:
                reaped, cleanup, returncode = self._cleanup_service_entry(managed)
            except Exception as exc:
                reaped = False
                cleanup = {
                    "process_reaped": False,
                    "notes": [f"cleanup_exception:{type(exc).__name__}"],
                }
                returncode = getattr(getattr(managed, "process", managed), "returncode", None)

            if reaped:
                self._service_cleanup_blocked.discard(name)
                if self.processes.get(name) is managed:
                    self.processes.pop(name, None)
            else:
                self._service_cleanup_blocked.add(name)

            return {
                **self.identity(),
                "status": "PASS" if reaped else "BLOCKED",
                "blocker": None if reaped else "service_cleanup_unverified",
                "name": name,
                "returncode": returncode,
                "execution_id": ctx.execution_id,
                "process_reaped": reaped,
                "cleanup": cleanup,
            }

    def git_validate(self, ctx):
        return GitAdapter(ctx).validate()

    def git_status(self, ctx):
        return GitAdapter(ctx).status()

    def git_push(self, ctx, authorized=False):
        return GitAdapter(ctx).push(authorized)

    def browser_execute(
        self,
        ctx,
        action,
        timeout_seconds=30,
    ):
        return (
            self.browser.execute(
                ctx.execution_id,
                ctx,
                action,
                timeout_seconds,
            )
            if self.browser
            else unavailable(
                "browser",
                ctx.execution_id,
            )
        )

    def verify_head(
        self,
        ctx,
        expected_head,
    ):
        return (
            self.github.verify_head(
                ctx.execution_id,
                ctx,
                expected_head,
            )
            if self.github
            else unavailable(
                "github",
                ctx.execution_id,
            )
        )

    def verify_ci(
        self,
        ctx,
        commit_sha,
    ):
        return (
            self.ci.verify(
                ctx.execution_id,
                ctx,
                commit_sha,
            )
            if self.ci
            else unavailable(
                "ci",
                ctx.execution_id,
            )
        )
