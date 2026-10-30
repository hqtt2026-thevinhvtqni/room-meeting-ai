# WORK LIFECYCLE ARCHITECTURE — CANONICAL V1.2
- **STT / Document ID:** DOC-009
- **Priority:** P1
- **Read order:** 10
- **Depends on:** DOC-008; DOC-033
- **Status:** ACTIVE
- **Version / Updated:** 1.2 / 2026-10-30

## Domain model
ROOM-HOP → Work (stable product/lifecycle aggregate) → nine lifecycle phases. The Work owns exactly one lifecycle. 05_BUILD is a mapping and engineering coordination layer with nine fixed child areas. It does not own canonical original Work records or product source files.

Work Packages are defined and planned at Work level in 04_PLAN. The current 05_BUILD/00_ROOT/BUILD_REGISTER files are legacy candidates under reconciliation and are not an independent canonical plan. Until a schema-backed WP registry is separately approved, the Work-level roadmap and registered plan documents remain the authoritative planning records. 05_BUILD/00_ROOT/BUILD_MAPPING_REGISTER.md maps engineering work to canonical Work/source artifacts. Top-level 06_EVIDENCE is the cross-phase evidence index. DASHBOARD is read-only.

## Canonical directory ownership
- 00_ROOT: Work identity, manifest, authority, standards, minutes, decisions, document register and Work-wide execution journal.
- 01_DISCOVER: product discovery inputs and findings.
- 02_DEFINE: product requirements, non-goals and acceptance definitions.
- 03_ARCHITECT: canonical approved drawings, models, architecture, data/API contracts and design decisions.
- 04_PLAN: canonical roadmap, Work Package plan, dependencies, priorities and milestones.
- 05_BUILD: mapping/indexes, engineering coordination and clearly labelled temporary working copies only; its child folders are navigation/mapping areas.
- 06_VERIFY: verification strategy, procedures, checklists and test plans.
- 06_EVIDENCE: Work-level canonical evidence index across every phase.
- 07_ACCEPT: formal acceptance decision and record.
- 08_RELEASE: controlled release package and approval.
- 09_OPERATE: operational ownership, monitoring and improvement.
- DASHBOARD: read-only projection from declared canonical sources.

## Logical services
1. Work Registry — stable Work ID, name, owner and metadata.
2. Lifecycle Service — phase state, gate state, transitions and decision history.
3. Work Package Registry — WP identity, owner, reviewer, dependencies, status and outputs, owned at Work level.
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
Owner defines scope → Work-level plan records WPs → 05_BUILD mapping links WPs to engineering areas and canonical source artifacts → adapter executes within permission scope → source artifacts are updated only in their declared canonical repository → evidence is indexed in top-level 06_EVIDENCE → independent verifier reviews → gate evaluator checks criteria → authorized lifecycle service records transition → dashboard reflects recorded state.

## Data ownership
Core owns authoritative identity, authorization, lifecycle transitions, decisions and canonical evidence metadata. Work root owns approved Work documentation and plans. Product source repositories are declared per Work/artifact. Artifact bytes may live in an approved managed store. Sandbox files and local PRODUCT_STATUS.json are working copies or snapshots, not production truth.

## Failure behavior
Unknown remains UNKNOWN. Missing evidence blocks PASS. Stale data is visibly STALE. Unauthorized transition is rejected and audited. Core unavailable means dashboard shows unavailable/cached state with timestamp, never silently fabricates local values. Partial writes require idempotency and reconciliation.

## Security
Least privilege per adapter and WP; server-side authorization; scoped credentials; secrets excluded from prompts/logs/exports; immutable audit trail; explicit human authority for high-impact actions; input/output validation; safe handling of untrusted tool content.

## Integration truth
Before declaring integration complete, verify actual routes, schemas, authentication/authorization, Work scoping, pagination, freshness, errors/timeouts, audit events and end-to-end behavior. Proposed contracts are not implementation evidence.
