# WORK 200 — MASTER IMPLEMENTATION PLAN v1.0
**Project:** CRYPTO-TRADING-BOT  
**Plan ID:** WORK200-MASTER-PLAN-V1.0  
**Date:** 2026-10-25 (ICT)  
**Prepared by:** Xu — AI-01 / HQTT Coordinator  
**Audience:** Cla (AI-03 / CTO), BX (Coder), Qw (Independent QA), An (Tester)  
**Status:** OFFICIAL CONSOLIDATED PLAN — READY FOR CODER TASKING; NOT A RELEASE APPROVAL  
**Operating model:** PLAN → BUILD → VERIFY. Evidence First. Necessary Conditions + Sufficient Acceptance Conditions.  
**Scope boundary:** Finish the current Work 200 foundation in controlled stages. Do not expand scope or enable live trading.

---

## 1. Mission and intended outcome

Build a maintainable, testable trading research system with a Python paper-trading core, reproducible backtesting, safe review-only ingestion of BX42MR V4.2.8 signals, operational dashboard backed by truthful read-only APIs, and a separately gated MT5 port track.

The system must keep these permissions separate:
1. **Signal:** strategy may describe a possible setup; it cannot authorize an order.
2. **Risk decision:** risk engine independently accepts, warns, or blocks a proposed paper action.
3. **Paper execution:** simulator records only simulated fills and costs.
4. **MT5 manual/demo:** separate extension, gated by compile, replay, parity, and explicit human approval.
5. **Live trading:** prohibited in this plan. Requires a new explicit decision and independent safety/security review.

No profit guarantee, no withdrawals/custody, no credentials in source, and no UI toggle may grant execution authority.

## 2. Evidence-based baseline (2026-10-25)

### Present in Work 200 Sandbox
- Python package under `04_CODE/crypto_bot`: models, data validation, strategy, risk, paper broker and signal intake.
- Baseline moving-average crossover; paper broker models fills, fees and slippage without exchange order submission.
- Dashboard static prototype; current financial values and controls are mock/local-only.
- BX42MR V4.2.8 Pine source and reference/integration docs.
- BX42MR signal intake is REVIEW_ONLY; raw Pine alert formats are not directly compatible with the strict typed parser.
- MT5 Swing Semi-Auto v0.1 MQL5 source, preset, docs and static source-contract tests.
- MT5_FULL_PORT_V1 design specification: input manifests, parity matrix, architecture, acceptance gates and sequence.

### Evidence available but limited
- 27/27 signal-intake tests reported on local Python 3.13.5 / pytest 9.0.2.
- 7/7 MT5 source-contract tests reported locally.
- Pine source SHA-256 recorded as `2cb18bd304a6951c2ffc7fea70a6510bfa5f4b07cc1b985b793201369e27bf3a`.
- These do not prove the full project passes. The core test suite and end-to-end pipeline have not been verified in the target Sandbox runtime.

### Known gaps/blockers
- Target Sandbox MCP tools currently available to Xu expose file operations but no code-execution command; test execution requires an authorized execution host. Do not simulate a run or label tests PASS without real output.
- BTCUSDT / OKX / SPOT / 15m intake test profile conflicts with BX42's initial XAUUSD CFD / Swing D1-H4-H1-M15 visual-test profile. Profiles must be explicitly separated.
- No durable idempotency/replay store; current deduplication is in-memory.
- No verified end-to-end chain from BX42 alert → validation → independent risk decision → paper broker → audit/report.
- Backtest/reporting gate is not complete or verified.
- Dashboard has no verified backend connection; stop control is not a real kill switch.
- MT5 v0.1 is partial and review-only; MetaEditor compilation, terminal replay, parity and demo acceptance are not evidenced. Full MT5 port is a specification, not completed implementation.

## 3. Architecture and non-negotiable contracts

### 3.1 Data flow
Market data / replay → data validation → strategy signal → normalized event → risk decision → paper broker → portfolio/accounting → audit log/report → read-only dashboard API.

A signal cannot bypass validation or risk. A dashboard cannot create or approve trades. MT5 stays a separate extension and cannot be silently merged into the Python paper core.

### 3.2 Signal contract
Define a versioned normalized event containing at minimum:
- stable `event_id`, `trace_id`, strategy and strategy version;
- venue/exchange, market type, canonical symbol, timeframe;
- UTC event time and candle-close time, explicit closed-bar evidence;
- event type and side; entry, stop, targets and quantity/units where applicable;
- source identifier/authentication metadata and validation status;
- execution mode and paper-only policy, with server-side policy authoritative rather than trusting client flags.

