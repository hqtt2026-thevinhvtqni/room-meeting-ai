# WORK 30 — PLAN E2E AUTOMATIC (KẾ HOẠCH TỰ ĐỘNG ĐẦU-CUỐI)

- Work ID: 30
- Tên Work: GPT-AUTONOMOUS-BUILD-TEAM
- Planner: Xu
- Chủ dự án / cổng phê duyệt: Vinh
- Nguồn căn cứ: `BIEN_BAN_W30.md`, `NHAT_KY_THI_CONG_W30.md`, proposal Vibe đã fetch/readback verified trên nhánh Work 30.
- Phiên bản: 2.0 — kế hoạch vận hành E2E thống nhất
- Trạng thái: **DRAFT — CHỜ VINH PHÊ DUYỆT; CHƯA ĐƯỢC BUILD**
- GitHub branch: `work/30-gpt-autonomous-build-team`
- Evidence root đề xuất: `audit/w30/`
- Lưu ý nguồn: Sandbox và GitHub chưa có bằng chứng parity/readback đầy đủ; không được coi là tự đồng bộ.

## 1. Mục tiêu và định nghĩa DONE

Xây dựng một vòng tự động khép kín từ khảo sát hiện trạng đến bàn giao, có thể chạy lại và truy vết bằng chứng. Tự động hóa việc khảo sát, build, test, thu thập bằng chứng, phân loại lỗi, kích hoạt sửa lỗi có kiểm soát và chạy lại các cổng liên quan. **Không tự động vượt qua cổng phê duyệt của Vinh, không tự cấp PASS và không tự thay đổi kiến trúc/phạm vi trọng yếu.**

Một lần chạy chỉ được bàn giao DONE khi:
- Candidate được định danh bằng commit SHA, môi trường và manifest.
- Real E2E chạy qua ranh giới công khai MCP → Core → Workspace/Execution Host phù hợp với kiến trúc thực tế; không dùng mock để chứng minh runtime thật.
- Test, log, exit code, artifacts và báo cáo độc lập được lưu, đọc lại được và gắn cùng candidate SHA.
- Security-negative và regression tests có kết quả; mọi ngoại lệ P0/P1 có quyết định rõ ràng.
- An → Cla → Ka hoàn tất đúng thứ tự; Xu bàn giao kết luận DONE / PASS / DECISION / BLOCKED, known gaps và hướng dẫn rollback.
- Mọi ACK là ACK tường minh của người nhận; file tồn tại không thay thế ACK.

## 2. Bảng Plan điều hành E2E

