"""Create the Work32 Windows E2E meeting through the Core service boundary."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SENTINEL_NAME = ".roomhop-disposable-test-store"
SENTINEL_VALUE = "ROOM-HOP-WORK32-DISPOSABLE-TEST-STORE"
MEETING_ID = "MEETING-W32-DISPOSABLE"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--store", required=True)
    parser.add_argument("--workspace", required=True)
    args = parser.parse_args()

    store = Path(args.store).resolve(strict=True)
    workspace = Path(args.workspace).resolve(strict=True)
    if not store.is_absolute() or store == workspace or workspace in store.parents:
        raise SystemExit("BLOCKED: fixture store must be outside the checkout")
    sentinel = store / SENTINEL_NAME
    if not sentinel.is_file() or sentinel.read_text(encoding="utf-8").strip() != SENTINEL_VALUE:
        raise SystemExit("BLOCKED: disposable-store sentinel is absent or invalid")
    contents = [p for p in store.iterdir() if p.name != SENTINEL_NAME]
    if contents:
        raise SystemExit("BLOCKED: fixture store is not empty before bootstrap")

    sys.path.insert(0, str(workspace))
    from core.meeting_manager import MeetingManager
    from core.meeting_service import MeetingService

    service = MeetingService(MeetingManager(meetings_dir=store))
    created = service.create_meeting(
        meeting_id=MEETING_ID,
        topic="Work32 Windows Browser Adapter disposable E2E",
        participants=["xu"],
        context_files=[],
        created_by="vinh",
    )
    assert created["status"] == "draft", created
    opened = service.open_meeting(MEETING_ID)
    assert opened["status"] == "open", opened
    joined_vinh = service.join_meeting(MEETING_ID, "vinh")
    assert "vinh" in joined_vinh["participants"], joined_vinh
    joined_xu = service.join_meeting(MEETING_ID, "xu")
    assert "xu" in joined_xu["participants"], joined_xu
    active = service.start_meeting(MEETING_ID, starter="vinh")
    assert active["status"] == "active", active
    confirmed = service.get_meeting(MEETING_ID)
    assert confirmed["status"] == "active", confirmed
    print(f"FIXTURE_PASS meeting_id={MEETING_ID} status={confirmed['status']} store={store}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
