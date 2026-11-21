"""Explicit, allowlisted PC host capabilities for Work 10.

This module deliberately does not add action types to the LOCKED browser
Action Contract. Host operations use a separate versioned API contract and
always execute inside the ProcessSupervisor worker containment.
"""
from __future__ import annotations

import base64
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class HostOperationBlocked(PermissionError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _path_list(env_name: str, fallback: list[Path]) -> list[Path]:
    raw = os.getenv(env_name, "")
    values = [part.strip().strip('"') for part in raw.split(os.pathsep) if part.strip()]
    roots = [Path(value).expanduser().resolve() for value in values]
    return roots or [p.resolve() for p in fallback]


class HostOperations:
    """Run a narrow set of host operations under explicit filesystem roots."""

    ALLOWED_OPERATIONS = {
        "list_directory", "read_file", "write_file", "run_pytest",
        "run_powershell_script",
    }

    def __init__(self, policy):
        self.policy = policy
        self.work_root = Path(
            policy.work_root or Path(__file__).resolve().parents[1]
        ).expanduser().resolve()
        self.allowed_roots = _path_list(
            "COMPUTER_AGENT_HOST_ALLOWED_ROOTS", [self.work_root]
        )
        self.writable_roots = _path_list(
            "COMPUTER_AGENT_HOST_WRITABLE_ROOTS", []
        ) if os.getenv("COMPUTER_AGENT_HOST_WRITABLE_ROOTS") else []
        self.powershell_roots = _path_list(
            "COMPUTER_AGENT_HOST_POWERSHELL_ROOTS", []
        ) if os.getenv("COMPUTER_AGENT_HOST_POWERSHELL_ROOTS") else []
        self.max_file_bytes = min(
            max(int(os.getenv("COMPUTER_AGENT_HOST_MAX_FILE_BYTES", "5242880")), 1),
            20 * 1024 * 1024,
        )
        self.max_output_bytes = min(
            max(int(os.getenv("COMPUTER_AGENT_HOST_MAX_OUTPUT_BYTES", "1048576")), 1024),
            4 * 1024 * 1024,
        )
        self.max_list_entries = min(
            max(int(os.getenv("COMPUTER_AGENT_HOST_MAX_LIST_ENTRIES", "1000")), 1),
            5000,
        )
        self.command_timeout = min(
            max(float(os.getenv("COMPUTER_AGENT_HOST_COMMAND_TIMEOUT_SECONDS", "120")), 1.0),
            300.0,
        )

    @staticmethod
    def _inside(path: Path, roots: list[Path]) -> bool:
        for root in roots:
            try:
                path.relative_to(root)
                return True
            except ValueError:
                continue
        return False

    def _resolve(self, raw_path: str, roots: list[Path], *, must_exist: bool) -> Path:
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise HostOperationBlocked("path must be a non-empty string")
        candidate_raw = Path(raw_path).expanduser()
        candidates = [candidate_raw] if candidate_raw.is_absolute() else [
            root / candidate_raw for root in roots
        ]
        for candidate in candidates:
            try:
                resolved = candidate.resolve(strict=must_exist)
            except (OSError, RuntimeError):
                continue
            if self._inside(resolved, roots):
                return resolved
        raise HostOperationBlocked("path is outside the configured allowlisted roots")

    @staticmethod
    def _base(status: str, operation: str, started_at: str, result=None, error=None) -> dict:
        finished = _utc_now()
        terminal = status if status in {"PASS", "FAIL", "BLOCKED"} else "BLOCKED"
        evidence_result = {
            key: value for key, value in (result or {}).items()
            if key not in {"content", "stdout", "stderr"}
        }
        return {
            "status": terminal,
            "operation": operation,
            "result": result or {},
            "steps": [],
            "evidence": [{
                "action": "host_operation",
                "operation": operation,
                "status": terminal.lower(),
                "ok": terminal == "PASS",
                "result": evidence_result,
                "error": error,
                "timestamp": finished,
            }],
            "error": error,
            "state_trace": ["PLANNED", "RUNNING", "VERIFYING", terminal],
            "work_id": "10",
            "started_at": started_at,
            "finished_at": finished,
        }

    def execute(self, operation: str, arguments: dict[str, Any] | None) -> dict:
        started = _utc_now()
        args = arguments or {}
        if operation not in self.ALLOWED_OPERATIONS:
            return self._base("BLOCKED", str(operation), started, error="operation_not_allowed")
        if not isinstance(args, dict):
            return self._base("BLOCKED", operation, started, error="arguments_must_be_object")
        try:
            if operation == "list_directory":
                result = self._list_directory(args)
            elif operation == "read_file":
                result = self._read_file(args)
            elif operation == "write_file":
                result = self._write_file(args)
            elif operation == "run_pytest":
                result = self._run_pytest(args)
            else:
                result = self._run_powershell(args)
            status = result.pop("_status", "PASS")
            cleanup_pending = bool(result.pop("_cleanup_pending", False))
            payload = self._base(status, operation, started, result=result,
                                 error=result.get("error"))
            payload["cleanup_pending"] = cleanup_pending
            return payload
        except HostOperationBlocked as exc:
            return self._base("BLOCKED", operation, started, error=str(exc))
        except FileNotFoundError as exc:
            return self._base("FAIL", operation, started, error=f"not_found: {exc}")
        except Exception as exc:
            return self._base("FAIL", operation, started,
                              error=f"{type(exc).__name__}: {exc}")

    def _list_directory(self, args: dict) -> dict:
        path = self._resolve(args.get("path", "."), self.allowed_roots, must_exist=True)
        if not path.is_dir():
            raise FileNotFoundError(str(path))
        entries = []
        for item in sorted(path.iterdir(), key=lambda p: p.name.casefold()):
            if len(entries) >= self.max_list_entries:
                break
            try:
                st = item.stat(follow_symlinks=False)
                entries.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size_bytes": st.st_size,
                    "is_symlink": item.is_symlink(),
                })
            except OSError as exc:
                entries.append({"name": item.name, "type": "unavailable", "error": str(exc)})
        return {
            "path": str(path),
            "entries": entries,
            "truncated": len(entries) >= self.max_list_entries,
            "entry_count": len(entries),
        }

    def _read_file(self, args: dict) -> dict:
        path = self._resolve(args.get("path"), self.allowed_roots, must_exist=True)
        if not path.is_file():
            raise FileNotFoundError(str(path))
        size = path.stat().st_size
        if size > self.max_file_bytes:
            raise HostOperationBlocked(
                f"file exceeds configured read limit ({self.max_file_bytes} bytes)"
            )
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        encoding = args.get("encoding", "utf-8")
        if encoding == "base64":
            content = base64.b64encode(raw).decode("ascii")
        elif encoding == "utf-8":
            try:
                content = raw.decode("utf-8")
            except UnicodeDecodeError:
                raise HostOperationBlocked("file is not valid UTF-8; request encoding=base64") from None
        else:
            raise HostOperationBlocked("encoding must be utf-8 or base64")
        return {"path": str(path), "bytes": len(raw), "sha256": digest,
                "encoding": encoding, "content": content}

    def _write_file(self, args: dict) -> dict:
        if not self.writable_roots:
            raise HostOperationBlocked("write_file disabled: COMPUTER_AGENT_HOST_WRITABLE_ROOTS is not configured")
        path = self._resolve(args.get("path"), self.writable_roots, must_exist=False)
        encoding = args.get("encoding", "utf-8")
        content = args.get("content")
        if not isinstance(content, str):
            raise HostOperationBlocked("write_file content must be a string")
        if encoding == "base64":
            try:
                raw = base64.b64decode(content, validate=True)
            except Exception:
                raise HostOperationBlocked("content is not valid base64") from None
        elif encoding == "utf-8":
            raw = content.encode("utf-8")
        else:
            raise HostOperationBlocked("encoding must be utf-8 or base64")
        if len(raw) > self.max_file_bytes:
            raise HostOperationBlocked("write content exceeds configured size limit")
        path.parent.mkdir(parents=True, exist_ok=True)
        overwrite = args.get("overwrite") is True
        existed = path.exists()
        if existed and path.is_dir():
            raise HostOperationBlocked("write target must be a file, not a directory")
        if existed and not overwrite:
            raise HostOperationBlocked("target already exists; set overwrite=true explicitly")
        if overwrite:
            tmp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
            try:
                with open(tmp, "xb") as handle:
                    handle.write(raw)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(tmp, path)
            finally:
                try:
                    tmp.unlink(missing_ok=True)
                except OSError:
                    pass
        else:
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            fd = os.open(path, flags, 0o600)
            with os.fdopen(fd, "wb") as handle:
                handle.write(raw)
                handle.flush()
                os.fsync(handle.fileno())
        # Read-back verifies the exact bytes written before PASS.
        actual = path.read_bytes()
        digest = hashlib.sha256(actual).hexdigest()
        if actual != raw:
            raise HostOperationBlocked("write read-back mismatch")
        return {"path": str(path), "bytes": len(actual), "sha256": digest,
                "created": not existed, "overwritten": existed, "readback_verified": True}

    def _run_process(self, command: list[str], cwd: Path, operation: str,
                     env_overrides: dict[str, str] | None = None) -> dict:
        started = time.monotonic()
        try:
            child_env = dict(os.environ)
            if env_overrides:
                child_env.update(env_overrides)
            proc = subprocess.Popen(
                command, cwd=str(cwd), stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding="utf-8", errors="replace", shell=False,
                env=child_env,
            )
            try:
                stdout, stderr = proc.communicate(timeout=self.command_timeout)
            except subprocess.TimeoutExpired:
                # The parent ProcessSupervisor owns tree termination. Returning
                # cleanup_pending asks it to kill the complete Job Object/group.
                return {
                    "_status": "BLOCKED",
                    "_cleanup_pending": True,
                    "command_profile": operation,
                    "pid": proc.pid,
                    "timeout_seconds": self.command_timeout,
                    "error": "host command timed out; parent must terminate containment",
                }
        except FileNotFoundError as exc:
            return {"_status": "BLOCKED", "command_profile": operation,
                    "error": f"executable_unavailable: {exc}"}
        duration = int((time.monotonic() - started) * 1000)
        stdout = stdout or ""
        stderr = stderr or ""
        out_bytes = stdout.encode("utf-8", errors="replace")
        err_bytes = stderr.encode("utf-8", errors="replace")
        result = {
            "command_profile": operation,
            "exit_code": int(proc.returncode),
            "duration_ms": duration,
            "stdout": stdout[-self.max_output_bytes:],
            "stderr": stderr[-self.max_output_bytes:],
            "stdout_truncated": len(out_bytes) > self.max_output_bytes,
            "stderr_truncated": len(err_bytes) > self.max_output_bytes,
        }
        result["_status"] = "PASS" if proc.returncode == 0 else "FAIL"
        return result

    def _run_pytest(self, args: dict) -> dict:
        raw_paths = args.get("paths")
        if not isinstance(raw_paths, list) or not raw_paths:
            raise HostOperationBlocked("run_pytest requires a non-empty paths list")
        cwd_default = str(self.allowed_roots[0]) if self.allowed_roots else str(self.work_root)
        cwd = self._resolve(args.get("cwd", cwd_default), self.allowed_roots, must_exist=True)
        if not cwd.is_dir():
            raise HostOperationBlocked("pytest cwd must be a directory")
        resolved_paths = []
        for raw in raw_paths:
            if not isinstance(raw, str) or raw.startswith("-"):
                raise HostOperationBlocked("pytest paths must be plain path strings, not flags")
            path = self._resolve(raw, self.allowed_roots, must_exist=True)
            if not self._inside(path, [cwd]):
                raise HostOperationBlocked("pytest paths must remain inside the selected cwd")
            if not (path.is_file() or path.is_dir()):
                raise HostOperationBlocked("pytest path must be a file or directory")
            resolved_paths.append(str(path))
        # Use a generated empty config and disable ambient plugin autoload.
        # Only conftest files under the selected cwd can participate.
        with tempfile.NamedTemporaryFile("w", suffix=".ini", encoding="utf-8",
                                         delete=False) as config:
            config.write("[pytest]\n")
            config_path = config.name
        try:
            command = [
                sys.executable, "-m", "pytest", "-q", "-c", config_path,
                "--confcutdir", str(cwd), *resolved_paths,
            ]
            return self._run_process(
                command, cwd, "pytest",
                env_overrides={"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
            )
        finally:
            try:
                Path(config_path).unlink(missing_ok=True)
            except OSError:
                pass

    def _run_powershell(self, args: dict) -> dict:
        if os.name != "nt":
            raise HostOperationBlocked("run_powershell_script is supported only on Windows")
        if not self.powershell_roots:
            raise HostOperationBlocked("PowerShell execution disabled: COMPUTER_AGENT_HOST_POWERSHELL_ROOTS is not configured")
        script = self._resolve(args.get("script"), self.powershell_roots, must_exist=True)
        if not script.is_file() or script.suffix.casefold() != ".ps1":
            raise HostOperationBlocked("PowerShell script must be an existing .ps1 file in an allowlisted root")
        raw_args = args.get("arguments", [])
        if not isinstance(raw_args, list) or any(not isinstance(x, str) for x in raw_args):
            raise HostOperationBlocked("PowerShell arguments must be a list of strings")
        if any(len(x) > 2048 for x in raw_args):
            raise HostOperationBlocked("PowerShell argument exceeds 2048 characters")
        executable = shutil.which("powershell.exe") or shutil.which("pwsh")
        if not executable:
            raise HostOperationBlocked("PowerShell executable is unavailable")
        command = [
            executable, "-NoLogo", "-NoProfile", "-NonInteractive",
            "-ExecutionPolicy", "RemoteSigned", "-File", str(script), *raw_args,
        ]
        return self._run_process(command, script.parent, "powershell_script")
