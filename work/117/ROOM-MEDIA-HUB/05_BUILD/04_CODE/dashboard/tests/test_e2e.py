#!/usr/bin/env python3
"""
W117 Dashboard — Automated E2E Test Suite
=========================================
Runs without external browser drivers (stdlib only).

Coverage:
  1. Snapshot integrity (counts + auth boundary)
  2. Static assets exist and are non-empty
  3. HTTP server serves index + data + assets
  4. HTML contains required views and provenance markers
  5. snapshot.json authorization boundary enforced
  6. No product-BUILD-authorized leakage in data

Usage:
  python tests/test_e2e.py
  python tests/test_e2e.py --port 8171

Exit 0 = all PASS, non-zero = FAIL
"""

from __future__ import annotations

import argparse
import json
import sys
import threading
import time
from http.client import HTTPConnection
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "snapshot.json"
DEFAULT_PORT = 8171  # avoid clash with manual run.py on 8170


class Results:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.errors: list[str] = []

    def ok(self, name: str) -> None:
        self.passed += 1
        print(f"  PASS  {name}")

    def fail(self, name: str, detail: str = "") -> None:
        self.failed += 1
        msg = f"  FAIL  {name}" + (f" — {detail}" if detail else "")
        print(msg)
        self.errors.append(msg)

    def summary(self) -> int:
        total = self.passed + self.failed
        print()
        print("=" * 56)
        print(f"  E2E RESULT: {self.passed}/{total} passed, {self.failed} failed")
        print("=" * 56)
        if self.errors:
            print("Failures:")
            for e in self.errors:
                print(e)
        return 0 if self.failed == 0 else 1


def test_snapshot_integrity(r: Results) -> dict | None:
    print("\n[1] Snapshot integrity")
    if not DATA_FILE.exists():
        r.fail("snapshot file exists", str(DATA_FILE))
        return None
    r.ok("snapshot file exists")

    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        r.ok("snapshot JSON parseable")
    except Exception as e:
        r.fail("snapshot JSON parseable", str(e))
        return None

    for key in ("meta", "overview", "dashboard_tasks", "product_tasks", "agents", "timeline"):
        if key in data:
            r.ok(f"key present: {key}")
        else:
            r.fail(f"key present: {key}")

    if len(data.get("dashboard_tasks", [])) == 9:
        r.ok("dashboard_tasks count == 9")
    else:
        r.fail("dashboard_tasks count == 9", f"got {len(data.get('dashboard_tasks', []))}")

    if len(data.get("product_tasks", [])) == 13:
        r.ok("product_tasks count == 13")
    else:
        r.fail("product_tasks count == 13", f"got {len(data.get('product_tasks', []))}")

    auth = data.get("meta", {}).get("authorization", {})
    if auth.get("dashboard_build") == "AUTHORIZED":
        r.ok("dashboard_build == AUTHORIZED")
    else:
        r.fail("dashboard_build == AUTHORIZED", str(auth.get("dashboard_build")))

    if auth.get("product_build") == "NOT AUTHORIZED":
        r.ok("product_build == NOT AUTHORIZED")
    else:
        r.fail("product_build == NOT AUTHORIZED", str(auth.get("product_build")))

    # Product tasks that must stay NOT AUTHORIZED
    for tid in ("W117-T009", "W117-T010", "W117-T011", "W117-T013"):
        t = next((x for x in data.get("product_tasks", []) if x.get("id") == tid), None)
        if t and "NOT AUTHORIZED" in t.get("status", ""):
            r.ok(f"{tid} remains NOT AUTHORIZED")
        else:
            r.fail(f"{tid} remains NOT AUTHORIZED", str(t))

    go = next((a for a in data.get("agents", []) if str(a.get("name", "")).startswith("Go")), None)
    if go and ("ACK" in go.get("status", "").upper() or "IN_PROGRESS" in go.get("status", "").upper()):
        r.ok("Go agent ACK/IN_PROGRESS present")
    else:
        r.fail("Go agent ACK/IN_PROGRESS present", str(go))

    if len(data.get("timeline", [])) >= 3:
        r.ok("timeline has >= 3 entries")
    else:
        r.fail("timeline has >= 3 entries", str(len(data.get("timeline", []))))

    return data


