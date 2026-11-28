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


