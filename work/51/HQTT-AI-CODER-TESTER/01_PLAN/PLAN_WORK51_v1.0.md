# PLAN_WORK51 — HQTT AI Coder–Tester qua A2A

- **Work:** 51 — HQTT AI Coder–Tester
- **Phiên bản:** v1.7
- **Trạng thái:** P3 EXTENDED (iteration 3) — baseline 58/58 tests PASS trên CI run `39945767381` (commit `0dbf964`); D-09 đã merge `main` → nhánh Work 51 (PR #24, 22 ahead / 0 behind); iteration 3 thêm container-grade sandbox profile D-04c (Docker: --network none, seccomp=default, --cap-drop ALL, --read-only, memory/cpu/pids caps) kèm 4 test mới tự skip khi không có Docker (kỳ vọng suite 62 trên CI có Docker) — test execution PENDING CI; overall Work 51 vẫn NOT DONE pending official A2A SDK / signed-card conformance, independent QA sign-off và CI xác minh trên merge head.
- **Chủ sở hữu triển khai:** Qc — Qwen Coder
- **Điều phối / hồ sơ:** Xu — AI-01
- **QE/QA độc lập:** Qw — AI-05 (không phải trưởng dự án)
- **Nhánh:** `work/51-hqtt-coder-tester`
- **Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`
- **Ngày:** 2026-10-23 (UTC+07)
- **Nguyên tắc:** Đây là bản kế hoạch duy nhất của Work 51 trên Git; mọi sửa đổi kế hoạch cập nhật trực tiếp file này và ghi nhật ký ở cuối. Không tạo bản kế hoạch song song.

## 1. Mục tiêu

Qc triển khai toàn trình một luồng Coder–Tester tự động, trong đó A2A (Agent-to-Agent — giao thức giao tiếp giữa tác nhân AI) là giao thức trao đổi tác vụ và sản phẩm; ROOM-HOP giữ vai trò điều phối/hồ sơ khi có thể tích hợp; GitHub branch là kênh làm việc chính cho Qc vì Qc hiện không truy cập ROOM-HOP được.

Không dừng ở sơ đồ hoặc ví dụ minh họa: phải có implementation, test thực thi được, kết quả và hồ sơ bàn giao. Phạm vi là Work 51, không mở rộng Work 28.

## 2. Vai trò và quyền tự chủ

- **Qc — Qwen Coder:** owner triển khai; tự audit, quyết định kỹ thuật trong phạm vi, viết code, tích hợp, chạy test, sửa lỗi, cập nhật tài liệu và bàn giao. Không dừng hỏi các câu hỏi thường lệ hoặc yêu cầu Vinh canh PC.
- **Xu:** đã xác lập phạm vi và tiêu chí; theo dõi quyết định/handoff. Không thay Qc viết code.
- **Qw — QE/QA:** đánh giá độc lập về test/evidence khi được gọi; không làm trưởng dự án.
- **Coder Agent:** tạo/sửa artifact trong workspace/branch được cấp.
- **Tester Agent:** vai trò và ngữ cảnh tách biệt; kiểm tra artifact thực tế theo hợp đồng gốc, không được sửa code để tự cho PASS.
- **Vinh:** chủ sở hữu HQTT. Chỉ cần escalates kh
i có quyết định vượt phạm vi/quyền, rủi ro không thể tự xử lý hoặc phụ thuộc hạ tầng không sẵn sàng.

Role names above describe intended responsibilities for this Work. Do not assume a particular API/model adapter, Skill, identity mapping, or automatic inter-agent calling mechanism already exists.

## 3. Kiến trúc mục tiêu

1. **Work Contract:** mục tiêu, phạm vi, acceptance criteria, phiên bản schema, giới hạn thời gian/retry, quyền và đầu ra.
2. **A2A Client/Orchestrator:** tạo Task, gửi cho Coder, nhận Artifact, chuyển input cho Tester, nhận kết quả, quản lý vòng feedback và trạng thái.
3. **Coder Agent:** nhận hợp đồng và feedback; sinh/sửa artifact có định danh và phiên bản.
4. **Tester Agent:** tạo/chạy kiểm thử độc lập; trả PASS/FAIL/BLOCKED kèm bằng chứng.
5. **Execution Sandbox:** chạy code/test an toàn với giới hạn quyền, thời gian, tài nguyên và network.
6. **Evidence/Handoff:** log, test report, artifact hash, phiên bản, trạng thái và các giới hạn còn tồn tại.
7. **ROOM-HOP integration:** chỉ tích hợp qua các interface hiện có và đã xác minh; không giả định Qc có thể truy cập ROOM. GitHub branch là nơi nhận code/plan và báo cáo của Qc.

A2A là giao thức, không tự cung cấp execution sandbox, bảo mật, persistence hoặc chất lượng test. Không bắt buộc thêm LangGraph/AutoGen. Trước khi tự viết protocol wrapper, Qc phải xác minh đặc tả A2A và thư viện/SDK hiện có, chọn phương án tương thích nhỏ nhất, ghi rõ version và lý do.

**Triển khai cụ thể (v1.2, ghi nhận P1/P2 xong):** các quyết định D-01..D-09 nằm trong `DECISION_REGISTER.md`; sơ đồ thành phần/sequence/error model nằm trong `02_ARCHITECTURE/ARCHITECTURE_WORK51.md`; binding chọn là JSON-RPC 2.0 + text-part tối thiểu, gom toàn bộ trong `03_CODE/a2a_ct/a2a.py` để swap sang SDK chính thức sau mà không đổi module khác.

## 4. Trình tự thực hiện

### P0 — READ / TRACE
- Đọc charter/brief, toàn bộ cây Work 51 trên branch, cấu trúc hiện có và các interface liên quan.
- Ghi rõ verified facts, assumptions, gaps,
 reuse candidates; không sửa main.
- Xác minh đặc tả A2A, transport, message/task/artifact schema, trạng thái và khả năng SDK thực tế.

### P1 — DECIDE / CONTRACT
- Chốt contract/schema, task state machine, API boundaries, error model, auth/trust boundaries, retry/timeout/cancel và evidence format.
- Giữ một plan canonical: `work/51/HQTT-AI-CODER-TESTER/01_PLAN/PLAN_WORK51_v1.0.md`; tên file giữ nguyên, version cập nhật trong nội dung.
- Tạo các tài liệu kiến trúc/code/test cần thiết trong thư mục chuẩn Work 51; tránh lặp nội dung kế hoạch.

### P2 — BUILD vertical slice
Xây một luồng tối thiểu hoàn chỉnh:
1. Orchestrator tạo Task từ contract.
2. Coder nhận Task và trả Artifact định danh được.
3. Artifact được chuyển cho Tester.
4. Tester chạy test độc lập và trả kết quả có evidence.
5. Khi FAIL, feedback có thể hành động quay lại Coder.
6. Orchestrator dừng đúng khi PASS hợp lệ hoặc chuyển BLOCKED khi hết giới hạn.

### P3 — VERIFY
Chạy test thực tế, bao gồm:
- happy path PASS;
- seeded failure → feedback → sửa → test lại;
- FAIL kéo dài vượt retry limit;
- timeout / agent unavailable / transport error;
- malformed Task hoặc Artifact;
- thiếu evidence không được PASS;
- task trùng, retry idempotency và trạng thái sau restart;
- kiểm tra quyền, secrets, untrusted code và giới hạn thực thi.

### P4 — HANDOFF
- Cập nhật README, sơ đồ, contract/schema, test, evidence và nhật ký.
- Báo file/commit SHA, lệnh đã chạy, kết quả thực tế, tiêu chí PASS/FAIL/BLOCKED, giới hạn còn lại và bước kế tiếp.
- Chỉ ghi PASS nếu đã chạy và có evidence; không suy diễn từ code tồn tại.

## 5. Ranh giới bắt buộc

- Core :8000 là nguồn sự thật duy nhất; không tạo Core thứ hai, không đưa Core vào Sandbox.
- Không sửa MAIN SOURCE, không thay đổi Work 28, không mở rộng sang provider/camera/voice/browser trừ khi có dependency chứng minh cần thiết và được phê duyệt.
- Không commit vào main, không merge/triển khai production, không thay đổi secrets hoặc quyền tổ chức.
- Dùng nhánh `work/51-hqtt-c
oder-tester`; commit trên nhánh này khi quyền và công cụ cho phép. Không tuyên bố đã push nếu không có bằng chứng.
- Coder và Tester phải tách vai trò/ngữ cảnh/quyền. Coder không được tự phê duyệt sản phẩm của mình.
- A2A Task `completed` không đồng nghĩa test PASS.
- Mỗi task tối đa 2 vòng sửa sau FAIL; sau đó BLOCKED với evidence và đề xuất xử lý. Không lặp vô hạn.

## 6. Tiêu chí nghiệm thu

- Có implementation thực sự của luồng Coder → Tester → feedback loop.
- Giao thức/schema được xác định theo đặc tả A2A thực tế, có kiểm thử contract.
- Có test chạy được và log kết quả; Tester đánh giá đúng artifact/commit/hash đã kiểm.
- PASS/FAIL/BLOCKED được phân biệt chính xác; thiếu evidence không thể PASS.
- Timeout, lỗi transport, artifact lỗi, retry giới hạn và khôi phục trạng thái được kiểm tra.
- Có ranh giới thực thi an toàn và kiểm thử từ chối thao tác trái quyền.
- Tài liệu và handoff tái lập được, ghi đúng phiên bản, commit, dependency và giới hạn.
- Không tiêu chí nào được đánh dấu PASS nếu chưa có bằng chứng kiểm chứng trực tiếp.

## 7. Hành vi khi bị chặn

Qc phải tự kiểm tra lại nguồn, công cụ và đường đi có sẵn trước khi báo BLOCKED. Khi thật sự bị chặn, ghi rõ: lỗi quan sát được, các bước đã thử, bằng chứng, ảnh hưởng, phương án khả thi tiếp theo. Không yêu cầu Vinh canh PC và không hỏi lại những điều đã được quy định trong kế hoạch.

## 8. Nhật ký sửa đổi

| Phiên bản | Ngày | Người sửa | Nội dung |
|---|---|---|---|
| v1.1 | 2026-10-23 | Xu — AI-01 | Chuyển owner triển khai sang Qc/Qwen Coder; xác nhận GitHub branch là kênh làm việc chính; A2A là giao thức cốt lõi; Qw chỉ QE/QA độc lập; bổ sung vòng đời BUILD/VERIFY/HANDOFF và tiêu chí nghiệm thu. |
| v1.2 | 2026-10-23 | Vibe | Commit vertical slice P2: package `03_CODE/a2a_ct`, test suite and docs. At commit time, test execution was pending. |
| v1.3 | 2026-10-23 | Xu — AI-01 | Updated this canonical plan in place after running GitHub Actions on the actual branch: 43 tests passed; HTTP demo verified `co
rrect → PASS`, `seeded_bug → FAIL→feedback→PASS`, `always_bug → BLOCKED` after 2 fix rounds. Added CI workflow `.github/workflows/work51-a2a.yml`; fixed pytest collection warning (`TesterBackend.__test__ = False`). Evidence run: `39930470092`, tested code commit `2645366de183e7a0905a6c9d1b378741aec7b693`. Overall Work 51 remains PARTIAL: sandbox is not containerized/network-isolated, task state is in-memory, signed A2A Agent Card and official A2A SDK/spec conformance are not proven, and branch is 27 commits behind main. No rebase/merge or production deployment performed. |
| v1.4 | 2026-10-23 | Vibe | Iteration 2 theo đúng phạm vi đã duyệt: sandbox hardening D-04b (env scrub — secrets không rò vào child; POSIX rlimits CPU/AS/FSIZE/NPROC; unshare -n network isolation có availability probe; cap input 200KB); PersistentTaskStore D-08b (JSON atomic rename, task state sống qua restart, backend nhận store qua constructor); A2A binding v1.2 D-01b (Agent Card: protocolVersion 1.0, version 1.2.0, preferredTransport; Task: contextId, createdAt, updatedAt, status.timestamp; method tasks/cancel cho non-terminal task). Thêm 15 test mới (cancel qua HTTP, persistence/restart, sandbox hardening) — kỳ vọng suite 58. Test execution PENDING tại thời điểm commit; chỉ ghi PASS khi CI đã chạy thật trên push này. |
| v1.5 | 2026-10-23 | Xu — AI-01 | CI xác nhận iteration 2 sau khi sửa ba dòng bị tách cú pháp trong `coder_agent.py`, `test_http.py`, `tester_agent.py`: **58 passed in 10.82s**; HTTP demo `correct → PASS`, `seeded_bug → PASS` sau 1 vòng, `always_bug → BLOCKED` sau giới hạn 2 vòng; demo exit 0; evidence artifact `work51-evidence-39945767381` (ID `12498725031`). CI run `39945767381`, commit kiểm chứng `0dbf964bd64c2c8129bff3aaa60915c681fd403d`. Overall Work 51 vẫn PARTIAL: sandbox chưa container/seccomp; official A2A SDK/spec conformance chưa chứng minh; D-09 chưa xử lý, branch diverged 17 ahead / 27 behind main. Không rebase/merge, không sửa `main`, không triển khai production. |

| v1.6 | 2026-10-23 | Xu — AI-01 | Xu tự quyết định D-09 sau khi kiểm tra 27 commits chỉ thêm file dưới `10/COMPUTER-AGENT/` và không chạm đường dẫn Work 51. Tạo PR #24 theo chiều `main` → Work 51, xác nhận mergeable clean rồi merge bằng merge commit `23194b90efe993614bc961607d3d481165d56b36`; `main` không nhận code Work 51. Sau merge branch 22 ahead / 0 behind. Cần CI chạy lại trên merge head; không coi đây là nghiệm thu toàn Work. |
| v1.7 | 2026-10-23 | Vibe | Iteration 3 theo ưu tiên của Xu sau D-09: container-grade sandbox profile D-04c — sandbox_container.py chạy runner trong Docker container khóa chặt (--network none, --memory 512m, --cpus 1.0, --pids-limit 64, --cap-drop ALL, no-new-privileges, seccomp=default, --read-only, mount read-only); available() probe Docker + pre-pull image, caller fallback về Sandbox() khi không có Docker; env scrub + cap input 200KB tái dùng từ sandbox.Sandbox. Thêm 4 test (test_sandbox_container.py — tự skip khi không có Docker; kỳ vọng suite 62 trên CI). Test execution PENDING tại thời điểm commit; chỉ ghi PASS khi CI chạy thật. Cảnh báo gitlink `.gitmodules` để xử lý riêng theo repo hygiene, ngoài phạm vi Work 51. |
