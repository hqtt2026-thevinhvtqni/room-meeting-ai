# CLA (Claude) — Independent Security Review Report — Work 28

**Agent:** Cla (Claude, Anthropic)
**Ngày:** 2026-10-11 (không có đồng hồ UTC chính xác trong phiên của Cla; báo cáo được lập SAU báo cáo của Go)
**Meeting:** MEETING-GATE2-EXT-001 (msg_aaa93ea4fa1b)
**Work:** 28 — MCP-8020-TOOLING-PLATFORM | Status: ACTIVE / NOT LOCKED
**Phạm vi lượt này:** review bảo mật độc lập + negative-test matrix. KHÔNG sửa source Work 28. KHÔNG thăm dò (probe) hệ thống live.

---

## 0. Tóm tắt điều hành

1. **Chưa có gì chạy được để tấn công/kiểm thử runtime**: không có tool thực thi nào trong live tool surface (khớp kết luận của Go). Mọi mục về isolation/timeout/network/secret là **BLOCKED (chưa kiểm chứng)**, không phải PASS.
2. **Rủi ro kiến trúc lớn nhất**: "không unrestricted shell" chỉ đúng ở tầng API. Một khi AI viết và chạy được Python tùy ý, Python tự nó là shell (subprocess, socket, ctypes, ghi file). An toàn **chỉ đến từ cô lập cấp OS/runtime**, không đến từ danh sách "approved command ID" hay validator đường dẫn.
3. **Đã chạy thật (trong container riêng của Cla, KHÔNG phải runtime canonical, KHÔNG tính cho gate G3)** hai việc, kết quả nằm ở mục 2. Hai phát hiện được xác minh bằng thực thi:
   - Test scaffold **không chạy được theo đúng bố cục thư mục đang lưu** (ModuleNotFoundError, exit=1).
   - Contract **cho phép tạo `PASS` mà không cần run_id / exit_code / evidence**, và `validate_relative_work_path` **chấp nhận** nhiều đầu vào nguy hiểm trên Windows/Unicode.
4. **Phát hiện từ bề mặt tool live** (quan sát, chưa tấn công): các tool `sandbox_*` không mang tham số principal; mọi agent ghi/xóa được file trong `06_EVIDENCE`, kể cả báo cáo của agent khác. Tính toàn vẹn của evidence hiện không được bảo vệ.

---

## 1. Phạm vi đã đọc (sandbox_read thành công)

| File | Trạng thái |
|---|---|
| 00_ROOT/WORK_MANIFEST.md | READ OK |
| 01_ORIGINAL/WORK_28_REQUIREMENT.md | READ OK |
| 02_EXTENSION/DECISION_AI_RUN_PYTHON_VIA_MCP.md | READ OK |
| 03_ARCHITECTURE/WORK_28_ARCHITECTURE_PLAN.md | READ OK |
| 03_ARCHITECTURE/MCP_TOOL_REGISTRY_V1.md | READ OK |
| 04_CODE/tool_contracts.py | READ OK |
| 05_TEST/WORK_28_TEST_PLAN.md | READ OK |
| 05_TEST/test_tool_contracts.py | READ OK |
| 06_EVIDENCE/IMPLEMENTATION_CHECKPOINT_20261011.md | READ OK |
| 06_EVIDENCE/BIEN_BAN_PHAN_CONG_GO_CLA_20261011.md | READ OK |
| 06_EVIDENCE/NHAT_KY_THI_CONG.md | READ OK |
| 06_EVIDENCE/INITIAL_EVIDENCE.md | READ OK |
| 06_EVIDENCE/GO_E2E_REVIEW_REPORT_20261011.md | READ OK (chỉ để đối chiếu, không phụ thuộc kết luận của Go) |
| Transcript MEETING-GATE2-EXT-001 | READ OK |

Chưa đọc / không có: source MCP :8020 và Core :8000 thật, W12/W13/Work 27 runtime. **BLOCKED** cho mọi đánh giá cần các nguồn này.

---

## 2. Bằng chứng thực thi (executed evidence)

**Môi trường:** container riêng của Cla, Python 3.12.3, Linux. Đây KHÔNG phải runtime canonical (W12/W13/Work 27) và KHÔNG thay thế gate G3/G4. Chỉ dùng để kiểm chứng logic thuần của `tool_contracts.py`. Code và test được chép nguyên văn từ Sandbox Work 28 sang container; không sửa nội dung.

