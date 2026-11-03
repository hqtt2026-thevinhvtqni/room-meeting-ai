# WORK 28 — MASTER EXECUTION PLAN V2.0

**Date:** 2026-11-03  
**Status:** ACTIVE / INTEGRATION BLOCKED / NOT RELEASED  
**Execution Gate:** CLOSED  
**Authority:** Vinh  
**Coordinator / decision owner:** Xu  
**Implementation lead:** Vi  
**Independent architecture/security review:** Ka  
**Independent QA/verification:** An  
**Repository branch:** `work/28-mcp-tooling-platform`

## 1. Product destination

Deliver a production-ready ROOM-HOP MCP Tooling Platform that allows authorized AI/workflow clients to discover capabilities, read and write scoped Work artifacts, submit controlled execution jobs, observe execution state, collect evidence and complete a verifiable handoff.

The product is not merely a collection of tool schemas. It must work end-to-end across:

1. AI/client-facing MCP interfaces;
2. canonical tool registry and versioned contracts;
3. Core :8000 authorization and Work/task authority;
4. Build/Verification MCP :8030;
5. a separately rebuilt Runtime MCP (new implementation, not the historical listener);
6. Execution Host :8031 and process-tree containment;
7. evidence collection, audit and readback;
8. CI, independent review, deployment and rollback.

## 2. Governing decisions

- GitHub branch `work/28-mcp-tooling-platform` is the canonical source of code and controlled Work documents.
- GitHub Actions is the primary repeatable CI evidence lane.
- Exactly four AI participants: Xu, Vi, Ka and An. Co is excluded.
- Core :8000 is the only authorization/application authority.
- MCP Build/Verification :8030 remains the supported build/verification service.
- The historical MCP :8020 listener is quarantined and DO NOT USE. Do not probe, restart, activate, modify, or send traffic to it. Runtime MCP is a clean, separate rebuild. Any future use of the :8020 address requires a fresh deployment identity and explicit migration evidence; it must never inherit the historical process or state.
- Execution Host :8031 is the only approved execution boundary. No arbitrary shell, direct Workspace/DB access, Core bypass, or parallel execution authority.
- Sandbox/MCP 8030 is a supporting verification environment, not an independent source of truth.
- Do not delete historical reports. Preserve and classify them.
- No claim of AI task receipt without acknowledgement evidence; no claim of PASS without an actual run.

## 3. Work packages — complete end-to-end

### WP0 — Baseline and provenance reconciliation
**Lead:** Xu; **support:** Vi; **independent check:** An; **review:** Ka.

- Capture branch HEAD and file-level source state.
- Inventory code, tests, workflows, current MCP 8030 runtime tools and the documented v54 catalog.
- Separate design-only tools, registered tools, real handlers, mock handlers and blocked dependencies.
- Trace provenance for MCP 8030 deployment and source-to-runtime correspondence.
- Reconcile GitHub branch, Sandbox copy and runtime evidence without copying unverified Sandbox state over GitHub.

**Exit:** reproducible inventory with exact commit, source hashes, runtime tool names/schemas and explicit unknowns.

### WP1 — Canonical contracts and tool registry
**Lead:** Vi; **review:** Ka; **verification:** An.

- Establish one authoritative schema/version source.
- Enforce schema validation, bounded arguments, stable error/status envelopes and correlation IDs.
- Ensure registry metadata cannot claim IMPLEMENTED unless a real handler is registered and tested.
- Add schema parity and duplicate/unexplained-tool checks.
- Keep unsupported capabilities visibly BLOCKED.

**Exit:** registry/schema parity tests, valid/invalid invocation tests and no placeholder success.

### WP2 — Execution Host process lifecycle and fail-closed containment
**Lead:** Vi; **review:** Ka; **verification:** An.

- Trace all process creation paths, not only `process_job.py`.
- On Windows, establish Job Object containment before untrusted command code can execute. A process started and only then assigned to a Job Object has a race and is not acceptable as proof of pre-execution containment.
- If Job Object creation/assignment or required containment cannot be established, do not start/continue the command; return BLOCKED with evidence.
- On POSIX, establish process-session/group containment at creation and verify parent/child cleanup.
- Test parent and child processes, timeout, cancellation, spawn/attach failure, cleanup failure, service spawn and concurrent runs on native Linux and Windows runners.
- Keep OS sandbox/isolation status separate from process-tree containment. Do not change `ISOLATION_STATUS=NOT_VERIFIED` without independent evidence of OS isolation.

