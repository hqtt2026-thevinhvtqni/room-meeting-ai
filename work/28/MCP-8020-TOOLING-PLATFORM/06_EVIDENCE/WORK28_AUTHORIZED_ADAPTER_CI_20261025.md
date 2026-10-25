# Work 28 — Authorized adapter staging evidence

- Date: 2026-10-25
- Reviewer/implementer: Xu (AI-01)
- Branch: `work/28-mcp-tooling-platform`
- Decision: **STAGED / NOT WIRED / NOT RELEASED**

## Changes

- `04_CODE/mcp8020_authorized_execution_adapter_v1.py`
  - Introduces a narrow policy seam around injected trusted Core authorization, immutable source snapshot provider, and pinned runtime.
  - Rejects missing/denied caller context before snapshot resolution.
  - Checks Work/path binding, immutable snapshot attestation, expected SHA-256, exact snapshot reference, pinned runtime identity, required request/run/evidence IDs, integer exit code, process-tree cleanup attestation, and non-empty clean test summary.
  - Does not authenticate callers itself, inspect/hash source bytes itself, launch processes, or provide trustworthy attestations; those are contracts for trusted injected components.
  - Not registered in MCP and not wired into v54 service or W13 HTTP route.

- `05_TEST/test_mcp8020_authorized_execution_adapter_v1.py`
  - Positive contract test and negative tests for forged public authority/command fields, absent caller context, authorization denial, hash mismatch, mutable snapshot, Work/path mismatch, runtime identity mismatch, wrong snapshot, missing evidence binding, failed cleanup, invalid/empty test summary, and missing pinned runtime identity.

## CI evidence

- Run: [Work 28 MCP Tooling Tests #104](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40150058368)
- Commit: `d61d6a33dded605a74bce1d128a94f611fc68ac8`
- Result: **PASS** — 191 tests, 4 skipped.
- The earlier run at `01f9269fafc12560cba088b88e5cf739a0c435b8` failed because its commit snapshot contained the pre-update test fixture; the subsequent test commit above ran the updated source and fixture successfully. No failure was concealed.

## Boundary / next gate

This CI run proves only staged unit/regression behavior with mocks. It does **not** prove live Core authorization, source bytes are actually snapshotted and hashed by a trusted resolver, W13 executes that exact snapshot, approved runtime identity is cryptographically/trustworthily pinned, process-tree cleanup is real, or live E2E works.

Keep all seven public execution/evidence tools `NOT_IMPLEMENTED`. Do not wire this adapter or enable tools until trusted implementations exist and W13 unit tests plus authorized live E2E prove the complete evidence chain. No second execution host is authorized.
