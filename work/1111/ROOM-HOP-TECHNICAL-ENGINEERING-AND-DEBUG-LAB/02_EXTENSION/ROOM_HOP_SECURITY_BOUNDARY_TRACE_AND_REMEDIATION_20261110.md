# ROOM-HOP Security Boundary — Technical Trace & Remediation Tracker

- **Record date:** 2026-11-10 (UTC+7)
- **Owning Work:** 1111 — ROOM-HOP Technical Engineering & Debug Lab
- **Related Work:** W32 (DOC-117), W70 (lifecycle / governance), W01 (Gateway), W02 (authorization policy), W28 (execution authority/grants), W99 (entry gate), W112 (cross-Work contracts/evidence)
- **Repository:** hqtt2026-thevinhvtqni/room-meeting-ai
- **Disposition:** ACTIVE INVESTIGATION / PREPARATION ONLY
- **Security gate:** PROTECTED EXECUTION DENIED — NOT RELEASED
- **Source/runtime modification:** NOT AUTHORIZED by this record

## 1. Purpose and ownership

Consolidate the ROOM-HOP authorization-boundary findings previously discussed across W32 and technical review into one traceable engineering workstream under W1111. This document is the working technical tracker; DOC-003 remains the canonical execution journal. Do not create a parallel journal.

W1111 coordinates source/runtime trace, architecture reconciliation, remediation design, independent QE planning and evidence handoff. It does not override W70 governance, W32's DOC-117 decision, or the owner approval required for protected execution.

## 2. Evidence basis and scope limitations

### 2.1 Evidence already recorded

- W32 **DOC-117 — W32 Scoped Execution Boundary** (2026-11-10): fail-closed target contract selected; enforcement NOT IMPLEMENTED OR VERIFIED. Protected Work32 mutation/execution remains denied.
- Cla's source review report: `work/32/...` report path recorded in the W32 conversation as `06_EVIDENCE/W32-EVIDENCE-CLA-03-CORE-SOURCE-TRACE-ROOM-HOP-CLEAN-ZIP-20261110.md`; corresponding W32 DOC-035 journal entry was reported as W32-LOG-20261110-CLA-02. The report is a read-only source review, not runtime proof.
- Cla reviewed an extracted source/document subset from the supplied ROOM-HOP CLEAN ZIP. The review did **not** cover every Python file or every runtime deployment path. The ZIP did not contain a checkout at the exact PR #49 head. No runtime execution or source modification was performed in that review.
- Xu's subsequent read-only review of selected W01/W02 source files found that the gateway/authentication prototypes are not wired into the live runtime entry path based on the files inspected. This is a scoped finding, not a complete system-wide proof.
- W1111 existing DOC-006 baseline and DOC-007 execution-host trace contain earlier, separate evidence. Their historical findings are not silently upgraded by this tracker.

### 2.2 Important revision/runtime caveats

- PR #49 observed head in the prior review: `06ac86825febfc83032b58adc19aeb32f706725a`; the supplied ZIP checkouts did not match it. Refresh exact head before claiming current source coverage.
- The proxy in front of `/build/mcp` and the live Gateway :8040 deployment were not established by the ZIP source review.
- Current deployed module path, process identity, service configuration, proxy chain, bypass routes and live authorization behavior remain NOT VERIFIED.
- No claim is made that the entire ROOM-HOP source tree has been read. Remaining source directories and call sites must be inventoried explicitly.

## 3. Consolidated technical findings

### F-01 — Generic Sandbox file mutations are not an authorization boundary
The reviewed MCP 8030 implementation exposes `sandbox_write`, `sandbox_append`, `sandbox_create` and `sandbox_delete` without trusted principal, Work/Assignment, action scope, source revision or durable audit authorization in the reviewed handlers. The reviewed `sandbox_create_work` identity check only validates a supplied identity string against agent YAML records. This is source-level evidence from the inspected implementation; live exposure through proxy/runtime is NOT VERIFIED.

**Risk:** a caller reaching the generic file API may mutate Work records or source-adjacent artifacts without the scoped authorization contract required by DOC-117.

### F-02 — Existing governance/policy code is not proven to guard Sandbox mutations
The reviewed governance implementation relies on identity/path-style rules, has an audit path that is not fail-closed, and was not found wired into the inspected Sandbox/MCP mutation handlers. Multiple versions exist; canonical version selection remains unresolved.

**Risk:** the presence of policy code or identity files can create a false impression of enforcement when the actual mutation path does not invoke it.

### F-03 — Gateway/authentication prototypes are not yet proven as the live enforcement point
W01 contains gateway/authentication and Work99 gate prototypes. The inspected gateway runtime proxy forwards caller headers and has no demonstrated trusted authentication/authorization adapter. The Work99 middleware fails closed when a trusted context resolver is absent, but the inspected runtime path did not demonstrate that middleware is mounted on the live /build/mcp route. W02 contains simpler member/capability checks that do not implement the full scoped tuple.

**Risk:** caller-controlled headers, unmounted middleware, or capability-only checks must not be treated as authenticated, Work-scoped authority.

### F-04 — W28 execution-grant work is a candidate, not a complete contract
The reviewed W28 branch includes stronger service-credential/grant/revocation and fail-closed audit concepts. It still lacks evidence for the full Work/Assignment/ACK + exact path/action + exact source SHA + isolated environment + commit-time revalidation tuple required by DOC-117. It is a separate branch and must not be assumed deployed or merged.

