# VI → KA — WP2 SERVICE BLOCKED MAPPING + RACE COVERAGE — SECURITY REVIEW HANDOFF (2026-11-13)

**From:** Vi (Vibe, theo ủy quyền tự chủ của Vinh)  
**To:** Ka | Independent Reviewer  
**Work:** 28 — MCP Tooling Platform, WP2  
**Branch:** `work/28-mcp-tooling-platform`  
**Related:** JRN-W28-012 (handoff trước), JRN-W28-013, handoff AN cùng ngày

## DIFF UNDER REVIEW

1. `execution_host/host.py` — commit `98d68a7209447aa0e234455991975b9df59102d8`: `start_service()` giờ bắt `JobObjectUnavailable` (OSError subclass) và trả kết quả cấu trúc BLOCKED thay vì raise. Khi BLOCKED: không đăng ký process, `pid: None`, `job_object: NOT_ATTACHED`, `process_reaped` phản ánh việc dọn tiến trình suspended.
2. `tests/test_wp2_service_mapping_and_race.py` — commit `31f21c34e6296121cd3d086077db7a7f6ab20d8f` (5 test: mapping, no-register + retry, 5 vòng lặp, process đã exit, 4 worker đồng thời).

## REVIEW QUESTIONS FOR KA

1. **Fail-closed đúng nghĩa chưa?** BLOCKED có phải là trạng thái an toàn (không process sống, không registry entry, không caller nhầm là RUNNING) hay có kịch bản caller coi BLOCKED là "thử lại được" rồi bỏ qua containment?
2. **Reap semantics:** việc reaped tiến trình suspended trong except-path có rò rỉ handle/zombie trên Windows và POSIX trong mọi nhánh lỗi?
3. **Race/reentrancy:** T5 (4 worker đồng thời) có đủ để khẳng định không race registry, hay cần thêm kịch bản (spawn fail + cleanup fail đồng thời, exception giữa register)?
4. **API surface:** mapping BLOCKED có nên kèm mã lỗi chuẩn hóa/audit event để WP6 correlation dùng, trước khi service API được lộ ra ngoài?
5. **Scope:** diff có đụng gì ngoài contract đã nêu (so diff thực tế, không tin mô tả)?

## CI STATUS

- Run #326 (`66cb78f`) SUCCESS; run #327 (HEAD `8c9ff9d`) IN_PROGRESS lúc lập handoff. Ka review diff là review tĩnh + contract; không cần chờ #327 để bắt đầu, nhưng kết luận chấp nhận phải tham chiếu run xanh trên commit có code.

## BOUNDARIES

- Không đụng MCP :8020. Không đổi Core/Runtime/Execution Host.
- Không khai review PASS thay Ka; acknowledgement chỉ có hiệu lực khi Ka tự ghi artifact tham chiếu commit SHA.

**STATUS:** HANDOFF ISSUED / KA ACKNOWLEDGEMENT PENDING. Work ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.
