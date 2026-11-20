# DC-118-003 — BRIEF PHẢN BIỆN KIẾN TRÚC (DRAFT)

- **Work:** W118
- **Vai trò người soạn:** Vibe (đại diện chạy khảo sát, áng theo hướng dẫn chuẩn hóa
  của Vinh)
- **Trạng thái:** DRAFT — GIAO PHẢN BIỆN (Ka review độc lập; Xu tổng hợp; Vinh
  quyết)
- **Đối tượng cần phản biện:** 6 quyết định kiến trúc (AD-1..AD-6) dưới đây.

## AD-1 — Dùng GitHub-native events trước, webhook sau
- Phát biểu: Điều phối trong v1 hoàn toàn qua workflow GitHub events (`issues`,
  `issue_comment`, `pull_request`, `push`) + labels một mục đích. Không có
  webhook server ROOM-HOP trong v1.
- Lý do: giảm bề mặt xác thực HMAC/replay/idempotency cần trả lời trước khi có
  test thật; GitHub Actions sẵn có identity + secrets scoped.
- Trade-off: ROOM-HOP không nghe event realtime, chỉ xem trung gian qua evidence
  file. Khó mở rộng cross-repo sau này.

## AD-2 — Tái dùng schema evidence Work 70
- Phát biểu: mỗi run CI ghi một evidence row theo schema EVIDENCE_REGISTER.json
  (W70) tại work tương ứng, một nguồn sự thật là evidence JSON.
- Trade-off: schema W70 thiết kế cho evidence tổng quát, có field dư; cần thêm
  mapping run_id/SHA/exit_code nếu field chưa có — kiểm tra trước khi chốt.

## AD-3 — Failure path có capped retry
- Phát biểu: khi CI FAIL, không auto-thử lại máy móc: chặn ở cap tối đa 2 lần retry, sau đó mark issue `w118-blocked` + assign actor; chống
  vòng lặp bằng cờ "[skip-loop]" trong commit của bot + limit 2 mutation/run
  con.
- Tiền tiêu: count-tracked bằng evidence row, không bằng memory bot.

## AD-4 — Review/nghiệm thu qua PR gate
- Phát biểu: merge chỉ sau review độc lập + CI PASS; không auto-merge; squash
  merge tạo evidence entry duy nhất dễ đối soát.

## AD-5 — Evidence ghi qua commit riêng của bot
- Phát biểu: sau mỗi run, workflow commit evidence row (file JSON) vào nhánh
  evidence-``work/…`` bằng GITHUB_TOKEN có scope giới hạn; GITHUB_TOKEN push
  không trigger workflow (đã chạy lâu) do đó an toàn khỏi vòng lặp CI.
- Mở: chính sách lịch retry chi tiết (schedule) cần Ka thẩm định thêm.

## AD-6 — Conventions vẫn giả lập cho docs-only trên main
- Phát biểu: hồ sơ W118 trước G3 vẫn commit thẳng main (docs-only); flow PR
  bắt buộc chỉ key các path code/mutation sau khi pilot.

## Câu hỏi cần trả lời khi phản biện
1. AD-1: có cần giữ webhook ROOM-HOP như mục tiêu v2 rõ ràng không?
2. AD-2: schema W70 có field đủ cho run-id/SHA/exit-code không, hay cần
   extension doc riêng?
3. AD-3: cap 2 restart có đúng là "giới hạn có người" Vinh muốn với không?
4. AD-5: nhánh evidence có cần branch protection riêng (ai được push bot)?
5. Conventions (QC-118-002) có cần thêm phần conflict-resolution khi nhánh
   package trùng Work đã tồn tại trên main không?