**Exit:** native Linux and Windows CI, fail-closed failure injection, real process-tree tests and no execution window before containment.

### WP3 — Build/Verification MCP :8030
**Lead:** Vi; **review:** Ka; **verification:** An.

- Preserve the existing Build/Verification role and endpoint contract.
- Trace the deployed service source/provenance and reconcile runtime tools/list with the repository registry.
- Verify sandbox path containment, Work isolation, read/write authorization, size limits, append semantics and readback.
- Keep `sandbox_read()` quarantined from AI-facing use if its known empty-result defect remains; do not repeat it without new error evidence. Use the proven diagnostic path only for investigation.
- Verify tools/list, schema and safe invocation against exact deployed build identity.

**Exit:** source provenance closed, runtime registry parity, safe read/write smoke evidence and repeatable verification.

#### WP3 feature package — Binary file upload to Work Sandbox
**Feature ID:** W28-WP3-F01 — `sandbox_upload_file`
**Implementation:** Vi; **architecture/security review:** Ka; **independent verification:** An; **coordination and acceptance:** Xu.

**Objective:** Provide an authorized, auditable way to transfer original binary files (including ZIP archives and nested source bundles) into the correct Work Sandbox without converting them to text or changing their bytes. This is a shared platform capability, not a Work 0001-only workaround.

**Required behavior and contract:**
- Add a registered, versioned `sandbox_upload_file` tool (or a formally documented streaming upload contract if the transport cannot safely carry a single large payload). Tool discovery, schema, handler and runtime implementation must agree; no placeholder handler or false success.
- Accept binary content without UTF-8/text conversion. Preserve exact bytes, filename and authorized destination path; support ZIP and common document/data/image formats without format-specific mutation.
- Enforce Core-authorized identity, Work ID and destination scope. Reject traversal, absolute-path escape, symlink escape, unauthorized overwrite and cross-Work writes. Default to no overwrite unless an explicit authorized overwrite contract is approved.
- Apply configurable per-file and per-Work quotas, maximum size, bounded streaming/chunking, timeouts, cancellation and safe temporary staging. Do not buffer unbounded payloads in memory.
- Verify byte count and SHA-256 before atomic promotion to the destination. On interruption or mismatch, clean up the partial object and return BLOCKED/FAIL with correlation ID and evidence; never report success for a partial upload.
- Return a stable result containing Work ID, normalized destination, byte count, SHA-256, upload ID, service/build identity and final status. Do not expose secrets or local host paths.
- Record append-only audit evidence for actor, authorization decision, destination, size, checksum, timestamps, outcome and correlation ID.
- Provide a readback/metadata verification path that confirms stored size and SHA-256. Test duplicate filenames, large files, zero-byte files, invalid names, traversal, symlinks, quota limits, interrupted transfers, checksum mismatch, cancellation, concurrent uploads and overwrite denial.
- Define Sandbox-to-GitHub publication as a separate controlled operation. Do not claim automatic two-way synchronization until binary Git object creation, commit, readback and checksum parity are implemented and tested. Keep GitHub as canonical source for controlled code/documents; Sandbox remains supporting storage/verification.

**Acceptance evidence:** exact source commit and deployed build identity; registered tool/schema parity; authorization and path-isolation tests; bounded-memory/large-file tests; failure-injection results; byte-for-byte readback and matching SHA-256; independent Ka review and An reproduction; CI run references. Until all evidence exists, mark the feature NOT VERIFIED and retain the source file at its original location.

### WP4 — New Runtime MCP (clean rebuild)
**Lead:** Vi; **review:** Ka; **verification:** An.

- Build a new Runtime MCP implementation in a clean source/deployment boundary.
- Do not reuse, attach to, or depend on the historical MCP :8020 listener, its process, files, credentials, cache or state.
- Define the runtime contract, identity propagation, request correlation, bounded transport, health/readiness and graceful shutdown.
- Runtime MCP may request operations but cannot authorize them; Core :8000 remains authoritative.
- Runtime must call only the approved Execution Host :8031 contract for execution.

**Exit:** independent service identity, clean deployment provenance, contract tests, authorization-denial tests and controlled runtime smoke evidence.

### WP5 — Core :8000 authority integration
**Lead:** Vi; **review:** Ka; **verification:** An.

- Trace and use the existing approved Core routes/contracts; do not invent endpoints.
- Validate principal, Work ID, task/run identity, authorization decision and capability scope.
- Ensure cross-Work access cannot leak data and returns the approved indistinguishable NOT_FOUND behavior.
- Ensure Core owns authorization and task lifecycle; MCP/Runtime/Execution Host cannot self-authorize.
- Test denied, expired, malformed, replayed and mismatched-context requests.

