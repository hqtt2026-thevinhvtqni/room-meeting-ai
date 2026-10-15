# BIÊN BẢN REVIEW ĐỘC LẬP — Trust Boundary, F1, F3
Ngày: 2026-10-15 (+07)
Work: 28 / MCP-8020-TOOLING-PLATFORM
Người review: Cla (CTO) — reviewer độc lập
Người nhận / hoàn thiện: Ka (CSA)
Chế độ: STATIC-ONLY (chỉ đọc source qua Room Hop Sandbox; KHÔNG chạy code, KHÔNG truy cập PC)

## 1. Kết luận (disposition)
| Hạng mục | Kết luận của Cla |
|---|---|
| Trust boundary (tool_contracts 1.3.0) | NOT PROVEN. Ở mức hợp đồng dữ liệu, TrustedPrincipal/WorkContext/AuthorizedSandboxRequest có thể bị giả mạo trong tiến trình; PASS gate của ToolResult do bên tạo tự khai. |
| F1 (race / symlink / TOCTOU) | NOT PASS. Đã có hardening đáng kể nhưng còn lỗ hổng chưa đóng (đặc biệt trên Windows) và chưa có test nào cho collector. |
| F3 (provenance chưa xác thực) | BLOCKED — đồng ý với Nu. Bổ sung thêm các điểm ở verifier (mục 4). |
| E2E-Automatic / release | NO-GO (giữ nguyên). |

Không có PASS nào được cấp trong biên bản này.

## 2. Bằng chứng đã đọc (qua MCP Sandbox, Work 28)
Đọc đủ nội dung, không có SHA-256 (connector không cung cấp):
- 04_CODE/tool_contracts.py (CONTRACT_VERSION 1.3.0)
- 04_CODE/pc_readonly_source_collector.py (pc-readonly-collector/0.2.0)
- 04_CODE/source_snapshot_contract.py (0.1.1)
- 04_CODE/source_snapshot_import_verifier.py (verifier 0.1.0)
- 06_EVIDENCE/GO_STATIC_SOURCE_INSPECTION_20261015_0855.md
- 06_EVIDENCE/NU_FINDING_REMEDIATION_F1_F3_F7_F8_20261015_0840.md

## 3. Trust boundary — phát hiện
TB-1 (CAO) TrustedPrincipal giả mạo được. `source` chỉ bị chặn bởi denylist 4 chuỗi ("caller", "client", "user-supplied", "identity_id"). Chuỗi bất kỳ khác ("request", "header", "body", hoặc "core-session" do chính caller tự điền) đều qua. Bất kỳ code nào import module đều tạo được `TrustedPrincipal("admin", "core-session")`. Docstring nói "adapter MUST derive" nhưng không có cơ chế kỹ thuật buộc điều đó.
  Yêu cầu: dùng allowlist (enum) các nguồn transport; chỉ adapter giữ capability/factory để tạo principal (token nội bộ không export, hoặc Core-issued và được xác minh); thêm test chứng minh code ngoài adapter không tạo được principal hợp lệ.

TB-2 (CAO) WorkContext / AuthorizedSandboxRequest tự cấp quyền. `allowed_operations` là chuỗi tự do (không kiểm tra thuộc SandboxOperation), do chính caller xây; `AuthorizedSandboxRequest` chỉ kiểm tra thao tác nằm trong tập mà caller vừa khai. Không có ràng buộc với grant do Core cấp (không chữ ký, nonce, hạn dùng, không đối chiếu principal–work_id với nguồn thật). Tên "Authorized" gây hiểu nhầm.
  Yêu cầu: adapter phải dựng WorkContext từ tra cứu Core server-side và đối chiếu lại principal + work_id trên MỖI request; kiểm tra `allowed_operations ⊆ SandboxOperation`; đổi tên hoặc ghi rõ "ShapeValidated…" cho đến khi có enforcement.

