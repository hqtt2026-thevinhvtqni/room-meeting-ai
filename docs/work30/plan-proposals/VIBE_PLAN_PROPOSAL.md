# VIBE PLAN PROPOSAL — WORK 30 (GPT-AUTONOMOUS-BUILD-TEAM)

- Task: W30-PLAN-REQ-002 (đề xuất độc lập của Vibe, nộp trước khi đọc proposal của Cla/Go/Qe)
- Người nộp: Vibe — Independent Planner — lộ trình GitHub
- Thời điểm nghe/đọc chỉ thị của Xu: 2026-10-17 22:35 UTC+7 (qua yêu cầu của anh Vinh trong phiên Vibe Work "Work 30")
- Định danh: ACK — W30-PLAN-REQ-002 — Vibe (GLM, Mistral Vibe Work, acting for VINH MR) — Independent Planner (GitHub route) — 2026-10-17 22:40:00 UTC+7
- Trạng thái: SUBMITTED — chưa đọc proposal của Cla/Go/Qe tại thời điểm nộp

## 1. Phạm vi khảo sát đã thực hiện (bằng chứng READ/TRACE)

Nguồn đã đọc trên branch `work/30-gpt-autonomous-build-team` (commit đọc: b7bc31e2):
- `30/README.md` — vị trí Work 30, giao thức đồng bộ, phase hiện tại: independent planning.
- `GPT-AUTONOMOUS-BUILD-TEAM/BIEN_BAN_W30.md` — mô hình đội, quy tắc ACK, trình tự cổng.
- `GPT-AUTONOMOUS-BUILD-TEAM/PLAN_W30.md` — bảng cổng W30-P01..P10 và yêu cầu kiểm thử.
- `GPT-AUTONOMOUS-BUILD-TEAM/NHAT_KY_THI_CONG_W30.md` — nhật ký hiện trạng.
- Cây mã nguồn: `core/` (governance, identity, meeting_service, secretary, intent_router, connectors...), `tests/` (34 file test gồm test_e2e.py, test_integration.py, test_governance.py, test_identity.py, test_mcp_server.py...), `pytest.ini`, `w14_browser_e2e.py`, `wee_work13_adapter.py`.
- `docs/`: WORK30_* governance docs, MCP_PUBLIC_BOUNDARY_V1.md, ROOM-2026-001-transcript.
- `README.md`: onboarding ROOM HOP, baseline frozen v0.2.1, bài học Provenance Gate.

Chưa đọc được (ghi NOT VERIFIED): nội dung Sandbox ROOM-HOP (không có endpoint xác minh trong phiên), các file chi tiết trong `core/`/`tests/` (chỉ cấu trúc), các proposal của Cla/Go/Qe (cố ý chưa đọc).

## 2. Kiến trúc thi công E2E — Automatic đề xuất

Nguyên tắc: mọi bước đều có cổng, mỗi cổng có đầu ra bằng chứng và lệnh chạy tự động tái lập được. Không bước nào tự nhận PASS nếu thiếu bằng chứng.

### 2.1 Chuỗi tự động hoá (pipeline 6 tầng)
1. **GATE-0 SURVEY (tự động):** script quét cấu trúc repo + Sandbox mirror (nếu endpoint có), xuất `survey_report.json` (danh sách file, hash, khác biệt Sandbox/GitHub). Lệnh: `python -m tools.w30 survey --out audit/w30/survey_report.json`.
2. **GATE-1 PLAN-APPROVAL (thủ công, Vinh):** input là plan hợp nhất của Xu; output là quyết định APPROVE/REVISE/REJECT ghi trong biên bản. Cổng duy nhất chặn build.
3. **GATE-2 BUILD (Nu, tự động):** Nu thi công theo plan đã duyệt; mỗi commit gắn task ID + defect ID; build chạy trong CI-style runner: `pytest tests/ -q` xanh là điều kiện để tạo build candidate. Không deploy trước khi có candidate + manifest (commit SHA, thời điểm, môi trường).
4. **GATE-3 REPAIR (Vi, tự động theo defect ID):** mỗi defect cần: tái hiện (lệnh + log), patch có phạm vi, test trước/sau, 2 lần sửa không hiệu quả → escalate phân tích nguyên nhân gốc cho Xu/Vinh.
5. **GATE-4 VERIFY (An → Cla → Ka):** An chạy bộ kiểm thử độc lập (mục 3); Cla phản biện đối kháng trên candidate đóng băng; Ka review tổng thể. Ba báo cáo độc lập, đúng thứ tự.
6. **GATE-5 HANDOFF (Xu):** kết luận DONE/PASS/DECISION/BLOCKED, known gaps, hướng dẫn tái chạy + rollback.

### 2.2 Chuỗi E2E thật (không mock để tuyên bố runtime thật)
Luồng bắt buộc: `MCP client → room_hop_mcp (server) → core (intent_router → governance → identity → meeting_service/secretary) → workspace/execution_host`.
- Dùng đúng ranh giới công khai đã ghi trong `docs/MCP_PUBLIC_BOUNDARY_V1.md`; không gọi nội bộ để "đi tắt".
- Mỗi run E2E ghi: lệnh, môi trường, thời điểm UTC+7, exit code, log path, commit SHA — xuất vào `audit/w30/e2e/<run-id>/`.
- E2E browser (mở rộng từ `w14_browser_e2e.py`) chỉ tính là bằng chứng khi có log runtime thật + artifact.

