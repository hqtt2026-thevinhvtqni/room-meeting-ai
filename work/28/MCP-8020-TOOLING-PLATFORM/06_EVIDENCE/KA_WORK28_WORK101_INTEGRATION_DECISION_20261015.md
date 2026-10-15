# KA — WORK 28 / WORK 101 INTEGRATION DECISION
Date: 2026-10-15 (+07)
Authority: Vinh
Technical owner: Ka / CSA
Status: SOURCE AUDIT CONTINUED; LIVE EXECUTION BLOCKED; TOOL REGISTRATION NO-GO

## 1. Scope and evidence boundary

This decision is based on read-back from ROOM-HOP MCP Sandbox:
- Work 28: `04_CODE/tool_contracts.py`, `05_TEST/test_tool_contracts.py`,
  `06_EVIDENCE/CO_WORK28_TOOL_CONTRACT_AUDIT_20261015.md`,
  `06_EVIDENCE/XU_WP1_TEST_SUMMARY_HARDENING_20261014.md`.
- Work 101 inventory includes `ROOM-HOP-DUAL-WORKSPACE/00_ROOT/SYNC_TARGET.yaml`,
  integration trace, runtime probe and live-tools-list evidence files.
- The ROOM-HOP context states Core :8000 is the single source of truth,
  MCP :8020 is the agent boundary, Sandbox is the build zone, and AI must not
  commit, push, merge or modify MAIN SOURCE.

Sandbox inventory confirms Work 28 and Work 101 are present. This is not proof
of current PC process identity or live MCP registry/source correspondence.

## 2. Work 28 source findings

Observed in the current Sandbox copy:
- Contract version is 1.1.0.
- `ToolResult` is a pure data/shape validator, not an authorization service,
  execution adapter, evidence store, or runtime attestation mechanism.
- `ToolResult.operation_kind` defaults to READ. A trusted adapter must derive
  operation kind and execution operation from the server-side route/policy,
  never accept caller fields as authority.
- RUN_TESTS PASS checks run_id, exit_code=0, non-empty evidence_ref,
  syntactically valid source_sha256, and explicit integer tests_run/failures/
  errors/skipped counters; tests_run must be >=1 and all other counters 0.
- The test source has 19 test methods. That is source inventory only. Discovery,
  execution, exit code and test output are not available.
- A syntactically valid digest and non-empty evidence_ref do not prove that
  a snapshot was hashed, evidence exists, evidence is immutable, or readback
  matches the runtime result.

## 3. Architecture decision

Keep this single trust chain:
MCP :8020 -> Core :8000 (authenticated principal + WorkContext + operation
authorization) -> existing approved W12/W13 / Work 27 runtime -> protected
evidence store -> authorized readback -> independent verifier.

No direct MCP-to-process execution; no caller-controlled `authorized`;
no new Core, bridge, listener or execution host. Do not register python_run.

## 4. Work 101 boundary

Work 101 owns sync planning, target binding, base/source/destination revision
comparison, conflict detection, approval tracking and evidence. It must consume
typed, Core-authorized Work 28 capabilities; it must not implement a competing
runtime or bypass Core. Keep SYNC_TARGET UNBOUND / DRY_RUN with writes, merge
and release disabled until separately approved.

Read-only capabilities should be separately typed from mutation/execution:
- inspect_target
- read_source_snapshot
- compare_revisions
- create_sync_plan
- verify_content_digest
- read_back_evidence

Any future mutation requires a distinct operation, server-derived authorization,
a bound target/revision, approval bound to the exact digest and destination,
idempotency enforcement, and post-write readback. This document does not grant
such permission.

## 5. Required gates

G0 — Identify live PC source/runtime and obtain raw read-only MCP tools/list.
G1 — Run canonical Work 28 unit tests in approved runner; retain command,
Python/runtime identity, source SHA, raw stdout/stderr, exit code, and counts.
G2 — Add adapter-boundary negative tests for forged PASS, missing/replaced
evidence, wrong snapshot hash before process creation, replay/key reuse,
spoofed principal, cross-Work read/cancel, and operation-kind spoofing.
G3 — Prove Core-derived identity/WorkContext and authenticated transport to
the existing approved runtime.
G4 — Prove OS isolation, process-tree cleanup, resource/network limits and
runtime identity/attestation.
G5 — Prove evidence is protected, immutable to the caller, hash-verifiable,
and can be read back through the authorized path.
G6 — Run live MCP -> Core -> runtime -> evidence -> readback acceptance;
Cla performs independent security review and Go performs independent E2E.
G7 — Only after all required gates pass may Vinh consider tool registration
and separately authorize any write/sync/release capability.

## 6. Canonical unit test command

From the Work 28 root in the approved runner:
`python -m unittest discover -s 05_TEST -t . -v`

Capture at minimum: command, timestamp, Python version, runtime/runner identity,
git/source revision if applicable, SHA-256 of the tested source snapshot,
discovered and executed test counts, failures, errors, skipped, stdout/stderr,
exit code, run ID, and evidence readback. Do not treat absent counters as zero.

## 7. Decision and next action

DONE: Sandbox source inventory and architecture boundary have been re-read.
DONE: Existing contract behavior and its evidence limits are documented here.
BLOCKED: Test execution, live registry/source binding, Core-to-runtime path,
OS isolation, protected evidence, and full live E2E have not been demonstrated.
NO-GO: python_run registration, live registry change, PC/GitHub writes, sync,
merge and release.

Next implementation slice: establish the live read-only identity chain first:
capture raw MCP tools/list on PC and bind it to the exact listener PID,
executable/source revision and runtime configuration. Then run the canonical
unit test command in the approved runner. Do not invent an endpoint or infer
runtime availability from a prior initialize/HTTP 200.

No claim in this report means a test process was executed or E2E passed.
