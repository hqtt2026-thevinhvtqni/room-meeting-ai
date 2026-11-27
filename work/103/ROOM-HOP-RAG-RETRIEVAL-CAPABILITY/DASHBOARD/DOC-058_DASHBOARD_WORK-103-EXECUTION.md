# BẢNG ĐIỀU KHIỂN WORK 103 (READ-ONLY) / WORK 103 EXECUTION DASHBOARD
- **STT / Document ID:** DOC-058
- **Priority:** P1
- **Read order:** 6
- **Depends on:** DOC-001; DOC-055; DOC-056; DOC-057; DOC-035
- **Status:** ACTIVE — READ-ONLY PROJECTION (NOT VERIFIED)
- **Version / Updated:** 1.1 / 2026-11-27
- **Authority:** Vinh
- **Owner:** Xu / AI-01
- **Producer:** Vibe (created under Vinh's standing full-build authorization, 2026-11-08)

> Quy tắc nguồn sự thật: mọi giá trị dưới đây là chiếu rải (projection) từ hồ sơ chuẩn DOC-001 / DOC-055 / DOC-056 / DOC-057 / DOC-035 kèm tham chiếu bằng chứng. KHÔNG có giá trị mock. Dashboard KHÔNG thay thế quyết định gate; tiến độ trên dashboard không bao giờ là PASS theo nghĩa gate (DOC-001 §6, §8). Xác minh dashboard (schema, readback, browser) chưa hoàn tất — Batch 5 DOC-056 vẫn IN_PROGRESS.

## 1. Thông tin Work
| Mục | Giá trị | Nguồn |
|---|---|---|
| Work ID / Tên | 103 / ROOM-HOP-RAG-RETRIEVAL-CAPABILITY | DOC-001 |
| Sản phẩm | Evidence-grounded RAG retrieval capability cho ROOM-HOP | DOC-001 §1 |
| Repo / Nhánh chuẩn | hqtt2026-thevinhvtqni/room-meeting-ai / work/103-rag-retrieval-capability | DOC-001 |
| Final Authority | Vinh | DOC-001 |
| Lifecycle Orchestrator | Xu (AI-01) | DOC-001 |
| Chuẩn quản trị | Work 70 (lifecycle G0–G9, WP, evidence, dashboard) | DOC-056 |
| Ranh giới | Core :8000 là nguồn sự thật duy nhất; không Core/Host/Dispatcher thứ hai; nội dung truy xuất là input không tin cậy | DOC-001 §2 |

## 2. Trạng thái gate và vòng đời (2026-11-27)
| Gate / mốc | Trạng thái | Bằng chứng |
|---|---|---|
| Đồng bộ Sandbox → branch (G0 lịch sử) | PASS cho đồng bộ file | W103-SYNC-01 (DOC-035 archived entries) |
| Gate B — evidence-support decision set (build) | PASS build-level: 11/11 rows, CI run 42467375198 (head 3512690), Python 3.11+3.12 | EVD-008 |
| Gate A — adjudication độc lập dataset | OPEN / BLOCKED; Ka review recorded, B5 freeze/row-level dataset recording remains incomplete | DOC-063 / DEBT-ES-02 |
| Corpus diagnostic hai tầng (REPORT-ONLY, 50 query) | specs=50 match=49 no_answer_leak=0 false_abstention=0 contradiction_missed=1 | EVD-009, CI run 42559810631 |
| Corpus diagnostic v2 metrics (citation alignment + relaxed probe) | citation_misaligned=2 (Q037/Q045), expected_source_missed=2 (Q037/Q040) | EVD-010, CI run #96 |
| Independent gate Manifest V4 + Ka V3 (corpus-aligned) | **FAIL: no_answer_accuracy=0.300 vs floor 0.8** (giữ nguyên, không được suy yếu) | EVD-007/010, CI run #96 |
| Gate C design | BLOCKED chờ xử lý adjudication findings và DEBT-ES-08 citation-source alignment | DOC-063 / DEBT-ES-08 |
| E2E MCP :8020 → Core :8000 | CLOSED | DOC-035 LOG-005, DEBT-ES-04 |
| Tích hợp (Integration) | BLOCKED | DOC-001 §7 |
| Release | NOT PASS | DOC-001 §7 |
| Chuẩn hóa Work 70 | IN_PROGRESS / NOT PASS | DOC-056 |

## 3. Chỉ số CI mới nhất (AUTHORED_PENDING_INDEPENDENT_ADJUDICATION)
- **Run #96**, head c14939a4eab69a6995fc6289cabc30042eab2014 (workflow "Work 103 RAG Retrieval CI"):
  - V2 (50 specs): match=49, no_answer_leak=0, false_abstention=0, contradiction_missed=1 (Q040 — retrieval miss, zero candidates ≥ min_score 0.35; relaxed_best 0.19145), citation_misaligned=2 (Q037/Q045 — duplicate-content corpus; Q037 relaxed_best 0.353077), mismatch_other=0.
  - V1 (22 specs): match=21, contradiction_missed=1.
  - Unit suites PASS trên Python 3.11/3.12; independent gate FAIL 0.300 vs 0.8 (bảo toàn).
- **Chú ý trung thực:** 49/50 MATCH là bằng chứng build, KHÔNG phải adjudication (DEBT-ES-07). Ka đã ghi nhận độc lập các finding trong DOC-063; số liệu build vẫn không tự động trở thành adjudicated/frozen dataset.
- Root-cause Q040 (diagnostic v3, REPORT-ONLY): rank-1 span bị loại bởi ngưỡng; 6/12 query term zero-df phình IDF ~3x; counterfactual: mọi biến thể normalization khôi phục Q040 đều mở lại cả 10 no-answer leak. EVD-011.

## 4. Tiến độ chuẩn hóa (DOC-056)
| Batch | Phạm vi | Trạng thái |
|---|---|---|
| 0 | Governance baseline (DOC-001/055/056/057/035) | DONE |
| 1 | 00_ROOT + hồ sơ chính thức | DONE — Xu closed 2026-11-27; 4/4 pointer audit + CI disposition documented (DOC-061); independent gate unchanged |
| 2 | Lifecycle folders | IN_PROGRESS (mapping/classification DONE — DOC-059 + README indexes; physical moves DEFERRED có lý do) |
| 3 | 05_BUILD engineering map / WP register | DONE — register + source/CI mapping only (DOC-060/DOC-059); no physical source move implied |
| 4 | EVIDENCE migration | NOT_STARTED (prep audit xong — DOC-061 §2: 1 write target C7, 26 file) |
| 5 | DASHBOARD | IN_PROGRESS (DOC-058 đã tạo; verification chưa xong) |
| 6 | VERIFY / ACCEPT / RELEASE readiness | NOT_STARTED |

## 5. Nợ kỹ thuật mở (ghi nợ)
| Mã | Nội dung | Chủ |
|---|---|---|
| DEBT-ES-01 | Contract V3 defects: absence source binding, scope-limited flag semantics, support-source scope rule — FAIL; correction required | Ka |
| DEBT-ES-02 | Decision Set V1 row semantics reviewed; B5 row-level record + freeze SHA-256/attestation still BLOCKED — PARTIAL | Ka / Xu |
| DEBT-ES-06 | Retrieval-side misses/leaks: Q008 0.990, Q010, Q025, Q030, Q035, Q044, Q045, Q040 (relaxed_best 0.19145); QUERY_EXPANSIONS overfit risk | Ka/Qw |
| DEBT-ES-07 | Fact Specs V2: Q009/Q015/Q020/Q023 semantic corrections and Q037 source alignment required — FAIL | Ka |
| DEBT-ES-03 | Thiết kế/phê duyệt Gate C (chỉ sau adjudication findings và citation alignment) | Xu |
| DEBT-ES-04 | Quyết định tích hợp riêng cho E2E MCP :8020 → Core :8000 | Xu |
| DEBT-ES-08 | Citation-source alignment — metric Gate C ứng viên (fold vào Gate C design sau adjudication) | Xu / Ka |
| DEBT-ES-05 | Đăng ký artifact mới trong DOC-055/DOC-057 | CLOSED — Xu confirmed 2026-11-27; DOC-062/DOC-055 and EVD-013/DOC-057 exact-readback verified |
| DEBT-ES-09 | Browser verification DOC-058 | OPEN — browser verification not performed; DOC-058 remains NOT VERIFIED |
| DEBT-ES-10 | Closure Batch 1: inbound-link audit + CI regression disposition | CLOSED — Xu approved 2026-11-27 per DOC-061; 4/4 pointer audit + CI disposition recorded; independent gate unchanged |

## 6. Chỉ mục bằng chứng (DOC-057)
EVD-001 (CI 40668733280) · EVD-002 (blind pool V1, UNLABELED) · EVD-003 (thí nghiệm có kiểm soát lịch sử) · EVD-004 (replication addendum) · EVD-005 (Gate A/B report) · EVD-006 (evidence lịch sử) · EVD-007 (run #85 FAIL độc lập 0.300) · EVD-008 (Gate A/B CI runs) · EVD-009 (corpus diagnostic 50 query) · EVD-010 (v2 metrics run #96) · EVD-011 (root-cause diagnostic v3) · EVD-012 (DOC-061 inbound-link/CI disposition + main drift) · EVD-013 (DOC-062 handover integrity anchors) · EVD-014 (DOC-063 Ka independent adjudication DEBT-ES-01/02/07).

## 7. Bước tiếp theo (critical path)

**Adjudication 2026-11-27 (DOC-063 / EVD-014):** Ka đã hoàn tất review read-only. Kết quả: DEBT-ES-01 FAIL; DEBT-ES-02 PARTIAL / B5 freeze BLOCKED; DEBT-ES-07 FAIL. Integrity anchors của DOC-062 khớp Git blob SHA; SHA-256 trên UTF-8 content được ghi trong DOC-063. Không có thay đổi code, tests, labels, fixtures, threshold, CI hoặc gate.

**Việc tiếp theo:**
1. Chuẩn bị bản Contract V4 hoặc amendment có version cho F01/F02 và support-source scope; bổ sung negative tests sau khi được duyệt.
2. Chuẩn bị Fact Specs phiên bản mới, không ghi đè V2; xử lý Q009/Q015/Q020/Q023 và Q037 source alignment.
3. Xu xác nhận blind-process/freeze attestation; B5 cần raw-byte SHA-256 và row-level reviewer/resolution fields trước khi đóng Gate A.
4. Giữ Gate C BLOCKED cho đến khi DEBT-ES-08 citation-source alignment được giải quyết rõ ràng.
5. Batch 4 vẫn PREPARED, chưa di chuyển; cần một commit phối hợp gồm CI C7 tee path, hash/readback/link checks.
6. Batch 6 QE độc lập chưa bắt đầu.

WP index: WP-103-01 retrieval core · 02 eval baseline · 03 evidence-support stage · 04 corpus diagnostic · 05 standardization · 06 Gate C design (BLOCKED) · 07 E2E (CLOSED) · 08 retrieval remediation (OPEN) — chi tiết DOC-060.

## Xu decisions — 2026-11-27 (LOG-W103-20261127-003)
- Batch 1 CLOSED (governance/build-level only); independent gate FAIL 0.300 vs 0.8 preserved.
- Batch 3 CLOSED for register and mapping only; no source/test/evidence migration implied.
- Four historical blind-labeling files found only on main are preserved in place; no silent copy/delete. Ka may use them as read-only context pending provenance verification.
- DEBT-ES-05 CLOSED after DOC-055/DOC-057 exact readback including DOC-062/EVD-013.
- DEBT-ES-09 OPEN; browser verification of this dashboard has not been done. Dashboard status remains NOT VERIFIED.
- Gate C remains BLOCKED pending adjudication findings and explicit DEBT-ES-08 citation-alignment disposition.


## Adjudication update — DOC-063 / EVD-014 (2026-11-27)
- Ka's independent read-only review is recorded in DOC-063 (blob `c66bcfb7cee83a7819a9d399c4cb26dd26e847b6`; commit `fce400abd8687bb992638673c264ae65019a9709`).
- DEBT-ES-01: **FAIL** — Contract V3 requires source-binding for absence evidence, correct handling of the scope-limited flag, and explicit support-source scope semantics.
- DEBT-ES-02: **PARTIAL / FREEZE BLOCKED** — Decision Set V1 semantic review recorded (13 rows: 11 gate-counted + 2 pending); B5 independent reviewer/resolution fields and valid freeze remain outstanding.
- DEBT-ES-07: **FAIL** — Q009/Q015/Q020/Q023 findings and Q037 source alignment require versioned correction/resolution; original V2 remains unchanged.
- No source, tests, labels, fixture, thresholds, CI workflows or gates were changed by this review. Gate A remains OPEN/BLOCKED; Gate C BLOCKED; independent retrieval gate remains FAIL 0.300 vs 0.800; Release NOT PASS.
- DOC-058 remains **NOT VERIFIED** because browser verification has not been performed. This note is a source-backed status update, not a gate decision.
