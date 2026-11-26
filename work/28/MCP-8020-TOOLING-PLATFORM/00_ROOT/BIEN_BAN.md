# WORK 28 — BIÊN BẢN / OFFICIAL MINUTES REGISTER

**Document status:** Canonical register  
**Work:** 28 — MCP Tooling Platform  
**Repository branch:** `work/28-mcp-tooling-platform`  
**Authority:** Vinh  
**Coordinator:** Xu

This is the single official minutes register for Work 28. Record decisions and instructions here. Technical reports, AI handoffs, test logs and review notes remain supporting evidence and must not be treated as parallel official minutes.

## BB-W28-20261103-001 — Governance reset and delivery direction

- **Date:** 2026-11-03
- **Source:** Vinh's instruction in the current ChatGPT conversation.
- **Decision:** Xu is to guide and coordinate the complete Work 28 scope; implementation and completion are to proceed on GitHub with maximum safe automation; Vinh should not be required to attend every small step or remain at the PC.
- **Team:** exactly Xu, Vi, Ka and An.
  - Xu — coordinator, architecture and technical decision owner.
  - Vi — implementation lead.
  - Ka — independent architecture/security review.
  - An — independent QA and verification.
  - Co — excluded from Work 28; no participation.
- **Source of truth:** GitHub branch `work/28-mcp-tooling-platform` for code and controlled documents; GitHub Actions for CI evidence.
- **Architecture:** Core :8000 remains the only authorization/application authority. MCP Build/Verification :8030 remains the supported build lane. Historical MCP :8020 listener is quarantined and DO NOT USE; Runtime MCP must be rebuilt as a separate target. Execution Host :8031 remains the approved execution boundary.
- **Safety state:** Work status ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.
- **Required behavior:** no unsupported PASS claims; preserve old evidence; one official minutes register and one Work-wide journal; record decisions, blockers, evidence and handoffs.
- **Important limitation:** this record establishes governance and assignments. It does not prove that Vi, Ka or An have acknowledged or executed a task. Their actual work must be evidenced in GitHub artifacts and CI/review records.

## Minutes maintenance rule

Append new numbered entries. Do not rewrite historical entries to make later outcomes appear earlier. Correct errors with a dated addendum that preserves the original record.


## BB-W28-20261124-002 — Khẩn cấp hoàn thiện Binary Upload phục vụ Work 119

- **Date:** 2026-11-24
- **Authority:** Vinh — trực tiếp chỉ đạo Xu hoàn thiện gấp công cụ upload file/ảnh nhị phân vào Work Sandbox vì Work 119 đang chờ sử dụng.
- **Priority:** P0 / URGENT — W28-WP3-F01 `sandbox_upload_file`.
- **Scope:** Một năng lực upload dùng chung cho ROOM-HOP; không tạo uploader riêng cho W119 hoặc từng Work.
- **Team:** Xu điều phối/tích hợp; Vi triển khai; Ka phản biện độc lập bảo mật; An kiểm thử độc lập. Giữ nguyên giới hạn bốn AI, không thêm Co.
- **Technical constraints retained:** Core :8000 là thẩm quyền duy nhất cấp/kiểm tra/revoke capability; caller identity và Work mapping phải lấy từ trusted server-side context/Core; không nhận identity/Work authority từ tool arguments; upload theo begin/chunk/finalize/abort; bounded streaming; path/symlink containment; quota/session persistence; no-overwrite mặc định; staging và atomic no-replace promotion; SHA-256 toàn file + readback; durable audit; fail-closed khi Core/store/audit/readback/cleanup không xác minh được.
- **Existing security gate:** Q4 design revision ngày 2026-11-22 vẫn ở trạng thái PROPOSED / NOT APPROVED sau khi Ka từ chối bản trước ngày 2026-11-15. Chỉ đạo khẩn cấp của Vinh cho phép Xu ưu tiên và điều phối hoàn thiện; không được hiểu là miễn review bảo mật, tự tạo Core endpoint, bỏ trusted caller binding hoặc mở quyền upload khi grant chưa được Core xác nhận.
- **Execution order:** Ka rà soát độc lập chính xác Q4 revision 2026-11-22 và chốt từng điều kiện còn thiếu; đồng thời Xu/Vi chỉ thực hiện source trace, contract/test scaffolding không tạo staging hoặc nhận bytes trước khi grant contract và Core route được phê duyệt. Sau phê duyệt, Vi triển khai tích hợp; An kiểm thử độc lập; Xu đối soát CI, readback và handoff W119.
- **Acceptance boundary:** Chỉ tuyên bố W119 dùng được sau khi tool được đăng ký trên runtime MCP mới/đúng build, Core authorization thực, upload byte-for-byte, readback SHA-256 khớp và evidence được ghi. Sandbox 8030 hiện có chỉ có text read/write tools; chưa có bằng chứng live binary upload. Không dùng historical runtime :8020.
- **Release:** Không merge/deploy, không mở Execution Gate, không đổi trạng thái Work 28 sang RELEASED bởi quyết định ưu tiên này.


