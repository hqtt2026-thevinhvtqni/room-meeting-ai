

## W21-20261025-TRANSFER-GPT-WORK-RECORDS
- Work: 21 — AI-SKILLS (đã đọc WORK_MANIFEST.md qua MCP).
- Người thực hiện / lập hồ sơ: Vi — CODER.
- Thời gian thực hiện: 2026-10-25T19:39:21+07:00 đến thời điểm lập hồ sơ; giờ bắt đầu là mốc kiểm tra Work, không phải thời điểm của lệnh người dùng.
- Thời gian lập hồ sơ: 2026-10-25T19:40:38+07:00.
- Nguồn yêu cầu: Người dùng yêu cầu “Chuyển skill vào room qua mcp vào work 21”.
- Mức nguồn: ĐÃ XÁC MINH TRỰC TIẾP.
- Phạm vi: sao chép skill vào Sandbox Work 21 qua ROOM-HOP MCP 8030; không phải kích hoạt runtime.
- Kết quả: tạo 3 tệp dưới roomhop-skills/gpt-work-records/ gồm SKILL.md, references/templates.md, agents/openai.yaml. Đọc lại từng tệp bằng sandbox_read, nội dung khớp chính xác bản nguồn.
- Trạng thái: DONE cho sao chép và xác minh 3 tệp; tích hợp loader/runtime NOT RUN trong tác vụ này; chưa có An PASS/Ka APPROVE.
- Bằng chứng: 3 đường dẫn trên là tệp thực đã đọc lại; nguồn gốc skill gpt-work-records từ Skills cá nhân. Công cụ create trả status=ok, operation=create cho cả 3; read trả status=ok và content khớp bản nguồn cho cả 3.
- Bước tiếp theo: dùng SKILL.md và references/templates.md khi lập hồ sơ Work; nếu cần tự động nạp vào runtime phải kiểm tra hợp đồng loader riêng.

### Biên bản bàn giao
Quyết định theo chỉ thị người dùng: đặt bản skill tại roomhop-skills/gpt-work-records, giữ bản nguồn Skills hiện có. Tiêu chí sao chép đủ tệp và nội dung khớp đã đạt. Không thay đổi registry hay kết luận trạng thái toàn Work 21. Hồ sơ liên quan: NHAT_KY_THI_CONG_W21.md và transcript.md cùng mã sự kiện.
[KÝ: VI | CODER]


## W21-20261030-EXTERNAL-SKILLS-JAMESROCHABRUN-HYBRID
- Work: 21 — AI-SKILLS.
- Người thực hiện / lập hồ sơ: Grok (qua MCP ROOM-HOP 8030).
- Thời gian: 2026-10-30.
- Nguồn yêu cầu: Người dùng yêu cầu “quy hoạch cái này vào work 21 qua mcp” (cái này = phân tích jamesrochabrun/skills 24 Skills + chiến lược chia sẻ Hybrid khi team có nhiều người không dùng Claude Code).
- Mức nguồn: ĐÃ XÁC MINH TRỰC TIẾP (web + README repo + list works + list/read files Work 21).
- Phạm vi: Ghi nhận research + đề xuất chiến lược Hybrid vào Work 21; không kích hoạt runtime.
- Kết quả:
  - Tạo file mới: `08_EXTERNAL_SKILLS_JAMESROCHABRUN_AND_TEAM_HYBRID.md`
  - Cập nhật `07_RESEARCH_BACKLOG.md` (thêm mục 16–18 + NOW).
- Trạng thái: DONE cho ghi nhận research & đề xuất. Implementation (chuyển đổi Skill / tạo docs/ai-workflows mẫu) NOT STARTED.
- Bằng chứng: File 08 đã create thành công; backlog đã write; list works xác nhận work_id=21 tồn tại với tên AI-SKILLS.
- Bước tiếp theo: Chờ quyết định ưu tiên (Claude-centric vs full hybrid) rồi triển khai mẫu docs/ai-workflows hoặc mapping Manifest.

### Biên bản bàn giao
Quyết định: Lưu toàn bộ phân tích và khuyến nghị Hybrid vào Work 21 dưới dạng research note chính thức. Không thay đổi registry runtime hay loader trong task này.
[KÝ: GROK | RESEARCH]


## W21-20261120-AI-TEMPLATES-PHAN-DONG-GIANG-RESEARCH-ONLY
- Work: 21 — AI-SKILLS (existing registered Work; no new Work ID created).
- Người lập/điều phối: Xu / AI-01.
- Thời điểm: 2026-11-20 (UTC+07).
- Nguồn yêu cầu: Vinh yêu cầu lập Work/chuyển nội dung AI Templates vào để nghiên cứu chỉ nghiên cứu.
- Đối soát danh mục: Sandbox registry hiện có Work ID 21 — AI-SKILLS, manifest_exists=true; Work 21 purpose đã bao gồm nghiên cứu, thiết kế và xây dựng reusable/portable/verifiable AI Skills cho ROOM-HOP. Vì vậy dùng Work 21 hiện hữu, không tạo Work trùng.
- Quyết định phạm vi: Chỉ nghiên cứu thư viện Phan Đông Giang AI Templates và nguồn aitmpl.com. Không cài đặt, không chạy mã, không kích hoạt MCP/plugin, không tích hợp runtime, không sửa Work khác và không đồng bộ GitHub trong tác vụ này.
- Ghi nhận nguồn: trang giới thiệu hiển thị 11 nhóm Skills, Agents, Commands, MCPs, Plugins, Hooks, Settings, Loops, Mods, Sandbox, Templates; trang tự mô tả thư viện Claude Code & ChatGPT Codex. Catalog item-level chưa được enumerate trong lượt này.
- Hồ sơ: tạo research note 09_AI_TEMPLATES_PHAN_DONG_GIANG_RESEARCH.md; cập nhật 07_RESEARCH_BACKLOG.md mục 19/NOW; cập nhật DOCUMENT_REGISTER.md.
- Trạng thái: DONE cho việc chuyển nội dung nghiên cứu vào Work 21 và ghi backlog/register; item-level research NOT STARTED; compatibility/security/license verification NOT RUN; installation/implementation NOT AUTHORIZED.
- Bằng chứng: trực tiếp đọc Sandbox list_works (71 Works; Work 21 hiện hữu), Work 21 file inventory, manifest, README, register, backlog, biên bản và nhật ký; đọc trực tiếp trang https://phandonggiang.com/ai-templates ngày 2026-11-20.
- Bước tiếp theo: enumerate catalog thật và kiểm tra nguồn/commit/license; bắt đầu Skills và Agents; ghi evidence theo từng candidate.


