"""Provision one isolated ROOM HOP meeting for the Windows Browser Adapter lane.

This helper runs only inside the dedicated GitHub Actions runner job. It never
falls back to the repository's default meetings directory.
"""
from __future__ import annotations

import json
import os
import socket
import sys
from pathlib import Path

# When Python executes a file by path, sys.path[0] is its scripts/ directory.
# Add this exact checkout root explicitly so the fixture imports the Core
# package from the revision under test, independent of runner cwd/PYTHONPATH.
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService

SENTINEL = "ROOM-HOP-WORK32-DISPOSABLE-TEST-STORE"


def _free_loopback_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def provision() -> dict:
    runner_temp = Path(os.environ["RUNNER_TEMP"]).resolve()
    workspace = Path(os.environ["GITHUB_WORKSPACE"]).resolve()
    run_id = "".join(ch for ch in os.environ["GITHUB_RUN_ID"] if ch.isdigit())
    attempt = "".join(ch for ch in os.environ["GITHUB_RUN_ATTEMPT"] if ch.isdigit())
    if not run_id or not attempt:
        raise RuntimeError("GITHUB_RUN_ID and GITHUB_RUN_ATTEMPT must be numeric")

    base = (runner_temp / "room-hop-w32-disposable").resolve()
    if base == workspace or workspace in base.parents:
        raise RuntimeError("Disposable fixture path must be outside GITHUB_WORKSPACE")
    base.mkdir(parents=True, exist_ok=True)
    store = base / f"run-{run_id}-attempt-{attempt}"
    store.mkdir(parents=False, exist_ok=False)
    (store / ".roomhop-disposable-test-store").write_text(
        SENTINEL, encoding="utf-8"
    )

    meeting_id = f"MEETING-W32-{run_id}-{attempt}"
    manager = MeetingManager(meetings_dir=store)
    service = MeetingService(manager)
    service.create_meeting(
        meeting_id=meeting_id,
        topic=f"Disposable Work32 Browser E2E run {run_id}/{attempt}",
        participants=["xu"],
        context_files=[],
        created_by="vinh",
    )
    service.open_meeting(meeting_id)
    service.join_meeting(meeting_id, "vinh")
    service.join_meeting(meeting_id, "xu")
    active = service.start_meeting(meeting_id, starter="vinh")
    if active.get("status") != "active":
        raise RuntimeError(f"Disposable meeting did not become active: {active!r}")

    port = _free_loopback_port()
    identity_id = "vinh"
    adapter_url = f"http://127.0.0.1:{port}"
    fixture = {
        "repository": os.environ.get("GITHUB_REPOSITORY"),
        "ref": os.environ.get("GITHUB_REF"),
        "run_id": run_id,
        "run_attempt": attempt,
        "source_sha": os.environ["GITHUB_SHA"],
        "meetings_dir": str(store),
        "sentinel": str(store / ".roomhop-disposable-test-store"),
        "meeting_id": meeting_id,
        "meeting_status": active["status"],
        "participants": active.get("participants", []),
        "identity_id": identity_id,
        "adapter_port": port,
        "adapter_url": adapter_url,
    }

    results = Path("test-results")
    results.mkdir(parents=True, exist_ok=True)
    (results / "windows-fixture.json").write_text(
        json.dumps(fixture, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    github_env = os.environ.get("GITHUB_ENV")
    if not github_env:
        raise RuntimeError("GITHUB_ENV is required inside GitHub Actions")
    env_values = {
        "ROOMHOP_TEST_MODE": "1",
        "ROOMHOP_TEST_MEETINGS_DIR": str(store),
        "ROOMHOP_TEST_MEETING_ID": meeting_id,
        "ROOMHOP_TEST_IDENTITY_ID": identity_id,
        "ROOM_HOP_MEETINGS_DIR": str(store),
        "ROOMHOP_BROWSER_ADAPTER_PORT": str(port),
        "ROOMHOP_BROWSER_ADAPTER_URL": adapter_url,
        "PLAYWRIGHT_BROWSERS_PATH": str(runner_temp / "playwright-browsers"),
    }
    with open(github_env, "a", encoding="utf-8") as stream:
        for key, value in env_values.items():
            if "\n" in value or "\r" in value:
                raise RuntimeError(f"Invalid newline in Actions environment value: {key}")
            stream.write(f"{key}={value}\n")
    return fixture


if __name__ == "__main__":
    print(json.dumps(provision(), indent=2, ensure_ascii=False))
