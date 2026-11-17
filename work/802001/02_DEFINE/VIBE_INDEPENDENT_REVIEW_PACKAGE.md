# HỒ SƠ BÀN GIAO PHẢN BIỆN ĐỘC LẬP — VIBE
## Work 802001 / Independent Review Handoff to Vibe

- Work ID: 802001
- Handoff ID: W802001-REV-VIBE-001
- Recipient: Vibe (Mistral Vibe — GitHub-based coding/review agent)
- Sender/coordinator: Xu / AI-01
- Date: 2026-11-17
- Target branch: main
- Status: READY FOR VIBE REVIEW — HANDOFF RECORDED; VIBE ACKNOWLEDGEMENT NOT YET VERIFIED
- Canonical subject under review: `02_DEFINE/AGENT_SUPERVISION_BUSINESS_RULES.md` (W802001-DEF-001, v0.1)
- Governing standard: Work 70

## 1. Mục tiêu bàn giao
Vibe được đề nghị thực hiện phản biện độc lập đối với bộ quy tắc nghiệp vụ theo dõi, nhắc nhở, hướng dẫn, điều chỉnh và kiểm tra lại Agent trong suốt assignment/Work. Sau phản biện, Vibe được phép chỉnh sửa trực tiếp các hồ sơ tài liệu liên quan trên GitHub `main` trong đúng phạm vi được giao, ghi bằng chứng và đồng bộ các chỉ mục/nhật ký tương ứng.

Đây là bàn giao công việc qua Git, không phải bằng chứng Vibe đã nhận việc. Chỉ xác nhận ACK khi Vibe để lại dấu vết rõ ràng trên Git.

## 2. Nguồn bắt buộc phải đọc
Đọc trực tiếp từ GitHub `main`, không dựa vào bản sao trong chat:
1. `work/802001/02_DEFINE/AGENT_SUPERVISION_BUSINESS_RULES.md` — tài liệu cần phản biện.
2. `work/802001/01_DISCOVER/AGENT_SUPERVISION_CASE_INVENTORY.md` — 10 tình huống lịch sử và phân loại độ tin cậy.
3. `work/802001/03_ARCHITECT/AGENT_OPERATIONAL_GATE_ARCHITECTURE.md` — kiến trúc nghiệp vụ hiện tại.
4. `work/802001/00_ROOT/BIEN_BAN.md` — phạm vi và quyết định đã ghi.
5. `work/802001/04_PLAN/IMPLEMENTATION_ROADMAP.md` — WP/trạng thái/gate.
6. Work 70 canonical standards, đặc biệt DOC-001, DOC-004, DOC-005, DOC-033, DOC-057 và DOC-096 (đọc bản hiện hành trên repo, nếu truy cập được).

Nếu nguồn không đọc được, ghi rõ BLOCKED và đường dẫn/điều kiện còn thiếu; không tự dựng nội dung thay nguồn.

## 3. Phạm vi phản biện
Phản biện tối thiểu các chủ đề:
- Taxonomy: phân loại finding có đủ, không chồng lấn, có thể áp dụng ngoài trường hợp kỹ thuật của W802001 không?
- Severity S0–S3: ranh giới, ví dụ, tác động, confidence và cách xử lý có hợp lý không?
- Assignment lifecycle: intake, briefing, acknowledgement, checkpoint, observation, guidance, correction, recheck, close/block/escalate có thiếu trạng thái hoặc chuyển trạng thái sai không?
- Reminder: event-driven cadence có chống spam, xử lý múi giờ, thời gian không hoạt động, Agent đã phản hồi và tình huống BLOCKED tốt không?
- Authority: quyền của Vinh, Xu, Work Owner, Agent, Reviewer/QE, System Owner có chồng lấn hoặc tạo quyền ngầm không?
- Evidence/journal: bằng chứng tối thiểu có thể truy nguyên, readback, kiểm tra độc lập và chống self-certification không?
- Governance: tương thích Work 70; không thay thế lifecycle/Gates W70; ranh giới DOC-057/DOC-096; không tạo policy mới trái thẩm quyền.
- Failure modes: multi-agent/multi-work findings, false positives, missing prerequisites, stale docs, system failures, reviewer conflict of interest, repeat findings, appeal/dispute, privacy/secret handling.
- Khả năng triển khai: quy tắc nào cần DEFINE thêm, quy tắc nào chỉ nên để ARCHITECT/PLAN; không thiết kế code khi nghiệp vụ chưa ổn định.

## 4. Quyền thực hiện trên Git
Vibe được phép:
1. Đọc, đối chiếu và phản biện các hồ sơ được liệt kê.
2. Chỉnh sửa trực tiếp tài liệu DEFINE v0.1 thành bản kế tiếp nếu có căn cứ; giữ lịch sử thay đổi và nêu lý do.
3. Cập nhật hồ sơ bàn giao này với review verdict, findings, evidence, đề xuất và danh sách file đã sửa.
4. Cập nhật `00_ROOT/WORK_CONTENT_INDEX.md`, `00_ROOT/DOCUMENT_REGISTER.md`, `04_PLAN/IMPLEMENTATION_ROADMAP.md` và `00_ROOT/NHAT_KY_THI_CONG.md` để phản ánh đúng kết quả.
5. Commit trực tiếp trên `main` theo quy ước hiện hành của Work; mỗi commit có message mô tả đúng nội dung. Không tạo branch mới trừ khi Vinh cho phép rõ ràng.

