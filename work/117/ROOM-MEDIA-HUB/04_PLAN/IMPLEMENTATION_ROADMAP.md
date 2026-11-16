# IMPLEMENTATION PLAN — WORK 117 ROOM MEDIA HUB
- Work ID: 117
- Canonical plan: this file only
- Product authority: Vinh
- CEO / coordinator: Xu (AI-01)
- Status: PLANNING BASELINE — BUILD NOT AUTHORIZED
- Revision: 0.2
- Date: 2026-11-17

## 1. Purpose and product boundary
Build one Room-wide shared image/video library for ROOM-HOP. The canonical Media Catalog and Asset identity are shared across Works. A single Asset may be associated with multiple Works; Work-specific views and access scopes are allowed. Shared does not mean public.
W117 owns the media product layer: media catalog, metadata, gallery, collections, search, previews, playback, Work associations and media workflows. W33 is a reuse candidate for content-addressed binary storage, not a production-ready service. W26, W29 and Core are integration dependencies whose actual contracts must be verified.
GitHub stores source, schemas, policy and documentation only; never raw media binaries, user media, secrets or tokens.

## 2. User-confirmed constraints
1. Hybrid internal + Cloud storage is required.
2. First stage prioritizes zero actual cost. No paid plan, payment method, billable resource, account authorization, API credential, real-media upload or deployment without separate Vinh approval.
3. Storage provider must be replaceable without changing canonical Asset IDs or the Media Catalog.
4. Go (Grok) is the selected primary Builder and accountable lead for W117 construction, subject to task dispatch/access confirmation.
5. Vibe (Mistral) is the independent architecture challenger and GitHub-based supporting Builder; Vibe may review Go's design and code, identify risks, propose alternatives and contribute code on explicitly assigned GitHub tasks. Vibe does not replace Go as lead and does not self-accept its own work.
6. Cla is CTO technical assurance only: technical reconciliation, repair, technical planning, code review, debugging and root-cause analysis; not the default feature Builder.
7. Qc is the implementation coder for assigned UI/Backend work. Qw is independent QE/QA and must not approve its own implementation.
6. Exactly four canonical project-control records are maintained across the Work: one Journal, one Minutes, one Plan and one Task Board. Supporting technical artifacts may remain as evidence/annexes, but must not become competing control records.
7. Sandbox and GitHub main are parallel construction environments. Keep the same canonical relative paths and reconcile changes; no separate Work branch is introduced for this sync.

## 3. Role and responsibility model
| Identity | Accountable role | Scope / boundary |
|---|---|---|
| Vinh | Product Owner / final authority | Approves product scope, architecture gate, cost exposure, real-data testing, deployment and release |
| Xu / AI-01 | CEO / Work coordinator | Owns the four canonical records, task decomposition, dependency and gate coordination, reconciliation and handoff |
| Cla / AI-03 (Claude) | CTO technical assurance | Architecture/source reconciliation, technical plan, repair, code review, debugging and root-cause analysis; not default feature builder |
| Go / AI-06 (Grok) | Primary Builder / construction lead | Accountable for W117 build delivery, technical task decomposition and integration coordination; execution begins only through authorized task dispatch and confirmed access |
| Vibe (Mistral) | Independent architecture challenger + supporting Builder | Independently reviews Go's architecture/design and implementation; contributes code on GitHub for explicitly assigned tasks; GitHub-only workflow; does not replace Go as lead |
| Qc (Qwen Coder) | Implementation coder | UI/Backend code implementation on authorized scope; GitHub-only/no MCP |
| Qw (Qween) | Independent QE/QA | Test design, execution, evidence and independent acceptance recommendation; not implementation owner |
| Ka / AI-02 | CSA independent reviewer | Security, privacy, governance, architecture and risk review |

Builder leadership decision: Go is SELECTED as primary Builder by Vinh. Vibe is SELECTED as independent architecture challenger and supporting GitHub Builder. This records the user's role decision, not proof that either agent has been dispatched, accepted a task or has verified repository access. Do not claim execution has started until dispatch, acceptance and access are evidenced.

