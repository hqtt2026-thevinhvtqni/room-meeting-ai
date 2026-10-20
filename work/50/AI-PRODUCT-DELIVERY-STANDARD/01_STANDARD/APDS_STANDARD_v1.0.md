# HQTT AI Product Delivery Standard (APDS) v1.0
## Tiêu chuẩn đề xuất xây dựng và vận hành sản phẩm CNTT/AI

- Work sở hữu: Work 50
- Người quyết định cuối cùng: Vinh
- Điều phối: Xu (AI-01)
- Phiên bản: v1.0 — PROPOSED / ĐỀ XUẤT
- Ngày lập: 2026-10-20 (UTC+07:00)
- Hiệu lực toàn HQTT: CHƯA PHÊ DUYỆT

## 1. Mục đích và nguyên tắc

APDS chuẩn hóa cách biến một bài toán thành sản phẩm CNTT/AI có thể phát triển, kiểm thử, phát hành, vận hành và bàn giao một cách có trách nhiệm.

Nguyên tắc:
1. Evidence First — ưu tiên bằng chứng hơn lời khẳng định.
2. Documentation First — tài liệu điều hành và quyết định phải truy vết được.
3. Architecture Before Code — hiểu bài toán, hợp đồng và kiến trúc trước khi xây.
4. One Product Source of Truth — một nguồn hồ sơ chuẩn cho mỗi sản phẩm; nhiều Work có thể thực hiện các phần khác nhau.
5. Human Time First — trạng thái và báo cáo phải giúp người quyết định biết việc gì đã xong, việc gì cần quyết định và việc gì bị chặn.
6. Least Privilege — quyền công cụ/dữ liệu chỉ đủ cho nhiệm vụ.
7. No Fake PASS — không đánh dấu PASS nếu không có bằng chứng trực tiếp.
8. Traceability — yêu cầu, thiết kế, thay đổi, test và bằng chứng phải liên kết được.
9. Explicit Approval — thay đổi rủi ro cao và phát hành cần người có thẩm quyền phê duyệt.
10. No Silent Scope Expansion — không tự mở rộng phạm vi ngoài quyết định.

## 2. Mô hình quản lý

Ba cấp:
- Product: mục tiêu, giá trị, phạm vi, yêu cầu, kiến trúc, rủi ro và tiêu chí thành công.
- Work: phần việc có chủ sở hữu, phạm vi, đầu ra, phụ thuộc và tiêu chí nghiệm thu.
- Task/Execution: hành động cụ thể, người thực hiện, thời điểm, kết quả và bằng chứng.

Các cấp phải liên kết qua Product ID, Work ID, Task ID, Requirement ID và Evidence ID khi phù hợp. Hạ tầng Evidence Hub có thể được dùng nếu khả dụng, nhưng không giả định tích hợp đã triển khai.

## 3. Cấu trúc hồ sơ sản phẩm đề xuất