## BB-W28-20261124-003 — Thay đổi chủ sở hữu triển khai: Xu tiếp nhận toàn bộ Work 28
- **Date/time:** 2026-11-24 17:01 +07
- **Authority:** Chỉ thị trực tiếp mới nhất của Vinh.
- **Decision:** Xu tiếp nhận trực tiếp toàn bộ việc xây dựng và hoàn thiện Work 28, gồm F01 filesystem safety, F02 crash recovery/durability, F03 Core upload authority/revoke-finalize, F04 raw-byte Build MCP transport/registration, kiểm thử tích hợp và bàn giao.
- **Assignment change:** Dừng giao Vi implementation Work 28. Không chờ Vi hoàn thành; các evidence Vi đã ghi trước quyết định này được giữ nguyên lịch sử, chỉ dùng sau khi Xu xác minh lại. Mọi thay đổi mới từ Vi không tự động được tích hợp.
- **Independent roles:** An tiếp tục nghiệm thu độc lập; Ka tiếp tục review bảo mật độc lập. Xu không tự cấp PASS thay An/Ka.
- **Delivery approach:** Làm trực tiếp trên nhánh cô lập từ exact PR #77 head; chia mốc M0 baseline, M1 F01/F02, M2 Core authority + transport, M3 exact-SHA CI/review/canary/handoff. Báo cáo mốc dựa trên bằng chứng và ETA cập nhật khi có blocker.
- **Safety:** Không merge, register, deploy, mở Execution Gate hoặc tuyên bố RELEASED trước khi F01–F04, independent review, exact-SHA CI và live byte-for-byte SHA-256 canary được chứng minh.
- **Supersedes:** Các assignment implementation cho Vi trong các biên bản/nhật ký trước đây, kể từ thời điểm quyết định này. Lịch sử cũ không bị sửa.


## BB-W28-20261126-004 — Vinh xác nhận chuyển giao toàn quyền điều hành Work 28 cho Ka

- **Date-Time:** 2026-11-26 09:32 +07 (Asia/Ho_Chi_Minh)
- **Authority:** Chỉ thị trực tiếp của Vinh trong cuộc hội thoại ngày 2026-11-26; xác nhận sau khi An ghi JRN-W28-117 trong Sandbox.
- **Priority:** P0 — tiếp quản remediation F01–F04 và đưa Work 28 tới nghiệm thu/bàn giao có bằng chứng.
- **Decision:** Ka tiếp quản toàn bộ quyền điều hành vận hành Work 28 trong phạm vi ủy quyền của Vinh: điều phối remediation F01–F04, tích hợp, kiểm soát evidence, phối hợp nghiệm thu độc lập và bàn giao. Vinh vẫn là thẩm quyền cuối cùng của dự án.
- **Ownership change:** Xu dừng can thiệp implementation/điều hành Work 28 và tập trung Work 118. Không tiếp tục hai đầu điều hành. Quyết định này supersede BB-W28-20261124-003 và mọi assignment lịch sử trái với phân công mới; không sửa hoặc xóa lịch sử cũ.
- **Execution roles:** Ka — Work 28 operational/delivery owner; Vi — implementation contributor khi được Ka giao nhiệm vụ cụ thể; An — independent tester, giữ quyền kết luận QA; Xu — không có nhiệm vụ implementation/điều hành W28, ưu tiên W118.
- **Independent review safeguard:** Việc Ka tiếp quản implementation/điều hành không miễn independent security review. Ka không được tự coi review source do chính mình triển khai là independent approval. Chưa có reviewer độc lập khác được chỉ định trong quyết định này; security approval vẫn là gate riêng và phải được xử lý trước release.
- **An / Sandbox record:** An báo JRN-W28-117 đã append và readback OK trong Sandbox ngày 2026-11-26. Bản ghi đó chưa được đồng bộ vào GitHub canonical tại thời điểm quyết định; đây là lần ghi nhận governance chính thức trên canonical minutes, không sửa nội dung Sandbox history.
- **Safety state:** Work 28 giữ ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; F01 BLOCKED; F02 PARTIAL / NOT VERIFIED; F03 BLOCKED; F04 BLOCKED; Independent Acceptance NOT ACCEPTED; Execution Gate CLOSED.
- **PR #78:** vẫn là candidate OPEN / DRAFT / UNMERGED; metadata/mô tả hiện tại còn ghi Xu takeover. Phải reconcile metadata và branch divergence có kiểm soát; không merge hoặc force-sync chỉ để làm khớp hồ sơ.
- **Non-authorization:** Không có nội dung nào trong quyết định này cho phép merge, register, deploy, live upload, mở Execution Gate hoặc tự chuyển finding sang PASS.
