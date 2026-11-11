# BẢNG GIAO TASK — CLA (CTO, chủ trì W1111) → CO (Coder)

- Ngày lập: 2026-11-09 (UTC+7)
- Người giao: Cla (AI-03, CTO / Code-Debug Lead). Runtime identity trên MCP 8030: NOT VERIFIED — không tự đặt ID.
- Căn cứ giao việc: Anh Vinh (Chairman/CTO HQTT AI) giao Cla chủ trì Work 1111, chỉ đạo Co thực hiện; mọi trao đổi qua nhật ký Work.
- Căn cứ kỹ thuật: Cla đọc trực tiếp W1111 qua MCP 8030 ngày 2026-11-09 (nhật ký, baseline, runbook, DOC-010, patch ứng viên, test ứng viên, AI_WORKING_RULES). Chưa truy cập GitHub/PC; chưa chạy test.
- Mã task dùng tiền tố C (C01..C08) để không trùng T01..T06 trên AI_TASK_BOARD của GitHub. Liên hệ: C02/C03 ↔ T03; C07 ↔ T02; C06 ↔ T04.

## 1. Quy tắc bắt buộc cho Co (áp dụng mọi task)

1. Báo cáo CHỈ qua nhật ký canonical: `ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/00_ROOT/NHAT_KY_THI_CONG.md`. Mỗi entry có: giờ UTC+7, mã task, phương pháp/lệnh, phạm vi, bằng chứng (SHA, run ID, readback), trạng thái, giới hạn.
2. LUÔN dùng đường dẫn đầy đủ có tiền tố `ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/`. Ba file lẻ ở cấp ngoài (xem C01) là hậu quả của việc bỏ tiền tố.
3. Sửa lỗi = đưa TOÀN BỘ source đã sửa vào Work (Sandbox) kèm test; không chỉ diff/đề xuất. Diff đi kèm phải sinh từ `git diff` thật (có số dòng hunk), không viết tay.
4. Chỉ ghi DONE/PASS khi có bằng chứng (run ID + SHA + artifact hoặc readback). Thiếu điều kiện thì ghi BLOCKED theo quy định điều 6: vấn đề, lần thử, bottleneck, phương án, điều kiện còn thiếu.
5. Không đụng `main`, không merge, không thao tác PC, không gọi `/execute`, không sửa Work khác. Thay đổi source chỉ trên nhánh `work/w1111-core-execution-authority-v1-2` hoặc nhánh con của nó, qua draft PR.
6. Một tài liệu một vị trí (điều 9). Không xóa file nào; chỉ đánh LEGACY_NOTICE khi Cla duyệt.
7. Không tự duyệt thay Anh Vinh hoặc thay Cla. Khi xong task, ghi "READY FOR CLA REVIEW".

## 2. Bảng task của Co

