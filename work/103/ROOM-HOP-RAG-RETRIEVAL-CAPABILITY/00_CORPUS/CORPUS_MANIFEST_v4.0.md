# CORPUS MANIFEST v4.0 — WORK 103 ROOM-HOP-RAG-RETRIEVAL-CAPABILITY

- **Ngày phát hành:** 2026-10-29 (UTC+07:00)
- **Người lập:** Qc — Coder (theo chỉ thị đồng bộ của Ka/Xu sau rà soát GitHub 2026-10-29)
- **Trạng thái:** FROZEN / ĐÃ KHÓA — mọi thay đổi nội dung corpus phải tăng version và có phê duyệt mới của Xu.
- **Nguồn sự thật:** `work/103/ROOM-HOP-RAG-RETRIEVAL-CAPABILITY/05_TEST/EVAL_SET.json` (version 2), commit cơ sở `5f91f3ea2143dafaa5af958dc2bb431399e93621`, tree `8c05feccedb83e2d44d01b09d1c9a63fbd12cb5d`.
- **Phạm vi:** manifest này khai báo 8 tài liệu corpus được đóng băng cho đánh giá Work 103; không chứa nhãn truy vấn (xem tệp nhãn V5 tại `06_EVIDENCE/QW_BLIND_LABELS_50_QUERIES_V5_20261029.md`).

## 1. Hash nền đã kiểm chứng trong phiên (raw bytes, SHA-256)

| Đối tượng | Giá trị |
|---|---|
| `EVAL_SET.json` — kích thước | 11641 bytes |
| `EVAL_SET.json` — file_sha256 | `ab60cabdeee6254e11ee6889c20b6f2e68cd5072687bafcb314fb7c9a37c9f07` |
| `EVAL_SET.json` — canonical_sha256 | `03d1c964ce3368b89d5fcfcc56c6b1c2d0a8079b109055f78e183d4fd17e15ae` |
| Freeze manifest `FROZEN_EVAL_SET_v2.json` | `e61e96af04bee23bf5a514169d626d2e9912d6920442e1f2504f8175bfd52b47` |

Quy ước canonical: `json.dumps(sort_keys=True, separators=(',',':'), ensure_ascii=False)` mã hóa UTF-8 trước khi băm — đồng nhất với công cụ `04_CODE/freeze_eval_set.py` và `04_CODE/verify_frozen_eval_set.py` (đã chạy PASS trong phiên này).

## 2. Danh mục 8 tài liệu corpus (raw-byte SHA-256 theo từng tài liệu)

Băm tính trên raw bytes UTF-8 của trường `text` nguyên trạng trong EVAL_SET v2.

```
docs/bien-ban-hop-tuan-ont.md|279|aa5927ce0de6cbe9ccd2da58d4918c432de9b3b0a52f3cb6d3bb2696c936599b
docs/quy-trinh-xu-ly-su-co-mang.md|292|6c1ae2b5c58304a06537db0dc57f949be691696c087f564b4e2b95c756e3e975
docs/ke-hoach-giao-hang.md|207|636b655f488b5d797181c85a226b3c03a972644629bfc837b663f79ccb48816a
docs/bao-cao-doanh-thu.md|207|3d3e63553f69e9796325694efc09731e54b10918caa57288031893b38c0b1a85
docs/ky-luat-hop.md|209|13bdc553692c6c7c7ec04e0429e7e9aad6c8be50c6c4d4b04e44177aaae4c02f
docs/bao-mat-thong-tin.md|238|232b532ee5ff9c882814ac9318e6884006c1f8c8087f775843af804a60179b24
docs/nhiem-vu-tuan-42.md|242|28e0f03d7731558c05b8f1be6677a4b6b5d78f90da4aa35077fb7abfb2750281
docs/quy-dinh-cong-tac.md|228|b9c7f2c3c6f13f7016fc0615bc8835d1edcf14433378fbbc59ab91517d8fc21c
```

