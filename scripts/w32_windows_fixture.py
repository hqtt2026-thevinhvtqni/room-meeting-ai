"""Create one isolated Core meeting fixture for a Work 32 Windows job."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from core.meeting_manager import MeetingManager
from core.meeting_service import MeetingService

SENTINEL_NAME = ".roomhop-disposable-test-store"
SENTINEL_VALUE = "ROOM-HOP-WORK32-DISPOSABLE-TEST-STORE"
ALLOWED_TEST_IDENTITIES = {"xu"}


def create_fixture(
    store_path: str | Path,
    meeting_id: str,
    identity_id: str,
    runner_temp: str | Path,
    workspace: str | Path,
) -> Path:
    runner_root = Path(runner_temp).resolve(strict=True)
    workspace_root = Path(workspace).resolve(strict=True)
    raw_store = Path(store_path).expanduser()
    if not raw_store.is_absolute():
        raise ValueError("fixture store must be an absolute path")
    store = raw_store.resolve()
    if not store.is_relative_to(runner_root):
        raise ValueError("fixture store must be a child of RUNNER_TEMP")
    if store.is_relative_to(workspace_root):
        raise ValueError("fixture store must be outside GITHUB_WORKSPACE")
    if store.exists():
        raise ValueError("fixture store already exists; refusing to reuse it")
    if not re.fullmatch(r"MEETING-W32-[0-9]+-[0-9]+", meeting_id):
        raise ValueError("meeting ID must be unique to a Work32 run and attempt")
    if identity_id not in ALLOWED_TEST_IDENTITIES:
        raise ValueError("identity is not in the approved Windows E2E test allowlist")

    store.mkdir(parents=True, exist_ok=False)
    (store / SENTINEL_NAME).write_text(SENTINEL_VALUE, encoding="utf-8")

    manager = MeetingManager(meetings_dir=store)
    service = MeetingService(manager)
    service.create_meeting(
        meeting_id=meeting_id,
        topic="Work32 disposable Windows Browser Adapter E2E",
        participants=[identity_id],
        context_files=[],
        created_by="vinh",
    )
    service.open_meeting(meeting_id)
    service.join_meeting(meeting_id, "vinh")
    service.join_meeting(meeting_id, identity_id)
    active = service.start_meeting(meeting_id, "vinh")
    if active.get("status") != "active":
        raise RuntimeError("Core did not start the disposable E2E meeting")
    return store


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", required=True)
    parser.add_argument("--meeting-id", required=True)
    parser.add_argument("--identity-id", required=True)
    parser.add_argument("--runner-temp", required=True)
    parser.add_argument("--workspace", required=True)
    args = parser.parse_args()
    store = create_fixture(
        store_path=args.store,
        meeting_id=args.meeting_id,
        identity_id=args.identity_id,
        runner_temp=args.runner_temp,
        workspace=args.workspace,
    )
    print(f"fixture_store={store}")
    print(f"fixture_meeting_id={args.meeting_id}")
    print(f"fixture_identity_id={args.identity_id}")
    print("fixture_status=active")
    print(f"fixture_sentinel={store / SENTINEL_NAME}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
