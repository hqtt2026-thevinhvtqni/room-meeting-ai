# BX42MR Pine V4.2.8 -> MT5 v0.1 parity matrix
Date: 2026-10-24 | REVIEW ONLY

| Element | Pine V4.2.8 reference | MT5 MQL5 v0.1 | Acceptance |
|---|---|---|---|
| D1 bias | D1 Swing trend logic | Closed D1 EMA21/50 and price | Approximation; parity not verified |
| H4 zones | OB/FVG/Fibonacci | H4 3-bar FVG, OB proxy, confirmed-pivot Fib .382-.618 | Partial; lifetime/selection differs |
| H1 confirmation | RSI/candle/EMA | RSI14 + selected candle/EMA on closed H1 bar | Approximation |
| M15 entry | SMC multi-feature filters | M15 BOS displacement, locked setup + later retest | Partial; no full CHoCH/CISD |
| Stop and target | Multiple leg exits and profit locks | SL with ATR buffer; 1R/2R/3R display only | No order management |
| Pyramiding | Up to three Pine strategy legs | None | Not implemented |
| Momentum | RSI Momentum engine | None | Not implemented |
| Chart zones | Several advanced Pine overlays | H4 high/low level lines; Entry/SL/TP | Partial |
| Backtest | Pine Strategy Tester | MT5 EA contains no order execution | Cannot compare PnL yet |
| Automation | TradingView simulation/alert modes | No broker/API order execution | Safe review-only |
| Mobile | TradingView alerts/chart | Optional desktop MT5 push to iPhone | Not directly runnable on phone |

Required parity trial: compile in MetaEditor, visually compare same symbol/timeframe/timezone, verify every gate on closed bars, and retain failing cases. Do not claim comparable PnL or 100% strategy parity.
