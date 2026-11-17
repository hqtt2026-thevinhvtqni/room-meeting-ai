# DOCUMENT REGISTER — WORK 117 ROOM MEDIA HUB
- Status: ACTIVE REGISTER — INITIAL DRAFT
- Authority: Vinh
- Coordinator: Xu / AI-01
- Naming and lifecycle standard: Work 70 DOC-033, DOC-038, DOC-039 and DOC-040; official DOC codes remain pending central registration.

| Record | Canonical path | Status | Notes |
|---|---|---|---|
| Work Manifest | 00_ROOT/WORK_MANIFEST.md | ACTIVE | Work identity and scope boundary |
| Biên bản | 00_ROOT/BIEN_BAN.md | PROVISIONAL | One canonical minutes file; pending consultation |
| Nhật ký thi công | 00_ROOT/NHAT_KY_THI_CONG.md | ACTIVE | Append-only execution record |
| Task Board | 00_ROOT/TASK_BOARD.md | ACTIVE | Canonical task board; Dashboard statuses updated by Go 2026-11-17 |
| Discover Brief | 01_DISCOVER/DISCOVER_BRIEF.md | DRAFT | Initial discovery baseline |
| Product Requirements | 02_DEFINE/PRODUCT_REQUIREMENTS.md | DRAFT | Not approved |
| Architecture Consultation Brief | 03_ARCHITECT/ARCHITECTURE_CONSULTATION_BRIEF.md | READY TO SEND — NOT DISPATCHED | Dispatch blocked; includes Cla source-correlated W33 risks |
| Architecture Proposal | 03_ARCHITECT/ARCHITECTURE_PROPOSAL.md | PROPOSED | Not an approved baseline |
| Architecture Options & ADR Draft | 03_ARCHITECT/ARCHITECTURE_OPTIONS_AND_ADR_DRAFT.md | DRAFT — NOT APPROVED | T1/T2/T3 and P1/P2/P3 comparison; ADR-117-001 pending independent review |
| Existing Work Technical Audit | 03_ARCHITECT/EXISTING_WORK_TECHNICAL_AUDIT.md | DONE — DOCUMENT/SOURCE REVIEW | W33/W26/W29 findings; W33 follow-up source-correlated; no runtime tests |
| Cost Evaluation Hybrid | 03_ARCHITECT/COST_EVALUATION_HYBRID.md | INITIAL — ASSUMPTION-BASED | Go / CFO cost model; not baselined |
| Egress Sensitivity Analysis | 03_ARCHITECT/EGRESS_SENSITIVITY_ANALYSIS.md | DONE — ASSUMPTION-BASED | Sensitivity model; inputs/provider prices not independently verified |
| Open Decisions & Risks | 03_ARCHITECT/OPEN_DECISIONS_AND_RISKS.md | OPEN | Includes ODR-001..ODR-022 |
| Implementation Roadmap | 04_PLAN/IMPLEMENTATION_ROADMAP.md | DRAFT | Build not authorized |
| **W117 Dashboard (preview)** | **05_BUILD/04_CODE/dashboard/index.html** | **IN_PROGRESS** | Go first working preview 2026-11-17; read-only; snapshot data |
| W117 Dashboard README | 05_BUILD/04_CODE/dashboard/README.md | ACTIVE | Usage and boundary notes |

No parallel minutes, plan or journal files should be created. Update these canonical records in place and preserve the journal append-only.

## Verification history — 2026-11-16
- `W117-LOG-20261116-001` (Ka): READBACK VERIFIED by Xu via diagnostic read of the canonical journal. The original entry's PENDING READBACK disposition is preserved as the status at the time of Ka's operation; later verification does not rewrite that history.
- Go's Egress Sensitivity Analysis and Cost Evaluation files were readable. Their status remains ASSUMPTION-BASED; formulas, inputs, provider tariffs and actual Room telemetry have not been independently validated.
- Cla's additional W33 findings were independently checked against Work 33 store/CLI and existing tests. They are source-correlated risks, not runtime test results or evidence of a deployed exploit.
- Architecture consultation remains READY TO SEND / NOT DISPATCHED; architecture remains PENDING; BUILD remains NOT AUTHORIZED.

## Architecture options update — 2026-11-16
- Created `ARCHITECTURE_OPTIONS_AND_ADR_DRAFT.md` and appended ODR-017..ODR-022 to the existing open-decision register.
- Package A (T1 internal primary + encrypted asynchronous Cloud replica; P1 evolve W33 behind a stable service/storage port) is the leading candidate for review only. Package B remains a valid alternative.
- ADR-117-001 is DRAFT / NOT APPROVED. No reviewer dispatch, implementation, runtime test or provider selection is claimed.

## GitHub synchronization verification — 2026-11-16
- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Branch: `main`
- Canonical target: `work/117/ROOM-MEDIA-HUB/`
- Scope: 14 canonical Markdown records synchronized from Sandbox Work ID 117.
- Verification: Full-content readback comparison completed for all 14 files; 14/14 matched the Sandbox source.
- Status: DOCUMENTATION SYNC / READBACK PARITY — PASS. No media binaries, secrets, credentials or real user media were uploaded.
- This status does not approve architecture baseline, provider selection, BUILD, testing, deployment or release.

## Dashboard first preview — 2026-11-17
- Go / AI-06 delivered first working local/preview Dashboard under `05_BUILD/04_CODE/dashboard/`.
- Tasks W117-DASH-001..004 marked ACKNOWLEDGED + IN_PROGRESS with Journal evidence.
- Independent reviews (Cla/Ka/Qw) still DISPATCH UNCONFIRMED.
- Product BUILD remains NOT AUTHORIZED.

## Structure alignment — 2026-11-17
- W117 canonical Sandbox root is `ROOM-MEDIA-HUB/`; do not prefix Sandbox paths with `work/117/`.
- Dashboard package canonical path is `05_BUILD/04_CODE/dashboard/`; original root `04_CODE/dashboard/` implementation files removed after 7/7 exact content parity; empty assets/data/tests directory entries remain pending supported directory retirement.
- Cross-phase evidence canonical path is root `EVIDENCE/`; original `06_EVIDENCE/` evidence files removed after successful copy/readback; empty directory entry remains pending supported directory retirement. No root `06_EVIDENCE/` is to receive new evidence.
- Root `03_ARCHITECT/` is the correct canonical architecture phase and remains unchanged.
- Root `01_ORIGINAL/`, `02_EXTENSION/`, `03_ARCHITECTURE/`, `04_CODE/`, `05_TEST/`, `07_RELEASE/` are legacy misplaced directories; inventory showed no files in them at audit time. Directory retirement is pending a fresh inventory and supported delete-directory capability.
- Structure normalization status: Dashboard implementation/data 7/7 exact parity; 8 old Dashboard files and 2 old evidence files deleted after copy; canonical docs and evidence read back. Empty legacy directory entries remain. Post-migration test execution, GitHub/PC parity and independent QE pending.


## GitHub synchronization — 2026-11-17
- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`; branch: `main`.
- Canonical path: `work/117/ROOM-MEDIA-HUB/`.
- Current sync scope: canonical lifecycle markers, Dashboard implementation and tests, Dashboard evidence, and updated Work records.
- GitHub `main` readback verification: PASS — 38/38 tracked files exactly match Sandbox content; recursive tree is complete (truncated=false). Empty legacy Sandbox directories are not tracked by Git and contain no files. This PASS covers tracked Work files only, not runtime tests, independent QE or PC parity.
- Product BUILD remains NOT AUTHORIZED.
