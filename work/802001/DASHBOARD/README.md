# WORK 802001 DASHBOARD — READ MODEL CONTRACT

Dashboard là read-only projection từ nguồn canonical theo chuẩn W70: Manifest, WP/Roadmap, assignment, checkpoint, reminder, finding, correction, recheck, escalation, Evidence Register và Nhật ký thi công.

## Required views
- Work lifecycle và Gate theo W70 (không tự tính PASS).
- Agent/assignment roster: Agent, role, owner, scope, current assignment, checkpoint, last activity.
- Work progress: ON_TRACK, AT_RISK, BLOCKED, DEVIATION_FOUND, NO_RESPONSE.
- Reminder & guidance: reminder due/sent, correction notice, recipient, deadline, acknowledgement.
- Correction tracking: finding open, correction submitted, recheck pending, verified closed, escalated.
- Journal/evidence: source path, timestamp, freshness, evidence status, reviewer.
- Blockers, overdue checkpoints và next actions.

## Integrity
Mọi chỉ số phải truy về record canonical, source version và as_of. Dashboard không được tự suy diễn trạng thái từ % tiến độ, lời Agent hoặc file tồn tại; không có quyền ghi trạng thái authoritative.

## Current truth
DASHBOARD CONTRACT ONLY. Chưa có tích hợp dữ liệu runtime, chưa chứng minh tự động theo dõi/nhắc nhở Agent và chưa có browser E2E evidence.