```text
AI-PRODUCT/
├── 00_GOVERNANCE/
│   ├── PRODUCT_CHARTER.md
│   ├── GOVERNANCE_AND_RACI.md
│   ├── DECISION_REGISTER.md
│   ├── CHANGE_CONTROL.md
│   └── PRODUCT_STATUS.md
├── 01_DISCOVERY/
│   ├── PROBLEM_STATEMENT.md
│   ├── USERS_AND_WORKFLOWS.md
│   ├── BUSINESS_REQUIREMENTS.md
│   └── SUCCESS_METRICS.md
├── 02_REQUIREMENTS/
│   ├── FUNCTIONAL_REQUIREMENTS.md
│   ├── NONFUNCTIONAL_REQUIREMENTS.md
│   ├── AI_BEHAVIOR_REQUIREMENTS.md
│   ├── DATA_REQUIREMENTS.md
│   └── ACCEPTANCE_CRITERIA.md
├── 03_ARCHITECTURE/
│   ├── SYSTEM_CONTEXT.md
│   ├── ARCHITECTURE_DECISIONS.md
│   ├── COMPONENT_DESIGN.md
│   ├── API_AND_DATA_CONTRACTS.md
│   ├── SECURITY_THREAT_MODEL.md
│   └── DEPLOYMENT_ARCHITECTURE.md
├── 04_AI_ENGINEERING/
│   ├── MODEL_PROVIDER_POLICY.md
│   ├── AGENT_PROMPT_TOOL_DESIGN.md
│   ├── TOOL_PERMISSION_POLICY.md
│   ├── EVALUATION_DATASET_SPEC.md
│   ├── AI_EVALUATION_PLAN.md
│   └── HUMAN_OVERRIDE.md
├── 05_DELIVERY_PLAN/
│   ├── ROADMAP.md
│   ├── WORK_BREAKDOWN.md
│   ├── DEPENDENCY_MAP.md
│   ├── RESOURCE_AND_COST_PLAN.md
│   └── RISK_REGISTER.md
├── 06_IMPLEMENTATION/
│   ├── CODING_STANDARDS.md
│   ├── BRANCH_AND_RELEASE_POLICY.md
│   └── CODE_REVIEW_POLICY.md
├── 07_QUALITY_ASSURANCE/
│   ├── TEST_STRATEGY.md
│   ├── AI_EVALUATION_RESULTS.md
│   ├── SECURITY_TESTS.md
│   ├── PERFORMANCE_TESTS.md
│   └── RELEASE_ACCEPTANCE.md
├── 08_RELEASE_AND_OPERATIONS/
│   ├── DEPLOYMENT_PLAN.md
│   ├── ROLLBACK_PLAN.md
│   ├── MONITORING_AND_ALERTING.md
│   ├── BACKUP_AND_RECOVERY.md
│   ├── INCIDENT_RESPONSE.md
│   └── MAINTENANCE_PLAN.md
├── 09_EVIDENCE/
│   ├── EVIDENCE_INDEX.md
│   ├── REQUIREMENT_TRACEABILITY.md
│   └── RELEASE_EVIDENCE.md
├── 10_HANDOFF/
│   ├── USER_GUIDE.md
│   ├── RUNBOOK.md
│   ├── KNOWN_LIMITATIONS.md
│   └── HANDOFF_ACCEPTANCE.md
└── 11_LOGS/
    ├── EXECUTION_LOG.md
    ├── CHANGE_LOG.md
    └── INCIDENT_LOG.md
```

Đây là cấu trúc chuẩn tham chiếu, không bắt buộc mọi sản phẩm phải tạo file rỗng cho tất cả mục. Sản phẩm phải ghi rõ mục nào áp dụng, không áp dụng hoặc còn thiếu và lý do. Ba hồ sơ điều hành chính thức của mỗi Work tuân thủ governance của ROOM-HOP.

## 4. Vòng đời và cổng nghiệm thu

### G0 — Initiation / Khởi tạo
Yêu cầu: mục tiêu, chủ sở hữu, phạm vi, quyền quyết định, nguồn lực sơ bộ và rủi ro ban đầu.
Gate: charter được người có thẩm quyền chấp nhận.

### G1 — Discovery / Khám phá
Yêu cầu: vấn đề thực tế, người dùng, workflow, giá trị, giới hạn và chỉ số thành công.
Gate: có thể giải thích vấn đề và cách đo kết quả.

### G2 — Requirements / Đặc tả
Yêu cầu: yêu cầu chức năng, phi chức năng, hành vi AI, dữ liệu, bảo mật, tích hợp và tiêu chí nghiệm thu.
Gate: yêu cầu trọng yếu có ID và có phương pháp kiểm tra.

### G3 — Architecture / Kiến trúc
Yêu cầu: ngữ cảnh hệ thống, thành phần, luồng dữ liệu, hợp đồng, phân quyền, quyết định kiến trúc, rủi ro và phương án triển khai.
Gate: thiết kế được review; phụ thuộc và rủi ro chưa xử lý được ghi rõ.

