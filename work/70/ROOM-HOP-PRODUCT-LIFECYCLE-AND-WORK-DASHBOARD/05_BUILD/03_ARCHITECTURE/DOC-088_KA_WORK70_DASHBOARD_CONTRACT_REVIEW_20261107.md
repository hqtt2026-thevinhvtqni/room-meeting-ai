# DOC-088 — RÀ SOÁT ĐỘC LẬP DASHBOARD CONTRACT VÀ DATA INTEGRITY WORK 70
# WORK 70 DASHBOARD CONTRACT & DATA-INTEGRITY INDEPENDENT REVIEW

- **Document ID:** DOC-088
- **Priority:** P1
- **Read order:** 88
- **Date / Time:** 2026-11-07 11:10 +07:00
- **Version:** 1.0
- **Status:** REVIEW COMPLETE — ACCEPT WITH CONDITIONS FOR BOUNDED BROWSER E2E / FORMAL QE BLOCKED
- **Owner / Author:** Ka / AI-02
- **Role:** CSA / Architecture & Independent Review
- **Coordinator:** Xu / AI-01
- **Authority:** Vinh / Product Owner
- **Depends on:** DOC-001; DOC-010; DOC-014; DOC-035; DOC-054; DOC-057; DOC-061; DOC-063; DOC-067; DOC-072; DOC-085; DOC-086; DOC-087
- **Review scope:** Work 70 Dashboard only — REVIEW / ARCHITECTURE ONLY. No product implementation or source mutation.

## 1. Executive decision

**ACCEPT WITH CONDITIONS for a bounded, static Sandbox Browser E2E exploration only.** This does not authorize product changes, Core integration, Gate transition, acceptance, release or a formal Independent QE PASS.

The underlying metric values checked by Ka reconcile for the current snapshot: six WP IDs match across BUILD_REGISTER and PRODUCT_STATUS; five blockers are open; twelve evidence records are RECORDED; Gate PASS count is zero; the AI capability registry is empty. However, the provenance contract and nested schema definitions have material gaps. The Product Capability payload also declares global freshness FRESH while one declared source has last_updated=UNKNOWN. The UI renders RECORDED and no_mock_data with success styling, which can visually overstate verification.

**Browser E2E conditions:** pin or snapshot the exact Sandbox inputs; make source revision/hash and freshness semantics explicit; retain the visible local/mixed-source labels; test missing, malformed and stale data paths. Formal QE remains BLOCKED until Qw has a valid scoped Work Entry/ACK, frozen test inputs, an approved test environment and reproducible evidence capture. Full Draft 2020-12 validation remains NOT RUN.

## 2. Sources inspected and evidence boundary

### 2.1 Sandbox Work 70 — read_probe status=ok

The following canonical Work-root files were read directly during this review:

- `05_BUILD/00_ROOT/BUILD_REGISTER.json`
- `DASHBOARD/PRODUCT_STATUS.json`
- `06_EVIDENCE/EVIDENCE_REGISTER.json`
- `DASHBOARD/execution/EXECUTION_STATUS.json`
- `DASHBOARD/execution/EXECUTION_STATUS.schema.json`
- `DASHBOARD/execution/index.html`
- `DASHBOARD/product/PRODUCT_CAPABILITY_STATUS.json`
- `DASHBOARD/product/PRODUCT_CAPABILITY_STATUS.schema.json`
- `DASHBOARD/product/index.html`
- `DASHBOARD/DATA_INTEGRITY_VERIFICATION_20261107.md`
- `03_ARCHITECT/DOC-085_KIEN-TRUC_HAI-LOAI-DASHBOARD_WORK-VA-SAN-PHAM.md`
- `03_ARCHITECT/DASHBOARD_CORE_READ_CONTRACT.md`
- `05_BUILD/03_ARCHITECTURE/WORK70_KA_ARCHITECTURE_CONTRACT_V1.md`
- `05_BUILD/03_ARCHITECTURE/DOC-061_RA-SOAT-DOI-CHIEU-HOP-DONG-KIEN-TRUC-RUNTIME-WORK-70.md`
- `03_ARCHITECT/DOC-063_KIEN-TRUC-THUC-THI_WORK-ENTRY-AUTHORIZATION-AND-DENY-RECOVERY.md`
- `06_EVIDENCE/DOC-072_DOI-CHIEU_HOP-DONG-KIEN-TRUC_DOC-061_063_064_065.md`
- Canonical `00_ROOT/DOC-035_NHAT-KY-THI-CONG_WORK-EXECUTION-LOG.md`
- Xu handoff `05_BUILD/10_AI_DEBUG_HANDOFF/KA_HANDOFF_WORK70_DASHBOARD_CONTRACT_REVIEW_20261107.md`

