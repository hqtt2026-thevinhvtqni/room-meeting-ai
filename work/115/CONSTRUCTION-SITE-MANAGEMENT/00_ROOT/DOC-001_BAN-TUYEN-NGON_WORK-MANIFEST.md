# TUYÊN NGÔN WORK 115 / WORK MANIFEST
- **STT / Document ID:** DOC-001
- **Priority:** P0
- **Read order:** 1
- **Depends on:** NONE
- **Status:** ACTIVE / INITIALIZED — DISCOVERY ONLY
- **Version / Updated:** 0.2 / 2026-11-12
- **Work ID:** 115
- **Work Name:** CONSTRUCTION-SITE-MANAGEMENT
- **Product:** Ứng dụng quản lý và báo cáo thi công công trình / Construction Site Management & Field Reporting App
- **Product Owner / Final Authority:** Vinh
- **Lifecycle Orchestrator:** Xu / AI-01
- **Governing standard:** Work 70 — ROOM-HOP Product Lifecycle & Work Dashboard, current baseline Standard 1.3 (W70 DOC-001 v1.5); W70 DOC-002, DOC-033, DOC-038, DOC-039, DOC-056, DOC-096
- **Sandbox:** Work 115 — created in ROOM-HOP Sandbox 8030; exact parity verification in progress
- **GitHub repository:** hqtt2026-thevinhvtqni/room-meeting-ai
- **GitHub branch:** main
- **Canonical Work path:** work/115/CONSTRUCTION-SITE-MANAGEMENT/
- **Canonical product source repository/path:** NOT ASSIGNED — do not infer this Work documentation repository to be the product source.
- **Product source branch / starting commit:** NOT ASSIGNED
- **Current lifecycle phase:** 01_DISCOVER — INITIALIZED / DISCOVERY IN PROGRESS
- **Gate status:** G0/G1 NOT ASSESSED; no gate PASS claimed.
- **Work status:** ACTIVE / DESIGN BASELINE ONLY / NOT RELEASED

## 1. Purpose
Create a practical web application for a construction-site manager (the user's uncle) and field workers. Workers report work performed at construction sites from a phone; the manager reviews progress and reports through a web dashboard.

## 2. Confirmed initial product direction
- A web-based management interface for the manager.
- Field workers submit reports from the construction site using a phone.
- Reports are returned to a central workspace for the manager to review.
- The product is intended as a useful gift for the user's uncle.
- Initial report concepts to investigate: work description, progress, completed quantity, site photos and issues/obstacles. These are discovery candidates, not approved requirements.

## 3. Product users — initial hypotheses
- Manager / owner: creates and monitors projects, work items and worker assignments.
- Site supervisor / team lead: reviews or consolidates daily site reports.
- Field worker: submits a concise daily or task-based report with optional photos.
These roles require confirmation during DISCOVER.

## 4. Scope boundaries
IN SCOPE FOR DISCOVERY:
- User journeys for manager and field workers.
- Project/site, work item, worker, daily report, photo and progress concepts.
- Mobile-first reporting experience and manager web dashboard.
- Connectivity, data retention, access control, privacy and backup needs.
- MVP definition, architecture options and measurable acceptance criteria.

NOT AUTHORIZED YET:
- Production deployment, public exposure, real personal/site data, paid services or recurring costs.
- Choosing a final framework, database, hosting provider or authentication provider.
- Building native Android/iOS applications or integrations before requirements are confirmed.
- Treating sample/mock data as real field evidence.

## 5. Source of truth and storage
- Work governance and official records: this Work's canonical lifecycle tree on GitHub main.
- Product source code: separate canonical repository/path to be declared before BUILD.
- Sandbox: intended working environment; not currently verified or created in this operation.
- Dashboard: read-only projection only.
- Cross-phase evidence: top-level EVIDENCE/.
- Nhật ký thi công: 00_ROOT/DOC-035_NHAT-KY-THI-CONG_WORK-EXECUTION-LOG.md.

## 6. Canonical top-level directory set
00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE, DASHBOARD.

## 7. Authority and operating rules
1. Vinh is Product Owner and final authority for goals, material scope, acceptance and release.
2. Xu coordinates end-to-end execution and may make routine reversible decisions within approved scope.
3. Follow W70 READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF.
4. No evidence, no PASS. File creation is not product verification.
5. Record actual actions, checks, experiments, results and blockers in DOC-035 with timestamp, scope, method, evidence and next step.
6. Preserve history; do not silently overwrite or delete artifacts.
7. No product implementation before discovery/requirements/architecture and applicable entry gates are ready.

## 8. Governing control adoption\n- Adopt current Work 70 baseline Standard 1.3, including DOC-096 AI Work Session Integrity & Journal Control (P0).\n- DOC-096 is a governing external control; W115 must apply identity verification, full-journal scan before append, unique sequence/evidence IDs, append-only corrections and exact readback.\n- Work 70 Sandbox paths are relative to the Work root; W115 Sandbox paths are relative to Work 115 root.\n\n## 9. Current truth
- Work documentation scaffold created on GitHub main; exact-path readback PASS for all 11 registered canonical files (2026-11-12).
- Sandbox Work 115 creation: BLOCKED / NOT RUN because ROOM-HOP 8030 connection failed.
- Existing Sandbox portfolio collision check: NOT VERIFIED during this operation.
- Product code, UI, backend, database, authentication, tests and deployment: NOT STARTED.
- Requirements and architecture: initial discovery hypotheses only; not approved.
- Acceptance and release: NOT READY / NOT RELEASED.
