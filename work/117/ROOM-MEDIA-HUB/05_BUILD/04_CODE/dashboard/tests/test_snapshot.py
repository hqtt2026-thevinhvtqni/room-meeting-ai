#!/usr/bin/env python3
"""
Self-test for W117 Dashboard snapshot integrity.
Run: python tests/test_snapshot.py
Exit code 0 = PASS, non-zero = FAIL
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "snapshot.json"


def main() -> int:
    failures = []

    if not DATA.exists():
        print(f"FAIL: missing {DATA}")
        return 1

    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAIL: cannot parse JSON: {e}")
        return 1

    # Required top-level keys
    for key in ("meta", "overview", "dashboard_tasks", "product_tasks", "agents", "timeline"):
        if key not in data:
            failures.append(f"missing key: {key}")

    # Counts must match canonical Task Board
    if len(data.get("dashboard_tasks", [])) != 10:
        failures.append(f"dashboard_tasks count != 10 (got {len(data.get('dashboard_tasks', []))})")
    if len(data.get("product_tasks", [])) != 13:
        failures.append(f"product_tasks count != 13 (got {len(data.get('product_tasks', []))})")

    # Authorization boundary
    auth = data.get("meta", {}).get("authorization", {})
    if auth.get("dashboard_build") != "AUTHORIZED":
        failures.append("dashboard_build must be AUTHORIZED")
    if auth.get("product_build") != "NOT AUTHORIZED":
        failures.append("product_build must be NOT AUTHORIZED")

    # Go must be present and ACK'd
    go = next((a for a in data.get("agents", []) if a.get("name", "").startswith("Go")), None)
    if not go:
        failures.append("Go agent missing from agents list")
    elif "ACK" not in go.get("status", "").upper() and "IN_PROGRESS" not in go.get("status", "").upper():
        failures.append(f"Go status does not show ACK/IN_PROGRESS: {go.get('status')}")

    # No task should claim product BUILD is authorized
    for t in data.get("product_tasks", []):
        if t["id"] in ("W117-T009", "W117-T010", "W117-T011", "W117-T013"):
            if "NOT AUTHORIZED" not in t.get("status", ""):
                failures.append(f"{t['id']} must remain NOT AUTHORIZED")

    # Timeline non-empty
    if len(data.get("timeline", [])) < 3:
        failures.append("timeline too short")

    if failures:
        print("FAIL — snapshot integrity")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("PASS — snapshot integrity")
    print(f"  dashboard_tasks = {len(data['dashboard_tasks'])}")
    print(f"  product_tasks   = {len(data['product_tasks'])}")
    print(f"  agents          = {len(data['agents'])}")
    print(f"  timeline        = {len(data['timeline'])}")
    print(f"  dashboard_build = {auth.get('dashboard_build')}")
    print(f"  product_build   = {auth.get('product_build')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

