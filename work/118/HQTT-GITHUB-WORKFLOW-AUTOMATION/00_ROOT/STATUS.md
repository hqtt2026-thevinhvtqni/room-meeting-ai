# STATUS — WORK 118 (PRODUCT v1 PILOT)

- **Ngày:** 2026-11-20
- **Quyết định Vinh (2026-11-20):** Vibe tự quyết cấu trúc; vòng phản biện dài bỏ; Xu nghiệm thu sản phẩm.
- **Sản phẩm v1:** workflow ".github/workflows/w118-workflow-automation.yml" (W118 Workflow Automation Pilot), 3 jobs:
  1. handoff-brief: issue gắn label w118-handoff được comment hướng dẫn nhận việc.
  2. ack-verification: comment bắt đầu bằng "ACKED-" được ghi nhận bằng chứng (anti-spoof manual ở pilot v1; Xu kiểm tra mapping role khi nghiệm thu).
  3. ci-failure-diagnostics: khi CI của W300/W70 FAIL, mở hoặc cập nhật 1 issue chẩn đoán duy nhất có label w118-blocked (run URL + SHA + quy tắc retry cap 2, không retry vô hạn).
- **An toàn thiết kế:** GITHUB_TOKEN events không tự kích hoạt lại workflow (không vòng lặp); least-privilege (issues: write, contents: read); timeout 5 phút mỗi job; khớp thiết kế TD-118-005/006/007/008.
- **Chưa có trong v1:** evidence row tự động vào register W70 (chờ ACK schema v1.2), realtime ROOM-HOP, auto-merge (cấm vĩnh viễn theo TD-118-007).
- **Trạng thái:** DEPLOYED PILOT — run #2 (runtime test qua comment ACKED) đang QUEUED tại thời điểm ghi nhật ký Entry 007; PILOT NOT PASS cho tới khi run #2 xanh và bot comment bằng chứng có trên Issue #65.