def test_static_assets(r: Results) -> None:
    print("\n[2] Static assets")
    required = [
        ROOT / "index.html",
        ROOT / "run.py",
        ROOT / "assets" / "dashboard.css",
        ROOT / "assets" / "dashboard.js",
        ROOT / "data" / "snapshot.json",
        ROOT / "README.md",
    ]
    for path in required:
        if path.exists() and path.stat().st_size > 0:
            r.ok(f"asset exists & non-empty: {path.relative_to(ROOT)}")
        else:
            r.fail(f"asset exists & non-empty: {path.relative_to(ROOT)}")


def test_html_markers(r: Results) -> None:
    print("\n[3] HTML structural markers")
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    checks = [
        ("view-overview", "id=\"view-overview\"" in html or 'id="view-overview"' in html),
        ("view-tasks", "view-tasks" in html),
        ("view-agents", "view-agents" in html),
        ("view-timeline", "view-timeline" in html),
        ("dashboard.js referenced", "dashboard.js" in html),
        ("dashboard.css referenced", "dashboard.css" in html),
        ("load-error element", "load-error" in html),
        ("provenance element", "provenance" in html),
    ]
    for name, ok in checks:
        if ok:
            r.ok(f"HTML marker: {name}")
        else:
            r.fail(f"HTML marker: {name}")


def test_js_contract(r: Results) -> None:
    print("\n[4] JS data contract")
    js = (ROOT / "assets" / "dashboard.js").read_text(encoding="utf-8")
    checks = [
        ("fetches snapshot.json", "snapshot.json" in js),
        ("statusClass helper", "statusClass" in js),
        ("renderOverview", "renderOverview" in js),
        ("renderAgents", "renderAgents" in js),
        ("renderTimeline", "renderTimeline" in js),
        ("no-store cache", "no-store" in js),
    ]
    for name, ok in checks:
        if ok:
            r.ok(f"JS: {name}")
        else:
            r.fail(f"JS: {name}")


class _Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        pass  # quiet


def test_http_server(r: Results, port: int) -> None:
    print(f"\n[5] HTTP server E2E (port {port})")
    server = ThreadingHTTPServer(("127.0.0.1", port), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.15)

    def fetch(path: str) -> tuple[int, str]:
        conn = HTTPConnection("127.0.0.1", port, timeout=3)
        try:
            conn.request("GET", path)
            resp = conn.getresponse()
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body
        finally:
            conn.close()

    try:
        # index
        status, body = fetch("/")
        if status == 200 and "W117 Dashboard" in body:
            r.ok("GET / → 200 + title")
        else:
            r.fail("GET / → 200 + title", f"status={status}")

        # snapshot
        status, body = fetch("/data/snapshot.json")
        if status == 200:
            try:
                data = json.loads(body)
                r.ok("GET /data/snapshot.json → 200 + JSON")
                if data.get("meta", {}).get("authorization", {}).get("product_build") == "NOT AUTHORIZED":
                    r.ok("served snapshot keeps product_build NOT AUTHORIZED")
                else:
                    r.fail("served snapshot keeps product_build NOT AUTHORIZED")
            except json.JSONDecodeError as e:
                r.fail("GET /data/snapshot.json → 200 + JSON", str(e))
        else:
            r.fail("GET /data/snapshot.json → 200 + JSON", f"status={status}")

        # assets
        for path in ("/assets/dashboard.css", "/assets/dashboard.js"):
            status, body = fetch(path)
            if status == 200 and len(body) > 50:
                r.ok(f"GET {path} → 200 + content")
            else:
                r.fail(f"GET {path} → 200 + content", f"status={status} len={len(body)}")

        # 404 for missing
        status, _ = fetch("/this-should-not-exist-w117")
        if status == 404:
            r.ok("GET missing path → 404")
        else:
            r.fail("GET missing path → 404", f"status={status}")

    finally:
        server.shutdown()
        server.server_close()


def main() -> int:
    parser = argparse.ArgumentParser(description="W117 Dashboard E2E tests")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    print("W117 Dashboard — Automated E2E Test Suite")
    print(f"Root: {ROOT}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    r = Results()
    test_snapshot_integrity(r)
    test_static_assets(r)
    test_html_markers(r)
    test_js_contract(r)
    test_http_server(r, args.port)

    return r.summary()


if __name__ == "__main__":
    sys.exit(main())
