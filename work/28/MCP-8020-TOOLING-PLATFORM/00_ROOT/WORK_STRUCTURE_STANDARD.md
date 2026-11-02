# WORK 28 — DOCUMENT AND STORAGE STANDARD

This Work follows the Work 70 document-control principles.

## Canonical records
1. One official minutes register: `00_ROOT/BIEN_BAN.md`.
2. One master plan: `01_PLAN/WORK28_MASTER_EXECUTION_PLAN_V2.0.md`.
3. One Work-wide execution journal: `00_ROOT/NHAT_KY_THI_CONG.md`.
4. One controlled document register: `00_ROOT/WORK_DOCUMENT_REGISTER.md`.
5. Architecture decisions and contracts live under `03_ARCHITECTURE/`.
6. Code and tests remain under `04_CODE/` and `05_TEST/`.
7. Evidence and technical reports remain under `06_EVIDENCE/`.
8. AI-specific review, debug, patch and test handoffs remain under `10_AI_DEBUG_HANDOFF/`.

## Record classification
- Official minutes: decisions/instructions recorded in the canonical register.
- Plan: approved scope, sequence, owners, dependencies and acceptance criteria.
- Journal: chronological execution record.
- Decision: a bounded technical/governance decision with rationale and impact.
- Review: independent assessment; not approval unless explicitly recorded.
- Test evidence: command, environment, commit, run URL, exit code and result.
- Handoff: transfer of findings or patch candidates; not proof of integration.
- Archive: retained historical material; not current authority.

## Controls
- No AI may create a separate Work-wide minutes or journal file.
- Supporting reports are allowed, but must be indexed in the document register and linked from the canonical journal when materially relevant.
- Preserve historical files and their authorship. Do not mass-delete, rename or rewrite legacy evidence.
- New records must identify date, author/role, status, source commit, and evidence references where applicable.
- Sandbox/MCP 8030 copies are secondary evidence; GitHub is the canonical record for this Work.
- A successful document write/readback is not code verification or product acceptance.
