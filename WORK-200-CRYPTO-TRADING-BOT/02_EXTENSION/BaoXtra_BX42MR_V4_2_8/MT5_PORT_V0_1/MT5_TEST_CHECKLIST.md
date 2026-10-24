# Work 200 — MT5 BX42MR v0.1 test gate

## Source-level verification
- [ ] Source checksum published/verified in MCP 8030.
- [ ] No trading API calls or broker orders in source (static audit).
- [ ] No unconfirmed HTF bar requests (shift 0) in signal evaluation.
- [ ] Only M15 timeframe allows signals.
- [ ] Entry planning gated by D1, H4 zone touch, H1 confirmation, confirmed M15 structure and later retest.

## Terminal verification — PENDING
- [ ] MetaEditor F7 compiled: 0 errors.
- [ ] MT5 Experts/Journal show REVIEW_ONLY and data loaded.
- [ ] No BUY/SELL without confirmed H4 touch within TTL.
- [ ] No BUY/SELL against D1 EMA and H1 RSI+candle.
- [ ] No entry on the same M15 candle as BOS lock.
- [ ] Wrong chart timeframe: USE M15, no plans.
- [ ] TP1/TP2/TP3 and SL remain on intended side of Entry.
- [ ] Spread > configured ATR ratio suppresses plan.
- [ ] Trading disabled and tester shows no deals opened by EA.
- [ ] Push to MT5 iPhone works via MetaQuotes ID if opted in.
- [ ] Price/contract/lot/stops values verified for selected broker symbol.
- [ ] Snapshot video, compile logs, config file and run window attached as evidence.

Release: SOURCE_PREVIEW / NOT COMPILE VERIFIED / NO LIVE.
