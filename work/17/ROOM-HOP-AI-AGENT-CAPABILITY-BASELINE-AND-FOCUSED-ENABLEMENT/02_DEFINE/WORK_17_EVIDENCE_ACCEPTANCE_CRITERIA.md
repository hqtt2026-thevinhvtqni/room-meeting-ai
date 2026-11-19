# TIÊU CHÍ CHẤP NHẬN BẰNG CHỨNG — WORK 17

- Work ID: 17 · Owner: Vinh · Điều phối: Xu / AI-01
- Ngày ban hành: 2026-11-19 · Trạng thái: ACTIVE
- Mục đích: chốt trước G2/G3 câu hỏi "thế nào là bằng chứng đủ" để đánh giá năng lực không quay lại suy diễn từ tài liệu (vi phạm điều 4 Execution Plan: "Do not infer capability from a Work name, manifest, roster, source file or design diagram").

## 1. Thang phân loại bằng chứng

| Cấp | Tên | Định nghĩa | Cho phép kết luận tối đa |
|-----|-----|------------|--------------------------|
| E0 | DOC_ONLY | Chỉ văn bản, sơ đồ, manifest | DOC_ONLY |
| E1 | SOURCE | Mã nguồn / cấu hình tồn tại trong canonical repo, có commit SHA | SOURCE_EXISTS |
| E2 | RUNTIME_LOG | Log / artifact sinh ra từ lần chạy thật, có timestamp, được lưu kèm hash | RUNTIME_VERIFIED |
| E3 | E2E_TRACE | Chuỗi request → dispatch → ACK → execution → artifact → verification có log liền mạch, không đứt giữa chừng | ROOM_IN_USE |
| E4 | INDEPENDENT_REPRO | Reviewer độc lập hoặc bên thứ ba chạy lại được cùng kết quả | ROOM_IN_USE (xác nhận) |

## 2. Điều kiện tối thiểu theo mảng năng lực (G2/G3)

| Năng lực | Yêu cầu tối thiểu để đạt RUNTIME_VERIFIED |
|----------|-------------------------------------------|
| Identity & session | Log session binding từ provider thật, không phải roster khai báo |
| Dispatch & ACK | Delivery receipt + ACK có trace ID khớp với dispatch log |
| Tool/provider | Attempt log + ghi nhận timeout/retry + artifact đầu ra |
| Execution (sandbox/browser/computer) | Session record + artifact hash + teardown log |
| Token/cost telemetry | Bảng usage theo (member, model, session) từ nguồn metering, không phải ước lượng |
| Knowledge/RAG | Truy vấn thử read-only trả kết quả có citation trỏ về nguồn chuẩn |
| Coding & testing | CI run xanh + test report lưu trong 06_EVIDENCE của Work liên quan |
| Safety | Bằng chứng fail-closed: một thao tác ngoài quyền bị chặn và có log |
| Dispatch & ACK idempotency | Một dispatch bị lặp (retry) chỉ tạo một lần thực thi, có log chứng minh |

## 3. Quy tắc ghi nhận

1. Một kết luận PASS phải kết cấu đủ: Work ID liên quan, đường dẫn canonical, revision/commit SHA, phương pháp kiểm tra, và bằng chứng cấp cao nhất đạt được (E0–E4).
2. Bằng chứng cấp E2 trở lên phải lưu tệp trong 06_EVIDENCE của Work liên quan và trỏ đường dẫn tương đối.
3. Không nâng cấp trạng thái chỉ vì hai tài liệu giống nhau (duplication ≠ verification).
4. Xung đột nguồn: bản của Work được chỉ canonical owner là chuẩn; ghi CONFLICT và chờ Gate G4, không tự phân xử.
5. Roster DOC-010 (AI_TEAM_AND_TOKEN_USAGE.md) chỉ là E0: KHÔNG được dùng làm bằng chứng runtime identity.
6. Mọi thử nghiệm nâng cấp trạng thái đều là thay đổi phạm vi "READ/TRACE ONLY" hiện tại; cần quyết định của Vinh trước khi thực hiện.
