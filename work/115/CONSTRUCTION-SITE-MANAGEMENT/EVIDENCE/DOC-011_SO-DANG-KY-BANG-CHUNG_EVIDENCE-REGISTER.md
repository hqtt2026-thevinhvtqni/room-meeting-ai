# SỔ ĐĂNG KÝ BẰNG CHỨNG WORK 115 / EVIDENCE REGISTER
- **STT / Document ID:** DOC-011
- **Priority:** P1
- **Read order:** 11
- **Depends on:** DOC-001; DOC-002
- **Status:** ACTIVE — INITIALIZED
- **Version / Updated:** 0.4 / 2026-11-12

| Evidence ID | Date | Scope | Method / source | Result | Status |
|---|---|---|---|---|---|
| EV-115-001 | 2026-11-12 | Product intent | Current conversation with Vinh | Web app for construction manager; field workers report from site by phone; manager reviews through web; intended gift for uncle | RECORDED — user-confirmed direction |
| EV-115-002 | 2026-11-12 | W70 governance baseline | Exact GitHub fetch of W70 DOC-001, DOC-002, DOC-033, DOC-055 and DOC-056 | Work lifecycle, documentation, evidence, naming and register rules inspected | RECORDED — source read |
| EV-115-003 | 2026-11-12 | Sandbox availability | ROOM-HOP 8030 list/context/structure requests | Connection failed; Work inventory and Sandbox create/readback unavailable | BLOCKED |
| EV-115-004 | 2026-11-12 | GitHub initialization readback | Exact-path fetch from GitHub main for all 11 canonical files | All 11 paths returned content and blob SHAs; structural marker checks passed | RECORDED — GitHub readback PASS; Sandbox parity NOT VERIFIED |\n| EV-115-005 | 2026-11-12 | ROOM-HOP Sandbox Work 115 creation | `sandbox_list_works` inventory (63 entries), W70 current Manifest/DOC-033/DOC-043/DOC-057/DOC-096 read via `sandbox_read_probe`, then `sandbox_create_work` as identity `xu` | No existing Work ID 115; create returned status=ok and `authorization=ALLOW: xu is a registered ROOM HOP member` | PASS — Work created after collision check |\n| EV-115-006 | 2026-11-12 | GitHub–Sandbox canonical file parity | Exact GitHub `fetch_file` content compared with Sandbox `sandbox_read_probe` content for 11 registered documents and 5 lifecycle `.gitkeep` placeholders | All 16 files matched exactly; no content differences. Auto-generated nested scaffold observed separately and excluded from canonical map. | PASS — 16/16 exact content matches |\n| EV-115-007 | 2026-11-12 | Post-create Sandbox registry and journal integrity | Re-run `sandbox_list_works`; full-file DOC-035 sequence scan; `sandbox_list` for Work 115 | Registry count=64; Work 115 present with manifest_exists=true; journal sequence IDs 001–008 unique, no duplicates | PASS — registry and journal integrity check |

Evidence is not a claim of product implementation, test PASS, acceptance or release.


| EV-115-008 | 2026-11-12 | Conditional architecture principle | Vinh's shared Teacher–Student–Rule Engine proposal, reconciled against current W115 Manifest, Decision Log, Architecture and Journal | Rule-first authority boundary, optional AI assistance/escalation, privacy/security/audit/fallback/cost controls and QS exclusion documented as a conditional design baseline; no implementation authorization | PASS — GitHub main readback and Sandbox exact content parity verified for DOC-003, DOC-008, DOC-011 and DOC-035 (4/4) |
| EV-115-009 | 2026-11-12 | Primary business actors and reporting relationship | Vinh's clarification in the current conversation | Quản công reports progress to nhà thầu; chủ đầu tư may be granted access when needed. Candidate role model and scoped investor visibility documented; detailed workflows/permissions remain open. | PASS — user-confirmed direction documented; exact GitHub main readback and Sandbox parity verified for DOC-003, DOC-007, DOC-008, DOC-011 and DOC-035 (5/5) |

| EV-115-010 | 2026-11-12 | Material and warehouse role discovery | Vinh's clarification in the current conversation | Construction-material operations are added to W115 discovery; Storekeeper is a new actor responsible for recording material receipts into the project warehouse. Detailed permissions, issue/approval workflow and inventory scope remain OPEN. | RECORDED — user-confirmed direction; documentation parity verification pending |
