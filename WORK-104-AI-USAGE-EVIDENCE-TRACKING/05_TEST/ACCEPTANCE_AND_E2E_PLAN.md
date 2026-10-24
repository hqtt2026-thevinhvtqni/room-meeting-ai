# Work 104 — Acceptance and E2E Plan

Status: PLANNED — no test result is claimed yet.

## Necessary conditions before implementation
- [ ] Inventory current provider invocation paths and adapters with file/API evidence.
- [ ] Confirm Core/Sandbox boundary and persistence choices.
- [ ] Agree event schema, privacy rules, source labels and acceptance gates.
- [ ] Document pricing source/version policy.

## Sufficient conditions for PASS
### Schema and attribution
- [ ] Every captured event has unique ID, timestamp, type and source.
- [ ] AI identity and Work/task correlation are attached where known; missing correlation is explicit.
- [ ] Multiple providers' usage fields fit without corrupting the common schema.

### Accuracy and cost
- [ ] Preserve provider-reported usage and source/category metadata.
- [ ] Missing usage is null/unavailable, not fabricated zero.
- [ ] Cost calculation uses versioned provider/model pricing and records inputs.
- [ ] Estimated cost is distinguishable from actual billing.
- [ ] Reconcile a sample against provider response or billing evidence.

### Reliability
- [ ] Duplicate events/retries are idempotent.
- [ ] Timeout, provider error, storage failure and recovery are tested.
- [ ] Logging failures are visible.
- [ ] Core :8000 is never placed inside Sandbox.

### Security and privacy
- [ ] Automated tests verify secret redaction.
- [ ] Prompt/response content is not stored by default without approval.
- [ ] Access and retention behavior is documented and tested where implemented.

### End-to-end
- [ ] Trace a supported invocation from AI identity → Work/task → provider/model → usage/cost → artifact → independent acceptance evidence.
- [ ] Demonstrate unavailable-usage and retry/error cases.
- [ ] Record commands, environment, timestamps, hashes/links and reviewer identity.

## Required artifacts
Discovery inventory/decision record; architecture/schema; implementation plan and changed-file list; automated tests/E2E report; usage-cost reconciliation; limitations, runbook and handoff.

## Status rule
Until all required conditions have reproducible evidence, status remains ACTIVE / BLOCKED / PARTIAL VERIFIED. A design document or file creation alone is not PASS.
