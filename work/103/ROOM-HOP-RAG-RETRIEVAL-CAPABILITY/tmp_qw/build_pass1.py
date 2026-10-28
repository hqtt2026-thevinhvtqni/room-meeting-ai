import json, hashlib, datetime
from pathlib import Path

ROOT = Path('.')
POOL = ROOT/'05_TEST/BLIND_RETRIEVAL_CHALLENGE_POOL_V1.json'
EV   = ROOT/'05_TEST/EVAL_SET.json'

S_ONT='docs/bien-ban-hop-tuan-ont.md'
S_QT ='docs/quy-trinh-xu-ly-su-co-mang.md'
S_GH ='docs/ke-hoach-giao-hang.md'
S_DT ='docs/bao-cao-doanh-thu.md'
S_KL ='docs/ky-luat-hop.md'
S_BM ='docs/bao-mat-thong-tin.md'
S_NV ='docs/nhiem-vu-tuan-42.md'
S_CT ='docs/quy-dinh-cong-tac.md'

# QW PASS-1 independent labels: id -> (answerable, [source_ids], rationale)
L = {
"Q001":(False,[],"Corpus chi co bao cao doanh thu QUY 3 (dat 120% ke hoach); quy 4 chi duoc DU BAO tang truong on dinh va khong co so lieu theo chi nhanh; 'chi nhanh Ha Noi' khong xuat hien o bat ky tai lieu nao. Yeu cau dang tinh chinh xac (doanh thu Q4 cua chi nhanh HN) khong duoc corpus ho tro."),
"Q002":(True,[S_KL],"Toan bo noi dung ky luat hop tuan nam trong docs/ky-luat-hop.md: phat di muon 50 nghin, dien thoat che do im lang, vang mat phai bao truoc 1 ngay, hop 8 gio sang thu hai."),
"Q003":(False,[],"Bien ban ONT chi ghi tin hieu quang yeu o KHU B va khong ghi gia tri dBm nao cho bat ky khu nao; 'khu C' va don vi dBm deu khong co trong corpus."),
"Q004":(True,[S_QT],"docs/quy-trinh-xu-ly-su-co-mang.md liet ke day du 5 buoc: tiep nhan ticket -> kiem tra LOS va do RX power tren ONT -> ve sinh dau noi quang -> escalate NOC neu LOS keo dai qua 30 phut -> ghi ket qua vao bien ban."),
"Q005":(False,[],"Khong co so lieu doanh thu quy 4, cung khong co thong tin 'van phong chi nhanh Da Nang' trong corpus; chi co du bao quy 4 mang tinh khai quat trong bao cao doanh thu quy 3."),
"Q006":(True,[S_CT],"docs/quy-dinh-cong-tac.md noi dung: ve may bay can quan ly truc tiep phe duyet, ho tro per diem 500 nghin/ngay, khach san hoan qua ke toan, bao cao cong tac trong 3 ngày sau khi ve."),
"Q007":(False,[],"Chi co mot dong LOS alarm xuat hien luc 3 gio sang trong bien ban ONT, gan voi su co o KHU B; corpus khong nhac den 'khu C' nen khong the gan moc gio cho khu C."),
"Q008":(True,[S_BM],"docs/bao-mat-thong-tin.md ghi cac quy dinh: khong chia se mat khau qua email, token truy cap luu trong vault, xoa du lieu khach hang sau 30 ngay, ro ri thong tin phai bao ngay cho bao mat."),
"Q009":(False,[],"Corpus khong chua gia tri RX power/dBm nao; bien ban ONT chi ghi Nguyen Van A phu trach kiem tra RX power, khong co so do va khong co 'khu A'."),
"Q010":(True,[S_GH],"docs/ke-hoach-giao-hang.md: ke hoach giao hang xi mang quy 4, khach hang dat 5000 tan, lich giao 5/11, 12/11 va 19/11."),
"Q011":(False,[],"Quy dinh chung ghi ve may bay can phe duyet cua 'quan ly truc tiep', nhung corpus khong co chuyen di Ha Noi tuan sau cung khong dinh danh nguoi cu the nao cho viec duyet nay."),
"Q012":(True,[S_DT],"docs/bao-cao-doanh-thu.md: doanh thu quy 3 dat 120% ke hoach, bo phan sales dan dau doanh so, du bao quy 4 tang truong on dinh, so lieu ke toan xac nhan ngay 5/10."),
"Q013":(False,[],"Khong co so lieu doanh thu quy 4 va khong tai lieu nao nhac den bo phan marketing; chi co 'sales' dan dau doanh so quy 3."),
"Q014":(True,[S_NV],"docs/nhiem-vu-tuan-42.md liet ke: Nguyen Van A viet bao cao tin hieu quang, Tran B ho tro trien khai sales tai chi nhanh, cap nhat vault token he thong truoc thu sau, chuan bi bien ban hop tuan toi."),
"Q015":(False,[],"Lich giao xi mang chi co ba moc thang 11 (5/11, 12/11, 19/11) va khong ghi nhan chi nhanh mien Trung hay bat ky moc nao trong thang 12."),
"Q016":(True,[S_QT],"Duong danh quy trinh mo ta theo thu tu tu buoc 1 den buoc 5; buoc dau tien khi nhan ticket khach hang la kiem tra LOS va do RX power tren ONT, tiep den ve sinh dau noi quang, escalate NOC neu LOS keo dai qua 30 phut, ghi ket qua vao bien ban."),
"Q017":(False,[],"Nguoi phu trach kiem tra RX power (Nguyen Van A) gan voi su co khu B; han chot xu ly su co la 20/10. Corpus khong co 'khu C' cung khong co moc 15/11."),
"Q018":(True,[S_ONT,S_QT],"Hai nguồn bo sung nhau: bien ban ONT de cap tin hieu yeu o khu B va de xuat ve sinh dau noi cap quang; quy trinh xu ly su co neu cac buoc kiem tra LOS/do RX power va ve sinh dau noi quang."),
"Q019":(False,[],"Muc phat di muon hop 50 nghin la cua phong theo docs/ky-luat-hop.md ('ky luat hop tuan cua phong'), khong gan voi chi nhanh Ha Noi; corpus khong co thong tin theo chi nhanh."),
"Q020":(True,[S_BM],"docs/bao-mat-thong-tin.md: 'Ro ri thong tin phai bao ngay cho bao mat'; cac quy dinh lien quan (khong chia se mat khau qua email, token luu vault, xoa du lieu khach hang sau 30 ngay) la bo canh cho trach nhiem bao cao nay."),
"Q021":(False,[],"Corpus chi yeu cau 'token truy cap phai luu trong vault' va 'cap nhat vault token he thong truoc thu sau'; khong tai lieu nao dinh nghia chu ky doi token theo so ngay."),
"Q022":(True,[S_CT],"Cac khoan ho tro/cong tac trong docs/quy-dinh-cong-tac.md: ve may bay (can phe duyet), per diem 500 nghin moi ngay, khach san hoan qua ke toan."),
"Q023":(False,[],"Tai lieu chi ghi 'Khach san hoan qua ke toan' (ngan quy/cach thuc hoan), khong co muc tran toi da tien hoan moi dem."),
"Q024":(True,[S_GH],"docs/ke-hoach-giao-hang.md: 'Lich giao: 5/11, 12/11 va 19/11' trong ke hoach giao hang xi mang quy 4."),
"Q025":(False,[],"Con so 120% ke hoach la doanh thu quy 3 TOAN cong ty/trong bao cao doanh thu, khong phai cua 'chi nhanh Ha Noi'; corpus khong cat so lieu theo chi nhanh."),
"Q026":(True,[S_NV],"docs/nhiem-vu-tuan-42.md ghi rang mo tac vu 'Cap nhat vault token he thong truoc thu sau' phai hoan thanh truoc thu sau; do la viec duy nhat trong corpus co moc 'truoc thu sau'."),
"Q027":(False,[],"Quy trinh neu nguong escalate: LOS keo dai qua 30 PHUT thi escalate cho NOC. Day la dieu kien trigger cua ky thuat vien, khong phai SLA xu ly cho NOC va cung khong phai don vi gio; corpus khong co SLA cho NOC."),
"Q028":(True,[S_BM,S_NV],"docs/bao-mat-thong-tin.md: token truy cap phai luu trong vault; docs/nhiem-vu-tuan-42.md: cap nhat vault token he thong truoc thu sau."),
"Q029":(False,[],"Corpus khong co danh sach khach hang no qua han cung khong co du lieu cong no cho quy 4."),
"Q030":(True,[S_KL],"docs/ky-luat-hop.md: hop dien ra 8 gio sang thu hai, phai bao truoc 1 ngay khi vang mat, dien thoat de che do im lang trong hop, phat 50 nghin neu di muon."),
"Q031":(False,[],"Pham vi phe duyet trong quy dinh cong tac chi lap cho 've may bay' (quan ly truc tiep); khong tai lieu nao nhac den chi phi taxi hay nguoi duyet loai chi phi nay."),
"Q032":(True,[S_DT,S_GH,S_NV],"Doanh thu: bao cao doanh thu quy 3 dat 120% ke hoach, sales dan dau doanh so, du bao quy 4 on dinh, ke toan xac nhan 5/10. Lien quan den sales: phu trach giao hang xi mang (ke hoach giao hang) va ho tro trien khai sales tai chi nhanh (nhiem vu tuan 42)."),
"Q033":(False,[],"Corpus khong ghi viec thay thiet bi ONT cho khu nao va khong co 'khu B duoc thay thiet bi' cung moc ngay nao cho viec thay thiet bi; chi co de xuat ve sinh dau noi va han chot xu ly 20/10."),
"Q034":(True,[S_QT,S_NV,S_ONT],"Quy trinh buoc 5: ghi nhan ket qua vao bien ban; nhiem vu tuan 42: chuan bi bien ban hop tuan toi; chinh bien ban ONT la mau tai lieu hop tuan duoc lap."),
"Q035":(False,[],"Ky luat hop ghi hop 8 GIO SANG THU HAI cua phong; khong co lich hop 'chieu thu sau' va khong co thong tin theo chi nhanh Ha Noi."),
"Q036":(True,[S_QT],"Buoc 4 va buoc 5 cua quy trinh: escalate cho NOC neu LOS keo dai qua 30 phut; ghi nhan ket qua vao bien ban."),
"Q037":(False,[],"Bao cao doanh thu chi cap bo phan (sales dan dau doanh so); khong co so lieu doanh thu theo tung nhan vien cung khong co theo thang 10."),
"Q038":(True,[S_CT],"Nghia vu sau chuyen cong tac trong docs/quy-dinh-cong-tac.md: bao cao cong tac trong 3 ngay sau khi ve; khach san hoan qua ke toan."),
"Q039":(False,[],"Chính sách chi cam ket 'khong chia se mat khau qua email'; khong tai lieu nao dat ra yeu cau do dai toi thieu cua mat khau vault."),
"Q040":(True,[S_KL,S_ONT],"Ky luat hop: hop tuan cua phong dien ra 8 gio sang thu hai; bien ban ONT: cuoc hop tuan ONT ngay 12/10."),
"Q041":(False,[],"Tai lieu chi la KE HOACH: 5000 tan duoc dat va lich giao gom 19/11; khong co so lieu giao THUC TE cua ngay 19/11."),
"Q042":(False,[],"Xac nhan so lieu ke toan ngay 5/10 gan voi bao cao QUY 3; khong co ai ky xac nhan cho doanh thu quy 4 (quy 4 moi chi la du bao)."),
"Q043":(False,[],"Quy trinh trong corpus la xu ly su CO MANG (LOS/RX power/dau noi quang/NOC); khong co quy trinh xu ly su co DIEN tai van phong."),
"Q044":(False,[],"Muc per diem 500 nghin moi ngay la muc chung cua quy dinh cong tac xa; khong tai lieu nao phan theo quoc gia hay nhac den Nhat Ban."),
"Q045":(False,[],"Bien ban ghi de xuat ve sinh dau noi va han chot xu ly su co 20/10 cho su co KHU B; khong co trang thai 'khac phuc xong' va khong co su co khu C."),
"Q046":(False,[],"Ngay 5/10 la ngay ke toan xac nhan so lieu cho bao cao doanh thu QUY 3; khong co ngay xac nhan cho quy 4."),
"Q047":(False,[],"Corpus khong co so luong ticket LOS theo tuan; tuan 42 chi xuat hien trong danh sach nhiem vu, khong gan voi so lieu ticket."),
"Q048":(False,[],"Chinh sach bao mat neu kenh bi cam la EMAIL; khong tai lieu nao de cap den Zalo hoac quy dinh chia se file qua ung nhan nay."),
"Q049":(False,[],"Doanh so dan dau duoc ghi o cap BO PHAN (sales) cho bao cao quy 3; khong co xep hang doanh so theo CHI NHANH va khong co so lieu quy 4."),
"Q050":(False,[],"LOS alarm xuat hien luc 3 gio sang va bien ban ngay 12/10, nhưng corpus khong ghi nhan su truc ca hay danh tinh nguoi truc NOC luc 3 gio sang."),
}

