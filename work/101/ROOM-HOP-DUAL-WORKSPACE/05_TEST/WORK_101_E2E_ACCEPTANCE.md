# Work 101 — Automated E2E Acceptance Plan

Status: PLANNED; NOT RUN.

## Discovery and compatibility
- Confirm Work Index 99 and status policy.
- Read Work 24/27/28/14 manifests and contracts.
- Inventory MCP tools and Core/Workspace APIs to prevent duplicates.
- Confirm repository, branch, work root and approved credential mechanism.

## Bidirectional sync
- Sandbox-only file -> GitHub branch -> read-back digest matches.
- GitHub-only change -> Sandbox -> read-back digest matches.
- Changes on separate paths yield deterministic non-overlapping plan.
- Divergent same-path changes become CONFLICT_PENDING without overwrite.
- Test delete/rename/binary/symlink/case-only rename, stale revisions, retries, restart, timeout, rate-limit and auth failures.
- Identical operation is idempotent; mutated payload under same operation ID is rejected.

## Security and approval
- Unapproved integration/merge/release denied server-side.
- Approval replay against different digest/branch/base/operation denied.
- Non-Vinh identities cannot approve for Vinh.
- Test traversal, protected branches, secrets, databases, logs, archives and generated outputs.
- Credentials never appear in output, logs or diffs.
- Direct tool invocation cannot bypass policy.

## E2E evidence
A real operation must traverse approved MCP/Core/Workspace boundary; revisions, operation ID and runtime identity correlate; destination read-back matches digest; evidence manifest records commands, timestamps, reports, logs, revisions and failures.

No case is PASS until executed on connected real targets and evidence is inspected. Overall status remains ACTIVE / NOT VERIFIED until then.
