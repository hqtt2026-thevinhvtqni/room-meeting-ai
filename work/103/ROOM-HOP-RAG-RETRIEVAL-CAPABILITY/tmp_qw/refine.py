import json, re, hashlib, subprocess
from pathlib import Path

POOL='05_TEST/BLIND_RETRIEVAL_CHALLENGE_POOL_V1.json'
EV='05_TEST/EVAL_SET.json'
S_ONT='docs/bien-ban-hop-tuan-ont.md'; S_QT='docs/quy-trinh-xu-ly-su-co-mang.md'
S_GH='docs/ke-hoach-giao-hang.md';    S_DT='docs/bao-cao-doanh-thu.md'
S_KL='docs/ky-luat-hop.md';           S_BM='docs/bao-mat-thong-tin.md'
S_NV='docs/nhiem-vu-tuan-42.md';      S_CT='docs/quy-dinh-cong-tac.md'

# QW PASS-1 labels (independent). confidence: HIGH = explicit fact in listed source(s);
# MEDIUM = answer requires multi-line/multi-doc aggregation or a semantic bridge.
LAB={
"Q001":(False,[],"HIGH","Corpus chi co bao cao doanh thu QUY 3 (120% ke hoach); quy 4 chi la DU BAO 'tang truong on dinh', khong co so lieu va khong cat theo chi nhanh; 'Ha Noi' khong xuat hien trong tai lieu nao."),
"Q002":(True,[S_KL],"HIGH","docs/ky-luat-hop.md ghi toan bo noi dung ky luat hop tuan: phat di muon 50 nghin, dien thoat che do im lang, vang mat phai bao truoc 1 ngay, hop 8 gio sang thu hai."),
"Q003":(False,[],"HIGH","Bien ban ONT chi ghi tin hieu yeu o KHU B va khong ghi gia tri dBm cho bat ky khu nao; 'khu C' + don vi dBm deu khong ton tai trong corpus."),
"Q004":(True,[S_QT],"HIGH","docs/quy-trinh-xu-ly-su-co-mang.md liet ke du 5 buoc: tiep nhan ticket -> kiem tra LOS va do RX power tren ONT -> ve sinh dau noi quang -> escalate NOC neu LOS keo dai qua 30 phut -> ghi ket qua vao bien ban."),
"Q005":(False,[],"HIGH","Khong co so lieu doanh thu quy 4, khong co 'van phong chi nhanh Da Nang' trong corpus; bao cao chi lap o muc toan cong ty cho quy 3."),
"Q006":(True,[S_CT],"HIGH","docs/quy-dinh-cong-tac.md: ve may bay can quan ly truc tiep phe duyet, ho tro per diem 500 nghin/ngay, khach san hoan qua ke toan, bao cao cong tac trong 3 ngay sau khi ve."),
"Q007":(False,[],"HIGH","Dong 'LOS alarm xuat hien luc 3 gio sang' gan voi su co KHU B; corpus khong nhac den khu C nen khong the gan moc gio cho khu C (near-miss doi tuong/chu the)."),
"Q008":(True,[S_BM],"HIGH","docs/bao-mat-thong-tin.md: khong chia se mat khau qua email, token truy cap luu trong vault, xoa du lieu khach hang sau 30 ngay, ro ri thong tin phai bao ngay cho bao mat."),
"Q009":(False,[],"HIGH","Corpus khong chua bat ky gia tri do RX power/dBm nao; bien ban chi ghi nguoi phu trach kiem tra RX power, khong co so do va khong co 'khu A'."),
"Q010":(True,[S_GH],"HIGH","docs/ke-hoach-giao-hang.md: ke hoach giao hang xi mang quy 4, khach hang dat 5000 tan, lich giao 5/11, 12/11 va 19/11."),
"Q011":(False,[],"HIGH","Quy dinh chung: ve may bay can 'quan ly truc tiep' phe duyet; nhung corpus khong co chuyen di Ha Noi tuan sau va khong dinh danh nguoi cu the cho lo trinh nay."),
"Q012":(True,[S_DT],"HIGH","docs/bao-cao-doanh-thu.md: doanh thu quy 3 dat 120% ke hoach, sales dan dau doanh so, du bao quy 4 tang truong on dinh, ke toan xac nhan so lieu ngay 5/10."),
"Q013":(False,[],"HIGH","Khong co so lieu doanh thu quy 4; khong tai lieu nao nhac den bo phan marketing (chi co 'sales')."),
"Q014":(True,[S_NV],"HIGH","docs/nhiem-vu-tuan-42.md: Nguyen Van A viet bao cao tin hieu quang, Tran B ho tro trien khai sales tai chi nhanh, cap nhat vault token he thong truoc thu sau, chuan bi bien ban hop tuan toi."),
"Q015":(False,[],"HIGH","Lich giao chi co ba moc thang 11 (5/11, 12/11, 19/11); khong co 'chi nhanh mien Trung' cung khong co moc thang 12."),
"Q016":(True,[S_QT],"HIGH","Quy trinh mo ta tuyen tinh tu buoc 1: tiep nhan ticket tu khach hang -> buoc 2 kiem tra LOS/do RX power tren ONT -> buoc 3 ve sinh dau noi quang -> buoc 4 escalate NOC neu LOS qua 30 phut -> buoc 5 ghi ket qua vao bien ban."),
"Q017":(False,[],"HIGH","Han chot xu ly su co trong corpus la 20/10 gan voi su co KHU B; khong co 'khu C' va khong co moc 15/11, nen khong the xac dinh nguoi chiu trach nhiem nhu cau hoi."),
"Q018":(True,[S_ONT,S_QT],"MEDIUM","Hai nguon bo sung nhau: bien ban ONT noi su co tin hieu yeu o khu B va de xuat ve sinh dau noi cap quang; quy trinh neu cac buoc kiem tra LOS/do RX power va ve sinh dau noi quang. Khong tai lieu nao liet ke thanh 'cac bien phap xu ly tin hieu yeu' nhu mot danh muc."),
"Q019":(False,[],"HIGH","Muc phat 50 nghin thuoc 'ky luat hop tuan cua phong'; corpus khong gan quy dinh nao voi chi nhanh Ha Noi."),
"Q020":(True,[S_BM],"MEDIUM","Nghia vu bao cho bao mat duoc ghi ro ('Ro ri thong tin phai bao ngay cho bao mat'); nhung cau hoi hoi 'nhung truong hop' so luong nhieu hon mot thi corpus chi cung cap DUOC MOT truong hop cu the."),
"Q021":(False,[],"HIGH","Corpus chi yeu cau token luu trong vault va 'cap nhat vault token he thong truoc thu sau'; khong tai lieu nao dinh nghia chu ky doi token theo so ngay, cung khong noi 'token API'."),
"Q022":(True,[S_CT],"HIGH","Cac khoan lien quan cong tac: ve may bay (can phe duyet), per diem 500 nghin moi ngay, khach san hoan qua ke toan."),
"Q023":(False,[],"HIGH","Tai lieu chi ghi 'Khach san hoan qua ke toan' (quy/cach thuc hoan), khong co muc tran toi da tien hoan moi dem."),
"Q024":(True,[S_GH],"HIGH","docs/ke-hoach-giao-hang.md: 'Lich giao: 5/11, 12/11 va 19/11' trong ke hoach giao hang xi mang quy 4."),
"Q025":(False,[],"HIGH","Con so 120% ke hoach la doanh thu quy 3 o cap bao cao chung, khong phai cua 'chi nhanh Ha Noi'; corpus khong cat so lieu theo chi nhanh."),
"Q026":(True,[S_NV],"MEDIUM","Viec duy nhat co moc 'truoc thu sau' la 'Cap nhat vault token he thong truoc thu sau'; cac dong khong trong danh sach co gan moc thoi gian nao."),
"Q027":(False,[],"HIGH","Quy trinh neu nguong 30 PHUT de KY THUAT VIEN escalate cho NOC, khong phai SLA xu ly cua NOC va khong phai don vi GIO; corpus khong co SLA cho NOC."),
"Q028":(True,[S_BM,S_NV],"MEDIUM","Token truy cap phai luu trong vault (bao-mat-thong-tin) va viec cap nhat vault token he thong truoc thu sau (nhiem-vu-tuan-42)."),
"Q029":(False,[],"HIGH","Corpus khong co danh sach khach hang no qua han cung khong co du lieu cong no."),
"Q030":(True,[S_KL],"HIGH","Hop 8 gio sang thu hai; vang mat phai bao truoc 1 ngay; dien thoat de che do im lang; di muon phat 50 nghin."),
"Q031":(False,[],"HIGH","Pham vi phe duyet trong quy dinh cong tac chi lap cho 've may bay'; khong tai lieu nao nhac den chi phi taxi hay nguoi duyet loai chi phi nay."),
"Q032":(True,[S_DT,S_GH,S_NV],"MEDIUM","Doanh thu: quy 3 dat 120% ke hoach, sales dan dau doanh so, du bao quy 4 on dinh, ke toan xac nhan 5/10 (bao-cao-doanh-thu). Sales con xuat hien voi vai tro phu trach giao hang (ke-hoach-giao-hang) va ho tro trien khai sales tai chi nhanh (nhiem-vu-tuan-42)."),
"Q033":(False,[],"HIGH","Corpus khong ghi viec THAY THIET BI cho ONT khu nao; chi co de xuat ve sinh dau noi va han chot xu ly 20/10."),
"Q034":(True,[S_QT,S_NV,S_ONT],"MEDIUM","Buoc 5 quy trinh: ghi nhan ket qua vao bien ban; nhiem vu tuan 42: chuan bi bien ban hop tuan toi; chinh bien ban ONT la tai lieu hop tuan duoc lap."),
"Q035":(False,[],"HIGH","Ky luat hop ghi hop 8 GIO SANG THU HAI cua phong; khong co lich 'chieu thu sau' va khong co thong tin theo chi nhanh Ha Noi."),
"Q036":(True,[S_QT],"HIGH","Buoc 4 va buoc 5: escalate cho NOC neu LOS keo dai qua 30 phut; ghi nhan ket qua vao bien ban."),
"Q037":(False,[],"HIGH","Bao cao doanh thu chi o cap bo phan; khong co doanh thu theo tung nhan vien, cung khong co so lieu thang 10."),
"Q038":(True,[S_CT],"MEDIUM","Nghia vu sau chuyen cong tac: bao cao cong tac trong 3 ngay sau khi ve; khach san hoan qua ke toan (len quan sau khi ve)."),
"Q039":(False,[],"HIGH","Chinh sach chi cam ket khong chia se mat khau qua email va token luu vault; khong yeu cau do dai toi thieu cho mat khau vault."),
"Q040":(True,[S_KL,S_ONT],"MEDIUM","Ky luat hop: hop tuan cua phong 8 gio sang thu hai; bien ban ONT: cuoc hop tuan ONT ngay 12/10."),
"Q041":(False,[],"HIGH","Tai lieu chi la KE HOACH (5000 tan duoc dat, lich co 19/11); khong co so lieu giao THUC TE cua ngay 19/11."),
"Q042":(False,[],"HIGH","Xac nhan so lieu ke toan ngay 5/10 gan voi bao cao QUY 3 va khong ghi ten nguoi ky; khong co xac nhan cho doanh thu quy 4."),
"Q043":(False,[],"HIGH","Quy trinh trong corpus la xu ly su CO MANG (LOS/RX power/dau noi quang/NOC); khong co quy trinh su co DIEN tai van phong."),
"Q044":(False,[],"HIGH","Per diem 500 nghin moi ngay la muc chung cua quy dinh cong tac xa; khong tai lieu nao phan theo quoc gia hay nhac den Nhat Ban."),
"Q045":(False,[],"HIGH","Corpus khong co su co khu C va khong co trang thai 'khac phuc xong' cho bat ky su co nao (chi co de xuat va han chot 20/10 cho khu B)."),
"Q046":(False,[],"HIGH","Ngay 5/10 la ngay ke toan xac nhan so lieu cho bao cao doanh thu QUY 3; khong co ngay xac nhan cho quy 4."),
"Q047":(False,[],"HIGH","Corpus khong co so luong ticket LOS theo tuan; 'tuan 42' chi gan voi danh sach nhiem vu."),
"Q048":(False,[],"HIGH","Chinh sach neu kenh bi cam la EMAIL; khong tai lieu nao de cap Zalo hay viec chia se file qua ung nhan nay."),
"Q049":(False,[],"HIGH","Doanh so dan dau ghi o cap BO PHAN (sales) cho quy 3; khong co xep hang theo CHI NHANH va khong co so lieu quy 4."),
"Q050":(False,[],"HIGH","LOS alarm luc 3 gio sang va bien ban ngay 12/10 co ton tai, nhung corpus khong ghi danh tinh nguoi truc ca/truc NOC."),
}

