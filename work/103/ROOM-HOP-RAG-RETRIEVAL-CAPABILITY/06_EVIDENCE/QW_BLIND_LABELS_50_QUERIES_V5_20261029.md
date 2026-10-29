# QW BLIND LABELS — 50 QUERIES (V5) — WORK 103

- **Ngày:** 2026-10-29 (UTC+07:00)
- **Người lập:** Qc — Coder, ghi nguyên trạng bộ nhãn đã được Qw rà soát độc lập và Xu chấp thuận ngày 2026-10-28 (quyết định ghi tại `05_TEST/ACCEPTANCE_AND_E2E_PLAN.md`; phân tích chất lượng tại `06_EVIDENCE/LABELED_SET_AUDIT_20261028.md`).
- **Trạng thái:** ĐÃ DUYỆT để đóng băng — chờ adjudication cuối cùng của Ka cho Blind Labeling Gate.
- **Nguồn sự thật:** `work/103/ROOM-HOP-RAG-RETRIEVAL-CAPABILITY/05_TEST/EVAL_SET.json` (version 2), mục `labeled_queries`. Tệp này KHÔNG tự tạo nhãn mới; chỉ kết xuất nguyên trạng dữ liệu đã khóa để đối chiếu trên GitHub.
- **Tính bất biến:** mỗi hàng kèm SHA-256 canonical của đúng đối tượng nhãn `{"expected": [...], "query": "..."}` (sort_keys, compact separators, UTF-8) — Ka có thể tái lập từng hash mà không phụ thuộc định dạng bảng.

## Hash nền

| Đối tượng | Giá trị |
|---|---|
| `EVAL_SET.json` file_sha256 (raw bytes) | `ab60cabdeee6254e11ee6889c20b6f2e68cd5072687bafcb314fb7c9a37c9f07` |
| `labeled_queries` (50) canonical_sha256 | `c44eded3b829c180dd63ae155721231c8f226f4442e49011769c95040a07d9e4` |
| Số lượng truy vấn có nhãn | 50 |

## Bảng 50 nhãn blind (nguyên trạng từ EVAL_SET v2)

