# W32-EVIDENCE-CLA-06 — CTO review DOC-125: OS resource quota cho Execution Host (Windows Job Object)

- **Số hiệu:** tự đặt bởi Cla; Ka cấp số đăng ký chính thức (Cla không sửa DOC-055)
- **Work:** 32 — CI/CD
- **Người thực hiện:** Cla (Claude) — AI-03 / CTO, phản biện triển khai và kiểm thử
- **Ngày:** 2026-11-14
- **Đối tượng:** DOC-125 (PROPOSED — NOT APPROVED)
- **Phạm vi quyền:** READ-ONLY. Không sửa code, không commit, không PR, không protected execution, không chạm ADMIN-PC.
- **Kết luận:** IMPLEMENTABLE WITH CONDITIONS

## A. Truy vết và giới hạn bằng chứng

- Nhánh `work/32-main-integration-remediation-20261113`; SHA tham chiếu Run #508 `7a93ce6d5546f778e76db47b201dc1574e02940d`.
- Blob (theo DOC-035 LOG-129/130): `execution_host/process_control.py` = `9f5eeddbbcb32152b19321ac59563e2729a3303c`; `execution_host/granted_host.py` = `1c5c05f9204510b98775069ed8378d8ac2c69e3f`; `core/execution_authority.py` = `dd9becadd56a1df4c3f306de317b2f70f2b3b1db`; `tests/test_execution_host_grants.py` = `c70ed4bee8a098aae27fcf921e0570bde95bf1f7`.
- **GIỚI HẠN:** Sandbox Work 32 không có `execution_host/`; `sandbox_read execution_host/process_control.py` trả FileNotFoundError; phiên này không có công cụ đọc GitHub. Mô tả mã dưới đây là THỨ CẤP từ DOC-035 LOG-129/130/132 (Xu) và DOC-124 (Ka), CHƯA tự đối chiếu từng dòng.
- Hiện trạng theo hồ sơ: `run_bounded()` cap 1 MiB stdout+stderr, timeout, `taskkill /PID /T /F` (xác nhận cây chỉ khi taskkill thành công và root thoát; nếu không, kill root, kết quả unconfirmed). Không có Job Object; không có quota memory/CPU/process-count. Chưa thấy đường cancellation ở cấp Host.
- Test hiện có: output cap, timeout + child marker (hosted Windows Run #508, 26 test); Core: thread concurrency (8 thread/16 grant), tamper, single-use. Chưa có test đa process, chưa có crash/restart sau `run_started`.

## B. Thiết kế (tóm tắt)

Giao diện hẹp `ResourceBackend` (spawn_contained / verify / resume / terminate_tree / usage / close); `WindowsJobObjectBackend`; `UnsupportedBackend` luôn DENY (BLOCKED, quota_backend_unsupported).

Trình tự fail-closed (lỗi bất kỳ bước nào → terminate cây, đóng handle, BLOCKED, lệnh chưa chạy):
1. Policy hợp lệ = min(policy đã được Core xác thực, trần cứng của Host); không lấy từ request.
2. Ghi `run_started` kèm digest/giá trị policy.
3. CreateJobObjectW (handle không kế thừa).
4. Đặt giới hạn, đọc lại bằng QueryInformationJobObject, so khớp từng trường.
5. Tạo process suspended.
6. Gán vào Job; xác minh IsProcessInJob, PID list = 1, ActiveProcesses = 1.
7. Validate online lần hai với Core.
8. ResumeThread (suspend count trước đó phải = 1).
9. Chạy: output cap, timeout, cancel.
10. Sau khi root thoát/timeout/cancel: kiểm ActiveProcesses; còn dư thì TerminateJobObject, poll về 0, đóng handle.
11. Ghi `run_completed` kèm giới hạn, cơ chế, kết quả gán/xác minh, peak memory, CPU time, max process, orphans_killed, kết quả terminate.

`taskkill` chỉ là lớp phụ.

## C. API Windows / Python

- Memory cả cây: ExtendedLimitInformation + JOB_MEMORY (0x200); từng process: PROCESS_MEMORY (0x100). Là giới hạn committed memory; vượt thì cấp phát lỗi/process chết, không đảm bảo bị kill.
- Process count: ACTIVE_PROCESS (0x8). Hành vi khi vượt phải đo bằng test.
- CPU rate: CpuRateControlInformation, ENABLE|HARD_CAP (0x1|0x4), CpuRate = % x 100 trên tổng core; bóp, không kill.
- CPU time: JOB_TIME (0x4), PerJobUserTimeLimit (100 ns, chỉ user time); vượt thì terminate job.
- KILL_ON_JOB_CLOSE (0x2000). KHÔNG đặt BREAKAWAY_OK / SILENT_BREAKAWAY_OK.
- Hàm: AssignProcessToJobObject, IsProcessInJob, QueryInformationJobObject, TerminateJobObject, CloseHandle; tùy chọn IOCP để phân loại telemetry.
- Python: `ctypes` thuần, không phụ thuộc pywin32; khai báo argtypes/restype đủ (HANDLE c_void_p, SIZE_T c_size_t, use_last_error=True); tự định nghĩa CREATE_SUSPENDED=0x4.
- A1 (ít thay đổi): Popen(CREATE_SUSPENDED|CREATE_NEW_PROCESS_GROUP|CREATE_NO_WINDOW) + Assign + resume qua Toolhelp32 thread (phải đúng 1 thread). Còn cửa sổ nhỏ: host chết trước Assign để lại process suspended ngoài job (chưa chạy code).
- A2 (mạnh hơn): CreateProcessW + STARTUPINFOEX + PROC_THREAD_ATTRIBUTE_JOB_LIST (0x2000D) + CREATE_SUSPENDED; sinh ra đã trong job; cần tự tạo pipe. Ghi nhận Windows 10+; cần probe build ADMIN-PC.
- Khuyến nghị: A1 trước, nâng A2 sau khi probe xác nhận; cùng một backend interface.

## D. File cần thay đổi nếu được duyệt (tên mới là đề xuất)

`execution_host/process_control.py`; `execution_host/resource_quota.py` (mới); `execution_host/win32_job.py` (mới); `execution_host/granted_host.py`; `core/execution_authority.py` (CÓ ĐIỀU KIỆN, chỉ nếu schema từ chối trường mới); `tests/test_execution_host_resource_quota.py` (mới, Windows-only); `tests/test_execution_authority_multiprocess.py` (mới); `tests/helpers/quota_workloads.py` (mới); `.github/workflows/ci-validation.yml`.
Vướng: lane Linux hiện chạy đường Host; nếu Linux DENY thì test đỏ -> test-double chỉ tiêm qua constructor, không qua env/config; `server.py` chọn backend cố định theo nền tảng.

## E. Test matrix (PASS khi)

- a Memory: child chạm trang tới >=4x giới hạn; host sống; peak job <= giới hạn (sai số có tài liệu); run không PASS; Run Record ghi.
- b CPU: N thread quay T>=10 s; CPU time <= cap% x core x T x (1+dung sai); thêm ca JOB_TIME bị terminate.
- c Process count: K > giới hạn child; số marker <= giới hạn-1; không process ngoài job.
- d Cha nhiều child, sâu 3 tầng: mọi PID IsProcessInJob = TRUE.
- e Con sống sau cha: ActiveProcesses > 0 được phát hiện, kill, về 0; ghi orphans_killed; không đủ điều kiện PASS (D3).
- f Timeout/cancel/thu hồi grant giữa chừng: cả cây chết <= N giây; không marker mồ côi; đọc pipe không treo.
- g Gán Job thất bại (tiêm lỗi từng bước, job cha chặn assign): marker tác dụng phụ KHÔNG xuất hiện; BLOCKED đúng mã; process suspended bị terminate.
- h Host crash/restart: TerminateProcess harness -> cây chết nhờ KILL_ON_JOB_CLOSE; restart không resume run cũ, đánh dấu incomplete.
- i Không orphan: quét theo marker/PPID sau mọi ca.
- j Giới hạn thật: chạy trên hosted windows-latest VÀ self-hosted ADMIN-PC; hosted không thay thế ADMIN-PC.
- Bổ sung: job handle không kế thừa; fail-closed khi Core down, policy sai, OS không hỗ trợ, telemetry lỗi; test hiện có vẫn xanh.

## E2. Run Record

1. 6–8 process Core độc lập ghi cùng JSONL (barrier): event đủ, không dòng xé, chain hợp lệ từ genesis, grant_id duy nhất, không mất event. Kiểm mã: `msvcrt.locking` LK_LOCK thử ~10 lần/1 s rồi OSError; khóa phải ở byte cố định; không lấy được khóa -> fail-closed (chưa thấy mã; điểm cần xác minh, không phải kết luận lỗi). Thêm: giết process giữ khóa, process khác lấy được.
2. Crash sau `run_started` trước `run_completed` (start_run rồi os._exit): mở lại -> completion=None, grant vẫn consumed, chain hợp lệ, không tổng hợp PASS. Biến thể đứt đuôi: D4.
3. Hash chain sau restart: xác minh toàn chain, ghi tiếp vẫn hợp lệ.
4. Run chưa hoàn tất không PASS: kiểm cả tầng người tiêu thụ (WEE adapter / evidence / release gate).
5. Không tái dùng grant: start lại sau completed; sau crash-incomplete; hai process start đồng thời (đúng 1 thành công); grant hết hạn + đã tiêu thụ.
Nên đặt policy digest/giới hạn/cơ chế vào `run_started`.

## F. Rủi ro / tương thích

- Win10 Pro hỗ trợ job lồng, CPU rate control (Win8+), JOB_LIST (Win10); build ADMIN-PC chưa biết -> probe chỉ-đọc trên self-hosted runner. ctypes có sẵn trong Python 3.12; không Docker; không đổi cấu hình OS toàn cục; không cần admin. Nếu Assign bị từ chối do job cha -> coi là môi trường không hỗ trợ, BLOCKED.
- Process do dịch vụ khác tạo (WMI, Task Scheduler, SCM) nằm ngoài job; allowlist pytest-only giảm rủi ro, ghi vào threat model.
- venv python.exe thường sinh interpreter con: ActiveProcessLimit phải tính launcher + interpreter + child thật của test; đo, không đoán.
- Memory limit không đồng nghĩa kill; CPU hard cap bóp, đo trên VM có biến thiên (dung sai + cửa sổ dài).
- Giá trị quota: không đoán; đo baseline >=20 lần trên ADMIN-PC và hosted (peak memory, CPU time, max process), lấy p99 x hệ số dự phòng.
- Linux: setrlimit không tương đương (RLIMIT_NPROC theo user) -> khuyến nghị DENY protected execution trên Linux.
- Quyết định cần Xu: D1 backend theo nền tảng + Linux deny + test-double qua constructor; D2 trường resource_policy ở Core hay Host-ceiling (khuyến nghị Host-ceiling trước); D3 process mồ côi sau root thoát: kill + ghi + không-PASS (khuyến nghị); D4 journal đứt đuôi: fail-closed hay cắt đuôi; D5 định nghĩa đường cancel cấp Host; D6 xác nhận JSONL + khóa file là persistence được duyệt (DOC-123 ghi SQLite).

## G. Ước lượng (một kỹ sư, sau DOC-034; chưa có số đo)

B0 nhận nguồn + trace + chốt D: 0,5–1 ngày; B1 spike ctypes + probe ADMIN-PC: 1–2; B2 backend A1 + UnsupportedBackend: 1,5–2; B3 tích hợp Host + Run Record: 1–1,5; B4 test a–j hosted Windows: 2–3; B5 test Run Record đa process + crash: 1–1,5; B6 đo baseline quota: 1 + thời gian chạy; B7 exact-SHA CI + retest + bằng chứng ADMIN-PC: 1–2; B8 (tùy chọn) A2: 1–2. Tổng khoảng 9–14 ngày công.

## H. Kết luận

**IMPLEMENTABLE WITH CONDITIONS.**
C1 trace từng dòng tại SHA 7a93ce6 xác nhận giả định mục A; C2 Xu chốt D1–D6; C3 spike chứng minh job lồng, CPU rate control, (nếu A2) JOB_LIST trên môi trường giống ADMIN-PC; C4 giá trị quota từ phép đo; C5 H1 chỉ PASS khi có bằng chứng self-hosted ADMIN-PC (hosted Run #508 không đủ).
Run Record: hash-chain và grant dùng một lần đã có; test đa process và crash/restart chưa có nên H1 mục 7 chưa đạt.

Không sửa code, không commit/PR, không protected execution, không PC action. Work 32 ACTIVE — NOT ACCEPTED — NOT RELEASED.

[KÝ: CLA | CTO — phản biện triển khai và kiểm thử; không phải phê duyệt triển khai]