Handle `BX421|MANUAL_REVIEW` and `BX42_MR|MANUAL_REVIEW` as separate review-only formats. Keep `BACKTEST_AUTO`, `BACKTEST_ADD`, `PAPER`, `PAPER_ONLY|SL_UPDATE`, exits and other event types distinct. Never turn an SL_UPDATE, backtest event, or unknown event into a BUY/SELL entry. Missing/ambiguous metadata fails closed.

### 3.3 Market profiles
Use independent configuration profiles; do not mix datasets, contract assumptions or results:
- **CORE_BASELINE:** generic OHLCV / moving-average research profile.
- **CRYPTO_SPOT_TEST:** BTCUSDT / OKX / SPOT / 15m only as a parser-test profile until venue data and contract settings are independently verified.
- **BX42_XAUUSD_REFERENCE:** XAUUSD CFD reference, Swing mode, optional D1/H4/H1/M15 confluence; closed HTF bars only. It is not crypto spot.
- **MT5_BX42:** separate terminal-specific port with broker symbol specs and its own acceptance gates.

Each profile must specify data source, symbol/contract, timeframe, timezone, session/calendar rules, fee/spread/slippage, tick/lot/quantity steps, risk limits, and source/config version. Unknown values block a run.

### 3.4 Risk and execution boundaries
- Default state is NO TRADE until data, signal and risk checks pass.
- Risk result is explicit: APPROVE_PAPER / WARN_REVIEW / BLOCK, with versioned rule ID and reason.
- WARN requires human review; BLOCK is non-overridable in this milestone.
- Enforce exposure/order notional, daily loss/drawdown, quantity normalization, symbol contract details, spread and stale-data guards where relevant, and kill switch.
- Paper broker must be demonstrably incapable of live exchange order submission.
- Persistent event idempotency must survive process restart and reject duplicate/replay events.
- No credentials or secrets in source, fixtures, reports or logs.

## 4. Work packages and execution order

### WP0 — Plan/configuration freeze (Cla owns plan; BX supplies source details)
**Tasks**
1. Freeze scope, module boundaries and data contracts.
2. Define configuration schema and the four independent profiles above.
3. Inventory dependencies and identify the authorized execution environment for tests.
4. Map each requirement to test(s), evidence path and owner.
**Dependencies:** none.
**Exit:** approved schema, profile configs, runtime/dependency evidence, traceable acceptance matrix. No implementation gate passes by documentation alone.

### WP1 — Verify and stabilize the existing Python core (BX; An tests; Qw reviews)
**Tasks**
1. Inspect `models.py`, `data_validation.py`, `strategy.py`, `risk.py`, `paper_broker.py`, `signal_intake.py` and existing tests.
2. Add/fix tests for timezone-aware candles, OHLC constraints, duplicate/out-of-order/missing data, deterministic strategy, fees/slippage, exposure/daily-loss limits and kill switch.
3. Prove paper broker has no live network/order path.
4. Execute tests on an authorized Python host; record exact command, runtime/dependency versions, exit code and pass/fail/blocked.
**Dependencies:** WP0 contracts and execution-host decision.
**Exit:** all applicable core tests pass in the declared environment; no critical safety defects; reproducible evidence stored in `06_EVIDENCE`.

### WP2 — BX42 alert review-only adapter and durable idempotency (BX; Qw independent review)
**Tasks**
1. Implement separate parsers for the documented BX421 and BX42_MR MANUAL_REVIEW envelopes; preserve event type distinctions.
2. Validate source metadata, timestamps, confirmed/closed bars, strategy version, profile, symbol/venue/market, price relationships, units and expiry.
3. Reject malformed, incomplete, unknown, stale, future-dated, unauthenticated, replayed or mismatched-profile events.
4. Add durable idempotency store with explicit retention/transaction behavior; test duplicate delivery and process restart.
5. Keep all accepted adapter output REVIEW_ONLY until WP3 is complete.
6. Never infer authenticated source solely from user-provided JSON flags. If authenticated transport/source provenance is not available, keep the adapter local/offline review-only.
**Dependencies:** WP0 contract; WP1 stable model/data validation.
**Exit:** parser contract tests and failure-path tests pass; all raw alert variants are classified; no event can directly place an order.