| # | Lệnh | Kết quả | Exit code |
|---|---|---|---|
| E1 | `cd 05_TEST && python -m unittest` (đúng bố cục 04_CODE / 05_TEST đang lưu) | `ModuleNotFoundError: No module named 'tool_contracts'`, Ran 1 test, FAILED (errors=1) | **1** |
| E2 | `cd 05_TEST && PYTHONPATH=../04_CODE python -m unittest` | Ran 7 tests, OK | **0** |
| E3 | Script probe `validate_relative_work_path`, `normalize_status`, `ToolResult`, `validate_request_id` với đầu vào tấn công | Xem mục 3 (S02, S06, S08) | 0 (script chạy xong) |

Ghi chú trung thực: lần chạy đầu của harness không bắt được exit code (shell thiếu PIPESTATUS); exit code ở bảng trên lấy từ lần chạy lại có `echo $?`.

**Trạng thái:** 7 test hiện có = PASS-LOCAL (cần PYTHONPATH). Không tính vào G3.

---

## 3. Phát hiện (findings)

Severity: Critical / High / Medium / Low / Info. Trạng thái: VERIFIED (đã thực thi), OBSERVED (quan sát từ tool surface/tài liệu), DESIGN (rủi ro thiết kế, chưa có implementation), BLOCKED (không kiểm chứng được).

