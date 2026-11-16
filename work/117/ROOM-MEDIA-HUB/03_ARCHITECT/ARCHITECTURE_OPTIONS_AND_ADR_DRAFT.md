# ARCHITECTURE OPTIONS & ADR DRAFT — WORK 117
- Work: 117 ROOM-MEDIA-HUB
- Status: DRAFT FOR INDEPENDENT REVIEW — NOT APPROVED
- Version: 0.1
- Authority: Vinh
- Coordinator: Xu / AI-01
- Date: 2026-11-16
- Boundary: Architecture decision preparation only. No source/runtime/cloud resource changed.

## 1. Decision framing
Two independent choices must not be conflated:
1. Storage topology: where the durable original is written and how replicas/cache behave.
2. Platform ownership: whether W33 is evolved behind a service boundary or replaced by a different storage implementation.

Product constraints already confirmed by Vinh:
- One shared media catalog and canonical asset identity for the whole ROOM-HOP.
- One asset may be associated with multiple Works.
- Work-specific views and permissions are allowed; shared does not mean public.
- Hybrid internal + Cloud storage is required.
- GitHub stores code/schema/config/docs, never media binaries.

## 2. Topology options

### T1 — Internal primary + encrypted asynchronous Cloud replica (candidate)
Write original to internal durable storage; commit metadata and durable ingest state; enqueue idempotent Cloud replication; verify remote checksum; expose replica health/lag separately from upload acceptance.
- Advantages: local ingest/read path can continue during WAN disruption; potentially lower routine egress for Room-local use; Cloud provides off-site durability.
- Costs/risks: internal capacity/operations are mandatory; replication lag and queue growth must be monitored; internal site failure before replication completes can lose the newest unreplicated data; restore and failover need rehearsals.
- Required controls: durable internal write contract, transactional outbox or equivalent recoverable queue, immutable object identity, idempotency, checksum verification, retry/back-pressure, reconciliation, capacity alerts, tested restore.
- Unknowns: internal target, bandwidth, Cloud provider/region, RPO/RTO, capacity and cost.

### T2 — Cloud primary + internal cache/replica
Write original to Cloud as the durable authority; maintain internal cache or replica for frequent Room access.
- Advantages: off-site durability from first successful Cloud commit; easier remote collaboration and cloud-native scaling.
- Costs/risks: ingest and normal use depend on WAN/provider availability; egress and request charges may rise; cache invalidation and local offline behavior remain complex.
- Required controls: provider availability design, local cache policy, egress guardrails, authorized URLs, local outage behavior and restore plan.
- Unknowns: provider/region/contract, actual egress profile, connectivity and data-residency constraints.

### T3 — Active-active dual write
Write to internal and Cloud as co-equal targets during ingest.
- Advantages: potentially lower replica lag when both writes succeed.
- Costs/risks: partial success, split-brain, retries, conflict resolution, duplicate handling and user-visible consistency are materially more complex; two-phase distributed commit is not assumed available.
- Disposition: NOT RECOMMENDED for initial release unless a concrete availability requirement proves T1/T2 inadequate and a fault-tested consistency protocol is specified.

## 3. Platform ownership options

### P1 — Evolve W33 behind a stable storage port/service boundary (candidate)
Retain W33's content-addressed storage/integrity concepts, but refactor the local prototype into a properly authorized component with storage adapters, a normalized media/Work association model, durable job handling and service-level observability.
- Advantages: preserves useful existing work and avoids creating a competing raw-file store; potentially lower migration cost.
- Risks: W33 currently has a single work_id, caller-supplied agent attribution, local CLI/filesystem assumptions, no cloud replication/API evidenced, and source-correlated risks around restore, dedup metadata disclosure and concurrent temp writes.
- Conditions: no production reuse until trusted authorization boundary, many-to-many associations, restore/purge lifecycle, concurrency-safe writes, recovery/reconciliation, and cloud adapter contracts are designed and tested.

### P2 — Adopt a managed/object storage platform as the canonical blob layer; migrate or retire W33's blob role
W117 owns media-domain catalog/workflows; selected internal and Cloud object stores provide binary persistence through adapters.
- Advantages: can use mature object-store durability, lifecycle and replication capabilities; avoids overloading W33 prototype with responsibilities it does not yet implement.
- Risks: provider lock-in, recurring cost/egress, migration complexity, local/internal target integration and operational dependency on provider semantics.
- Conditions: provider and contract comparison, portability boundary, data export/migration strategy, security and cost model, and no duplication of catalog authority.

### P3 — Build a new bespoke binary store independent of W33
- Advantages: maximum control over implementation.
- Risks: duplicates W33's purpose, increases maintenance and security burden, delays delivery, and creates competing sources of truth.
- Disposition: REJECT as default. Reconsider only if P1 and P2 are shown infeasible with evidence.