| Gate / ID | Mục tiêu và việc tự động thực hiện | Chủ trì / vai trò | Điều kiện vào | Đầu ra và bằng chứng bắt buộc | Điều kiện qua / dừng |
|---|---|---|---|---|---|
| G0 / W30-E2E-00 READ | Khảo sát toàn bộ Work 30: biên bản, nhật ký, proposal, repo tree, branch/commit, cấu hình, test, dịch vụ runtime; lập inventory và hash. Kiểm tra Sandbox và GitHub như hai nguồn riêng. | Xu điều phối; Cla/Go/Qe/Vibe khảo sát độc lập theo nhiệm vụ | Có task ID và nguồn được cấp quyền đọc | `survey_report.json`, manifest file/path/hash/source, lỗi đọc, commit SHA, thời điểm UTC+7 | Chỉ qua khi nguồn và giới hạn được ghi rõ. Reader rỗng hoặc thiếu quyền → BLOCKED, không giả định parity |
| G1 / W30-E2E-01 TRACE | Truy vết dependency và luồng thực thi thật; xác định entry point, ranh giới public MCP, Core, Workspace/Execution Host, service/port, test hiện hữu, baseline và rủi ro. | Xu tổng hợp; các planner cung cấp chứng cứ | G0 có inventory đủ dùng | Dependency/sequence map, bảng claim → evidence → confidence, blocker list, baseline SHA/version | Không thiết kế theo phỏng đoán; kiến trúc chưa rõ → DECISION/BLOCKED |
| G2 / W30-E2E-02 PLAN | Nhận các proposal độc lập, xác minh ACK/readback, lập bảng đồng thuận/bất đồng, phạm vi, kiến trúc, test matrix, rollout/rollback và tiêu chí nghiệm thu. | Cla/Go/Qe/Vibe nộp độc lập; Xu hợp nhất | Brief W30-PLAN-REQ-002; mỗi proposal phải nộp trước khi đọc proposal khác | Proposal riêng, ACK tường minh, readback evidence, `PLAN_W30.md` và decision log | Chưa đủ proposal hoặc thiếu bằng chứng thì ghi rõ phần thiếu; không tạo đồng thuận giả |
| G3 / W30-E2E-03 APPROVAL | Trình kế hoạch hợp nhất cho Vinh; thu quyết định APPROVE / REVISE / REJECT và khóa phạm vi/candidate baseline. | Vinh quyết định; Xu ghi biên bản | G2 có plan và danh sách quyết định còn mở | Quyết định có timestamp UTC+7, phạm vi duyệt, ngoại lệ, baseline SHA | **Hard gate:** chưa có APPROVE tường minh thì không bắt đầu build |
| G4 / W30-E2E-04 BUILD | Nu triển khai end-to-end theo plan được duyệt; tự chạy lint/type/static checks và test nền; mỗi thay đổi gắn task/defect ID; tạo candidate manifest. | Nu — Autonomous Coder | G3 APPROVE; workspace/runner được xác minh; quyền và boundary rõ | Commit(s), diff, build log, test output, `candidate_manifest.json` gồm SHA, environment, timestamp, command và artifacts | Build lỗi hoặc thiếu manifest → chuyển Repair/ BLOCKED; không deploy candidate chưa xác định |
| G5 / W30-E2E-05 REPAIR LOOP | Tự phân loại lỗi; tạo defect ID; tái hiện lỗi; giao Vi sửa trong phạm vi; chạy test trước/sau và test liên quan; chỉ chạy lại cổng bị ảnh hưởng cùng regression. | Vi — Repair Coder; Xu giám sát | Có log tái hiện, candidate SHA và defect ID | Defect record, root-cause hypothesis, patch SHA, test-before/after, attempt counter | Tối đa 2 lần sửa không hiệu quả cho cùng lỗi; sau đó dừng vá, phân tích nguyên nhân gốc và xin quyết định nếu cần |
| G6 / W30-E2E-06 VERIFY | An chạy kiểm thử độc lập trên candidate đóng băng: unit, integration, real E2E, security-negative, regression. Ghi lệnh, môi trường, thời gian, exit code, log/artifact và SHA. | An — Independent Tester | Candidate build hoàn tất; test plan và môi trường có thể tái lập | Test report, JUnit/logs, `evidence.json`, real E2E trace MCP → Core → Workspace/Execution Host | Mock không được tính là real E2E. Thiếu log/exit code/artifact hoặc SHA không khớp → NOT VERIFIED |
| G7 / W30-E2E-07 CHALLENGE | Cla phản biện đối kháng độc lập: thử edge cases, bypass, permission/identity, path escape, giả mạo ACK, thiếu provenance, race/timeout và các kết luận PASS không đủ bằng chứng. Không tự sửa code. | Cla — Adversarial Challenger | Báo cáo An có kết quả; candidate SHA đóng băng | Challenge report gồm vector, bước tái hiện, mức độ, evidence và kết luận | Phát hiện mới → defect loop quay lại G5 rồi chạy lại các cổng liên quan; Cla không tự chứng nhận bản sửa |
| G8 / W30-E2E-08 REVIEW | Ka review độc lập mã, kiến trúc, security, test evidence, challenge findings, quyết định ngoại lệ và rollback. | Ka — Independent Reviewer | An report + Cla challenge report + xử lý defect, tất cả cùng SHA | Review report, findings theo mức độ, verdict PASS / REVISE / BLOCKED | P0/P1 chưa xử lý hoặc không có quyết định của Vinh → BLOCKED |
| G9 / W30-E2E-09 HANDOFF | Xu tổng hợp trạng thái, hướng dẫn chạy/tái chạy, cấu hình cần thiết, manifest, bằng chứng, known gaps, rollback và quyết định còn chờ. | Xu — Planner / Handoff | G8 có verdict và bằng chứng truy xuất được | Handoff package, runbook, rollback guide, evidence index, decision log | DONE chỉ khi người nhận có đủ thông tin tái lập; trạng thái phải là DONE / PASS / DECISION / BLOCKED đúng nghĩa |
| G10 / W30-E2E-10 CONTINUOUS | Sau handoff, khi code/config thay đổi hoặc có regression, tạo run ID mới, so sánh với baseline và chạy lại các gate bị ảnh hưởng; security/real E2E chạy theo policy đã duyệt. | Nu + Vi; An/Cla/Ka độc lập; Xu điều phối | Có trigger hợp lệ và policy được duyệt | Run history, diff report, evidence per run, liên kết defect/commit | Không ghi đè evidence cũ; mỗi run phải bất biến và truy xuất được |

