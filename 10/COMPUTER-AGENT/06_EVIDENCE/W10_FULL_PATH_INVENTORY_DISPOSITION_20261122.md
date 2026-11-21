# WORK 10 — FULL SANDBOX / GITHUB PATH INVENTORY & DISPOSITION

- Document ID: W10-FULL-PATH-INVENTORY-20261122-01
- Work: 10 — COMPUTER-AGENT
- Date-Time: 2026-11-22 06:32 (UTC+07:00)
- Canonical repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Branch: `work/10-computer-agent-mirror`
- Sandbox Work ID: `10`

## 1. Inventory snapshot

| Measure | Count |
|---|---:|
| Sandbox files under `COMPUTER-AGENT/` | 157 |
| GitHub branch files under `10/COMPUTER-AGENT/` | 64 |
| Shared paths | 64 |
| Sandbox-only files | 93 |
| GitHub-only files | 0 |
| Sandbox-only `.github/` directory | 1 |

The 64 shared paths are all represented on both sides. The 93 Sandbox-only files below have explicit KEEP / SANDBOX-ONLY dispositions; the Sandbox and GitHub directory trees are therefore intentionally not byte-for-byte identical. No GitHub-only Work 10 file remains in this snapshot.

## 2. Shared-path verification

- 30 source/test/architecture/config files were independently fetched from Sandbox and GitHub and compared as exact UTF-8 text; all 30 matched.
- The remaining shared governance/evidence/manifest/journal/dashboard/release files were compared in targeted batches; all compared content matched after each update/readback.
- Three LOCKED contracts are exact-match: `ACTION_CONTRACT.md`, `WORKFLOW_CONTRACT.md`, `SAFETY_POLICY.md`.
- Current accepted runtime source, test suites, host contract, operational Dashboard, current runbooks, owner authorization, current CI evidence, Work Manifest, BIÊN BẢN and NHẬT KÝ are on the canonical branch.
- No divergent accepted source/test/config file is intentionally left Sandbox-only.

## 3. Sandbox-only path dispositions

### A. Generated / transient artifacts — KEEP SANDBOX-ONLY

Python bytecode caches, local owner lock/state, generated offline test output and legacy test evidence. These are machine/session outputs, not canonical source; regenerate on the execution host.

- `04_CODE/__pycache__/agent_api.cpython-312.pyc`
- `04_CODE/__pycache__/agent_runtime.cpython-312.pyc`
- `04_CODE/__pycache__/browser_adapter.cpython-312.pyc`
- `04_CODE/__pycache__/models.cpython-312.pyc`
- `04_CODE/__pycache__/process_supervisor.cpython-312.pyc`
- `05_TEST/__pycache__/test_p0_p5.cpython-312.pyc`
- `05_TEST/evidence.txt`
- `06_EVIDENCE/.computer-agent-owner.lock`
- `06_EVIDENCE/computer-agent-owner-state.json`
- `06_EVIDENCE/offline-test-evidence.json`

### B. Original/reference/preview material — KEEP SANDBOX-ONLY

Original HTML, extension/reference files, Sandbox-local duplicate workflow and sample-only Dashboard preview. They are not current runtime source and must not be promoted as implementation.

- `.github/workflows/real-browser-e2e.yml`
- `01_ORIGINAL/README.md`
- `01_ORIGINAL/index.html`
- `02_EXTENSION/README.md`
- `04_CODE/index.html`
- `09_DASHBOARD_PREVIEW/README.md`
- `09_DASHBOARD_PREVIEW/data.json`
- `09_DASHBOARD_PREVIEW/index.html`

### C. Historical evidence / superseded design records — KEEP SANDBOX-ONLY

Immutable historical reviews, old candidate audits, old design amendments, debug reports and prior evidence snapshots. Current accepted implementation/evidence is mirrored separately; these historical records remain in Sandbox for traceability.

