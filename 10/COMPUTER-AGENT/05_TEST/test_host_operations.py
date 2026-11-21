"""Unit tests for the separate PC host capability contract."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from host_operations import HostOperations


FAILED = []
SKIPPED = 0


class DummyPolicy:
    def __init__(self, root):
        self.work_root = str(root)


def check(name, fn):
    global SKIPPED
    try:
        outcome = fn()
        if outcome == "SKIP":
            SKIPPED += 1
            print(f"  SKIP  {name}")
        elif outcome is False:
            raise AssertionError("check returned False")
        else:
            print(f"  PASS  {name}")
    except Exception as exc:
        FAILED.append(f"{name}: {exc}")
        print(f"  FAIL  {name}: {exc}")


def main():
    print("Work 10 — PC Host Operations Tests")
    print("=" * 58)
    with tempfile.TemporaryDirectory(prefix="w10-host-ops-") as temp:
        root = Path(temp) / "allowed"
        outside = Path(temp) / "outside"
        root.mkdir()
        outside.mkdir()
        (root / "sample.txt").write_text("HOST_READ_OK", encoding="utf-8")
        (outside / "secret.txt").write_text("OUTSIDE_SECRET", encoding="utf-8")
        (root / "test_sample.py").write_text(
            "def test_host_operation_pytest():\n    assert 40 + 2 == 42\n",
            encoding="utf-8",
        )
        (root / "probe.ps1").write_text("Write-Output 'W10_PS_OK'\n", encoding="utf-8")
        env = {
            "COMPUTER_AGENT_HOST_ALLOWED_ROOTS": str(root),
            "COMPUTER_AGENT_HOST_WRITABLE_ROOTS": str(root),
            "COMPUTER_AGENT_HOST_POWERSHELL_ROOTS": str(root),
            "COMPUTER_AGENT_HOST_COMMAND_TIMEOUT_SECONDS": "30",
        }
        with patch.dict(os.environ, env, clear=False):
            ops = HostOperations(DummyPolicy(root))
            listing = ops.execute("list_directory", {"path": "."})
            check("list_directory only returns allowlisted directory",
                  lambda: listing["status"] == "PASS"
                  and any(x["name"] == "sample.txt" for x in listing["result"]["entries"]))
            read = ops.execute("read_file", {"path": "sample.txt"})
            check("read_file returns content and SHA-256",
                  lambda: read["status"] == "PASS"
                  and read["result"]["content"] == "HOST_READ_OK"
                  and len(read["result"]["sha256"]) == 64)
            check("evidence metadata does not duplicate file contents",
                  lambda: "content" not in read["evidence"][0]["result"])
            traversal = ops.execute("read_file", {"path": "../outside/secret.txt"})
            check("path traversal outside root is BLOCKED",
                  lambda: traversal["status"] == "BLOCKED")
            unknown = ops.execute("run_shell", {"command": "whoami"})
            check("generic shell operation is not exposed",
                  lambda: unknown["status"] == "BLOCKED")
            bad_pytest = ops.execute("run_pytest", {"cwd": str(root), "paths": ["-c", "evil"]})
            check("pytest rejects arbitrary command-line flags",
                  lambda: bad_pytest["status"] == "BLOCKED")
            write = ops.execute("write_file", {"path": "new.txt", "content": "WRITE_OK"})
            check("write_file verifies exact read-back",
                  lambda: write["status"] == "PASS"
                  and write["result"]["readback_verified"] is True
                  and write["result"]["created"] is True)
            implicit = ops.execute("write_file", {"path": "new.txt", "content": "overwrite"})
            check("write_file refuses implicit overwrite",
                  lambda: implicit["status"] == "BLOCKED")
            explicit = ops.execute("write_file", {
                "path": "new.txt", "content": "OVERWRITE_OK", "overwrite": True
            })
            check("write_file accepts explicit overwrite and verifies bytes",
                  lambda: explicit["status"] == "PASS"
                  and explicit["result"]["overwritten"] is True
                  and (root / "new.txt").read_text(encoding="utf-8") == "OVERWRITE_OK")
            pytest_result = ops.execute("run_pytest", {
                "cwd": str(root), "paths": ["test_sample.py"]
            })
            check("run_pytest uses fixed Python module command",
                  lambda: pytest_result["status"] == "PASS"
                  and pytest_result["result"]["exit_code"] == 0)

            try:
                (root / "escape").symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                check("symlink escape is blocked", lambda: "SKIP")
            else:
                symlink_result = ops.execute("read_file", {"path": "escape/secret.txt"})
                check("symlink escape is blocked",
                      lambda: symlink_result["status"] == "BLOCKED")

        with patch.dict(os.environ, {
            "COMPUTER_AGENT_HOST_ALLOWED_ROOTS": str(root),
        }, clear=True):
            read_only = HostOperations(DummyPolicy(root))
            denied_write = read_only.execute("write_file", {
                "path": "disabled.txt", "content": "NO"
            })
            check("write_file is disabled unless writable roots are configured",
                  lambda: denied_write["status"] == "BLOCKED")

        if os.name == "nt":
            with patch.dict(os.environ, env, clear=False):
                ps_result = HostOperations(DummyPolicy(root)).execute(
                    "run_powershell_script", {"script": "probe.ps1"}
                )
                check("PowerShell executes only allowlisted .ps1 file",
                      lambda: ps_result["status"] == "PASS"
                      and "W10_PS_OK" in ps_result["result"].get("stdout", ""))
                outside_ps = HostOperations(DummyPolicy(root)).execute(
                    "run_powershell_script", {"script": str(outside / "probe.ps1")}
                )
                check("PowerShell rejects scripts outside allowlisted roots",
                      lambda: outside_ps["status"] == "BLOCKED")
        else:
            check("PowerShell is blocked on non-Windows hosts", lambda: "SKIP")

    print("=" * 58)
    print(f"Host operations tests: {len(FAILED)} failed, {SKIPPED} skipped")
    if FAILED:
        for item in FAILED:
            print(f"  - {item}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