## 4. Combined candidate packages

| Package | Topology | Platform | Preliminary disposition |
|---|---|---|---|
| A | T1 internal primary + Cloud replica | P1 evolve W33 behind service boundary | PREFERRED FOR REVIEW, NOT APPROVED |
| B | T1 internal primary + Cloud replica | P2 managed/object storage canonical blob layer | VALID ALTERNATIVE; requires provider/internal target evidence |
| C | T2 Cloud primary + internal cache/replica | P1 or P2 | VALID ALTERNATIVE if remote-first access and WAN assumptions justify it |
| D | T3 active-active | P1 or P2 | DEFER / NOT RECOMMENDED for initial release |
| E | Any | P3 bespoke new store | REJECT BY DEFAULT due to duplicate-store risk |

## 5. Qualitative decision matrix
Legend: Strong / Medium / Weak are preliminary qualitative assessments, not measured scores.

| Criterion | A | B | C | D | E |
|---|---|---|---|---|---|
| Reuse existing W33 investment | Strong | Weak | Medium | Medium | Weak |
| Local operation during WAN outage | Strong | Depends on internal target | Weak–Medium | Medium but complex | Depends on design |
| Off-site durability after successful replica | Strong | Strong if configured | Strong after Cloud commit | Potentially strong, consistency complex | Depends on design |
| Initial engineering complexity | Medium–High | Medium–High | Medium–High | Very High | Very High |
| Provider portability | Medium–High with adapters | Medium, contract-dependent | Medium | Medium | Depends on design |
| Current evidence readiness | Low–Medium | Low | Low | Low | Low |
| Risk of duplicate canonical store | Low if W33 evolved in place | Medium during migration | Low–Medium | Medium | Very High |

Interpretation:
- No package is implementation-ready today.
- A is the current review candidate because it aligns with local-first use and reuses W33 concepts, not because W33 is production-ready.
- B must remain a serious alternative until internal hardware and W33 remediation costs are known.
- C depends on actual remote collaboration and connectivity requirements.
- D/E should not be selected without evidence that simpler alternatives fail.

## 6. Draft ADR-117-001 — Room-wide media storage ownership and topology
- Status: PROPOSED — OPEN FOR CLA/KA/QW/GO REVIEW; NOT APPROVED BY VINH
- Context: Room-wide shared media catalog; hybrid storage; W33 is a local prototype, not a proven multi-user hybrid service.
- Proposed decision: Adopt package A as the leading candidate for review: W117 owns media product/catalog/workflow; W33-derived storage component remains behind a stable service/storage port; internal durable primary plus encrypted asynchronous Cloud replica; Core is the intended authorization authority only after its actual contract is verified.
- Alternatives considered: B managed/object storage canonical blob layer; C Cloud-primary with internal cache; D active-active dual write; E bespoke independent store.
- Rationale: preserves local-first behavior and existing content-addressed work while avoiding a second competing raw-file store. The proposal remains conditional on remediation feasibility and verified internal/Cloud economics.
- Consequences: requires substantial W33 hardening or replacement of its blob implementation; requires many-to-many asset_work; durable replication state machine; trusted authorization; operational recovery and cost controls.
- Reversal conditions: internal target cannot meet durability/capacity/RPO/RTO; W33 remediation cost/risk exceeds P2; WAN/off-site requirements favor Cloud primary; provider/legal terms rule out candidate.
- Approval: pending independent reviews and explicit Vinh architecture-gate decision.

## 7. Mandatory conditions before architecture baseline
1. Cla: compare P1 vs P2; assess W33 remediation, storage ports, internal target, replication and migration.
2. Ka: threat model, per-Work authorization, metadata leakage, encryption/key ownership, retention, privacy and provider/legal constraints.
3. Qw: acceptance strategy and test design for concurrency, dedup, restore, replication faults, checksum mismatch, recovery and authorization negatives.
4. Go: validate model assumptions; compare provider/internal costs, storage, operations, bandwidth, egress, proxy/cache economics and growth scenarios.
5. Core contract: inspect actual Core identity/authorization integration and prove supported call path; do not invent endpoints.
6. Product owner: approve measurable NFRs including capacity, max file size, throughput/concurrency, RPO/RTO, retention and supported formats.

## 8. Cost model caution
Go's egress sensitivity is recorded as ASSUMPTION-BASED. Example values (e.g. $0.08/GB, 8 TB, egress ratios and cache-hit rates) are scenario inputs, not verified provider quotes or Room telemetry. Do not turn cache-hit ≥70%, cost alerts or proxy requirements into approved NFRs until the inputs, formulas, provider tariff, measurement window and owner are validated.

