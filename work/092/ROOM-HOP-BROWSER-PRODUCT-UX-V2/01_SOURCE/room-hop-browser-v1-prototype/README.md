# ROOM-HOP Browser Product UX V2 — Static Mock Prototype

## Mục tiêu và ranh giới

Đây là giao diện demo Browser Agent dùng HTML/CSS/JavaScript tĩnh, **MOCK ONLY**. Không kết nối agent, Chromium điều khiển thật, website, Internet, Core/MCP hoặc external API. UI cho phép nhập task để chọn một trong các kịch bản định sẵn (`Browse`, `Search`, `Agent Workflow`); nội dung result cards là dữ liệu mẫu, không phải thực thi task tự do.

## T5 — Task input / Run

`workflow.js` parse task có nội dung, nhận diện intent hỗ trợ, chọn scenario và trích từ khóa Search. Task rỗng bị từ chối; task không có intent dùng scenario demo đã chọn. `Run demo` yêu cầu các demo permission tối thiểu tương ứng được người dùng cấp trước. Nội dung task được đưa vào DOM bằng `textContent` ở các vùng hiển thị động.

## T9 — Evidence provenance

Các sự kiện hiển thị dưới nhãn **SIMULATED EVIDENCE**; mỗi bản ghi có `id`, `action`, `source=mock-engine`, `type=simulated`, `timestamp`, `status=simulated`, `artifact=null` và mô tả. Sự kiện screenshot ghi rõ không tạo ảnh/tệp. Khi mọi bước script hoàn tất, UI báo **DEMO COMPLETE**, không báo PASS hoặc xác minh task thật.

## T12 — Demo permissions

Mọi quyền khởi tạo `false`. Người dùng phải chọn `Grant for demo`; quyền có thể thu hồi. Chỉ các quyền cần cho scenario hiện tại mới được yêu cầu. Đây là trạng thái điều khiển trong UI demo, không phải browser permission hoặc security boundary thật.

## Chạy prototype

Yêu cầu Python 3.10+.

```bash
./start.sh
# hoặc: python3 server.py
# mở http://127.0.0.1:8787/
```

Server bind `0.0.0.0:8787`, phục vụ static assets và `GET /api/health`. Chỉ chạy trong môi trường tin cậy; không công khai ra Internet. Có thể mở `index.html` trực tiếp nhưng khi đó không có health endpoint.

## Kiểm thử

```bash
python3 -m pip install -r requirements-test.txt
python3 -m pytest -q
node --test tests/workflow.test.js
```

Python tests kiểm tra health/root/routes/assets/static contract. Node built-in tests kiểm tra parse task, permission requirements/missing grants, evidence schema và điều kiện hoàn tất demo. Đây là unit/API/static checks; không thay browser E2E, screenshot, accessibility audit hoặc xác minh Chromium/browser agent thực sự.

## Bằng chứng lần chạy hiện tại

Ngày 2026-11-22, mirror Cloud Sandbox được dựng từ source đã read-back qua MCP Work Sandbox chạy thành công: **pytest 12/12**, **Node 14/14**, và Playwright với executable Chromium **7/7 kiểm tra** trên viewport desktop/mobile. Kết quả E2E ghi rõ `mode=local mirror from Work 092 MCP read-back`; vì vậy đây **không** phải thực thi trực tiếp trong Work Sandbox và **không** phải GitHub Actions. GitHub CI được xác nhận riêng qua run URL/SHA sau khi Actions chạy.

Screenshot E2E là capture toàn trang của prototype mô phỏng, không phải screenshot từ website bên ngoài. E2E có kiểm tra blank-task rejection, demo permissions, evidence provenance/artifact:none, XSS-safe text rendering, mobile overflow và không có request ngoài local server/page/console errors.
