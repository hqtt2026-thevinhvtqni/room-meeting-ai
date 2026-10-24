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


## GitHub mirror / two-way synchronization
- Repository: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai
- Work branch: `work/200-crypto-trading-bot`
- Canonical Work folder on GitHub: `WORK-200-CRYPTO-TRADING-BOT/`
- The Work source tree and evidence are mirrored under the same numbered folders (`00_ROOT` through `07_RELEASE`) where text/source files are available through Sandbox MCP 8030.
- After changes in either location, compare the affected revisions before overwriting, sync the changed files to the counterpart, then record verification in the Work journal.
- This is an agent-driven/manual two-way sync workflow. No always-on daemon or webhook has been configured; do not claim continuous automatic synchronization.
- GitHub branch is not merged into `main`. Do not place secrets or exchange credentials in the repository.
