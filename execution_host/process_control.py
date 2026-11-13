from __future__ import annotations

import os
import shutil
import signal
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


MAX_OUTPUT_BYTES = 1024 * 1024


@dataclass(frozen=True)
class BoundedProcessResult:
    returncode: int
    stdout: bytes
    stderr: bytes
    timed_out: bool
    output_limit_exceeded: bool
    tree_termination_confirmed: bool


def _terminate_process_tree(process: subprocess.Popen[bytes]) -> bool:
    """Terminate the process group/tree and fail closed if termination is unconfirmed."""
    if os.name == "nt":
        taskkill = shutil.which("taskkill")
        if not taskkill:
            root = os.environ.get("SystemRoot", r"C:\Windows")
            candidate = Path(root) / "System32" / "taskkill.exe"
            taskkill = str(candidate) if candidate.is_file() else None
        if not taskkill:
            return False
        try:
            result = subprocess.run(
                [taskkill, "/PID", str(process.pid), "/T", "/F"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
                check=False,
            )
            process.wait(timeout=5)
            return result.returncode == 0 and process.poll() is not None
        except (OSError, subprocess.SubprocessError):
            try:
                process.kill()
                process.wait(timeout=5)
            except (OSError, subprocess.SubprocessError):
                pass
            return False

    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        try:
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            return False
        return True
    except OSError:
        return False

    try:
        process.wait(timeout=0.5)
    except subprocess.TimeoutExpired:
        pass

    try:
        os.killpg(process.pid, 0)
    except ProcessLookupError:
        return process.poll() is not None
    except OSError:
        return False

    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except OSError:
        return False

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        try:
            process.kill()
            process.wait(timeout=2)
        except (OSError, subprocess.SubprocessError):
            return False

    try:
        os.killpg(process.pid, 0)
    except ProcessLookupError:
        return process.poll() is not None
    except OSError:
        return False
    return False


def run_bounded(
    command: Sequence[str],
    *,
    cwd: str | Path,
    env: dict[str, str],
    timeout: float,
    max_output_bytes: int = MAX_OUTPUT_BYTES,
) -> BoundedProcessResult:
    """Run without a shell, cap combined stdout/stderr, and terminate the process tree on limits."""
    if not command or timeout <= 0 or max_output_bytes < 1:
        raise ValueError("bounded_process_arguments_invalid")

    kwargs = {
        "args": list(command),
        "cwd": str(cwd),
        "env": env,
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "bufsize": 0,
    }
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True

    process = subprocess.Popen(**kwargs)
    stdout = bytearray()
    stderr = bytearray()
    remaining = [max_output_bytes]
    lock = threading.Lock()
    output_exceeded = threading.Event()

    def drain(stream, target: bytearray) -> None:
        try:
            while True:
                chunk = stream.read(65536)
                if not chunk:
                    return
                with lock:
                    allowed = min(len(chunk), remaining[0])
                    if allowed:
                        target.extend(chunk[:allowed])
                        remaining[0] -= allowed
                    if allowed < len(chunk):
                        output_exceeded.set()
        except (OSError, ValueError):
            return

    readers = [
        threading.Thread(target=drain, args=(process.stdout, stdout), daemon=True),
        threading.Thread(target=drain, args=(process.stderr, stderr), daemon=True),
    ]
    for reader in readers:
        reader.start()

    deadline = time.monotonic() + timeout
    timed_out = False
    tree_confirmed = True

    while process.poll() is None:
        if output_exceeded.is_set():
            tree_confirmed = _terminate_process_tree(process)
            break
        if time.monotonic() >= deadline:
            timed_out = True
            tree_confirmed = _terminate_process_tree(process)
            break
        time.sleep(0.025)

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        tree_confirmed = _terminate_process_tree(process) and tree_confirmed

    for reader in readers:
        reader.join(timeout=2)
    if any(reader.is_alive() for reader in readers):
        tree_confirmed = _terminate_process_tree(process) and tree_confirmed
        for reader in readers:
            reader.join(timeout=2)
    if any(reader.is_alive() for reader in readers):
        tree_confirmed = False

    if process.poll() is None:
        try:
            process.kill()
            process.wait(timeout=2)
        except (OSError, subprocess.SubprocessError):
            pass
        tree_confirmed = False

    return BoundedProcessResult(
        returncode=process.returncode if process.returncode is not None else -1,
        stdout=bytes(stdout),
        stderr=bytes(stderr),
        timed_out=timed_out,
        output_limit_exceeded=output_exceeded.is_set(),
        tree_termination_confirmed=tree_confirmed,
    )
