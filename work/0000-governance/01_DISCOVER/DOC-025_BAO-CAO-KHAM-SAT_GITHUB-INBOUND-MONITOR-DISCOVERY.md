# DOC-025 — BÁO CÁO KHẢO SÁT GIÁM SÁT SỰ KIỆN GITHUB ĐẦU VÀO
# GITHUB INBOUND MONITOR DISCOVERY REPORT

- Document ID: DOC-025
- Priority: P0
- Status: ACTIVE — DISCOVERY COMPLETE / DESIGN PROPOSAL ONLY
- Version: 1.0
- Updated: 2026-11-03
- Owner: Xu / AI-01
- Authority: Vinh
- Work: 0000 — HQTT Company Governance
- Related: DOC-001, DOC-002, DOC-003, DOC-004, DOC-008; Work 70 DOC-057, DOC-063, DOC-064, DOC-066, DOC-069, DOC-071, DOC-072, DOC-084

## 1. Mục tiêu

Khảo sát cách tiếp nhận thay đổi từ GitHub về nhật ký chính của Work 0000, bảo đảm mỗi commit/PR được kiểm tra trước khi ghi nhận. Không tạo nhật ký thứ hai.

## 2. Quy tắc nguồn sự thật

- Sandbox Work0000 DOC-003 là nhật ký thi công chính.
- GitHub DOC-003 là bản sao ánh xạ; không cho các AI khác ghi trực tiếp vào bản sao này như một nhật ký độc lập.
- Commit, PR, review và CI là bằng chứng đầu vào, không tự động chứng minh AI identity, ACK, DONE, PASS hoặc Gate PASS.
- Xu kiểm tra nguồn, nhiệm vụ, nhánh, file thay đổi, test evidence và receipt trước khi ghi vào Sandbox DOC-003.
- Sau khi Sandbox read-back thành công, đồng bộ toàn bộ DOC-003 sang GitHub và fetch lại để so sánh.

## 3. Hiện trạng đã quan sát

1. GitHub canonical repository: hqtt2026-thevinhvtqni/room-meeting-ai.
2. Work0000 canonical branch: work/0000-governance-baseline.
3. GitHub repository metadata xác nhận repository tồn tại, default branch main; connector có quyền đọc/ghi theo phiên hiện tại. Quyền connector không đồng nghĩa quyền Work Entry.
4. Có thể truy xuất PR/commit và file nội dung qua GitHub connector trong phiên xử lý. Đây là thao tác do Xu chủ động thực hiện, không phải webhook/poller nền.
5. Work 70 DOC-057: chính sách Work Entry ACTIVE, enforcement kỹ thuật REQUIRED; thiếu enforcement không được tuyên bố đã bảo vệ thao tác.
6. Work 70 DOC-069: quyền của Xu trong Work 70 chỉ là tài liệu/read-only trace giới hạn; không cho phép sửa Core/API/database/auth/runtime hoặc cấp quyền cho AI khác.
7. Work 70 DOC-071: Core owner NOT IDENTIFIED; Work/WP/Assignment/Evidence API và authoritative persistence NOT FOUND IN INSPECTED SCOPE / NOT VERIFIED; HTTP app factory chưa được chứng minh chạy trong runtime.
8. Work 70 DOC-072/DOC-084: Hybrid Dispatch và authorization vẫn là thiết kế; implementation chưa được phê duyệt; G0/G1/G4 chưa sẵn sàng.

## 4. Các phương án

### Option A — Webhook
GitHub event → HTTPS receiver → signature verification → event deduplication → fetch evidence → assignment/scope validation → verified queue → append Sandbox DOC-003 → read-back → GitHub mirror.

Điều kiện: phải có endpoint HTTPS được sở hữu và vận hành, xác minh chữ ký webhook, secret management, chống replay, lưu trạng thái bền vững, xử lý retry, giám sát và kiểm thử bảo mật.

