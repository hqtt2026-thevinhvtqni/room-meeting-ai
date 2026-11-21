"""
Work 10 — test runner + evidence writer (Gate 4)

Runs every offline/HTTP suite in a fresh subprocess, captures the output, hashes
the sources under test, and writes a JSON evidence file into 06_EVIDENCE.

It never claims a browser result: the real Chromium E2E is reported as
NOT RUN unless the host evidence files already exist.

Usage:  python 05_TEST/run_all_tests.py [--evidence-dir PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "05_TEST"
SUITES = [
    ("offline_contract_p0_p5", "test_p0_p5.py"),
    ("safety_policy_negative", "test_safety_policy.py"),
    ("http_api", "test_http.py"),
    ("process_containment", "test_process_containment.py"),
    ("host_operations", "test_host_operations.py"),
    ("acceptance_validator", "test_acceptance_validator.py"),
    ("dashboard_contract", "test_dashboard_contract.py"),
]
HASH_GLOBS = [
    "04_CODE/*.py", "04_CODE/*.md", "05_TEST/*.py", "05_TEST/*.html",
    "05_TEST/*.md", "05_TEST/evidence.txt", "08_DASHBOARD/*.html",
    "08_DASHBOARD/*.md", "03_ARCHITECTURE/*.md", "00_ROOT/*.md",
    "README.md", "07_RELEASE/*.md", ".github/workflows/*.yml",
    "10_AI_DEBUG_HANDOFF/**/*.md",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def hash_sources() -> dict:
    manifest = {}
    for pattern in HASH_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            if "__pycache__" in str(path):
                continue
            manifest[str(path.relative_to(ROOT)).replace("\\", "/")] = hashlib.sha256(
                path.read_bytes()).hexdigest()
    return manifest


def run_suite(name: str, script: str, evidence_dir: Path) -> dict:
    started = utc_now()
    proc = subprocess.run(
        [sys.executable, str(TEST_DIR / script)],
        cwd=str(ROOT), capture_output=True, text=True, timeout=300,
    )
    output = (proc.stdout or "") + (proc.stderr or "")
    passed = output.count("  PASS  ")
    failed = output.count("  FAIL  ")
    skipped = output.count("  SKIP  ")
    tail = [line for line in output.splitlines() if line.strip()][-12:]
    log_dir = evidence_dir / "test-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{name}.log"
    log_path.write_text(output, encoding="utf-8")
    failure_lines = [line for line in output.splitlines()
                     if "  FAIL  " in line or "Traceback" in line or "AssertionError" in line]
    return {
        "suite": name,
        "script": f"05_TEST/{script}",
        "exit_code": proc.returncode,
        "checks_passed": passed,
        "checks_failed": failed,
        "checks_skipped": skipped,
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "started_at": started,
        "finished_at": utc_now(),
        "output_lines": len(output.splitlines()),
        "output_tail": tail,
        "output_failures": failure_lines,
        "output_log": str(log_path.relative_to(evidence_dir)).replace("\\", "/"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", default=str(ROOT / "06_EVIDENCE"))
    args = parser.parse_args()

    evidence_dir = Path(args.evidence_dir).resolve()
    evidence_dir.mkdir(parents=True, exist_ok=True)
    results = [run_suite(name, script, evidence_dir) for name, script in SUITES]
    total_pass = sum(r["checks_passed"] for r in results)
    total_fail = sum(r["checks_failed"] for r in results)
    total_skipped = sum(r.get("checks_skipped", 0) for r in results)
    suites_ok = all(r["status"] == "PASS" for r in results)

    host_result = evidence_dir / "real-browser-e2e-result.json"
    host_shot = evidence_dir / "real-browser-e2e.png"
    host_e2e = "NOT RUN"
    if host_result.exists() and host_shot.exists():
        try:
            host_payload = json.loads(host_result.read_text(encoding="utf-8"))
            host_e2e = host_payload.get("status", "INVALID")
            if host_e2e not in ("PASS", "FAIL", "BLOCKED"):
                host_e2e = "INVALID"
        except (OSError, json.JSONDecodeError):
            host_e2e = "INVALID"

    payload = {
        "work_id": "10",
        "work_name": "COMPUTER-AGENT",
        "generated_at": utc_now(),
        "timezone_note": "all timestamps are UTC (Z)",
        "runner": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "script": "05_TEST/run_all_tests.py",
        },
        "scope": {
            "offline": "agent contracts, safety policy enforcement, HTTP API (deterministic adapter double)",
            "not_covered": [
                "real Chromium/Playwright behaviour",
                "physical Windows 10 PC execution and local ACL/Chrome profile validation",
                "Linux cgroup-v2 production containment",
            "production validator HMAC key and pinned-hash provisioning on Owner PC",
                "integrated ROOM-HOP E2E",
                "P4 dashboard behaviour in a real browser",
            ],
        },
        "summary": {
            "suites": len(results),
            "suites_passed": sum(1 for r in results if r["status"] == "PASS"),
            "checks_passed": total_pass,
            "checks_failed": total_fail,
            "checks_skipped": total_skipped,
            "overall": "PASS" if suites_ok and total_fail == 0 else "FAIL",
            "host_chromium_e2e": host_e2e,
            "release_gate": "NOT READY (physical Windows 10 validation, V8 semantic validator, Linux cgroup-v2 and ROOM-HOP integration remain open)",
        },
        "suites": results,
        "source_hashes_sha256": hash_sources(),
    }

    evidence_dir = Path(args.evidence_dir)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    out = evidence_dir / "offline-test-evidence.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=" * 58)
    for result in results:
        print(f"{result['status']:4}  {result['suite']:24} "
              f"{result['checks_passed']} passed, {result['checks_failed']} failed")
    print("=" * 58)
    print(f"Total: {total_pass} passed, {total_fail} failed, {total_skipped} skipped")
    print(f"Host Chromium E2E: {host_e2e}")
    print(f"Evidence: {out}")
    return 0 if payload["summary"]["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
