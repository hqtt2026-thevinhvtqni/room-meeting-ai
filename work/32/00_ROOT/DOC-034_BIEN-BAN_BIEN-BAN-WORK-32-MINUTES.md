# BIÊN BẢN CHUẨN HÓA WORK 32 / WORK 32 GOVERNANCE NORMALIZATION MINUTES
- **STT / Document ID:** DOC-034
- **Priority:** P1
- **Read order:** 11
- **Depends on:** DOC-001; DOC-002; DOC-003; DOC-033
- **Status:** ACTIVE — INSTRUCTION RECORDED; MIGRATION IN PROGRESS
- **Version / Updated:** 1.0 / 2026-11-04

## Biên bản
- **Chủ sở hữu / thẩm quyền cuối cùng:** Vinh.
- **Điều phối:** Xu — CEO / Lead Architect.
- **Thực hiện chuẩn hóa hồ sơ:** Ka — CSA / Work 32 delegated execution owner.
- **Thời điểm:** 2026-11-04, Asia/Ho_Chi_Minh.
- **Chỉ đạo:** Vinh yêu cầu lấy Work 70 làm chuẩn để chuẩn hóa Work 32 phục vụ công tác triển khai chung.

### Nội dung thực hiện
1. Đọc các chuẩn Work 70 DOC-001, DOC-002, DOC-003, DOC-004, DOC-005, DOC-006, DOC-033, DOC-038, DOC-039, DOC-040, DOC-042, DOC-043 và Document Register DOC-055.
2. Thiết lập Work 32 canonical governance tree và các hồ sơ chuẩn; áp dụng DOC-ID, priority, read order, dependency và naming bilingual Vietnamese-first.
3. Giữ nguyên cây tài liệu/kỹ thuật cũ `CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/`; chưa di chuyển, đổi tên hoặc xóa file.
4. Phân định Sandbox governance records và GitHub source code branch; không tự đồng bộ hai chiều.
5. Giữ nguyên các trạng thái PASS/BLOCKED/NOT RUN/NOT VERIFIED theo bằng chứng; không nâng trạng thái nghiệm thu hoặc phát hành.

### Kết luận
Đây là đợt chuẩn hóa quản trị và hồ sơ ban đầu, không phải nghiệm thu sản phẩm. Các tài liệu cũ sẽ được phân loại và ánh xạ; di trú vật lý, thay đổi branch, GitHub docs sync, kiến trúc tích hợp Dashboard/Workspace và release cần các bước/gate riêng.


---

## Biên bản W32-20261114-08 — HỌP PHẢN BIỆN DOC-125 / RESOURCE ISOLATION

**Chủ trì và điều phối:** Xu / AI-01. **Chủ sở hữu cuối cùng:** Vinh. **Thành phần phản biện:** Ka / AI-02 (CSA), Cla / AI-03 (CTO). **Phạm vi:** DOC-125, READ-ONLY review và quyết định hướng thiết kế.

### 1. Kết quả phản biện

- Ka kết luận implementation resource isolation hiện tại REJECT; hướng Windows Job Object chỉ APPROVE WITH CONDITIONS.
- Cla kết luận IMPLEMENTABLE WITH CONDITIONS; Cla nêu rõ không có quyền đọc GitHub source trong phiên review và đã dựa vào DOC-035/prior evidence, do đó Xu không xem đây là source audit độc lập.
- Xu đã truy xuất trực tiếp các blob trên nhánh remediation. Protected GrantedExecutionHost gọi run_bounded(); Windows process creation hiện dùng Popen + CREATE_NEW_PROCESS_GROUP, không phải CREATE_SUSPENDED. Đường generic ExecutionHost trong host.py cũng dùng Popen thông thường. Không đường nào chứng minh Job Object assignment trước khi user code chạy.
- Hai reviewer thống nhất: phải thiết lập và xác minh OS resource boundary trước khi resume workload; mọi lỗi phải DENY/BLOCKED; không fallback sang Popen thường.

### 2. Quyết định của Xu

**APPROVE WITH CONDITIONS** đối với hướng kiến trúc Windows Job Object + ResourceBackend abstraction + unsupported-platform DENY. Đây chỉ là phê duyệt hướng thiết kế, không phải phê duyệt triển khai.

Core vẫn là nguồn duy nhất cấp grant và resource policy. Host áp dụng policy được Core ràng buộc và hard ceiling nội bộ; không nhận quota từ caller. Windows workload phải được tạo suspended hoặc được đưa vào Job ngay tại thời điểm tạo; cấu hình/query quota, assign và verify membership, final Core validation, sau đó mới resume. Job Object phải quản lý descendants, active process count, memory, CPU rate và kill-on-close. Job Object không thay thế restricted identity và filesystem/network/credential isolation.

Linux/unsupported OS tiếp tục DENY protected execution cho đến khi có backend kernel-enforced riêng được kiểm chứng. Không Docker.

### 3. Điều kiện chưa được khép

D1 creation-time Job assignment và orphan handling; D2 Core resource policy schema; D3 Host cancellation/descendant lifecycle; D4 incomplete/torn Run Record recovery; D5 JSONL hiện tại so với yêu cầu SQLite trong DOC-123; D6 quota values từ workload measurements. Các mục này phải được giải quyết trước implementation.

### 4. Quyền được cấp và không được cấp

Xu được phép chuẩn bị bounded isolated Windows API proof-of-concept/test specification để làm rõ D1/D3; không tích hợp vào sản phẩm, không chạy protected workload. Chưa cho phép sửa source/test sản phẩm, đổi Core schema, branch/PR mutation, PC runner dispatch, thay đổi service/port/config, protected execution, main integration, deployment hoặc release. Sau khi D1–D6 khép, Xu ban hành implementation authorization riêng. Vinh giữ quyền nghiệm thu và phát hành cuối cùng.

**Kết luận:** Hướng thiết kế APPROVED WITH CONDITIONS; implementation NOT AUTHORIZED; protected execution DENIED; Work32 ACTIVE — NOT ACCEPTED — NOT RELEASED.
