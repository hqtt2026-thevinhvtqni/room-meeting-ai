# BIÊN BẢN THỐNG NHẤT — KHÔNG THI CÔNG QUA CHAT
## Work 28 — MCP Tooling Platform / MCP :8020

- **Thời gian ghi nhận:** 2026-10-16 20:07 ICT (UTC+07:00)
- **Người ra quyết định:** Vinh — Work Owner / Decision Authority
- **Điều phối, kiểm tra và nghiệm thu:** Xu — Planner / Chief Strategy Architect (CSA)
- **Thi công chính:** Co — Builder, Work 28
- **Rà soát độc lập:** Ka — Chief Strategy Architect (CSA), reviewer độc lập
- **Phạm vi:** Chỉ Work 28; không mở rộng sang Work khác trừ khi có phụ thuộc kỹ thuật bắt buộc được chứng minh.

## 1. Quyết định thống nhất

1. **Không tiếp tục thi công, sửa mã, kiểm thử, hoặc điều phối từng bước trong cửa sổ chat.** Mọi công việc triển khai phải diễn ra trong môi trường Work 28 đã được chỉ định, trên repository `hqtt2026-thevinhvtqni/room-meeting-ai`, branch `work/28-mcp-tooling-platform`.
2. Mọi giao việc, quyết định kỹ thuật, thay đổi mã, kết quả kiểm thử, blocker, bằng chứng và bàn giao phải được ghi thành **biên bản và nhật ký thi công ngay trong Work 28**. Mỗi mục bắt buộc ghi **tên/mã người thực hiện, chức danh/vai trò, thời gian có múi giờ ICT, hành động, kết quả, đường dẫn bằng chứng và trạng thái DONE/PASS/DECISION/BLOCKED**.
3. Xu phải **đọc và truy vết hiện trạng trong Work 28 trước**, sau đó thực hiện các cập nhật/triển khai có thể làm qua repository Work 28; kiểm tra lại bằng cách đọc lại tài liệu hoặc mã sau khi ghi. Không tuyên bố đã triển khai runtime nếu mới chỉ ghi tài liệu.
4. Co tiếp tục thi công phần builder/tool integration và E2E trong phạm vi được phép. Ka rà soát độc lập theo bằng chứng lưu tại Work 28. Các thành viên khác chỉ nhận phần việc khi được giao rõ trong biên bản của Work 28.
5. Chat không được dùng làm nơi lưu trạng thái thi công hoặc thay thế hồ sơ Work. Hồ sơ chuẩn, lịch sử thay đổi và bằng chứng có thể kiểm tra phải nằm trong Work 28.

## 2. Hiện trạng đã đọc lại trước khi ghi biên bản

- **DONE — repository evidence:** Xu đọc lại `work/28/MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/NHAT_KY_THI_CONG.md` và báo cáo Co lúc khoảng 13:27 ICT trên branch `work/28-mcp-tooling-platform`.
- **REPORTED, chưa tái kiểm tra độc lập:** Co báo HTTPS MCP :8020 trả HTTP 200, `tools/list` có phản hồi và thao tác Sandbox write/readback khớp probe.
- **BLOCKED / NOT PROVEN:** Full E2E chưa có bằng chứng được nghiệm thu; `runtime_run_tests` và `github_read_file` không có trong tool list theo báo cáo Co. File live evidence được Co nêu chưa đọc được qua GitHub connector tại đường dẫn/ref đã thử; điều này không chứng minh file không tồn tại trong Sandbox.
- **Trạng thái:** Work 28 = ACTIVE / NOT RELEASED. Không merge vào `main`; release NO-GO cho tới khi đủ bằng chứng kiểm thử, bảo mật, tích hợp Core/runtime và E2E thực tế.

## 3. Lệnh thi công tiếp theo

### Xu — Planner / CSA, điều phối và nghiệm thu
- Đọc, truy vết và đối chiếu code, test, nhật ký, issue và bằng chứng hiện có trong branch Work 28.
- Triển khai các sửa đổi tài liệu/mã thuộc Work 28 mà có đủ căn cứ và quyền; mỗi thay đổi phải kèm test hoặc ghi rõ BLOCKED.
- Tạo/readback biên bản và nhật ký sau từng mốc có ý nghĩa; không thay thế việc thi công bằng kế hoạch.
- Không tuyên bố PASS nếu không có log/kết quả thực thi thật.

### Co — Builder, Work 28
- Lưu snapshot nguyên văn của MCP `tools/list` và bằng chứng write/readback vào đúng thư mục evidence chuẩn của Work 28; ghi endpoint đã làm sạch thông tin bí mật, thời gian, request/response và hash khi có.
- Hoàn tất adapter/tool integration qua kiến trúc được phê duyệt; chỉ sử dụng MCP/Core/runtime hiện hữu, Core giữ quyền xác thực và phân quyền.
- Khi có runner được phê duyệt, chạy test và E2E thật; ghi command, exit code, stdout/stderr, test inventory, revision, log/hash và readback.
- Nếu runner/capability thiếu, ghi chính xác schema/capability/lỗi nguyên văn; không giả lập PASS.

### Ka — CSA, reviewer độc lập
- Rà soát độc lập thay đổi, test và bằng chứng trong Work 28; ghi kết luận PASS/FAIL/BLOCKED và lý do trong hồ sơ Work 28.
- Không coi báo cáo miệng hoặc việc tạo file là bằng chứng runtime PASS.

## 4. Ranh giới an toàn và kiến trúc

- Giữ luồng: AI → MCP :8020 → Core :8000 → capability/runtime được cấp quyền.
- Không tạo Core/MCP/runtime trùng lặp; không bypass Core; không thêm shell/Python tùy ý; không tự tin caller-provided identity.
- Không sửa Work 13, không sửa PC hoặc khởi động lại dịch vụ đang chạy, không thay đổi live MCP registry nếu chưa có quyền và quy trình được phê duyệt.
- Không merge/release cho tới khi đạt đủ cổng kiểm thử và bảo mật.

## 5. Tiêu chí hoàn tất và bàn giao

- **DONE:** Artifact/code được tạo và đọc lại trong branch Work 28.
- **PASS:** Lệnh/test thực sự chạy và có kết quả kiểm chứng được, gồm exit code/log.
- **BLOCKED:** Thiếu capability/quyền/runner được chỉ rõ bằng bằng chứng; không dùng DONE để ngụ ý PASS.
- **HANDOFF:** Có biên bản, nhật ký, revision/commit, bằng chứng kiểm thử, blocker còn lại và kết luận của Xu/Ka.

**Kết luận tại thời điểm ghi:** Biên bản đã được tạo trong branch Work 28; việc lưu hồ sơ không đồng nghĩa E2E đã PASS. Work 28 tiếp tục ACTIVE / NOT RELEASED.
