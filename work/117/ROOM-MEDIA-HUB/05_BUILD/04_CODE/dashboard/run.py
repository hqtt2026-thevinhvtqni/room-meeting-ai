#!/usr/bin/env python3
"""
W117 Operational Dashboard — local preview server

Usage:
  python run.py              # default port 8170
  python run.py --port 9000

Then open: http://127.0.0.1:8170/

Scope: read-only Dashboard for Work 117 only.
Does NOT implement ROOM MEDIA HUB product features.
"""

from __future__ import annotations

import argparse
import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "snapshot.json"
DEFAULT_PORT = 8170


def validate_snapshot() -> dict:
    if not DATA_FILE.exists():
        print(f"[FAIL] Missing data file: {DATA_FILE}", file=sys.stderr)
        sys.exit(1)
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[FAIL] Invalid JSON in snapshot: {e}", file=sys.stderr)
        sys.exit(1)

    errors = []
    if "meta" not in data:
        errors.append("missing meta")
    if len(data.get("dashboard_tasks", [])) != 9:
        errors.append(f"dashboard_tasks expected 9, got {len(data.get('dashboard_tasks', []))}")
    if len(data.get("product_tasks", [])) != 13:
        errors.append(f"product_tasks expected 13, got {len(data.get('product_tasks', []))}")
    if len(data.get("agents", [])) < 1:
        errors.append("agents list empty")
    if len(data.get("timeline", [])) < 1:
        errors.append("timeline empty")

    auth = data.get("meta", {}).get("authorization", {})
    if auth.get("dashboard_build") != "AUTHORIZED":
        errors.append("dashboard_build is not AUTHORIZED in snapshot")
    if auth.get("product_build") != "NOT AUTHORIZED":
        errors.append("product_build must remain NOT AUTHORIZED")

    if errors:
        print("[FAIL] Snapshot integrity checks failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    print("[OK] Snapshot integrity checks passed")
    print(f"     dashboard_tasks = {len(data['dashboard_tasks'])}")
    print(f"     product_tasks   = {len(data['product_tasks'])}")
    print(f"     agents          = {len(data['agents'])}")
    print(f"     timeline        = {len(data['timeline'])}")
    return data


class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        # Keep logs short
        sys.stdout.write("%s - %s\n" % (self.address_string(), fmt % args))


def main() -> None:
    parser = argparse.ArgumentParser(description="W117 Dashboard local server")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--skip-check", action="store_true", help="Skip snapshot integrity check")
    args = parser.parse_args()

    if not args.skip_check:
        validate_snapshot()

    server = ThreadingHTTPServer(("127.0.0.1", args.port), QuietHandler)
    print()
    print("=" * 56)
    print("  W117 W117 Operational Dashboard")
    print("=" * 56)
    print(f"  URL     : http://127.0.0.1:{args.port}/")
    print(f"  Root    : {ROOT}")
    print(f"  Data    : {DATA_FILE}")
    print("  Scope   : Dashboard ONLY (product BUILD not authorized)")
    print("  Stop    : Ctrl+C")
    print("=" * 56)
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[STOP] Server stopped")
        server.server_close()


if __name__ == "__main__":
    main()
