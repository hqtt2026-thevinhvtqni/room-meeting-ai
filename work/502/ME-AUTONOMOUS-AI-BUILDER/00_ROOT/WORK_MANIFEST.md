# WORK MANIFEST — WORK 502
- Document ID: W502-DOC-001
- Work ID: 502
- Vietnamese name: NỀN TẢNG AI BUILDER TỰ ĐỘNG MÊ
- English name: ME AUTONOMOUS AI BUILDER
- Product: A user-facing autonomous product builder that turns one natural-language request into a verified, runnable software product and handoff package.
- Product Owner / Final Authority: Vinh
- Executive Coordinator: Xu / ROOM-HOP identity xu / HQTT role AI-01
- Created: 2026-11-18 (Asia/Ho_Chi_Minh)
- Status: ACTIVE — DISCOVER / DESIGN BASELINE; BUILD NOT AUTHORIZED
- Governing standard: Work 70 lifecycle, evidence, gate and documentation standards (DOC-001, DOC-002, DOC-003, DOC-033, DOC-035, DOC-057, DOC-096).
- Canonical repository target: hqtt2026-thevinhvtqni/room-meeting-ai
- Canonical branch target: main
- Canonical repository path target: work/502/ME-AUTONOMOUS-AI-BUILDER/
- Sandbox work id: 502
- Canonical records:
  - 00_ROOT/WORK_MANIFEST.md
  - 00_ROOT/BIEN_BAN.md
  - 00_ROOT/NHAT_KY_THI_CONG.md
  - 00_ROOT/TASK_BOARD.md
  - 03_ARCHITECTURE/ARCHITECTURE_PROPOSAL.md
  - 03_ARCHITECTURE/ARCHITECTURE_CONSULTATION_BRIEF.md
  - 04_PLAN/IMPLEMENTATION_ROADMAP.md
  - EVIDENCE/EVIDENCE_REGISTER.md
- Integration principles:
  1. AutoGPT Platform is the selected candidate execution/workflow engine; self-hosted deployment is preferred for data and cost control.
  2. ROOM-HOP Core remains the authority for Agent identity, authorization, task ownership and global controls.
  3. Work 501 is the model/provider capability plane; MÊ must not duplicate its provider registry, model router or global model policy.
  4. AutoGPT is a subordinate execution engine behind a ROOM-HOP adapter/gateway boundary; it must not become a second identity or authorization authority.
  5. Six functional roles are Research, Architect, Coder, Designer, QA and Deploy, coordinated by one MÊ Manager/Orchestrator.
  6. Model topology is policy-controlled: a single model may serve all roles, or role-specific models may be assigned through Work 501. No provider/model is selected as final until Work 501 is approved.
- Cost and resource guard:
  - ZERO-COST FIRST; no paid API, subscription, billing enablement, payment method, billable cloud resource, account/key creation or financial commitment without Vinh's separate explicit approval.
  - Hosted AutoGPT paid service is not selected.
  - Self-host still has hardware, electricity, storage, bandwidth and maintenance costs; these must be assessed, not described as absolutely free.
- Security guard: no public exposure, open signup, unrestricted shell, direct production credentials, arbitrary network egress or unreviewed third-party blocks. Bind local web ports to loopback until security review.
- License guard: verify current AutoGPT Platform license and permitted internal/commercial use before adoption; no redistribution or competing hosted offering is authorized.
- Structure note: Sandbox create_work supplied legacy starter directories (01_ORIGINAL–07_RELEASE). They are preserved as generated starter content. The lifecycle root is not yet normalized to Work 70; do not add colliding numbered lifecycle folders, rename, delete or move starter folders until a controlled migration plan and readback are completed.
- Current gates: G0 identity/entry authorization for Xu = ALLOW from Sandbox create_work; full G0–G5 assessment NOT COMPLETE. DISCOVER/ARCHITECTURE IN PROGRESS. BUILD, install, model download, API calls, billing, deployment and release NOT AUTHORIZED.
- Evidence rule: no evidence, no PASS. File creation is not verification.