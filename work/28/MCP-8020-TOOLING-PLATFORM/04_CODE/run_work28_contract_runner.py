#!/usr/bin/env python3
"""WORK 28 - WP6 DETERMINISTIC CONTRACT TEST RUNNER.

Runs the canonical Work 28 local contract command:

    python -m unittest discover -s 05_TEST -t . -v

from the Work 28 sandbox root, captures full stdout/stderr, exit code and
test counters, writes machine-readable (JSON) and human-readable (Markdown)
evidence, verifies readback, and exits non-zero on any required failure.

Contract rules enforced (WORK_28_TEST_PLAN.md rev 1.2):
- exit code 0 ALONE is not PASS: at least 1 test must have run.
- a green process with zero discovered tests is FAILURE.
- non-zero exit code, or failures/errors > 0, is FAILURE.
- timeout / capture failure is BLOCKED, never promoted to PASS.

Security rules:
- no arbitrary shell: only the canonical unittest command is executed,
  constructed as an argv list (no shell=True).
- bounded timeout (default 600s); no secrets captured or logged.
- evidence written only under the sandbox 06_EVIDENCE directory.

Usage:
    python 04_CODE/run_work28_contract_runner.py [--root PATH] [--timeout SECONDS]

--root defaults to the parent directory of this file (the Work 28
sandbox root containing 05_TEST/ and 06_EVIDENCE/).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone

RUNNER_VERSION = "1.0.0"
CANONICAL_COMMAND = [
    sys.executable, "-m", "unittest", "discover",
    "-s", "05_TEST", "-t", ".", "-v",
]
DEFAULT_TIMEOUT_SECONDS = 600

PASS = "PASS"
FAIL = "FAIL"
BLOCKED = "BLOCKED"

_RAN_RE = re.compile(r"^Ran (\d+) tests? in ", re.MULTILINE)
_FAILED_RE = re.compile(r"^FAILED \(([^)]*)\)", re.MULTILINE)
_FAILED_PLAIN_RE = re.compile(r"^FAILED\b", re.MULTILINE)
_OK_RE = re.compile(r"^OK\b", re.MULTILINE)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_request_id() -> str:
    rid = "W28-RUN-" + uuid.uuid4().hex[:16]
    if not all(32 <= ord(c) < 127 for c in rid):
        raise ValueError("non-ascii request id generated")
    return rid


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_unittest_output(text: str) -> dict:
    """Parse unittest -v output into counters. Never raises."""
    parsed = {
        "tests_run": 0,
        "failures": 0,
        "errors": 0,
        "skipped": 0,
        "ok_line_found": False,
        "failed_line_found": False,
        "parse_error": None,
    }
    try:
        m = _RAN_RE.search(text)
        if m:
            parsed["tests_run"] = int(m.group(1))
        m = _FAILED_RE.search(text)
        if m:
            parsed["failed_line_found"] = True
            for part in m.group(1).split(","):
                part = part.strip()
                if part.startswith("failures="):
                    parsed["failures"] = int(part.split("=", 1)[1])
                elif part.startswith("errors="):
                    parsed["errors"] = int(part.split("=", 1)[1])
                elif part.startswith("skipped="):
                    parsed["skipped"] = int(part.split("=", 1)[1])
        elif _FAILED_PLAIN_RE.search(text):
            # FAILED without a counter summary: unknown counters, at least 1 bad.
            parsed["failed_line_found"] = True
            parsed["failures"] = 1
        if _OK_RE.search(text):
            parsed["ok_line_found"] = True
    except Exception as exc:  # defensive: parsing must never crash the runner
        parsed["parse_error"] = str(exc)
    return parsed


def decide_status(exit_code, parsed, timeout_hit=False) -> str:
    """PASS requires real evidence: >=1 test, 0 failures, 0 errors, exit 0."""
    if timeout_hit:
        return BLOCKED
    if exit_code is None or exit_code != 0:
        return FAIL
    if parsed.get("parse_error"):
        return BLOCKED
    if parsed.get("tests_run", 0) < 1:
        # Green process with zero discovered tests is FAILURE (test plan s.1).
        return FAIL
    if parsed.get("failures", 0) > 0 or parsed.get("errors", 0) > 0:
        return FAIL
    return PASS


def summarize_verdict(status, exit_code, parsed) -> str:
    if status == PASS:
        return ("Contract tests passed: exit_code=0, tests_run={0}, failures=0, errors=0."
                .format(parsed.get("tests_run", 0)))
    if status == BLOCKED:
        return "Runner could not obtain trustworthy test evidence (timeout or parse failure). No PASS claimed."
    if parsed.get("tests_run", 0) < 1:
        return ("FAILURE: process exited {0} but zero tests were discovered; "
                "a green run with no tests does not satisfy acceptance.".format(exit_code))
    return ("FAILURE: exit_code={0}, tests_run={1}, failures={2}, errors={3}."
            .format(exit_code, parsed.get("tests_run", 0), parsed.get("failures", 0),
                    parsed.get("errors", 0)))


def _safe_join(root, *parts):
    """Containment-checked join: reject absolute/traversal paths."""
    rel = os.path.join(*parts)
    norm = rel.replace("\\", "/")
    if os.path.isabs(rel) or ".." in norm.split("/"):
        raise ValueError("refusing non-relative evidence path: %r" % rel)
    return os.path.join(root, rel)


def run_canonical_tests(root, timeout):
    """Execute the canonical command inside the sandbox root. No shell, bounded timeout."""
    try:
        proc = subprocess.run(
            CANONICAL_COMMAND,
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return {
            "command": " ".join(CANONICAL_COMMAND),
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "timeout_hit": False,
            "spawn_error": None,
        }
    except subprocess.TimeoutExpired as exc:
        def _s(x):
            return x.decode("utf-8", "replace") if isinstance(x, bytes) else (x or "")
        return {
            "command": " ".join(CANONICAL_COMMAND),
            "exit_code": None,
            "stdout": _s(exc.stdout),
            "stderr": _s(exc.stderr),
            "timeout_hit": True,
            "spawn_error": "timeout after %ss" % timeout,
        }
    except Exception as exc:
        return {
            "command": " ".join(CANONICAL_COMMAND),
            "exit_code": None,
            "stdout": "",
            "stderr": "",
            "timeout_hit": False,
            "spawn_error": str(exc),
        }


FENCE = chr(96) * 3


def build_markdown(payload, verdict):
    lines = [
        "# WORK 28 - AUTOMATIC CONTRACT TEST RUN EVIDENCE",
        "",
        "- Runner: run_work28_contract_runner.py v{0}".format(payload["runner_version"]),
        "- request_id: {0}".format(payload["request_id"]),
        "- recorded_at (UTC): {0}".format(payload["recorded_at_utc"]),
        "- canonical command: {0}".format(payload["command"]),
        "- exit_code: {0}".format(payload["exit_code"]),
        "- tests_run: {0} / failures: {1} / errors: {2} / skipped: {3}".format(
            payload["counters"]["tests_run"], payload["counters"]["failures"],
            payload["counters"]["errors"], payload["counters"]["skipped"]),
        "- STATUS: {0}".format(payload["status"]),
        "- verdict: {0}".format(verdict),
        "- readback: json_ok={0} md_ok={1}".format(
            payload["readback"]["json_ok"], payload["readback"]["md_ok"]),
        "- json_sha256: {0}".format(payload["readback"]["json_sha256"]),
        "- md_sha256: {0}".format(payload["readback"]["md_sha256"]),
        "",
        "## stdout",
        "",
        FENCE,
        payload["stdout"],
        FENCE,
        "",
        "## stderr",
        "",
        FENCE,
        payload["stderr"],
        FENCE,
        "",
    ]
    return "\n".join(lines)


def write_and_readback(root, evidence_dir_rel, stem, payload, md_text):
    """Write JSON + MD evidence, then read both back and verify SHA-256."""
    evidence_dir = _safe_join(root, *evidence_dir_rel.split("/"))
    os.makedirs(evidence_dir, exist_ok=True)
    json_path = os.path.join(evidence_dir, stem + ".json")
    md_path = os.path.join(evidence_dir, stem + ".md")

    json_text = json.dumps(payload, indent=2, ensure_ascii=True, sort_keys=True)
    with open(json_path, "w", encoding="utf-8") as fh:
        fh.write(json_text)
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(md_text)

    readback = {"json_ok": False, "md_ok": False,
                "json_sha256": None, "md_sha256": None}
    try:
        with open(json_path, "r", encoding="utf-8") as fh:
            rb = fh.read()
        readback["json_ok"] = (rb == json_text)
        readback["json_sha256"] = sha256_text(rb)
    except Exception:
        pass
    try:
        with open(md_path, "r", encoding="utf-8") as fh:
            rb = fh.read()
        readback["md_ok"] = (rb == md_text)
        readback["md_sha256"] = sha256_text(rb)
    except Exception:
        pass
    return readback


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    default_root = os.path.dirname(here)
    parser = argparse.ArgumentParser(description="Work 28 WP6 deterministic contract test runner")
    parser.add_argument("--root", default=default_root,
                        help="Work 28 sandbox root (contains 05_TEST/ and 06_EVIDENCE/)")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--evidence-dir", default="06_EVIDENCE",
                        help="evidence directory relative to --root")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    if not os.path.isdir(os.path.join(root, "05_TEST")):
        print("BLOCKED: no 05_TEST directory under root: %s" % root, file=sys.stderr)
        return 3

    request_id = new_request_id()
    started = time.time()
    result = run_canonical_tests(root, args.timeout)
    combined = result["stdout"] + "\n" + result["stderr"]
    parsed = parse_unittest_output(combined)
    if result["spawn_error"] and not result["timeout_hit"]:
        status = BLOCKED
    else:
        status = decide_status(result["exit_code"], parsed, result["timeout_hit"])
    verdict = summarize_verdict(status, result["exit_code"], parsed)
    if result["spawn_error"]:
        verdict = "BLOCKED: %s" % result["spawn_error"]

    stem = "W28_CONTRACT_RUN_{0}_{1}".format(
        datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"), request_id)
    payload = {
        "runner_version": RUNNER_VERSION,
        "request_id": request_id,
        "recorded_at_utc": utc_now_iso(),
        "command": result["command"],
        "exit_code": result["exit_code"],
        "timeout_seconds": args.timeout,
        "duration_seconds": round(time.time() - started, 3),
        "counters": parsed,
        "status": status,
        "readback": {"json_ok": False, "md_ok": False, "json_sha256": None, "md_sha256": None},
        "stdout": result["stdout"],
        "stderr": result["stderr"],
    }
    md_text = build_markdown(payload, verdict)
    write_and_readback(root, args.evidence_dir, stem, payload, md_text)
    # Second pass with readback fields recorded, then final verification.
    md_text = build_markdown(payload, verdict)
    readback2 = write_and_readback(root, args.evidence_dir, stem, payload, md_text)
    payload["readback"] = readback2
    readback_ok = bool(readback2["json_ok"] and readback2["md_ok"])

    if not readback_ok:
        print("BLOCKED: evidence readback verification failed; no PASS claimed.", file=sys.stderr)

    print("request_id: {0}".format(request_id))
    print("status: {0}".format(status))
    print("exit_code: {0}".format(result["exit_code"]))
    print("counters: {0}".format(json.dumps(parsed, sort_keys=True)))
    print("verdict: {0}".format(verdict))
    print("evidence: {0}/{1}.json (+ .md)".format(args.evidence_dir, stem))
    print("readback_ok: {0}".format(readback_ok))

    if status == PASS and readback_ok:
        return 0
    if status == BLOCKED or not readback_ok:
        return 3
    return 1


if __name__ == "__main__":
    sys.exit(main())