Vibe không được:
- Mở hoặc triển khai BUILD; sửa source code, runtime, API, MCP, credential, permission hoặc workflow tự động.
- Thay đổi mục tiêu/scope Work, Work 70 lifecycle, Gate W70, decision đã chốt hoặc policy đã được phê duyệt.
- Tự tuyên bố policy được Vinh phê duyệt, tự đánh dấu G4 PASS, hoặc biến tài liệu dự thảo thành policy binding.
- Xóa/di chuyển/đổi tên hồ sơ legacy; sửa/xóa evidence gốc; làm sai lệch journal.
- Ghi PASS khi chỉ đọc code/tài liệu mà chưa chạy phép thử cần thiết.
- Tự nhận danh tính/ủy quyền ngoài dấu vết Git và quyền truy cập thực tế.

## 5. Cách thực hiện bắt buộc
Theo thứ tự:
1. READ: xác nhận HEAD `main`, đọc toàn bộ nguồn bắt buộc và ghi commit/path đã xem.
2. TRACE: truy nguyên từng quy tắc trong DEFINE về case/source/decision tương ứng; đánh dấu rule chưa có evidence hoặc chỉ là inference.
3. REVIEW: ghi verdict cho từng chủ đề; phân biệt Critical/Major/Minor/Observation; nêu căn cứ cụ thể.
4. DECIDE: đề xuất KEEP / CHANGE / REMOVE / DEFER cho từng finding. Không tự phê duyệt policy.
5. EDIT: nếu đủ căn cứ, chỉnh sửa tài liệu DEFINE và các index/plan/journal liên quan. Nếu chưa đủ, giữ nguyên và ghi BLOCKED/open questions.
6. VERIFY: đọc lại tất cả file đã sửa từ GitHub; xác nhận diff, consistency, links/path, version, status và journal.
7. HANDOFF: ghi commit SHA, file list, kết quả readback, unresolved findings, next action. Không tuyên bố Xu/Vinh/Agent khác đã duyệt nếu không có bằng chứng.

## 6. Định dạng kết quả bắt buộc
Cập nhật phần “VIBE REVIEW RESULT” ở cuối chính hồ sơ này với:
- Reviewer identity: Vibe (chỉ ghi theo dấu vết phiên/commit, không tuyên bố xác thực danh tính ngoài Git).
- Review date/time (+07:00).
- Starting main HEAD và final commit SHA.
- Verdict: ACCEPT WITH CHANGES / ACCEPT WITH COMMENTS / REVISE REQUIRED / BLOCKED.
- Bảng findings: ID, severity, topic, source/evidence, issue, recommendation, disposition.
- Traceability: mỗi thay đổi gắn với case/source/decision hoặc ghi rõ là đề xuất mới.
- Files changed + lý do.
- Verification: file readback, commit, consistency, test (nếu có) và giới hạn.
- Open questions cần Xu/Vinh quyết định.
- Xác nhận rõ policy vẫn NOT APPROVED và BUILD vẫn NOT AUTHORIZED.

## 7. Acceptance criteria cho lượt review
- Không bỏ qua bất kỳ chủ đề phản biện tối thiểu nào ở mục 3.
- Mọi finding có nguồn hoặc ghi rõ là inference/open question.
- Không gán mọi vấn đề cho Agent; phân biệt lỗi Agent, lỗi hệ thống, thiếu điều kiện, tài liệu cũ/xung đột và lỗi điều phối/reviewer.
- Không đưa SLA/tần suất nhắc chung nếu chưa có dữ liệu/ủy quyền.
- Không tạo quyền ngầm; các hành động nhạy cảm vẫn cần Vinh/ủy quyền rõ ràng.
- Tài liệu DEFINE, index, register, roadmap và journal nhất quán sau chỉnh sửa.
- GitHub readback khớp nội dung đã commit.
- Không mở BUILD và không tuyên bố policy approval.

## 8. Trạng thái bàn giao
- Handoff package: CREATED ON GITHUB MAIN.
- Vibe acknowledgement: PENDING — chưa có bằng chứng Vibe đã mở/nhận hồ sơ.
- Independent review: NOT STARTED / PENDING VIBE.
- Policy approval: NOT APPROVED.
- BUILD: NOT AUTHORIZED.

## 9. VIBE REVIEW RESULT — VIBE ONLY TO COMPLETE
> Vibe: cập nhật phần này sau khi thực sự thực hiện review. Không để Xu điền thay verdict của reviewer.

- Reviewer:
- Review date/time:
- Starting main HEAD:
- Final commit SHA:
- Verdict:
- Findings:
- Traceability:
- Files changed:
- Verification/readback:
- Open questions:
- Policy approval: NOT APPROVED (unless separately approved by Vinh with explicit record).
- BUILD: NOT AUTHORIZED.

---
**Handoff note:** This file is the single canonical review handoff/result record for Vibe in Work 802001. Do not create parallel review reports unless Vinh explicitly authorizes them.
