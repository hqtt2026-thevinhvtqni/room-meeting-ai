# Work 200 Dashboard Prototype

## File
- `04_CODE/dashboard/index.html` — responsive, dependency-free static dashboard.

## Current features
- KPI cards for simulated equity, P&L, drawdown, and paper fills.
- Demo equity curve with 1D / 1W / 1M tabs.
- Risk limit visualization and a UI-only demo stop switch.
- Watchlist table and sample paper-trade history.
- System readiness indicators for data source, strategy, backtest, and tests.
- Responsive layout for desktop and mobile.

## Important limitations
- All market prices, balances, trades, and metrics are **illustrative mock data**.
- No exchange API, websocket, backend, persistence, or live order execution.
- “Kích hoạt dừng demo” changes only the interface status; it is not connected to the risk engine.
- Do not use this UI to make live trading decisions.

## Integration plan
1. Define a read-only dashboard API contract for status, market data, portfolio, risk, trades, and backtest results.
2. Replace mock values only with validated, timestamped backend responses.
3. Add loading, stale-data, unavailable, and error states.
4. Wire the kill switch to the backend risk engine only after authenticated authorization, audit logging, and tests.
5. Keep live execution disabled unless a separate project gate explicitly authorizes it.
