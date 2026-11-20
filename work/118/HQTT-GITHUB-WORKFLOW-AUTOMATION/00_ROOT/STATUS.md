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


## Cập nhật kiểm thử độc lập — 2026-11-20 (Entry 021)
- **T-02 ACK runtime:** PASS — tài khoản GitHub `thevinhqtni-1911` comment `ACKED-test-65`; W118 Run #8 success, job `ack-verification` success, bot ghi đúng actor. [Run #8](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44740499758).
- **T-02 anti-spoof/authorization:** NOT VERIFIED — pilot v1 chỉ kiểm tra prefix `ACKED-`; role mapping còn MANUAL, chưa chứng minh actor không được ủy quyền bị từ chối.
- **T-03:** NOT VERIFIED — cần login ↔ role mapping được phê duyệt.
- **T-04:** NOT VERIFIED — chờ một CI FAIL tự nhiên sau khi W118 listener hoạt động.
- **T-05:** BLOCKED — chưa có ACK riêng để mở rộng self-listener.
- **Freeze:** main chỉ cập nhật hồ sơ kiểm thử; không sửa workflow/permission, không merge PR #66; B-118-010 chưa được áp dụng.
- **Nhật ký chuẩn:** Entry 021 trong `EVIDENCE/NHAT-KY-THI-CONG.md`.


## Quyết định chủ sở hữu — Identity mapping (Entry 022)
- Vinh xác nhận hai GitHub login `hqtt2026-thevinhvtqni` và `thevinhqtni-1911` đều thuộc mình.
- Mapping được duyệt: cả hai login → cùng HQTT principal **Vinh / HQTT Owner**; vẫn giữ nguyên login riêng trong audit log.
- T-03 mapping: **APPROVED / DOCUMENTED**.
- T-03 runtime authorization: **NOT VERIFIED** — workflow pilot chưa thực thi allowlist/role policy và chưa có negative test từ actor ngoài mapping.
- T-02 Run #8 vẫn chỉ chứng minh event/actor propagation từ account thứ hai; không chứng minh unauthorized denial.
- Không sửa workflow/permission; PR #66 OPEN; B-118-010 vẫn khóa chờ lệnh chính xác; T-05 vẫn BLOCKED.
- Nhật ký chuẩn: Entry 022 trong `EVIDENCE/NHAT-KY-THI-CONG.md`.
