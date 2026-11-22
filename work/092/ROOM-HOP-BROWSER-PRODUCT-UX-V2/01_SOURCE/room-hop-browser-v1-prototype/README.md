# ROOM-HOP Browser Product UX V2 — Static Mock Website

## Mục tiêu
Chuyển ROOM-HOP Browser V1 từ control dashboard thành trải nghiệm Browser Agent rõ ràng: Browser là nhân vật chính, AI Agent là người đang sử dụng Browser trong cùng một session.

## UX V2
Browser View chiếm vị trí chính với tabs, New Tab, Back, Forward, Reload, URL bar, mock web page, Loading/Ready và session state `Agent controlled / Human control`.

Agent rail có task input, Run, trạng thái Connected/Working/Done, current action bằng ngôn ngữ người dùng, next action, progress, Agent Activity timeline, Session Evidence chi tiết, runtime PASS và Agent Permissions.

Human ↔ Agent control là interaction mock: Take control / Give control to Agent. Ba scenario V1 vẫn tồn tại trong **Demo / Test Mode**, còn architecture được chuyển vào **Developer / Architecture View**.

## Cách chạy
Mở trực tiếp `index.html` bằng browser. Website không cần backend, database, API, CDN hoặc Internet.

Nếu cần preview server: `python3 -m http.server 8787`.

## Giới hạn
Đây vẫn là **MOCK ONLY**: không có Chromium thật, không điều khiển website thật và không gọi external API. PASS chỉ xuất hiện sau khi runtime state hoàn tất toàn bộ action của workflow hiện tại.
