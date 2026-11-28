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
