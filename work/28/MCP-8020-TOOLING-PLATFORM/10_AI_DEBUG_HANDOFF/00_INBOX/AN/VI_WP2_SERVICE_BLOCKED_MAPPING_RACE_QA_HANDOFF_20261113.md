# VI → AN — WP2 SERVICE BLOCKED MAPPING + RACE COVERAGE — INDEPENDENT QA HANDOFF (2026-11-13)

**From:** Vi (Vibe, theo ủy quyền tự chủ của Vinh)  
**To:** An | Independent QA  
**Work:** 28 — MCP Tooling Platform, WP2  
**Branch:** `work/28-mcp-tooling-platform`  
**Related:** JRN-W28-011 (handoff trước), JRN-W28-013, handoff KA cùng ngày

## SCOPE DELIVERED (this slice closes the two open items in JRN-W28-011)

1. `execution_host/host.py` — commit `98d68a7209447aa0e234455991975b9df59102d8`: `start_service()` bắt `JobObjectUnavailable` và trả cấu trúc `{status: BLOCKED, blocker: job_object_attach_failed, notes, process_reaped, pid: None, job_object: NOT_ATTACHED}`; không đăng ký process khi BLOCKED.
2. `tests/test_wp2_service_mapping_and_race.py` (mới, 5 test) — commit `31f21c34e6296121cd3d086077db7a7f6ab20d8f`:
   - T1: BLOCKED mapping khi attach Job Object thất bại (patch `assign_to_job` raise `JobObjectUnavailable`).
   - T2: BLOCKED không đăng ký process vào registry; retry sau khi gỡ patch → PASS.
   - T3: 5 vòng spawn/cleanup lặp trên cùng service, tất cả reaped.
   - T4: cleanup process đã tự exit không lỗi.
   - T5: 4 worker thread spawn/cleanup đồng thời, tất cả reaped.

## CI EVIDENCE STATUS

- Run #324 (`98d68a7`) SUCCESS; run #326 (`66cb78f`, docs) SUCCESS; run #325 bị cancel do concurrency.
- Run #327 trên HEAD `8c9ff9d` đang IN_PROGRESS lúc lập handoff này. **Yêu cầu An đọc kết quả run #327 (5 job) trên đúng commit trước khi xác nhận; không dùng run #324 làm bằng chứng cho test mới.**

## WHAT AN IS ASKED TO DO (independently)

1. Đọc kết quả run #327: unit/regression, Linux lifecycle, Windows lifecycle, immutable-source-artifact retest, auto E2E gate report — từng job, không chỉ conclusion.
2. Tự chạy lại 5 test mới trên Linux và Windows native; kiểm tra T5 không flaky (chạy lặp ≥3 lần nếu có điều kiện).
3. Adversarial: spawn fail giữa chừng cleanup, cleanup raise, registry state sau BLOCKED, signal/timeout tương tác với mapping BLOCKED.
4. Xác nhận không có route production bị ảnh hưởng (server.py /execute không qua start_service).
5. Báo cáo: exact commit, môi trường, lệnh, kết quả, log/artifact, phần CHƯA test.

## BOUNDARIES

- Không đụng MCP :8020 (quarantined). Không đổi Core :8000 / Runtime / Execution Host :8031.
- Không khai PASS thay An; acknowledgement của An chỉ có hiệu lực khi An tự ghi artifact tham chiếu commit.

**STATUS:** HANDOFF ISSUED / AN ACKNOWLEDGEMENT PENDING. Work ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.
