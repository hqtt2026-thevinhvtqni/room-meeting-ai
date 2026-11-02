# 01 — DISCOVER / KHÁM PHÁ
- **STT / Document ID:** DOC-007
- **Priority:** P1
- **Read order:** 11
- **Depends on:** DOC-001
- **Status:** ACTIVE
- **Version / Updated:** 1.0 / 2026-10-30

## Problem statement

ROOM-HOP tracks many Works and child branches, but the current Work-centric folder structure does not consistently reveal the lifecycle position and readiness of the whole product. A completed child task can be mistaken for product-level completion.

## Product outcome

Every Work can answer, from one place:
1. What product is this Work building?
2. Which lifecycle phase is active?
3. What has been verified?
4. What is blocked, by whom, and by what dependency?
5. What evidence is required for the next gate?

## Users

- Vinh: portfolio/product oversight and final authority.
- Xu / lifecycle coordinator: planning, coordination, decision preparation.
- Builders: execute assigned work packages.
- Independent QE/QA: verify outputs and evidence.
- Reviewers / release owners: inspect gate readiness and decisions.

## Non-goals

- Do not rebuild the agent framework as the product.
- Do not migrate all existing Works in this initial Work 70 pass.
- Do not claim live dashboard integration before a real data source is connected.
- Do not replace Core with per-Work local state files.


## Addendum — Discovery evidence, assumptions and unresolved questions (2026-11-01)

### A. Evidence register (internal / user-stated only)

| ID | Classification | Evidence / source | Supported finding | Limitation |
|---|---|---|---|---|
| D70-DISC-E01 | User-stated product intent | Vinh's prior Work 70 discussions (2026-10-29 onward): wants a machine that runs plan → code → test → review; AI models are adapters attached to the machine, not the machine itself | Product problem is lifecycle execution/orchestration, not merely adding more autonomous agents | One product-owner statement; not external market research |
| D70-DISC-E02 | Current system baseline | DOC-001 Manifest v1.4 | Work 70 scope includes reusable lifecycle, WP model, evidence/gates, dashboard reference, storage/export design and future migration standard | Manifest says current phase 01_DISCOVER PLANNED; G0/G1 NOT_READY |
| D70-DISC-E03 | Governance requirement | DOC-004 Lifecycle Gate Matrix v1.2 | Nine lifecycle gates have defined phase exits, evidence minima and decision authorities | Policy document; does not prove technical enforcement |
| D70-DISC-E04 | State model requirement | DOC-005 State Machine v1.2 | Work, Phase, Gate and WP states are distinct; illegal transitions must fail closed; progress is not gate status | Historical baseline not yet reconciled against live runtime implementation |
| D70-DISC-E05 | Product boundary | DOC-010 Dashboard/Core Read Contract | Dashboard must be read-only; local snapshot/sample must not be represented as Core live | Contract is not evidence that Core endpoints exist |
| D70-DISC-E06 | Technical capability observation | DOC-017 Core Capability Gap Assessment and DOC-061 runtime reconciliation | Reviewed Core router is Meeting-centric; Work-scoped registry/read/write/evidence capabilities remain NOT VERIFIED | Read-only review of identified source/revisions; absence in reviewed router is not proof no implementation exists elsewhere |
| D70-DISC-E07 | Planning baseline | DOC-011 Roadmap and DOC-062 WP baseline proposal | Six WP candidates cover governance, WP registry, Dashboard, Core read integration, evidence/storage-export and independent verification | DOC-062 remains DRAFT; no approved execution baseline |

### B. Problem statement refinement

The current operational problem is that Work planning, assignments, execution, verification, acceptance and release are represented across documents, branches, tools and AI participants without one verified authoritative runtime enforcing the lifecycle. This creates risk of confusing a written assignment with accepted work, a local snapshot with live state, a file write with verified evidence, and a completed child task with product-level completion.

The product opportunity is a provider-neutral lifecycle engine and authoritative Work control plane that can accept interchangeable AI/tool adapters while retaining deterministic state, authorization, evidence, audit, recovery and independent verification.

### C. Assumptions — not yet validated

1. Vinh is the primary Product Owner and first operational user; additional builders/reviewers/QE roles are represented by the planned operating model.
2. Existing ROOM-HOP Core should remain the authority for identity, authorization and persistent Work state if its capabilities can be extended safely.
3. AI providers may change independently without changing lifecycle rules or authoritative Work data.
4. Work/WP/evidence volume, concurrency, retention, availability and latency requirements are not yet quantified.
5. A read-only Dashboard is sufficient for the initial product control surface; all state-changing commands should pass through an authorized service boundary.