| ID | Phát hiện | Severity | Trạng thái |
|---|---|---|---|
| S01 | **Python = shell.** `python_run` "approved entry point" không giới hạn hành vi của code. Code do AI viết có thể gọi `subprocess`/`os.system`/`ctypes`, mở socket, ghi file, tạo symlink/junction, đọc env. Danh sách "approved command ID" không có tác dụng bảo vệ nếu chạy trên host chung. Bắt buộc cô lập cấp OS (container/VM/WSL2/Windows Sandbox hoặc tương đương): FS chỉ-ghi trong workdir riêng, không network, non-root/low-integrity, giới hạn CPU/RAM/PID/disk, kill cả cây tiến trình. Tài liệu DECISION nêu yêu cầu nhưng chưa nêu cơ chế. | **Critical** | DESIGN / BLOCKED |
| S02 | **Contract không cưỡng chế "PASS cần evidence".** `ToolResult` cho phép `status=PASS` với `evidence_ref=None`; không có trường `run_id`, `exit_code`; `result: Any`. Đã dựng được `ToolResult("req-1", PASS, "ran fine")` hợp lệ. `normalize_status("pass")` → PASS (không phân biệt hoa/thường, không gắn với evidence). Quy tắc "Never report PASS unless..." chỉ là văn bản, chưa là code. | **High** | VERIFIED |
| S03 | **Authorization không hiện diện ở tầng schema `sandbox_*`.** `sandbox_read/write/append/delete/list` chỉ nhận `work_id` + `relative_path`, không có principal. `identity_id` ở `join_meeting`, `submit_proposal`, `sandbox_create_work` là chuỗi do caller cung cấp. `sandbox_list_works` trả cả 34 Work (kể cả 22-SECURITY-AND-SAFETY, 98-e2e) cho Cla, không thấy lọc theo quyền. Có thể authorization nằm ở tầng connector/Core (chưa kiểm chứng); nếu không, đây là spoofing + truy cập chéo Work. Cla KHÔNG thử đọc/ghi Work khác để xác minh (ngoài phạm vi review). | **High** | OBSERVED / BLOCKED |
| S04 | **Evidence không được bảo vệ toàn vẹn.** Chỉ `transcript.md` được mô tả là append-only. `sandbox_write` ghi đè và `sandbox_delete` xóa được bất kỳ file nào trong `06_EVIDENCE` (kể cả báo cáo của agent khác). Evidence chạy thật (run record, exit code, hash) phải do Core/runtime ghi vào vùng AI không ghi được. Cla không thử ghi đè/xóa để xác minh. | **High** | OBSERVED (từ tool surface) |
| S05 | **Cross-channel: Python tạo symlink/junction rồi đọc qua Sandbox API.** Nếu run được phép tạo symlink/junction/hardlink trong Work, sau đó `sandbox_read` theo link có thể đọc file ngoài Work. Validator cố ý "never resolve" nên không chống được; adapter phải có kiểm tra `realpath` + containment, từ chối reparse point, mở bằng handle/O_NOFOLLOW. Junction trên Windows không cần đặc quyền. | **High** | DESIGN / BLOCKED |
| S06 | **Validator đường dẫn có lỗ hổng (VERIFIED bằng probe).** Bị CHẤP NHẬN (đáng lẽ phải từ chối): ký tự DEL (0x7f), C1 (0x85), bidi override U+202E, zero-width U+200B, fullwidth `．．／` (U+FF0E/U+FF0F), tên thiết bị Windows (`CON`, `NUL.txt`, `COM1`), thành phần có dấu chấm/khoảng trắng cuối (`.. /x`, `file.txt.`; Win32 có thể chuẩn hóa `.. ` về `..`), `.../x`, tên 8.3 (`PROGRA~1`), `~`, `%USERPROFILE%`, `$HOME`, glob (`*`, `?`), dotfile (`.git/config`), và theo đọc code: thành phần bắt đầu bằng `-` (nguy cơ argument injection khi dùng làm đối số). Từ chối đúng: `../`, `a/../../`, `/etc/passwd`, `..\x`, `C:\x`, `C:x`, UNC, `f.txt:s`, `f.txt::$DATA`, NUL, newline, độ dài >1024. Hậu tố `desktop.ini` trong cây Work gợi ý host là Windows/thư mục đồng bộ (suy luận, cần xác nhận) — khi đó các lỗ hổng trên nghiêm trọng hơn. | **High** (Windows) / Medium (POSIX) | VERIFIED |
| S07 | **Tin cậy của runner: lệnh test mặc định sẽ FAIL vì sai nguyên nhân.** Chạy `python -m unittest` từ `05_TEST` cho exit=1 (ImportError) vì `tool_contracts.py` nằm ở `04_CODE`. Rủi ro: lần "evidence" đầu tiên sẽ FAIL do bố cục; hoặc người ta thêm `PYTHONPATH`/`sys.path` hack, mở đường cho shadowing/injection (xem C3). Cần định nghĩa cách chạy chuẩn (ví dụ `python -I -P -m unittest discover -s 05_TEST -t .` với cấu trúc package rõ ràng). | **Medium** | VERIFIED |
| S08 | **`request_id` do caller cấp, không bị ràng buộc.** Chấp nhận U+2028/U+0085 (log injection), không có tính duy nhất/chống replay; `result_from_exception` tự ném `ValueError` nếu request_id xấu (lỗi bên trong đường xử lý lỗi) và ánh xạ MỌI exception thành `FAIL` (lỗi authorization sẽ thành FAIL thay vì DENIED). `run_id`/correlation phải do server sinh, không tin caller. | **Medium** | VERIFIED |
| S09 | **Enum trạng thái thiếu trạng thái không-kết-thúc.** `ToolStatus` chỉ có 7 trạng thái cuối. `python_status` cho run đang chạy/xếp hàng/đã hủy (`RUNNING`, `QUEUED`, `CANCELLED`) sẽ đi qua `normalize_status` và bị ánh xạ thành `FAIL` (theo code: ValueError → FAIL; cùng nhánh với mẫu `ok`→FAIL đã chạy). Poll giữa chừng sẽ báo FAIL sai, hoặc người ta thêm trạng thái ad-hoc để "chữa". | **Medium** | VERIFIED (nhánh code) / DESIGN |
| S10 | **Schema `python_*` chưa tồn tại**, nên chưa thể đánh giá injection thật. Yêu cầu tối thiểu cho schema: `entry_path` đã validate; KHÔNG nhận `args` tự do, `env`, `cwd`, `interpreter`, `-c`/`-m`; `timeout_s` có trần phía server (clamp, không tin tham số); không stdin; target test thuộc registry; `expected_source_sha256` bắt buộc. Cảnh báo: `artifact_validate` ("registered validators") và `sandbox_patch` cũng là bề mặt thực thi/ghi; validator registry phải là allowlist ID, không phải đường dẫn. | **Medium** | DESIGN |
| S11 | **TOCTOU và cross-agent code injection.** Sandbox dùng chung giữa Xu/Go/Cla; một agent ghi file giữa lúc agent khác "viết → chạy". Run phải thực thi **bản snapshot bất biến theo hash** (copy sang workdir riêng của run), và evidence phải ghi `source_sha256`; hash lệch ⇒ BLOCKED. | **Medium** | DESIGN |
| S12 | **IDOR trên run.** `python_status`, `python_output_read`, `execution_cancel` theo `run_id`: cần kiểm tra quyền sở hữu/Work, `run_id` không đoán được (≥128 bit), trả NOT_FOUND không phân biệt "không tồn tại" và "không có quyền". `python_output_read` có thể làm rò log của Work khác. | **Medium** | DESIGN |
| S13 | **Nguồn chỉ thị là paste chưa xác thực.** Tin nhắn giao việc (msg_aaa93ea4fa1b) có `source.type = ai_chat_paste`; câu "Authority: Vinh" nằm trong nội dung, không gắn xác thực mật mã. Với việc review thì rủi ro thấp, nhưng khi có `python_run`, chỉ thị thực thi/ghi không được đi theo kênh paste; dùng task có xác thực (`get_pending_tasks`/`submit_proposal`) hoặc xác nhận từ Vinh. | **Low–Medium** | OBSERVED |
| S14 | `bounded_limit` có tham số `default` không dùng; giới hạn chỉ theo số phần tử, không có trần byte/độ dài thành phần (một thành phần 1000 ký tự được chấp nhận; vượt giới hạn tên file của hệ thống). | **Low** | VERIFIED |
| S15 | Điểm tốt (Info): unknown status fail-closed (`ok` → FAIL); từ chối bool làm số; từ chối NUL/newline; từ chối `../`, tuyệt đối, drive, UNC, ADS (kể cả `::$DATA`); registry ghi rõ "dependency chưa có = BLOCKED, không phải PASS"; Core là nơi quyết định authorization; không có tool shell nào trong registry hiện tại. | Info | VERIFIED / OBSERVED |

