# WORK 17 — Authorization Remediation Reconciliation

- Work: 17 — ROOM-HOP AI Agent Capability Baseline & Focused Enablement
- Date: 2026-11-19 (UTC+7)
- Coordinator: Xu / AI-01
- Source baseline: GitHub main snapshot read during this review; Work 17 Core/Auth trace and Work 1111/W28/W32 records fetched from main.
- Disposition: READ / TRACE / ANALYZE COMPLETE FOR THIS RECONCILIATION; DESIGN HANDOFF ONLY.
- Security: PROTECTED EXECUTION DENY / NOT RELEASED.
- This document is a cross-Work reconciliation note, not a new authorization policy, coder assignment, or implementation approval.

## 1. Executive finding

Work 17 Entry 014 identifies a P0 source-level trust-boundary defect in the inspected Execution Host HTTP path: the request supplies WorkContext.authorized=true and the Host path trusts that boolean after local context/path checks. The inspected bridge does not attach a Core bearer grant or service credential. The inspected Core entrypoint/adapter did not show the Work execution-grant routes mounted. The command allowlist is broader than the documented pytest-only purpose contract.

This is a source-level finding only. It does not prove that the Host endpoint is publicly reachable. Live process, bind address, proxy/authentication perimeter, deployed source revision and runtime behavior remain NOT VERIFIED.

## 2. Cross-Work reconciliation

### W32 DOC-117 — controlling boundary

The W1111 security tracker records DOC-117 as the governing fail-closed contract. Each protected effect must bind one immutable, auditable tuple:
1. Trusted authenticated principal and authentication provenance.
2. Work ID plus canonical Work manifest/state revision.
3. Exact active Assignment and Task, owner, ACK, state and revocation.
4. Canonical repository and normalized exact path/resource; reject traversal, symlink escape, wildcard and alias bypass.
5. Explicit action allowlist.
6. Exact source provenance: repository, ref, commit SHA and target blob/content hash.
7. Named isolated execution environment.
8. Issued-at, expiry, revocation, policy version, gate snapshot, command and correlation/idempotency identifiers.
9. Work Entry and applicable gates, Xu READY/EXECUTION_AUTHORIZED decision and recipient ACK.

Any missing, stale, mismatched or unverifiable element => DENY. Revalidate immediately before protected effects/commit. Audit/persistence failure => DENY. DOC-117 enforcement itself remains NOT IMPLEMENTED OR VERIFIED in the W1111 record; do not claim it is already enforced.

### W28 — candidate design, not authority

W1111's existing tracker explicitly classifies W28 grant work as a candidate only. The reviewed W28 material contains stronger service-credential, grant/revocation and fail-closed audit concepts, but does not establish the complete DOC-117 tuple, isolated environment and commit-time revalidation. W28 is a separate branch/workstream and must not be assumed deployed, merged or authoritative. Its runbook also describes a gate requiring exact source commit, runtime/Host identities, registered tool-list digest, trusted principal/Core authorization, canonical Work/snapshot/source hash, OS-isolation attestation, actual exit code, process cleanup, protected evidence and matching read-back hash. A reported PASS string is not sufficient evidence.

### Work 17 Entry 014 — bounded source trace

The inspected source path has these gaps:
- Core grant route mounting was not found in the inspected Core entrypoint/adapter.
- Host HTTP handler parses caller-supplied WorkContext and invokes execution; service authentication/Core validation was not found in that handler.
- WorkContext exposes caller-supplied authorized boolean; local validator trusts it.
- Bridge sends WorkContext JSON without bearer grant/service credential.
- Command policy accepts interpreters/tools beyond pytest-only contract.
- Existing tests exercise local authorized=True behavior and an unconfigured Core grant URL response; they do not prove configured grant issuance/validation/revocation and Host integration.

These findings align with the broader W1111 trust-boundary tracker; they do not establish that every other route or deployed runtime has been inspected.

## 3. Existing implementation ownership — preserve, do not duplicate