### D. Unknowns requiring discovery or architecture decisions

- Which Core owner/team is accountable for Work lifecycle APIs and authorization?
- What are the actual authentication principal, role, permission and revocation interfaces in current Core?
- Which database and object/file storage services are approved for authoritative Work state and evidence bytes?
- What retention, backup, recovery, data classification and audit requirements apply?
- What workload targets are expected: number of concurrent Works/WPs, AI participants, evidence size, event rate and latency?
- Which AI adapters and tool execution environments are required for the first production slice, and what existing entitlements can be reused?
- What is the minimum useful first release: Work/WP registry and gates, or also evidence storage/export and Dashboard live read?

### E. G1 readiness assessment

- Problem and intended product outcome: DEFINED from product-owner statement and internal operating evidence.
- User roles and non-goals: IDENTIFIED at a preliminary level.
- Evidence provenance: RECORDED above; all evidence is internal or user-stated, not external customer research.
- Assumptions and unknowns: EXPLICIT.
- External user validation, operational metrics and workload baselines: NOT AVAILABLE / NOT RUN.
- Product Owner confirmation of this refined discovery brief: PENDING.

**Conclusion: DISCOVER OUTPUT PREPARED — G1 NOT EVALUATED / NOT PASS.** This addendum does not start the phase, change the Manifest, or grant entry to DEFINE. G1 may be evaluated only by the authorized Product Owner after reviewing the evidence, assumptions and unknowns.


## Addendum — lifecycle G0/G1 readiness evidence (2026-11-02)

### G0 — Work initialized
| Criterion (DOC-004) | Evidence | Assessment |
|---|---|---|
| Stable Work ID and name | DOC-001: Work ID 70 and canonical Work name | PRESENT |
| Owner and authority | DOC-001: Vinh as Product Owner/final authority; Xu as lifecycle orchestrator | PRESENT |
| Manifest and source identity | DOC-001: Manifest, Sandbox Work 70, GitHub repository and scoped Build branch | PRESENT |
| Scope boundary | DOC-001: lifecycle/WP/evidence/gates/Dashboard reference/storage-export design; no migration of other Works | PRESENT |
| Initial permissions | DOC-043 is a role policy, not proof of per-participant technical grants. DOC-069 records only Xu's limited document-control/read-only assignment. Other participants' Work-specific scope/permissions/ACK and server-side enforcement are not verified. | PARTIAL / NOT VERIFIED |

**G0 disposition: NOT_READY / NOT PASS.** Identity, owner, manifest and scope are documented; initial permissions are not yet sufficiently evidenced for the Work as a whole. The Work Owner must confirm the initial permission baseline and authorized participant scopes. A limited Work Entry for Xu does not grant permission to other participants.

### G1 — DISCOVER → DEFINE
| Criterion (DOC-004) | Evidence | Assessment |
|---|---|---|
| Problem statement and product outcome | Discover Brief sections “Problem statement”, “Product outcome” and addendum B | PREPARED |
| User/context evidence | D70-DISC-E01..E07; evidence is user-stated/internal operating evidence | RECORDED — INTERNAL ONLY |
| Opportunity | Addendum B: provider-neutral lifecycle engine and authoritative Work control plane | PREPARED |
| Assumptions and unknowns | Addendum C and D | EXPLICIT |
| Product Owner confirmation | Addendum E states confirmation pending; no G1 decision record found | PENDING |

**G1 disposition: NOT_READY / NOT PASS.** The discovery package is prepared but relies on internal/user-stated evidence, has unvalidated workload and external-user assumptions, and lacks the required Product Owner decision. Vinh retains G1 authority under DOC-004; D70-018 does not delegate Product Owner gate approval to Xu.

### Allowed continuation and exit conditions
- Xu may continue read-only source tracing, evidence reconciliation, documentation correction and preparation of downstream plans.
- Do not advance the Manifest phase pointer, mark G0/G1 PASS, enter DEFINE/ARCHITECT as an active phase, or open G4/BUILD until the authorized gate decisions are recorded.
- G0 exit: Work Owner confirms initial participant/role/scope permissions and the evidence is recorded.
- G1 exit: Product Owner reviews this Discover Brief and records an explicit G1 decision (PASS, FAIL or a reasoned request for additional discovery).