Sandbox read_probe confirms these paths were readable. The Sandbox tool response did not expose immutable content hashes or a commit revision for these files; this is recorded as a provenance limitation, not inferred as parity.

### 2.2 GitHub main — exact file readback

- AI Capability Registry `registry.json`: blob SHA `2cdb4d01ba534c2c97363c2f17aefb539e8d71ea`; content confirms `entries=[]`, `registry_status=INITIALIZED_EMPTY`.
- AI Capability Registry README: blob SHA `85495753af51d6b4346ba6a7dbbcdf793c5c19f7`; rules require exact provider/model/version and reproducible evidence before VERIFIED.
- DOC-055 GitHub main readback: blob SHA `41eddeda4dd7774b5eeb1089307cb96d937415bd`; it registers DOC-086 and DOC-087, making DOC-088 the next available ID in that observed register. Sandbox DOC-055 remains older/different and was not modified in this review.

### 2.3 Contract references

- DOC-010: Dashboard is a read-only projection. Proposed Work API paths are design proposals, not verified Core routes. Browser must not read DB, Sandbox filesystem or Execution Host directly in a production integration.
- DOC-085: Work Dashboard and Product Dashboard are separate products/boundaries. Work Dashboard can use local snapshots if clearly labeled. Independent Product Dashboard requires its own canonical product source, domain contract, product users and acceptance.
- DOC-061: DRAFT; contract approval pending; Core Work API/auth and implementation not verified.
- DOC-063: DRAFT — design only; not approved or implemented; it does not grant execution permission.
- DOC-072: reconciliation is design-only and does not prove deployed runtime, Core authorization or persistence.
- Ka architecture contract V1: DRAFT; not approved for implementation.
- The separate DOC-061 supplemental file under `05_BUILD/03_ARCHITECT/` was also read; it is an addendum/source recheck, not treated as a replacement for the full DOC-061 path above.

## 3. Independent metric recomputation

| Metric | Recalculation from source | Ka result | Disposition |
|---|---|---:|---|
| WP total | Unique wp_id in BUILD_REGISTER and PRODUCT_STATUS; compare sets | 6; exact same IDs; no duplicates | PASS — bounded data reconciliation |
| WP status breakdown | BUILD_REGISTER status values | 4 IN_PROGRESS, 1 BLOCKED, 1 PLANNED | PASS — matches payload |
| Open blockers | Count PRODUCT_STATUS blockers where status != CLOSED | 5; all 5 OPEN | PASS — bounded data reconciliation |
| Evidence | Count EVIDENCE_REGISTER.evidence | 12; all 12 RECORDED | PASS — count only; not verified evidence |
| Gate PASS | Count nine lifecycle phases where gate_status == PASS | 0; all nine NOT_READY | PASS — bounded data reconciliation |
| AI capability entries | GitHub registry.json entries.length | 0 | PASS — empty registry confirmed |
| Verified capabilities | Count registry entries with status VERIFIED | 0 | PASS — no entry exists to verify |
| Independent Product Dashboard | DOC-085 §2.2 and §8; Product payload | NOT_CREATED / NOT_VERIFIED | PASS — correctly distinguished in payload |

**Important interpretation:** these PASS labels apply only to arithmetic and source-to-payload reconciliation. They do not promote RECORDED evidence to VERIFIED, do not establish a Gate PASS and do not constitute QE.

## 4. Findings and risks

### F-01 — P1: Source provenance is not immutable/reproducible

Both payloads list source_id, source_type, source_path, retrieved_at, calculation_method and verification_status, but do not bind each source to an immutable Git commit/blob SHA or Sandbox content hash. Several sources have last_updated=UNKNOWN. A later reviewer cannot reliably reconstruct the exact bytes used for a displayed metric from the payload alone.