TB-3 (CAO) PASS gate của ToolResult là tự khai. Gate kiểm tra hình dạng (run_id dạng run-<32hex>, exit_code==0 kiểu int, evidence_ref chuỗi không rỗng, source_sha256 đúng định dạng, bộ đếm). Không có sổ đăng ký run_id đã phát, không xác minh evidence_ref tồn tại, không chứng thực từ runner. Mọi code tự dựng được một ToolResult PASS hợp lệ. Vì vậy PASS gate không thay thế được bằng chứng runner thật (khớp với trạng thái BLOCKED hiện tại).
  Yêu cầu: PASS thực thi chỉ được phát từ runner đã phê duyệt kèm attestation (chữ ký hoặc truy vết run registry); evidence_ref phải truy được tới log lưu trữ.

TB-4 (TRUNG BÌNH) Chưa có bề mặt ủy quyền cho EXECUTION (RUN_SCRIPT / RUN_TESTS). SandboxOperation chỉ gồm LIST/READ/CREATE/WRITE/APPEND/DELETE. Thực thi là rủi ro cao nhất nhưng không có request type tương ứng với principal/work/limits (timeout, tài nguyên, mạng).

TB-5 (THẤP) `result_from_exception` ánh xạ PermissionError → NOT_FOUND, làm mất trạng thái DENIED trong audit. Che giấu với client có thể chấp nhận, nhưng log nội bộ cần phân biệt.

TB-6 (ĐẠT ở mức hình dạng) `validate_relative_work_path` mạnh: NFC/NFKC, ký tự điều khiển/confusable, backslash, đường dẫn tuyệt đối/UNC/drive, thành phần `.`/`..`/rỗng, tên thiết bị Windows, ký tự mở rộng (`~ % $` và dấu backtick), thành phần bảo vệ (.git, .env, …). Đây chỉ là kiểm tra chuỗi; việc chứa đựng thật trên filesystem vẫn thuộc adapter và chưa được chứng minh.

Điều kiện để Cla xem xét nâng trust boundary lên PASS: bằng chứng (code adapter/Core + test chạy thật trong runner được duyệt) rằng principal lấy từ transport đã xác thực, WorkContext resolve phía Core, mọi request bị chặn nếu principal/work không khớp, và test đỏ cho TB-1/TB-2/TB-3.

## 4. F3 — phát hiện (verifier / contract / collector)
F3-1 (CAO) Chữ ký receipt không được xác minh. `issuer_signature` chỉ cần là chuỗi không rỗng; `verifier_result` bị ép bằng đúng "TRUSTED_RECEIPT_PENDING_EXTERNAL_AUTH" nên receipt không bao giờ đạt trạng thái đã xác thực. Đúng thiết kế an toàn hiện tại, nhưng nghĩa là F3 không thể đóng bằng code này. Cần bên xác minh ngoài (khóa công khai ghim ngoài băng tần hoặc token do Core cấp).
F3-2 (TRUNG BÌNH) `receipt` là tuỳ chọn: truyền None vẫn trả "VERIFIED_IN_MEMORY_NOT_IMPORTED". Nên trả trạng thái riêng (ví dụ INTEGRITY_ONLY_NO_RECEIPT) và bắt buộc receipt trên mọi đường import.
F3-3 (TRUNG BÌNH) `source_identity` và `approved_channel` chỉ kiểm tra là chuỗi; không có allowlist. `nonce` chỉ kiểm tra định dạng; không có kho nonce chống replay; `transferred_at_utc` không có cửa sổ hiệu lực.
F3-4 (TRUNG BÌNH) Khớp SHA-256 chỉ chứng minh toàn vẹn, không chứng minh nguồn gốc: archive, manifest và hash do cùng một tiến trình tạo. Đồng ý với Nu: `repo_root`, branch, HEAD, dirty chỉ là quan sát cục bộ, giữ nhãn UNAUTHENTICATED_LOCAL_OBSERVATION.
F3-5 (TRUNG BÌNH) Denylist lệch giữa collector và contract: collector chặn thêm coverage, htmlcov, secrets.json, .bak, .dump; contract/verifier không chặn. Verifier cũng không áp ALLOWED_SUFFIXES / ALLOWED_ROOT_FILES, chỉ dùng allowlist gốc do caller truyền. Manifest/ZIP độc hại có thể chứa `.bak`, `secrets.json`, file không phải mã nguồn mà vẫn qua. Cần một nguồn quy tắc duy nhất dùng chung.
F3-6 (THẤP, cho bước extract sau này) Verifier chỉ trùng lặp chính xác theo chuỗi; chưa chặn trùng không phân biệt hoa/thường (Core/a.py vs core/A.py trên Windows), và chưa kiểm tra external_attr của ZIP (symlink/mode). Bắt buộc xử lý trước khi cho phép extract.
Điểm tốt của verifier (ghi nhận): xác minh trong bộ nhớ, không extract; kiểm tra số entry, trùng entry, thư mục, mã hoá, nén, tỷ lệ nén, kích thước thật khi stream, hash từng file, manifest canonical.