W1111-T07 is already decomposed into three non-overlapping coder packages. Its current execution plan explicitly states that only Co, Vi and Xuco are the active coder roster; no additional reviewer, QA agent, architect or other AI is assigned. This reconciliation respects that constraint and does not dispatch or assign Cla, Ka or Qw.

| Existing task | Owner | Reconciliation / required outcome |
|---|---|---|
| W1111-T07-CO | Co | Own the single canonical trusted-principal and authorization/grant contract, policy decision API, expiry/revocation and durable fail-closed audit. Include Work/Assignment/ACK, exact resource/action, source revision and environment bindings. |
| W1111-T07-XUCO | Xuco | Enforce Co's contract at actual Gateway/MCP/Sandbox mutation entrypoints; inventory deployed route and bypass paths; normalize paths/actions; revalidate before mutation; audit failure blocks the effect. |
| W1111-T07-VI | Vi | Enforce the same grant at Host execution time; remove caller-controlled authorization; verify source/purpose/expiry/revocation immediately before execution; enforce named isolation and narrow pytest command profile; preserve truthful result/evidence integrity. |
| Integration | Xu | Resolve one canonical contract and dependency order; reconcile exact base/source SHA and environment; ensure downstream consumers use the same policy API; maintain fail-closed disposition and evidence traceability. |

Task board status remains READY — ACK REQUIRED for the three child tasks. This reconciliation does not change status to IN_PROGRESS and does not infer delivery/ACK.

## 4. Acceptance sequence (design handoff; not executed)

1. **Identity and grant contract (Co):** trusted service/principal authentication; immutable typed tuple; short-lived scoped grant; expiry/revocation; durable append-only audit; deterministic ALLOW/DENY reason codes.
2. **Enforcement choke points (Xuco):** trace actual request path and every direct/internal mutation route; authenticate server-side principal; deny unknown actions; normalize paths and block traversal/symlink/wildcard/alias bypass; revalidate immediately before effect; fail closed on audit failure.
3. **Execution boundary (Vi):** Host service authentication; no caller-controlled authorized boolean; online grant validation and revocation; exact Work/purpose/source binding; named OS-isolated environment; enforce pytest-only command semantics in code; protect evidence and result correlation.
4. **Negative and positive evidence:** missing/invalid/spoofed principal; wrong Work/task/path/action/source/environment; absent ACK where required; expired/revoked/replayed grant; stale source; arbitrary Python/shell/node/git; Core unavailable; audit store unavailable; timeout; concurrent revoke; idempotency/replay; valid narrow pytest request. Record raw outputs, exact commit, environment identity, timestamps and evidence hashes.
5. **Independent verification and release gate:** required independent QE/security review must not be self-approved by implementation owner. Current W1111 task plan does not assign an additional reviewer/QA agent. Therefore independent verification remains a separate unresolved gate and must not be silently waived or represented as Xu self-approval. Protected execution remains DENY until the governing authority and required independent evidence are satisfied.

## 5. Open blockers / explicit non-claims

- W32 DOC-117 enforcement: NOT IMPLEMENTED OR VERIFIED per W1111 tracker.
- W28 grant candidate: not established as deployed/merged or complete against DOC-117.
- Work 17 Core/Auth E2E: NOT PASS; GAP-04 OPEN; GAP-11 P0 OPEN.
- W1111 child tasks: READY — ACK REQUIRED; no ACK, implementation start or coder availability inferred.
- Independent QE/security verification: REQUIRED, but not assigned under the current three-coder-only W1111 plan.
- Runtime exposure, proxy perimeter, active PID, bind address and deployed build identity: NOT VERIFIED.
- No protected execution, source/runtime mutation, CI dispatch, merge, deploy, release, permission grant, secret change or test execution occurred in this reconciliation.

## 6. Handoff

This note supplies Xu's cross-Work architecture reconciliation for the existing W1111-T07 owners. It is not a new task board, does not replace W1111 DOC-003 or the technical tracker, and does not alter the existing task allocation. The next safe action is for the already-named owners to ACK their existing task with exact identity, task ID, base SHA, branch, scope and intended outputs; only then may work proceed within the exact authorized scope. Until a valid authorization tuple and required independent evidence exist, protected execution remains DENIED.