### Đính chính biên bản — 2026-11-20
- Cụm từ ngoài ngôn ngữ trong dòng “Vinh yêu cầu lập Work/chuyển nội dung AI Templates vào để nghiên cứu chỉ nghiên cứu” là lỗi đánh máy.
- Cách hiểu và nội dung chính xác: Vinh yêu cầu đưa nội dung AI Templates vào Work để nghiên cứu chỉ nghiên cứu → chỉ nghiên cứu, không triển khai. Ranh giới research-only trong toàn bộ hồ sơ vẫn giữ nguyên.


## W21-20261120-GITHUB-INITIAL-SYNC
- Work: 21 — AI-SKILLS.
- Thời gian: 2026-11-20 (UTC+07).
- Điều phối: Xu / AI-01.
- Chỉ thị: Vinh yêu cầu kiểm tra Work 21 trên GitHub; nếu chưa có thì tạo và đồng bộ.
- READ: Kiểm tra room-meeting-ai/main: không có work/21 root; exact fetch các đường dẫn dự kiến work/21/* trả 404. Đọc lại W21 Manifest và W112 Execution Journal events 007–015: trước đó Work 21 NOT SYNCED do chưa pin branch/path/commit.
- DECIDE: Dùng nhánh riêng work/21-ai-skills, không ghi trực tiếp main. Base main SHA 70ae3fb762bd4719facbf9448919aa2ab9516429. Mapping: Sandbox AI-SKILLS/ → work/21/AI-SKILLS/; root-level Work records → work/21/; research note → work/21/09_AI_TEMPLATES_PHAN_DONG_GIANG_RESEARCH.md.
- BUILD: Tạo branch từ main; cập nhật Manifest và Document Register để ghi mapping; cập nhật research note để phân biệt quyền đồng bộ hồ sơ với quyền cài đặt/triển khai; đồng bộ README, backlog, research note, Manifest, Register, Biên bản và Nhật ký.
- Boundary: Chỉ đồng bộ hồ sơ nghiên cứu/governance. Không cài đặt, không chạy mã, không tích hợp runtime, không sửa main, không merge PR.
- Status: branch created; file writes/readback and PR creation pending.


### GitHub synchronization result — 2026-11-20
- Repository: hqtt2026-thevinhvtqni/room-meeting-ai.
- Branch: `work/21-ai-skills`, created from `main` @ `70ae3fb762bd4719facbf9448919aa2ab9516429`.
- Mapping: Sandbox root-level Work records → `work/21/`; Sandbox `AI-SKILLS/` → `work/21/AI-SKILLS/`.
- Files synchronized and exact-readback compared: 7/7 — README.md, 07_RESEARCH_BACKLOG.md, 09_AI_TEMPLATES_PHAN_DONG_GIANG_RESEARCH.md, AI-SKILLS/00_ROOT/WORK_MANIFEST.md, AI-SKILLS/00_ROOT/DOCUMENT_REGISTER.md, BIEN_BAN_W21.md, NHAT_KY_THI_CONG_W21.md.
- Result: PASS for seven exact GitHub branch file readbacks only. This is partial Work-record sync, not complete Work 21 tree parity, not main merge, not Work acceptance/release.
- PR: pending creation after final journal/register update.


### Pull request handoff — 2026-11-20
- Draft PR #62 created: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/62
- Head: `work/21-ai-skills`; base: `main`; state OPEN / DRAFT / UNMERGED.
- GitHub PR snapshot: 7 changed files, 495 additions, 0 deletions, 10 commits at creation time.
- No merge performed. PR mergeable=false at creation snapshot; review/merge readiness not inferred.
- Synchronization result remains PARTIAL: 7 scoped records exact-readback verified; remaining Work 21 tree not yet reconciled.


## 2026-11-20 — W300 capability-driven research direction
- Decision direction: use Work 300 as the first practical demand case for Work 21 reusable AI Skills; do not create another Work.
- Boundary: W21 owns reusable Skill research/specifications; W17 remains canonical owner of AI member capability/evidence profiles; W300 owns image/photo product requirements and implementation. W300 remains image/photo-only; video belongs to Work 29.
- Eight demand areas: safe local image processing; provider/model research; image generation/editing; image QA; cost/quota circuit breaker; privacy/security; artifact provenance; multi-agent evidence workflow.
- Proposed role mapping is a research hypothesis only, not assignment, authorization, runtime identity proof or capability PASS. Member/session/dispatch/ACK and tool access remain governed by W17 evidence and per-task permission.
- Research-only boundary: no install, model download, provider/API call, credential/payment activation, runtime/config change, code implementation or W300 source modification. No W300 architecture/build gate is advanced.
- Next: define reusable Skill contracts against W21 schema, reconcile duplication/ownership, prepare evidence-based capability mapping for W17 and a bounded handoff packet for W300.
