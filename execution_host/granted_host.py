from __future__ import annotations

import hashlib
import json
import os
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from typing import Any

from .core_authority_client import CoreAuthorityClient
from .security import redact, safe_env
from .source_snapshot import workspace_source_sha256
from .process_control import run_bounded


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

    def execute_for_work(
        self,
        work_id: str,
        grant_id: str,
        grant_token: str,
    ) -> dict[str, Any]:
        if not work_id or not grant_id or not grant_token:
            raise GrantedExecutionError("grant_and_work_required")
        try:
            binding = self.authority_client.validate_grant(
                work_id, grant_id, grant_token
            )
            if binding.get("work_id") != work_id or binding.get("grant_id") != grant_id:
                raise GrantedExecutionError("core_grant_binding_mismatch")
            return self._execute_validated(binding, grant_id, grant_token)
        except Exception as exc:
            reason = (
                exc.code if hasattr(exc, "code")
                else str(exc) if isinstance(exc, GrantedExecutionError)
                else "execution_blocked:" + type(exc).__name__
            )
            return {
                "status": "BLOCKED",
                "work_id": work_id,
                "grant_id": grant_id,
                "run_record_started": False,
                "run_record_persisted": False,
                "blocker": reason,
                **self.identity(),
            }

    def _execute_validated(
        self,
        binding: dict[str, Any],
        grant_id: str,
        grant_token: str,
    ) -> dict[str, Any]:
        required = (
            "work_id", "work_name", "repository", "branch", "expected_head", "purpose", "assignment_id", "task_id",
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
        if not _inside(canonical_workspace, root) or not _inside(workspace, canonical_workspace):
            raise GrantedExecutionError("execution_workspace_escape")
        if not _inside(evidence_root, root):
            raise GrantedExecutionError("evidence_root_escape")
        if _inside(evidence_root, workspace):
            raise GrantedExecutionError("evidence_root_inside_execution_workspace")

        actual_source_hash = workspace_source_sha256(workspace)
        if actual_source_hash != binding["source_sha256"]:
            raise GrantedExecutionError("execution_source_hash_mismatch")

        expected_head = binding["expected_head"]
        if not isinstance(expected_head, str) or len(expected_head) not in (40, 64):
            raise GrantedExecutionError("canonical_git_head_invalid")
        try:
            git_head = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=workspace,
                text=True,
                capture_output=True,
                timeout=5,
                check=True,
            ).stdout.strip().lower()
        except (OSError, subprocess.SubprocessError):
            raise GrantedExecutionError("execution_git_head_unavailable") from None
        if git_head != expected_head.lower():
            raise GrantedExecutionError("execution_git_head_mismatch")
        try:
            git_top_level = Path(subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=workspace,
                text=True,
                capture_output=True,
                timeout=5,
                check=True,
            ).stdout.strip()).resolve()
        except (OSError, subprocess.SubprocessError):
            raise GrantedExecutionError("execution_git_root_unavailable") from None
        if _inside(evidence_root, git_top_level):
            raise GrantedExecutionError("evidence_root_inside_git_repository")
        try:
            git_branch = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=workspace,
                text=True,
                capture_output=True,
                timeout=5,
                check=True,
            ).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            raise GrantedExecutionError("execution_git_branch_unavailable") from None
        if git_branch != binding["branch"]:
            raise GrantedExecutionError("execution_git_branch_mismatch")
        try:
            origin = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=workspace,
                text=True,
                capture_output=True,
                timeout=5,
                check=True,
            ).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            raise GrantedExecutionError("execution_git_origin_unavailable") from None
        if origin.startswith("git@github.com:"):
            remote_repository = origin.split(":", 1)[1].removesuffix(".git")
        else:
            parsed_origin = urlsplit(origin)
            remote_repository = parsed_origin.path.strip("/").removesuffix(".git")
            if (
                parsed_origin.scheme != "https"
                or parsed_origin.hostname != "github.com"
                or parsed_origin.username
                or parsed_origin.password
                or parsed_origin.query
                or parsed_origin.fragment
            ):
                raise GrantedExecutionError("execution_git_origin_invalid")
        if remote_repository.lower() != binding["repository"].lower():
            raise GrantedExecutionError("execution_git_origin_mismatch")
        try:
            git_status = subprocess.run(
                ["git", "status", "--porcelain", "--untracked-files=all"],
                cwd=workspace,
                text=True,
                capture_output=True,
                timeout=5,
                check=True,
            ).stdout
        except (OSError, subprocess.SubprocessError):
            raise GrantedExecutionError("execution_git_status_unavailable") from None
        if git_status.strip():
            raise GrantedExecutionError("execution_git_worktree_dirty")

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
        process_tree_termination_confirmed = True
        output_limit_exceeded = False
        run_started_persisted = False
        try:
            self.authority_client.start_run(
                binding["work_id"],
                grant_id,
                grant_token,
                {
                    "run_id": run_id,
                    "repository": binding["repository"],
                    "branch": binding["branch"],
                    "expected_head": expected_head,
                    "command": command,
                    "source_sha256": actual_source_hash,
                    "environment_id": binding["environment_id"],
                    "started_at": started_at,
                },
            )
            run_started_persisted = True
        except Exception as exc:
            blocker = "run_start_persistence_failed:" + type(exc).__name__
            status = "BLOCKED"

        if run_started_persisted:
            try:
                env = safe_env(isolated_home=run_dir / "home")
                env.update({
                    "ROOM_HOP_EXECUTION_ID": run_id,
                    "ROOM_HOP_WORK_ID": binding["work_id"],
                    "PYTHONUNBUFFERED": "1",
                })

                # Final online authorization is the last operation before spawn.
                latest = self.authority_client.validate_grant(
                    binding["work_id"], grant_id, grant_token
                )
                if latest.get("status") != "active":
                    raise GrantedExecutionError("grant_not_active_at_execution")
                if (
                    latest.get("source_sha256") != actual_source_hash
                    or latest.get("host_identity_id") != binding["host_identity_id"]
                    or latest.get("test_entrypoint") != command
                    or latest.get("repository") != binding["repository"]
                    or latest.get("branch") != binding["branch"]
                    or latest.get("expected_head") != expected_head
                ):
                    raise GrantedExecutionError("grant_binding_changed_before_execution")
                completed = run_bounded(
                    command,
                    cwd=workspace,
                    env=env,
                    timeout=timeout,
                )
                exit_code = completed.returncode
                stdout = redact(completed.stdout.decode("utf-8", "replace"))
                stderr = redact(completed.stderr.decode("utf-8", "replace"))
                process_tree_termination_confirmed = completed.tree_termination_confirmed
                output_limit_exceeded = completed.output_limit_exceeded
                if not process_tree_termination_confirmed:
                    status = "BLOCKED"
                    blocker = "execution_process_tree_termination_unconfirmed"
                elif output_limit_exceeded:
                    status = "BLOCKED"
                    blocker = "execution_output_limit_exceeded"
                elif completed.timed_out:
                    status = "TIMEOUT"
                    blocker = "execution_timeout"
                else:
                    status = "PASS" if exit_code == 0 else "FAILED"
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
        evidence_path = run_dir / "RUN_EVIDENCE.json"
        evidence_errors: list[str] = []
        stdout_sha256 = hashlib.sha256(stdout.encode("utf-8")).hexdigest()
        stderr_sha256 = hashlib.sha256(stderr.encode("utf-8")).hexdigest()

        for target, content in ((stdout_path, stdout), (stderr_path, stderr)):
            try:
                target.write_text(content, encoding="utf-8")
                if target == stdout_path:
                    stdout_sha256 = _hash_file(target)
                else:
                    stderr_sha256 = _hash_file(target)
            except Exception as exc:
                evidence_errors.append(target.name + ":" + type(exc).__name__)

        evidence_persisted = not evidence_errors
        reported_status = "BLOCKED" if evidence_errors else status
        reported_blocker = blocker
        if evidence_errors:
            reported_blocker = "run_evidence_persistence_failed"
            if blocker:
                reported_blocker += ":" + blocker

        evidence = {
            "run_id": run_id,
            "grant_id": grant_id,
            "work_id": binding["work_id"],
            "repository": binding["repository"],
            "branch": binding["branch"],
            "expected_head": expected_head,
            "assignment_id": binding["assignment_id"],
            "task_id": binding["task_id"],
            "principal_id": binding["principal_id"],
            "host_identity_id": binding["host_identity_id"],
            "command": command,
            "source_sha256": actual_source_hash,
            "environment_id": binding["environment_id"],
            "started_at": started_at,
            "finished_at": finished_at,
            "status": reported_status,
            "execution_status": status,
            "exit_code": exit_code,
            "blocker": reported_blocker,
            "process_tree_termination_confirmed": process_tree_termination_confirmed,
            "output_limit_exceeded": output_limit_exceeded,
            "stdout_sha256": stdout_sha256,
            "stderr_sha256": stderr_sha256,
            "evidence_persisted": evidence_persisted,
            "evidence_errors": list(evidence_errors),
        }
        evidence_file_verified = False
        try:
            evidence_path.write_text(
                json.dumps(evidence, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            evidence_sha256 = _hash_file(evidence_path)
            evidence_file_verified = True
        except Exception as exc:
            evidence_errors.append(evidence_path.name + ":" + type(exc).__name__)
            evidence_persisted = False
            reported_status = "BLOCKED"
            reported_blocker = "run_evidence_persistence_failed"
            if blocker:
                reported_blocker += ":" + blocker
            evidence.update({
                "status": reported_status,
                "blocker": reported_blocker,
                "evidence_persisted": False,
                "evidence_errors": list(evidence_errors),
            })
            evidence_sha256 = hashlib.sha256(
                json.dumps(
                    evidence, sort_keys=True, separators=(",", ":"),
                    ensure_ascii=False,
                ).encode("utf-8")
            ).hexdigest()
        evidence_ref = str(evidence_path) if evidence_file_verified else None
        stdout_ref = str(stdout_path) if stdout_path.is_file() else None
        stderr_ref = str(stderr_path) if stderr_path.is_file() else None

        if not run_started_persisted:
            return {
                **evidence,
                "status": "BLOCKED",
                "execution_status": status,
                "blocker": blocker or "run_start_record_not_persisted",
                "run_record_started": False,
                "run_record_persisted": False,
                "evidence_ref": evidence_ref,
                "stdout_ref": stdout_ref,
                "stderr_ref": stderr_ref,
                **self.identity(),
            }
        completion = {
            "finished_at": finished_at,
            "status": reported_status,
            "execution_status": status,
            "exit_code": exit_code,
            "evidence_sha256": evidence_sha256,
            "evidence_ref": evidence_ref,
            "evidence_persisted": evidence_persisted,
            "evidence_errors": list(evidence_errors),
            "stdout_sha256": evidence["stdout_sha256"],
            "stderr_sha256": evidence["stderr_sha256"],
        }
        try:
            persisted = self.authority_client.complete_run(
                binding["work_id"], grant_id, grant_token, run_id, completion
            )
        except Exception as exc:
            return {
                **evidence,
                "status": "BLOCKED",
                "execution_status": status,
                "blocker": "run_record_completion_failed:" + type(exc).__name__,
                "run_record_started": True,
                "run_record_persisted": False,
                "evidence_ref": evidence_ref,
                "stdout_ref": stdout_ref,
                "stderr_ref": stderr_ref,
                **self.identity(),
            }

        return {
            **evidence,
            "run_record": persisted,
            "run_record_started": True,
            "run_record_persisted": True,
            "evidence_persisted": evidence_persisted,
            "evidence_ref": evidence_ref,
            "stdout_ref": stdout_ref,
            "stderr_ref": stderr_ref,
            **self.identity(),
        }