pool=json.load(open(POOL)); ev=json.load(open(EV))
valid={d['source_id'] for d in ev['documents']}
items=pool['items']
assert len(items)==50 and set(LAB)=={i["id"] for i in items}
for it in items:
    a,srcs,conf,rat=LAB[it["id"]]
    assert (not a) == (srcs==[])
    if a: assert all(s in valid for s in srcs) and len(set(srcs))==len(srcs)
    it.update(answerable=a, expected_source_ids=srcs, annotator_rationale=rat,
              confidence=conf, annotation_status="LABELED_PASS1_INDEPENDENT")

corpus_canon='\n'.join(f"{d['source_id']}\x1f{d['text']}" for d in ev['documents'])
nt=sum(1 for i in items if i['answerable']); nm=sum(1 for i in items if i.get('confidence')=='MEDIUM')
qh=sorted(i['id'] for i in items if i.get('confidence')=='MEDIUM')
out={
 "schema_version":1,
 "record_type":"blind_annotation_pass1",
 "title":"Work 103 blind retrieval challenge — QW annotation record, PASS 1 (independent)",
 "annotator_id":"QW-QE-PASS1",
 "annotator_role":"Qw — QE/QA independent testing (not the pool author, not the retrieval implementer)",
 "annotated_at_utc":"2026-10-28T12:00:00Z",
 "status":"PASS1_INDEPENDENT_NOT_FROZEN_NOT_FOR_METRIC_REPORTING",
 "pool_file":"05_TEST/BLIND_RETRIEVAL_CHALLENGE_POOL_V1.json",
 "blindness_protocol":[
   "Inputs used: pool item ID + query text only, plus the committed corpus documents (source_id/title/text).",
   "Not consulted as labeling input: retrieval scores, rankings, system outputs, baseline metrics, EVAL_SET labeled_queries/no_answer_queries ground truth, and the author candidate list.",
   "Labels assigned strictly by the labeling_rules of BLIND_RETRIEVAL_CHALLENGE_POOL_V1.json before any comparison with author labels.",
   "Self-check performed AFTER labeling, using corpus text only (query-token coverage per document) to catch missed support and over-claimed sources; no ranking/score data used.",
   "Pass 1 of an independent double-annotation scheme: disagreements with pass 2 must be resolved before unblinding, then the labeled-set version/hash is frozen."
 ],
 "labeling_rule_interpretation":[
   "R1 (strict explicit support): answerable=true only when a committed document states the requested fact; queries that add an unsupported object/attribute (khu C, khu A, chi nhanh Ha Noi/Da Nang/mien Trung, marketing, NOC duty roster, actual delivered quantity, taxi cost, Japan per diem, Zalo sharing, password length, token rotation period, hotel cap, SLA hours, device replacement, resolution status, Q4-specific figures/signers/rankings) are answerable=false.",
   "R2 (enumeration/summary queries): true when one document enumerates the requested content (Q002, Q004, Q006, Q008, Q010, Q012, Q014, Q016, Q022, Q024, Q030, Q036).",
   "R3 (multi-source aggregation): true when two or more documents materially contribute (Q018, Q028, Q032, Q034, Q040); each contributing source listed.",
   "R4 (single-instance answers to plural questions): counted answerable=true with MEDIUM confidence but flagged for adjudication (Q020, Q026, Q038).",
   "R5 (unit/role mismatch): '30 phut' is an escalation trigger for the technician, not an NOC handling SLA in hours -> Q027 false.",
   "R6 (planned vs actual): plan dates/values never establish actual outcomes -> Q041 false.",
   "R7 (no-answer label): every answerable=false item carries expected_source_ids=[] per rule 3."
 ],
 "provenance":{
   "branch_head_commit":subprocess.check_output(['git','-C','/workspace','rev-parse','HEAD']).decode().strip(),
   "pool_file_sha256":hashlib.sha256(open(POOL,'rb').read()).hexdigest(),
   "eval_set_file_sha256":hashlib.sha256(open(EV,'rb').read()).hexdigest(),
   "corpus_fingerprint_sha256":hashlib.sha256(corpus_canon.encode('utf-8')).hexdigest(),
   "corpus_document_count":len(ev['documents']),
   "corpus_source_ids":[d['source_id'] for d in ev['documents']],
   "note":"Only the documents[] array of EVAL_SET.json was read as corpus; its labeled_queries/no_answer_queries arrays were not used as label input."
 },
 "label_summary":{"total":50,"answerable_true":nt,"answerable_false":50-nt,
                  "confidence_high":50-nm,"confidence_medium":nm,"medium_confidence_ids":qh},
 "open_questions_for_adjudication":[
   "Q018/Q020/Q026/Q032/Q034/Q038/Q040: scope of enumeration/summary queries — accept single-instance or partial lists as material support, or require an explicit consolidated statement?",
   "Q034: should docs/bien-ban-hop-tuan-ont.md itself be listed (it is an instance of a meeting minute, not a statement about minute-related work)?",
   "Q032: breadth boundary — bao-cao-doanh-thu.md clearly supports 'doanh thu'; ke-hoach-giao-hang.md and nhiem-vu-tuan-42.md support 'sales' only. Confirm whether listing all three is required or acceptable.",
   "Q027: if the project defines 'SLA' loosely as any time bound in the procedure, Q027 would flip to true with docs/quy-trinh-xu-ly-su-co-mang.md; recorded here as false under R5.",
   "Q007/Q017/Q003/Q009/Q045: near-miss entity swaps (khu C/khu A) — confirm these stay answerable=false rather than 'partially answerable'."
 ],
 "items":items,
}
Path('05_TEST/BLIND_LABELS_QW_PASS1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding='utf-8')
print("true:",nt,"false:",50-nm*0-nt,"medium:",nm,qh)
print("sha256 of label file:",hashlib.sha256(Path('05_TEST/BLIND_LABELS_QW_PASS1.json').read_bytes()).hexdigest())
