# BaoXtra BX42MR V4.2.8 in Work 200
Status: SOURCE COPIED AND SHA256 VERIFIED; Pine compile/backtest NOT RUN; signal intake 27/27 local tests PASS.

This extension registers the user-provided Pine Script v6 Swing strategy and defines the gates for safe future integration into Work 200.
Complete Pine source is stored in this Sandbox extension folder and preserved in the user Library /Work200-BaoXtra-V428/; patch is stored in Library only. See IMPORT_RECORD.md.
Source original ZIP: BaoXtra_BX42MR_V4_2_8_Swing_TEST_PACKAGE.zip. Source completeness verified by content SHA256 via MCP read_probe.
Source hash (SHA256): 2cb18bd304a6951c2ffc7fea70a6510bfa5f4b07cc1b985b793201369e27bf3a.

- IMPORT_RECORD.md — source inventory, provenance and location, connector limitation.
- WORK200_BX428_INTEGRATION_PLAN.md — architecture decisions, integration roadmap.
- TEST_CHECKLIST.md — source-integrity and local module tests PASS; TradingView/E2E gates remain pending.

Boundary: do not treat the Pine Script as a Python module. Preserve Python research + paper core in 04_CODE. Work 200 currently does not import Pine code and has no approved live execution.

- ALERT_COMPATIBILITY_CONTRACT_V01.md — Pine alert formats and safe adapter requirements.
- 06_EVIDENCE/BX428_INTEGRATION_VERIFICATION_20261024.md — source hash and local test evidence.
