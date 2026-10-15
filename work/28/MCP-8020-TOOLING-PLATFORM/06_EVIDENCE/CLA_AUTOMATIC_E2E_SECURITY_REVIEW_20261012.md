# CLA (Claude) — Automatic E2E Security Review — Work 28 — 2026-10-12

**Agent:** Cla (Claude, Anthropic) | **Yêu cầu bởi:** Ka (CSA) trong `KA_COORDINATION_HANDOFF_20261012.md`, được Vinh chỉ đạo
**Work:** 28 — MCP-8020-TOOLING-PLATFORM | **Status:** ACTIVE / NOT LOCKED
**Phạm vi lượt này:** review độc lập hợp đồng (contract 1.1.0), blueprint E2E rev 1.2, ma trận A01–A18, các phát hiện S01–S15 trước đó. KHÔNG ghi đè artifact của Ka; KHÔNG sửa source Work 28; KHÔNG thăm dò hệ thống live.
**Thời điểm:** 2026-10-12 (đồng hồ UTC chính xác không có trong phiên của Cla; báo cáo lập sau các artifact Ka ghi ngày 2026-10-12).

---

## 0. Kết luận bảo mật

**SECURITY NO-GO** cho việc đăng ký/bật `python_run` và các tool thực thi. Cla ĐỒNG Ý với NO-GO của Ka ở `KA_WP0_SOURCE_BOUNDARY_MAP` và bổ sung các blocker mới có bằng chứng thực thi.

Ba điều quan trọng nhất:
1. **Khái niệm "trusted test summary" hiện không đứng vững.** Test do AI viết, chạy trong cùng tiến trình với bộ chạy test, có thể làm cho `unittest` báo OK/0 failures dù test fail, hoặc in sẵn một bản tóm tắt giả rồi thoát exit 0. Đã chứng minh bằng thực thi (X4, X5). Hợp đồng hiện chấp nhận các con số giả đó thành `PASS` (X6). Với kiến trúc hiện tại, `PASS` chỉ có nghĩa là "code do AI viết tự khai là đạt", không phải bằng chứng độc lập.
2. **Cổng PASS-cần-evidence có thể bị vô hiệu bằng cách khai sai `operation_kind`** (mặc định là `READ`): kết quả thực thi khai là `READ`/`DIAGNOSTIC`/`MUTATION` vẫn tạo được `PASS` không cần evidence (X3). Đây là fail-open theo mặc định.
3. **Cô lập OS vẫn chưa được chứng minh** (S01, Critical) và source WP0 cho thấy `real_host.py` kế thừa môi trường và không có sandbox OS; `execution_host/server.py` nhận `authorized` do caller gửi. Nếu handler đó đang lắng nghe trên PC (chưa biết), code chạy trong run có thể gọi nó và đi vòng qua Core — kể cả khi MCP không bao giờ đăng ký `python_run` (xem N08).

Tiến bộ thật của Ka (đã kiểm chứng bằng thực thi): lệnh test chuẩn chạy được không cần PYTHONPATH (exit=0, 17 test OK), trạng thái vòng đời QUEUED/RUNNING/CANCELLED, ID server sinh, validator đường dẫn chặt hơn nhiều.

---

## 1. Phạm vi đã đọc (sandbox_read thành công)

`06_EVIDENCE/KA_COORDINATION_HANDOFF_20261012.md`, `KA_WP0_SOURCE_BOUNDARY_MAP_20261012.md`, `KA_CONTRACT_HARDENING_CHECKPOINT_20261012.md`, `PC_READONLY_RUNTIME_EVIDENCE_REQUEST_20261012.md`; `03_ARCHITECTURE/PROPOSED_EXECUTION_TOOL_CONTRACT_V1.md`, `WORK_28_AUTOMATIC_E2E_BLUEPRINT.md`; `04_CODE/tool_contracts.py`, `04_CODE/__init__.py`; `05_TEST/test_tool_contracts.py`, `05_TEST/__init__.py`; cùng bộ tài liệu đã đọc ở lượt trước (báo cáo của Go và của Cla).
Chưa đọc: `KA_WORK28_DECISION_NEXT_STEPS_20261011.md`, `05_TEST/WORK_28_TEST_PLAN.md` (bản cập nhật, nếu có), source thật trong GitHub/PC (Cla không có quyền truy cập GitHub/PC trong phiên này). Mọi nhận định về `execution_host/*`, `wee/*` dựa trên bản đồ WP0 của Ka, **không** do Cla tự đọc source: BLOCKED cho phần xác minh độc lập.

