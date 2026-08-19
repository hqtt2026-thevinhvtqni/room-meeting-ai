# ROOM HOP

## Agent onboarding

Agent mới vào ROOM HOP phải đọc theo thứ tự:

1. `AGENTS.md` — Constitution / Governance Contract
2. `context/PROJECT_STATE.md` — Verified Project State / Truth
3. `context/XU_CORE.md` — Xu Identity / Authority
4. `context/XU_SESSION.md` — Current Working State
5. `context/XU_MEMORY.md` — Long-term Memory
6. `meetings/{latest}/` — Historical Evidence, chỉ tham khảo; không dùng làm project state
7. `ROOM-2026-001-BASELINE-FROZEN-v0.2.1.md` — Regression baseline hiện hành
8. `SECRETARY_LARGE_FILE_IMPORT_SIGNOFF.md` — Secretary + Large File Import evidence

### Context rules

- `AGENTS.md` là Constitution.
- `context/PROJECT_STATE.md` là nguồn truth về trạng thái dự án.
- `context/XU_SESSION.md` là working memory của phiên hiện tại.
- Meeting log là evidence, không phải state.
- Authority hierarchy: `VINH > XU > AGENT`.
- Không tự ý sửa Protected Core hoặc baseline frozen.

=> Đọc đủ context rồi mới được hành động.

## Known Incidents / Lessons Learned

- **ROOM-2026-001 — Provenance Gate**: `docs/ROOM-2026-001-PROVENANCE-GATE-LESSON-LEARNED.md`
  Bài học về provenance reasoning, multi-agent source independence, credential discipline và agent onboarding.
  Đọc trước khi Agent mới xử lý dữ liệu chưa xác minh nguồn gốc (preview/cache/second-hand report).
