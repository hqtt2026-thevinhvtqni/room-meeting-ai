# Initial Architecture Plan — Work 200

## Components
1. **Market data adapter** — fetch/import OHLCV data; validate schema, timestamps, gaps, duplicates, and symbol/timeframe.
2. **Strategy interface** — deterministic signal generation from data available at decision time.
3. **Portfolio and risk engine** — position sizing, exposure caps, max daily loss/drawdown, cooldown, and global kill switch.
4. **Execution simulator** — model fees, spread/slippage, fills, rejected orders, and latency assumptions for backtests.
5. **Paper broker** — simulated orders only; explicit adapter boundary prevents accidental live execution.
6. **Backtest runner** — reproducible runs, out-of-sample splits, walk-forward evaluation, and benchmark comparison.
7. **Persistence and observability** — structured logs, configuration snapshots, trade ledger, metrics, and run identifiers.
8. **Reporting** — returns, drawdown, volatility, turnover, fees, win/loss distribution, exposure, and comparison against a baseline.

## Safety and correctness gates
- No look-ahead or survivorship bias in evaluation.
- Fees and slippage must be included and configurable.
- Missing/invalid data fails closed.
- Position/risk limits are enforced independently of the strategy.
- Kill switch blocks new orders and cancels simulated outstanding orders.
- API credentials must be externalized; never log secrets.
- Initial milestone must not contain a live-order adapter.
- A profitable backtest is not evidence of future profitability.

## Proposed build phases
- **P0 — Requirements and interfaces:** define scope, data contract, strategy contract, configuration, and acceptance criteria.
- **P1 — Core simulation:** data validation, strategy interface, portfolio/risk engine, paper broker.
- **P2 — Backtest and metrics:** fees/slippage, benchmarks, out-of-sample checks, reports.
- **P3 — Verification:** unit tests, integration tests, deterministic replay, failure-path tests.
- **P4 — Paper-trading dry run:** observe without real funds; record evidence and unresolved risks.
- **P5 — Separate decision gate:** any future live-trading work requires explicit approval, security review, and independent risk sign-off.

## Proposed technology
Python is a candidate because of its data-analysis and testing ecosystem; final selection remains a P0 decision after checking the Sandbox runtime and dependency availability.