## 3. Ma trận kiểm thử bắt buộc

| Nhóm | Phạm vi tối thiểu | Bằng chứng |
|---|---|---|
| Unit | Contract dữ liệu, state machine, router, identity/governance, path safety | Lệnh, exit code, test report/JUnit, commit SHA |
| Integration | Ranh giới MCP/Core/Workspace/connectors, timeout, lỗi và phục hồi | Log tích hợp, trace, artifact, môi trường |
| Real E2E | Client → MCP server → Core governance/identity/router → Workspace/Execution Host theo public boundary thật | Runtime trace và artifact; không mock; cùng candidate SHA |
| Security-negative | Path traversal/escape, command allowlist bypass, secret leakage, identity/permission, giả mạo ACK/provenance, quyền vượt ranh giới | Test tái hiện và chứng minh vector bị chặn |
| Regression | Tất cả defect đã sửa và baseline được Vinh duyệt | Test trước/sau, baseline comparison, defect ID |
| Reliability | Timeout, retry, idempotency, service unavailable, lỗi một phần và recovery | Log từng tình huống, state cuối và hành vi retry |
| Evidence integrity | Hash/readback, artifact tồn tại, timestamp, actor/role, SHA khớp giữa báo cáo | Manifest, evidence index, readback result |

Mỗi test/run cần ghi tối thiểu: `task_id`, `run_id`, actor, role, timestamp UTC+7, environment, command, exit_code, result, artifact paths, commit SHA, evidence hash và status. Không lưu secrets trong log.

## 4. Cơ chế tự động điều phối

1. Tạo run ID duy nhất và snapshot nguồn/commit trước khi chạy.
2. Đọc trạng thái gate trước đó; không bỏ qua gate bắt buộc.
3. Chạy bước có thể tái lập bằng runner/script đã được review; lưu stdout/stderr, exit code và artifact.
4. Phân loại kết quả: PASS chỉ khi assertion + evidence đạt; FAIL khi assertion thất bại; NOT VERIFIED khi thiếu bằng chứng; BLOCKED khi thiếu quyền/đầu vào/môi trường; DECISION khi cần Vinh.
5. Khi FAIL, mở defect ID và gửi đúng người nhận; xác minh ACK. Không suy diễn ACK từ file mới xuất hiện.
6. Sau patch, xác nhận diff và SHA; chạy test tái hiện, nhóm test liên quan và regression.
7. Cùng defect thất bại sau 2 lần sửa: dừng loop, chuyển root-cause analysis; không tự tăng số lần vá.
8. Candidate đóng băng trước G6–G8. Mọi thay đổi sau đó tạo SHA mới và làm mất hiệu lực các báo cáo không còn khớp SHA.
9. Xu chỉ tổng hợp kết quả có nguồn; không được sửa báo cáo của An/Cla/Ka để tạo đồng thuận.
10. Handoff ghi rõ DONE (việc đã hoàn tất), PASS (cổng kiểm thử đạt), DECISION (chờ Vinh), BLOCKED (không thể tiếp tục).