**Recommendation:** add source_revision (Git ref/commit where applicable), content_sha256, retrieved_at, and source authority. For Sandbox files, capture a content hash at collection time. Keep metric.source_id references stable and ensure each metric can be traced to the exact source revision.

### F-02 — P1: Product payload freshness is over-broad

`PRODUCT_CAPABILITY_STATUS.json` declares global freshness=FRESH, while its source list includes DOC-085 last_updated=2026-11-06 and AI README last_updated=UNKNOWN. No freshness threshold or aggregation rule is declared. The status may be true for the registry snapshot alone, but is not demonstrated for every source in the composite payload.

**Recommendation:** define freshness policy and aggregation (for example, worst-source status or per-source freshness); UNKNOWN last_updated must not silently contribute to global FRESH. Display as_of and source freshness separately.

### F-03 — P1: Nested JSON Schema contracts are under-specified

For `EXECUTION_STATUS.schema.json`:
- `blockers.items` is an array with no `items` schema.
- `data_integrity.primary_sources.items` declares required field names but no `properties` types; `additionalProperties=true`.
- Nested objects including lifecycle, work_packages, blockers, evidence and data_integrity allow additional properties.
- Metric `value` is unconstrained; nested metric objects permit additional properties by default.
- Several status fields are plain strings without enumerated values.

For `PRODUCT_CAPABILITY_STATUS.schema.json`:
- `ai_capability_registry.entries` is an array with no item schema.
- `data_integrity.primary_sources.items` declares required names but no property types; `additionalProperties=true`.
- Nested registry, modules, room_hop_integration and data_integrity objects are permissive.
- `registry_status` and registry `verification_status` are plain strings, not controlled enums.
- No schema-level constraint enforces `entries_count == entries.length`.

**Recommendation:** define item schemas and property types for blockers, primary_sources and capability entries; define controlled enums for state fields; decide and enforce nested additionalProperties policy; add cross-field consistency checks in a separate deterministic validator if JSON Schema cannot express the required invariant.

**Validation status:** JSON source files were parsed/read successfully in the inspection process. A full approved JSON Schema Draft 2020-12 validator was NOT RUN. Do not claim schema validation PASS.

### F-04 — P2: UI gives RECORDED success styling

Both HTML files map RECORDED to the `ok` class. RECORDED means evidence exists in a register; it does not mean independently VERIFIED or accepted. Green success styling can blur this distinction.

**Recommendation:** use neutral/blue styling for RECORDED; reserve success styling for a clearly defined verified/accepted state, and add a legend explaining status semantics.

### F-05 — P2: no_mock_data is hard-coded as success styling

Both HTML renderers use a fixed success class for the no_mock_data display. If the payload later changes to false, the UI can still show a green state.

**Recommendation:** derive the class from the boolean value; false must render as warning/failure. Treat no_mock_data as a claim requiring source/test evidence, not self-authenticating proof.

### F-06 — P2: Product view hides source-level provenance

The Product Capability JSON contains primary_sources and per-metric verification_status, but product/index.html does not render the primary_sources list or those verification statuses. The view therefore shows high-level freshness without exposing the underlying source trace.

**Recommendation:** show source ID, path, source type, last_updated, retrieved_at, verification status and revision/hash, or link to a read-only provenance detail view.

### F-07 — P2: generated_by label may imply live collection

Both payloads use `generated_by=live_collector_v1`, while `source_mode=github_derived+sandbox_derived` and DOC-010 explicitly distinguish local/mixed snapshots from Core live.

**Recommendation:** rename to a neutral collector identifier (for example `work_snapshot_collector_v1`) and include an explicit statement that this is not Core live. Do not use a label that can be interpreted as a live Core collector.

## 5. Architecture boundary

