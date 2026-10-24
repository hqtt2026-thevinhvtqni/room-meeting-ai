# Work 200 — Crypto Trading Bot

## Goal
Build a maintainable cryptocurrency trading bot that can ingest market data, generate strategy signals, simulate execution, enforce risk limits, and report performance transparently.

## Safe first release
1. Historical data ingestion with validation and timestamp normalization.
2. Strategy interface and one baseline strategy for experiments.
3. Backtesting with fees, slippage assumptions, and no look-ahead bias.
4. Paper-trading adapter; no real funds or live orders.
5. Risk engine: max position, max daily loss, max drawdown, cooldown, and kill switch.
6. Tests, reproducible configuration, logs, and performance report.

## Non-goals for the first release
- No promise or implication of guaranteed profit.
- No live trading or withdrawal capability.
- No storing API secrets in source files or logs.
- No strategy promotion based only on in-sample results.

## Status
ACTIVE. Project created in ROOM-HOP Sandbox. Implementation and verification remain pending.
