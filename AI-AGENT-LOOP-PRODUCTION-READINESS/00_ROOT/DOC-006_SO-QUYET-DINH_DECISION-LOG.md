# DECISION LOG — WORK 102
- Document ID: DOC-006 | Priority: P0 | Read order: 6 | Version: 1.0 | Status: ACTIVE

| Decision ID | Decision | Authority | Date/source | Status |
|---|---|---|---|---|
| W102-DEC-001 | Work 102 is common Agent Loop orchestration and closed-loop acceptance; do not duplicate queue, dispatcher, registry, task DB, execution host or MCP registry | Vinh / Xu record | 2026-10-24 convergence ledger | ACTIVE |
| W102-DEC-002 | Reuse Work 30/52 requirements and prototypes as references; preserve original artifacts | Vinh / Xu record | 2026-10-24 convergence ledger | ACTIVE |
| W102-DEC-003 | Repair budget max_repairs=2 and max_test_runs=3 per defect cycle | Vinh | 2026-10-24 repair budget decision | LOCKED in existing evidence |
| W102-DEC-004 | No MCP 8020 use; reconcile legacy references to approved boundaries before live integration | Vinh | 2026-11-07 instruction | ACTIVE |
| W102-DEC-005 | Work 70 is governance/layout standard only; Work 102 remains independent and must not alter Work 70 | Vinh | 2026-11-07 | ACTIVE |
| W102-DEC-006 | Preserve legacy source/evidence paths during structural alignment; use mapping and staged migration | Xu | 2026-11-07 | ACTIVE |

 
## W102-DEC-007 — Chuẩn hóa mục 6 theo Work 70 Standard v1.2 (2026-11-07)
- **Decision:** `06_VERIFY/` là phase-06 verification; `EVIDENCE/` là kho cross-phase evidence duy nhất; `05_BUILD/06_EVIDENCE/` chỉ là staging; top-level `06_EVIDENCE/` cũ là legacy compatibility/archive và không nhận hồ sơ canonical mới.
- **Authority:** Vinh — chỉ thị trực tiếp trong phiên; Xu / AI-01 ghi nhận và triển khai trong phạm vi chuẩn hóa tài liệu.
- **Implementation:** DOC-014 canonical path đặt tại `EVIDENCE/DOC-014_SO-DANG-KY-BANG-CHUNG_EVIDENCE-REGISTER.md`; DOC-001/003/033/036/055 được cập nhật đồng bộ; DOC-034 ghi biên bản và DOC-035 ghi nhật ký.
- **Preservation:** Không xóa/di chuyển raw evidence hoặc run bundles lịch sử. DOC-037 ghi nhận 72 legacy path entries; file-level classification, hash/link audit và migration vẫn OPEN.
- **Status:** APPROVED POLICY / SANDBOX DOCUMENTATION UPDATED / FINAL READ-BACK REQUIRED / FILE-LEVEL MIGRATION OPEN / GITHUB SYNC NOT VERIFIED / NOT ACCEPTED / NOT RELEASED.


## W102-DEC-008 — Hợp nhất Work 51 + Work 52 vào Work 102 làm nền tảng triển khai duy nhất
- **Authority:** Vinh (chỉ thị trực tiếp ngày 2026-11-12).
- **Recorded by:** Xu / AI-01; Vi / CODER.
- **Decision:** Work 102 là Work canonical duy nhất cho tích hợp và phát triển tiếp Agent Loop. Work 51 và Work 52 được giữ nguyên làm nguồn tham chiếu, provenance và evidence; không xóa/đổi trạng thái DONE, không copy nguyên runtime, không tạo task schema/queue/dispatcher/Core/registry/Execution Host thứ hai.
- **Work 51 contribution:** Coder–Tester role separation; tester-only acceptance criteria; artifact hash/version; bounded repair; timeout/transport/hash/evidence negative behavior; sandbox hardening patterns.
- **Work 52 contribution:** provider-neutral task/event model; adapter ports; correlation/idempotency/scope/approval; event sequence; provider dialect isolation; cancellation confirmation; execution status tách khỏi acceptance verdict.
- **Work 102 ownership:** common orchestration policy, role handoff, authorization boundary use, repair/retry budgets, candidate-bound acceptance/recovery/evidence.
- **Authority boundaries:** Core :8000 remains sole task/state/event authority; Work 01/02/22 identity/authorization; Work 20/21 provider/agent bindings; Work 28 tool contracts; Work 12/13/27 execution/isolation; Work 14 E2E consumer; Work 24 PC/workspace bridge; Work 70 lifecycle standard only.
- **Contract rule:** W52 contract is the preferred provider-neutral design reference, not an automatically approved Core schema. Map against actual Core schema and obtain owner approval before promotion. Preserve W51 Coder opacity rule. Keep execution state, task state and acceptance verdict separate.
- **Budget:** retain W102 locked max_repairs=2 and max_test_runs=3 per defect cycle.
- **Preservation:** all three Work source/evidence trees remain intact. No code/test/runtime modified and no source copied in this decision-recording phase.
- **Implementation reference:** DOC-012 consolidated architecture and DOC-013 implementation plan.
- **Status:** DECISION RECORDED; WORK 102 CONSOLIDATION ACTIVE; WP0 PARTIAL; CORE CONTRACT COMPATIBILITY NOT VERIFIED; LIVE INTEGRATION NOT VERIFIED; NOT ACCEPTED / NOT RELEASED.
[KÝ: VI | CODER]