### 2.3 Kiểm soát đồng bộ Sandbox ↔ GitHub
- Hai nguồn độc lập cho đến khi có bằng chứng đồng bộ (theo bài học Provenance Gate ROOM-2026-001).
- Mọi file mirror phải verify bằng readback + hash; thiếu file → BLOCKED, không PASS.
- Loại khỏi mirror: `__pycache__`, `*.pyc`, `desktop.ini`.

## 3. Kế hoạch kiểm thử (khớp mục B PLAN_W30)

| Nhóm | Phạm vi | Cách chạy | Đầu ra |
|---|---|---|---|
| Unit | data contract, state machine, router, path safety (`test_governance.py`, `test_identity.py`, `test_intent_router.py` + test mới cho W30) | `pytest tests/ -q -k "unit or governance or identity or router"` | JUnit XML + exit code |
| Integration | ranh giới ROOM-HOP, lỗi/timeout (`test_integration.py`, `test_connectors.py`, `test_mcp_server.py`) | `pytest tests/test_integration.py tests/test_mcp_server.py -q` | log + artifact |
| Real E2E | MCP → Core → Workspace, không mock; mở rộng `tests/test_e2e.py` | script `audit/w30/e2e/run_e2e.py` | log runtime, artifact truy vết |
| Negative/Security | path escape, allowlist bypass, secrets, identity/permission, giả mạo ACK | test mới `tests/test_w30_security_negative.py` | báo cáo lỗi bắt được |
| Regression | defect đã sửa + baseline v0.2.1 (`test_meeting_lifecycle_v021.py`) | full `pytest` + so baseline | kết quả so sánh baseline |

Mỗi test ghi: lệnh, môi trường, thời điểm, exit code, kết quả, artifact, commit SHA.

## 4. Trình tự thi công (timeline)

| Bước | Việc | Chủ trì | Bằng chứng |
|---|---|---|---|
| 1 | Bốn proposal độc lập nộp + ACK | Cla/Go/Qe/Vibe | file proposal + ACK + readback |
| 2 | Hợp nhất plan (đồng thuận/bất đồng, blocker) | Xu | PLAN_W30 v2 |
| 3 | Vinh phê duyệt | Vinh | quyết định ghi biên bản |
| 4 | Build + manifest | Nu | commit chain + build report |
| 5 | Repair defects | Vi | defect ID + patch + test trước/sau |
| 6 | Test độc lập | An | 5 nhóm test mục 3 |
| 7 | Phản biện | Cla | challenge report |
| 8 | Review | Ka | review report |
| 9 | Handoff | Xu | DONE/PASS/DECISION/BLOCKED + rollback guide |

## 5. Tiêu chí nghiệm thu (acceptance)

- 4 proposal đọc lại được; mọi task có ACK thực (file xuất hiện ≠ ACK).
- Real E2E đi hết MCP → Core → Workspace với log + artifact; không mock thay runtime thật.
- 100% unit/integration xanh hoặc có exception được ghi rõ + quyết định của Vinh.
- Security negative tests: mọi vector thử đều bị chặn và có test chứng minh.
- 3 báo cáo độc lập An/Cla/Ka đúng thứ tự cổng; không blocker P0/P1 chưa quyết.
- Hướng dẫn tái chạy + rollback đủ để bên thứ ba lặp lại được kết quả.

## 6. Rủi ro và giảm thiểu

| Rủi ro | Tác động | Giảm thiểu |
|---|---|---|
| Sandbox read endpoint trả rỗng (đã từng xảy ra theo 30/README.md) | Không verify mirror | Mọi mirror bắt buộc readback + hash; thiếu → BLOCKED |
| Dispatch/ACK không xác minh được giữa các AI | Cổng P02/P03 kẹt | ACK tường minh trong file proposal + biên bản; CHƯA XÁC NHẬN nếu thiếu |
| Đổi baseline v0.2.1 không kiểm soát | Mất regression anchor | Baseline frozen, chỉ Vinh quyết thay đổi |
| Vá lặp lỗi (2 lần không hiệu quả) | Lãng phí, che nguyên nhân gốc | Quy tắc dừng và escalate bắt buộc |
| Mock bị dùng thay runtime thật | PASS giả | Cấm trong định nghĩa E2E; Cla challenge gate kiểm tra |

## 7. Rollback

- Mọi thay đổi trên branch riêng `work/30-gpt-autonomous-build-team`; main không bị ảnh hưởng.
- Mỗi cổng GATE-2..4 tạo tag `w30/<gate>-<date>-<sha>`; rollback = revert commit/tag trước cổng gần nhất.
- Rollback phải ghi trong nhật ký: ai, khi nào, lý do, SHA trước/sau.

## 8. Khuyến nghị cho plan hợp nhất (góp ý độc lập)

- Chuẩn hoá `audit/w30/` làm nơi chứa mọi bằng chứng (survey, e2e run, challenge, review).
- Thêm định dạng `evidence.json` thống nhất: {task_id, actor, role, timestamp_utc7, action, command, exit_code, artifact, commit_sha, status}.
- Cổng An/Cla/Ka nên chạy trên cùng candidate SHA đóng băng, ghi SHA trong cả ba báo cáo.
- Vibe tự nguyện nhận thêm vai trò verify runner GitHub nếu Xu cần.

— Hết đề xuất độc lập của Vibe. Chưa đọc proposal của Cla/Go/Qe tại thời điểm nộp này.