- `06_EVIDENCE/CANONICAL_VERIFICATION_2026-10-27.md`
- `06_EVIDENCE/GITHUB_SANDBOX_RECONCILIATION_20261116.md`
- `06_EVIDENCE/REMEDIATION_2026-10-27.md`
- `06_EVIDENCE/VI_CLA_DEBUG_AUDIT_2026-10-28/VI_DEBUG_AUDIT.md`
- `06_EVIDENCE/VI_CLA_DEBUG_AUDIT_2026-10-28/audit-evidence.json`
- `06_EVIDENCE/VI_CLA_PATCH_REVIEW_2026-10-28/VI_PATCH_REVIEW.md`
- `06_EVIDENCE/VI_CLA_PATCH_REVIEW_2026-10-28/evidence-package.json`
- `06_EVIDENCE/VI_CODER_GATE0_RETRY_TASK_2026-10-28.md`
- `06_EVIDENCE/VI_CODER_GATE0_TASK_2026-10-28.md`
- `06_EVIDENCE/VI_GATE0_CANONICAL_RETRY_2026-10-28.md`
- `06_EVIDENCE/VI_GATE0_CANONICAL_VERIFICATION_2026-10-28.md`
- `06_EVIDENCE/VI_GATE0_RECONCILIATION_REVIEW_TASK_2026-10-28.md`
- `06_EVIDENCE/W10_CANDIDATE_SOURCE_PARITY_RECHECK_20261117_01.md`
- `06_EVIDENCE/W10_CANDIDATE_STATIC_REVIEW_20261117_01.md`
- `06_EVIDENCE/W10_CANONICAL_BRANCH_RECHECK_20261117_01.md`
- `06_EVIDENCE/W10_DEBUG/DEBUG_REPORT.md`
- `06_EVIDENCE/W10_DEBUG/RUN_LOGS.md`
- `06_EVIDENCE/W10_DEBUG/proposed_patch.diff`
- `06_EVIDENCE/W10_DEBUG/test_prevention_timeout_boundary.py`
- `06_EVIDENCE/W10_DECISION_MEMO_VERIFICATION_DEFAULT_20261117_02.md`
- `06_EVIDENCE/W10_EXECUTION_CHECKPOINT_20261116.md`
- `06_EVIDENCE/W10_P0_ACCEPTANCE_MANIFEST_V6.schema.json`
- `06_EVIDENCE/W10_P0_CANDIDATE_IMPLEMENTATION_20261116.md`
- `06_EVIDENCE/W10_P0_CRASH_ACCEPTANCE_MATRIX_V6.csv`
- `06_EVIDENCE/W10_P0_CROSS_REQUEST_TIMEOUT_CONTAINMENT_20261117_01.md`
- `06_EVIDENCE/W10_P0_IMPLEMENTATION_READINESS_GATE_20261118_01.md`
- `06_EVIDENCE/W10_P0_PROCESS_ISOLATION_DESIGN_20261117_01.md`
- `06_EVIDENCE/W10_P0_PROCESS_ISOLATION_DESIGN_AMENDMENT_20261118_01.md`
- `06_EVIDENCE/W10_P0_PROCESS_ISOLATION_DESIGN_AMENDMENT_20261118_02.md`
- `06_EVIDENCE/W10_P0_PROCESS_ISOLATION_DESIGN_AMENDMENT_20261118_03.md`
- `06_EVIDENCE/W10_P0_PROCESS_ISOLATION_DESIGN_AMENDMENT_20261118_04.md`
- `06_EVIDENCE/W10_P0_PROCESS_ISOLATION_DESIGN_AMENDMENT_20261118_05.md`
- `06_EVIDENCE/W10_P0_PROCESS_ISOLATION_DESIGN_AMENDMENT_20261119_06.md`
- `06_EVIDENCE/W10_P0_PROCESS_ISOLATION_REVIEW_20261117_01.md`
- `06_EVIDENCE/W10_P0_PROTOCOL_ADMISSION_DESIGN_20261117_01.md`
- `06_EVIDENCE/W10_P0_PROTOCOL_ADMISSION_SECOND_PASS_20261118_01.md`
- `06_EVIDENCE/W10_P0_SOURCE_DESIGN_GAP_REVIEW_20261118_01.md`
- `06_EVIDENCE/W10_P0_TIMEOUT_REVIEW_20261117_02.md`
- `06_EVIDENCE/W10_P1_TRANSPORT_DOWNLOAD_REMEDIATION_20261117_01.md`
- `06_EVIDENCE/W10_REMEDIATION_20261117_01.md`
- `06_EVIDENCE/W10_WINDOWS_HOST_VALIDATION_20261117.md`
- `06_EVIDENCE/XU_CI_RUN5_ARTIFACT_VERIFICATION_2026-10-28.md`
- `06_EVIDENCE/XU_CLA_DEBUG_REVIEW_2026-10-28.md`
- `06_EVIDENCE/XU_GATE0_CANONICAL_SOURCE_DECISION_2026-10-28.md`
- `06_EVIDENCE/XU_GATE0_INDEPENDENT_REVIEW_2026-10-28.md`
- `06_EVIDENCE/vi-gate0-file-diff.json`
- `06_EVIDENCE/vi-gate0-retry-diff.json`

