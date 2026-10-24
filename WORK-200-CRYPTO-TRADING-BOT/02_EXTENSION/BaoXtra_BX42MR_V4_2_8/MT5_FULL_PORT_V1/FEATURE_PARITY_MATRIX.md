# Pine V4.2.8 to MQL5: precise feature map
State: planned, not implemented unless noted for existing MT5 v0.1. 2026-10-24.

| Feature | Original Pine location / settings | MT5 v0.1 | Full-port implementation target |
|---|---|---|---|
| Engine/profile | lines 19-34 RSI Momentum(default), Legacy SMC; Scalping(default)/Swing | Swing-only | Separate engines and profile presets |
| Execution modes | lines 31-47 Signal Only, Semi-Auto Alerts, Auto Backtest | Review only | Explicit signal/manual/demo gates |
| Manual plan | lines 36-46 Entry L1-3, SL1-3, TP1-3 | Limited preview | Full manual level UI + persistence |
| Scalping preset | lines 49-60 EMAs, HTF, swing, score, SL | Missing | Implement |
| Swing preset | lines 63-74 HTF, EMA21/55/200, min score | Approximation | Exact per-input |
| Optional Swing confluence | lines 80-99 D1/H4 zones/H1 confirmation/M15 | Partial | Exact zone mode, BOS TTL, RSI thresholds and gated next-bar retest |
| Sweeps, BOS, CHoCH, CISD | lines 103-113, 431-517 | Basic BOS only | Confirmed pivots and correct event timestamps |
| Core locked setup | lines 643-997 | Partial | Lock snapshot, freeze TTL, next confirmed bar retest, cancel and invalidation |
| SMC zone drawings | lines 542-643, 1643-1716 | Partial horizontal lines | OB/FVG/Fib boxes, history, invalidation, overlap filters |
| Core risk | lines 116-135 | Only spread reference | Actual price/volume specs, day DD, order count, session, cooldown |
| Core exits | lines 138-146, 713-868 | Plans only | True fill TP1/2/3, BE after TP1, trailing, cost-aware state |
| Advanced pyramiding | lines 172-186, 997-1059 | Missing | Max 3 legs, add BOS and pullback, aggregate downside risk |
| RSI momentum | lines 192-226, 1073-1163, 1478-1576 | Missing | M1 execution, D1/H1 bias, M15/M5/M1 RSI, CH/BOS and CI watch |
| Momentum fib/stop/TP | lines 231-243, 1117-1198, 1512-1529 | Missing | M5/M15 pivot fib touch TTL, ATR/swing stop, R+Fib extension |
| Momentum dynamic SL | lines 250-263, 1198-1476 | Missing | True fill accounting and campaign 20/40/60/70 peak retention |
| Momentum sizing/risk | lines 194-212, 1163-1184, 1482-1488 | Missing | Per-entry/total stop risk, equity/margin, broker lot step |
| Alerts | lines 993,1055,1403,1569 | MT5 Push optional | Distinct entry/exit/SL update types; never parse as orders |
| Dashboard & ZigZag | lines 149-169, 1571-1758 | Basic dashboard | Both engine dashboards, L1-L3 overlays, bilingual logs |
| Full PnL and broker reconciliation | Pine strategy emulation state vs MT5 actual | Missing | Position/deal ledger, OnTradeTransaction, netting/hedging |
| Backtesting | TradingView broker emulator | Not executable orders | Tick-based MT5 demo-only/paper test harness |

Only scope currently demonstrably sourced in Work 200 is MT5 v0.1 review-only, not feature-complete. Any feature marked 'missing' must not be represented as deployed.