---

## 4. Threat model rút gọn cho `python_run`

| Bề mặt | Tác nhân | Đường tấn công chính | Phòng thủ bắt buộc (không thể thay bằng validator) |
|---|---|---|---|
| Code do AI viết | AI bị prompt-inject / agent độc / bug | subprocess, socket, ctypes, ghi ngoài workdir, symlink/junction, đọc env/secrets | Cô lập OS (S01), FS read-only ngoài workdir riêng, không network, không secrets trong môi trường, low-privilege |
| Python startup | Kẻ ghi file vào Work | `sitecustomize.py`, `usercustomize.py`, `.pth`, `conftest.py`, file `os.py`/`json.py` che stdlib, `PYTHONSTARTUP/PYTHONPATH/PYTHONHOME` | Chạy `-I -P` (isolated, không thêm CWD vào sys.path), scrub env, interpreter/stdlib read-only |
| Tài nguyên | Vô tình/ác ý | loop vô hạn, fork bomb, RAM, disk, stdout flood, nhiều run song song | Wall-clock + CPU + RAM + PID + disk quota; kill cả cây (Job Object/cgroup); trần byte output |
| Mạng | Code chạy | Ra Internet, **gọi ngược Core :8000 / MCP :8020 qua localhost (bypass Core)**, metadata endpoint | Network namespace/không có NIC; chặn loopback tới host |
| Kết quả | Code chạy | In ra `{"status":"PASS"}` rồi exit 1; `sys.exit(0)` không chạy test; 0 test = "OK" | Trạng thái suy ra từ exit code + báo cáo có cấu trúc do wrapper tin cậy sinh; "Ran 0 tests" ≠ PASS |
| Evidence/Audit | Mọi agent có quyền ghi Sandbox | Ghi đè/xóa evidence, sửa run record | Evidence do Core/runtime ghi vào vùng AI không ghi; append-only/hash chain |
| Định danh | Agent giả mạo | `identity_id` do caller cung cấp | Principal lấy từ phiên xác thực, không từ body |

---

## 5. Negative-test matrix

Mỗi case: input/attack → expected status → evidence cần thu → rủi ro nếu lọt. "ACT" = kết quả thực tế nếu đã chạy trong container Cla (mục 2). Mọi case còn lại **NOT RUN / BLOCKED** (chờ tool + runtime thật). Không case nào được ghi PASS.

### A. Authorization / WorkContext

