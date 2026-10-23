#!/usr/bin/env python3
"""Work 51 demo: run the A2A Coder-Tester pipeline end-to-end over HTTP.

Starts a Coder Agent server and a Tester Agent server on ephemeral local
ports, then drives three scenarios through the orchestrator:

  1. correct      -> expect PASS on first verify
  2. seeded_bug   -> expect FAIL -> feedback -> fix -> PASS
  3. always_bug   -> expect BLOCKED after max_fix_rounds (2)

Evidence (JSONL) is written to ./evidence_runs/<timestamp>/.

Run:  python 03_CODE/run_demo.py   (from the Work 51 root)
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))

from a2a_ct.a2a import A2AClient, A2AServer                 # noqa: E402
from a2a_ct.coder_agent import CoderBackend                  # noqa: E402
from a2a_ct.contract import make_demo_contract              # noqa: E402
from a2a_ct.evidence import EvidenceLog                     # noqa: E402
from a2a_ct.orchestrator import run_pipeline                # noqa: E402
from a2a_ct.tester_agent import TesterBackend               # noqa: E402

SCENARIOS = [
    ("correct", "PASS"),
    ("seeded_bug", "PASS"),
    ("always_bug", "BLOCKED"),
]


def main() -> int:
    run_dir = Path(__file__).resolve().parent / "evidence_runs" / time.strftime("%Y%m%dT%H%M%SZ")
    run_dir.mkdir(parents=True, exist_ok=True)
    evidence = EvidenceLog(run_dir / "evidence.jsonl")

    summary: list[tuple[str, str, str]] = []
    for mode, expected in SCENARIOS:
        coder_server = A2AServer(CoderBackend())
        tester_server = A2AServer(TesterBackend())
        coder_server.start()
        tester_server.start()
        try:
            coder = A2AClient(coder_server.base_url)
            tester = A2AClient(tester_server.base_url)
            print(f"coder card: {coder.agent_card().get('name')}  at {coder_server.base_url}")
            print(f"tester card: {tester.agent_card().get('name')}  at {tester_server.base_url}")
            contract = make_demo_contract(coder_mode=mode, contract_id=f"WORK51-DEMO-{mode}")
            report = run_pipeline(contract, coder, tester, evidence)
            print(report.summary())
            verdict_text = "verdict: " + str((report.verdict or {}).get("verdict"))
            print(f"    expected={expected} rounds_used={report.rounds_used} {verdict_text}")
            summary.append((mode, expected, report.status))
        finally:
            coder_server.stop()
            tester_server.stop()

    print("\n--- demo summary ---")
    ok = True
    for mode, expected, actual in summary:
        mark = "OK " if expected == actual else "!! "
        ok = ok and (expected == actual)
        print(f"{mark}{mode:<12} expected={expected:<8} actual={actual}")
    print(f"evidence: {evidence.path}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
