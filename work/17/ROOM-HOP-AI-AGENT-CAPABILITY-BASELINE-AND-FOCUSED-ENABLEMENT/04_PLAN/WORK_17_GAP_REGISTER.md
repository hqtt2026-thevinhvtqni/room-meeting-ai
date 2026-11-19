# GAP REGISTER — WORK 17

- Work ID: 17 · Owner: Vinh · Điều phối: Xu / AI-01
- Ngày cập nhật: 2026-11-19 · Trạng thái: ACTIVE — READ/TRACE ONLY
- Nguồn phát hiện: WORK_17_AUDIT_JOURNAL.md Entry 001–005; quét GitHub main kỳ 2026-11-19.

## Định mức ưu tiên
- P0: chặn trực tiếp khả năng chạy được luồng AI end-to-end; phải xử lý trước G3.
- P1: gây sai lệch bằng chứng/kết luận nếu không xử lý trước G4–G6.
- P2: chất lượng, hiệu suất, dọn dẹp; xử lý sau G6.

## Danh mục gap

| ID | Gap | Mảng năng lực | Ưu tiên | Evidence hiện tại | Tiêu chí nghiệm thu | Trạng thái |
|----|-----|---------------|---------|-------------------|---------------------|------------|
| GAP-01 | Dispatch/ACK tới AI member chưa được chứng minh; tool surface 8030 không có private-session dispatch; source adapters được kiểm tra là browser/execution/Git/CI/Meeting artifact, không phải AI provider transport | Dispatch & acknowledgment | P0 | Journal Entries 002, 016–018; WORK_17_GAP01_DISPATCH_ACK_SOURCE_RECONCILIATION.md §8–9 | Một dispatch thật có trace ID khớp provider delivery receipt + ACK accountable, đạt cấp E3 | OPEN |
| GAP-02 | Token/cost telemetry NOT_AVAILABLE cho toàn bộ AI member | Observability & cost | P0 | Journal Entry 002 | Bảng usage (member, model, session) từ nguồn metering, cấp E2 | OPEN |
| GAP-03 | Chuỗi execution/browser chưa E2E verified | Execution | P0 | Journal Entry 002 (tham chiếu DOC-018) | Một tác vụ browser thật: session record + artifact hash, cấp E3 | OPEN |
| GAP-04 | Core owner/API/auth/persistence chưa xác minh; Core execution-grant routes chưa được chứng minh mount vào entrypoint; authoritative Work persistence/owner chưa xác minh | Core authority & orchestration | P0 | Journal Entry 002 + WORK_17_CORE_AUTHORITY_SOURCE_TRACE.md (2026-11-19) | Trace request thật qua Core, grant fail-closed, owner được chỉ định, Work persistence/audit và Host online validation; E3 | OPEN |
| GAP-05 | Xung đột mapping AI-06/AI-07/AI-08 trong DOC-010 | Identity & authorization | P1 | Journal Entry 002 | Quyết định của Vinh + cập nhật DOC-010 v1.2, ghi Decision Log | OPEN |
| GAP-06 | Chênh lệch danh mục: Sandbox 71 Work vs DOC-018 snapshot 56 Work (+15 chưa phân loại) | Portfolio reconciliation | P1 | Journal Entry 002 | Mỗi Work chênh lệch được phân loại: mới hợp lệ / legacy / trùng / anomaly | OPEN |
| GAP-07 | GitHub main chỉ mirror 17 workfolder; 54 Work còn lại không có bản canonical trên GitHub | Evidence & governance | P1 | WORK_17_PORTFOLIO_RECONCILIATION.md kỳ 2026-11-19 | MVSR tăng từ 17/71 lên ≥ 70/71 hoặc ghi rõ ngoại lệ có lý do | OPEN |
| GAP-08 | Journal self-reference commit SHA (Entry 004/005) | Evidence & governance | P2 | Journal Entry 005 | Chuyển sang SYNC_RECORD.md; dừng ghi SHA HEAD vào thân journal | OPEN |
| GAP-09 | Roster DOC-010 v1.1: runtime identity phần lớn NOT VERIFIED; participation khai báo chưa chứng minh | Identity & session | P1 | Journal Entry 002 | Mỗi member được gắn trạng thái theo bộ tiêu chí evidence (E0–E4), không theo khai báo | OPEN |
| GAP-11 | Execution Host nhận WorkContext từ caller và dựa vào boolean `authorized`; chưa thấy service authentication/Core grant online validation trong HTTP Host path; command surface rộng hơn pytest-only contract | Security & execution authority | P0 | WORK_17_CORE_AUTHORITY_SOURCE_TRACE.md; source blobs execution_host/server.py, models.py, security.py, host.py, wee_bridge.py | Host ingress xác thực service identity; Core grant bind Work/purpose/source/policy/expiry; online validate + revoke; pytest-only enforcement; negative integration tests + independent QE; E3 | OPEN |
| GAP-10 | Một số Work tham chiếu kiến trúc cũ cần kiểm soát (legacy references) | Nguồn chuẩn (canonical) | P2 | Journal Entry 002 | Danh sách tham chiếu legacy + đề xuất lỗi thời hóa theo Work 70 | OPEN |

## Quy tắc vận hành register
1. Không đóng gap nào chỉ bằng cách viết thêm tài liệu mô tả; cần bằng chứng đúng cấp.
2. Mỗi gap P0 phải có: owner được chỉ, Work phụ thuộc, mốc dự kiến trước Gate tương ứng.
3. Việc sửa Work thành phần để xử lý gap phải đi qua Gate G7 (sau quyết định của Vinh) và hội ý Work 70.
