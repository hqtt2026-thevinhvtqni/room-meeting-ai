(() => {
  const el = (tag, cls, text) => { const n=document.createElement(tag); if(cls)n.className=cls; if(text!==undefined)n.textContent=text; return n; };
  const card=(label,value,hint)=>{const n=el('article','metric');n.append(el('span','muted',label),el('strong','metric-value',value),el('small','muted',hint));return n;};
  const pill=(text,state='neutral')=>el('span','pill pill-'+state,text);
  const section=(title,sub)=>{const n=el('div','section-title');n.append(el('h2','',title),el('p','muted',sub));return n;};
  const table=(headers,rows)=>{const wrap=el('div','table-wrap'),t=el('table'),thead=el('thead'),hr=el('tr');headers.forEach(h=>hr.append(el('th','',h)));thead.append(hr);const tb=el('tbody');rows.forEach(row=>{const tr=el('tr');row.forEach(cell=>{const td=el('td');if(typeof cell==='string')td.textContent=cell;else td.append(cell);tr.append(td)});tb.append(tr)});t.append(thead,tb);wrap.append(t);return wrap;};
  const note=(title,body,state='warn')=>{const n=el('div','notice notice-'+state);n.append(el('strong','',title),el('p','',body));return n;};
  const stateFor=s=>s==='ONLINE'?'good':s==='WARNING'?'warn':s==='OFFLINE'?'bad':'neutral';
  window.PreviewRenderers={
    dashboard:(v,d)=>{
      v.append(note('BẢN XEM TRƯỚC · MOCK DATA','Các con số và bản ghi dưới đây chỉ minh họa giao diện. Chưa phải dữ liệu đọc từ ONT thật.','info'));
      v.append(section('Tổng quan vận hành','Theo dõi ONT, chất lượng kết nối và công việc cần xử lý'));
      const metrics=el('div','metrics');d.summary.forEach(x=>metrics.append(card(x.label,x.value,x.hint)));v.append(metrics);
      const grid=el('div','content-grid'),left=el('section','panel'),right=el('section','panel');
      left.append(section('Thiết bị gần đây','Mỗi bản ghi gắn nguồn MOCK'));
      left.append(table(['ONT / khách hàng','Model','Tín hiệu quang','Trạng thái'],d.onts.map(o=>[o.id+' · '+o.customer,o.model,o.signal,pill(o.status,stateFor(o.status))])));
      right.append(section('Sự cố cần chú ý','Fixture minh họa'));
      right.append(table(['Ticket','Mức độ','Trạng thái'],d.tickets.map(t=>[t.id+' · '+t.title,t.priority,pill(t.status,t.status==='OPEN'?'bad':'warn')])));
      grid.append(left,right);v.append(grid);
      v.append(note('Runtime chưa xác minh','Build và E2E vẫn NOT RUN/BLOCKED. Không coi dữ liệu minh họa là trạng thái hệ thống thật.','warn'));
    },
    customer:(v,d)=>{
      v.append(note('APP KHÁCH HÀNG · DEMO','Luồng UI minh họa; đăng nhập, quyền truy cập và dữ liệu thật chưa được xác minh.','info'));
      v.append(section('Internet nhà bạn','Bố cục mục tiêu cho khách hàng'));
      const phone=el('div','phone-frame'),hero=el('div','phone-hero');
      hero.append(el('div','eyebrow','ONT CARE'),el('h2','','Kết nối Internet'),el('p','','Trạng thái minh họa — MOCK'),pill('DEMO · NOT LIVE','warn'));phone.append(hero);
      const body=el('div','phone-body');body.append(card('Thiết bị','ONT-DEMO-001','Fixture'),card('Tín hiệu quang','-21.4 dBm','Mock value'),card('Yêu cầu hỗ trợ','TK-DEMO-101','Demo ticket'));
      body.append(note('Tạo yêu cầu hỗ trợ','Luồng thật cần lưu ticket và chỉ cho khách xem ticket thuộc tài khoản đã xác thực.','info'));phone.append(body);v.append(phone);
    },
    technician:(v,d)=>{
      v.append(note('APP KỸ THUẬT VIÊN · DEMO','Luồng minh họa. Không chạy lệnh thay đổi cấu hình ONT trong preview.','info'));
      v.append(section('Công việc kỹ thuật','Nhận việc → chẩn đoán read-only → ghi kết quả → xác nhận'));
      v.append(table(['Ticket','Thiết bị','Trạng thái','Bước an toàn tiếp theo'],d.tickets.map(t=>[t.id+' · '+t.title,'ONT-DEMO-001',pill(t.status,t.status==='OPEN'?'bad':'warn'),'Thu thập diagnostic chỉ đọc'])));
      v.append(note('Ranh giới quyền','Ứng dụng thật phải kiểm tra role ở trusted service/local-agent boundary; ẩn nút UI không đủ.','warn'));
    },
    journeys:(v,d)=>{
      v.append(section('E2E Journey','Chỉ hiển thị kết quả khi có log thực thi'));
      v.append(table(['Journey','Trạng thái','Bằng chứng / ghi chú'],d.journeys.map(x=>[x.name,pill(x.state,x.state==='PASS'?'good':x.state==='BLOCKED'?'bad':'warn'),x.detail])));
      v.append(note('Chưa có E2E PASS','Các journey đang NOT RUN/BLOCKED; không suy diễn PASS từ việc source tồn tại.','warn'));
    },
    evidence:(v,d)=>{
      v.append(section('Build & Evidence','Tình trạng xác minh hiện tại'));
      const metrics=el('div','metrics');metrics.append(card('Build',d.meta.build_status,'Chưa chạy trong Sandbox'),card('Lint / typecheck','NOT RUN','Chưa có exit code'),card('Browser E2E',d.meta.runtime_test,'Chưa có log'),card('Source revision','UNKNOWN','Chưa có Git repository'));v.append(metrics);
      v.append(note('Lý do BLOCKED','Đã xác minh được công cụ MCP đọc/ghi file; chưa tìm thấy công cụ thực thi lệnh trong Sandbox. Không tạo bằng chứng giả.','warn'));
      v.append(table(['Trường','Giá trị'],Object.entries(d.meta).map(([k,val])=>[k,String(val)])));
    },
    structure:(v,d)=>{v.append(section('Sandbox source tree','Danh sách source không phải product preview'));v.append(table(['#','Path'],d.entries.map((p,i)=>[String(i+1),p])));},
    meta:(v,d)=>{v.append(section('Metadata','Snapshot metadata'));v.append(table(['Field','Value'],Object.entries(d.meta).map(([k,val])=>[k,String(val)])));}
  };
})();