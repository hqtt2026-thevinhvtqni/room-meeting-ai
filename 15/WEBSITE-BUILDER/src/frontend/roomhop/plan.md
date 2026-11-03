# Kế hoạch triển khai ROOM-HOP

## Phạm vi
Xây website giới thiệu ROOM-HOP — “Không gian cho mọi cuộc gặp”, tập trung giúp khách truy cập hiểu nhanh thương hiệu, khám phá các loại không gian, xem hình ảnh trực quan, nắm quy trình đặt chỗ và tìm thông tin liên hệ/tư vấn. Đây là website tĩnh, không dùng đăng nhập, server hay cơ sở dữ liệu.

## Hướng thiết kế

- **Design Movement:** Editorial hospitality / contemporary Swiss — cảm giác như một tạp chí kiến trúc kết hợp với trải nghiệm hiếu khách hiện đại.
- **Core Principles:** rõ nhịp đọc; tối giản nhưng có điểm nhấn; hình ảnh giàu chất liệu; nội dung ưu tiên hành động.
- **Color Philosophy:** nền kem ấm tạo cảm giác thân thiện và ánh sáng tự nhiên; xanh mực làm trụ cột tin cậy; cam san hô là tín hiệu thương hiệu dùng cho CTA và các điểm đánh dấu quan trọng.
- **Layout Paradigm:** bố cục lệch trục với hero chia hai mảng, các section dùng đường kẻ biên tập, số thứ tự lớn và gallery bất đối xứng thay vì các khối card đồng đều.
- **Signature Elements:** logo hình “căn phòng mở” gồm hai nét góc; nhãn số thứ tự dạng mono; đường line màu cam san hô chạy xuyên các mốc nội dung.
- **Interaction Philosophy:** thao tác nhẹ, rõ ràng và có phản hồi; nav mobile mở dạng panel; gallery có hover zoom; CTA cuộn đến liên hệ hoặc mở liên kết đặt lịch.
- **Animation:** fade-up theo thứ tự khi section xuất hiện, hover image zoom nhỏ, line/underline trượt vào khi rê chuột; chuyển động nhanh, tinh tế, tắt giảm-motion theo hệ điều hành.
- **Typography System:** `DM Sans` cho nội dung và UI; `Manrope` cho headline lớn, tạo cảm giác đương đại, chắc và thoáng. H1 có nhịp lớn, body tối đa 68ch, label dùng uppercase mono.
- **Brand Essence:** Không gian linh hoạt cho những cuộc gặp cần đúng bối cảnh — dành cho đội nhóm, cá nhân và cộng đồng; khác biệt ở trải nghiệm đặt chỗ gọn và không gian có cá tính. Tính cách: **ấm áp, linh hoạt, tinh gọn**.
- **Brand Voice:** trực diện, thân thiện, có nhịp nói tự nhiên, không sáo rỗng. Ví dụ: “Một căn phòng đúng mood có thể đổi cả cuộc gặp.” / “Chọn phòng. Chọn giờ. Bắt đầu điều đáng nhớ.”
- **Wordmark & Logo:** wordmark ROOM-HOP đi cùng biểu tượng hai nét góc tạo thành một căn phòng đang mở, có dấu chấm màu cam làm “điểm hẹn”.
- **Signature Brand Color:** **Coral Signal `#F26B4F`** — dễ nhận diện, giàu năng lượng nhưng vẫn hòa với bảng màu hospitality.

## Kiến trúc triển khai

- `index.html`: trang landing page một route, semantic sections: header, hero, giới thiệu, danh mục phòng, gallery, quy trình, liên hệ, footer.
- `styles.css`: design tokens, responsive layout, typography, animation, trạng thái mobile menu và accessibility focus.
- `script.js`: menu mobile, năm hiện tại, IntersectionObserver cho reveal animation và hỗ trợ smooth-scroll.
- `public/manus-routes.json`: khai báo route `/` theo yêu cầu WebDev.
- `app.config.ts`: metadata logoUrl dạng literal để nhận diện project; logo SVG dùng data URL HTTPS ổn định.
- `assets/`: các hình ảnh không gian được tạo riêng cho hero và gallery.

## Frontend / serving

Chạy static server trên port 3000, bind `0.0.0.0`, không cần backend. Trình duyệt tải trực tiếp `index.html`, CSS, JS và ảnh từ thư mục `assets`. Build publication dùng lệnh tĩnh `true` với output root `.` để checkpoint có sẵn `index.html`.