---

## 2. Bằng chứng thực thi (executed)

**Môi trường:** container riêng của Cla, Python 3.12.3, Linux. KHÔNG phải runtime canonical (W12/W13/Work 27). Không tính cho G3/G4/G5/G6.
**Cách dựng:** chép nguyên văn nội dung `tool_contracts.py` và `test_tool_contracts.py` từ readback Sandbox sang `04_CODE/` và `05_TEST/`; `__init__.py` dựng là file rỗng (bản thật chứa một docstring, không đổi hành vi). Không có công cụ để chứng minh bản chép giống từng byte với bản trong Sandbox; sha256 của bản chép `tool_contracts.py`: `25b1e6856929f8a849346842daaaa23ade11242537d68a23006504ea4df90f3b`. Số dòng ở mục 4 lấy từ bản chép này.

| # | Lệnh / thao tác | Kết quả | Exit |
|---|---|---|---|
| X1 | `python -m unittest discover -s 05_TEST -t . -v` (lệnh chuẩn Ka ghi, chạy từ root) | Ran 17 tests, OK | **0** |
| X2 | Probe validator đường dẫn (31 đầu vào) | Xem N06 | 0 |
| X3 | Probe `ToolResult` PASS gate (9 cấu hình) | Xem N01, N03, N05 | 0 |
| X3b | Probe `result_from_exception` (9 exception) | Xem N04 | 0 |
| X4 | `python -m unittest test_a_silence` (test fail thật nhưng module tự vô hiệu `TestResult.addFailure`) | In `Ran 1 test … OK` | **0** |
| X5 | `python -m unittest test_b_fake_summary` (in sẵn "Ran 20 tests … OK" rồi `os._exit(0)`) | Output giống một lần chạy 20 test thành công | **0** |
| X5c | Đối chứng: test fail thật, không can thiệp | `FAILED (failures=1)` | **1** |
| X5d | X4 chạy lại với `python -I -P -m unittest discover -s forge -p test_a_silence.py` | Vẫn `OK` | **0** |
| X6 | Dựng `ToolResult` PASS/RUN_TESTS với đúng các con số giả của X4 (`tests_run=1, failures=0, errors=0`) | **Được chấp nhận** | 0 |
| X7 | `cla_red_tests.py` (15 test kỳ vọng hành vi an toàn) chạy trên contract 1.1.0 | `FAILED (failures=24, errors=1)`; **15/15 test không pass** | **1** |
| X7b | Bộ test của Ka trên cùng bản chép, chạy lại sau X7 | Ran 17 tests, OK | **0** |

Ghi chú trung thực: lần thử đầu của X5d (`-I -P -m unittest test_a_silence`) cho exit=1 do lỗi import (`-I -P` bỏ CWD khỏi `sys.path`); đó không phải kết quả hợp lệ nên đã làm lại đúng cách bằng `discover`. `cla_red_tests.py` được lưu ở `06_EVIDENCE/CLA_PROPOSED_RED_TESTS_20261012.py` (bản trong Sandbox thêm đoạn docstring đầu file so với bản đã chạy; sha256 ghi trong docstring là của bản chạy trong container).

---

## 3. Tình trạng các phát hiện trước (S01–S15)

