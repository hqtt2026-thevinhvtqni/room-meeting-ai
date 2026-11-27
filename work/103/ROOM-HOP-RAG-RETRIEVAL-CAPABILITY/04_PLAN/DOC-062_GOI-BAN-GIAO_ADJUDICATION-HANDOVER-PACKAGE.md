# GÓI BÀN GIAO ADJUDICATION WORK 103 (KA) + PACK QUYẾT ĐỊNH (XU)
- **STT / Document ID:** DOC-062
- **Priority:** P0 (critical path)
- **Read order:** 10
- **Depends on:** DOC-001; DOC-035; DOC-057; DOC-059; DOC-061
- **Status:** ACTIVE — HANDOVER PACKAGE (Vibe không tự phê chuẩn)
- **Version / Updated:** 1.0 / 2026-11-27
- **Owner:** Ka (adjudication) / Xu (coordination)
- **Authority:** Vinh
- **Producer:** Vibe (2026-11-27, standing authorization; "xây tiếp, không chờ" — LOG-W103-20261127-002)

## 1. Artifact Ka cần phê chuẩn (neo toàn vẹn tại head a310db46; Ka tính lại SHA-256 lúc freeze theo B5)

| # | Artifact | Đường dẫn | Git blob SHA (neo tạm) | Phải làm | Debt |
|---|---|---|---|---|---|
| 1 | Interface Contract V3 | 03_ARCHITECTURE/EVIDENCE_SUPPORT_STAGE_CONTRACT_V3.md | 4c19b678e9ff37062081c0420c9de96f2852adfd | Review kiến trúc độc lập (B1..B6 closures §1; schema §2; scope §3; conflict §4; metamorphic §5) | DEBT-ES-01 |
| 2 | Decision set V1 (15 rows: T1,T2,T3,T4a,T4b,T5,T6,T7,C1,C2,C3 + Q008-PENDING, Q037-PENDING) | 05_TEST/EVIDENCE_SUPPORT_DECISION_SET_V1.json | 4f782f2d37620937f054de4a9c3a1a476b4ad7d9 | Adjudication từng row theo B5 (§6): independent decision + rationale + resolution; 2 row PENDING hiện không tính gate | DEBT-ES-02 |
| 3 | Fact specs V2 (50 rows, dataset work103.evidence-support-fact-specs.v2) | 05_TEST/EVIDENCE_SUPPORT_FACT_SPECS_V2.json | 00bb8f89e7fe380ee5c8695a4d81002a62a688cb | Adjudication 50 rows: ideal_decision + support/absence/negation patterns + query_scope + các field mới (expected_source/citation) | DEBT-ES-07 |
| 4 | Fact specs V1 (22 rows, historical) | 05_TEST/EVIDENCE_SUPPORT_FACT_SPECS_V1.json | ed26f8f8ced43a4fcd631510f9882d2bd2d93301 | Đã superseded bởi V2 (V1 rows carried unchanged); chỉ tham chiếu | — |

## 2. Các row cần chú ý đặc biệt (quan điểm tác giả, quyết định cuối là của Ka)

1. **Q004/Q008 (documented absence):** đề xuất EXPLICITLY_UNSPECIFIED dựa trên absence statement có sẵn trong corpus; leak analysis của Ka gọi Q008 borderline. Chú ý kỷ luật T2: chỉ EXPLICITLY_UNSPECIFIED khi chunk chứa absence statement thực sự được retrieve.
2. **Q044 (contract probe):** cố ý INSUFFICIENT_EVIDENCE (không có absence statement cho default min_score) — kiểm tra quy tắc fail-closed của contract.
3. **Q037/Q045 (duplicate-content):** cite đúng nội dung nhưng từ source trùng nội dung (RAG_RETRIEVAL_ARCHITECTURE.md thay vì architecture.md). Quyết định cần: chấp nhận duplicate-source citation hay yêu cầu alignment metric (DEBT-ES-08).
4. **Q040 (retrieval miss):** CONTRADICTED về mặt label nhưng retrieval trả 0 candidates tại min_score 0.35 (relaxed_best 0.19145). Nếu Ka giữ label, harness sẽ báo CONTRADICTION_MISSED — đây là By-design finding thuộc DEBT-ES-06, không phải lỗi specs.
5. **Q015/Q023/Q050 (negative-form answerable):** span chứa phủ định nhưng mệnh đề query khớp — đề xuất SUPPORTED; cần Ka xác nhận cách đọc.

## 3. Bối cảnh chuỗi blind-labeling V1–V5 (từ main, EVD-012)

Trên main (head 83f39944, thư mục lạc work/103/06_EVIDENCE/) có BLIND_LABELING_GATE_STATUS_20261028.md + 3 review record V4: chuỗi Ka/Qw chốt ở **manifest V5 hash/byte-size verification FAIL → freeze BLOCKED**. Theo B5, freeze SHA-256 của specs V2 cần hash được xác thực từ đầu: Ka nên xử lý/xác nhận lại nguồn file trước khi freeze. Đề xuất Xu: chuyển 4 file này về 06_EVIDENCE chuẩn trên nhánh làm việc (không copy im lặng — cần quyết định).

## 4. Pack quyết định Xu (không chặn, nhưng cần cho closure)

| # | Quyết định | Tham chiếu |
|---|---|---|
| 1 | Xác nhận closure Batch 1 (link audit PASS 4/4 + CI disposition xong) | DOC-061 §1/§4; DEBT-ES-10 |
| 2 | Xử lý drift: thư mục lạc work/103/06_EVIDENCE trên main | DOC-061 §3; EVD-012 |
| 3 | Browser verification DOC-058 + xác nhận closure DEBT-ES-05 | DEBT-ES-09; LOG-006 |
| 4 | Gate C design: đầu vào đã đủ (EVD-009/010/011/012 + citation alignment) — thiết kế SAU adjudication | DEBT-ES-03/08 |
| 5 | Xác nhận register Batch 3 (DOC-060 WP-103-01..08) | DOC-060 |

## 5. Số liệu build-level Ka cần biết (KHÔNG phải adjudication)

- V2 (50 rows): match=49, no_answer_leak=0, false_abstention=0, contradiction_missed=1 (Q040), citation_misaligned=2 (Q037/Q045), expected_source_missed=2 (Q037/Q040).
- V1 (22 rows): match=21, contradiction_missed=1, citation_misaligned=0, expected_source_missed=1.
- Unit suites PASS py3.11/3.12; independent gate FAIL 0.300 vs 0.8 bảo toàn (root-cause EVD-011).
- 49/50 MATCH chỉ là bằng chứng build từ tác giả specs; giá trị adjudication nằm ở việc Ka độc lập với tài liệu corpus gốc.