| # | source_id | text_bytes | text_sha256 (raw bytes) |
|---|---|---|---|
| 1 | `docs/bao-cao-doanh-thu.md` | 207 | `3d3e63553f69e9796325694efc09731e54b10918caa57288031893b38c0b1a85` |
| 2 | `docs/bao-mat-thong-tin.md` | 238 | `232b532ee5ff9c882814ac9318e6884006c1f8c8087f775843af804a60179b24` |
| 3 | `docs/bien-ban-hop-tuan-ont.md` | 279 | `aa5927ce0de6cbe9ccd2da58d4918c432de9b3b0a52f3cb6d3bb2696c936599b` |
| 4 | `docs/ke-hoach-giao-hang.md` | 207 | `636b655f488b5d797181c85a226b3c03a972644629bfc837b663f79ccb48816a` |
| 5 | `docs/ky-luat-hop.md` | 209 | `13bdc553692c6c7c7ec04e0429e7e9aad6c8be50c6c4d4b04e44177aaae4c02f` |
| 6 | `docs/nhiem-vu-tuan-42.md` | 242 | `28e0f03d7731558c05b8f1be6677a4b6b5d78f90da4aa35077fb7abfb2750281` |
| 7 | `docs/quy-dinh-cong-tac.md` | 228 | `b9c7f2c3c6f13f7016fc0615bc8835d1edcf14433378fbbc59ab91517d8fc21c` |
| 8 | `docs/quy-trinh-xu-ly-su-co-mang.md` | 292 | `6c1ae2b5c58304a06537db0dc57f949be691696c087f564b4e2b95c756e3e975` |

## 3. Khóa tổng corpus (aggregates)

| Khóa | Quy ước tính | SHA-256 |
|---|---|---|
| corpus_source_ids_canonical | canonical danh sách 8 `source_id` đã sắp xếp | `8ec8e622e32c1be4e2454efce3408780cdd237b3a8f972ffe532b1930e3f5ce1` |
| corpus_documents_canonical | canonical toàn bộ đối tượng `documents` theo thứ tự tệp | `edd22d0dcba4ba4be1de2140e933e4d9c0b4d16f65c67d00c5d59616ff2b0a31` |
| corpus_texts_concat_raw | SHA-256 trên chuỗi nối raw bytes `text` theo thứ tự tệp | `80766cc77d26424b9ef04a0771cf399d41d673dd71b258f79ed5a2e4df9ee80b` |

## 4. Trạng thái đóng băng

- Dữ liệu corpus KHÓA tại EVAL_SET v2; tái xác minh bằng `python3 04_CODE/verify_frozen_eval_set.py` → exit 0, "FROZEN SET INTACT" (log: `06_EVIDENCE/frozen/verify_stdout_20261028.txt`).
- Đánh giá theo quy trình đã duyệt @ min_score=0.35, top_k=5, chunking 300/40: Hit@5=1.000, MRR=1.000, Recall@5=0.970, Precision@5=0.860, answered_rate=1.000, no_answer_accuracy=0.8667 (13/15); gate PASS. Báo cáo: `06_EVIDENCE/QC_FREEZE_AND_EVAL_REPORT_20261028.md`.
- Giới hạn: G4 (MCP→Core E2E) vẫn ĐÓNG; RAG E2E NOT PASS; Blind Labeling Gate chờ adjudication của Ka trên tệp nhãn V5.

## 5. Chính sách thay đổi

Mọi sửa đổi corpus/nhãn: (1) tăng `version` trong EVAL_SET, (2) xin phê duyệt Xu ghi trong `NHAT_KY_HOP_THI_CONG.md`, (3) chạy lại `freeze_eval_set.py --out ../06_EVIDENCE/FROZEN_EVAL_SET_v<N>.json`, (4) cập nhật manifest V tiếp theo. Không sửa các phiên bản lịch sử.