## 5. Bằng chứng và cấu trúc thư mục đề xuất

```text
audit/w30/
  survey/<run-id>/survey_report.json
  trace/<run-id>/dependency_map.md
  plan/decision_log.md
  build/<run-id>/candidate_manifest.json
  build/<run-id>/build.log
  defects/<defect-id>/defect.json
  defects/<defect-id>/before_after_tests/
  e2e/<run-id>/evidence.json
  e2e/<run-id>/logs/
  e2e/<run-id>/artifacts/
  security/<run-id>/report.md
  regression/<run-id>/report.md
  challenge/<candidate-sha>/cla_report.md
  review/<candidate-sha>/ka_report.md
  handoff/<candidate-sha>/README.md
```

Đây là cấu trúc đề xuất, chưa khẳng định thư mục hay script đã tồn tại. Chỉ tạo code/tool mới sau khi G3 được APPROVE.

## 6. Trạng thái đầu vào hiện tại (theo bằng chứng đã đọc)

| Hạng mục | Trạng thái | Ghi chú |
|---|---|---|
| Biên bản chính trên GitHub | READBACK VERIFIED | Đã fetch nội dung và blob SHA |
| Nhật ký trên GitHub | READBACK VERIFIED | Đã fetch nội dung và blob SHA |
| Proposal Vibe | READBACK VERIFIED | Có ACK tường minh và nội dung proposal |
| Proposal Cla | CHƯA XÁC NHẬN | Chưa có nội dung/ACK đọc lại được trong các nguồn đã kiểm tra |
| Proposal Go | CHƯA XÁC NHẬN | Chưa có nội dung/ACK đọc lại được trong các nguồn đã kiểm tra |
| Proposal Qe | NOT FOUND trên đường dẫn dự kiến | Fetch `docs/work30/plan-proposals/QWEN_PLAN_PROPOSAL.md` trả 404; không kết luận Qe chưa làm ở nơi khác |
| Sandbox ↔ GitHub parity | BLOCKED / NOT VERIFIED | Sandbox reader từng trả `{}`; thao tác write `status: ok` không chứng minh readback/hash parity |
| Build/E2E runtime Work 30 | NOT STARTED theo plan hiện có | Chưa có căn cứ trong biên bản cho phép build; đang chờ Vinh phê duyệt |
| Phê duyệt plan hợp nhất | PENDING | Chỉ Vinh có quyền quyết định |

## 7. Rủi ro, rollback và giới hạn an toàn

- Không dùng mock, fixture hoặc gọi thẳng hàm nội bộ để tuyên bố Real E2E thành công.
- Không tự động deploy, merge vào main, đổi baseline, mở rộng quyền hoặc sửa kiến trúc nếu chưa được phê duyệt rõ.
- Mỗi gate tạo artifact bất biến gắn SHA; không ghi đè bằng chứng của run trước.
- Rollback theo commit/tag đã biết, ghi SHA trước/sau, lý do, actor và test xác minh sau rollback.
- Nếu môi trường, reader, dispatch hoặc quyền không xác minh được: BLOCKED / NOT VERIFIED; không thay thế bằng phỏng đoán.
- Sau hai lần sửa không hiệu quả cùng defect: dừng vá lặp.
- Không có P0/P1 chưa giải quyết hoặc chưa có quyết định chấp nhận rủi ro trước handoff.

## 8. Quyết định cần Vinh phê duyệt

- [ ] APPROVE kế hoạch E2E Automatic v2.0 để bắt đầu triển khai.
- [ ] REVISE — yêu cầu chỉnh sửa trước khi triển khai.
- [ ] REJECT — không triển khai theo kế hoạch này.

**Trạng thái mặc định hiện tại: CHỜ QUYẾT ĐỊNH.** Việc tạo/cập nhật tài liệu Plan không phải là phê duyệt build.