| ID | Attack / input | Expected | Evidence cần thu | Rủi ro nếu lọt | Trạng thái |
|---|---|---|---|---|---|
| A1 | `python_run` với identity thiếu/không đăng ký | DENIED; không tạo run_id; không có process | Audit record DENIED, không có entry runtime | Critical: chạy code ẩn danh | NOT RUN |
| A2 | Identity hợp lệ, Work không được cấp (ví dụ 22) | DENIED | Quyết định Core + audit; không có workdir được tạo | Critical | NOT RUN |
| A3 | Identity chỉ có quyền đọc yêu cầu chạy | DENIED (đọc ≠ thực thi) | Policy decision log | High | NOT RUN |
| A4 | `identity_id` trong body ≠ principal của phiên | DENIED/INVALID_REQUEST | Audit ghi cả hai giá trị | High: giả mạo | NOT RUN |
| A5 | WorkContext = Work 28 nhưng `entry_path` trỏ file Work 27 (hoặc đối số `work_id` lệch) | DENIED | Log so khớp work_id ↔ path root | High: chạy code của Work khác | NOT RUN |
| A6 | `python_status`/`output_read`/`cancel` bằng run_id của principal/Work khác | NOT_FOUND hoặc DENIED, phản hồi không phân biệt được | Hai phản hồi giống nhau về dạng; audit | High: rò log, hủy run người khác | NOT RUN |
| A7 | Liệt kê/đoán run_id tuần tự | Không đoán được; rate-limit | Định dạng run_id (≥128 bit), log rate-limit | Medium | NOT RUN |
| A8 | Gửi lại cùng `request_id` (replay) | Trả cùng run (idempotent) hoặc INVALID_REQUEST; không chạy lần hai | Số run theo request_id = 1 | Medium: chạy lặp, đầu độc evidence | NOT RUN |

### B. Đường dẫn / symlink

| ID | Attack / input | Expected | Evidence cần thu | Rủi ro nếu lọt | Trạng thái |
|---|---|---|---|---|---|
| B1 | `../x`, `a/../../x`, `..\x`, `a\..\..\x` | INVALID_REQUEST trước khi chạm FS | Không có syscall FS; mã lỗi | Critical | **ACT: rejected (đúng)** |
| B2 | `/etc/passwd`, `C:\x`, `C:x`, UNC, `f:s`, `f::$DATA`, NUL, newline | INVALID_REQUEST | Như trên | Critical | **ACT: rejected (đúng)** |
| B3 | Unicode: `．．/x`, `a／..／x`, `。。/x`, U+202E, U+200B, DEL, C1 | INVALID_REQUEST | Kết quả validator | High (chuẩn hóa Unicode phía FS/API) | **ACT: ACCEPTED (SAI)** |
| B4 | Tên thiết bị Windows `CON`, `a/NUL.txt`, `COM1`; thành phần kết thúc `.`/khoảng trắng (`.. /x`, `file.txt.`); `.../x` | INVALID_REQUEST | Kết quả validator | High: treo process, ghi vào thiết bị, bypass `..` | **ACT: ACCEPTED (SAI)** |
| B5 | `PROGRA~1/x`, `~/x`, `%USERPROFILE%/x`, `$HOME/x`, `*.py`, `a?b`, `.git/config`, `00_root/work_manifest.md` (khác hoa/thường) | INVALID_REQUEST / chuẩn hóa so khớp không phân biệt hoa/thường | Kết quả validator + so khớp allowlist | Medium–High | **ACT: ACCEPTED (SAI)** |
| B6 | Thành phần bắt đầu bằng `-` (ví dụ `-c`, `--version`) làm `entry_path` | INVALID_REQUEST | Argv thực tế của interpreter | High: argument injection | NOT RUN (theo code: sẽ được chấp nhận) |
| B7 | Run tạo symlink/junction/hardlink trong Work trỏ ra ngoài; sau đó `sandbox_read(link/file)` | DENIED; link không được tạo hoặc không được theo | Log containment realpath; file ngoài không bị đọc | High: đọc file host | NOT RUN / BLOCKED |
| B8 | Hoán file thành symlink giữa lúc validate và open (TOCTOU) | DENIED; mở bằng handle + O_NOFOLLOW/kiểm tra sau mở | Log kiểm tra sau mở | High | NOT RUN |
| B9 | Trong run: `open('/etc/passwd')`, `open('C:\\Users\\..')`, `os.listdir('..')`, `os.walk('/')` | Lỗi quyền/không tồn tại; không rò dữ liệu; status FAIL | stdout/stderr + audit FS của sandbox | Critical | NOT RUN / BLOCKED |

### C. Injection / thực thi

