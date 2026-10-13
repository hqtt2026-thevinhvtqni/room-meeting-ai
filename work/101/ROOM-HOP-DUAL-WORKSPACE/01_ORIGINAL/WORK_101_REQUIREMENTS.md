# WORK 101 — REQUIREMENTS

## Decisions from Vinh
1. Two-way rule-based synchronization between ROOM-HOP Sandbox and GitHub.
2. Integration/merge/release only after explicit approval by Vinh.
3. AI participation assigned by actual capability. AI without execution access can advise, review, or test evidence.
4. Automated E2E is the preferred build/verify loop.
5. Inspect and reuse existing ROOM-HOP components before adding functionality.
6. Never report PASS without evidence.

## Functional requirements
FR-01 Inventory supported Sandbox and GitHub targets and their permissions.
FR-02 Map each synchronization target to a Work ID, repository, branch, and path allowlist.
FR-03 Track immutable change identity, base revision, source revision, destination revision, content digest, actor, timestamps, and state.
FR-04 Detect one-sided changes and propose/perform transfer only when the configured policy allows it.
FR-05 Detect concurrent edits and produce a conflict record; never silently overwrite.
FR-06 Make retries idempotent and recoverable after timeout or process restart.
FR-07 Enforce path allowlists and reject credentials, secrets, runtime databases, generated artifacts, and excluded files unless explicitly allowed by policy.
FR-08 Keep sync distinct from merge/release; merge/release requires Vinh's approval.
FR-09 Store auditable evidence for every transfer, conflict, rejection, test, and approval.
FR-10 Provide a dry-run/preview showing planned changes before any write.
FR-11 Support capability-based assignment to AI contributors and independent review.
FR-12 Run automatic validation and E2E with correlated run ID and evidence manifest.

## Security requirements
- Least privilege; credentials remain in approved secret storage and never enter logs.
- Verify repository, branch, base SHA and target path before writes.
- Reject stale-base writes and replayed approvals.
- Approval is bound to exact diff/content digest, target branch and operation; any diff change invalidates it.
- Default deny on missing identity, unknown path, unknown branch, unavailable validation, or ambiguous conflict.
- Audit log is append-only or tamper-evident where supported.
- No AI identity can impersonate Vinh or mint Vinh approval.

## Acceptance policy
Each acceptance case must include command/tool invocation, timestamp, target revision, output, and artifact/log reference. Unit tests alone do not prove cross-environment E2E.
