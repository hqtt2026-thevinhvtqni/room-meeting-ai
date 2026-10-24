# Work 200 — BX42MR V4.2.8 Signal Intake, v0.1

`crypto_bot.signal_intake` is an isolated, standard-library-only, **review-only** typed validation boundary for *future* normalized webhook messages. Not wired to TradingView, n8n, MT5, `PaperBroker` or an exchange. TradingView currently emits legacy pipe-formatted alerts; those alerts are intentionally rejected, not parsed into orders.

## Example input (for unit tests, not a live webhook)

```json
{"event_id":"BX428-20261024-0001","strategy":"BX42MR","version":"4.2.8","symbol":"BTCUSDT","exchange":"OKX","market":"SPOT","timeframe":"15m","side":"BUY","event_time":"2026-10-24T01:00:00+00:00","candle_closed_at":"2026-10-24T01:00:00+00:00","closed_bar":true,"execution_mode":"SIGNAL_ONLY","live_execution":false,"paper_only":true,"entry":"100","stop_loss":"98","take_profit_1":"102","take_profit_2":"104","take_profit_3":"106"}
```

## Supported behavior

- Reject live-mode or unconfirmed-bar signals, unknown market/symbol, stale/future events, missing explicit safety flags, invalid prices/SL/TP ordering, and duplicate IDs within the same process.
- Never place any order or load broker credentials; output only `REVIEW_ONLY` plans.
- No trust/authentication from fields alone. A future production gateway must verify transport, signatures, persistent replay store, source-data accuracy, portfolio/risk, and failure paths before permitting even simulated fills.
- Default policies: OKX BTCUSDT SPOT, 15m. No claim that the original Pine script produces this JSON.
- Timeframe and symbol assumptions must be adapted and validated before applying to XAUUSD CFD or perpetuals.

Run from the package parent (`04_CODE`): `python -m pytest ../05_TEST/tests/test_signal_intake.py -q`.
