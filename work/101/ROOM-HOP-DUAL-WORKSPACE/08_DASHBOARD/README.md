# Work 101 Dashboard

## Purpose
Read-only dashboard for monitoring both sides of Work 101: ROOM-HOP Sandbox and the dedicated GitHub branch. It surfaces connection health, revisions, file counts, parity, pending conflicts/deletions, evidence, freshness and the integration gate.

## Current behavior
- The dashboard UI has been built in `index.html`.
- On load and on the refresh button, it attempts a same-origin GET to the **proposed** Core read-model route `/api/work/101/dual-workspace/status`.
- The route is not yet confirmed to exist in ROOM-HOP Core. If unavailable, the dashboard explicitly shows DISCONNECTED / UNKNOWN / NOT VERIFIED; it must not fabricate live metrics.
- The UI has no GitHub token, no write controls, and no direct GitHub API calls.
- The proposed endpoint is a contract target, not evidence of an implemented backend or a successful live connection.

## Read-model fields
Top level: `work_id`, `source_status`, `parity`, `parity_detail`, `conflict_count`, `integration_state`, `updated_at`, `stale`, `sandbox`, `github`, `pending_items[]`, `activity[]`.

Each source object can include `status`, `file_count`, `revision`, `last_read_at`, `detail`, `evidence_refs[]`; GitHub also includes `branch`. Pending items include `path`, `kind`, `status`. Activity items include `at`, `event`, `status`, `evidence_ref`.

## Required backend work
1. Register a read-only Work 101 status route through Core, after checking the existing Core route conventions and authorization.
2. Build the response from authoritative Sandbox/MCP and GitHub branch read-back, including per-source timestamps and revision identifiers.
3. Compute structural and content parity from a common, explicit baseline; do not infer content parity from path counts.
4. Return conflict/deletion queues and evidence references. Mark incomplete or stale data as UNKNOWN/STALE.
5. Add contract tests and a real runtime smoke test through the supported Core/MCP boundary.

## Security and authority
- Render-only. No browser-held tokens and no direct mutation or GitHub write from the UI.
- Do not bind `SYNC_TARGET.yaml` until the true common baseline and revisions are established.
- No last-write-wins. Same-path divergent edits become `CONFLICT_PENDING`; deletions become `DELETION_PENDING`.
- Integration/merge/release remains locked until Vinh explicitly approves the exact operation ID, diff digest, destination branch and base revision.

## Acceptance
1. Unknown/unavailable data renders UNKNOWN/BLOCKED, never PASS.
2. UI distinguishes planned work, read-back, tests, real E2E and approved integration.
3. Stale responses are timestamped and marked stale.
4. A sync plan shows target, base revision, diff digest and conflicts before approval.
5. All mutations remain disabled unless a server-side capability is registered and authorized.
