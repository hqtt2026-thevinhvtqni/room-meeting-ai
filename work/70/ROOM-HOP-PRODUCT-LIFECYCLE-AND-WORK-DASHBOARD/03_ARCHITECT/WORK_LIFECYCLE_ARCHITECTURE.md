# WORK LIFECYCLE ARCHITECTURE — CANONICAL V1.1

## Domain model
ROOM-HOP → Work (stable product/lifecycle aggregate) → nine lifecycle phases. The Work owns exactly one lifecycle. 05_BUILD is the engineering workspace with its nine fixed child directories. Work Packages are logical delivery records maintained in 05_BUILD/00_ROOT/BUILD_REGISTER.md; they reference branches, build areas and artifacts rather than creating another lifecycle or mandatory per-WP folder tree. Top-level 06_EVIDENCE is the cross-phase evidence index. DASHBOARD is read-only.

## Canonical directory ownership
- 00_ROOT: Work identity, manifest, authority, standard version and glossary.
- 01_DISCOVER–04_PLAN: product discovery, definition, architecture and planning records.
- 05_BUILD: implementation workspace; child folders are 00_ROOT, 01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE, 07_RELEASE and 10_AI_DEBUG_HANDOFF.
- 06_VERIFY: independent verification and regression.
- 06_EVIDENCE: Work-level evidence index across every phase.
- 07_ACCEPT: formal acceptance decision and record.
- 08_RELEASE: controlled release package and approval.
- 09_OPERATE: operational ownership, monitoring and improvement.
- DASHBOARD: read-only projection from declared source.

## Logical services
1. Work Registry — stable Work ID, name, owner and metadata.
2. Lifecycle Service — phase state, gate state, transitions and decision history.
3. Work Package Registry — WP identity, owner, reviewer, dependencies, status and outputs.
4. Evidence Registry — evidence ID, type, URI, hash, producer, timestamp, environment and verification status.
5. Gate Evaluator — deterministic evaluation; fail-closed on missing/invalid evidence.
6. Authorization Service — role/permission checks for transitions, acceptance and release.
7. Dashboard Read Model — read-only projections.
8. Adapter Runtime — invokes human/AI/tool adapters under scoped permissions and records provenance.
9. Storage Adapter — managed artifact bytes behind Core-controlled metadata and access policy.
10. Export Service — authorized exports from a consistent source snapshot.
11. Audit/Event Log — append-only lifecycle, storage, export and execution events.

These are logical boundaries, not claims that all services or APIs already exist in Core.

## State and event flow
Owner defines scope → WP is recorded in BUILD_REGISTER → adapter executes within permission scope → code/test artifacts are written to canonical build areas → evidence is indexed in top-level 06_EVIDENCE → independent verifier reviews → gate evaluator checks criteria → authorized lifecycle service records transition → dashboard reflects recorded state.

## Data ownership
Core owns authoritative identity, authorization, lifecycle transitions, decisions and canonical evidence metadata. Artifact bytes may live in an approved managed store. Sandbox files and local PRODUCT_STATUS.json are design/build artifacts or snapshots, not production truth.

## Failure behavior
Unknown remains UNKNOWN. Missing evidence blocks PASS. Stale data is visibly STALE. Unauthorized transition is rejected and audited. Core unavailable means dashboard shows unavailable/cached state with timestamp, never silently fabricates local values. Partial writes require idempotency and reconciliation.

## Security
Least privilege per adapter and WP; server-side authorization; scoped credentials; secrets excluded from prompts/logs/exports; immutable audit trail; explicit human authority for high-impact actions; input/output validation; safe handling of untrusted tool content.

## Integration truth
Before declaring integration complete, verify actual routes, schemas, authentication/authorization, Work scoping, pagination, freshness, errors/timeouts, audit events and end-to-end behavior. Proposed contracts are not implementation evidence.
