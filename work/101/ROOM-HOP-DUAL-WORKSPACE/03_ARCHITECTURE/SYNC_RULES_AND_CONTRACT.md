# Sync Rules and Contract — Proposal

Every operation declares operation_id, work_id, source/destination kind and ref, base/source revision, path allowlist, actor identity, policy version and content digest.

## Modes
- DRY_RUN: calculate/display changes only; no destination writes.
- SYNC_SANDBOX_TO_GITHUB / SYNC_GITHUB_TO_SANDBOX: transfer only permitted changes under the configured target and authorization policy.
- RESOLVE_CONFLICT: apply a reviewed resolution in an isolated target.
- INTEGRATE and RELEASE: separate operations requiring Vinh's explicit approval.

## Invariants
1. No AI build write to MAIN_SOURCE.
2. No routine write to default/protected branches.
3. No integration without explicit Vinh approval.
4. Any digest, base SHA, branch or scope change invalidates approval.
5. Identical operation retries are idempotent; same operation ID with changed payload is rejected.
6. Read back destination and verify digest after transfer.
7. Missing credentials, network, validation or schema produce BLOCKED, not PASS.
8. Redact credentials and sensitive environment values.
9. Reject traversal, out-of-root paths, reserved runtime files and secrets.
10. Any baseline-file deletion enters DELETION_PENDING and blocks all transfers until explicit resolution is designed and approved.\n11. Every result links evidence or says evidence unavailable.

## Proposed API — not implemented
plan_sync, execute_sync, list_conflicts, resolve_conflict, request_integration, approve_integration and verify_evidence require review against existing MCP/Core contracts before registration. Do not add duplicate tools.