## 9. Decision status
- Product scope: CONFIRMED by Vinh.
- Hybrid requirement: CONFIRMED by Vinh.
- Leading architecture candidate: A / T1+P1, PROPOSED ONLY.
- ADR-117-001: DRAFT / NOT APPROVED.
- Independent consultation: NOT DISPATCHED / BLOCKED by current agent-discovery entitlement.
- BUILD: NOT AUTHORIZED.


## 10. ZERO-COST PROVIDER SCREEN — W117 (2026-11-16)
Purpose: Screen temporary providers for the current zero-cost phase without selecting or authorizing any provider.

### Mandatory pass/fail conditions
A candidate is NOT eligible for the zero-cost phase unless all are evidenced:
1. Actual usable free quota is stated separately from marketing capacity, promotional capacity and trial credits.
2. API access is available to this project/use case, including developer approval requirements and any fees.
3. Upload, download, list, metadata lookup and deletion/export are supported through documented interfaces or a documented manual operating procedure.
4. Quota, file-size, bandwidth, request-rate, token expiry and account restrictions are documented.
5. No paid resource can be silently enabled; billing exposure can be prevented or strictly bounded before any trial.
6. Data ownership, privacy, account recovery, retention and provider termination/export conditions are acceptable for non-sensitive test assets.
7. Provider-specific IDs/URLs do not become canonical Asset IDs; data can be exported and integrity-checked.

### Comparison dimensions
| Dimension | TeraBox | Google Drive personal | Cloudflare R2 |
|---|---|---|---|
| Advertised/included free capacity | 1 TB advertised; eligibility and API entitlement unverified | Up to 15 GB shared with Gmail/Photos | 10 GB-month Standard |
| API readiness | Official Open Platform exists; app credentials require separate application | Mature Drive API; quota and user ownership must be designed | S3-compatible API |
| API approval/identity | client_id/client_secret/private_secret application; OAuth token lifecycle | Google Cloud project/OAuth consent and quota controls | Account/API token and bucket setup |
| Free-tier API use proven for W117 | NO | NO | NO |
| Billing exposure | Need verify paid-plan/feature boundaries | No automatic charge for basic free account storage, but quota is small/shared; paid upgrade excluded | Usage above free quota is billable; must prevent billing exposure |
| Portability/export | Must test API and bulk export | Export/Drive API; ownership and rate limits to verify | S3-compatible object export |
| Current disposition | FIRST INVESTIGATION CANDIDATE, NOT SELECTED | SECONDARY CANDIDATE | TECHNICAL FREE-TIER CANDIDATE ONLY WITH BILLING GUARD |
| Evidence status | Public docs only | Official quota docs only | Official pricing docs only |

### Required test plan after separate Vinh approval
Use synthetic, non-sensitive files only. Do not upload real ROOM media.
- T0: confirm provider account and free quota without adding payment method or enabling paid services.
- T1: confirm API eligibility and obtain approval path; no secret/token is to be stored in chat or journal.
- T2: upload a small synthetic image and video; record size, duration, throughput and error behavior.
- T3: list, retrieve metadata, download and compare SHA-256.
- T4: rename/move and delete; verify expected behavior and recycle-bin/retention semantics.
- T5: export all test assets and metadata; verify portability and checksum.
- T6: test token expiry/refresh, rate limits and recovery.
- T7: confirm billing controls and demonstrate no charge path for the approved test scope.

### Decision rule
- Any mandatory condition FAIL/UNKNOWN => provider remains NOT APPROVED.
- Lowest cost is not enough: account recovery, privacy, exportability and API eligibility must pass.
- No provider selection or BUILD approval is implied by this screening rubric.

 
## TeraBox official-source findings — 2026-11-16
- Official product/app pages advertise 1 TB / 1024 GB free capacity. This is not evidence that developer API access is included.
- Official Open Platform documentation requires application for client_id, client_secret and private_secret. access_token validity: 2 days; refresh_token validity: 30 days. The docs describe quota lookup, multipart upload (precreate/chunks/create) and download operations.
- API approval, API fees/free entitlement, free-tier API quota, per-file limits, rate limits, region eligibility and bulk export remain UNKNOWN for W117.
- Official Terms allow changes/limits, including possible reduction of free capacity after inactivity and fees for services previously free, subject to the terms' notice provisions. Account activity and exportability must therefore be part of operational controls.
- Official product page markets 128 GB large-file upload as a Premium benefit; do not assume this limit is available on the free plan.
- Disposition unchanged: TeraBox is the first candidate to investigate, NOT SELECTED. No account, API application, credential, payment method, bucket or test upload has been created.
