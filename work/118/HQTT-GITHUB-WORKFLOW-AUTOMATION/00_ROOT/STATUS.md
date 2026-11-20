# STATUS — WORK 118 (PRODUCT v1 PILOT)

- **Ngày:** 2026-11-20
- **Quyết định Vinh (2026-11-20):** Vibe tự quyết cấu trúc; vòng phản biện dài bỏ; Xu nghiệm thu sản phẩm.
- **Sản phẩm v1:** workflow ".github/workflows/w118-workflow-automation.yml" (W118 Workflow Automation Pilot), 3 jobs:
  1. handoff-brief: issue gắn label w118-handoff được comment hướng dẫn nhận việc.
  2. ack-verification: comment bắt đầu bằng "ACKED-" được ghi nhận bằng chứng (anti-spoof manual ở pilot v1; Xu kiểm tra mapping role khi nghiệm thu).
  3. ci-failure-diagnostics: khi CI của W300/W70 FAIL, mở hoặc cập nhật 1 issue chẩn đoán duy nhất có label w118-blocked (run URL + SHA + quy tắc retry cap 2, không retry vô hạn).
- **An toàn thiết kế:** GITHUB_TOKEN events không tự kích hoạt lại workflow (không vòng lặp); least-privilege (issues: write, contents: read); timeout 5 phút mỗi job; khớp thiết kế TD-118-005/006/007/008.
- **Chưa có trong v1:** evidence row tự động vào register W70 (chờ ACK schema v1.2), realtime ROOM-HOP, auto-merge (cấm vĩnh viễn theo TD-118-007).
- **Trạng thái:** PILOT RUNTIME VERIFIED ở mức **2/3 job** (ack-verification + handoff-brief, Entry 018: Runs #6/#7 success, 2 comment bot "handoff registered" trên Issue #65) nhưng **XU NOT ACCEPTED 2026-11-20** (hồ sơ XU-118-AC-001 — AC-R1..AC-R6). Đang chạy vòng kiểm thử độc lập theo [KT-118-009](../04_PLAN/KT-118-009_KE-HOACH-KIEM-THU-BO-SUNG.md): main giữ nguyên, PR #66 chưa merge, không sửa mã trong vòng nghiệm thu.