### Option B — Scheduled poller
Worker định kỳ đọc commit/PR/review/CI từ nhánh canonical, duy trì cursor/checkpoint, lọc event mới, rồi dùng chung pipeline kiểm chứng và ghi nhật ký.

Điều kiện: runtime worker có owner, lịch chạy được xác nhận, persistence/checkpoint, API quota handling, pagination, retry và giám sát.

### Option C — Pull-on-check
Xu chủ động truy vấn GitHub khi xử lý nhiệm vụ, kiểm chứng bằng chứng, ghi Sandbox DOC-003 và mirror GitHub.

Đây là phương án hiện có bằng chứng hoạt động trong phiên công cụ. Không gọi là realtime hoặc tự động.

## 5. Khuyến nghị

- Duy trì Option C làm chế độ vận hành hiện tại.
- Chọn Option A làm kiến trúc đích nếu sau này có HTTPS ingress và owner phù hợp.
- Option B là phương án dự phòng khi webhook chưa khả thi.
- Không xây worker riêng, database riêng hoặc endpoint giả định trong Work 70.
- Không dùng automation nhắc việc như bằng chứng của webhook/poller tự động.

## 6. Kiểm soát bắt buộc

- Allowlist repository, branch, event type và path scope.
- Mỗi event có ID duy nhất và chống xử lý trùng.
- Receipt tối thiểu: Work ID, Assignment ID, actor, branch, commit SHA/PR URL, changed paths, test evidence, blocker và trạng thái.
- Actor GitHub không tự chứng minh AI runtime; identity assurance phải được ghi riêng.
- CI pending/missing = PENDING/UNKNOWN, không phải PASS.
- Event sai repo/branch/scope hoặc thiếu receipt phải quarantine/NEEDS_CLARIFICATION.
- Journal append chỉ sau khi xác minh; mirror chỉ sau Sandbox read-back.
- Mirror lỗi phải ghi GITHUB_MIRROR_PENDING; không xóa hoặc ghi đè dữ liệu GitHub khác.
- Không tự merge, deploy, cấp quyền hoặc đổi Gate.

## 7. Blockers và hướng khắc phục

| Blocker | Bằng chứng | Hướng khắc phục | Owner cần xác định |
|---|---|---|---|
| Chưa có webhook ingress được xác minh | Chưa tìm thấy endpoint/owner trong hồ sơ hiện tại | Xác định service owner, runtime, HTTPS endpoint và secret management; sau đó threat-model/test | Core/Platform owner |
| Chưa có poller worker được xác minh | Chưa có process, scheduler hoặc checkpoint evidence | Xác định nơi chạy, persistence, lịch, retry và monitoring | Platform owner |
| Chưa có Work-scoped authorization/persistence | DOC-071 | Xác định Core owner và source contract thật; không tự tạo shadow store | Core owner |
| Work70 implementation gate chưa mở | DOC-057/069/072/084 | Tạo Work Package, hoàn tất Work Entry cho từng participant và xin authorization theo DOC-057 | Xu điều phối; Vinh quyết định |
| Hai path DOC-003 trên GitHub bị lệch | E0000-025 | Đối chiếu register và lịch sử; lập change có kiểm soát, không tự xóa path | Xu / Vinh |

## 8. Trạng thái

- Discovery: COMPLETE trong phạm vi nguồn đã kiểm tra.
- Current operation: PULL-ON-CHECK / MANUAL TRIGGER.
- Target architecture: WEBHOOK-FIRST; POLLER FALLBACK.
- Implementation: NOT AUTHORIZED.
- Tests: NOT RUN.
- Release: NOT RELEASED.

## 9. Điều kiện chuyển bước

Chỉ lập Work Package triển khai sau khi xác định được owner/runtime ingress hoặc poller, contract persistence/audit, quyền tối thiểu, Work Entry evidence cho từng participant và authorization có hiệu lực. Mọi thay đổi kỹ thuật phải có test allow/deny, duplicate/replay, scope violation, retry, journal read-back, mirror parity và independent QE.

---
**Prepared by:** Xu / AI-01
**Decision authority:** Vinh
