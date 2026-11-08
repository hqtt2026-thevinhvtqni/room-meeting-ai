"""Exact-SHA bootstrap for a job-owned Work32 Browser Adapter process."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Running this file by path puts scripts/ at sys.path[0]. The embedded Python
# runtime is intentionally isolated, so explicitly expose this exact checkout
# root before Uvicorn imports the application module.
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

import yaml
import uvicorn

SENTINEL = "ROOM-HOP-WORK32-DISPOSABLE-TEST-STORE"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--meetings-dir", required=True)
    parser.add_argument("--meeting-id", required=True)
    parser.add_argument("--identity-id", required=True)
    parser.add_argument("--port", required=True, type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = Path.cwd().resolve()
    actual_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=workspace, text=True
    ).strip()
    if actual_sha.lower() != args.source_sha.lower():
        raise SystemExit(
            f"BLOCKED: checkout SHA {actual_sha} != requested SHA {args.source_sha}"
        )

    store = Path(args.meetings_dir).expanduser().resolve(strict=True)
    marker = store / ".roomhop-disposable-test-store"
    if not marker.is_file() or marker.read_text(encoding="utf-8").strip() != SENTINEL:
        raise SystemExit("BLOCKED: disposable store sentinel missing or invalid")
    meeting_file = store / args.meeting_id / "meeting.yaml"
    if not meeting_file.is_file():
        raise SystemExit("BLOCKED: exact disposable meeting is missing")
    meeting = yaml.safe_load(meeting_file.read_text(encoding="utf-8")) or {}
    if meeting.get("id") != args.meeting_id or meeting.get("status") != "active":
        raise SystemExit("BLOCKED: disposable meeting is not active")
    if args.identity_id not in meeting.get("participants", []):
        raise SystemExit("BLOCKED: configured identity has not JOIN_ACCEPTED")

    os.environ["ROOMHOP_TEST_MODE"] = "1"
    os.environ["ROOMHOP_TEST_MEETINGS_DIR"] = str(store)
    os.environ["ROOMHOP_TEST_MEETING_ID"] = args.meeting_id
    os.environ["ROOMHOP_TEST_IDENTITY_ID"] = args.identity_id
    os.environ["ROOM_HOP_MEETINGS_DIR"] = str(store)
    os.environ["ROOMHOP_BROWSER_ADAPTER_PORT"] = str(args.port)

    uvicorn.run(
        "room_hop_mcp.browser_agent_adapter.adapter:app",
        host="127.0.0.1",
        port=args.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
