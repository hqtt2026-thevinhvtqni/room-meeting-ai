from __future__ import annotations

import hashlib
import json
import os
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .core_authority_client import CoreAuthorityClient
from .security import redact, safe_env
from .source_snapshot import workspace_source_sha256


class GrantedExecutionError(RuntimeError):
    pass


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class GrantedExecutionHost:
    """Protected Execution Host path; no caller-supplied WorkContext or allow bit."""

    provider_type = "CORE_AUTHORIZED_PYTEST"

    def __init__(self, authority_client: CoreAuthorityClient | None = None):
        self.authority_client = authority_client or CoreAuthorityClient()

    def identity(self) -> dict[str, Any]:
        return {
            "provider_type": self.provider_type,
            "authority": "CORE_ONLINE",
            "grant_cache": False,
        }

    def execute_granted(self, grant_id: str, grant_token: str) -> dict[str, Any]:
        if not grant_id or not grant_token:
            raise GrantedExecutionError("grant_required")

        # This online check is deliberately performed for every execution.
        # No ALLOW result or grant token is cached by this process.
        binding = self.authority_client.validate_grant(
            self._work_id_hint(grant_id), grant_id, grant_token
        )
        return self._execute_validated(binding, grant_id, grant_token)

    def _work_id_hint(self, grant_id: str) -> str:
        # The Work ID is supplied by the request envelope, then checked against
        # the Core-returned grant binding. It is not trusted for authorization.
        work_id = getattr(self, "_request_work_id", None)
        if not work_id:
            raise GrantedExecutionError("work_id_required")
        return work_id

    def execute_for_work(
        self,
        work_id: str,
        grant_id: str,
        grant_token: str,
    ) -> dict[str, Any]:
        if not work_id or not grant_id or not grant_token:
            raise GrantedExecutionError("grant_and_work_required")
        binding = self.authority_client.validate_grant(
            work_id, grant_id, grant_token
        )
        if binding.get("work_id") != work_id or binding.get("grant_id") != grant_id:
            raise GrantedExecutionError("core_grant_binding_mismatch")
        return self._execute_validated(binding, grant_id, grant_token)

    def _execute_validated(
        self,
        binding: dict[str, Any],
        grant_id: str,
        grant_token: str,
    ) -> dict[str, Any]:
        required = (
            "work_id", "work_name", "purpose", "assignment_id", "task_id",
            "workspace_root", "execution_workspace", "evidence_root",
            "source_sha256", "environment_id", "test_entrypoint",
            "max_timeout_seconds", "host_identity_id",
        )
        if any(key not in binding for key in required):
            raise GrantedExecutionError("core_work_binding_incomplete")
        if binding["purpose"] != "pytest_run":
            raise GrantedExecutionError("execution_purpose_not_supported")

        root = Path(binding["workspace_root"]).resolve(strict=True)
        workspace = Path(binding["execution_workspace"]).resolve(strict=True)
        evidence_root = Path(binding["evidence_root"]).resolve()
        canonical_workspace = (root / "workspace").resolve()
        if not root.is_dir() or not workspace.is_dir():
            raise GrantedExecutionError("canonical_workspace_missing")
        if not _inside(workspace, canonical_workspace):
            raise GrantedExecutionError("execution_workspace_escape")
        if not _inside(evidence_root, root):
            raise GrantedExecutionError("evidence_root_escape")

        actual_source_hash = workspace_source_sha256(workspace)
        if actual_source_hash != binding["source_sha256"]:
            raise GrantedExecutionError("execution_source_hash_mismatch")

        command = binding["test_entrypoint"]
        if not isinstance(command, list) or not command:
            raise GrantedExecutionError("canonical_test_entrypoint_invalid")
        executable = Path(command[0]).stem.lower()
        is_pytest = executable in {"pytest", "pytest.exe"} or (
            executable in {"python", "python3", "python.exe", "python3.exe"}
            and len(command) >= 3
            and command[1:3] == ["-m", "pytest"]
        )
        if not is_pytest:
            raise GrantedExecutionError("canonical_command_not_pytest")

        timeout = int(binding["max_timeout_seconds"])
        if timeout < 1 or timeout > 3600:
            raise GrantedExecutionError("canonical_timeout_invalid")

        run_id = "run_" + uuid.uuid4().hex
        run_dir = evidence_root / run_id
        run_dir.mkdir(parents=True, exist_ok=False)
        started_at = _utcnow()
        status = "BLOCKED"
        exit_code = None
        stdout = ""
        stderr = ""
        blocker = None
        try:
            # Final online validation immediately before the real process effect.
            # Re-fetching also ensures a revoke between request admission and
            # process creation is observed by the Host.
            latest = self.authority_client.validate_grant(
                binding["work_id"], grant_id, grant_token
            )
            if latest.get("status") != "active":
                raise GrantedExecutionError("grant_not_active_at_execution")
            if (
                latest.get("source_sha256") != actual_source_hash
                or latest.get("host_identity_id") != binding["host_identity_id"]
                or latest.get("test_entrypoint") != command
            ):
                raise GrantedExecutionError("grant_binding_changed_before_execution")

            env = safe_env()
            env.update({
                "ROOM_HOP_EXECUTION_ID": run_id,
                "ROOM_HOP_WORK_ID": binding["work_id"],
                "PYTHONUNBUFFERED": "1",
            })
            try:
                completed = subprocess.run(
                    command,
                    cwd=workspace,
                    env=env,
                    text=True,
                    capture_output=True,
                    timeout=timeout,
                    check=False,
                )
                exit_code = completed.returncode
                stdout = redact(completed.stdout or "")
                stderr = redact(completed.stderr or "")
                status = "PASS" if exit_code == 0 else "FAILED"
            except subprocess.TimeoutExpired as exc:
                stdout = redact((exc.stdout or "").decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or ""))
                stderr = redact((exc.stderr or "").decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or ""))
                status = "TIMEOUT"
                blocker = "execution_timeout"
        except Exception as exc:
            blocker = (
                exc.code if hasattr(exc, "code")
                else str(exc) if isinstance(exc, GrantedExecutionError)
                else "execution_blocked:" + type(exc).__name__
            )
            status = "BLOCKED"

        finished_at = _utcnow()
        stdout_path = run_dir / "stdout.log"
        stderr_path = run_dir / "stderr.log"
        stdout_path.write_text(stdout, encoding="utf-8")
        stderr_path.write_text(stderr, encoding="utf-8")
        evidence = {
            "run_id": run_id,
            "grant_id": grant_id,
            "work_id": binding["work_id"],
            "assignment_id": binding["assignment_id"],
            "task_id": binding["task_id"],
            "principal_id": binding["principal_id"],
            "host_identity_id": binding["host_identity_id"],
            "command": command,
            "source_sha256": actual_source_hash,
            "environment_id": binding["environment_id"],
            "started_at": started_at,
            "finished_at": finished_at,
            "status": status,
            "exit_code": exit_code,
            "blocker": blocker,
            "stdout_sha256": _hash_file(stdout_path),
            "stderr_sha256": _hash_file(stderr_path),
        }
        evidence_path = run_dir / "RUN_EVIDENCE.json"
        evidence_path.write_text(
            json.dumps(evidence, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        evidence_sha256 = _hash_file(evidence_path)

        record = {
            "run_id": run_id,
            "command": command,
            "source_sha256": actual_source_hash,
            "environment_id": binding["environment_id"],
            "started_at": started_at,
            "finished_at": finished_at,
            "status": status,
            "exit_code": exit_code,
            "evidence_sha256": evidence_sha256,
            "evidence_ref": str(evidence_path),
            "stdout_sha256": evidence["stdout_sha256"],
            "stderr_sha256": evidence["stderr_sha256"],
        }
        try:
            persisted = self.authority_client.record_run(
                binding["work_id"], grant_id, grant_token, record
            )
        except Exception as exc:
            return {
                **evidence,
                "status": "BLOCKED",
                "execution_status": status,
                "blocker": "run_record_persistence_failed:" + type(exc).__name__,
                "run_record_persisted": False,
                "evidence_ref": str(evidence_path),
                "stdout_ref": str(stdout_path),
                "stderr_ref": str(stderr_path),
                **self.identity(),
            }

        return {
            **evidence,
            "run_record": persisted,
            "run_record_persisted": True,
            "evidence_ref": str(evidence_path),
            "stdout_ref": str(stdout_path),
            "stderr_ref": str(stderr_path),
            **self.identity(),
        }