**Exit:** real authenticated integration evidence; mocks prove only local contract behavior.

### WP6 — Evidence, audit and handoff
**Lead:** Vi; **review:** Ka; **verification:** An; **coordination:** Xu.

- Correlate request_id, task_id, run_id and execution_id.
- Capture source commit/build hash, runtime identity, start/end time, exit code, status, safe stdout/stderr references, artifacts and readback.
- Redact secrets; bound output sizes; preserve append-only evidence.
- Distinguish DONE, PASS, FAIL, BLOCKED, DENIED and NOT_VERIFIED accurately.
- Make every result traceable to exact code and CI run.

**Exit:** complete evidence chain from request to result and independent reproduction.

### WP7 — Product integration, release and operations
**Lead:** Xu; **implementation:** Vi; **review:** Ka; **verification:** An.

- Run complete MCP → Core → Runtime MCP → Execution Host → evidence/readback E2E.
- Run security, regression, compatibility, failure-recovery and concurrency tests.
- Verify start/stop scripts, service ports, health checks, logs, deployment identity and rollback.
- Prepare operator guide, architecture, API/tool catalog, troubleshooting and known limitations.
- Release only after all required gates pass and release authority is recorded.

**Exit:** release candidate with complete evidence, reviewed PR, verified rollback and no unresolved critical/high risk.

## 4. Execution cadence and autonomous behavior

- Xu coordinates the whole plan and maintains one canonical journal; do not ask Vinh to approve every small implementation step.
- Vi works from the current branch HEAD, makes reviewable commits and reports exact changed paths, tests and blockers.
- Ka reviews architecture/security and diffs independently; findings must include severity, evidence, remediation and retest criteria.
- An independently reproduces targeted tests and CI; a developer's self-report is not QA evidence.
- Xu resolves decisions inside delegated scope. Any irreversible production change, credential change, release, migration affecting existing consumers or action outside the approved boundary remains blocked for explicit authority.
- Each handoff includes the complete task, context, acceptance criteria, evidence location and next owner. No fragmented micro-assignments.
- When PC-side or live service access is unavailable, continue all safe GitHub/source/CI work and mark only the specific live verification BLOCKED. Never fabricate PC evidence.

## 5. Acceptance gates

| Gate | Required evidence | State |
|---|---|---|
| G0 Source truth | branch/commit/provenance inventory | OPEN |
| G1 Contracts | approved registry, schemas, version and parity tests | NOT VERIFIED |
| G2 Execution safety | pre-execution containment, fail-closed and native Linux/Windows evidence | NOT VERIFIED |
| G3 Build MCP | :8030 provenance, tools/list parity, safe I/O and binary upload/readback with SHA-256 evidence | NOT VERIFIED |
| G4 Runtime MCP | clean rebuild, identity, contract and security tests | NOT VERIFIED |
| G5 Core authority | authenticated Core integration and denial tests | NOT VERIFIED |
| G6 E2E | complete request-to-evidence trace and independent reproduction | NOT VERIFIED |
| G7 Release | reviewed candidate, rollback, runbook and approval | CLOSED |

## 6. Current baseline and known blockers

- Current Work status remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED.
- The current Windows process lifecycle implementation calls process creation before Job Object attachment, then evaluates the gate. This leaves a possible pre-attachment execution race and must be fixed before WP2 acceptance.
- Existing unit tests include simulated missing-Job-Object gate tests; those do not prove the native Windows process is suspended until containment is attached.
- `ISOLATION_STATUS` is explicitly `NOT_VERIFIED`; Job Object containment is not OS sandboxing.
- Binary Sandbox upload is an explicit WP3 feature requirement (W28-WP3-F01); implementation and runtime evidence are pending. Do not claim `sandbox_upload_file` exists until verified.
- The historical MCP :8020 listener is not a valid test target.
- Existing architecture and continuation documents contain older assumptions about :8020 and prior team roles. This V2 plan and the current manifest supersede conflicting older instructions; preserve old files as historical context.

## 7. Reporting format

Every checkpoint reports:
- **DONE:** artifact/code actually changed, with commit.
- **PASS:** exact test command/run and successful result.
- **DECISION:** chosen option and rationale.
- **BLOCKED:** problem, attempts/evidence, bottleneck, available options and missing condition.

No silent status promotion. Work remains NOT RELEASED until G0–G7 are satisfied.