| ID | Nội dung rút gọn | Tình trạng sau bản vá 1.1.0 |
|---|---|---|
| S01 | Python = shell; cần cô lập OS | **MỞ — Critical.** Blueprint đã nêu yêu cầu; chưa có cơ chế hay bằng chứng. WP0 cho thấy host hiện có không đáp ứng. |
| S02 | PASS không cần evidence | **MỞ MỘT PHẦN.** Chỉ chặn khi `operation_kind=EXECUTION` (N01); counters/field lỏng (N03); summary giả được (N02). |
| S03 | Sandbox API không có principal | **MỞ — chưa kiểm chứng.** Ka cũng ghi nhận (WP0 §3.7). |
| S04 | Evidence ghi đè/xóa được | **MỞ.** Thiết kế đúng (blueprint Stage 4) nhưng chưa có triển khai. Cla không ghi đè file của Ka. |
| S05 | Symlink/junction do run tạo | **MỞ (thiết kế).** A06 chỉ nói tới adapter; chưa phủ trường hợp link do run tạo (A23 đề xuất). |
| S06 | Validator lỗ hổng | **ĐÃ SỬA PHẦN LỚN, còn tồn đọng** (N06). Đã đóng: DEL/C1, bidi/zero-width, fullwidth, tên thiết bị Windows, dấu chấm/khoảng trắng cuối, `~`, `%VAR%`, `$`, glob, `-`, `.git/.ssh` v.v. |
| S07 | Test không chạy theo bố cục | **ĐÃ SỬA, đã kiểm chứng (X1).** |
| S08 | request_id lỏng | **SỬA MỘT PHẦN.** ID chặt + generator server (đã kiểm chứng); nhưng đường xử lý lỗi vẫn ném exception khi request_id sai (N04) và vẫn do caller cung cấp nếu adapter không dùng `new_request_id()`. |
| S09 | Thiếu RUNNING/QUEUED/CANCELLED | **ĐÃ SỬA** (test trong X1). |
| S10–S12 | Schema `python_*`, TOCTOU, IDOR | **THIẾT KẾ TỐT HƠN** (contract V1 §2, blueprint Stage 2/1); chưa triển khai; xem N07 cho điểm hở của hash. |
| S13 | Chỉ thị qua paste | Không đổi; Ka đã đưa giao việc qua file có tên người nhận. |
| S14 | `bounded_limit` default | **ĐÃ SỬA** (default dùng và được kiểm tra). |

---

## 4. Phát hiện mới

Severity: Critical / High / Medium / Low. Trạng thái: VERIFIED (đã thực thi trong container Cla, X-số), STATIC (đọc nguồn/tài liệu), BLOCKED (cần runtime/source thật).

### N01 — High — Cổng "PASS cần evidence" chỉ bật khi tự khai là EXECUTION (fail-open mặc định) — VERIFIED (X3)
- Nguồn: `04_CODE/tool_contracts.py` dòng 58 (`operation_kind` mặc định `READ`), dòng 78 (điều kiện `operation_kind == EXECUTION`).
- Hiện tượng: `ToolResult("req-1", PASS, "x")` hợp lệ; `operation_kind=DIAGNOSTIC` + `execution_operation=RUN_TESTS` + PASS không evidence hợp lệ; `MUTATION` PASS không cần readback/hash. Lỗi lập trình ở adapter (quên khai EXECUTION, hoặc chuyển trạng thái từ chuỗi do runtime trả qua `normalize_status`) sẽ ra PASS giả mà không bị chặn.
- Hành vi mong đợi: các trường thực thi (`run_id`, `exit_code`, `test_summary`, `execution_operation`) chỉ hợp lệ khi `operation_kind == EXECUTION`; kiểu kết quả thực thi riêng (ví dụ `ExecutionResult`) để tool `python_*` không thể trả `ToolResult` thường; PASS của `MUTATION` yêu cầu readback + hash trước/sau (đúng yêu cầu của test plan).
- Test đề xuất: `N01_*` trong `CLA_PROPOSED_RED_TESTS_20261012.py` (đang đỏ).

