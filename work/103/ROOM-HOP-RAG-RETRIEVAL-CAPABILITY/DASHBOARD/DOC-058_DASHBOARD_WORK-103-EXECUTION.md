# BẢNG ĐIỀU KHIỂN WORK 103 (READ-ONLY) / WORK 103 EXECUTION DASHBOARD
- **STT / Document ID:** DOC-058
- **Priority:** P1
- **Read order:** 6
- **Depends on:** DOC-001; DOC-055; DOC-056; DOC-057; DOC-035
- **Status:** ACTIVE — READ-ONLY PROJECTION (NOT VERIFIED)
- **Version / Updated:** 1.0 / 2026-11-09
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
| Chuẩn quản trị | Work 70 (lifecycle G0–G9, WP, evidence, dashboard) | DOC-056 §1 |
| Ranh giới | Core :8000 là nguồn sự thật duy nhất; không Core/Host/Dispatcher thứ hai; nội dung truy xuất là input không tin cậy | DOC-001 §2 |

## 2. Trạng thái gate và vòng đời (2026-11-09)
| Gate / mốc | Trạng thái | Bằng chứng |
|---|---|---|
| Đồng bộ Sandbox → branch (G0 lịch sử) | PASS cho đồng bộ file | W103-SYNC-01 (DOC-035 archived entries) |
| Gate B — evidence-support decision set (build) | PASS build-level: 11/11 rows, CI run 42467375198 (head 3512690), Python 3.11+3.12 | EVD-008 |
| Gate A — adjudication độc lập dataset | OPEN / BLOCKED cho release use | DEBT-ES-02 (Ka), DOC-035 LOG-005 |
| Corpus diagnostic hai tầng (REPORT-ONLY, 50 query) | specs=50 match=49 no_answer_leak=0 false_abstention=0 contradiction_missed=1 | EVD-009, CI run 42559810631 |
| Corpus diagnostic v2 metrics (citation alignment + relaxed probe) | citation_misaligned=2 (Q037/Q045), expected_source_missed=2 (Q037/Q040) | EVD-010, CI run #96 head c14939a4 |
| Independent gate Manifest V4 + Ka V3 (corpus-aligned) | **FAIL: no_answer_accuracy=0.300 vs floor 0.8** (giữ nguyên, không được suy yếu) | EVD-007/010, CI run #96 |
| Gate C design | BLOCKED chờ adjudication | DEBT-ES-03/08 |
| E2E MCP :8020 → Core :8000 | CLOSED | DOC-035 LOG-005, DEBT-ES-04 |
| Tích hợp (Integration) | BLOCKED | DOC-001 §7 |
| Release | NOT PASS | DOC-001 §7 |
| Chuẩn hóa Work 70 | IN_PROGRESS / NOT PASS | DOC-056 |

## 3. Chỉ số CI mới nhất (AUTHORED_PENDING_INDEPENDENT_ADJUDICATION)
- **Run #96**, head c14939a4eab69a6995fc6289cabc30042eab2014 (workflow "Work 103 RAG Retrieval CI"):
  - V2 (50 specs): match=49, no_answer_leak=0, false_abstention=0, contradiction_missed=1 (Q040 — retrieval miss, zero candidates ≥ min_score 0.35; relaxed_best 0.19145), citation_misaligned=2 (Q037/Q045 — duplicate-content corpus; Q037 relaxed_best 0.353077), mismatch_other=0.
  - V1 (22 specs): match=21, contradiction_missed=1.
  - Unit suites PASS trên Python 3.11/3.12; independent gate FAIL 0.300 vs 0.8 (bảo toàn).
- **Chú ý trung thực:** 49/50 MATCH là bằng chứng build, KHÔNG phải adjudication (DEBT-ES-07). Chỉ số pending cho đến khi Ka phê duyệt và freeze SHA-256 theo B5.
- Root-cause Q040 (diagnostic v3, REPORT-ONLY): rank-1 span bị loại bởi ngưỡng; 6/12 query term zero-df phình IDF ~3x; counterfactual: mọi biến thể normalization khôi phục Q040 đều mở lại cả 10 no-answer leak. EVD-011.