## 5. F1 — phát hiện (collector)
Ghi nhận phần đã có: từ chối repo root là symlink/reparse; chặn symlink/reparse ở từng thành phần; open chỉ đọc với O_NOFOLLOW (nếu có); so sánh định danh trước/sau; kiểm tra chứa trong repo trước và sau khi đọc; giới hạn kích thước; thư mục output ngoài repo, mới/rỗng; dọn output khi lỗi.
F1-1 (CAO, Windows) `getattr(os, "O_NOFOLLOW", 0)` bằng 0 trên Windows nên không có bảo vệ ở bước open. Đồng thời so sánh định danh trước khi đọc bị bỏ qua khi `st_ino` bằng 0 (điều kiện `before.st_ino and before_path.st_ino`), tức fail-open. Môi trường đích có dấu hiệu là Windows (.ps1, thuộc tính reparse point). Trên Windows, phần lớn chống race hiện chỉ là kiểm tra không nguyên tử.
F1-2 (TRUNG BÌNH) Thành phần cha: kiểm tra symlink/reparse và `resolve()` diễn ra TRƯỚC `os.open`, còn O_NOFOLLOW chỉ áp cho thành phần cuối. Thay thế thành phần cha trong khoảng đó vẫn lọt; kiểm tra chứa-trong-repo sau khi đọc chỉ là phát hiện muộn (byte đã nằm trong bộ nhớ), không phải ngăn chặn.
F1-3 (TRUNG BÌNH) So sánh sau khi đọc chỉ dùng size và mtime_ns; không so lại dev/ino và không đối chiếu lại đường dẫn với fd. mtime có thể thô; sửa trong cùng tick không bị phát hiện.
F1-4 (TRUNG BÌNH) Không có nhất quán mức cây: liệt kê file và đọc là hai lượt riêng; branch/HEAD/status lấy trước khi đọc và không hỏi lại sau khi đọc. Manifest có thể mô tả trạng thái Git khác với byte đã đọc. Cần hỏi lại Git sau khi đọc và so sánh; cách chắc chắn là nguồn đóng băng/chỉ đọc như Nu đã ghi.
F1-5 (TRUNG BÌNH) Không có test nào cho collector: 05_TEST chỉ có test_tool_contracts, test_source_snapshot_contract, test_source_snapshot_import_verifier. Cổng F1 của Nu đòi test dùng-một-lần cho symlink/reparse, thay file khi đọc, thay thành phần cha, lệch byte/metadata; hiện chưa có.
F1-6 (THẤP, chức năng) `git rev-parse --show-toplevel` so sánh chuỗi với `str(repo)`; trên Windows Git trả đường dẫn dấu `/` nên có thể báo lỗi sai (fail-closed nhưng làm collector không chạy được).
Lưu ý ngoài F1 (liên quan F8): `git status` có thể kích hoạt clean filter do cấu hình/attributes của repo quy định, và `git` được tìm qua PATH được kế thừa. Cần xác nhận bằng kiểm tra cô lập hoặc chỉ chạy trên nguồn đóng băng, chỉ định đường dẫn tuyệt đối tới git đã duyệt. Ghi nhận là rủi ro cần kiểm chứng, chưa xác nhận bằng thực nghiệm.

