# QUYẾT ĐỊNH CHUẨN HÓA HỆ THỐNG TÀI LIỆU WORK 70 / WORK 70 DOCUMENT STANDARDIZATION POLICY
- **STT / Document ID:** DOC-056
- **Priority:** P0
- **Read order:** 56
- **Depends on:** DOC-001; DOC-033; DOC-038; DOC-039; DOC-040; DOC-055
- **Status:** ACTIVE — MIGRATION IN PROGRESS
- **Version / Updated:** 1.1 / 2026-11-07
- **Owner:** Xu / AI-01
- **Authority:** Vinh

## 1. Quyết định chuẩn / Governing decision
Áp dụng một chuẩn thống nhất cho toàn bộ Work 70. Từ thời điểm tài liệu này được ghi vào Manifest và Register:
- Mọi tài liệu do Work 70 tạo/quản lý (Markdown, tài liệu xuất bản, bản vẽ, báo cáo, biểu mẫu) phải có DOC-ID duy nhất và tên file chuẩn bắt đầu bằng DOC-NNN, trừ ngoại lệ kỹ thuật/máy đọc được liệt kê rõ.
- Tên file chuẩn: `DOC-NNN_TEN-VIET-KHONG-DAU_ENGLISH-DOCUMENT-NAME.ext`; tiếng Việt trước, tiếng Anh sau; ASCII không dấu; chữ hoa, số, gạch nối/gạch dưới; không khoảng trắng.
- Mỗi DOC-ID chỉ có một canonical path (đường dẫn chuẩn) trong Document Register. Mọi đường dẫn cũ chỉ được giữ làm compatibility pointer (tệp chuyển hướng tương thích) hoặc legacy alias (bí danh cũ), không được coi là bản nội dung độc lập.
- DOC-ID là định danh tài liệu; mã nghiệp vụ BB/QD/LENH/... là lớp mã khác; Priority và Read order không phải mã định danh.
- Version nằm trong metadata/Git history, không tạo file mới cho mỗi lần sửa.
- Tệp kỹ thuật bắt buộc tên cố định (README.md, index.html, package.json, schema, source, lockfile, desktop.ini, .gitkeep...) được miễn DOC prefix; phải được phân loại là technical/runtime artifact, có owner/path và metadata trong Register, schema hoặc sidecar phù hợp. Không cấp DOC-ID giả cho file máy.
- Document Register là control index và cũng phải có DOC-ID; bản chuẩn là DOC-055. Tệp DOCUMENT_REGISTER.md chỉ là compatibility pointer trỏ đến DOC-055, không phải một register thứ hai.

## 2. Nguồn sự thật
- DOC-055 là sổ đăng ký chuẩn duy nhất cho DOC-ID, Priority, Read order, dependencies, canonical path, status, version và branch/ref.
- DOC-040 là sổ mã văn bản nghiệp vụ, không thay thế DOC-055.
- DOC-001 Manifest xác định nguồn chuẩn, thư mục, nhánh và quyền sở hữu.
- DOC-038 quy định cách đặt tên; DOC-039 quy định mã loại văn bản; DOC-056 điều phối chuẩn hóa và di trú.
- Nhật ký thi công ghi từng thay đổi, kết quả, lỗi, bằng chứng và blocker.

## 3. Quy trình bắt buộc khi tạo/cập nhật
1. Tìm tài liệu tương đương trong DOC-055; ưu tiên cập nhật, không tạo bản trùng.
2. Nếu là tài liệu mới, cấp DOC-ID tiếp theo chưa dùng; kiểm tra trùng trước khi ghi.
3. Xác định canonical folder, owner, branch/ref và loại artifact.
4. Tạo tên file đúng chuẩn và metadata; với file máy, áp dụng schema/sidecar/register.
5. Cập nhật DOC-055, Manifest/mapping và tất cả liên kết bị ảnh hưởng.
6. Chạy kiểm tra: duplicate DOC-ID/path, filename convention, metadata-register parity, link integrity, parser/schema validation theo loại file.
7. Đọc lại Sandbox và GitHub đúng branch/commit; ghi bằng chứng vào nhật ký.
8. Chỉ báo PASS khi tất cả kiểm tra áp dụng đã chạy và có kết quả. Nếu chưa, ghi PARTIAL/BLOCKED/NOT VERIFIED.

## 4. Di trú tài liệu hiện hữu
Không đổi tên theo kiểu sửa lẻ từng file khi phát hiện. Thực hiện theo batch có inventory:
- Lập danh sách toàn bộ file, phân loại controlled document / technical artifact / legacy alias / generated output / external original.
- Lập mapping old path → new canonical path, DOC-ID, branch/ref, inbound links, owner, risk.
- Tạo bản mới tại canonical path, cập nhật mọi inbound links, Register, Manifest, Dashboard, scripts, schema và branch mappings.
- Kiểm tra nội dung/hash và lịch sử; giữ alias cũ trỏ về canonical path trong giai đoạn chuyển tiếp.
- Chạy link checker, duplicate checker, metadata validator và độc lập QE.
- Chỉ loại bỏ alias cũ khi không còn inbound reference và QE xác nhận; không xóa desktop.ini hoặc file kỹ thuật theo suy đoán.
- Mỗi batch phải có backup/commit khôi phục được và exact readback ở Sandbox + GitHub.
- Không đổi nội dung lịch sử của biên bản/quyết định đã phát hành; dùng bản sửa đổi có version hoặc văn bản mới theo DOC-039.

