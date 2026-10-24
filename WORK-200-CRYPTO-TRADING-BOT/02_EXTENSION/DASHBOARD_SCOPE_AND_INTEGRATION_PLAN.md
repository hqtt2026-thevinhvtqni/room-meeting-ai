# Dashboard Scope and Integration Plan — Work 200

## Purpose
Provide an operational overview for the cryptocurrency bot, initially using clearly labelled mock data and without live trading capability.

## Dashboard sections
- Portfolio KPIs: simulated equity, P&L, drawdown, paper fills.
- Equity curve: selectable 1D/1W/1M demo ranges.
- Risk monitor: order/position/daily-loss limits and kill-switch state.
- Market watchlist: symbol, price, percentage move, feed status.
- Recent paper trades: side, symbol, quantity, simulated price, time.
- System readiness: data adapter, strategy, backtest, test suite.

## Current artifact
`04_CODE/dashboard/index.html` is a responsive, dependency-free static prototype. All visible financial values are mock data. UI controls are local-only.

## Integration contract (next step)
The UI must consume a read-only backend API:
- `GET /api/dashboard/summary`
- `GET /api/market/watchlist`
- `GET /api/paper-trades?limit=...`
- `GET /api/risk/status`
- `GET /api/backtests/latest`

Every response should include timestamp, source, and freshness/status metadata. Missing or stale data must be shown as unavailable, never silently substituted with fake live values.

The stop control must not be represented as operational until it is authenticated, connected to the risk engine, audited, and covered by failure-path tests.

## Acceptance criteria
- Responsive on mobile and desktop.
- Mock data explicitly identified throughout.
- No live order submission or credential handling in the browser.
- Loading, stale, unavailable, and error states added during backend integration.
- Visual and interaction checks performed in an actual browser before claiming UI verification.