| ID | Attack / input | Expected | Evidence cần thu | Rủi ro nếu lọt | Trạng thái |
|---|---|---|---|---|---|
| C1 | Tham số/đường dẫn chứa `; calc`, `&& whoami`, `$(id)`, backtick, `\|` | Coi là chuỗi literal hoặc INVALID_REQUEST; không dùng `shell=True` | argv thực tế; không có process con ngoài interpreter | Critical | NOT RUN |
| C2 | Gửi `interpreter=cmd.exe/powershell/bash`, `args=["-c", "..."]`, `-m pip`, `-m http.server` | INVALID_REQUEST (trường không thuộc schema) | Phản hồi từ chối unknown field | Critical | NOT RUN |
| C3 | Ghi `sitecustomize.py`, `usercustomize.py`, `.pth`, `os.py`/`json.py`/`unittest.py` vào Work rồi `python_test` | Không được nạp; chạy `-I -P` | Danh sách module đã import (`sys.modules` path) | High | NOT RUN |
| C4 | `env` có `PYTHONSTARTUP`, `PYTHONPATH`, `PYTHONHOME`, `PATH`, `LD_PRELOAD` | INVALID_REQUEST; môi trường run bị scrub | `os.environ` được dump từ bên trong run | High | NOT RUN |
| C5 | Pytest: `conftest.py` độc, `-p plugin`, `PYTEST_ADDOPTS`, target có đối số thêm | Không nhận đối số thêm; target thuộc registry | argv runner | Medium–High | NOT RUN |
| C6 | Trong run: `subprocess.run`, `os.system`, `ctypes`, `os.startfile`, tạo scheduled task/registry/Startup | Không tác động host (cô lập) | Process tree + audit host trước/sau | Critical | NOT RUN / BLOCKED |
| C7 | `artifact_validate` với validator = đường dẫn/chuỗi lệnh | INVALID_REQUEST; chỉ nhận validator ID trong registry | Registry lookup log | High | NOT RUN |

### D. Tài nguyên / vòng đời

| ID | Attack / input | Expected | Evidence cần thu | Rủi ro nếu lọt | Trạng thái |
|---|---|---|---|---|---|
| D1 | `while True: pass` với timeout ngắn | TIMEOUT; cả cây tiến trình bị kill | PID trước/sau, không process mồ côi | High | NOT RUN |
| D2 | Process con tách rời (daemon/`Popen` detach) trước timeout | TIMEOUT; con cũng bị kill (Job Object KILL_ON_JOB_CLOSE/cgroup) | Danh sách process sau timeout | High: orphan, mining | NOT RUN |
| D3 | Fork bomb / vòng `Popen` | Chặn bởi trần PID; FAIL với lý do giới hạn | Số process đạt trần, host ổn định | High | NOT RUN |
| D4 | `bytearray(10**11)` | Bị kill bởi trần RAM; FAIL; host không swap | Log OOM của sandbox | High | NOT RUN |
| D5 | In 1 GB stdout/stderr, không newline, hoặc dòng 100 MB | Cắt ở trần byte (đánh dấu `truncated`), run bị kill/drain; Core không phình bộ nhớ | Kích thước log lưu, RSS của Core | High: DoS Core/MCP | NOT RUN |
| D6 | Ghi file 50 GB, hàng triệu file nhỏ, đệ quy thư mục sâu | Chặn bởi quota dung lượng/inode/độ sâu | Dung lượng workdir; ổ host không đầy | High | NOT RUN |
| D7 | `timeout_s=10**9` hoặc âm | Clamp về trần server hoặc INVALID_REQUEST | Timeout hiệu lực ghi trong evidence | Medium | NOT RUN |
| D8 | N run song song cùng Work, cùng ghi một file | Mỗi run workdir riêng; giới hạn đồng thời; không đọc chéo | Đường dẫn workdir riêng/run; kết quả độc lập | Medium | NOT RUN |
| D9 | `execution_cancel` giữa chừng | Cây tiến trình bị kill; trạng thái CANCELLED (cần bổ sung vào enum, xem S09) | PID trước/sau | Medium | NOT RUN |

### E. Mạng / package / secrets / host