## 5. Phạm vi ưu tiên
Batch 1: 00_ROOT — tài liệu quản trị và compatibility pointers.
Batch 2: 01_DISCOVER–09_OPERATE — tài liệu theo phase.
Batch 3: 05_BUILD, EVIDENCE, DASHBOARD — tài liệu kỹ thuật, schemas, runtime assets và mapping.
Batch 4: cross-links, branch refs, automated validators, independent QE.
Không tuyên bố “toàn bộ Work 70 chuẩn hóa xong” cho đến khi tất cả batch được kiểm tra.

## 6. Ngoại lệ có kiểm soát
Ngoại lệ phải có lý do kỹ thuật, loại artifact, canonical path, owner và cách kiểm tra thay thế. Ngoại lệ không có nghĩa là bỏ đăng ký. Không dùng tên tùy ý cho tài liệu do AI tạo.

## 7. Quyền và thực thi
Vinh là thẩm quyền cuối cùng. Xu được quyền tự thực hiện các thay đổi chuẩn hóa thường lệ trong phạm vi này, bao gồm cập nhật register, tên file, liên kết và aliases theo migration plan; không được tự ý xóa dữ liệu gốc hoặc thay đổi nội dung đã phát hành. Báo cáo kết quả theo bằng chứng, không xin duyệt từng file nhỏ.

**English summary:** One stable DOC ID, one canonical path, one register, one naming rule, controlled aliases, automated validation and evidence-backed migration batches.


## 8. 2026-11-07 canonical evidence-path correction
The canonical cross-phase evidence directory is `EVIDENCE/` (un-numbered). `06_VERIFY/` remains the phase-06 verification directory. `05_BUILD/06_EVIDENCE/` remains build-only staging and is not the cross-phase evidence source. The former top-level `06_EVIDENCE/` is a legacy compatibility path during this migration; no new canonical artifacts may be written there. Migration uses the existing files and DOC IDs, updates DOC-055 and all active references, retains old paths as non-authoritative pointers where technically valid, and requires exact readback/link/CI checks before closure. This correction changes paths, not document identity or official-record type.


## 11. Chuẩn quản lý tiến trình sản phẩm ba tầng — D70-019 / DOC-094
Mọi sản phẩm trong Work áp dụng mô hình ba tầng:
1. **Product Task (Tầng 1):** một task tổng hợp cho mỗi sản phẩm; hiển thị mục tiêu, trạng thái tổng thể, phase hiện tại, blocker, tiến độ và liên kết phase.
2. **Phase Task (Tầng 2):** một task cho mỗi sản phẩm ở từng lifecycle phase; bắt buộc có Agent chính (chịu trách nhiệm đầu ra), Agent phối hợp (tham gia thực hiện) và Agent kiểm tra (xác minh độc lập). Mỗi phase task có deliverable, acceptance criteria, dependency, status, next action và liên kết bằng chứng.
3. **Agent Task (Tầng 3):** task thực thi chi tiết. DOC-093 là nguồn chuẩn duy nhất cho 36 Agent Task hiện hữu của Work 70; không nhân bản các task đó trong DOC-094. DOC-094 chỉ tham chiếu ID Agent Task. Các task dùng chung cấp Work phải được đánh dấu shared support, không suy diễn thành assignment riêng cho từng sản phẩm.

Nguồn chuẩn và liên kết:
- DOC-094 sở hữu Product Task và Phase Task; DOC-093 sở hữu Agent Task.
- DOC-035 là nguồn lịch sử thực thi; mọi ACK, thao tác, thử nghiệm, kết quả, blocker và thay đổi tiến độ phải ghi nhật ký, kèm Task ID / Phase Task ID / Product Task ID phù hợp.
- DOC-034 ghi biên bản họp/thống nhất; DOC-006 ghi quyết định có tính ràng buộc. Cả hai tham chiếu ID liên quan, không tạo bảng log thứ hai.
- Dashboard chỉ đọc và kết hợp DOC-093 + DOC-094 + bằng chứng; projection không phải nguồn chuẩn.

Quy tắc trạng thái và tiến độ:
- Không đánh dấu Agent Task IN_PROGRESS khi chưa có ACK và hoạt động thực tế.
- Agent Task DONE không tự động làm Phase Task DONE; Phase Task DONE cần deliverable, acceptance và evidence được kiểm tra.
- Product Task DONE chỉ khi toàn bộ phase bắt buộc và product acceptance đạt.
- Agent kiểm tra không được tự kiểm tra/phê duyệt đầu ra của chính mình.
- Không tính phần trăm Product Task bằng trung bình tiến độ Agent. Khi chưa duyệt trọng số và công thức tổng hợp, dùng NOT_CALCULATED / null.
- PROPOSED assignment không phải ACK; source hiện diện không phải nghiệm thu; static check không phải Browser E2E/QE/runtime PASS.
