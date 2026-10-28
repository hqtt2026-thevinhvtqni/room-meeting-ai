# ROOM HOP — Room-wide Structure Reconciliation
Date: 2026-10-28
Owner: Ka — CSA / Architecture & Backend
Coordination and escalation: Xu — CEO / Lead Architect
Product acceptance: Vinh
Status: ACTIVE / AUDIT IN PROGRESS / NOT RELEASED

## Purpose
Reconcile GitHub and ROOM HOP Sandbox as parallel workspaces. Establish evidence-based structure and backend governance without assuming that matching names imply matching content or that Sandbox writes synchronize to GitHub.

## Non-negotiable rules
1. Evidence first: record exact repo, branch, commit SHA, path, blob SHA where available, Sandbox Work ID/path, readback outcome, test result, and timestamp.
2. Read before edit. Preserve existing work artifacts, transcripts, closed meetings, frozen baselines, and LOCKED contracts.
3. No bulk migration, bulk deletion, force-push, branch rewrite, or direct-main change during initial reconciliation.
4. GitHub source/policy changes use a scoped branch and reviewable PR. Sandbox writes are separate and must be verified independently.
5. Core :8000 stays outside Sandbox. No alternate dispatcher or execution bypass may be introduced to make a downstream Work pass.
6. Distinguish STRUCTURE_COMPLETE, FEATURE_COMPLETE, VERIFICATION_COMPLETE, and RELEASE_READY. Do not report PASS without relevant evidence.
7. Any inaccessible endpoint, permission, host action, or failed readback remains BLOCKED/WAITING and is escalated directly to Xu with exact evidence.

## Initial live evidence — 2026-10-28
- Repository: hqtt2026-thevinhvtqni/room-meeting-ai; default branch: main.
- Observed main HEAD: 0958c723a76d0f3e878f1e13883860b9b768de00.
- GitHub branch search returned 38 named branches across architecture, governance, Work 28, Work 102, Work 200, and other Works. Branch names alone do not establish freshness or acceptance.
- Sandbox inventory returned 53 Works.
- Sandbox inventory marks Work 15 (WEBSITE-BUILDER) and Work 98 (e2e) as missing manifests. This requires path-level confirmation and remediation; do not invent manifests before reading each Work's existing structure.
- Work 99 is named WORK-INDEX. Use it as a candidate index, not as a canonical source until compared with GitHub and other evidence.
- Active GitHub PR #27 (draft) introduces the common Work structure standard. Its own text explicitly says it does not complete per-Work migration/reconciliation.
- PR #27 defines operational dashboard at 08_DASHBOARD, preview-only dashboard at 09_DASHBOARD_PREVIEW, AI debug handoff zones under 10_AI_DEBUG_HANDOFF, protects Core :8000 from Sandbox placement, and requires branch/PR evidence for GitHub changes.
- Room build context reports Sandbox capabilities including list/read/create/write/append/delete and states Working Source is read-only while Sandbox is read/write; it also states AI cannot merge, commit, or push. The GitHub connector separately reports repository push/admin capability. Treat this as a capability-boundary discrepancy: connector permission is not equivalent to local/runtime authorization. Resolve through governance and auditable PRs, never by bypassing Core.
- A direct probe of the literal path manifest.json returned FileNotFoundError for Works 99, 28, 15, and 98. This does NOT contradict the inventory field until the actual manifest filename/path convention is confirmed; do not interpret this probe as evidence that all four manifests are absent.

## Work plan and gates
### Gate A — Inventory and source-of-truth matrix
For every Work: record Work ID/name, manifest status and exact path, GitHub repo/branch/HEAD, source tree/file hashes, Sandbox paths/readback, last evidence timestamp, active PR/CI, status, owner, and mismatch classification. Classify as MATCH, GITHUB_AHEAD, SANDBOX_AHEAD, DIVERGED, MISSING_MANIFEST, MISSING_SOURCE, READBACK_BLOCKED, or NOT_APPLICABLE.

### Gate B — Architecture/backend boundary map
Verify by source and runtime evidence: Web/API -> Core public boundary -> Meeting/Discussion lifecycle -> Agent Gateway/Connector -> provider; Core authority for execution; MCP 8020 public tools versus 8030 build/sandbox tools; transcript/history versus working context versus decision authority; authorization, identity propagation, provenance, idempotency, timeout, cleanup, and readback.

### Gate C — Highest-risk integration path
Prioritize Work 28 execution tooling. Keep ACTIVE / NOT RELEASED until one authorized request is traced from MCP through Core authority to approved runtime, result collection, evidence persistence, and readback, with negative authorization tests and independent verification. Existing PR descriptions explicitly state that staged snapshot runners and tool catalog alone do not prove live execution.

### Gate D — Work 102
Keep Gate A PARTIAL / NOT PASS until the existing Core task authority/host binding, idempotency, lease/fencing, ACK, recovery, and audit trail are demonstrated. Do not add a second dispatcher.

### Gate E — Work 200
Keep PAPER ONLY. Reconcile source/branch/tree and decision records before code changes. No live trading or claims of production readiness without independent risk controls and evidence.

### Gate F — Structure standard rollout
Use the approved common structure standard as a target, not a reason to mass-create empty folders. For each Work, preserve project-specific layout; add required zones or an explicit NOT_APPLICABLE README only after per-Work inspection and branch/PR review.

### Gate G — Daily audit
Each run must record timestamp, branch/commit snapshot, Work inventory delta, missing manifests, read/write/readback health, PR/CI deltas, top blockers, evidence references, actions taken, and escalation sent to Xu. A schedule existing is not proof the job ran; record actual run result and MCP/PC reachability separately.

## Acceptance criteria
- Every Work has a traceable identity, source reference, manifest/status, owner, and explicit applicability for required zones.
- GitHub and Sandbox differences are classified and reconciled with path/hash/readback evidence, not overwritten to look uniform.
- Backend trust boundaries and runtime authority are documented from actual source and live test evidence.
- Required tests and CI have verifiable results tied to exact commits.
- No false PASS, no destructive cleanup of unknown artifacts, no unauthorized merge/release.
- Final states are reported separately: structure, functionality, verification, and release.

## First actions
1. Inspect PR #27 and its CI/review status; do not merge merely to claim standardization.
2. Read actual manifest files using the Work-specific path convention, starting with Works 15, 98, 28, and 99.
3. Produce the first 53-Work reconciliation matrix and exact mismatch list.
4. Inspect Work 28, Work 102, and Work 200 source refs and compare to their Sandbox evidence.
5. Send Xu exact blockers that require PC/runtime/endpoint access or exceed the connector's documented execution boundary.