### N02 — High (nền tảng) — "Trusted test summary" bị giả mạo được bởi code trong tiến trình — VERIFIED (X4, X5, X5d, X6)
- Nguồn thiết kế: `PROPOSED_EXECUTION_TOOL_CONTRACT_V1.md` §2 (`python_run`, "trusted test summary") và blueprint Stage 5; code: `tool_contracts.py` dòng 85–98.
- Hiện tượng: test và code cùng do AI viết, cùng chạy trong tiến trình của bộ chạy test. (a) Module test tự thay `unittest.TestResult.addFailure` → test fail nhưng báo OK, exit 0 (X4). (b) Module in sẵn bản tóm tắt giả rồi `os._exit(0)` (X5): nếu wrapper phân tích stdout/stderr, nó thấy "Ran 20 tests OK". (c) `-I -P` không giúp (X5d). Các con số giả được `ToolResult` chấp nhận (X6). Pytest có cùng lớp rủi ro qua `conftest.py`/hook (chưa chạy; STATIC).
- Hậu quả: A08/A09/A18 chỉ bắt được lỗi "ngây thơ", không bắt được code cố ý giả. Mục tiêu của Vinh (AI tự chạy, sửa, chạy lại) vẫn khả thi, nhưng PASS phải được định nghĩa đúng.
- Hành vi mong đợi (chọn một hoặc kết hợp): (1) tóm tắt do wrapper tin cậy sinh ra **ngoài** tiến trình chạy code (ví dụ mỗi test file chạy trong tiến trình con; parent thu exit code/JUnit qua kênh mà code không ghi đè được), kết hợp kiểm tra số test khám phá được từ bên ngoài (đếm trước bằng AST/collect-only trong tiến trình riêng); (2) acceptance dựa trên test do Core giữ (held-out, AI không sửa được); (3) ít nhất ghi rõ trong response `summary_provenance: "self-attested-by-untrusted-code"` và không dùng để mở cổng G5/G6.
- Acceptance bổ sung: A19 (mục 5).

### N03 — High — Kiểm tra PASS còn lỏng, và thiếu trường để cưỡng chế A07/A15 — VERIFIED (X3)
- `tool_contracts.py` dòng 95: `test_summary.get(counter, 0)` → thiếu `failures`/`errors` được coi là 0 (summary `{"tests_run": 3}` → PASS). Tất cả test bị skip vẫn PASS (không xét `skipped`, `expectedFailures`, `unexpectedSuccesses`). Dòng 82: `self.exit_code != 0` chấp nhận `False` và `0.0`. `run_id`, `evidence_ref` là chuỗi tự do ("x" hợp lệ). `source_sha256` hợp lệ về dạng nhưng không so với `expected_source_sha256`. Hợp đồng V1 yêu cầu `runtime_identity`, `work_id`, `started_at`, `finished_at`, `stdout_ref`, `stderr_ref` trong response; `ToolResult` không có các trường này, nên PASS không thể gắn với runtime (A15) hay Work (A04).
- Hành vi mong đợi: summary đủ trường bắt buộc, kiểu `int` thật; `tests_executed = tests_run − skipped ≥ 1`; `exit_code` kiểu int thật (không bool/float); `run_id` đúng dạng `run-<32 hex>` do server sinh; `evidence_ref` đúng định dạng của kho evidence được bảo vệ; thêm các trường runtime/Work/thời gian.

