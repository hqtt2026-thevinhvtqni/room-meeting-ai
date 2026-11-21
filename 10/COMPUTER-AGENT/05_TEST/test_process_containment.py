"""Work 10 — OS process-tree containment regression tests.

Windows validates Job Object KILL_ON_JOB_CLOSE with a worker and grandchild.
POSIX validates the limited process-group termination primitive. A POSIX
process group is not claimed as equivalent to cgroup-v2 containment.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "04_CODE"))

from process_supervisor import (
    ContainmentError,
    WindowsJob,
    terminate_posix_process_group,
    wait_pid_exit,
)

FAILED = []


def check(name, fn):
    try:
        result = fn()
        if result is False:
            raise AssertionError("check returned False")
        print(f"  PASS  {name}")
    except Exception as exc:
        FAILED.append(f"{name}: {type(exc).__name__}: {exc}")
        print(f"  FAIL  {name}: {type(exc).__name__}: {exc}")


CHILD_CODE = (
    "import subprocess,sys,time; "
    "print('READY', flush=True); "
    "sys.stdin.readline(); "
    "p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)']); "
    "print(p.pid, flush=True); "
    "time.sleep(60)"
)


def test_windows_job_object():
    if os.name != "nt":
        print("  SKIP  Windows Job Object test requires Windows")
        return
    proc = subprocess.Popen(
        [sys.executable, "-c", CHILD_CODE],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    job = None
    try:
        if proc.stdout.readline().strip() != "READY":
            raise AssertionError("worker did not reach inert pre-start gate")
        job = WindowsJob()
        job.assign_process(proc)
        proc.stdin.write("START\n")
        proc.stdin.flush()
        grandchild_pid = int(proc.stdout.readline().strip())
        if job.active_processes() < 2:
            raise AssertionError("Job Object does not report both worker and grandchild")
        job.close()
        job = None
        proc.wait(timeout=5)
        if not wait_pid_exit(grandchild_pid, timeout_seconds=5):
            raise AssertionError(f"grandchild {grandchild_pid} survived Job Object close")
    finally:
        if job is not None:
            try:
                job.close()
            except Exception:
                pass
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=5)
        for stream in (proc.stdin, proc.stdout, proc.stderr):
            if stream:
                stream.close()


def test_posix_process_group():
    if os.name == "nt":
        print("  SKIP  POSIX process-group test requires POSIX")
        return
    proc = subprocess.Popen(
        [sys.executable, "-c", CHILD_CODE],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, start_new_session=True,
    )
    try:
        if proc.stdout.readline().strip() != "READY":
            raise AssertionError("worker did not reach inert pre-start gate")
        proc.stdin.write("START\n")
        proc.stdin.flush()
        grandchild_pid = int(proc.stdout.readline().strip())
        time.sleep(0.1)
        if not terminate_posix_process_group(proc, timeout_seconds=3):
            raise AssertionError("process group did not become empty")
        if not wait_pid_exit(grandchild_pid, timeout_seconds=5):
            raise AssertionError(f"grandchild {grandchild_pid} survived process-group kill")
    finally:
        if proc.poll() is None:
            try:
                os.killpg(proc.pid, 9)
            except ProcessLookupError:
                pass
            proc.wait(timeout=5)
        for stream in (proc.stdin, proc.stdout, proc.stderr):
            if stream:
                stream.close()


def main():
    print("Work 10 — Process Containment Tests")
    if os.name == "nt":
        check("Windows Job Object contains and kills descendant tree", test_windows_job_object)
    else:
        check("POSIX process group kills worker and descendant (limited profile)", test_posix_process_group)
    if FAILED:
        print(f"Process containment tests: {len(FAILED)} FAILED")
        for item in FAILED:
            print("  - " + item)
        raise SystemExit(1)
    print("Process containment tests: ALL PASSED")


if __name__ == "__main__":
    main()
