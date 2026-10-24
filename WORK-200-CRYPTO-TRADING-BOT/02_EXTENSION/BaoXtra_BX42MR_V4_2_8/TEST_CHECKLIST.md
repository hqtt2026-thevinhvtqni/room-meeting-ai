# BX42MR V4.2.8 — Verification and acceptance checklist
Updated 2026-10-24. Mark PASS only against documented evidence.

## Confirmed
- [x] Full Pine source copied into Work 200; content SHA-256 equals original ZIP.
- [x] Local isolated Python signal intake tests: 27/27 PASS (review-only schema/guards).
- [x] Static Pine alert format inventory documented: BX421 and BX42_MR.

## Pending
- [ ] Pine v6 compiles and saves in TradingView.
- [ ] V4.2.8 filter OFF parity with V4.2.7 on same chart data/configuration.
- [ ] D1 trend direction and closed-candle condition.
- [ ] H4 OB/FVG/Fib retest/TTL without look-ahead.
- [ ] H1 confirmation rejects countertrend setups.
- [ ] M15 trigger/retest and wrong-timeframe rejection.
- [ ] Legacy SMC TP1/TP2/TP3, BE, profit-lock and partial exit behavior.
- [ ] TradingView Strategy Tester results with fees/slippage.
- [ ] Authenticated, versioned alert transport with real UTC candle-close metadata.
- [ ] Durable event dedup/replay rejection and separately typed SL_UPDATE/EXIT events.
- [ ] Venue-specific contract sizes/tick/lot/fees/funding/spread/position accounting.
- [ ] Original Python core unit/integration/failure tests executed in target runtime.
- [ ] End-to-end Python paper broker test with risk enforcement and kill switch.
- [ ] Operator review of logs, hashes and configuration fingerprint.

No live trading approval. Current REVIEW_ONLY validation never submits orders.
Evidence: 06_EVIDENCE/BX428_INTEGRATION_VERIFICATION_20261024.md.