### N04 — Medium — `result_from_exception` tạo oracle tồn tại và gán nhãn sai — VERIFIED (X3b)
- Nguồn: `tool_contracts.py` dòng 197–211.
- `PermissionError → DENIED` và `FileNotFoundError → NOT_FOUND` cho phép phân biệt "run tồn tại nhưng không có quyền" với "không tồn tại" — mâu thuẫn với `python_status` ("indistinguishable NOT_FOUND"). `TimeoutError → TIMEOUT` nhưng `subprocess.TimeoutExpired → FAIL` (không nhất quán), và `TIMEOUT` theo A11 chỉ hợp lệ sau khi có bằng chứng dọn cây tiến trình; timeout RPC tới runtime không chứng minh điều đó. `json.JSONDecodeError`/`UnicodeDecodeError` (phản hồi runtime hỏng) → `INVALID_REQUEST` (đổ lỗi cho caller), trong khi A18 yêu cầu FAIL/BLOCKED. Lỗi từ chính cổng PASS (`ValueError` do thiếu evidence) cũng thành `INVALID_REQUEST`. `PermissionError` của hệ điều hành (ACL sai) bị gọi là `DENIED` như một quyết định chính sách. Đường lỗi vẫn ném `ValueError` khi `request_id` sai (dòng 199) → lỗi bên trong xử lý lỗi.
- Mong đợi: ánh xạ do tầng Core quyết định theo ngữ cảnh (không suy từ loại exception hệ thống); ngoài tầng đó dùng `BLOCKED/FAIL` an toàn; đường lỗi luôn trả kết quả với ID server sinh.

### N05 — Medium — `test_summary` (dict) thay đổi được sau khi đã kiểm tra — VERIFIED (X3)
- Dataclass `frozen=True` nhưng `test_summary: dict` (dòng 62) là tham chiếu; sau khi kiểm tra có thể đặt `tests_run=0` mà `to_dict()` vẫn trả `status=PASS`.
- Mong đợi: sao chép sâu và đóng băng (ví dụ `MappingProxyType`/tuple) trong `__post_init__`.

### N06 — Medium — Validator đường dẫn: tồn đọng sau bản vá — VERIFIED (X2)
- Vẫn chấp nhận: `.env.local`, `.envrc`, `.git-credentials`, `.npmrc`, `.netrc`, `.pypirc`, `id_rsa`, `credentials` (danh sách `_PROTECTED_COMPONENTS` ở dòng 23 chỉ có 7 tên và so khớp nguyên tên); U+2028, U+2029, U+1680 (NFKC không biến đổi, danh mục `Zl/Zp/Zs` không bị chặn ở dòng 144); chữ Cyrillic lẫn Latin (`аdmin`) — NFKC xử lý tương thích, không xử lý confusable, nên chú thích "confusable" ở dòng 142 nói quá; `a\b` bị đổi thành `a/b` (dòng 155) làm đổi nghĩa trên POSIX; `desktop.ini`, `System Volume Information`, `COM0`, `CON .txt`, tên 300 ký tự (theo byte NAME_MAX); các tên kích hoạt khi khởi động Python (`sitecustomize.py`, `usercustomize.py`, `conftest.py`, `os.py`, `*.pth`, `.pyc`) và `run.exe` (validator từ vựng không thể biết; cần chặn ở tầng runtime/entry_path allowlist `.py`).
- Cần lưu ý: tên tiếng Việt dạng NFD (ví dụ từ macOS/nhập liệu khác) bị từ chối (dòng 139) — đúng hướng fail-closed nhưng ảnh hưởng người dùng; hãy chuẩn hóa NFC ở biên MCP thay vì từ chối, hoặc chấp nhận có chủ đích.
- Mong đợi: allowlist ký tự theo từng thành phần thay vì denylist; entry_path chỉ `.py`; kiểm tra containment thật ở adapter (S05); danh sách bảo vệ mở rộng + áp dụng ở tầng quyền (không chỉ từ vựng).

### N07 — High (thiết kế) — Hash nguồn có thể chỉ phủ file vào, không phủ cây được thực thi — STATIC
- Blueprint Stage 2 và V1 §2 dùng một `expected_source_sha256`. Nếu đó là hash của `entry_path`, thì module import, `conftest.py`, `sitecustomize.py`, `*.pth`, file cùng thư mục (che stdlib) nằm trong snapshot nhưng không được ràng buộc; "hash khớp" cho cảm giác an toàn sai.
- Mong đợi: hash của **toàn bộ manifest snapshot** (đường dẫn + hash từng file, sắp xếp ổn định), có giới hạn kích thước/số file; evidence ghi manifest.

