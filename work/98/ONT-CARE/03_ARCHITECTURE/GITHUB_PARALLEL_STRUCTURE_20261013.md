# Work 98 — Sandbox/GitHub Parallel Structure
- TÊN: Xu
- CHỨC DANH: Work 98 technical lead
- NGÀY: 2026-10-13
- GIỜ-PHÚT: 15:02 UTC+7

## Rule
Use matching relative paths in Work 98 Sandbox and GitHub. Sandbox is the build zone; GitHub is versioned source/CI mirror. MCP is transport to Work Sandbox, not an ONT Care runtime dependency. Never claim sync until revisions and diffs are compared.

## Proposed target tree
98/
├── AGENTS.md
├── README.md
├── WORK_98_README.md
├── BIEN_BAN_W98.md
├── AI_SURVEY_ONCARE.md
├── PLAN_ONT_CARE_E2E_AUTOMATIC_20261013.md
├── SOURCE_AUDIT_20261013.md
├── GITHUB_PARALLEL_STRUCTURE_20261013.md
├── apps/
│   ├── dashboard-pc/
│   └── mobile-ont-care/
├── packages/
│   ├── domain/
│   ├── ont-adapters/
│   ├── diagnostics/
│   ├── auth/
│   └── ui/
├── services/
│   ├── app-api/
│   └── local-agent/
├── preview/
├── e2e/
│   ├── dashboard/
│   ├── mobile-customer/
│   ├── mobile-technician/
│   ├── direct-ont/
│   └── journeys/
├── tests/
├── docs/
│   ├── architecture/
│   ├── security/
│   └── runbooks/
└── 06_EVIDENCE/
    ├── baseline/
    ├── build/
    ├── e2e/
    ├── security/
    └── ont-device-lab/

## Migration rule
- This is a target, not an immediate move instruction.
- First trace imports, build commands, CI working directory and consumers of current paths.
- Preserve ont-platform/ as existing source until migration is planned and validated; avoid duplicate active source roots.
- Then choose evidence-based path: retain ont-platform/ and map DASH/APP logically inside it, or migrate in one reviewed change with compatibility tests.
- Root preview/ becomes product preview when wired to an explicit build artifact; preserve the old inventory preview as evidence if needed.
- Keep .env, credentials, local databases, raw customer data and transient artifacts out of GitHub.
- GitHub main = reviewed stable; feature branch/PR = proposed changes; CI required before merge. No commit/push/merge implied here.
- Sandbox-to-GitHub handoff manifest includes Work ID, revision, changed files, tests, evidence, known gaps and reviewer decision.
