# Work 200 integration plan — BX42MR V4.2.8
Status: REFERENCE REGISTERED / IMPLEMENTATION NOT APPROVED FOR LIVE / VERIFICATION PENDING
Date: 2026-10-24
Goal: add a maintainable, testable strategy-reference extension without disrupting the existing Python paper-trading core.

## Architecture decisions
1. Preserve 00_ROOT, 01_ORIGINAL, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE, 07_RELEASE. Use 02_EXTENSION for versioned external strategies.
2. Keep Pine v6 and Python interfaces independent. Do not run TradingView strategy orders as Work 200 broker orders.
3. Preserve original source and checksum. V4.2.7->4.2.8 patch is reference only; no automatic application.
4. Add normalized signal contract later: idempotent event_id, UTC event/candle-close timestamps, market/exchange/symbol/timeframe, strategy/version/mode, BUY/SELL/EXIT/NO_TRADE, setup expiry, entry/SL/TP, source bars, validation status, and trace id.
5. Data integrity: prohibit look-ahead; enforce only closed HTF candles (D1/H4/H1), confirmed M15 triggers, timezone/volume/symbol validation, stale-data and spread guards, idempotent deduplication.
6. Separate risk: Python RiskManager/Portfolio must approve all simulated orders after applying fees, slippage and margin/contract specifications. Pine signals can never bypass this gate.
7. Distinguish Spot BTCUSDT vs perpetual BTCUSDT vs XAUUSD CFD; each needs independent tick size, step size, notionals, contract sizing, fees, funding/margin modeling. Do not extrapolate XAUUSD results to crypto.
8. Safe default: Signal Only on TradingView and PAPER_ONLY in Python. No exchange connector, n8n-to-MT5 execution or brokerage API credentials.

## V4.2.8 strategy reading
- Experimental Swing trend bias: D1, with H4 zone confluence and closed H1 confirmation before M15 setup/retest.
- H4 uses FVG, OB proxy and Fibonacci 0.382-0.618; zone timing is limited by TTL.
- Core Legacy SMC uses locked setup logic, TP1/TP2/TP3 and risk rules. RSI Momentum's special profit lock is separate; no assumption that it applies to Swing.
- Initial recommended visual test: XAUUSD M15; Mode Swing; Legacy SMC; HTF 1D; D1/H4/H1/M15 filter ON; Execution Signal Only.

## Milestones and independent gates
A. Source integrity: verify full source checksum against user ZIP and verify Pine Editor compile; collect TradingView evidence.
B. Parity: when filter OFF, V4.2.8 outputs match V4.2.7 in a fixed dataset, aside from approved deltas.
C. Filters: on M15 test D1 trend, H4 touch and TTL, H1 confirmation, M15 retest; wrong timeframe or invalid signals must NO_TRADE.
D. Cost/risk: verify TP1/2/3, net PnL, 0.01 lot assumptions only for correctly configured XAUUSD contract, and drawdown protection.
E. Python interface: implement adapter plus typed schema, signature/auth if external messages, dedup, stale and replay rejection, explicit paper-only enforcement.
F. Deterministic replay/backtest: unit/integration/failure tests and evidence with source/data/config fingerprints.
G. Release decision: only after test evidence + human review; live trading requires separate explicit decision.

## Acceptance status
Source registered in Library: YES. Source also copied into Sandbox and hash verified: YES.
Sandbox full .pine copy: YES (SHA256 matched after staged transfer).
Pine compile: NOT RUN.
Python port: NOT IMPLEMENTED.
Backtest: NOT RUN.
Paper integration: NOT IMPLEMENTED.
Live execution: DISABLED / OUT OF SCOPE.
