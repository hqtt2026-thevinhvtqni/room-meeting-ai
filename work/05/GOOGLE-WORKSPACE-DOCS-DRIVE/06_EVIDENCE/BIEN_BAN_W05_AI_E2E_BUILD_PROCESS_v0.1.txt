# PHỤ LỤC BIÊN BẢN WORK 05 — AI E2E BUILD PROCESS v0.1

> Ngày: 2026-09-29
> Trạng thái: PROPOSED / READY FOR REVIEW
> Mục đích: ghi nhận chỉ đạo mới của CEO Vinh về việc xây dựng quy trình AI tự thực hiện công việc toàn trình để các AI trong Work 05 theo dõi và tham gia.

## 1. CHỈ ĐẠO / MỤC TIÊU

Từ kết quả tổng hợp các proposal độc lập trong Work 05, hướng tiếp theo là không xây một workflow riêng chỉ cho Google Docs.

Mục tiêu là xây một **AI E2E Build Process (quy trình AI xây và thực hiện công việc toàn trình)** có thể tái sử dụng cho các Work khác của ROOM-HOP.

Nguyên tắc:
- Vinh giao Goal/Objective (mục tiêu).
- AI tự phân rã công việc.
- Các AI tự nghiên cứu và đề xuất độc lập.
- Xu tổng hợp, điều phối và kiểm chứng.
- AI tự triển khai các phần được phép.
- Mọi bước quan trọng phải có Evidence (bằng chứng).
- Không tự vượt VINH GATE (điểm cần quyết định của Vinh).
- Không tuyên bố DONE nếu chưa có evidence phù hợp.


## 2A. BẢNG TỔNG HỢP 35 NHÓM CÔNG VIỆC TỪ CÁC AI

> Bảng này là bảng tổng hợp theo **công việc/hạng mục**, không phải bảng xếp hạng AI. Mục đích là nhìn toàn bộ phạm vi cần giải quyết và điểm hội tụ giữa các proposal.

| # | Nhóm công việc | Kết quả hội tụ / điểm cần kiểm chứng |
|---:|---|---|
| 1 | Overall architecture | Middleware/connector giữa AI và Google; cần chốt contract với ROOM-HOP |
| 2 | ROOM-HOP mapping | Core :8000 giữ vai trò SINGLE TRUTH; Google không trở thành Core 2 |
| 3 | Docs API | Create / Get / BatchUpdate và các thao tác tài liệu |
| 4 | Drive API | Create file/folder, location, permissions, revisions |
| 5 | Create minutes | Tạo biên bản/tài liệu mới có metadata và evidence |
| 6 | Read minutes | Đọc lại nội dung và trạng thái tài liệu |
| 7 | Append | Bổ sung nội dung mà không phá dữ liệu hiện hữu |
| 8 | Update section | Cập nhật có phạm vi, tránh blind overwrite |
| 9 | Concurrent write | Xử lý nhiều AI/người cùng ghi |
| 10 | Revision control | Theo dõi revision và kiểm tra version trước khi ghi |
| 11 | Conflict handling | Phát hiện và xử lý xung đột thay vì ghi đè mù |
| 12 | Idempotency | Retry không tạo bản ghi/nội dung trùng |
| 13 | Queue | Có cơ chế xếp hàng khi cần serialize các thao tác ghi |
| 14 | Sync | Đồng bộ trạng thái/nội dung giữa Core và Google |
| 15 | Reconciliation | Đối soát khi trạng thái hai phía khác nhau |
| 16 | Human edit | Con người có thể sửa trực tiếp; hệ thống phải nhận biết và bảo toàn thay đổi |
| 17 | Authentication | OAuth / Service Account / cơ chế xác thực phù hợp |
| 18 | Authorization | Xác định quyền thao tác theo identity/context |
| 19 | Storage model | Xác định dữ liệu nào ở Core, Google, hoặc metadata store |
| 20 | Versioning | Quản lý version/revision của tài liệu và metadata |
| 21 | Audit / logging | Lưu actor, action, time, result, evidence |
| 22 | Error handling | Phân loại lỗi, ghi evidence và recovery |
| 23 | Rate limit / quota | Xử lý quota, throttling và retry phù hợp |
| 24 | Middleware API | Contract API giữa ROOM-HOP và Google adapter |
| 25 | Data model | Model cho document, source, revision, operation, status |
| 26 | Security | Credential, secret, boundary, least privilege và dữ liệu nhạy cảm |
| 27 | Deployment | Cách chạy adapter/service trong kiến trúc ROOM-HOP |
| 28 | Create / read tests | Test tạo và đọc tài liệu |
| 29 | Concurrent write tests | Test nhiều writer và race/conflict |
| 30 | Human edit tests | Test sau khi con người chỉnh sửa |
| 31 | Retry / recovery tests | Test retry, duplicate prevention và recovery |
| 32 | Permission / auth tests | Test identity, authentication, authorization |
| 33 | Evidence | Mọi claim quan trọng phải có output/log/file/revision/test tương ứng |
| 34 | Migration | Kế hoạch đưa dữ liệu/biên bản hiện hữu vào mô hình mới |
| 35 | Backup / recovery | Khả năng khôi phục khi lỗi, mất đồng bộ hoặc thao tác sai |