**Confirmed at inspected source level:**
- Both pages fetch only their sibling JSON payload using GET-style `fetch(..., {cache:"no-store"})`.
- No POST/PUT/PATCH/DELETE method or HTML form was found in the inspected page source.
- Both pages set UNKNOWN and show an error message when fetch/JSON parsing fails.
- Navigation links connect the legacy Work Dashboard, Work Execution and Product/Capability views.
- Payloads explicitly state `source_mode=github_derived+sandbox_derived`, `core_live=NOT_VERIFIED`, authorization NOT_VERIFIED, and storage/export DESIGN_ONLY.
- Product view explicitly says Independent Product Dashboard NOT_CREATED / NOT_VERIFIED.

**Not established:**
- Browser behavior, runtime headers, actual hosting path, authentication or authorization.
- Any Core live endpoint, Work-scoped authorization, canonical persistence or export implementation.
- That the browser cannot reach other endpoints through external scripts/configuration not included in the inspected files.

The current pages are read-only Sandbox/static projections in the inspected code. They must not be described as Core-live or production-integrated.

## 6. Test readiness matrix

| Test / area | Current evidence | Ka disposition |
|---|---|---|
| E2E-01 source connectivity | Go reports PASS; Ka did not independently rerun the connectivity case | RECORDED by Go / NOT independently verified by Ka |
| E2E-02 | No sufficiently specific execution evidence located in reviewed handoff/source set | NOT VERIFIED |
| E2E-03..10, 12 | No execution evidence in reviewed journal | NOT RUN |
| E2E-11 Sandbox write/readback | Go reports PASS for four artifacts; Ka read-probed inputs but did not perform a write | RECORDED by Go / not a Ka write test |
| Browser desktop/mobile | No browser run | NOT RUN |
| Navigation/drill-down | Static links inspected only | NOT RUN |
| Missing/malformed JSON | Error branches inspected statically only | NOT RUN |
| Stale/unknown/fresh states | Static logic and payload values inspected only | NOT RUN |
| Regression/accessibility/keyboard | No execution evidence | NOT RUN |
| Draft 2020-12 full schema validation | No approved validator executed | NOT RUN / BLOCKED |

### Preconditions before Qw Independent QE

1. Qw ACK and participant-specific Work Entry authorization are recorded and verifiable; required G0–G5 status is checked under DOC-057.
2. Xu freezes the exact source snapshot/revisions and records hashes for all Sandbox inputs and GitHub sources.
3. Schema issues F-03 are corrected by the authorized owner, or Xu explicitly scopes schema-negative cases as known defects for the QE run.
4. An approved Draft 2020-12 validator and version are selected; positive and negative validation cases are reproducible.
5. Test environment/browser versions, static serving command, origin, test data and cleanup boundary are documented.
6. Test matrix covers desktop/mobile viewport, navigation, source missing, malformed JSON, HTTP errors, stale/unknown data, RECORDED vs VERIFIED presentation, no_mock_data true/false and regression.
7. Raw output, screenshots, console/network errors, exit codes, test case IDs and source revision/hash are retained as evidence.
8. Qw reports findings independently; no author self-approval and no automatic Gate promotion.

## 7. Recommendation to Xu

1. Keep the four Dashboard UI/data artifacts and the two schemas as Sandbox review inputs; do not overwrite legacy Dashboard files.
2. Ask the authorized owner to resolve F-01 through F-07 before declaring the contract ready for acceptance.
3. A bounded exploratory Browser E2E may be opened only against a frozen Sandbox snapshot, with no mutation and with all outputs labeled exploratory. Do not mark the E2E suite PASS.
4. Keep formal Independent QE BLOCKED until the preconditions above are met and Qw's Work Entry/ACK is verified.
5. Do not Git-sync, merge, change Gate/lifecycle/assignment, modify Core/API/DB/runtime or release under this review assignment.
6. Reconcile DOC-055 Sandbox version with GitHub main separately. DOC-088 is the next ID in the observed GitHub main register; this review did not modify DOC-055.

## 8. Explicit non-claims

- No Gate PASS.
- No BUILD authorization.
- No Core-live assertion.
- No browser E2E execution or Independent QE PASS.
- No schema validator PASS.
- No GitHub synchronization, merge or release.
- No change to Go's HTML, JSON, schemas, source data, Core, API, DB, runtime, permissions or production configuration.

**Signed:** Ka / AI-02 — CSA / Architecture & Independent Review  
**Submitted to:** Xu / AI-01  
**Final authority:** Vinh / Product Owner