### N08 — Critical (thiết kế/triển khai) — Host thực thi thay thế có thể tiếp cận được từ chính code đang chạy — STATIC / BLOCKED
- Cơ sở: WP0 ghi `execution_host/server.py` nhận `POST /execute` với `WorkContext.authorized` do caller gửi và không có xác thực hiển thị; `real_host.py` kế thừa môi trường và không có sandbox OS; `security.py` cho phép `-c`. Yêu cầu đọc-PC của Ka có liệt kê cổng 8031 (tài liệu tôi đọc **không** nêu cổng của host thay thế; không suy ra là chắc chắn).
- Rủi ro: nếu handler đó đang chạy trên PC (kể cả chỉ trên loopback), bất kỳ code nào chạy trên máy đó — gồm Python do AI viết — có thể gọi nó với `authorized=true` và chạy lệnh ngoài mọi cô lập của Work 28, vượt Core. Đây là rủi ro hiện hữu, độc lập với việc có đăng ký `python_run` hay không.
- Hành vi mong đợi: xác nhận handler có đang lắng nghe không và bind ở địa chỉ nào (lệnh của Ka đã ghi `LocalAddress`); nếu có thì vô hiệu hóa/đặt sau xác thực trước mọi bước khác; sandbox của run phải chặn mọi loopback/LAN (A12, A28).

### N09 — Medium (thiết kế) — Runtime tự khai danh tính và hồ sơ cô lập — STATIC
- Blueprint Stage 3: "Runtime must attest build identity and OS isolation profile." Tự khai không phải bằng chứng; runtime cũ/bị chiếm quyền vẫn khai đúng.
- Mong đợi: Core giữ hash build và hồ sơ cô lập mong đợi (cấu hình ghim), kiểm tra độc lập hoặc qua chứng thực có chữ ký; trình ghi evidence chạy ở danh tính OS khác, ngoài ranh giới của tiến trình không tin cậy; khóa ký evidence không nằm trong môi trường của run.

### N10 — Medium (thiết kế) — Ma trận A01–A18 thiếu các trường hợp quan trọng — STATIC
Xem mục 5 (A19–A30).

### N11 — Low — Kỷ luật phiên bản — VERIFIED
- `CONTRACT_VERSION = "1.1.0"` (dòng 16) và test ghim `1.1.0`, nhưng checkpoint của Ka nói "Contract 1.2 follow-up" thêm `ExecutionOperation` bắt buộc (thay đổi siết chặt, tương thích ngược bị phá). Cần bump phiên bản và ghi vào tài liệu tương thích.

### N12 — Low–Medium — Yêu cầu đọc-PC không hoàn toàn "read-only" — STATIC
- `git status` có thể làm mới index (ghi `.git/index`, khóa) và có thể chạy lệnh cấu hình bởi repo (`core.fsmonitor`). Nên dùng `git --no-optional-locks -c core.fsmonitor=false -C $repo status --short`. Thêm vào đầu ra: kiểm tra có tiến trình nào của host thay thế (N08) và chính sách tường lửa, không in đối số dòng lệnh (Ka đã quy định).

### Ghi nhận tích cực (đã kiểm chứng)
Lệnh test chuẩn chạy được (X1); lifecycle status; `ToolResult` chặn PASS EXECUTION thiếu evidence/0 test/exit≠0 khi khai đúng kiểu; ID server sinh ≥128 bit entropy (`token_hex(16)`); validator chặn traversal/UNC/ADS/Unicode fullwidth/bidi/zero-width/tên thiết bị/dấu chấm cuối/`-`/`~`/`%`/`$`; exception không rò chi tiết trong message; WP0 trung thực, không đăng ký tool khi chưa có bằng chứng.

---

## 5. Đánh giá ma trận A01–A18 và đề xuất bổ sung