### Kết luận hội tụ từ bảng 35 nhóm việc

Các proposal khác nhau về cách triển khai, nhưng các điểm cần giữ để đưa sang giai đoạn build là:

- AI không gọi Google trực tiếp; đi qua lớp tích hợp đã được ROOM-HOP quy định.
- Core :8000 là SINGLE TRUTH.
- Không dùng blind overwrite (ghi đè mù).
- Write phải có revision awareness (nhận biết revision/version).
- Retry phải chống duplicate.
- Human edit là một trạng thái thực tế phải được xử lý.
- Write/concurrency/conflict/recovery phải có test và evidence.

## 2B. BẢNG 8 QUYẾT ĐỊNH MỞ CẦN ĐƯỢC CHỐT

| ID | Quyết định | Các hướng đang được đặt lên bàn | Cần evidence/test trước khi chốt |
|---|---|---|---|
| D1 | Google Docs giữ vai trò gì? | Master / human-readable canonical / view | Mapping Core ↔ Docs và lifecycle tài liệu |
| D2 | Metadata nằm ở đâu? | Core DB / Shadow DB / JSON sidecar / kết hợp | Data model, consistency và recovery |
| D3 | Credential model | Service Account / OAuth / Hybrid | Identity, permission và vận hành thực tế |
| D4 | Storage target | My Drive / Shared Drive | Ownership, permission, migration, enterprise use |
| D5 | Write model | Append-only / Section Update / Full Update có kiểm soát | Concurrent write, revision và human edit |
| D6 | Concurrency model | Lock / Revision Check / Queue / kết hợp | Race condition và recovery test |
| D7 | Sync model | Polling / Drive Changes / Watch-WebHook | Latency, quota, reliability và reconciliation |
| D8 | Conflict model | Reject / Re-read-Re-plan / Auto-merge | Conflict test và khả năng bảo toàn dữ liệu |


## 2. E2E FLOW — QUY TRÌNH TOÀN TRÌNH

Flow dự kiến:

```
GOAL
  ↓
PLAN
  ↓
TASK DECOMPOSITION
  ↓
INDEPENDENT AI RESEARCH
  ↓
PROPOSAL COLLECTION
  ↓
SYNTHESIS
  ↓
EVIDENCE GATE
  ↓
DECISION GATE
  ↓
BUILD
  ↓
TEST
  ↓
QE / VALIDATION
  ↓
FIX / RECOVERY
  ↓
VERIFY
  ↓
RELEASE
  ↓
DOCUMENT
  ↓
DONE
```

Đây là workflow khung; từng Work có thể có số lượng AI, role và nhánh xử lý khác nhau.

## 3. AI ROLE — PHÂN VAI

Không cố định số lượng AI và không bắt buộc AI nào phải giữ một role duy nhất.

Các role chuẩn dự kiến:

| Role | Trách nhiệm |
|---|---|
| Orchestrator | Điều phối toàn Work và trạng thái |
| Researcher | Nghiên cứu độc lập, thu evidence |
| Architect | Đề xuất kiến trúc/giải pháp |
| Synthesizer | Tổng hợp các proposal |
| Builder | Thực hiện implementation |
| Tester | Chạy kiểm thử |
| QE | Kiểm định độc lập |
| Evidence | Thu thập và chuẩn hóa evidence |
| Recovery | Xử lý failure và phục hồi |
| Release | Kiểm tra điều kiện phát hành |

Một AI có thể giữ nhiều role nếu Orchestrator phân công như vậy.

## 4. GATE MODEL — ĐIỂM KIỂM SOÁT

### AUTO
AI có thể tự quyết và tiếp tục khi quyết định nằm trong policy đã được chốt.

### EVIDENCE GATE
AI phải cung cấp evidence trước khi chuyển stage.

Ví dụ:
- test output;
- file đã tạo;
- API response;
- revision;
- log;
- checksum;
- command + result;
- timestamp.

### CONFLICT GATE
Khi các AI đưa ra kết luận khác nhau, hệ thống không chọn ngẫu nhiên. Phải xác định:
- khác nhau ở đâu;
- nguyên nhân;
- evidence của từng phương án;
- cần test bổ sung hay không.

### VINH GATE
Dừng workflow khi cần quyết định của Vinh về:
- architecture authority;
- business/policy;
- destructive action;
- security boundary;
- thay đổi nguyên tắc ROOM-HOP;
- các quyết định mà AI không được tự vượt.