## 4. Work breakdown structure and acceptance evidence
| WP | Workstream | Scope / outputs | Primary responsibility (proposed) | Minimum acceptance evidence |
|---|---|---|---|---|
| W117-WP01 | Product & architecture | Use cases, context/container/component/deployment views, ADRs, ownership boundaries | Xu coordinates; Cla reconciles; Ka reviews | Approved architecture baseline; decisions and unresolved risks recorded |
| W117-WP02 | Backend services | Asset lifecycle, upload sessions, metadata operations, job orchestration | Go primary Builder; Vibe supports on assigned GitHub tasks; Qc coder; Cla reviews/debugs | Unit + API contract tests; idempotency and error-path evidence |
| W117-WP03 | Database & catalog | Asset, metadata, collection, Asset-Work many-to-many, indexes, migrations | Go lead + Qc coder; Vibe supports/reviews on assigned GitHub tasks; Cla reviews | Migration/rollback tests; uniqueness, referential and concurrency tests |
| W117-WP04 | Storage engine & adapters | Internal/Cloud adapter, provider-neutral object locator, checksum, replication state | Go lead; Vibe independent design review/support; Cla technical assurance | Adapter contract tests; SHA-256 readback; retry/reconcile and migration/export proof |
| W117-WP05 | Media processing | Thumbnail, preview proxy, video transcode, async worker, resource limits | Go lead + Qc coder; Vibe supports/reviews on assigned GitHub tasks | Original hash unchanged; supported format matrix; worker retry/failure tests |
| W117-WP06 | API & integration | Core authorization contract, W33 storage boundary, W26 artifact contract, W29 producer handoff | Builder; Cla leads technical reconciliation | Verified actual contracts; integration tests; no invented endpoints |
| W117-WP07 | Security & access control | Identity, per-Work authorization, signed/short-lived access, encryption, audit, privacy | Ka reviews; Go leads implementation; Qc codes assigned UI/Backend; Vibe challenges architecture/supports assigned GitHub code; Cla debugs | Positive/negative auth tests; threat review; audit evidence; fail-closed tests |
| W117-WP08 | UI/UX | Gallery, upload, preview, playback, collections, detail and access states | Go primary Builder; Vibe supporting GitHub Builder; Qc implements assigned UI/Backend | Browser E2E for authorized sample assets; accessibility and error-state checks |
| W117-WP09 | Search & metadata | Search/filter, tags, type/date/Work facets, metadata extraction | Go lead + Qc coder; Vibe supports/reviews on assigned GitHub tasks | Query correctness and performance tests on declared test dataset |
| W117-WP10 | Backup & recovery | Backup, restore, soft-delete/restore, purge controls, export/migration | Go lead; Cla technical review/repair; Vibe supports assigned GitHub tasks; Qw verifies | Restore rehearsal; checksum validation; recovery time and data-loss evidence |
| W117-WP11 | DevOps & operations | CI/CD, environment config, secrets, observability, capacity/billing guardrails | Go coordinates build operations (platform owner/access to be verified); Vibe supports GitHub work; Ka reviews | Reproducible deployment, CI evidence, monitoring and no-billing guard proof |
| W117-WP12 | QE/QA & acceptance | Test strategy, test data, security/contract/E2E/recovery/performance regression, release evidence | Qw independent; An supports if available | Traceable test results; defects dispositioned; independent acceptance recommendation |

