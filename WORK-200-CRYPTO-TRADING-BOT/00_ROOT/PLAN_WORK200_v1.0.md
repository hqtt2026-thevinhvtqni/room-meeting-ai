# PLAN WORK 200 v1.0 — Crypto Trading Bot

**Status:** ACTIVE / P0  
**Owner:** HQTT ROOM project coordination  
**Created:** 2026-10-24  
**Execution principle:** PLAN → BUILD → VERIFY; evidence required for every PASS.

## P0 — Requirements and interfaces
- [ ] Confirm data source/exchange and permitted API access.
- [ ] Choose initial symbols, candle timeframe, and historical-data period.
- [ ] Define baseline strategy as an experimental benchmark, not a profit promise.
- [ ] Define fee, spread/slippage, risk, and drawdown assumptions.
- [ ] Inspect available Sandbox runtime and installed dependencies.
- [ ] Freeze contracts for market data, strategy signals, portfolio, orders, and reports.

**Exit criteria:** approved requirements/config schema, explicit non-goals, dependency/runtime evidence, and testable acceptance criteria.

## P1 — Safe simulation core
- [ ] Implement validated market-data models.
- [ ] Implement strategy protocol and baseline example.
- [ ] Implement portfolio accounting and risk checks.
- [ ] Implement paper-only order simulator.
- [ ] Implement kill switch and structured event logging.

**Exit criteria:** deterministic unit tests; risk limits and paper-only boundary proven by tests.

## P2 — Backtesting and reporting
- [ ] Implement chronological event-driven backtesting.
- [ ] Apply fees and slippage.
- [ ] Prevent look-ahead leakage; separate train/validation/test periods.
- [ ] Report return, drawdown, volatility, turnover, costs, exposure, and benchmark.

**Exit criteria:** reproducible run with config/data fingerprint and complete report.

## P3 — Independent verification
- [ ] Unit, integration, and failure-path tests.
- [ ] Verify malformed data, exchange/data outage, rejected order, stale prices, risk-limit hit, and kill-switch scenarios.
- [ ] Run tests in the actual Sandbox environment and capture outputs.
- [ ] Review dependencies and secret handling.

**Exit criteria:** test evidence attached; no critical unresolved safety defects.

## P4 — Paper-trading observation
- [ ] Run simulated live market feed or replay.
- [ ] Compare expected vs actual paper fills and log divergence.
- [ ] Review stability, risk behavior, and operational alerts.

**Exit criteria:** defined observation window completed with evidence and a written decision.

## Out of scope until a separate explicit decision
- Real-money order execution, withdrawals, or custody.
- Claims of guaranteed or reliably predictable profit.
- Storing credentials in the repository.
- Deployment with unrestricted exchange permissions.

## Decision gates
- **Necessary conditions:** runtime/dependencies known, data contract defined, risk policy specified, tests executable.
- **Sufficient conditions:** all acceptance criteria for a phase pass with evidence and review.
- No phase is PASS solely because code or documents exist.

## Registered extension (2026-10-24): BaoXtra BX42MR V4.2.8
- Refer to `02_EXTENSION/BaoXtra_BX42MR_V4_2_8/README.md`, `IMPORT_RECORD.md`, `WORK200_BX428_INTEGRATION_PLAN.md`, and `TEST_CHECKLIST.md`.
- Full source is retained in user Library, not wholly transferred to Sandbox through MCP 8030.
- Preserve paper-only boundary and core P0-P4 gates; no PASS/Live authorization implied.

## MT5 Swing Semi-Auto v0.1 reference extension (2026-10-24)
- MQL5 review-only port registered at `02_EXTENSION/BaoXtra_BX42MR_V4_2_8/MT5_PORT_V0_1/`.
- Full .mq5 source, .set preset, README, source contract tests, parity matrix and evidence copied into Sandbox and verified against Library originals.
- Static 7/7 local tests passed; no terminal compiler or actual Strategy Tester acceptance.
- This is a partial M15 Swing signal/Entry/SL/TP visualization port, not a 1:1 Pine conversion or MT5 mobile EA.
- Paper-only Work 200 Python core remains unchanged. No auto broker orders or LIVE permission.
- Gate for next phase: MetaEditor F7 compile, demo Strategy Tester visual replay, original Pine parity audit and logs, risk/position safeguards before any order adapter.

## Full MT5 conversion specification (2026-10-24)
- Baseline: Pine BX42MR V4.2.8 (1758 lines, SHA256 2cb18bd304a6951c2ffc7fea70a6510bfa5f4b07cc1b985b793201369e27bf3a) and review-only MT5 V0.1 (517 lines) are immutable comparison references.
- Exact source scope: 179 Pine input declarations in 14 parameter groups, 2 independent strategy engines and optional Swing confluence; previous V0.1 is PARTIAL.
- New specification under 02_EXTENSION/BaoXtra_BX42MR_V4_2_8/MT5_FULL_PORT_V1/: MASTER_IMPLEMENTATION_PLAN.md, FEATURE_PARITY_MATRIX.md, ACCEPTANCE_GATES.md, DEV_SEQUENCE_AND_MODES.md, PINE_INPUTS_001_090.tsv and PINE_INPUTS_091_179.tsv.
- These files specify work; they are NOT a compiled or completed full MT5 port. Follow gates: input freeze -> SMC -> Momentum -> risk/ledger/exits -> dashboard -> parity -> demo proof.
- Demo/paper-first, no real-money broker execution, no automatic permission escalation. Manual trade confirmation must remain explicit.