## 5. ARTIFACT CONTRACT — AI PHẢI ĐỂ LẠI DẤU VẾT

Mỗi stage phải tạo artifact (sản phẩm/bằng chứng của stage), không chỉ trả lời bằng hội thoại.

Khung artifact:

```
01_INPUT
02_PLAN
03_RESEARCH
04_PROPOSALS
05_SYNTHESIS
06_EVIDENCE
07_DECISION
08_BUILD
09_TEST
10_QE
11_FIX
12_RELEASE
13_FINAL
```

Mỗi artifact quan trọng nên có tối thiểu:

```
STATUS
OWNER / AGENT
TIMESTAMP
INPUT
ACTION
RESULT
EVIDENCE
NEXT
```

Không dùng câu “PASS” hoặc “DONE” nếu không có căn cứ tương ứng.

## 6. FAILURE / RECOVERY

Failure không được tạo vòng lặp vô hạn.

Khung xử lý:

```
FAIL
 ↓
CLASSIFY ERROR
 ↓
READ ERROR / EVIDENCE
 ↓
REPAIR PLAN
 ↓
RETRY (có giới hạn)
 ↓
VERIFY
 ├─ PASS → tiếp tục
 └─ FAIL → ESCALATE / VINH GATE
```

Mỗi retry phải tạo thêm thông tin hoặc thay đổi cách xử lý; không retry mù.

## 7. COMPLETION CONTRACT — ĐIỀU KIỆN DONE

Một Work chỉ được đánh dấu DONE khi:
- yêu cầu đầu vào đã được đáp ứng;
- implementation (nếu có) đã hoàn tất;
- test phù hợp đã chạy;
- QE/validation đã hoàn tất;
- evidence được lưu;
- lỗi còn tồn tại đã được phân loại;
- documentation được cập nhật;
- không còn VINH GATE chưa xử lý.

Nếu chưa đủ điều kiện phải dùng trạng thái phù hợp như:
- PASS
- BLOCKED
- NEED_DECISION
- FAILED
- RECOVERY
- PARTIAL

## 8. VAI TRÒ CỦA XU

Xu là lớp **Orchestration + Synthesis (điều phối + tổng hợp)**, không phải nguồn duy nhất tạo ra kiến trúc.

Nguyên tắc:
- Không pre-lock architecture khi chưa thu đủ proposal.
- Thu proposal độc lập.
- Tổng hợp điểm hội tụ và điểm khác biệt.
- Chuyển các claim quan trọng thành evidence cần kiểm chứng.
- Điều phối build/test/QE.
- Báo cáo trạng thái thực tế cho Vinh.
- Khi vượt thẩm quyền AI thì dừng tại VINH GATE.

## 9. WORK 05 LÀ PROTOTYPE ĐẦU TIÊN

Work 05 được sử dụng làm prototype (mẫu thử) cho AI E2E Build Process.

Trình tự áp dụng:

```
Các AI đã nghiên cứu độc lập
        ↓
Proposal collection
        ↓
Xu tổng hợp
        ↓
Evidence
        ↓
Architecture decision
        ↓
Implementation
        ↓
Test / QE
        ↓
Release
```

Giá trị tiếp theo của Work 05 không còn nằm ở việc thu thêm các proposal generic giống nhau, mà nằm ở:
- kiểm chứng claims;
- xác định architecture contract;
- xây evidence;
- thử concurrency;
- thử human edit;
- thử recovery;
- kiểm tra integration với ROOM-HOP.

## 10. NGUYÊN TẮC KIẾN TRÚC CẦN GIỮ

AI E2E Process không được phá các nguyên tắc ROOM-HOP đã chốt:

```
AI
 ↓
MCP 8020
 ↓
Core 8000 — SINGLE TRUTH
 ↓
Workspace / Adapter / external systems
```

Google Docs/Drive không tự trở thành Core 2.

Sandbox là môi trường làm việc chung của AI; không đặt thêm governance/permission gate lên hoạt động nội bộ Sandbox ngoài các bảo vệ kỹ thuật cần thiết như filesystem/path safety.

## 11. NEXT STEP

Bước tiếp theo sau phụ lục này:

**AI E2E BUILD PROCESS v0.1 — Architecture Specification**

Cần đặc tả chính thức:
1. Input Contract.
2. Work State Machine.
3. Role Assignment.
4. Task Graph.
5. Artifact Contract.
6. Gate Engine.
7. Evidence Contract.
8. Failure/Recovery Engine.
9. Human/Vinh Gate.
10. Completion Contract.
11. Audit Trail.
12. Mapping xuống ROOM-HOP/MCP runtime.

**STATUS: PROPOSED — CHƯA CODE.**

---

Ghi chú vận hành: phụ lục này được tạo riêng để không overwrite (ghi đè) biên bản W05 hiện hữu. Nội dung biên bản cũ được giữ nguyên.