pool=json.load(open(POOL))
ev=json.load(open(EV))
valid_sources={d['source_id'] for d in ev['documents']}
items=pool['items']
assert len(items)==50, len(items)
missing=[i['id'] for i in items if i['id'] not in L]
extra=[k for k in L if k not in {i['id'] for i in items}]
assert not missing and not extra, (missing, extra)

for it in items:
    a,srcs,rat = L[it['id']]
    if a:
        assert srcs, it['id']
        assert all(s in valid_sources for s in srcs), it['id']
        assert len(set(srcs))==len(srcs), it['id']
    else:
        assert srcs==[], it['id']
    it['answerable']=a
    it['expected_source_ids']=srcs
    it['annotator_rationale']=rat
    it['annotation_status']='LABELED_PASS1_INDEPENDENT'

corpus_canon='\n'.join(f"{d['source_id']}\x1f{d['text']}" for d in ev['documents'])
n_true=sum(1 for i in items if i['answerable'])
out={
 "schema_version":1,
 "title":"Work 103 blind retrieval challenge — QW annotation record, PASS 1 (independent)",
 "annotator_id":"QW-QE-PASS1",
 "annotated_at_utc":"2026-10-28T12:00:00Z",
 "status":"PASS1_INDEPENDENT_NOT_FROZEN_NOT_FOR_METRIC_REPORTING",
 "blindness_protocol":[
   "Inputs used: pool item ID + query text only, plus the committed corpus documents (source_id/title/text).",
   "NOT consulted by the annotator: retrieval scores, rankings, system outputs, baseline metrics, and the author candidate list / EVAL_SET labeled_queries & no_answer_queries ground truth.",
   "Labels assigned per labeling_rules of BLIND_RETRIEVAL_CHALLENGE_POOL_V1.json before any comparison with author labels.",
   "This is pass 1 of an independent double-annotation scheme; disagreement resolution with pass 2 and freeze/hash come after unblinding."
 ],
 "provenance":{
   "branch_head_commit": __import__('subprocess').check_output(['git','-C','/workspace','rev-parse','HEAD']).decode().strip(),
   "pool_file_sha256": hashlib.sha256(open(POOL,'rb').read()).hexdigest(),
   "eval_set_file_sha256": hashlib.sha256(open(EV,'rb').read()).hexdigest(),
   "corpus_fingerprint_sha256": hashlib.sha256(corpus_canon.encode('utf-8')).hexdigest(),
   "corpus_document_count": len(ev['documents']),
   "note":"Only the documents[] array of EVAL_SET.json was read as corpus; labeled_queries/no_answer_queries were not used as label input."
 },
 "label_summary":{"total":50,"answerable_true":n_true,"answerable_false":50-n_true},
 "items":items,
}
Path('05_TEST/BLIND_LABELS_QW_PASS1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding='utf-8')
print("answerable true:",n_true,"false:",50-n_true)
print("written 05_TEST/BLIND_LABELS_QW_PASS1.json")
