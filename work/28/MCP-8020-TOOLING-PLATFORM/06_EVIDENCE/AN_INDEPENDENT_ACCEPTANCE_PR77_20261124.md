# WORK 28 — AN INDEPENDENT ACCEPTANCE — PR #77

- Date: 2026-11-24; time: 12:53 +07
- Role: An | TESTER
- PR: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/77
- Exact reviewed commit: 245e2962429433ea2145032970db1b7637d624ae
- Engine blob: e9f24f2516581ff7b4dd558cac92c0d73419541f
- Test blob: fcc13090f230317b56730fdc74de336457a361a0
- Signature: [KÝ: AN | TESTER]

## Disposition
**BLOCKED — NOT ACCEPTED. DO NOT MERGE / REGISTER / DEPLOY / ENABLE.**

Exact-head GitHub Actions run #504 (45336196761) completed SUCCESS in all six jobs. This is configured CI evidence, not an independent An test run and not production integration evidence.

## Evidence inspected
- Fetched engine and test source at the exact commit above.
- Retrieved all six run #504 job summaries: native Windows binary-upload tests, Windows Host lifecycle, Linux Host lifecycle, unit/regression, exact-SHA artifact build/retest, and automatic E2E gate report — all SUCCESS.
- Test module contains 22 methods covering PNG/arbitrary binary, invalid UTF-8, ZIP, zero-byte, missing authority, untrusted context, wrong Work, traversal, symlink, chunk order/replay, checksum mismatch, overwrite denial, concurrency, finalize retry/recovery and abort state.
- PR review submissions and inline review threads returned empty at inspection. Ka's JRN-W28-102 findings exist in the canonical journal, but no formal PR approval is recorded.
- Connected MCP 8030 Sandbox surface is text-oriented; no raw-byte upload/readback tool exists. Candidate engine/test files are absent from live Sandbox Work 28.

## Findings

### AN-W28-PR77-F01 — P1 — Filesystem containment race — FAIL
Source validates components with pathname-based resolve/symlink checks, then uses ordinary pathname mkdir/open/link/unlink/read operations. No verified directory-handle-relative backend or stable parent identity chain was found. Tests cover symlink denial but not hostile parent-directory replacement or Windows reparse-point races.
**Closure:** handle-anchored no-follow/reparse-point-safe operations on supported platforms, or fail closed; add parent-swap, destination-race and staging-replacement tests on native Windows and Linux.

### AN-W28-PR77-F02 — P1 — Restart reconciliation / durability — FAIL / NOT PROVEN
FINALIZING recovery exists, but no startup reconciliation routine was found for chunk ledger vs staging bytes, final destination, quota reservations and audit records after arbitrary restart. File fsync calls do not prove affected parent-directory entry durability; promotion/cleanup lacks demonstrated directory flush semantics. Selected finalize crash tests do not cover the full crash matrix.
**Closure:** idempotent restart reconciliation, orphan staging/quota repair or quarantine, and platform-appropriate directory durability/audit-order tests.

### AN-W28-PR77-F03 — P1 — Core revoke/finalize atomicity — BLOCKED
The engine uses an injected authorizer per operation, but the PR contains no production Core upload-grant route/client adapter or atomic lease/commit protocol spanning revocation and final promotion. Component stubs do not prove a revoke racing finalize is serialized by Core.
**Closure:** approved Core-owned upload capability, explicit revocation/finalize linearization semantics and race tests.

### AN-W28-PR77-F04 — P0 — Live Build MCP/Sandbox integration — BLOCKED
No raw-byte Build MCP :8030 transport or tool registration is present; candidate files are not in live Sandbox Work 28; no PC → Sandbox → binary readback SHA-256 canary was run.
**Closure:** add bounded raw-byte transport and registration only after security gates pass; run a disposable Work canary and compare byte count + SHA-256.

## Result matrix
| Criterion | Result |
|---|---|
| Exact-head configured CI | PASS — #504, 6/6 jobs |
| Component test inventory | PASS (inventory only; not An execution) |
| An independent local/native reproduction | NOT RUN — no direct test runner available in this session |
| Parent-swap/reparse-point containment | FAIL |
| Restart reconciliation/directory durability | FAIL / NOT PROVEN |
| Core revoke/finalize atomicity | BLOCKED |
| Build MCP raw-byte registration | BLOCKED |
| Live Sandbox byte-for-byte readback | NOT RUN |
| Formal Ka/An PR review approvals | NOT RECORDED |

## Required next actions
1. Xu keeps PR #77 open/unmerged and Execution Gate CLOSED.
2. Vi implements handle-safe filesystem containment and hostile race tests on Windows + Linux.
3. Vi implements full restart reconciliation and directory durability/fault-injection tests.
4. Xu obtains a distinct Core-owned `sandbox.file.upload` grant contract with atomic revoke/finalize semantics; do not assume execution grants are interchangeable.
5. Vi adds raw-byte Build MCP transport/registration only after the security gates pass.
6. An retests the corrected exact head, runs adversarial race/revocation tests, then performs the live disposable Sandbox SHA-256 canary.

**FINAL:** PR #77 BLOCKED / NOT ACCEPTED. Work 28 ACTIVE / INTEGRATION BLOCKED / NOT RELEASED. Execution Gate CLOSED. No merge, deployment, live upload capability, PC transfer or release approval is claimed.

[KÝ: AN | TESTER]
