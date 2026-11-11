# CTO REVIEW & ĐỀ XUẤT XỬ LÝ — WORK 1111

- Người thực hiện: Cla (AI-03, CTO / Code-Debug Lead) qua phiên claude.ai chat. Runtime identity trên MCP 8030: NOT VERIFIED (chưa tra registry agents/*.yaml; không tự đặt ID).
- Thời điểm: 2026-11-08 09:44 (UTC+7)
- Phạm vi: đọc W1111 (NHAT_KY_THI_CONG, TECHNICAL_INVENTORY, TECHNICAL_BASELINE_AND_OPEN_BLOCKERS, AI_WORKING_RULES, KE_HOACH), W0000 DOC-010, W102 (listing + RUN_MANIFEST Vi 20261025). Chỉ đọc; không sửa Work nào ngoài W1111.
- Trạng thái review: PARTIAL.

## 1. Đánh giá baseline của Xu
- Đồng ý các kết luận và trạng thái: DISCOVER = PARTIAL; W32 gate = FAIL; parity GitHub/Sandbox/PC = NOT VERIFIED; không có PASS không bằng chứng.
- Điểm mạnh: phân biệt exact branch/SHA, không bypass guard, không xóa/clean khi PC dirty.
- Điểm yếu: 5 blocker chưa có owner, tiêu chí đóng, thứ tự ưu tiên. Các phát hiện W32/W70/W09/W100 là thông tin đọc từ báo cáo (gián tiếp), chưa đối chiếu độc lập.

## 2. Kiểm chứng độc lập của Cla (có bằng chứng)
1. B-1111-03 cần chỉnh lại cách diễn đạt. MCP 8030 không có process/pytest execution là đúng, nhưng KHÔNG đồng nghĩa chưa có evidence thực thi. W102 có run Vi 20261025T135722Z-58be2c5213db (RUN_MANIFEST.json): pytest 151 tests, 0 failures/errors/skipped, exit_code=0, source hash before = after (15 file), verdict LOCAL_REFERENCE_PASS. Giới hạn trong chính manifest: claim_scope=LOCAL_REFERENCE_ONLY, pc_runtime_verified=false, production_pass=false; chạy ở runtime ngoài, kết quả giao vào Sandbox qua MCP8030 delivery receipt. => Đã có mẫu thực thi ngoài + giao evidence; thiếu là đối chiếu với exact SHA GitHub và chạy trên PC/Core live.
2. W102 có cây trùng lặp: 04_CODE ↔ 05_BUILD/04_CODE; 05_TEST ↔ 05_BUILD/05_TEST; 06_EVIDENCE ↔ EVIDENCE/LEGACY_EVIDENCE_ARCHIVE; 07_ENVIRONMENT ↔ 05_BUILD/05_TEST/environment; 07_RELEASE ↔ 05_BUILD/07_RELEASE; có __pycache__ trong 04_CODE/05_TEST. Trái AI_WORKING_RULES điều 9 (một tài liệu một vị trí). Rủi ro: test/review nhầm bản. Cla CHƯA so hash giữa các bản trùng nên chưa kết luận chúng giống hay khác.
3. W1111 có hai entry cấp ngoài 00_ROOT và 01_DISCOVER: sandbox_read trả FileNotFoundError và listing không có file con => nhiều khả năng là thư mục rỗng legacy; chưa đủ chứng cứ để xóa. W0000 đã có mẫu LEGACY_SCAFFOLD_NOTICE.md để áp dụng.
4. Định danh Cla: roster W0000 DOC-010 ghi AI-03 / Cla / CTO, runtime identity NOT VERIFIED. Cần tra registry thực trước khi gọi API cần identity.

## 3. Phân loại ưu tiên và đề xuất

| Ưu tiên | Blocker | Đề xuất | Tiêu chí đóng | Đề xuất owner |
|---|---|---|---|---|
| P0 | B-1111-01 drift + B-1111-04 parity | Lập REVISION LEDGER chỉ đọc: repo, branch, SHA, path, blob SHA/sha256 cho GitHub / Sandbox / PC. Bắt đầu với 6 cặp W32 + 15 file W102 (đã có sha256 trong manifest làm mốc). Chỉ đồng bộ qua change control, không overwrite mù, không reset/clean/stash trên PC | Mỗi file trong phạm vi có 3 giá trị hash cạnh nhau và trạng thái MATCH/DRIFT/MISSING | Xu (mapping) + Cla (review); PC side cần người có quyền PC |
| P1 | B-1111-03 execution | Chuẩn hóa EXECUTION EVIDENCE CONTRACT dựa trên RUN_MANIFEST của Vi: argv, cwd, exit_code, version runtime, hash source trước/sau, junit, claim_scope, pc_runtime_verified. Quy tắc nâng cấp: chỉ coi PASS cho một revision khi hash source trong manifest khớp exact SHA GitHub | Có contract + 1 run mẫu khớp SHA | Cla (contract) + An/Vi (chạy) |
| P1 | B-1111-02 Windows lane | Không đụng release gate. Thu evidence runner readiness và service provenance cho đúng Run #133 / SHA 554ebe31...; SKIPPED không phải PASS | Windows E2E chạy thật trên đúng SHA, hoặc BLOCKED có lý do và điều kiện thiếu | An / Vi |
| P2 | B-1111-05 inventory noise | Sinh manifest phân loại theo mẫu đường dẫn (.venv, site-packages, __pycache__, artifacts, source, evidence). Không xóa/di chuyển; đề xuất quy tắc loại trừ qua change control | Bảng phân loại 4,127 entries, mỗi entry có nhãn | Xu / La (PMO) |
| P2 | Cây trùng W102, thư mục rỗng W1111 | So hash bản trùng, chọn bản canonical, đánh LEGACY_NOTICE cho bản còn lại; chưa xóa | Mỗi tài liệu có một vị trí chuẩn được ghi rõ | Chủ W102 + Xu |

## 4. Nguyên tắc rủi ro
- Không dùng kết quả của SHA/branch này làm bằng chứng cho SHA/branch khác.
- PC working tree dirty: chỉ đọc.
- Mọi PASS cần: lệnh/phương pháp, thời gian, phạm vi, output thật, hash.

## 5. Phối hợp với Xu
- Xu đang làm: bản đồ source-of-truth và đường chạy pytest. Phát hiện mục 2.1 giúp bước thứ hai không phải khảo sát từ đầu.
- Cla nhận: review Revision Ledger khi có; soạn Execution Evidence Contract; code/debug khi blocker đã khoanh vùng tới file cụ thể (khi sửa lỗi sẽ chuyển toàn bộ source đã sửa vào Work trong Sandbox).
- Cần Anh Vinh quyết định: quyền truy cập PC cho P0, và owner cho Windows lane.

## 6. Giới hạn của review này
Chưa đọc trực tiếp báo cáo W32, W70 DOC-035, W100, W24, W11, W12; chưa truy vấn GitHub HEAD; chưa so hash giữa Sandbox/GitHub/PC; chưa chạy test. Các kết luận về những phần này lấy lại từ nhật ký Xu và được đánh dấu gián tiếp.
