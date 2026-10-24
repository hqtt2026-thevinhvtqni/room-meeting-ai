# Work 200 / BX42MR V4.2.8 — Verification record
Date: 2026-10-24
Release status: NOT APPROVED. Live execution: DISABLED.

## Verified
- Pine v6 source fully copied to 02_EXTENSION/BaoXtra_BX42MR_V4_2_8/.
- ZIP original and MCP read-back Pine SHA-256 agree:
  2cb18bd304a6951c2ffc7fea70a6510bfa5f4b07cc1b985b793201369e27bf3a
- Canonical Pine original: 1758 lines, 119280 UTF-8 bytes.
- Python signal intake and tests copied to 04_CODE and 05_TEST, respectively.
- Local test command: python -m pytest -q tests/test_signal_intake.py
- Local result: 27 passed in 0.04s (Python 3.13.5, pytest 9.0.2).
- Local compile check: python -m compileall -q crypto_bot/signal_intake.py ; no errors.

## Scope limits
- Test result pertains only to the new REVIEW_ONLY Python signal-intake module, not full Work 200.
- Tests were run in local container, not MCP 8030 Sandbox (no exposed execution tool).
- Pine source was not compiled in TradingView; no Strategy Tester evidence.
- Pine currently emits BX421 and BX42_MR pipe alerts; typed Python intake does not accept them directly.
- No authenticated bridge, durable replay prevention, paper broker integration, broker API or live orders.
- The original core test_core.py remains unverified in this evidence.
- See ALERT_COMPATIBILITY_CONTRACT_V01.md and TEST_CHECKLIST.md for next gates.
