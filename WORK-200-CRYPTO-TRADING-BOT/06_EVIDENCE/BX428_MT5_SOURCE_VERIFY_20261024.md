# Work 200 — MT5 port v0.1 verification evidence
Date: 2026-10-24
Result: MCP SOURCE_SYNC PASS / LOCAL STATIC TESTS 7/7 PASS / MT5 COMPILE NOT RUN

## Source and configuration
Path: 02_EXTENSION/BaoXtra_BX42MR_V4_2_8/MT5_PORT_V0_1/
- EA .mq5: 517 lines, 22092 bytes, SHA256 94ac4f83904df5d7ffee1f81921660d2e5f481fc262dd45b0541d3c18a966356
- .set preset: 784 bytes, SHA256 4509d14e11f844d1fbe2bc7d4d5cbaafa44e633ce301251f5e0230a97d25a7d0
- README_VI_EN.md: SHA256 3231e3fcaa2aaecc338c875a356e3e446825c2424efb865393924fa52a44e357
- MT5_TEST_CHECKLIST.md: SHA256 6da1ec393392d578abee991a612ea34153cc233e7251a80f34b5b2633c5a308d
- tests/test_mt5_source_contract.py: SHA256 9dd159715b91f72d642f177346265950f103dbcea7f1649e79caa5b79b1b2443
MCP Sandbox read-back compared with Library copy: all five file contents MATCH including final LF.

## Static tests
Command (local Python 3.13.5 / pytest 9.0.2): python -m pytest -q tests/test_mt5_source_contract.py
Output: 7 passed in 0.03s
Assertions include absence of trading APIs; required callbacks; M15 gate; confirmed HTF shifts; plan levels; manual-only defaults; naive balanced brackets.
ZIP integrity: testzip() = None.
These are STATIC TESTS, not MQL5 compiler or running terminal checks.

## Open tests
- Windows MT5/MetaEditor F7 0 errors — PENDING.
- D1/H4/H1/M15 chart replay, BOS/retest, zone TTL, BUY/SELL filter — PENDING.
- Signal frequency, false positives, TP/SL mathematical and broker contract validation — PENDING.
- Cross-check original Pine v4.2.8 on identical data — PENDING.
- Push notification to iPhone / MetaQuotes ID — PENDING.
- EA has NO execution API; MT5 Strategy Tester will NOT show actual trade PnL from this version.

## Safety
Use demo MT5 desktop for validation; no live orders or financial actions enabled. Release status: SOURCE_PREVIEW, NOT TERMINAL_VERIFIED.
