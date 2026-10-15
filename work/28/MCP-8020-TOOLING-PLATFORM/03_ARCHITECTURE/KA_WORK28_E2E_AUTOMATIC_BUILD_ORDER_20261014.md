# KA — WORK 28 E2E AUTOMATIC BUILD ORDER
Date: 2026-10-14 (+07)
Authority: Vinh. Technical lead: Ka. Status: ACTIVE / NOT LOCKED.
Decision: NO-GO for enabling Python execution until security, approved-runner tests, canonical runtime and live E2E are evidenced.

## Definition of done
Authenticated MCP request -> Core authorization and WorkContext -> immutable source snapshot and SHA-256 -> isolated canonical runtime -> trusted result derivation -> protected evidence -> independent readback by Go. Automatic repair/retest must preserve prior runs and evidence, require policy approval for each mutation, and never self-approve.

## Locked boundaries
- Core :8000 remains the sole authorization and WorkContext authority. MCP :8020 is an adapter.
- Do not create a second execution host or invent a route before tracing the existing W12/W13/Work 27 seam.
- Never trust caller-supplied authorized, identity, status, work ownership or evidence summaries.
- No arbitrary shell/command/interpreter/cwd/environment/argv exposed to callers.
- OS isolation must prove no host secrets, no network/host loopback, least privilege, resource quotas and process-tree cleanup.
- Lexical path checks do not replace canonical filesystem containment and symlink/reparse-point rejection.

## Work packages
### WP0 — deployed source/runtime inventory (Ka coordinates; PC evidence needed)
Record MCP/Core process identity, deployed revisions, registered tools, authenticated principal source, Core WorkContext route, canonical runtime API, runtime identity, isolation mechanism and evidence storage. Output: 06_EVIDENCE/KA_PC_RUNTIME_SOURCE_MAP_20261014.md. Until deployed/source revisions align, G1 remains PARTIAL and live execution BLOCKED.

### WP1 — contract hardening (Sandbox-only until approved runner)
Review 04_CODE/tool_contracts.py and 05_TEST/test_tool_contracts.py. RUN_TESTS must require explicit integer counters (bool rejected): tests_run >= 1, failures=0, errors=0, skipped=0. Missing counters must fail closed. Verify expected/discovered/executed test inventory, not merely some tests running. RUN_SCRIPT and RUN_TESTS need distinct validation. PASS requires trusted server-generated run_id, source hash, exit code, evidence reference, runner identity, timestamps and validated result manifest. Add regressions for missing counters, all-skipped, boolean counters, wrong inventory, forged status, replay, absent evidence, nonzero exit and zero discovered tests. Canonical command must work from documented root without ad-hoc PYTHONPATH. No G3 PASS until approved-runner command/output/exit code/revision are captured.

### WP2 — independent security review (Cla owns)
Review forged authorized/principal, cross-Work access, path traversal, symlink/reparse-point races, Unicode/path ambiguity, host secrets, network/loopback, process escape, quotas, timeout/tree cleanup, evidence tamper/delete/overwrite, replay, output limits and secret redaction. Output: 06_EVIDENCE/CLA_AUTOMATIC_E2E_SECURITY_REVIEW_20261014.md. Cla retains security veto.

### WP3 — canonical adapter integration
Only after WP0-WP2 pass. Integrate at existing MCP/Core seam; Core resolves principal and WorkContext. Runtime receives immutable snapshot reference and approved operation profile, not arbitrary command strings. Enforce ownership on status/output/cancel, server-side request_id/run_id, idempotency and QUEUED/RUNNING/terminal states.

### WP4 — isolated runtime proof
Demonstrate no host secrets/network/loopback, least privilege, CPU/RAM/PID/disk/output/time quotas, complete process-tree cleanup, immutable source snapshot and protected evidence storage. If any control is unproven, NO-GO.

### WP5 — independent live E2E (Go owns)
Test valid smoke; intentional failure; zero/all-skipped tests; timeout/tree cleanup; forged principal; cross-Work denial; traversal/symlink denial; source mutation after snapshot; evidence tamper; approved patch -> new hash -> rerun while preserving old evidence; status/output/readback consistency. Capture deployed SHAs, request_id/run_id, WorkContext, source hash, runtime identity, profile ID, exit code/status/timestamps and evidence hash. Output: 06_EVIDENCE/GO_AUTOMATIC_E2E_ACCEPTANCE_20261014.md.

### WP6 — release gate
Release only when Cla security and Go live acceptance both PASS, all critical/high findings close, deployed/source revisions align and evidence integrity/readback succeeds. Otherwise Work remains ACTIVE / NOT LOCKED.

## Current evidence (2026-10-14)
- Work 28 Sandbox and manifest are discoverable; contract and tests can be read through MCP.
- Read contract version is 1.1.0. No approved runner execution was performed in this session.
- Inbox query for identity cla returned empty; writing Sandbox documents is not task dispatch.
- Live MCP -> Core -> canonical runtime -> protected evidence has not been demonstrated.
- python_run is NOT REGISTERED / NOT ENABLED. G3-G6 BLOCKED.

## Immediate order
1. Collect read-only PC process/revision/route evidence.
2. Make WP1 changes in a reviewable isolated slice and add red tests; keep NOT EXECUTED until approved runner evidence exists.
3. Dispatch Cla/Go only through verified Core task dispatch, not by claiming Sandbox notes reached their inboxes.
4. Do not expose Python execution while WP0-WP4 remain unproven.