### WP3 — Paper-only end-to-end pipeline (BX; An tests; Qw reviews)
**Tasks**
1. Connect normalized event → data integrity → strategy/profile validation → risk decision → paper broker → portfolio/accounting → audit trail.
2. Ensure the risk engine is the sole gate for paper proposals; signals never create fills directly.
3. Simulate fill price, spread, fees, slippage, rejection and partial-fill behavior only to the extent explicitly implemented and tested.
4. Add deterministic audit records including trace/event ID, config/risk policy version, reject reason and simulated fill status.
5. Test restart/replay, stale signal, rejected risk, invalid SL/TP, kill switch and broker failure.
**Dependencies:** WP1 and WP2.
**Exit:** reproducible integration tests prove both accepted and blocked paths; no live execution route exists; audit trail ties input to final paper outcome.

### WP4 — Event-driven backtest and report (BX; An tests; Qw reviews)
**Tasks**
1. Implement chronological event-driven simulation using only information available at decision time.
2. Prevent look-ahead leakage, especially for D1/H4/H1 confirmation and M15 trigger logic; use closed higher-timeframe candles only.
3. Apply configured fees, spread and slippage; disclose any unmodeled funding, margin, contract or liquidity behavior.
4. Separate train/validation/test windows and freeze dataset/config fingerprints.
5. Report total/net return, max drawdown, volatility, turnover, costs, exposure, benchmark and trade-level outcomes; include limitations.
6. Use deterministic replay with same inputs producing same result.
**Dependencies:** WP0 profile/data contract and WP1 core.
**Exit:** fixed dataset + config fingerprint + command + report + tests reproducibly demonstrate no look-ahead and cost handling. Do not make profitability claims from an unvalidated sample.

### WP5 — Dashboard read-only integration (BX; An/browser QA; Qw reviews)
**Tasks**
1. Keep existing mock UI clearly labeled until APIs are connected.
2. Implement/read the agreed read-only endpoints: `GET /api/dashboard/summary`, `GET /api/market/watchlist`, `GET /api/paper-trades?limit=...`, `GET /api/risk/status`, `GET /api/backtests/latest`.
3. Include source, timestamp, freshness/status metadata in each response.
4. Show loading, stale, unavailable and error states; never replace missing live/backend data with plausible fake values silently.
5. Do not present the UI stop control as a real kill switch until authenticated, connected to risk engine, audited and failure-tested.
6. Perform actual browser checks on desktop and mobile viewport; record results.
**Dependencies:** WP3 API/data contract; WP4 report schema where applicable.
**Exit:** browser evidence, endpoint contract tests, clear mock/real status, no trade authority in browser.

### WP6 — BX42 Pine source parity validation (BX prepares comparisons; Qw independently checks)
**Tasks**
1. Treat Pine v6 source and its recorded checksum as immutable reference; do not silently edit canonical source.
2. Obtain TradingView compile evidence and fixed test dataset/replay evidence when access is available.
3. Verify documented default modes/parameters and separate Legacy SMC, RSI Momentum and optional Swing confluence behavior; do not blend strategies into one profile.
4. Record expected/actual events and timestamped deviations. Do not claim tick-for-tick PnL parity between TradingView broker emulator and MT5 broker.
5. If TradingView access/evidence is unavailable, mark this gate BLOCKED; do not substitute a source inspection for compile/backtest.
**Dependencies:** WP0 profiles and relevant reference data; can run in parallel with WP2 once scope is frozen.
**Exit:** comparison report with source/data/config fingerprints and explicit deviations; no unsupported parity claims.

### WP7 — MT5 track, separately gated (BX; Cla architecture oversight; Qw QA)
**Stage A: v0.1 verification**
1. Compile in MetaEditor; save compiler version/output and .ex5 hash.
2. Run closed-bar visual replay on an MT5 demo/tester environment across D1/H4/H1/M15; save logs/screenshots and event timestamps.
3. Compare behavior to Pine reference and update parity matrix; list unsupported features.
4. Confirm review-only/no-order behavior and symbol/time/lot assumptions.
**Stage B: full port only after Stage A review**
5. Follow `MT5_FULL_PORT_V1/MASTER_IMPLEMENTATION_PLAN.md` dependency sequence: freeze all 179 Pine inputs → data/closed bars → Legacy SMC → RSI Momentum → zones/confluence → risk/virtual ledger → exits → dashboard/notifications → parity → demo proof.
6. Keep product variants separate; implement each selected mode from the source rather than approximate formulas to make arrows look similar.
7. Broker-aware risk must account for tick size/value, volume min/max/step, contract size, margin, stop/freeze levels, actual fills, fees and server return codes.
8. Demo-only auto testing is outside the current approval unless explicitly approved at a later gate. Live is prohibited.
**Dependencies:** source/config freeze; terminal host availability; WP6 reference evidence for parity claims.
**Exit:** selected mode compiles with zero errors; input map is complete or explicitly unsupported; deterministic parity/failure tests and demo evidence archived; human review. No auto-escalation to live.