| Mã | Ưu tiên | Việc phải làm | Đầu vào | Sản phẩm bàn giao (path trong Work) | Tiêu chí nghiệm thu (Cla kiểm) | Phụ thuộc |
|---|---|---|---|---|---|---|
| C01 | P0 | **Gom nhật ký rời về canonical.** Ba file lẻ cấp ngoài: `00_ROOT/NHAT_KY_THI_CONG.md` (1,752 B, entry PC process identity + hash W13), `02_EXTENSION/TECHNICAL_BASELINE_AND_OPEN_BLOCKERS.md` (1,281 B) và `02_EXTENSION/AUTO_E2E_REMEDIATION_GATE_AND_PC_HANDOFF_20261108.md` (1,281 B, cùng nội dung "UPDATE AFTER APPROVED IMPLEMENTATION"). Append nguyên văn vào file canonical cùng tên, kèm dòng ghi nguồn. Thêm addendum có ngày vào baseline và runbook để sửa các câu đã cũ (Core authority/Host auth/contract "chờ quyết định" nay đã có implementation trên PR #48). KHÔNG viết lại lịch sử. Sau đó đặt `LEGACY_NOTICE` vào 3 file lẻ trỏ về file canonical; chưa xóa. | 3 file lẻ + 3 file canonical | Entry nhật ký C01; 3 file canonical đã cập nhật; 3 file lẻ có LEGACY_NOTICE | Readback: đoạn nối khớp từng byte với bản gốc; baseline/runbook có addendum nêu đúng hiện trạng; không còn câu nào mâu thuẫn nhật ký mà không có chú thích | Không |
| C02 | P0 | **Sửa lỗi aggregate PASS, giao full source.** (a) Lấy `execution_host/host.py` thật từ `main`, `work/28-mcp-tooling-platform` và nhánh PR #48; xác định lỗi nested test có còn tồn tại ở nhánh PR #48 không. (b) Sửa với điều kiện bảo vệ: chỉ propagate khi `run_test` thực sự chạy và `test` có mặt; `run_test=False` thì status giữ nguyên. Ánh xạ test TIMEOUT/BLOCKED/FAILED sang overall đúng. (c) Viết lại test: thêm ca `run_test=False` (PASS giữ PASS), test con TIMEOUT, test con BLOCKED, primary FAILED + test PASS; xác minh mọi key giả định (`evidence_ref`, `stdout_ref`, `blocker`) với source thật; bỏ fixture `authorized=True` nếu nhánh PR #48 đã từ chối trường này. (d) Chạy bằng GitHub Actions trên đúng SHA. | host.py của 3 nhánh; `04_CODE/HOST_AGGREGATE_TEST_STATUS_CANDIDATE.patch`; `05_TEST/test_host_aggregate_status_candidate.py` | `04_CODE/execution_host/host.py` (FULL, đã sửa); `05_TEST/test_host_aggregate_status.py` (FULL); `04_CODE/HOST_AGGREGATE_FIX.diff` sinh từ `git diff`; entry nhật ký kèm run ID, SHA, kết quả | Test chạy thật trên CI, có ca xanh cho `run_test=False`; diff `git apply --check` được; không regression 33 test hiện có; bản candidate cũ được đánh SUPERSEDED | Khuyến nghị làm sau C01 |
| C03 | P0 | **Đối chiếu bốn dòng Execution Host.** Lập bảng blob SHA theo từng file (`server.py`, `host.py`, `security.py`, `w12_adapter.py`, `wee_bridge.py`) cho 4 nguồn: `main`, `work/28-mcp-tooling-platform`, W13 Sandbox, nhánh PR #48. Ghi MATCH/DRIFT/MISSING; nêu đề xuất bản canonical và kế hoạch hội tụ. Chỉ đọc. | GitHub + Sandbox W13 | `03_ARCHITECTURE/EXECUTION_HOST_LINES_RECONCILIATION_20261109.md` | Đủ 4 nguồn × 5 file có SHA; mỗi DRIFT có mô tả khác biệt chính; có đề xuất canonical kèm lý do | Không |
| C04 | P0 | **Dự thảo hồ sơ phê duyệt V1.2 để Anh Vinh xác nhận.** Trích nguyên văn câu chỉ đạo đã được hiểu là approval, nêu cách diễn giải, phạm vi DR-1..DR-4 và gate 1–5, kèm các điều KHÔNG được suy ra. Trạng thái ghi `INTERPRETED — PENDING EXPLICIT CONFIRMATION`. Không tự đổi sang APPROVED. | Nhật ký ("APPROVAL ACKNOWLEDGEMENT"), PROPOSED_CORE_EXECUTION_AUTHORITY_CONTRACT_V1.md (W28) | `02_EXTENSION/APPROVAL_RECORD_CORE_EXEC_AUTHORITY_V1_2_DRAFT.md` | Có chỗ cho Anh Vinh ghi rõ từng DR đồng ý/không đồng ý; Cla trình lại cho Anh Vinh | Không |
| C05 | P1 | **Cập nhật sổ phiên bản DOC-010 và đồng bộ nhật ký lên GitHub.** Anchor mới: commit mới nhất của `main`, head nhánh `work/w1111-core-execution-authority-v1-2` (44d8f62f…), PR #48, blob SHA các file W1111. Đồng bộ phần nhật ký Sandbox từ byte 12,928 trở đi sang DOC-003 (docs-only, theo DOC-003 sync contract). Ghi parity chỉ trong phạm vi đã so sánh. | DOC-010 hiện tại; DOC-003 | DOC-010 có addendum mới; DOC-003 GitHub khớp Sandbox; entry nhật ký | Readback hai phía khớp; không mở rộng claim parity ra PC | C01 |
| C06 | P1 | **Gói tự rà PR #48 cho review độc lập.** Liệt kê test âm đã có và còn thiếu cho: giả mạo `work_id`/`authorized`, grant hết hạn, grant tái sử dụng (replay), token lọt vào log/evidence, path traversal/symlink/reparse, lệch `source_sha256` giữa lúc cấp grant và lúc chạy, lỗi ghi Core record (hạ cấp BLOCKED), dọn tiến trình con, giới hạn 30 giây. Chỉ nêu lỗ hổng, không tự kết luận an toàn. | Nhánh PR #48, CI run 42454767666 | `03_ARCHITECTURE/PR48_SELF_REVIEW_PACKAGE_20261109.md` | Mỗi hạng mục có: test hiện có (tên) / thiếu / rủi ro; Cla dùng làm đầu vào review độc lập (T04) | C02, C03 |
| C07 | P1 | **Gói PC handoff chỉ-đọc cho Anh Vinh.** Lệnh PowerShell in đủ giá trị (dùng `Format-List`, không bị cắt): CommandLine đầy đủ, working directory của PID, SHA256 đầy đủ của 4 file, đường dẫn module qua `importlib.util.find_spec` (không import để tránh chạy code), nhánh/HEAD/trạng thái working tree tại `D:\ROOM-HOP-CLEAN\room-meeting-ai`, và chỉ cho biết biến môi trường bí mật có tồn tại hay không (không in giá trị). Kèm khuyến nghị về rủi ro host cũ (allow_processes=true, `/execute` không auth): giữ nguyên hay tạm dừng — để Anh Vinh quyết, không khởi động/dừng/sửa. | Nhật ký PC attestation | `06_EVIDENCE/PC_READONLY_ATTESTATION_PACK_20261109.md` | Mọi lệnh chỉ đọc; có bảng đối chiếu kỳ vọng (build_hash, PID, hash) để điền kết quả | Không |
| C08 | P2 | **Phân loại inventory và cây trùng.** (a) Manifest phân loại 4,127 entry của W09 theo nhãn: source / dependency cache (`.venv`, `site-packages`) / `__pycache__` / artifact / evidence. (b) So sha256 các cặp thư mục trùng của W102 (04_CODE↔05_BUILD/04_CODE, 05_TEST↔05_BUILD/05_TEST, 06_EVIDENCE↔EVIDENCE/LEGACY_EVIDENCE_ARCHIVE, 07_RELEASE↔05_BUILD/07_RELEASE). Chỉ đọc; không xóa, không di chuyển. | Sandbox W09, W102 | `01_DISCOVER/INVENTORY_CLASSIFICATION_W09_W102_20261109.md` | Mỗi cặp có kết luận MATCH/DRIFT; đề xuất bản canonical; không thay đổi Work gốc | Không |

Thứ tự thực hiện đề xuất: C01 → (C02 ‖ C03 ‖ C04 ‖ C07) → C05 → C06 → C08.

## 3. Việc của Cla (chủ trì)

| Mã | Việc | Điều kiện |
|---|---|---|
| K1 | Trình Anh Vinh xác nhận phê duyệt V1.2 theo từng DR (dựa trên C04) | Có hồ sơ C04 |
| K2 | Review độc lập từng sản phẩm của Co và ghi quyết định ACCEPT / REWORK / BLOCKED vào nhật ký | Co ghi "READY FOR CLA REVIEW" |
| K3 | Review độc lập PR #48 (T04) dựa trên C06; không merge khi chưa có K1 và K2 cho C02/C03 | C02, C03, C06 |
| K4 | Giữ gate: không nâng bất kỳ trạng thái runtime/E2E nào lên PASS khi thiếu evidence live trên PC | Liên tục |
| K5 | Điều phối owner cho T05 (Windows lane) và T06 (identity/authorization) với An/Vi | Cần Anh Vinh chỉ định owner |

## 4. Việc cần Anh Vinh (chỉ khi tới lượt)

1. Xác nhận phê duyệt V1.2 theo từng DR (K1).
2. Chạy gói PC chỉ-đọc C07 và dán kết quả; quyết định giữ hay tạm dừng host cũ PID 16484.
3. Chỉ định owner cho Windows lane (T05).

## 5. Trạng thái hiện tại (2026-11-09)

- W1111 = ACTIVE; DISCOVER = PARTIAL.
- PR #48 (draft): CI 33 passed — chỉ là bằng chứng CI/in-process, không phải live PC/cloud.
- Live Core→Host→Sandbox→GitHub E2E = NOT PASS. Parity PC = NOT VERIFIED. Aggregate PASS fix = CANDIDATE, chưa đạt (xem C02).
