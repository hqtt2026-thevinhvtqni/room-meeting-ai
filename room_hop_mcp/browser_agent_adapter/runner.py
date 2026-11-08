"""Exact-SHA, disposable-store launcher for the Work 32 Windows lane."""
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from typing import Mapping


SENTINEL_NAME = ".roomhop-disposable-test-store"
SENTINEL_VALUE = "ROOM-HOP-WORK32-DISPOSABLE-TEST-STORE"


def validate_runtime_config(
    source_sha: str,
    meetings_dir: str | Path,
    port: int,
    environ: Mapping[str, str] | None = None,
) -> Path:
    """Fail closed unless this process is bound to the current job fixture."""
    env = os.environ if environ is None else environ
    if not re.fullmatch(r"[0-9a-f]{40}", source_sha):
        raise ValueError("source SHA must be a full 40-character lowercase Git SHA")
    if env.get("GITHUB_SHA") != source_sha:
        raise ValueError("launcher source SHA does not match GITHUB_SHA")
    if env.get("ROOMHOP_TEST_MODE") != "1":
        raise ValueError("ROOMHOP_TEST_MODE=1 is required")
    if not 1 <= int(port) <= 65535:
        raise ValueError("adapter port must be between 1 and 65535")

    raw_store = Path(meetings_dir).expanduser()
    if not raw_store.is_absolute():
        raise ValueError("disposable meetings directory must be an absolute path")
    try:
        store = raw_store.resolve(strict=True)
    except OSError as exc:
        raise ValueError("disposable meetings directory does not exist") from exc
    if not store.is_dir():
        raise ValueError("disposable meetings path is not a directory")

    configured_store = env.get("ROOMHOP_TEST_MEETINGS_DIR")
    if not configured_store:
        raise ValueError("ROOMHOP_TEST_MEETINGS_DIR is required")
    try:
        configured = Path(configured_store).expanduser().resolve(strict=True)
    except OSError as exc:
        raise ValueError("configured disposable meetings directory is unavailable") from exc
    if configured != store:
        raise ValueError("launcher store does not match ROOMHOP_TEST_MEETINGS_DIR")

    marker = store / SENTINEL_NAME
    try:
        marker_value = marker.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise ValueError("disposable-store sentinel is missing or unreadable") from exc
    if marker_value != SENTINEL_VALUE:
        raise ValueError("disposable-store sentinel is invalid")

    if not env.get("ROOMHOP_TEST_MEETING_ID"):
        raise ValueError("ROOMHOP_TEST_MEETING_ID is required")
    if not env.get("ROOMHOP_TEST_IDENTITY_ID"):
        raise ValueError("ROOMHOP_TEST_IDENTITY_ID is required")
    configured_port = env.get("ROOMHOP_BROWSER_ADAPTER_PORT")
    if configured_port is not None and configured_port != str(port):
        raise ValueError("launcher port does not match ROOMHOP_BROWSER_ADAPTER_PORT")
    return store


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--meetings-dir", required=True)
    parser.add_argument("--port", required=True, type=int)
    args = parser.parse_args(argv)

    store = validate_runtime_config(
        source_sha=args.source_sha,
        meetings_dir=args.meetings_dir,
        port=args.port,
    )
    os.environ["ROOMHOP_TEST_MEETINGS_DIR"] = str(store)
    os.environ["ROOMHOP_BROWSER_ADAPTER_PORT"] = str(args.port)

    import uvicorn

    uvicorn.run(
        "room_hop_mcp.browser_agent_adapter.adapter:app",
        host="127.0.0.1",
        port=args.port,
        log_level="info",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