### D. AI debug handoff archive — KEEP SANDBOX-ONLY

Immutable AI intake/review/task records and historical review reports. They are not current runtime source and are not silently promoted to the canonical branch.

- `10_AI_DEBUG_HANDOFF/00_INBOX/CLA_CTO/20261028_run01/DEBUG_REPORT.md`
- `10_AI_DEBUG_HANDOFF/00_INBOX/CLA_CTO/20261028_run01/RUN_LOGS.md`
- `10_AI_DEBUG_HANDOFF/00_INBOX/CLA_CTO/20261028_run01/proposed_patch.diff`
- `10_AI_DEBUG_HANDOFF/00_INBOX/CLA_CTO/20261028_run01/test_prevention_timeout_boundary.py`
- `10_AI_DEBUG_HANDOFF/00_INBOX/README.md`
- `10_AI_DEBUG_HANDOFF/00_INBOX/VI_P0_REMEDIATION_IMPLEMENTATION_TASK_20261116.md`
- `10_AI_DEBUG_HANDOFF/01_REVIEW/KA_HTTP_API_ORIGIN_AUTH_FINDING_20261101.md`
- `10_AI_DEBUG_HANDOFF/01_REVIEW/README.md`
- `10_AI_DEBUG_HANDOFF/01_REVIEW/VI_DEEP_REMEDIATION_REVIEW_20261116.md`
- `10_AI_DEBUG_HANDOFF/02_PATCH_CANDIDATES/README.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_RESULT_20261118_01.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_RESULT_20261118_02.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_RESULT_20261118_03.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_RESULT_20261118_04.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_RESULT_20261118_05.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_RESULT_20261119_06.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_RESULT_20261119_07.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_TASK_20261118_01.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_TASK_20261118_03.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_TASK_20261118_04.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_TASK_20261118_05.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_TASK_20261119_06.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_TASK_20261119_07.md`
- `10_AI_DEBUG_HANDOFF/03_VALIDATION/README.md`
- `10_AI_DEBUG_HANDOFF/04_DECISIONS/README.md`
- `10_AI_DEBUG_HANDOFF/README.md`

### E. Superseded owner handover — KEEP SANDBOX-ONLY

2026-11-17 handover is a historical snapshot superseded by 07_RELEASE/W10_HANDOVER_PACKAGE_20261122.md.

- `07_RELEASE/WORK10_HANDOVER_TO_OWNER_20261117.md`

### F. Transcript archive — KEEP SANDBOX-ONLY

Historical transcript archive; not a runtime artifact or canonical source.

- `transcript.md`

### G. Sandbox-only directory

- `COMPUTER-AGENT/.github/` — parent directory for the Sandbox-local workflow listed in section B; retain in Sandbox only.

## 4. Explicit non-actions

- No generated `__pycache__`, owner lock/state, or runtime-generated offline evidence was copied into GitHub.
- No sample preview data was promoted as live runtime evidence.
- No historical AI debug intake or superseded design review was overwritten or represented as current approval.
- No three LOCKED contracts were modified.
- No force push, main merge, deployment or release occurred.

## 5. Synchronization disposition

**Accepted source/test/architecture/config parity: PASS for the current shared set.** All 64 shared paths are present; no source/test/config divergence remains in the shared implementation set. The 93 Sandbox-only files and one parent directory are intentionally retained as historical/reference/generated Sandbox material, as itemized above.

This is a reconciled working/canonical branch inventory, not a claim that the two directory trees have identical file counts. Work 10 remains ACTIVE — NOT RELEASED pending physical Windows 10 acceptance, production V8 key provisioning, Linux cgroup-v2 disposition, ROOM-HOP integration and Owner's final acceptance.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
