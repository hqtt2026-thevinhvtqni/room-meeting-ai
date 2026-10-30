# WORK DOCUMENTATION & STORAGE STANDARD
- **STT / Document ID:** DOC-033
- **Priority:** P0
- **Read order:** 7
- **Depends on:** DOC-001; DOC-002; DOC-003
- **Status:** ACTIVE
- **Version / Updated:** 1.0 / 2026-10-30

## 1. Purpose and scope
This standard defines the shared documentation, source ownership, file storage and mapping rules for every ROOM-HOP Work. It prevents duplicate originals, competing registers, inconsistent AI reporting and confusion between the Work lifecycle tree and 05_BUILD.

## 2. Four official Work records
Every Work uses the following coordinated records. They are logical records, not permission to create multiple competing files.

| STT | Record | Purpose | Canonical owner |
|---|---|---|---|
| 01 | BIÊN BẢN | Meeting minutes, agreements, decisions, approvals and change history | 00_ROOT / DECISION_LOG and relevant phase record |
| 02 | KẾ HOẠCH | Work scope, milestones, tasks, owners, dependencies, priorities and acceptance criteria | 04_PLAN |
| 03 | BẢN VẼ / MÔ HÌNH SẢN PHẨM (when needed) | Approved architecture, workflows, data models, UI, technical drawings or 3D models | 03_ARCHITECT |
| 04 | NHẬT KÝ THI CÔNG | Chronological record of actual work, changes, tests, blockers and handoffs | 00_ROOT; technical details may be linked from build mappings |

Each Work must identify the canonical file/path for these records in its Manifest or Document Register. If the record does not apply (for example no drawing/model is needed), mark NOT REQUIRED with a reason; do not create an empty placeholder.

## 3. Canonical ownership by lifecycle
- 00_ROOT: Manifest, standards, Document Register, Decision Log, minutes and Work-wide execution log.
- 01_DISCOVER: original discovery inputs and discovery findings; preserve received originals.
- 02_DEFINE: approved product requirements and acceptance definitions.
- 03_ARCHITECT: canonical approved drawings, product models, architecture, data/API contracts.
- 04_PLAN: canonical plans, roadmap, WP plan and dependencies.
- 05_BUILD: mapping and engineering coordination only; never the canonical home of original Work documents or product source code.
- 06_VERIFY: verification plans, procedures and checklists.
- 06_EVIDENCE: cross-phase canonical evidence index and verified evidence references.
- 07_ACCEPT: acceptance decision and record.
- 08_RELEASE: approved release record and release manifest.
- 09_OPERATE: operating procedures, incidents and maintenance records.
- DASHBOARD: read-only projection of canonical records.

## 4. 05_BUILD is a mapping layer, not an original-file store
05_BUILD and its branch may contain mapping/index files that point to canonical Work records and source repository files; WP-to-engineering-area mapping and task execution pointers; temporary working copies required by a tool, clearly labelled TEMPORARY and traceable to an exact source version; and build/test coordination metadata and evidence links.

05_BUILD must not become the only location of official minutes, plans, approved drawings/models or Work-wide journals; canonical product source code, test source or production configuration; canonical cross-phase evidence, acceptance or release decisions.

A file's presence in 05_BUILD, Sandbox or a feature branch does not make it canonical. The source-of-truth location must be declared in the Work Manifest or controlled register.

## 5. Mapping record requirements
Every important mapping entry must include stable artifact/document/WP ID; artifact type and purpose; canonical repository and relative path/URI; exact branch + commit SHA, tag/version or immutable artifact version; SHA-256 where available; owner/producer and related WP; status (ACTIVE, TEMPORARY, SUPERSEDED, ARCHIVED, NOT VERIFIED); evidence reference and last-verified timestamp.

Do not use machine-specific absolute paths as canonical identifiers. A mapping without a resolvable canonical source and exact version is UNVERIFIED.

## 6. Source code and file storage
- Each Work declares its canonical source repository and source path before implementation.
- GitHub is canonical for version-controlled source only when the Manifest declares the repository/branch/path; Sandbox is a working/execution environment, not an independent source of truth.
- Binary artifacts and evidence must use the approved artifact store declared by the Work. Until that store is verified, record the current location as temporary/unverified; do not claim durable storage.
- A local or Sandbox copy is temporary unless explicitly designated canonical by an approved decision.
- Never overwrite an original input or approved artifact silently. Create a new version and record the supersedes relationship.
- Exclude credentials, tokens, passwords and private data not required for the artifact.

## 7. Four-record linkage and change control
Link minutes, plans, drawings/models and execution logs using Work ID, WP ID, Decision ID, Document ID and artifact version. A material plan/design change must reference its approving decision. An implementation result must link back to its WP and the design/version it followed. A test/evidence record must identify the exact source commit/version tested.

## 8. AI file creation and placement policy
AI must not create standalone documents, duplicate notes, reports or alternate registers merely for convenience. Before creating a file: identify artifact type and canonical owner; check Document Register/mapping register for an existing record; update the existing canonical record when appropriate; create a new document only when necessary and authorized; allocate the next stable Document ID and register metadata; write only to canonical path; update mappings; verify readback and record evidence.

Temporary files must be clearly labelled, scoped, and removed only under an approved cleanup procedure.

## 9. Migration of legacy 05_BUILD files
Existing 05_BUILD content is not to be deleted, moved or rewritten merely because this standard is adopted. First inventory each item and classify it as MAPPING, TEMPORARY, LEGACY, CANONICAL CANDIDATE or UNCLASSIFIED.

For every CANONICAL CANDIDATE, identify or establish its Work-root/source-repository canonical location, compare content and version, then update 05_BUILD to a mapping. Preserve old commit/history. Any physical move, deletion, branch rewrite or merge requires a separately verified migration plan and approval.

## 10. Compliance and status
A successful file write is not verification. A mapping is valid only after its target is read and exact version/hash is checked. No evidence, no PASS; a mapping cannot prove the target artifact works. Until legacy classification is complete, 05_BUILD transition status is ACTIVE / MIGRATION NOT VERIFIED. This standard applies to all new Works; existing Works adopt it through controlled, non-destructive migration.
