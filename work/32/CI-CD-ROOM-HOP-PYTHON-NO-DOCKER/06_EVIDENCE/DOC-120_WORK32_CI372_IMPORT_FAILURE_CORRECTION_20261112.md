# DOC-120 — Work32 CI Run #372 Failure Analysis and Corrective Action

- **Document Number:** DOC-120
- **Priority:** P0 — exact-SHA CI defect correction
- **Work:** 32 — CI/CD
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-12 00:25 Asia/Ho_Chi_Minh
- **Run:** #372 — 43071977580
- **PR:** #52
- **Tested merge revision:** 331b1743c41a83ac6c763019117374fadd731632
- **Implementation branch:** work/32-core-owned-execution-authority-20261112
- **Status:** ROOT CAUSE IDENTIFIED AND PATCHED — RETEST PENDING

## 1. Observed result

- Work32 tooling/workflow mirror: PASS.
- Python compileall: PASS.
- Product Auto E2E: PASS (existing bounded suite).
- Unit test job: FAIL during test collection; new Core authority HTTP test could not import the authority module.
- Windows Browser Adapter: still in progress at time of first failure inspection; its result is not included in this finding.
- Product artifact: SKIPPED because its dependency on unit failed.

## 2. Exact root cause

tests/test_execution_authority_http.py imported room_hop_mcp.adapter.execution_authority_http. That router module used a relative import for ExecutionAuthority as if the implementation lived inside room_hop_mcp.adapter. The canonical owner module is core.execution_authority, so collection failed with:

ModuleNotFoundError: No module named 'room_hop_mcp.adapter.execution_authority'

This is an implementation import defect, not an authorization test failure. The unit suite stopped at collection; no PASS is inferred for tests that did not execute.

## 3. Corrective action

- Changed the router import to: from core.execution_authority import AuthorityError, ExecutionAuthority.
- Corrective source commit: ea9c91825bbd831caa6ba2b7b0dfcca0a8eec926.
- No test was removed, skipped, weakened or reclassified.
- New PR head requires a fresh exact-SHA CI run. Run #372 remains FAIL and is not overwritten by the patch.

## 4. Acceptance status

- Corrective patch exists in the implementation branch.
- Retest is pending; no PASS is claimed.
- Security review, live Core/Host configuration, positive/negative protected execution E2E and PC self-hosted runner identity remain open.
- PROTECTED EXECUTION DENIED; Work32 remains ACTIVE — NOT RELEASED.

## BIÊN BẢN
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-12 00:25 Asia/Ho_Chi_Minh
- **Finding:** Identified a router import-path defect from the exact CI log and patched the canonical import.

## NHẬT KÝ
- **W32-LOG-20261112-112**
- Run #372 preserved as FAIL; corrective commit recorded; retest pending.