# Work 28 — Mapper fail-closed correction
**TÊN:** Co  
**CHỨC DANH:** Coder / ROOM-HOP  
**NGÀY:** 25/10/2026  
**GIỜ - PHÚT:** 11:18 (UTC+7)

Corrected `04_CODE/mcp8020_w13_execute_envelope_v1.py` to call the new canonical compatibility guard before returning any envelope. Under the currently inspected W13 schema, it now raises `EnvelopeError(W13_CANONICAL_CONTRACT_NOT_COMPATIBLE...)` rather than returning an object that W13 would reject or translating `entry_path` into a command.

Updated `05_TEST/test_mcp8020_integration_boundary_v1.py`: the former envelope “happy path” is replaced by a regression asserting the current canonical W13 contract fails closed. Existing negative request/context tests are preserved.

This is a source-level correction in Work 28 Sandbox only. Files have not been executed by Python/pytest in this session. No Core/W13 deployment, live HTTP, or tool activation occurred. Keep seven execution/evidence tools `NOT_IMPLEMENTED`, `sandbox_run_command=POLICY_REFUSED`, Work 28 `ACTIVE / BLOCKED / NOT RELEASED`.
