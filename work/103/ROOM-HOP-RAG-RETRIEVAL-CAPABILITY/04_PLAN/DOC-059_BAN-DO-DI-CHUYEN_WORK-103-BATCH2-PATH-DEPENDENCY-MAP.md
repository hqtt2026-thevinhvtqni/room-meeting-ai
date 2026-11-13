# BẢN ĐỒ DỊ CHUYỂN VÀ PHỤ THUỘC WORK 103 — BATCH 2 PREP (REPORT-ONLY)
- **STT / Document ID:** DOC-059
- **Priority:** P1
- **Read order:** 7
- **Depends on:** DOC-001; DOC-055; DOC-056
- **Status:** ACTIVE — MAPPING ONLY (NO MOVES PERFORMED)
- **Version / Updated:** 1.0 / 2026-11-09
- **Authority:** Vinh
- **Owner:** Xu / AI-01
- **Producer:** Vibe (2026-11-09, under Vinh's standing full-build authorization; instruction "xây tiếp, không chờ, không đợi" recorded in DOC-035 LOG-W103-20261109-007)

> Mục đích: chuẩn bị exit evidence cho Batch 2 (DOC-056) — "full old→new path map; no broken imports/CI". Tài liệu này CHỈ ánh xạ và trace phụ thuộc; KHÔNG file nào được di chuyển/đổi tên trong commit này. Mọi di chuyển phải thực hiện trong một commit duy nhất kèm cập nhật CI đồng bộ.

## 1. Phụ thuộc CI (.github/workflows/work-103-rag-ci.yml)

| # | Consumer | Tham chiếu | Loại |
|---|---|---|---|
| C1 | Trigger | paths: work/103/ROOM-HOP-RAG-RETRIEVAL-CAPABILITY/** + workflow file | glob path |
| C2 | py_compile | 8 file: 04_CODE/{rag_retrieval,rag_eval,rag_evidence_support,rag_evidence_support_corpus_eval}.py, 05_TEST/test_{rag_retrieval,rag_eval,rag_evidence_support,rag_evidence_support_corpus_eval}.py | đường dẫn tuyệt đối trong repo |
| C3 | unittest discover | working-directory 04_CODE; -s ../05_TEST | path TƯƠNG ĐỐI: 04_CODE và 05_TEST phải là thư mục anh em |
| C4 | Gate B | python rag_evidence_support.py (default decision set = parents[1]/05_TEST/EVIDENCE_SUPPORT_DECISION_SET_V1.json) | relative parents[1] |
| C5 | Corpus diagnostic | --specs ../05_TEST/EVIDENCE_SUPPORT_FACT_SPECS_V1.json và V2.json; fixture default ../05_TEST/EVAL_SET_CORPUS_V4_V3.json | relative ../05_TEST |
| C6 | Baseline gate | python rag_eval.py (EVAL_SET_PATH = parents[1]/05_TEST/EVAL_SET.json) | relative parents[1] |
| C7 | Grounded-abstention | python ../05_TEST/grounded_abstention_eval.py | tee ../06_EVIDENCE/grounded_abstention_diagnostic.json | **CI GHI FILE vào 06_EVIDENCE** |
| C8 | Independent gate | python rag_eval.py --eval-set ../05_TEST/EVAL_SET_CORPUS_V4_V3.json --diagnostics | relative ../05_TEST |
| C9 | Experiment + artifact | python rag_experiment.py > rag_experiment_results.json (ghi vào 04_CODE); upload path 04_CODE/rag_experiment_results.json, if-no-files-found: error | write target + artifact path |

## 2. Phụ thuộc nội bộ code (imports / sys.path / data paths)

| File | Phụ thuộc |
|---|---|
| 04_CODE/rag_retrieval.py | Thuần module, không đọc file repo nào; chỉ load file qua load_approved_text_files() do caller cung cấp (chấp nhận .txt/.md trong approved roots) |
| 04_CODE/rag_eval.py | sys.path.insert thư mục自身; import rag_retrieval; EVAL_SET_PATH = parents[1]/05_TEST/EVAL_SET.json |
| 04_CODE/rag_evidence_support.py | KHÔNG import rag_retrieval (độc lập theo contract §4); default decision set parents[1]/05_TEST/EVIDENCE_SUPPORT_DECISION_SET_V1.json |
| 04_CODE/rag_evidence_support_corpus_eval.py | sys.path CODE_DIR; import rag_retrieval + rag_evidence_support; default fixture parents[1]/05_TEST/EVAL_SET_CORPUS_V4_V3.json; default specs parents[1]/05_TEST/EVIDENCE_SUPPORT_FACT_SPECS_V1.json |
| 04_CODE/rag_experiment.py | import rag_retrieval + rag_eval.load_eval_set (default EVAL_SET.json); tạm ghi đè rr.K1/rr.B rồi khôi phục; ghi rag_experiment_results.json tại HERE (04_CODE) |
| 05_TEST/grounded_abstention_eval.py | sys.path ROOT/04_CODE; import rag_eval + rag_retrieval; EVAL_PATH = ROOT/05_TEST/EVAL_SET_CORPUS_V4_V3.json; không tự ghi file (CI tee sang 06_EVIDENCE) |

## 3. Ràng buộc di chuyển bắt buộc (Batch 2 rules — suy ra từ §1/§2)

1. 04_CODE và 05_TEST PHẢI giữ quan hệ anh em (mọi tham chiếu ../05_TEST và parents[1]/05_TEST), hoặc toàn bộ C3–C6, C8 và các hằng số path trong code phải cập nhật trong CÙNG một commit.
2. 06_EVIDENCE là CI write target (C7): không thể di chuyển mà không sửa đồng bộ bước tee trong workflow.
3. rag_experiment_results.json là write target trong 04_CODE + artifact upload path (C9): di chuyển 04_CODE đòi sửa đồng bộ upload path.
4. CI trigger glob (C1) phải cập nhật nếu cây work/103 đổi cấu trúc.
5. sys.path.insert giả định các module nằm cùng thư mục (C2/C3): không tách rời rag_retrieval.py khỏi các consumer.
6. unittest discover pattern test_*.py: tên file test phải giữ tiền tố test_.

## 4. Ánh xạ old → new đề xuất (chưa thực hiện)

| Đường dẫn hiện tại | Đích chuẩn theo DOC-001 §3/§4 | Điều kiện an toàn |
|---|---|---|
| 04_CODE/ | 05_BUILD/ (declared canonical source path) | Đồng bộ C1..C9 trong 1 commit; giữ requirements.txt |
| 05_TEST/ | 06_VERIFY/ (declared canonical test path) | Đồng bộ C2..C6, C8 + sys.path trong code |
| 06_EVIDENCE/ | EVIDENCE/ | Đồng bộ C7 (tee) + audit link nội bộ |
| 03_ARCHITECTURE/ | 03_ARCHITECT/ | Audit link từ specs/evidence (cited source_id strings) |
| 00_CORPUS/ | 01_DISCOVER/ + vị trí corpus chuẩn | Phân loại original vs fixture TRƯỚC; source_id trong fixtures trỏ "00_CORPUS/*.md" — đổi cấu trúc corpus = đổi dữ liệu fixture (CẤM trong Batch 2, thuộc phạm vi adjudication) |
| 02_EXTENSION/ | 01_DISCOVER/ hoặc 03_ARCHITECT/ | Chỉ là tài liệu tham khảo; audit link |
| 4 pointer legacy ở gốc | đã là pointer | Giữ nguyên |

**Cảnh báo dữ liệu (quan trọng):** các fixture/eval-set nhúng NỘI DUNG document và source_id dạng "00_CORPUS/...", "03_ARCHITECTURE/..." (ví dụ EVAL_SET_CORPUS_V4_V3.json, fact specs V1/V2, DOCUMENTED_ABSENCE trong grounded_abstention_eval.py). Đổi vị trí vật lý của corpus/architecture KHÔNG đổi source_id trong fixture (đó là dữ liệu đã freeze/adjudication-scoped), nhưng mọi ánh xạ thư mục phải ghi rõ: source_id là định danh logic, không phải đường dẫn vật lý.

## 5. Trạng thái
- Batch 2 chuyển IN_PROGRESS (bản đồ + trace hoàn tất; DI CHUYỂN CHƯA thực hiện). Exit evidence còn thiếu: mapping validation sau khi di chuyển + CI pass tại head mới (riêng independent gate luôn FAIL đã biết — cần disposition như Batch 1).
- Áp dụng chỉ dẫn Vinh 2026-11-09: xây tiếp không chờ xác nhận; các mục chưa xác nhận được ghi nợ (DEBT-ES-09/10, DOC-035 LOG-W103-20261109-007).
