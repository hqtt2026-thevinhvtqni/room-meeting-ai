# BÁO CÁO RÀ SOÁT LIÊN KẾT NGƯỢC VÀ DISPOSITION CI — WORK 103 (BATCH 1 CLOSURE + BATCH 4 PREP)
- **STT / Document ID:** DOC-061
- **Priority:** P1
- **Read order:** 9
- **Depends on:** DOC-001; DOC-055; DOC-056; DOC-057; DOC-035; DOC-059
- **Status:** ACTIVE — AUDIT REPORT (REPORT-ONLY)
- **Version / Updated:** 1.0 / 2026-11-27
- **Owner:** Xu / AI-01
- **Authority:** Vinh
- **Producer:** Vibe (2026-11-27, under Vinh's standing full-build authorization and the 2026-11-09 "xây tiếp, không chờ" instruction; DOC-035 LOG-W103-20261127-001)

> Phạm vi: rà soát liên kết ngược (inbound-link audit) cho Batch 1, audit tiêu dùng bằng chứng cho Batch 4 prep, và disposition CI regression. REPORT-ONLY: không file nào bị di chuyển/xóa; không gate thay đổi.

## 1. Kết quả audit pointer legacy (Batch 1)

| Pointer | Kiểm chứng tại head 0c89b311 | Target | Kết quả |
|---|---|---|---|
| 00_ROOT/WORK_MANIFEST.md | Có, đúng mẫu LEGACY COMPATIBILITY POINTER | 00_ROOT/DOC-001_BAN-TUYEN-NGON_WORK-MANIFEST.md | PASS |
| BIEN_BAN.md (gốc Work) | Có | 00_ROOT/DOC-034_BIEN-BAN_HOP-WORK-103-MINUTES.md | PASS |
| KE_HOACH_THI_CONG_XU.md (gốc Work) | Có | 04_PLAN/DOC-045_KE-HOACH-THI-CONG_WORK-103-ROADMAP.md | PASS |
| NHAT_KY_HOP_THI_CONG.md (gốc Work) | Có | 00_ROOT/DOC-035_NHAT-KY-THI-CONG_WORK-103-EXECUTION-LOG.md | PASS |

Ghi chú: WORK_MANIFEST.md chỉ tồn tại ở 00_ROOT (đúng theo ánh xạ DOC-055); không có bản trùng ở gốc Work. Cả 4 pointer đều có rule "do not add new content here" — nhất quán với DOC-055.

## 2. Audit tham chiếu 06_EVIDENCE (Batch 4 prep)

- Code/CI tiêu dùng 06_EVIDENCE vật lý: duy nhất 1 điểm — bước grounded-abstention trong CI GHI file (tee sang 06_EVIDENCE/grounded_abstention_diagnostic.json, consumer C7 của DOC-059). Đây là write target, phải sửa đồng bộ khi di chuyển (Batch 4).
- Tài liệu tham chiếu 06_EVIDENCE dưới dạng đường dẫn legacy: các báo cáo trong chính 06_EVIDENCE và DOC-055/057 (đã ghi chính sách "legacy read path"). Không phát hiện tham chiếu vật lý nào từ code.
- Kết luận Batch 4: điều kiện di chuyển = (a) sửa C7 trong workflow cùng commit; (b) hash/readback toàn bộ 26 file; (c) audit link nội bộ. Chưa thực hiện.

## 3. PHÁT HIỆN PATH-DRIFT CHÉO NHÁNH (quan trọng)

Nhánh mặc định **main** chứa thư mục lạc work/103/06_EVIDENCE/ (head main 83f39944) với 4 file lịch sử KHÔNG tồn tại trên nhánh làm việc:
1. BLIND_LABELING_GATE_STATUS_20261028.md — nhật ký gate blind-labeling: chuỗi Ka/Qw V1→V5 (Qw nộp labels, Ka review từng version, corpus manifest v1→v3, gate BLOCKED liên tục: provenance/hash/freeze chưa xác thực).
2. KA_FOLLOWUP_REVIEW_QW_MANIFEST_V4_20261029.md
3. KA_INDEPENDENT_REVIEW_QW_V4_20261029.md
4. KA_INDEPENDENT_REVIEW_QW_LABELS_20261029.md

Đánh giá: nhánh làm việc chỉ giữ QW_BLIND_LABELS_50_QUERIES_V5_20261029.md và KA_INDEPENDENT_REVIEW_V5_SYNC_GATE_20261029.md — tức phần ĐẦU của chuỗi adjudication blind-labeling (V1–V4 + gate status) chỉ tồn tại trên main, ngoài thư mục Work chuẩn. Theo chính sách DOC-057 (không copy im lặng), KHÔNG copy; đề xuất Xu/Ka quyết định: (a) đưa 4 file về ROOM-HOP-RAG-RETRIEVAL-CAPABILITY/06_EVIDENCE/ trên nhánh làm việc (prefer), và (dọn thư mục lạc trên main — ngoài phạm vi ủy quyền nhánh này). Bối cảnh quan trọng cho Ka: chuỗi này chốt ở "V5 manifest hash/byte-size verification FAIL; freeze BLOCKED" — liên quan trực tiếp DEBT-ES-02/07.

## 4. Disposition CI regression (Batch 1)

- Các run CI từ 42467546737 (head f56f86cb, 2026-11-08) đến nay: unit suites/py_compile/Gate B/baseline PASS trên Python 3.11+3.12; điểm fail DUY NHẤT là independent gate "Manifest V4 + Ka V3 corpus-aligned" (no_answer_accuracy=0.300 vs floor 0.8).
- Disposition: fail này là đặc tính dữ liệu/gate (root-cause: EVD-011 — single-threshold lexical retrieval không tách được no-answer; normalization khôi phục Q040 mở lại 10 leak), KHÔNG phải do di chuyển tài liệu. Gate giữ nguyên, không suy yếu; remediation thuộc WP-103-08 (DEBT-ES-06) chờ quyết định Ka/Qw.
- Batch 1 exit criteria "CI regression disposition" → ĐÃ CÓ disposition văn bản này (build-level). Batch 1 có thể đóng khi Xu xác nhận.

## 5. Kết luận
- Batch 1: link audit PASS (4/4 pointer); CI disposition xong — chờ Xu xác nhận closure.
- Batch 4 prep: đủ điều kiện kiện toàn (1 write target C7 + 26 file + audit link).
- Phát hiện mới cần phối hợp: main-branch evidence drift (mục 3) — chuyển cho Xu (dọn path) và Ka (bối cảnh adjudication V1–V5).
