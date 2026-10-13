# Work 101 Architecture

## Principle
Reuse existing ROOM-HOP authority and execution boundaries. Work 101 is a synchronization capability, not a replacement for Core, MCP, Workspace, Work 24, Work 27, Work 28 or Work 14.

## Components
1. Target Registry: Work ID, repo identity, branch, permitted roots, base revision, directions, identity and policy.
2. Sync Coordinator: plans changes, dispatches allowed transfers, retries and state transitions.
3. Change Ledger: source/destination revisions, digest, operation ID, provenance, result and timestamps.
4. Conflict Queue: base/source/destination snapshots or hashes and explicit resolution.
5. Policy Gate: identity, allowlist, revision freshness, secret exclusions and scope.
6. Validation Runner: reuse Work 28 contracts and Work 14 canonical E2E path; no parallel runner.
7. Approval Gate: bind Vinh's approval to exact operation, diff digest, destination branch and base SHA.
8. Evidence Publisher: machine-readable run manifest and human-readable summary.

## Flow
AI -> MCP :8020 -> Core :8000 -> Workspace :8010 / approved Sandbox interface. The coordinator reads a baseline, plans changes, validates policy, transfers only when authorized, verifies destination content and records evidence. AI agents do not receive unrestricted credentials.

## State and conflicts
States include DISCOVERED, PLANNED, POLICY_CHECKED, READY_TO_TRANSFER, TRANSFERRING, DESTINATION_VERIFIED, RECORDED, BLOCKED, CONFLICT_PENDING and DELETION_PENDING. Deletions of baseline files block all transfers until explicit review; no automatic delete. No last-write-wins. Same-path divergent edits require review. Missing/stale base stops the operation.

## Boundaries
Work 24 provides/reviews PC source bridge; Work 27 execution runtime; Work 28 MCP tools and authorization; Work 14 canonical autonomous E2E. Verify these live contracts before implementation.