| ID | Query | Expected source_id | n_expected | label_canonical_sha256 |
|---|---|---|---|---|
| L01 | tín hiệu quang ONT yếu ở khu B | docs/bien-ban-hop-tuan-ont.md | 1 | `078a9e52f3cd5c88d6831a7419a72fbd25ab590e05cd89691dda24d71f7ab72a` |
| L02 | LOS alarm xuất hiện lúc mấy giờ | docs/bien-ban-hop-tuan-ont.md | 1 | `762d334602e5de91782fef487a230faee7efa0e84c3bc2315634b34689d69e3e` |
| L03 | ai phụ trách kiểm tra RX power | docs/bien-ban-hop-tuan-ont.md; docs/nhiem-vu-tuan-42.md | 2 | `274a35775025c5aff9b4b42fcc6cc99d4ea29c076792957a665341d9d73d53ad` |
| L04 | vệ sinh đầu nối cáp quang cho khu nào | docs/bien-ban-hop-tuan-ont.md | 1 | `20c3727ef274f0024201ecb9c51f2b379e01145b9ef7118342cf1cb6f7cd6327` |
| L05 | hạn chót xử lý sự cố ngày nào | docs/bien-ban-hop-tuan-ont.md | 1 | `3b347d7b96b431bf975934be106cd95cee4fc2e837db4fab3a93de01b51c96da` |
| L06 | họp tuần ONT ngày mấy | docs/bien-ban-hop-tuan-ont.md | 1 | `fc9ccf2eac1cc8320be9d6b948355e6425ccf24c79b33bca2857a74f6744d34b` |
| L07 | đề xuất vệ sinh đầu nối | docs/bien-ban-hop-tuan-ont.md; docs/quy-trinh-xu-ly-su-co-mang.md | 2 | `384e9f733783802a4b544d24e7e66057396b6e4f37a32505c32b41cab8040b83` |
| L08 | quy trình xử lý sự cố mạng | docs/quy-trinh-xu-ly-su-co-mang.md | 1 | `6d4884a5d80666508f1c476e14d2bbaa58612418881f0f7eb53f7e58112dcc42` |
| L09 | kiểm tra RX power trên ONT | docs/quy-trinh-xu-ly-su-co-mang.md; docs/bien-ban-hop-tuan-ont.md | 2 | `4f4b111371bd8b3850f6f9cb7dc1ad00ee429f83ad8952bf691ea0fe3ed1dbb6` |
| L10 | khi nào escalate cho NOC | docs/quy-trinh-xu-ly-su-co-mang.md | 1 | `d47899d3a62b66fb7ec99da6b03d811a039b8b03b9f9e1a93197ec27c69b9be5` |
| L11 | vệ sinh đầu nối quang thế nào | docs/quy-trinh-xu-ly-su-co-mang.md; docs/bien-ban-hop-tuan-ont.md | 2 | `5a10a228c5efcde949d5830740efaac869b183aa8840e4508b29ee395397cd08` |
| L12 | tiếp nhận ticket từ khách hàng | docs/quy-trinh-xu-ly-su-co-mang.md | 1 | `2aef71bebe78b197d43f0339793c88526607828d39f1d61cf5f7f7736613a62d` |
| L13 | LOS kéo dài quá bao lâu thì escalate | docs/quy-trinh-xu-ly-su-co-mang.md | 1 | `118ebc2aa326cdab021f25ecd3c8c8c6fab7706bd3c45ebc7c6f87544d180750` |
| L14 | ghi nhận kết quả vào đâu | docs/quy-trinh-xu-ly-su-co-mang.md | 1 | `5ea22f895e53236ff00a48d4aaef0af7877164c65dbf27aff544e93428479612` |
| L15 | khách hàng đặt bao nhiêu tấn xi măng | docs/ke-hoach-giao-hang.md | 1 | `85e883a368e6945dfe995fbb891b862ee11dc653522e453eb42985cc5a24870a` |
| L16 | lịch giao hàng tháng 11 | docs/ke-hoach-giao-hang.md | 1 | `449ff775a4bcb9600650474f99a795281caebcbca9f4ae1a55be8c6a69a5a93c` |
| L17 | giao hàng xi măng quý mấy | docs/ke-hoach-giao-hang.md | 1 | `f398d5d661997e483dcb1493de08e2ee2be95be2ad72b874beb5c9365b9d42c9` |
| L18 | xác nhận số lượng trước khi làm gì | docs/ke-hoach-giao-hang.md | 1 | `1da1b025e24f732bdf11771e9efc39e50a779093bbc819c21c4baee86f9bee66` |
| L19 | ai phụ trách giao hàng | docs/ke-hoach-giao-hang.md | 1 | `9e075cece6192eaa073a596c8c0b317f23369c90c92599a34e78046b5e7525d8` |
| L20 | kế hoạch giao hàng xi măng | docs/ke-hoach-giao-hang.md | 1 | `02bd8e39362f43abb6a2527afe0eb7b172547bddd1b067bc6e82fff440686e1a` |
| L21 | doanh thu quý 3 đạt bao nhiêu phần trăm kế hoạch | docs/bao-cao-doanh-thu.md | 1 | `b026d1bb47cdbe57e080f45c699419b81c8e05063a468688a4c7615a5b85e7a8` |
| L22 | dự báo tăng trưởng quý 4 | docs/bao-cao-doanh-thu.md | 1 | `8f66cb15e09b0ad19eb2642a8dc520a4edccf1cb89d81743dc93f532f5907027` |
| L23 | bộ phận nào dẫn đầu doanh số | docs/bao-cao-doanh-thu.md | 1 | `8e65b27660311a1fba6bed69f3d1dfaf0bce40eb86f77b6927c27ec068b22feb` |
| L24 | xác nhận số liệu kế toán ngày mấy | docs/bao-cao-doanh-thu.md | 1 | `ddfc1db82942aeb426827ed1cddf051d39a918f09c0a5b951db09759c16d2a7b` |
| L25 | báo cáo doanh thu quý nào | docs/bao-cao-doanh-thu.md | 1 | `759e5f26dd68af5fd1f8f6dffc1b43aa4c16c4232c8646234508ec8c637de671` |
| L26 | doanh số dẫn đầu thuộc về ai | docs/bao-cao-doanh-thu.md | 1 | `f6d006d8e8dc1084ebcf7c95c79ebcc3722b39d237b70ec17d81e543256bcdb5` |
| L27 | đi muộn họp phạt bao nhiêu tiền | docs/ky-luat-hop.md | 1 | `d53c9331d49c89b7562052461ed30253e3aff29b14e857df26a13bbf0277bca0` |
| L28 | họp lúc mấy giờ thứ hai | docs/ky-luat-hop.md | 1 | `5a902b8444e7047cd1874aef75b3d0fb880f5c4c89b3504bba7a956b1450ce38` |
| L29 | vắng mặt phải làm gì | docs/ky-luat-hop.md | 1 | `0164359aaee3d2eb2342cf536aafa2b7612c0812ae3d5b8c2f63e8c207bcf129` |
| L30 | điện thoại trong họp thế nào | docs/ky-luat-hop.md | 1 | `8aae751716b3bf15071ab23d631bad4713a9b6fc26c91fd22b0ec9bc0ceeee13` |
| L31 | kỷ luật họp tuần gồm những gì | docs/ky-luat-hop.md | 1 | `fb81aaac21733c683d48803d3ee735e4564d2731e6dd34a3b74012e17a3fe0f8` |
| L32 | phạt đi muộn họp bao nhiêu | docs/ky-luat-hop.md | 1 | `0517b9acf94790f89be070314f14f341133764e0be030674b80d1b4a93195e4e` |
| L33 | mật khẩu và token lưu ở đâu | docs/bao-mat-thong-tin.md; docs/nhiem-vu-tuan-42.md | 2 | `93fb0e2855e642898b7592ddaef07081d899ccb6d63e491db24cbc7e2ce24775` |
| L34 | xóa dữ liệu khách hàng sau bao lâu | docs/bao-mat-thong-tin.md | 1 | `e4ae5eda973ce93f679dd5ccfc672f3f9dacaf743551de7c9ded6118a8568801` |
| L35 | rò rỉ thông tin phải làm gì | docs/bao-mat-thong-tin.md | 1 | `0d0f298181f3fdc8dc3e85ff473bfbadde51a370a59ca34771dd03cfb5d98e79` |
| L36 | không chia sẻ mật khẩu qua đâu | docs/bao-mat-thong-tin.md | 1 | `8a675379151800475403c077e9925534e3829a777fbb2be1f63f15e13624d152` |
| L37 | chính sách bảo mật thông tin | docs/bao-mat-thong-tin.md | 1 | `0b1ddb0ba1b0b918db8530fdffb0f4ab4ceb658a6beb57aa7e22c8fb214aa9cc` |
| L38 | token truy cập lưu ở đâu | docs/bao-mat-thong-tin.md; docs/nhiem-vu-tuan-42.md | 2 | `8d4180bb450557dccdcffc51e9cd31c3788b0d23bcc6926d54a0fe44140ee71d` |
| L39 | nhiệm vụ tuần 42 có gì | docs/nhiem-vu-tuan-42.md | 1 | `536ed1049dabca039557a42541765d30ebe5df9649c41b9155c361dc91ff4419` |
| L40 | ai viết báo cáo tín hiệu quang | docs/nhiem-vu-tuan-42.md | 1 | `5ee54e8a99a5c21abf6ee182318105623b9392b55363b86eccb0059b47b041b0` |
| L41 | Trần B làm nhiệm vụ gì | docs/nhiem-vu-tuan-42.md | 1 | `c079700664d66eee01ac5ee638ce6fa1a7f2d2847582d3511768a1ce742683fa` |
| L42 | cập nhật vault token trước ngày nào | docs/nhiem-vu-tuan-42.md | 1 | `491999b9eec5fa036a743e4dee6b61d9b490cd9f34129f5e21abb3a49a3b63c1` |
| L43 | chuẩn bị biên bản họp | docs/nhiem-vu-tuan-42.md | 1 | `df468005b4fc5d18ddc0a567d8bf2f23072b4aebec5384a6323e688822731551` |
| L44 | triển khai sales ở chi nhánh | docs/nhiem-vu-tuan-42.md | 1 | `0080c81119f138c6314c69ef203798863959bce754923633d2718d78b0bc4245` |
| L45 | vé máy bay cần ai phê duyệt | docs/quy-dinh-cong-tac.md | 1 | `11aa6dc2de4f28839cb9aee276cd488f2bcbfb69f2f250c2da24c0350310d1af` |
| L46 | per diem mỗi ngày bao nhiêu | docs/quy-dinh-cong-tac.md | 1 | `b2baf9769f8d37d4cc9106e42c4ecec03ccb65254f11710fb4d083e167a6d607` |
| L47 | khách sạn hoàn qua bộ phận nào | docs/quy-dinh-cong-tac.md | 1 | `76f1ffd7c548eaf5b49f9980bba80a1bf525c47ae215bb3a948e68b4686526cd` |
| L48 | báo cáo công tác trong bao lâu | docs/quy-dinh-cong-tac.md | 1 | `16331b0c9624d25d8307908a6a630518213fb2164eabd5228b7f9530cf9f6cfd` |
| L49 | quy định công tác xa | docs/quy-dinh-cong-tac.md | 1 | `dcbc78fc733fb12c60853b2df1536882e040d2cf29e628a3042af96591abb18c` |
| L50 | hỗ trợ công tác mỗi ngày bao nhiêu tiền | docs/quy-dinh-cong-tac.md | 1 | `8447bdc132d5d6fe9381f16baca7bd8fca14954259a4672b2f56906ba8e58185` |

## Ghi chú phạm vi

- 15 truy vấn no-answer (easy/near-miss) nằm trong cùng EVAL_SET v2, canonical_sha256 = `82116d0279cd469592a9d33743dbe83833e0aafa715e22c97b0b39de5af54228`; không lặp lại ở đây để giữ tệp nhãn answerable đúng 50 dòng theo thống nhất.
- Sau khi Ka adjudication xong từng nhãn, bản V5 này được coi là basis đóng băng cho RAG E2E. Mọi sửa đổi phải ra V6 với phê duyệt mới — không sửa V lịch sử.