### G4 — Build / Phát triển
Yêu cầu: code/config/tài liệu, review, kiểm thử tự động phù hợp, truy vết commit và thay đổi.
Gate: đầu ra đáp ứng yêu cầu phát triển; không tự coi code tồn tại là hệ thống đã hoạt động.

### G5 — Verify / Kiểm chứng
Yêu cầu: test chức năng, hợp đồng, tích hợp, E2E, chất lượng AI, bảo mật, hiệu năng và phục hồi theo rủi ro.
Gate: từng tiêu chí có kết quả và bằng chứng; lỗi nghiêm trọng chưa giải quyết sẽ chặn phát hành theo chính sách sản phẩm.

### G6 — Release / Phát hành
Yêu cầu: phiên bản xác định, cấu hình, quyền truy cập, kế hoạch triển khai/quay lui, giám sát và phê duyệt.
Gate: đủ điều kiện phát hành và có người chịu trách nhiệm.

### G7 — Operate & Handoff / Vận hành và bàn giao
Yêu cầu: runbook, hướng dẫn, monitoring, backup/restore, xử lý sự cố, chủ sở hữu, giới hạn đã biết và xác nhận bàn giao.
Gate: người nhận hiểu trách nhiệm và có đủ quyền/bằng chứng để tiếp quản.

Không tự động chuyển gate theo thời gian. Nếu thiếu điều kiện hoặc bằng chứng, giữ BLOCKED hoặc CHƯA XÁC MINH.

## 5. Tiêu chí Production Readiness cho sản phẩm AI

Mỗi sản phẩm phải xem xét và áp dụng theo rủi ro:
- Functional correctness — chức năng đúng.
- AI quality — chất lượng đầu ra trên tập đánh giá được duyệt.
- Agent/tool reliability — độ tin cậy khi gọi công cụ và thực hiện workflow.
- Safety/security — kiểm soát đầu vào/đầu ra, phân quyền, chống prompt injection và lộ dữ liệu khi liên quan.
- Data governance — nguồn, quyền sử dụng, retention, xóa và backup.
- Performance/availability — độ trễ, thông lượng, lỗi và tính sẵn sàng.
- Cost control — chi phí theo tác vụ hoặc đơn vị nghiệp vụ.
- Observability — log, metric, trace và correlation ID khi phù hợp.
- Recovery — backup/restore, rollback và xử lý sự cố.
- Reproducibility — ghi phiên bản model, prompt, config, code và dataset/test.
- Human oversight — chuyển người xử lý và phê duyệt thao tác rủi ro.
- Release ownership — người phê duyệt, người trực vận hành và điều kiện bàn giao.

Không áp một ngưỡng số chung cho mọi sản phẩm. Chủ sản phẩm phải đề xuất ngưỡng đo phù hợp với use case, mức rủi ro và dữ liệu nền; người có thẩm quyền duyệt ngưỡng trước khi nghiệm thu.

## 6. Vai trò và phân quyền

- Product Owner: chịu trách nhiệm vấn đề, giá trị, phạm vi và ưu tiên.
- Planner/Architect: lập kế hoạch, phân rã, phân tích phụ thuộc, thiết kế kiến trúc.
- Coder/Builder: triển khai trong phạm vi và quyền được giao.
- QE/QA: lập/chạy kiểm thử, quản lý lỗi và báo cáo kết quả độc lập khi khả thi.
- Reviewer/Security Reviewer: đánh giá thiết kế, code, quyền hạn, rủi ro và bằng chứng.
- Release/Operations Owner: phát hành, theo dõi, phục hồi và tiếp nhận vận hành.
- Approver: người được chỉ định quyết định gate/phát hành.

Quyền của agent không vượt quá quyền được giao. Capability không đồng nghĩa với authority. Người/AI xây dựng không được tự dùng lời khẳng định thay cho bằng chứng kiểm thử.