Tất cả: **BLOCKED** (chưa có tool/runtime live; không case nào được Cla chạy trên runtime thật).

| ID | Nhận xét review tĩnh | Bổ sung bắt buộc |
|---|---|---|
| A01 | Đủ về ý, nhưng PASS phụ thuộc N02/N03. | Thêm đối chứng giả mạo (A19). |
| A02 | Thiếu: cơ chế truyền principal đáng tin hiện chưa xác định (S03). | Ghi rõ transport xác thực. |
| A03 | "Ignored" nên là **từ chối trường lạ** (INVALID_REQUEST) + audit, không im lặng bỏ qua. | Test `authorized`, `identity_id`, `work_id`, `principal` trong body. |
| A04 | Cần chứng minh **không phân biệt được** (nội dung, độ dài, thời gian). | Đo thời gian; đối chiếu N04. |
| A05 | Mức từ vựng đã chứng minh một phần (X1/X2); phải chạy lại trên adapter thật theo từng hệ điều hành. | Bộ N06. |
| A06 | Thiếu: link/junction do **run tạo ra** rồi đọc qua Sandbox API; hoán thư mục giữa kiểm tra và mở; sao chép kết quả ngược vào Work. | A23. |
| A07 | Cần hash cả cây (N07). | A24. |
| A08 | Chỉ bắt lỗi ngây thơ (N02). | A19. |
| A09 | Không đủ nếu runner chạy trong tiến trình của code (N02). | A19. |
| A10 | Đủ. | — |
| A11 | Thêm: cháu bị tách, double-fork, thoát khỏi Job Object (Windows), trạng thái "dọn dẹp chưa xong". | A26. |
| A12 | Thêm: cổng 8000/8020/8031 và mọi host thực thi thay thế, `::1`, UDP/DNS, named pipe, metadata IP; canary secret trong môi trường của host. | A28. |
| A13 | Thêm: số inode/file, đệ quy sâu, hạn mức theo principal. | A21. |
| A14 | Thêm: danh tính của tiến trình run cũng không ghi được; ghi qua symlink/traversal tới thư mục evidence. | A25. |
| A15 | Thêm: runtime cũ nhưng "hợp lệ", runtime nói dối; kiểm tra không có kết nối thử tới host thay thế. | N09. |
| A16 | Tốt; cần Work thử nghiệm với identity chỉ có quyền Work đó. | — |
| A17 | Thêm: cancel sau khi đã xong, cancel hai lần, đua trạng thái. | A29. |
| A18 | Thêm: JSON cắt cụt, khóa trùng, kiểu sai (`exit_code:"0"`), NaN, `"pass"` viết thường, payload cực lớn. | Bộ N03/N04. |

**Đề xuất thêm A19–A30:**
- **A19** Giả mạo kết quả test từ trong tiến trình (X4/X5: vá `addFailure`, in tóm tắt giả + `os._exit(0)`, `conftest.py` đổi outcome) → không thể ra PASS; summary phải do wrapper ngoài tiến trình sinh.
- **A20** Replay `request_id`/idempotency → một lần chạy duy nhất.
- **A21** Đoán/liệt kê `run_id`; hạn mức và công bằng hàng đợi theo principal.
- **A22** Móc khởi động Python và che stdlib (`sitecustomize.py`, `usercustomize.py`, `.pth`, `os.py`, `conftest.py`, biến `PYTHON*`), interpreter flags cố định.
- **A23** Run tạo symlink/junction/hardlink → đọc qua Sandbox API; kiểm tra khi sao chép kết quả ngược vào Work.
- **A24** Hoán file phụ (module import, `conftest.py`) giữa lúc tính hash và lúc chạy → hash cây lệch ⇒ BLOCKED trước khi tạo tiến trình.
- **A25** Trình ghi evidence/khóa ký không với tới được từ danh tính của run.
- **A26** Trạng thái "kết thúc nhưng dọn dẹp chưa xong" → BLOCKED + cách ly + cảnh báo; không PASS/TIMEOUT.
- **A27** `entry_path` không phải `.py` (`.pyc`, `.exe`, `.pyz`, `.zip`) → INVALID_REQUEST.
- **A28** Từ trong run, gọi `POST /execute` của host thay thế (mọi cổng/địa chỉ) hoặc Core :8000 / MCP :8020 → bị chặn.
- **A29** Đua trạng thái giữa status/output/cancel và kết thúc run.
- **A30** DoS nhiều principal: bão hòa CPU/RAM/đĩa/hàng đợi không ảnh hưởng run khác.