## 4. Tiến độ chuẩn hóa (DOC-056)
| Batch | Phạm vi | Trạng thái |
|---|---|---|
| 0 | Governance baseline (DOC-001/055/056/057/035) | DONE |
| 1 | 00_ROOT + hồ sơ chính thức | IN_PROGRESS (link audit + CI disposition còn treo) |
| 2 | Lifecycle folders | IN_PROGRESS (mapping/classification DONE — DOC-059 + README indexes; physical moves DEFERRED có lý do) |
| 3 | 05_BUILD engineering map / WP register | DONE-register (DOC-060, WP-103-01..08; chờ Xu xác nhận) |
| 4 | EVIDENCE migration | NOT_STARTED |
| 5 | DASHBOARD | IN_PROGRESS (DOC-058 đã tạo; verification chưa xong) |
| 6 | VERIFY / ACCEPT / RELEASE readiness | NOT_STARTED |

## 5. Nợ kỹ thuật mở (ghi nợ)
| Mã | Nội dung | Chủ |
|---|---|---|
| DEBT-ES-01 | Review kiến trúc độc lập EVIDENCE_SUPPORT_STAGE_CONTRACT_V3.md (HIGH) | Ka |
| DEBT-ES-02 | Adjudication độc lập EVIDENCE_SUPPORT_DECISION_SET_V1.json + freeze SHA-256 (B5) | Ka |
| DEBT-ES-06 | Retrieval-side misses/leaks: Q008 0.990, Q010, Q025, Q030, Q035, Q044, Q045, Q040 (relaxed_best 0.19145); QUERY_EXPANSIONS overfit risk | Ka/Qw |
| DEBT-ES-07 | Adjudication độc lập 50 rows EVIDENCE_SUPPORT_FACT_SPECS_V2.json (bao gồm expected-source/citation fields) | Ka |
| DEBT-ES-03 | Thiết kế/phê duyệt Gate C (chỉ sau adjudication) | Xu |
| DEBT-ES-04 | Quyết định tích hợp riêng cho E2E MCP :8020 → Core :8000 | Xu |
| DEBT-ES-08 | Citation-source alignment — metric Gate C ứng viên (fold vào Gate C design sau adjudication) | Xu |
| DEBT-ES-05 | Đăng ký artifact mới trong DOC-055/DOC-057 | Xu — ĐÃ ĐÓNG bởi mapping 2026-11-09 (chờ Xu xác nhận) |
| DEBT-ES-09 | Browser verification DOC-058 + xác nhận closure DEBT-ES-05 | Xu |
| DEBT-ES-10 | Closure Batch 1: inbound-link audit + CI regression disposition | Xu |

## 6. Chỉ mục bằng chứng (DOC-057)
EVD-001 (CI 40668733280) · EVD-002 (blind pool V1, UNLABELED) · EVD-003 (thí nghiệm có kiểm soát lịch sử) · EVD-004 (replication addendum) · EVD-005 (Gate A/B report) · EVD-006 (evidence lịch sử) · EVD-007 (run #85 FAIL độc lập 0.300) · EVD-008 (Gate A/B CI runs) · EVD-009 (corpus diagnostic 50 query) · EVD-010 (v2 metrics run #96) · EVD-011 (root-cause diagnostic v3).

## 7. Bước tiếp theo (critical path)

WP index: WP-103-01 retrieval core · 02 eval baseline · 03 evidence-support stage · 04 corpus diagnostic · 05 standardization · 06 Gate C design (BLOCKED) · 07 E2E (CLOSED) · 08 retrieval remediation (OPEN) — chi tiết DOC-060.
1. Ka: DEBT-ES-01/02/07 — adjudication độc lập là nút thắt cổ chai của mọi gate còn lại.
2. Xu: DEBT-ES-03/08 (Gate C design sau adjudication), DEBT-ES-04, xác nhận DEBT-ES-05, verification Batch 5.
3. Vibe: tiếp tục build theo ủy quyền thường trực; không tự phê duyệt.