## 5. Delivery sequence and gates
| Phase | Included WPs | Deliverable | Exit gate | Current status |
|---|---|---|---|---|
| P0 — Discover & reconcile | WP01, WP03, WP04, WP06 | Verified as-is map for W33/W26/W29/Core; dependency and risk map | Source/contract evidence recorded; unknowns explicit | IN PROGRESS |
| P1 — Define & consult | WP01, WP07, WP12 | Approved requirements/NFR, security and QE strategy, agent review findings | Cla/Ka/Qw findings received or explicitly blocked; Vibe independent architecture review received or explicitly blocked; Vinh scope approval | BLOCKED / PENDING |
| P2 — Architecture baseline | WP01, WP03, WP04, WP06, WP07, WP11 | Final architecture, data model, ADR, cost and recovery model | Independent review and explicit Vinh architecture-gate approval | NOT READY |
| P3 — Foundation build | WP02, WP03, WP04, WP06, WP07, WP11 | Secure backend/catalog/storage/API foundation | Authorized WP scope; code review; contract and security tests | NOT AUTHORIZED |
| P4 — Product build | WP05, WP08, WP09 | Media workflows and user experience | Product acceptance tests pass on synthetic/approved sample data | NOT AUTHORIZED |
| P5 — Reliability & verification | WP10, WP11, WP12 | Recovery, operations, QE report and defect disposition | Mandatory verification PASS or explicit risk disposition | NOT RUN |
| P6 — Accept & release | WP12 and all WPs | Release candidate, operations handoff | Vinh accepts and separately approves deployment/release | NOT AUTHORIZED |

## 6. Mandatory technical decisions before BUILD
- Choose internal primary vs Cloud primary and replication/failover semantics using measured capacity, connectivity and cost evidence.
- Decide W33 evolution vs managed object-store boundary; do not create a competing raw-file store by default.
- Define canonical Asset ID, provider-neutral object locator, Asset-Work many-to-many relationship and metadata ownership.
- Verify Core's actual identity/authorization contract; fail closed if authority is unavailable.
- Define upload limits, supported image/video formats, concurrency, throughput, retention, RPO/RTO, replication lag and preview latency from evidence, not guesses.
- Define encryption/key ownership, malware scanning, privacy, audit, soft-delete/restore and approved purge.
- Complete zero-cost provider screening. TeraBox is only an investigation candidate; Google Drive is a small shared-quota fallback candidate; R2 is not zero-cost-safe unless billing exposure is prevented. No provider is selected.

## 7. Operating rules
- Every task has one accountable owner, dependencies, status, acceptance criteria and evidence link/path.
- Status vocabulary: PLANNED, READY, IN_PROGRESS, BLOCKED, DONE, PASS, FAIL, NOT RUN, NOT AUTHORIZED. DONE means the action completed; PASS is reserved for a verified test/gate.
- No agent assignment or acceptance is inferred from a role table.
- No implementation starts before architecture gate and Vinh's explicit authorization.
- Every meaningful action/test is appended to the one canonical Journal with date/time (if captured), scope, method, evidence, result and next step.
- Decisions and scope changes go into the one canonical Minutes; progress state belongs in the one Task Board; sequencing and gates belong in this Plan.
- Sandbox and GitHub main are kept in parity for the four canonical records. Resolve conflicts by inspecting both versions and recording the reconciliation; never silently overwrite newer work.
- No fake PASS, no unverified integration claim, no raw media binaries or credentials in GitHub.

## 8. Current overall status
- Product scope: CONFIRMED.
- Hybrid storage direction: CONFIRMED.
- Zero-cost-first constraint: CONFIRMED.
- Role separation: CONFIRMED as project direction; individual task acceptance is not yet verified.
- Architecture: PROVISIONAL / OPEN.
- Builder leadership: Go SELECTED; Vibe independent architecture challenger + supporting GitHub Builder SELECTED.
- Agent consultation: BLOCKED / NOT VERIFIED.
- BUILD: NOT AUTHORIZED.
- Deployment/release: NOT AUTHORIZED.

## 9. Immediate next actions
1. Reconcile and approve this plan and the canonical Task Board.
2. Complete technical reconciliation of W33/W26/W29/Core and zero-cost provider evidence.
3. Dispatch the architecture challenge to Vibe and obtain independent findings; record unavailable/undelivered review honestly.
4. Verify Go's execution channel, GitHub access and explicit task acceptance; verify Vibe's GitHub access and review/support acceptance.
5. Obtain independent Cla/Ka/Qw findings through authorized channels; record unavailable reviewers honestly.
6. Present architecture gate package to Vinh. Do not begin implementation until explicit BUILD approval.