### WP8 — Independent acceptance and handoff (Qw; An; Xu coordinates)
**Tasks**
1. Review code diff/source, tests, reports, environment details and risk controls independently.
2. Verify each acceptance item against evidence rather than implementer claims.
3. Classify each item PASS / FAIL / BLOCKED / NOT RUN with reason.
4. Produce release-readiness report, residual risks, known limitations and next decision needed.
**Dependencies:** applicable WPs complete.
**Exit:** all selected milestone criteria have evidence; no unresolved critical safety defect; explicit human decision for any scope change. Work 200 is not DONE merely because one extension passes.

## 5. Shared definition of done for every task
Each task must include:
- unique task ID, owner, inputs/dependencies and files expected to change;
- necessary conditions to start and sufficient acceptance conditions to finish;
- test command and expected result before execution;
- actual runtime/environment, dependency versions, exit code and full result after execution;
- evidence file under `06_EVIDENCE`, journal entry and limitations;
- independent QA where the gate is safety-critical.
If no authorized runtime exists, set status BLOCKED and name the missing capability. Do not create fake output, inferred PASS or claimed execution.

## 6. Global release gates
- **G0 — Requirements/contracts:** profiles, schemas, risk policy and runtime known.
- **G1 — Core safety:** validation, deterministic baseline, risk and paper-only broker proven.
- **G2 — Signal adapter:** review-only parser, provenance checks, durable idempotency and fail-closed behavior proven.
- **G3 — Paper E2E:** risk-gated simulated order lifecycle and audit trail proven.
- **G4 — Backtest:** no-look-ahead, costs, split periods, reproducible report proven.
- **G5 — Dashboard:** read-only backend and truthful freshness/error states proven.
- **G6 — BX42 parity:** only claims supported by TradingView/replay evidence.
- **G7 — MT5:** separate compile/replay/parity/demo gate.
- **G8 — Release review:** independent QA report and explicit human decision.

Gates can run in parallel only where dependencies permit; a downstream gate cannot be marked PASS if a prerequisite is BLOCKED. Passing MT5 source tests does not pass Python core; passing signal-intake tests does not pass Work 200 as a whole.

## 7. Immediate coder queue

**First priority**
1. Cla freezes task map/profile/schema and identifies authorized test execution host.
2. BX audits the current core and adds/runs the core tests on that host; no new feature expansion until baseline test status is clear.
3. BX implements review-only BX42 parsers plus persistent idempotency and tests.
4. BX integrates the paper-only end-to-end pipeline.
5. An/Qw verify as evidence becomes available; do not wait for every feature to start independent review of completed tasks.

**Then**
6. Backtest/reporting.
7. Dashboard read-only integration.
8. Pine parity evidence.
9. MT5 v0.1 compile/replay, followed by full-port stages only when authorized and prior gates pass.

## 8. Explicit non-goals for this plan
- Real-money orders, live exchange/broker API, withdrawal/custody.
- Unauthenticated webhook-to-MT5 order routing.
- Automatic conversion of Pine alerts into executable orders.
- Profit guarantees or claims based on unverified backtests.
- Blending BTC spot, perpetuals and XAUUSD CFD into one config or result.
- Treating dashboard demo controls as operational controls.
- Claiming tests run when only source inspection or local tests from a different environment exist.

## 9. References in this Work
- `00_ROOT/PLAN_WORK200_v1.0.md`
- `05_TEST/ACCEPTANCE_CRITERIA.md`
- `06_EVIDENCE/IMPLEMENTATION_STATUS_20261024.md`
- `06_EVIDENCE/WORK200_MINUTES_20261025_01.md`
- `06_EVIDENCE/WORK_JOURNAL_20261024.md`
- `02_EXTENSION/BaoXtra_BX42MR_V4_2_8/WORK200_BX428_INTEGRATION_PLAN.md`
- `02_EXTENSION/BaoXtra_BX42MR_V4_2_8/ALERT_COMPATIBILITY_CONTRACT_V01.md`
- `02_EXTENSION/BaoXtra_BX42MR_V4_2_8/MT5_FULL_PORT_V1/MASTER_IMPLEMENTATION_PLAN.md`
- `02_EXTENSION/DASHBOARD_SCOPE_AND_INTEGRATION_PLAN.md`

**Final status:** Consolidated master plan prepared and saved for coder tasking. Implementation, test execution, acceptance and release are separate gates; none are pre-approved by this document.
