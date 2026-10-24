# Build order, controlled profiles and user review checkpoints
2026-10-24 | Work 200 | specification only

1. BASELINE / do not overwrite v0.1. Freeze Pine V4.2.8 and MQL5 V0.1. Generate a profile-dependent exact parameter manifest from Pine (179 input declarations). Test read-only indicator parity.
2. SMC / implement full structure engine, OB/FVG/Fib, score, locked setup, retest; test Legacy Scalping separately from Legacy Swing. Toggle optional D1-H4-H1-M15 confluence ON and OFF, preserving the default OFF.
3. MOMENTUM / independent engine on M1, D1/H1 bias and RSI M15/M5/M1, CH/BOS and CI window. Port fib confirmation by M5/M15 and swing/ATR stop.
4. ACCOUNTING / separate per-leg and portfolio ledger. Define all entry/fill/partial-exit/SL update events; true TP1 fills, 20/40/60/70 peak net-profit lock, no stop widening. Support virtual legs on netting; ticket legs on hedging.
5. RISK / broker contract/tick sizing, margin, spread, session, equity, maximum total stop loss, max trades/day, kill-switch, loss-limit recovery only by authorized human.
6. UI & MOBILE / chart boxes, ZigZag and signals; VI/EN dashboard and notifications; mobile monitor/confirmation only. No MQL5 EA executes inside MT5 iOS.
7. TEST / MetaEditor -> closed-bar deterministic replay -> Strategy Tester real ticks -> demo forward and controlled regression -> evidence-based release.

Preset cases:
- BX_LEGACY_SCALP: engine Legacy SMC; mode Scalping; selected chart lower than HTF.
- BX_LEGACY_SWING: engine Legacy SMC; mode Swing, optional D1-H4-H1-M15 filter as declared in Pine; entry M15 when enabled.
- BX_RSI_MOMENTUM: engine RSI Momentum; chart M1; D1/H1 bias and M5/M15/M1 RSI confirmation.
- BX_MANUAL_PLAN: manual Entry/SL1-3/TP1-3; no broker order.
All presets default SIGNAL_ONLY and DEMO_READ_ONLY for initial validation. Any switch to demo order placement requires explicit future approval. Real account auto order sending is not authorized.
Definition of parity: logical event, direction, price level and confirmation timing on comparable normalized history. Difference in fills, slippage, contract specs and ticks is reported separately; it is not covered up or forced to look identical.
