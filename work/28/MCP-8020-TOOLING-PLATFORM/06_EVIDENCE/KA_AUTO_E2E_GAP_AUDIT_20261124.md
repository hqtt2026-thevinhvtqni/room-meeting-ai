# WORK 28 — KA AUTO E2E GAP AUDIT

**Document ID:** W28-KA-AUD-116  
**Priority:** P0  
**Owner:** Ka — CSA / Technical Delivery  
**Date:** 2026-11-24 (Asia/Ho_Chi_Minh)  
**Target:** PR #78 — `xu/w28-f02-tests-20261124`  
**Observed PR HEAD before this report:** `3be7a02ffe584c735af7df598af70fdbf02ef3ca`  
**Canonical base observed:** `work/28-mcp-tooling-platform` @ `1d7c92294a0c68f109da9e07af9ad6d49566ea75`

## 1. Purpose and authority

This audit executes Vinh's delegation dated 2026-11-24: Ka continues Work 28 through implementation, Auto E2E, independent acceptance and handover. This report records verified state and the next controlled build gates. It does not authorize merge, deployment, upload enablement or opening the Execution Gate.

## 2. Source and branch trace

- PR #78 is OPEN / DRAFT / UNMERGED; GitHub reports mergeable=false.
- Compare against canonical branch: DIVERGED, 54 commits ahead and 4 commits behind; merge base `4b2a8663a0b9ff40aad8e6812efff197b5085de5`.
- PR changed files at audit time: Work 28 workflow, canonical journal, upload engine, upload tests, and historical An PR #77 acceptance report.
- The PR branch's native-Windows component test job runs `test_sandbox_binary_upload_v1.py`; this is component CI, not deployed product E2E.
- Its machine report summarizes configured CI job outcomes and explicitly records deployed E2E as BLOCKED. It does not invoke the canonical `work28_auto_e2e_gate_v1.py` evaluator or validate a trusted deployment attestation.
- Exact-head workflow lookup returned no run for PR HEAD `3be7a02...` or implementation commit `665cc605...`. No CI PASS is claimed for those revisions.

## 3. Independent security disposition

Ka's PR #78 review COMMENT is recorded as review ID `6043253986`, anchored to `3be7a02ffe584c735af7df598af70fdbf02ef3ca`. Verdict: NOT ACCEPTED; P0 findings remain open. GitHub did not permit REQUEST_CHANGES because the connected identity is the PR author; the COMMENT is not a formal blocking review event.

### F01 — Filesystem containment: BLOCKED

Pathname-based resolve/check followed by open/mkdir/link/stat/unlink remains vulnerable to TOCTOU and Work-root aliasing. Required:
- POSIX descriptor-relative traversal and operations (`dirfd`, `O_NOFOLLOW`, openat-style APIs).
- Separately reviewed Windows handle/reparse-point containment and safe promotion.
- Adversarial parent-swap, symlink and reparse-point tests on native platforms.
- Fail closed where the platform cannot provide the required guarantee.

### F02 — Recovery and durability: PARTIAL / NOT VERIFIED

Sandbox-root enumeration was added in implementation commit `665cc6056f07364db4e42067559fb95e76ce9660`, closing a previously missed zero-session orphan discovery path by design. It is not yet test/CI evidence. Required:
- Root enumeration failure, symlinked Work root, symlinked staging directory and symlinked staging entry tests.
- Orphan preservation/quarantine policy, including a Work with no SQLite session.
- Crash-point matrix across staging creation, chunk bytes, ledger commit, FINALIZING, final promotion, readback, staging cleanup and audit.
- Directory-entry durability or an explicit platform limitation that blocks acceptance.
- Multi-process recovery/locking and quota/session reconciliation.

### F03 — Core upload authority: BLOCKED

FakeCore/component authorizer tests are not real Core integration. Required:
- Approved Core-owned upload grant contract and schema.
- Server-derived principal and Work mapping; no caller-supplied trusted context.
- Durable revocation epoch and atomic revoke-vs-finalize semantics at the real Core transaction boundary.
- Negative tests for revoked, expired, wrong-Work and wrong-audience grants with zero filesystem side effects.

### F04 — MCP raw-byte transport and live integration: BLOCKED

No live raw-byte upload/readback action is exposed in the connected MCP 8030 tool surface inspected for this audit. Required:
- Bounded raw-byte begin/chunk/finalize/abort transport and exact tool registration.
- Live `tools/list` identity/schema parity against the approved contract.
- Disposable Sandbox canary, byte-for-byte readback, independently computed SHA-256 and durable audit correlation.

## 4. Auto E2E acceptance model

Do not collapse component CI into product E2E. Maintain two distinct evidence layers:

1. **Exact-SHA CI:** source checkout identity, Linux/Windows component tests, regression suites, artifact build, checksum, extracted-source retest, machine-readable report.
2. **Trusted live product E2E:** deployment identity and revision, live MCP tool identity/schema, Core-derived authorization grant, runtime/Work isolation, raw-byte transfer, independent readback SHA-256, durable audit and protected evidence artifact.

The product E2E evaluator must consume trusted deployment-held evidence, bind every stage to one immutable source/deployment identity, reject missing or contradictory evidence, and fail closed. A CI job that writes a report saying E2E=BLOCKED is a precondition report, not an E2E PASS.

## 5. Immediate build order

1. Reconcile PR #78 against the latest canonical base without blind merge or force-push; inspect the four behind commits and resolve conflicts deliberately.
2. Implement F01 handle-safe filesystem boundary before expanding upload exposure.
3. Complete F02 crash/durability matrix and native Linux/Windows evidence.
4. Obtain approved F03 Core contract and implement atomic authority/finalize semantics.
5. Implement F04 raw-byte MCP transport/registration only against the approved Core contract.
6. Run exact-SHA CI, then trusted live Auto E2E in a disposable Sandbox.
7. Obtain independent QA and security review on the exact final revision; assemble acceptance minutes, journal, artifact hashes, rollback and handover package.

## 6. Evidence and limitations

- GitHub PR metadata and commit/compare data were read directly for the exact refs above.
- Sandbox Work 28 journal append entries JRN-W28-114 and JRN-W28-115 were read back successfully through the diagnostic read probe; this confirms Sandbox persistence only, not GitHub canonical journal synchronization.
- No source test, CI job, live Core call, MCP upload, Sandbox binary readback or deployment was executed by this audit.
- No test is claimed PASS. No release or acceptance is claimed.

## 7. Decision

**NO-GO — NOT ACCEPTED.** Keep PR #78 DRAFT / UNMERGED, Execution Gate CLOSED, and Work 28 ACTIVE / INTEGRATION BLOCKED / NOT RELEASED. Do not register, deploy or enable binary upload until F01–F04 and all exact-SHA/live Auto E2E/independent QA gates have evidence.

**Signed:** Ka — CSA / Technical Delivery  
**Date:** 2026-11-24
