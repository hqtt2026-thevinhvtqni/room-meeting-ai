
## Entry 004 — W118-09 PILOT: triển khai w118-coordination-ci + templates
- **Thời gian:** 2026-11-20 (UTC+07)
- **Ủy quyền:** Vinh phê duyệt BUILD trong phiên ("xây đi, khi xong Xu nghiệm thu") — G3 được chấp nhận trong phiên; G2 phản biện chéo thành AFTER-pilot (Ka/Xu phản biện sau; KHÔNG coi là bỏ gate).
- **Phạm vi:** `.github/workflows/w118-coordination-ci.yml` (validate docs + diagnostic idempotent), `.github/ISSUE_TEMPLATE/work-execution.md`, `.github/PULL_REQUEST_TEMPLATE.md`, tài liệu thiết kế W118-02..08 từ Entry 003, `05_BUILD/W118-09_PILOT_COORDINATION_CI.md`.
- **An toàn:** KHÔNG branch protection, KHÔNG secrets, KHÔNG webhook, KHÔNG auto-merge; workflow chỉ contents:read + issues:write.
- **Kết quả CI:** (đang cập nhật sau push — bổ sung run URL + SHA trong Entry sau.)
