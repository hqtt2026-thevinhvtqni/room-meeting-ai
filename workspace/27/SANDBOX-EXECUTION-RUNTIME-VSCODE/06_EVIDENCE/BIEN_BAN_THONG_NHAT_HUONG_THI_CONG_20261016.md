# BIEN BAN THONG NHAT HUONG THI CONG WORK 27

- Ma Work chu tri: WORK 27
- Ten Work: SANDBOX-EXECUTION-RUNTIME-VSCODE
- Nguoi chi dao: Vinh
- Nguoi lap bien ban: Xu - Planner / Chief Strategy Architect
- Ngay ghi nhan: 2026-10-16
- Gio ghi nhan: 15:00 ICT (moc gio theo phien; phut chinh xac chua duoc he thong xac minh)
- Trang thai: DECISION - THONG NHAT HUONG LAM; CHUA XAC NHAN DA THI CONG / PASS

## 1. Muc dich
Tap trung xay dung Sandbox Execution Runtime hoan chinh tai Work 27. Khong chia viec thi cong thanh nhieu Work doc lap de tranh phan tan AI, dut mach kien truc va lap lai cong suc.

## 2. Quyet dinh to chuc
1. Work 27 la Work chu tri duy nhat, so huu ke hoach, kien truc Runtime, tich hop va nghiem thu.
2. Work 28 chi la nguon chung cu ve MCP :8020, hop dong tool, doc/ghi va readback; khong mo luong thi cong song song.
3. Work 14 chi la nguon chung cu ve E2E, tu dong sua/chay lai va loi tich hop; khong mo luong thi cong song song.
4. Work 12 chi la nguon chung cu/hop dong Execution Host, vong doi Work va cach ly de truy vet, tai su dung khi phu hop; khong tao ban sao hop dong neu chua doi chieu.
5. Moi phu thuoc phai duoc truy vet tu Work 27; khong tu dong xem noi dung trong Work khac la da PASS.

## 3. Muc tieu san pham
- Doc source va yeu cau trong pham vi Work duoc cap quyen.
- Tao/sua ma trong workspace duoc cach ly.
- Chay lenh va test trong runtime duoc phep.
- Thu log, exit code, diff va artifact lam bang chung.
- Phat hien loi, tu sua co gioi han va chay lai.
- Sau toi da 5 vong patch/rerun, neu chua PASS thi dung, luu bang chung va chuyen ESCALATED_HUMAN.
- Chi ket luan PASS khi co ket qua thuc thi va bang chung doc lai doc lap.

## 4. Yeu cau ky thuat can dua vao Work 27
- P0: audit va truy vet Work 27; thu thap chung cu lien quan tu Work 28, 14, 12.
- P1: xac minh hop dong MCP read/write va readback; hash SHA-256 tren raw persisted bytes, khong tu dong chuan hoa newline; kiem tra ASCII, tieng Viet UTF-8, tep 10 MB, CRLF/LF va binary/non-UTF-8 neu duoc ho tro.
- Ghi tep: uu tien temp + flush/fsync neu backend ho tro + atomic replace cung filesystem; neu khong ho tro, can version/commit marker va tu choi doc du lieu dang ghi do.
- Tester/Reviewer phai doc lap ve session/context va chi duoc danh gia requirement, test contract va evidence duoc phep; khong dua chain-of-thought cua Coder lam bang chung. Khong tuyen bo khac model neu chua co co che chung minh.
- Runtime isolation: chay non-root; gioi han CPU/RAM/PID/disk/time; chi mount workspace cua Work va input read-only can thiet; khong mount host root, Docker socket hay credential; network mac dinh deny, chi allowlist khi co ly do va phe duyet.
- Core :8000 la single source of truth. Runtime khong duoc bypass Core. Can test Core outage/recovery, tu choi task moi khi Core khong kha dung va doi soat task dang chay sau recovery; dam bao state ben vung/idempotency.
- Timebox P0 1 ngay, P1 2 ngay, P2 1 tuan, P3 3 ngay, P4 1 ngay la DE XUAT de xem xet, chua phai cam ket tien do da duoc phe duyet.

## 5. Thu tu trien khai
READ -> TRACE -> ANALYZE -> DECIDE -> BUILD -> VERIFY -> HANDOFF.
- P0: audit va lap bang phu thuoc/evidence, khong sua ma khi chua hieu trang thai.
- P1: xu ly hop dong MCP doc/ghi va readback; chua dat thi giu BLOCKED, khong nhay qua runtime.
- P2: chi trien khai Python runtime truoc; chi mo rong Node sau khi Python co evidence PASS.
- P3: Browser E2E sau khi P2 PASS.
- P4: hoan thien tai lieu kien truc theo implementation va evidence thuc te.

## 6. Trang thai tai thoi diem lap bien ban
- Da thong nhat huong tap trung Work 27 trong cuoc trao doi.
- Da truy van danh sach tep Work 27; danh sach cho thay cac khu vuc requirement, architecture, contract, test plan va evidence hien huu.
- Trong lan kiem tra truoc, doc lai mot so tep qua MCP tra ve {}. Vi vay chua xac minh duoc noi dung file qua readback.
- Chua co bang chung cho thay da chay Python/pytest, da sua source, hoac da dat PASS.

## 7. Hanh dong tiep theo
1. Xu truy vet noi dung Work 27 va cac chung cu phu tro bang cach doc lai co kiem chung.
2. Neu MCP readback van tra {}, ghi BLOCKED voi request/response va khong suy dien file rong hay file hop le.
3. Lap evidence ledger tai Work 27: yeu cau, nguon, ket qua doc, hash, test, owner va trang thai.
4. Chi sau khi P0 co chung cu doc duoc moi chot contract va bat dau thi cong theo P1/P2.

## Xac nhan
Bien ban ghi nhan quyet dinh huong lam va trang thai bang chung; khong phai thong bao da hoan tat thi cong.