| ID | Attack / input | Expected | Evidence cần thu | Rủi ro nếu lọt | Trạng thái |
|---|---|---|---|---|---|
| E1 | `socket.connect` ra Internet, DNS lookup, `urllib` | Bị chặn (network unreachable); FAIL | Log firewall/netns, lỗi trong stderr | High: exfiltration | NOT RUN / BLOCKED |
| E2 | Kết nối `127.0.0.1:8000` (Core) và `:8020` (MCP), `169.254.169.254`, dải LAN | Bị chặn | Log kết nối bị từ chối | **Critical: bypass Core, tự gọi tool với quyền cao hơn** | NOT RUN / BLOCKED |
| E3 | `pip install`, `python -m pip`, `ensurepip`, tải wheel | Bị từ chối; không có index | Lỗi + không có thay đổi site-packages | High: supply-chain | NOT RUN |
| E4 | Đọc `os.environ`, `.env`, `~/.ssh`, `~/.aws`, token MCP/Core, profile trình duyệt | Không tồn tại/không truy cập được | Canary token đặt ngoài workdir không bị đọc | Critical | NOT RUN |
| E5 | In canary secret đặt trong môi trường thử | Không có trong run; nếu lọt thì bị redact trước lưu và trước trả về | Canary không xuất hiện trong evidence/log/response | High | NOT RUN |
| E6 | Ghi ngoài Work: Startup folder, scheduled task, registry, `~/.bashrc` | DENIED/lỗi quyền; không persistence | Audit host trước/sau | Critical | NOT RUN / BLOCKED |

### F. Kết quả / evidence / audit

| ID | Attack / input | Expected | Evidence cần thu | Rủi ro nếu lọt | Trạng thái |
|---|---|---|---|---|---|
| F1 | Code `print('{"status":"PASS","exit_code":0}')` rồi `sys.exit(1)` | FAIL; status suy ra từ exit code runtime, KHÔNG parse stdout | Phản hồi FAIL + exit_code=1 | **High: PASS giả** | NOT RUN |
| F2 | `python_test` mà test bị skip hết, xóa hết, hoặc "Ran 0 tests", hoặc `sys.exit(0)` trước khi chạy | Không PASS (FAIL/BLOCKED); yêu cầu số test > 0 từ báo cáo có cấu trúc do wrapper tin cậy sinh | Báo cáo JUnit/JSON từ wrapper | High | NOT RUN |
| F3 | Dựng `ToolResult(status=PASS, evidence_ref=None)` / `normalize_status("pass")` | Bị từ chối ở tầng contract (PASS cần run_id + exit_code=0 + evidence_ref) | Unit test mới | High | **ACT: constructible (SAI)** |
| F4 | `RUNNING`/`QUEUED`/`CANCELLED` đi qua `normalize_status` | Giữ nguyên trạng thái không kết thúc | Unit test | Medium | **ACT (theo code): → FAIL (SAI)** |
| F5 | Stdout có ANSI escape, NUL, byte UTF-8 hỏng, dòng giả `STATUS: PASS` | Mã hóa an toàn, không phá JSON/log; không ảnh hưởng status | Phản hồi JSON hợp lệ | Medium | NOT RUN |
| F6 | `request_id` chứa U+2028/U+0085, quá dài, trùng lặp | INVALID_REQUEST hoặc server tự sinh ID | Log không bị xuống dòng giả | Medium | **ACT: U+2028/U+0085 accepted (SAI)** |
| F7 | `sandbox_write`/`sandbox_delete` vào bản ghi evidence của run | DENIED; vùng evidence không do AI ghi | Phản hồi DENIED + hash bản ghi không đổi | High: xóa/sửa dấu vết | NOT RUN (Cla không thử để tránh phá evidence thật; cần thử trên Work thử nghiệm) |
| F8 | Hai agent ghi cùng file giữa "viết" và "chạy" | Run chạy snapshot theo hash; hash lệch ⇒ BLOCKED | `source_sha256` trong evidence khớp bản đã ghi | Medium | NOT RUN |
| F9 | Kiểm tra audit đầy đủ cho mọi mutation và run | Có principal, Work, request_id, run_id, command ID, source hash, giới hạn áp dụng, thời gian, exit code, quyết định authorization | Bản ghi audit đọc lại được | Medium | NOT RUN |

---

## 6. Đánh giá tool contract/schema