## 6. Yêu cầu cho Ka / Go / Nu (không giao việc lắt nhắt; gom thành một gói)
1. Sửa/ghi rõ TB-1, TB-2, TB-3 (cấu trúc, không chỉ docstring) hoặc ghi chúng thành nghĩa vụ adapter/Core có test chấp nhận.
2. Collector: xử lý F1-1..F1-4 (đặc biệt nhánh Windows), thêm bộ test fixture cô lập (F1-5).
3. Verifier: F3-2, F3-3, F3-5, F3-6; hợp nhất quy tắc allowlist/denylist một nguồn.
4. Test đỏ đề xuất (viết trước khi sửa): principal giả với source tuỳ ý bị từ chối; allowed_operations ngoài enum bị từ chối; ToolResult PASS không có attestation bị từ chối ở adapter; collector từ chối symlink/reparse/thay file/thay thư mục cha; verifier không trả trạng thái "đã xác minh" khi thiếu receipt; ZIP có `.bak`/`secrets.json`/trùng hoa-thường bị từ chối.
5. Chỉ khi có approved runner: chạy `python -m unittest discover -s 05_TEST -t . -v` và lưu nguyên interpreter/OS/lệnh/stdout/stderr/exit code/bộ đếm/hash. Nếu không, giữ NOT RUN.

## 7. Giới hạn của biên bản này (không được suy rộng)
- Chỉ đọc tĩnh 4 file code và 2 báo cáo ở mục 2. Chưa đọc file test, adapter MCP :8020, Core hay mã Room Hop ngoài Work 28; do đó không kết luận gì về enforcement thật.
- Không chạy code, không có log/exit code/bộ đếm; không có SHA-256 nên không khẳng định bản đã đọc trùng bản Go đã đọc.
- Không truy cập PC, không chạy collector, không import source, không thay đổi dịch vụ live.
- Cla không thể kiểm tra inbox của chính mình: `get_pending_tasks(cla)` lỗi kết nối nhiều lần, nên không có task_id và chưa gửi proposal qua cổng. Ka cần giao lại task hoặc gắn biên bản này vào task F1/F3 hiện có.
- Một số điểm đánh dấu "cần kiểm chứng" (git filter, hành vi Windows) là suy luận từ mã nguồn, chưa xác nhận bằng thực nghiệm.

## 8. Ghi nhận trạng thái sau biên bản
- Trust boundary: NOT PROVEN
- F1: NOT PASS
- F3: BLOCKED
- Approved runner / test execution: BLOCKED / NOT RUN
- E2E-Automatic / release: NO-GO
- Chuyển source sang PC: KHÔNG được phép

Ký: Cla — CTO, reviewer độc lập — 2026-10-15


## 9. Ký xác nhận
- Người ký: Cla — CTO, reviewer độc lập
- Thời điểm ký: 2026-10-15 09:45:41 +07 (02:45:41 UTC), theo đồng hồ container của Cla tại lúc ký.
- Lưu ý về thời gian: đồng hồ này chưa được đối chiếu với đồng hồ Room Hop. Trong Work 28 có tệp KA_WORK28_COORDINATION_ORDER_20261015_1153.md, mang mốc 11:53 muộn hơn giờ ký trên. Khi có mâu thuẫn, Ka lấy mốc của Room Hop làm chuẩn và ghi rõ vào nhật ký.
- Phạm vi ký: biên bản này (review tĩnh) và bộ test đề xuất CLA_PROPOSED_RED_TESTS_20261015.py (PROPOSED / NOT RUN). Việc ký chỉ xác nhận Cla là tác giả và nội dung các kết luận; không xác nhận có thực thi, PASS hay phát hành.
- Không có SHA-256 của hai tệp (connector không cung cấp).
- Trạng thái khi ký: Trust boundary NOT PROVEN; F1 NOT PASS; F3 BLOCKED; Approved runner BLOCKED / NOT RUN; E2E-Automatic / release NO-GO.

Ký tên: Cla (CTO)