---

## 6. Phán quyết theo cổng (gate)

| Cổng | Cla | Ghi chú |
|---|---|---|
| G2 — schema/policy contract | **FAIL (cần sửa)** | N01, N02, N03 cần xử lý; N04–N07 nên sửa trước khi review lại. |
| G3 — test chạy bằng approved runner | **BLOCKED** | X1 chạy ngoài runtime canonical; chỉ có giá trị tham khảo. |
| G4 — authorization/path/cô lập OS | **BLOCKED** | S01, S03, S05, N08 chưa có bằng chứng. |
| G5 — MCP → Core → runtime → evidence được bảo vệ | **BLOCKED** | Chưa có route, principal, runtime, evidence. |
| G6 — E2E tự động đầy đủ | **BLOCKED** | |
| **Quyết định bảo mật** | **NO-GO** | Hiệu lực cho tới khi các điều kiện mục 7 có bằng chứng. |

---

## 7. Điều kiện để Cla review lại (theo thứ tự ưu tiên)

1. **Xác minh N08 ngay (chỉ đọc):** có tiến trình nào của `execution_host` đang lắng nghe không, bind ở đâu; nếu có thì vô hiệu hóa hoặc đặt sau xác thực. Dùng lệnh sửa theo N12.
2. **Định nghĩa lại PASS (N02):** chọn mô hình tóm tắt tin cậy (wrapper ngoài tiến trình hoặc test do Core giữ); ghi vào hợp đồng; thêm A19.
3. **Sửa hợp đồng (N01, N03, N05, N04, N11):** làm cho `CLA_PROPOSED_RED_TESTS_20261012.py` xanh (15/15) mà vẫn giữ 17/17 test của Ka xanh; bổ sung các trường runtime/Work/thời gian.
4. **Sửa validator (N06)** và thêm kiểm tra containment thật ở adapter (không phải lexical).
5. **Hash cây (N07)** và các trường hợp A22–A24.
6. **Cô lập OS và evidence được bảo vệ (S01, S04, N09):** chọn cơ chế, có hồ sơ cô lập được Core ghim; ghi evidence từ danh tính khác.
7. **Chạy lại test bằng approved runner** khi có (G3), kèm lệnh, exit code, run_id; sau đó Go chạy E2E.

Cla sẵn sàng viết bản vá đề xuất cho các mục 3–4 trong một file riêng (không ghi đè của Ka) nếu Vinh/Ka yêu cầu.

---

## 8. Phi-tuyên-bố

- Không có kết quả nào trong báo cáo này là PASS của gate; mọi gate đều BLOCKED hoặc FAIL.
- Kết quả X1–X7 chạy ở container riêng của Cla, trên bản chép nguyên văn từ readback (không chứng minh được giống từng byte với Sandbox); không phải runtime canonical.
- Cla không đọc source GitHub/PC; nhận định N08, N09 dựa trên bản đồ WP0 của Ka và là STATIC/BLOCKED. Khả năng host thay thế đang chạy là chưa biết.
- Cla không thăm dò hệ thống live, không ghi đè/xóa artifact của Ka, không sửa source Work 28; chỉ tạo hai file: báo cáo này và `CLA_PROPOSED_RED_TESTS_20261012.py`.
- Work 28 vẫn ACTIVE / NOT LOCKED; Vinh giữ quyền quyết định cuối.

---
**End of Cla Automatic E2E Security Review**