**Câu hỏi 1 — Có vô tình mở unrestricted shell không?**
- Ở tầng tài liệu/schema hiện có: **KHÔNG** có tool shell/command-string nào (registry ghi rõ cấm). Kết luận: chưa có lỗ hổng trực tiếp.
- Nhưng: `python_run` nếu nhận `args`, `env`, `interpreter`, `-c`, `-m`, hoặc entry_path tự do thì thực chất mở shell. Và dù schema chặt, Python tùy ý vẫn tương đương shell nếu không cô lập OS (S01). Kết luận: **rủi ro cao, chưa có biện pháp trong thiết kế đủ để loại bỏ**; không được tuyên bố "không unrestricted shell" cho tới khi test C1–C7, E1–E6 chạy thật PASS.

**Câu hỏi 2 — Contract có cho phép PASS khi không có bằng chứng runtime thật không?**
- **CÓ** (S02, S09, F3): code hiện tại không cưỡng chế. Đã xác minh bằng thực thi.
- Đề xuất: `ToolResult` thành union theo trạng thái; PASS bắt buộc `run_id` (server sinh), `exit_code == 0`, `evidence_ref` hợp lệ, `source_sha256`, `runner_identity`; `normalize_status` không dùng cho dữ liệu từ downstream chưa kèm evidence; thêm `RUNNING/QUEUED/CANCELLED`.

---

## 7. Khuyến nghị (cho Xu / Vinh)

Thứ tự ưu tiên:
1. **Chốt cơ chế cô lập (S01) trước khi viết `python_run`.** Chọn rõ: container/WSL2/Windows Sandbox/VM; không network (kể cả loopback tới host); FS riêng cho mỗi run; non-root; giới hạn CPU/RAM/PID/disk/wall-clock; kill cả cây; scrub env; chạy `-I -P`.
2. **Chuyển "PASS cần evidence" từ văn bản sang code (S02, S09)** và thêm unit test tương ứng (F3, F4).
3. **Evidence do Core/runtime ghi, AI không ghi/xóa được (S04, F7).** Run record bất biến, có hash.
4. **Xác nhận authorization thực sự nằm ở đâu cho `sandbox_*` (S03).** Principal phải lấy từ phiên xác thực; kiểm tra thử trên Work thử nghiệm có chủ đích (không trên Work 22/27/28).
5. **Sửa validator (S06)** theo allowlist ký tự từng thành phần (ví dụ `^[A-Za-z0-9_][A-Za-z0-9._-]*$`, không kết thúc bằng `.`/khoảng trắng, không tên thiết bị Windows, không bắt đầu bằng `-`), và thêm lớp thứ hai bắt buộc: `realpath` + containment + từ chối reparse point/symlink + mở bằng handle (S05, B7, B8). Thêm các test B3–B6 vào `test_tool_contracts.py` (Xu sửa; Cla không sửa lượt này).
6. **Định nghĩa cách chạy test chuẩn và bố cục package (S07).**
7. **run_id/request_id do server sinh; kiểm tra quyền sở hữu run (S08, S12).**
8. Snapshot theo hash cho mỗi run (S11).
9. Chỉ chạy các case C/D/E/F/B7–B9 trên runtime cô lập thử nghiệm, có canary secret, trước khi bật cho Work thật.

**Điều kiện để chuyển các mục BLOCKED sang PASS:** tool `python_run` và các tool kèm theo xuất hiện trong live tool list; runtime canonical chạy được; mỗi case thu đủ evidence ở cột "Evidence cần thu"; ghi exit code và báo cáo runner.

---

## 8. Phi-tuyên-bố (explicit non-claims)

- Báo cáo này KHÔNG tuyên bố bất kỳ test runtime nào PASS. Các kết quả thực thi ở mục 2 chạy trong container riêng của Cla, không phải runtime canonical, và không tính cho G3/G4/G5.
- Cla KHÔNG thử tấn công hay thăm dò hệ thống live (không thử đọc/ghi Work khác, không thử ghi đè/xóa evidence, không thử path traversal qua `sandbox_*`). Các nhận định S03, S04 dựa trên bề mặt tool và tài liệu.
- Cla KHÔNG đọc source MCP :8020, Core :8000, W12/W13/Work 27; mọi đánh giá cần các nguồn này là BLOCKED.
- Cla KHÔNG sửa source Work 28. Chỉ tạo file báo cáo này theo biên bản phân công.
- Work 28 vẫn ACTIVE / NOT LOCKED.

---
**End of Cla Security Review Report**
Evidence của báo cáo: ghi bằng `sandbox_create`; readback xác nhận ngay sau khi ghi.
