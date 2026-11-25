# BIÊN BẢN CHÍNH THỨC W122
## Khởi tạo phạm vi ROOM-HOP EMAIL INTELLIGENCE

- Work: 122 — ROOM-HOP EMAIL INTELLIGENCE
- Ngày lập: 2026-11-25 (Asia/Ho_Chi_Minh, UTC+07:00)
- Người lập: Xu — AI-01
- Owner: Vinh
- Trạng thái: BASELINE / DISCOVER IN PROGRESS
- Phân loại: FACT / OWNER REQUIREMENT / PROPOSAL / UNKNOWN.

## 1. Quyết định thành lập và ranh giới
1. Thành lập W122 cho ROOM-HOP EMAIL INTELLIGENCE (AI Email Assistant / Mail Center).
2. W120 và W121 giữ nguyên toàn bộ tên, hồ sơ, trạng thái, tài liệu, mã nguồn và phạm vi. W122 không sửa, di chuyển, hợp nhất, đổi tên hoặc phụ thuộc W120/W121.
3. W122 là sản phẩm email; không phải Work CUA và không yêu cầu CUA để hoạt động.
4. Tuân thủ Work 70. Hiện tại DISCOVER/ARCHITECTURE INTAKE; chưa được phép BUILD hoặc gửi email thật.

## 2. Mục tiêu sản phẩm
- Theo dõi email đến tự động khi provider hỗ trợ push/event; polling fallback có kiểm soát.
- Kết nối nhiều mailbox từ các nhà cung cấp khác nhau.
- Phân loại email, nhận diện mức ưu tiên, yêu cầu hành động và hạn phản hồi.
- Tóm tắt nội dung/ngữ cảnh hội thoại; đề xuất hành động.
- Soạn sẵn thư trả lời để người dùng xem, sửa và duyệt.
- Gửi tự động chỉ trong phạm vi quy tắc Owner phê duyệt; ngoài chính sách phải chuyển duyệt.
- Cảnh báo trên Dashboard và email notification.
- Audit đầy đủ cho đồng bộ, phân loại, soạn, duyệt, gửi, lỗi và thu hồi quyền.

## 3. Yêu cầu chức năng
### 3.1 Mailbox & sync
Provider-neutral adapters: Gmail/Google Workspace, Outlook/Microsoft 365, IMAP. Tách mailbox identity, token, sync cursor, policy và trạng thái. Ưu tiên push/webhook, polling fallback; deduplication, idempotency, retry/backoff, dead-letter và cursor recovery. Không lưu mật khẩu email; ưu tiên OAuth 2.0/delegated authorization. Không tự đăng ký ứng dụng, consent hoặc thay đổi credential khi chưa được phép.

### 3.2 Email Intelligence
Phân loại P0 Khẩn cấp; P1 Quan trọng; P2 Cần phản hồi; P3 Thông tin; P4 Spam/nghi ngờ. Priority và security/phishing là hai trục riêng. Trích xuất sender, mailbox, subject, thời điểm, thread, tóm tắt, yêu cầu, deadline được nêu rõ và confidence. Không bịa dữ kiện, giá, thời hạn, lời hứa hoặc cam kết.

### 3.3 Draft & send
AI tạo draft; draft không đồng nghĩa sent. Mặc định yêu cầu người dùng duyệt. Auto-send chỉ bật theo mailbox, tác vụ, người nhận/đối tác và mẫu đã duyệt. Báo giá, hợp đồng, thanh toán/tài chính, pháp lý, khiếu nại/tranh chấp, dữ liệu nhạy cảm, thay đổi cam kết, thiếu dữ kiện hoặc confidence thấp luôn yêu cầu duyệt. Gửi phải kiểm tra policy tại thời điểm gửi, chống gửi trùng, xác nhận provider receipt và ghi audit.

### 3.4 Dashboard & notifications
Mail Center gồm Inbox Overview, Priority Inbox, Action Required, AI Drafts, Sent by AI, Mailbox Settings, Audit/Errors. Hiển thị mailbox, sender, subject, received time, priority, summary, requested action, sourced deadline, confidence, draft và send state. Dashboard chỉ render; không phải authority cấp quyền/gửi. Alerts qua Dashboard + email theo cấu hình.

## 4. Kiến trúc đề xuất — chưa phê duyệt
Provider Adapter Layer; Email Event & Sync Engine; Email Intelligence Engine; Notification Service; Send Control/Policy Enforcement; Core Authority & Audit; Mail Center UI. Candidate mapping cần kiểm chứng: Core :8000, Gateway :8040, Event Listener :8050, Agent Runtime :8051, Dashboard :3000. Đây không phải bằng chứng runtime/API đã tồn tại.

## 5. Phân công ban đầu
- Xu/AI-01: điều phối, kiến trúc.
- Ka/AI-02: review kiến trúc, security, authority.
- Cla/AI-03: CTO integration/code/debug sau khi duyệt kiến trúc.
- Kha/AI-04: chỉ khảo sát ban đầu Gmail/Google Workspace API, OAuth, push/watch; không BUILD sâu hoặc vận hành dài hạn.
- Go/AI-06: CFO/Cost Analyst, default QE/QA, hỗ trợ code và review độc lập theo W122. Nếu Go sửa code thì không tự review/accept chính phần đó; phải có reviewer khác.
- Vibe/Mistral: code support GitHub-only; không có numeric AI ID.
- Manus/AI-18: autonomous builder sau khi xác minh runtime identity, permission, audit. Khi đủ điều kiện giao một outcome-based assignment trọn gói.
- Qw/AI-05: HQTT reviewer, không mặc định QE/QA.
- Qc/AI-08, Co/AI-07, Vi/AI-09: đúng vai trò theo danh bạ chính thức.
Không đổi roster, không cấp ID mới.

## 6. Security
OAuth 2.0, least privilege, tách read/draft/send scopes nếu provider hỗ trợ; token mã hóa trong vault; không ghi secret vào prompt/log/GitHub. Per-mailbox identity/policy/revoke/audit. Email body, links, headers, attachments là dữ liệu không tin cậy; chống prompt injection. Không chạy attachment/macro/executable/script. Email đáng ngờ bị quarantine/escalate. Không gửi nếu policy/approval không hợp lệ.

## 7. Giai đoạn và cổng
DISCOVER → ARCHITECT → BUILD (chỉ sau phê duyệt) → VERIFY (synthetic/test tenants) → OPERATE (read-only → draft-only → limited auto-send → mở rộng sau nghiệm thu). Hiện tại BUILD NOT AUTHORIZED; REAL SEND NOT AUTHORIZED.

## 8. UNKNOWN cần làm rõ
Provider ưu tiên/test tenant; contract thực tế Core/Gateway/Event/Runtime; khả năng tái sử dụng W52; OAuth registration/scopes/quotas; data retention/storage/deletion; notification mailbox/loop prevention; approval UX; per-mailbox auto-send policy.

## 9. Nguyên tắc
UNKNOWN nếu chưa có bằng chứng runtime; không dùng mock để tuyên bố live; không claim PASS nếu chưa có test tái lập/read-back; mọi hoạt động phải ghi nhật ký; tuyệt đối không sửa W120/W121.