### F-05 — Core/Host/Work boundaries are not yet unified end-to-end
The reviewed Core, Execution Host, MCP and Work records do not yet establish one verified authority path from authenticated principal through Work assignment and exact revision to protected mutation/execution and durable evidence. Prior W1111 records separately identify runtime and aggregate-result correctness issues; they remain separate gates and must not be conflated with this authorization incident.

### F-06 — Identity registry is incomplete for operational authorization
The inspected agent YAML directory did not contain all roster identities expected by HQTT, and the reviewed permission/authority fields were empty. A YAML identity name or client-supplied identity string is not proof of authenticated principal.

## 4. Required authorization contract (from W32 DOC-117)

Every protected action must be authorized against one immutable, auditable tuple:

1. Trusted authenticated principal (never client-supplied identity text).
2. Work ID and canonical Work manifest/state.
3. Exact active Assignment and Task, including owner, ACK, state and revocation.
4. Canonical repository and normalized exact path/resource; traversal, symlink and wildcard bypass blocked.
5. Independent action allowlist (e.g. READ, CREATE_DRAFT, WRITE_ASSIGNED_FILE, RUN_NAMED_TEST, DISPATCH_CI).
6. Exact source provenance: repository, branch/ref, commit SHA and target blob/content hash.
7. Named isolated execution environment.
8. Issued-at, expiry, revocation, policy version, gate snapshot, command and idempotency/correlation identifiers.
9. Matching Work Entry, G0–G5 state, Xu READY/EXECUTION_AUTHORIZED decision and recipient ACK.

Any missing, stale, mismatched or unverifiable element => DENY. Revalidate immediately before the protected effect/commit. If durable audit/persistence fails, the protected action must not proceed.

## 5. Work breakdown and acceptance gates

| ID | Work item | Lead / support | Required output | State |
|---|---|---|---|---|
| SEC-01 | Complete source inventory and exact-head trace | Cla / CTO; Xu coordinates | Exact repo/ref/SHA/path map, all mutation/execution entrypoints and call sites, gaps in current ZIP coverage | READY — ACK REQUIRED |
| SEC-02 | Live topology and enforcement-point trace | Cla + Ka | Proxy → Gateway :8040 → MCP :8030 → SandboxService and bypass-route map; runtime identity/build/config evidence | BLOCKED — PC/runtime evidence required |
| SEC-03 | Canonical architecture decision | Xu; Ka review | One approved enforcement architecture reconciling W70/W01/W02/W28/W99/W32/W112 | PENDING — owner decision |
| SEC-04 | Remediation design | Vi / Cla; Xu approves | Trusted principal, scoped grant, policy evaluation, commit-time revalidation, fail-closed audit and migration plan | NOT STARTED |
| SEC-05 | Independent QE matrix | Qw; An as applicable | Positive, negative, bypass, expiry, revocation, path traversal, stale SHA, audit failure and race tests | NOT STARTED |
| SEC-06 | Controlled implementation and integration | Named implementer after authorization | Scoped branch/PR, exact-SHA CI and review artifacts | DENIED until explicit BUILD authorization |
| SEC-07 | Live verification and release gate | Qw independent; Xu coordinates; Vinh owner approval | Runtime attestation, positive/negative live probes, durable audit readback, parity and release decision | BLOCKED / NOT AUTHORIZED |

Task rows above are a planning decomposition, not agent ACKs. No agent is considered IN_PROGRESS until its exact task claim and starting revision are recorded in DOC-003.

## 6. Immediate execution sequence

1. **READ / TRACE:** Cla completes the exact source inventory, including files/call sites omitted from the CLEAN ZIP, and refreshes PR #49 head before tracing.
2. **TRACE RUNTIME:** establish actual deployed proxy/Gateway/MCP route, process/module hashes, configuration provenance and all alternate/bypass paths using read-only evidence.
3. **ANALYZE:** Xu + Ka reconcile the candidate enforcement components and identify one canonical server-side enforcement point; do not compose overlapping policy engines without explicit ownership.
4. **DECIDE:** record the architecture decision and allowed action classes. Protected operations remain denied until Vinh's required approval and the matching execution authorization are present.
5. **BUILD:** only after a separate explicit authorization, implement on a scoped branch; no direct main/source mutation.
6. **VERIFY:** Qw independently tests real runtime paths, including denial cases and audit-store failure. Unit/mock tests alone are insufficient.
7. **HANDOFF:** record exact SHA, test artifacts, readback and residual blockers in DOC-003 and the evidence register.

## 7. Safety and change boundary

Until the gates above are satisfied:

- PREPARATION ONLY.
- PROTECTED EXECUTION DENIED.
- No protected Sandbox/source write, CI dispatch, runner/PC execution, merge, deploy or release.
- No use of caller-supplied identity headers or self-asserted identity as authorization.
- No claim of runtime PASS, complete source coverage, or production readiness.
- Existing generic MCP file-write operations must not be treated as safe authorization or used to modify protected code/security controls while their enforcement weakness remains unresolved.

This document is a technical tracking record, not an authorization grant.

## 8. Evidence and update protocol

Each update must record date/time (UTC+7), actor and verified identity, task ID, exact repository/ref/SHA/path, method/command, evidence artifact, PASS/FAIL/BLOCKED/NOT RUN, scope limitations and next step. Preserve prior observations as dated addenda. DOC-003 is the canonical journal; this document is the consolidated technical tracker; do not create a second journal.

