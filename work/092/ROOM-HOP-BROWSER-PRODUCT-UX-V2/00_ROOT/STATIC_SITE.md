# STATIC SITE DELIVERY

Work 092 hiện được đóng gói dưới dạng static website:

- Không cần Python server để chạy UI.
- Không gọi `fetch`, XMLHttpRequest, external API, CDN hay Internet.
- Mở trực tiếp `01_SOURCE/room-hop-browser-v1-prototype/index.html`.
- `styles.css` và `app.js` là các dependency nội bộ duy nhất.
- Các tương tác mock chạy hoàn toàn trong browser memory.

Đã kiểm chứng bằng Chromium với file local và bằng preview HTTP server để kiểm tra responsive. Bản preview HTTP chỉ là phương pháp phục vụ file, không phải backend của sản phẩm.
