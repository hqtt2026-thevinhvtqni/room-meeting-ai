# BaoXtra BX42MR V4.2.8 -> MT5 Full Port V1.0
Work 200 | Architecture baseline | 2026-10-24
Status: SPECIFICATION ONLY. No claim of full implementation, terminal compilation, or strategy parity.
Safety target: demo/paper first. Signal Only default; Semi-Auto needs manual order confirmation. Live order sending NOT enabled.

## Source of truth / configuration freeze
- Source: BaoXtra_BX42MR_V4_2_8_Swing_D1_H4_H1_M15_TEST.pine, 1758 lines.
- SHA256: 2cb18bd304a6951c2ffc7fea70a6510bfa5f4b07cc1b985b793201369e27bf3a.
- Pine default: market Forex; mode Scalping; trading engine RSI Momentum; execution Signal Only; direction Both.
- The D1/H4/H1/M15 Swing confluence feature is OPTIONAL and OFF by default in Pine.
- Existing MT5 port v0.1 only approximates optional Swing D1-H4-H1-M15, has no positions/real orders, and is not 1:1 with Pine.
- Do not substitute new indicator formulas merely because a signal arrow looks similar: freeze detailed thresholds, signal state, HTF indexing and defaults from Pine.
- Required product variants: A Legacy SMC Scalping, B Legacy SMC Swing with optional 03A confluence, C RSI Momentum on M1 with D1/H1 MTF bias, D Manual level planner. Build per-engine profile presets, NOT one blended strategy.

## Component topology (proposed MQL5 source layout)
04_CODE/mt5/BaoXtra_BX42MR_Full_V1_0.mq5: EA orchestrator, callbacks and mode controller.
04_CODE/mt5/Include/BX42/
- BX42_Types.mqh : immutable Candle/Zone/Setup/Leg/Campaign/Signal types, enum profiles.
- BX42_Config.mqh : Pine parameter parity table, validation, settings/migrations.
- BX42_Data.mqh : CopyRates/CopyBuffer, symbol properties, UTC/server-time conversion, stale-data and closed-bar guards.
- BX42_Indicators.mqh : EMA9/21/34/55/144/200, RSI14, ATR14, confirmed pivots ZigZag helpers.
- BX42_Structure.mqh : pivots, sweeps, BOS, CHoCH, CISD, displacement, score.
- BX42_Zones.mqh : SMC OB/FVG/FIB generation, zone aging/TTL, invalidation/visibility and overlap controls.
- BX42_SwingMTF.mqh : D1/H4/H1/M15 optional confluence with previous CLOSED HTF bars only.
- BX42_LockedSetup.mqh : initial snapshot, wait-for-next-confirmed-bar retest, cancel, expiration, campaign state.
- BX42_Momentum.mqh : M1 RSI MTF (M1/M5/M15/H1/D1), aligned CH/BOS, CI window, cooldown, Fibonacci and momentum gates.
- BX42_Risk.mqh : lot/tick/contract normalization, stop-risk on account currency, spread, margin, session, day-DD, kill-switch.
- BX42_Campaign.mqh : L1-L3, MB1-MB3/MS1-MS3 virtual ledger, position mapping, individual realized net, costs, peak net, risk.
- BX42_Exit.mqh : actual TP1/TP2/TP3 fills, fee-aware BE, monotonic trailing stop and 20/40/60/70 percent peak-profit floor.
- BX42_PaperBroker.mqh : deterministic, no-network virtual fills incl bid/ask, spread, gaps, slippage, partial fills and rejects.
- BX42_TradeMonitor.mqh : reconcile externally/manually opened MT5 demo deals using OnTradeTransaction; do not infer TP from candle touches.
- BX42_Dashboard.mqh : VI/EN chart UI, Entry/SL/TP1-3, zones, protected gains, gates, warning states.
- BX42_Notify.mqh : throttled MT5 desktop/push review-only notices; no unauthenticated trade commands.
- BX42_Logger.mqh : schema-versioned CSV/JSONL audit records, config/data fingerprint and reject reasons.
- BX42_TestHooks.mqh : deterministic replay diagnostics and scenario assertions.

## Execution modes with explicit boundaries
SIGNAL_ONLY: calculations, drawings, alerts; no real broker trade calls.
SEMI_AUTO: user independently places/approves a trade; monitoring can suggest updates; any actual broker stop update requires separate opt-in.
DEMO_AUTO_TEST: after test evidence and approval only, may execute solely on confirmed DEMO account, not live account.
LIVE: not in the first full-port milestone; fail closed if real account or unexpected permissions.
Data/signal/risk/decision layers must never gain order authority through a UI toggle alone.

## Work packages / dependency order
W1 freeze all 179 input declarations; map each Pine input, default, option and current behavior to MQL5; preserve modes.
W2 reproduce data and closed-bar MTF series. Normalize tick size, lot step, point value, broker server time and UTC.
W3 implement core Legacy SMC + locked setup + three independent legs; validate deterministic signals first, no orders.
W4 implement RSI Momentum M1 + CI observation + M5/M15 Fibonacci touch, ATR/swing stop and target extension.
W5 implement zone lifecycle and rendering: OB supply/demand, FVG, Fib 0.382-0.618, ZigZag, BOS/CHoCH/CISD labels.
W6 implement independent risk and virtual ledger, hedging/netting adapters, day-DD, spread, loss caps and kill switch.
W7 implement TP1-TP3 partials and actual-fill-aware dynamic profit locks; ensure no stop widening, peak floor conservative.
W8 implement bilingual dashboard, manual L1-L3 plan, mobile notifications, review-only journal and control states.
W9 compile, unit/integration/failure tests, TradingView-vs-MQL5 event parity using same OHLC timestamps and parameters.
W10 demo-only visual tester with real ticks, forward period, broker symbol specs, paper-to-demo audit; freeze release only after evidence.

## Platform-specific implementation constraints
- MQL5 CopyRates shift 0 is forming bar; closed-bar logic must exclude it on all TFs; HTF series must account for differing session boundaries.
- Confirmed swing pivots have a right-side confirmation delay and cannot retroactively trigger.
- AccountInfoInteger(ACCOUNT_MARGIN_MODE) distinguishes RETAIL_HEDGING from NETTING/EXCHANGE. Hedging supports separate tickets; netting must maintain a virtual per-leg ledger, not assume positions are independent.
- OnTradeTransaction handles DEAL_ADD and modifications; order request success is not evidence of execution.
- Prefer SymbolInfoDouble for SYMBOL_VOLUME_MIN/MAX/STEP, SYMBOL_TRADE_CONTRACT_SIZE and tick size/value; OrderCalcProfit/OrderCalcMargin/OrderCheck for broker-aware estimates, checking trade-server return codes.
- TP1/2/3 must not be marked filled from Bid/Ask touch alone. Real realized PnL includes relevant commission, swap, spread and slippage.
- Stop updates must be monotonic, valid under broker stops/freeze limits and fail closed on rejection. A positive planned stop cannot guarantee positive realized PnL on gaps.
- Pine TradingView broker emulator results cannot be required to match Exness MT5 PnL tick-for-tick.

## Definition of DONE
No DONE until each selected mode compiles in MetaEditor with zero errors; input map 100 percent accounted for (implemented or explicitly labeled unsupported); signal parity test with timestamps and documented deviations; risk/failure tests; actual-fill handling verified in DEMO; chart UI reviewed; no live execution permission; versioned logs, config and reports archived in 06_EVIDENCE.