## 7. Hồ sơ Work tối thiểu

Mỗi Work phải có:
- ID, tên, mục tiêu và phạm vi trong/ngoài.
- Product ID hoặc Work cha nếu có.
- Chủ sở hữu, người thực hiện, tester, reviewer và approver.
- Trạng thái, giai đoạn/gate hiện tại.
- Deliverables, tiêu chí nghiệm thu và bằng chứng cần có.
- Phụ thuộc, rủi ro, blocker và quyết định đang chờ.
- Nhánh/phiên bản, lịch sử thay đổi và hồ sơ bàn giao.
- Ba hồ sơ điều hành chính thức theo quy định ROOM-HOP.

## 8. Evidence Contract / Hợp đồng bằng chứng

Khi phù hợp, mỗi evidence record có:
- Evidence ID, Product/Work/Task ID, Requirement ID.
- Người/AI thực hiện, role, timestamp UTC+07:00.
- Loại bằng chứng, nguồn và đường dẫn.
- Phiên bản code/commit/model/prompt/config/dataset.
- Lệnh kiểm tra, exit code, log, artifact và kết quả.
- Reviewer, trạng thái và hash toàn vẹn nếu cần.

DONE chỉ nói hành động đã thực hiện. PASS chỉ áp dụng cho tiêu chí cụ thể được kiểm tra và có bằng chứng phù hợp. Commit không chứng minh test PASS; log đơn lẻ không chứng minh E2E hoàn chỉnh; demo thành công không tự chứng minh độ tin cậy Production.

## 9. Quản lý thay đổi và phụ thuộc

Luồng chuẩn:
1. Ghi đề xuất và lý do.
2. Phân tích tác động tới yêu cầu, kiến trúc, dữ liệu, bảo mật, chi phí, vận hành và Work phụ thuộc.
3. Xin phê duyệt theo authority boundary.
4. Thực hiện trên nhánh/phiên bản được phép.
5. Kiểm thử lại các phần bị ảnh hưởng.
6. Cập nhật biên bản, kế hoạch, nhật ký, traceability và evidence.
7. Xác nhận trạng thái và bàn giao.

Thay đổi đối với quyền công cụ, dữ liệu nhạy cảm, API contract, kiến trúc lõi, bảo mật hoặc release gate cần review tăng cường. Không tự sửa protected core hoặc baseline frozen.

## 10. Trạng thái chuẩn

- DONE: hành động/đầu việc đã thực hiện.
- PASS: tiêu chí kiểm tra cụ thể đạt, có evidence.
- FAIL: kiểm tra cho thấy không đạt.
- BLOCKED: không thể tiếp tục do điều kiện/phụ thuộc/quyền hạn.
- CHƯA XÁC MINH: bằng chứng hiện có chưa đủ.
- DECISION: cần người có thẩm quyền ra quyết định.

Không gom trạng thái của nhiều tiêu chí thành một PASS chung nếu vẫn có tiêu chí bắt buộc chưa đạt/chưa xác minh.

## 11. Áp dụng và quản lý phiên bản

- Work 50 là nơi quản lý tiêu chuẩn và lịch sử phiên bản APDS.
- Work sản phẩm ghi phiên bản APDS đã áp dụng và các ngoại lệ được duyệt.
- Thay đổi tiêu chuẩn phải có lý do, tác động, reviewer, quyết định và ngày hiệu lực.
- Trước khi áp dụng toàn HQTT, APDS phải được thử trên ít nhất một sản phẩm mẫu và trình Vinh phê duyệt.
- Không tuyên bố tiêu chuẩn có hiệu lực bắt buộc toàn HQTT khi chưa có quyết định phê duyệt rõ ràng.

## 12. Trạng thái v1.0

APDS v1.0 là bản đề xuất được đưa vào Work 50 để review. Chưa có kết quả thử nghiệm sản phẩm mẫu; do đó chưa được đánh dấu PASS hoặc Approved for rollout.
