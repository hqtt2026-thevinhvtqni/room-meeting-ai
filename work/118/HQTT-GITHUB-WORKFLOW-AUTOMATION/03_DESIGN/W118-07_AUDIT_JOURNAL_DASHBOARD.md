# W118-07 — THIẾT KẾ AUDIT JOURNAL & DASHBOARD (DATA CONTRACT)

- **Work:** W118 (Issue #65) · **Ngày:** 2026-11-20 (UTC+07) · **Trạng thái:** DRAFT chờ phản biện

## 1. Nguồn dữ liệu (single source of truth)

- \`work/118/HQTT-GITHUB-WORKFLOW-AUTOMATION/EVIDENCE/NHAT-KY-THI-CONG.md\` — nhật ký thi công (Entry NNN).
- \`EVIDENCE_REGISTER.json\` chuẩn Work 70 — dùng chung schema toàn repo.
- GitHub Issues labels = trạng thái realtime; KHÔNG ghi trùng trạng thái ở hai nơi.

## 2. Data contract cho Dashboard

\`\`\`json
{
  "work": "118",
  "issue": "https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/65",
  "wp": {"id": "W118-01", "state": "DONE|IN_PROGRESS|BLOCKED|NOT_STARTED", "evidence": ["EV-W118-YYMMDD-001"]},
  "state_machine": "label trạng thái hiện tại",
  "ci": {"run_url": "...", "sha": "...", "result": "PASS|FAIL|intentional-fail"},
  "provenance": {"actor": "vibe|xu|ka|vinh|ci-bot", "timestamp_utc7": "..."},
  "limitations": ["..."]
}
\`\`\`

- Dashboard chỉ **đọc và tổng hợp** — không tự sản sinh trạng thái (tránh hai nguồn sự thật).

## 3. Provenance & audit

- Mọi mutation của AI phải để lại dấu vết: Issue comment + evidence entry + commit body có actor (W118-02).
- Mutation của con người phải được phê chuẩn trước (G3/G5) — không ghi mutation chưa có căn cứ.
- Evidence entry gồm \`purpose, producer, UTC+07, branch/commit, kết quả, hạn chế\` — khớp quy ước Work 103 (DOC-057) và schema v1.1 Work 70.
