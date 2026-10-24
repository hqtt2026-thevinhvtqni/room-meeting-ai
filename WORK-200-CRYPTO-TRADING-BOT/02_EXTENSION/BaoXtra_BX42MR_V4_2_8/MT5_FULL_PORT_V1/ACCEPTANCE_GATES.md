# BX42MR Full MT5 acceptance gates (planned, no PASS without evidence)
Release candidate: BaoXtra_BX42MR_Full_V1_0_DEMO.
Evidence path: Work 200 / 06_EVIDENCE; capture builds, screenshots, test logs and input/data fingerprints.

G0 SOURCE BASELINE
- [ ] Pine original hash frozen; complete list of 179 input declarations and source line mapping stored.
- [ ] All engines/modes specified and versioned; unsupported behaviors explicitly logged.
G1 COMPILE + LOAD
- [ ] MQL5 MetaEditor F7 build: 0 compilation errors, warning review.
- [ ] All indicators copied/released correctly; no invalid handles; volume, tick and broker contract property checks pass.
- [ ] Real account fails closed in DEMO_AUTO_TEST; no credentials in code.
G2 PURE SIGNAL PARITY
- [ ] Same OHLC timestamps + same preset; compare independently computed EMA/RSI/ATR/pivots.
- [ ] Confirm BOS/CHoCH/CISD/sweep confirmation at event bar, never pivot origin bar.
- [ ] Reconstruct OB/FVG/Fib zones with TTL and invalidation; no future data.
- [ ] Test Legacy SMC Scalping; Legacy SMC Swing optional filter OFF and ON; RSI Momentum M1.
- [ ] Signal-only manual L1-L3 overlays; checked on XAUUSD and separately on BTCUSDT data.
G3 REPLAY AND EDGE CASES
- [ ] Timezone/DST gaps, weekend/gapped sessions, stale data, missing indicators and partial HTF candles blocked.
- [ ] Locked setup snapshot immutable; next-bar retest only; expiry, reversal and duplicate event correct.
- [ ] Risk gate rejects spread spikes, stop too close, volume below broker min or above exposure, daily loss, cooldown, wrong engine/timeframe.
G4 VIRTUAL CAMPAIGN
- [ ] L1-3 risk budgets validated; same-direction and hedging/netting behavior correctly reconciled.
- [ ] Simulate fills with Bid/Ask, spread, fees, slippage and missing ticks; rejects and pending cancel handled.
- [ ] TP1/TP2/TP3 partial percentages of ORIGINAL volume, actual fill events only; BE after real TP1, no missing reserved quantity.
- [ ] Dynamic SL 20 -> 40 -> 60 -> 70 percent *peak* net-profit floor; stop never widens; collective and per-leg sums consistent after restarts.
- [ ] GAP / slippage below floor logged as risk, not called guaranteed retained profit.
G5 E2E TERMINAL
- [ ] MT5 Strategy Tester visual + Every tick based on real ticks, tester journal captured; forward sample.
- [ ] Demo-only manual-trade watch in OnTradeTransaction reconciles partial close/deals/commission.
- [ ] MT5 iPhone push notification tested; no EA running on iPhone.
- [ ] Restart/VPS loss, duplicate transaction, reject, illiquid spread, freeze level, unknown symbol/account mode fail closed.
G6 HANDOFF
- [ ] Parity report notes justified Pine/MT5 differences; no profit guarantee.
- [ ] Source + .set + release notes + evidence reviewed and attached; release hash frozen.
- [ ] LIVE trading remains disabled in this full-port candidate; separate approval for any future real-money execution.

Status of all G0-G6: NOT PASSED at the time of drafting; they are acceptance targets.
