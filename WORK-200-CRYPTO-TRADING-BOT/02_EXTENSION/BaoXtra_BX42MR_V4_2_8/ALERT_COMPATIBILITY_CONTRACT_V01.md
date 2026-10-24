# BX42MR V4.2.8 — Alert compatibility contract (v0.1)
Date: 2026-10-24
State: DOCUMENTED / ADAPTER NOT IMPLEMENTED / LIVE FORBIDDEN

## Actual Pine alerts
Source: BaoXtra_BX42MR_V4_2_8_Swing_D1_H4_H1_M15_TEST.pine.
- Legacy plan at ~line 993: BX421|MANUAL_REVIEW|<leg_id>|<symbol>|BUY/SELL|ENTRY=...|SL=...|TP1=...|TP2=...|TP3=...|QTY_CHART=...
- Legacy backtest order mode at ~line 993: BX421|BACKTEST_AUTO|...; NOT an exchange fill or live order.
- Legacy backtest add at ~line 1055: BX421|BACKTEST_ADD|...; no ordinary reviewed entry schema.
- Momentum plan at ~line 1569: BX42_MR|MANUAL_REVIEW|<symbol>|BUY/SELL|LOT=...|ENTRY=...|SL=...|TP1=...|TP2=...|TP3=...|TP_SHARE=...
- Momentum paper signal at ~line 1569: BX42_MR|PAPER|...; not broker execution.
- Momentum trailing stop update at ~line 1403: BX42_MR|PAPER_ONLY|SL_UPDATE|...; distinct event type; NEVER mapped into a new BUY/SELL order.
- Pine executionMode = Signal Only suppresses alert() on the reviewed entry branches. No connector should silently toggle this option to a mode that emits alerts.

## Compatibility gap
crypto_bot.signal_intake.parse_signal() expects a typed Mapping with explicit event_id, strategy/version, symbol/venue/market/timeframe, event_time, candle_closed_at, closed_bar=true, execution_mode=SIGNAL_ONLY, live_execution=false, paper_only=true, Entry/SL/TP.
None of the raw Pine formats supplies sufficient verifiable data for this contract; direct conversion is NOT safe without authenticated transport and verified source metadata. Current parser correctly rejects raw strings.

## Reference JSON (synthetic, not actual chart data)
{
 "event_id":"BX428-20261024-0001","strategy":"BX42MR","version":"4.2.8",
 "symbol":"BTCUSDT","exchange":"OKX","market":"SPOT","timeframe":"15m",
 "side":"BUY","event_time":"2026-10-24T01:00:00Z",
 "candle_closed_at":"2026-10-24T01:00:00Z","closed_bar":true,
 "execution_mode":"SIGNAL_ONLY","live_execution":false,"paper_only":true,
 "entry":"100","stop_loss":"98","take_profit_1":"102",
 "take_profit_2":"104","take_profit_3":"106"
}
This synthetic object exercises the parser only. BTCUSDT/OKX/SPOT is its test allowlist; the Pine Swing reference is primarily XAUUSD CFD.

## Required implementation gates
1. Define transport envelope and verifiable Pine alert source, with fixed strategy version and venue metadata; prohibit self-attested trust solely via JSON flags.
2. Create review-only preview parser separately for BX421 MANUAL_REVIEW and BX42_MR MANUAL_REVIEW. Incomplete, unknown, stale, or ambiguous events fail closed. PAPER/BACKTEST_AUTO/BACKTEST_ADD/SL_UPDATE remain distinct types and must never silently become an entry.
3. Event IDs must be stable and persisted for idempotency; timestamps UTC; allow only confirmed close; reject replay, future and stale events; enforce H1/H4/D1 close rules.
4. Authenticate signed gateway requests and never commit secrets to source or logs. No unauthenticated webhook-to-MT5 routing.
5. Validate venue-native symbol/contract units, tick size, quantity step, order direction, spread, margin/leverage, costs and risk parameters.
6. Signals remain REVIEW_ONLY until an independently validated portfolio/risk and paper broker gate exists.
7. No live broker APIs or orders without a separate explicit decision and security/risk review.

## Not verified
No TradingView Pine compilation, no Strategy Tester export, no source-authenticated webhook, no complete Pine-to-Python adapter, no execution.
