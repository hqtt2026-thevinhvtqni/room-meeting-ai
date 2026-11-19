let data = null;
let refreshTimer;
let heartbeatTimer;
let reconnectTimer;
let reconnectAttempt = 0;
let requestInFlight = false;
const BACKOFF = [5000, 10000, 20000, 40000, 60000];
const tone = (s) => ({OPEN:'amber',BLOCKED:'red','NOT VERIFIED':'slate',CONFLICT:'red',PARTIAL:'amber',REFRESHED:'teal','IN PROGRESS':'amber','NOT STARTED':'slate',PENDING:'slate',LOCKED:'red','DESIGN ONLY':'slate'}[s] || 'slate');
const badge = (s) => `<span class="badge ${tone(s)}">${s}</span>`;
const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));

function setConnection(state, message = '', retryMs = 0) {
  const el = document.querySelector('#liveStatus');
  const alert = document.querySelector('#connectionAlert');
  const button = document.querySelector('#refreshLive');
  if (!el || !alert) return;
  const labels = {
    live: ['MCP LIVE', 'Kết nối MCP đang hoạt động'],
    cache: ['MCP CACHE', 'Bridge MCP chưa cấu hình · đang dùng cache'],
    reconnecting: ['MCP RECONNECTING', 'Đang tự động thử kết nối lại'],
    offline: ['MCP OFFLINE', 'Mất kết nối MCP · dữ liệu cuối vẫn được giữ']
  };
  const [label, defaultMessage] = labels[state] || labels.cache;
  const seconds = Math.max(1, Math.ceil(retryMs / 1000));
  const timestamp = data?.meta?.syncedAt ? new Date(data.meta.syncedAt).toLocaleString('vi-VN') : 'chưa có timestamp';
  el.className = `live-status state-${state}`;
  el.innerHTML = `<span class="live-led"></span><div><strong>${label}</strong><span>${esc(message || defaultMessage)}</span></div><small>${esc(timestamp)}</small>`;
  if (state === 'live' || state === 'cache') {
    alert.hidden = true;
  } else {
    alert.hidden = false;
    alert.className = `connection-alert alert-${state}`;
    alert.innerHTML = `<span class="alert-icon">${state === 'offline' ? '!' : '↻'}</span><div><strong>${state === 'offline' ? 'MCP connection lost' : 'Reconnecting to MCP'}</strong><span>${esc(message || 'Dashboard vẫn hiển thị dữ liệu cuối cùng đã đồng bộ.')} ${retryMs ? `Lần thử tiếp theo sau ${seconds}s.` : ''}</span></div>`;
  }
  if (button) {
    button.disabled = requestInFlight;
    button.textContent = requestInFlight ? 'Đang đồng bộ…' : 'Refresh MCP';
  }
}

function render() {
  if (!data) return;
  const status = document.querySelector('#statusFilter').value;
  const priority = document.querySelector('#priorityFilter').value;
  const gate = document.querySelector('#gateFilter').value;
  const q = document.querySelector('#searchFilter').value.toLowerCase();
  const { summary, gates, portfolio, agents, members, gaps, e2e } = data;

  document.querySelector('#kpis').innerHTML = [
    [summary.works, 'Works in Sandbox', 'MCP summary'],
    [`${summary.mirrors} / ${summary.works}`, 'GitHub mirrors', `${portfolio.missingMirrors} missing · P1`],
    [`${summary.agentsRead} / 13`, 'Agent types read', '0 with E2+'],
    [summary.p0Open, 'P0 gaps open', 'G3 blocked']
  ].map(([n, l, s]) => `<div class="kpi"><strong>${esc(n)}</strong><span>${esc(l)}</span><small>${esc(s)}</small></div>`).join('');

  document.querySelector('#gates').innerHTML = gates
    .filter(x => gate === 'all' || x.id === gate)
    .map(x => `<div class="gate-row"><span class="gate-id">${esc(x.id)}</span><div class="gate-main"><strong>${esc(x.name)}</strong><span>${esc(x.detail)}</span></div>${badge(x.state)}</div>`)
    .join('');

  const coverage = Math.round((portfolio.mirrors / portfolio.works) * 100) || 0;
  document.querySelector('#portfolio').innerHTML = `
    <div class="ring" style="background: conic-gradient(var(--teal) 0 ${coverage}%, #dce9e8 ${coverage}% 100%)">
      <div><strong>${coverage}%</strong><span>mirror coverage</span></div>
    </div>
    <div class="portfolio-stats">
      <div><strong>${portfolio.works}</strong><span>Sandbox registry</span></div>
      <div><strong>${portfolio.mirrors}</strong><span>GitHub workfolders</span></div>
      <div><strong>${portfolio.missingMirrors}</strong><span>mirror missing</span></div>
    </div>
    <div class="portfolio-note">Work 17 is ACTIVE and exists in both Sandbox and GitHub work/17, but parity is not globally proven.</div>`;

  document.querySelector('#agents').innerHTML = `<table><thead><tr><th>Agent type</th><th>Evidence</th><th>Finding</th><th>Source</th></tr></thead><tbody>${agents.map(a => `<tr><td>${esc(a[0])}</td><td>${badge(a[1])}</td><td>${esc(a[2])}</td><td><code>${esc(a[3])}</code></td></tr>`).join('')}</tbody></table>`;

  document.querySelector('#members').innerHTML = members.map(m => `<div class="member-row"><div class="avatar">${esc(m[0].slice(-2))}</div><div><strong>${esc(m[0])} · ${esc(m[1])}</strong><span>${esc(m[2])}</span><span>${esc(m[3])}</span></div></div>`).join('');

  const filtered = gaps.filter(g =>
    (status === 'all' || g[4] === status) &&
    (priority === 'all' || g[3] === priority) &&
    (gate === 'all' || g[6] === gate) &&
    (!q || g.join(' ').toLowerCase().includes(q))
  );
  document.querySelector('#gapCount').textContent = `${filtered.length} SHOWN / ${gaps.length} TOTAL`;
  document.querySelector('#gaps').innerHTML = filtered.map(g =>
    `<article class="gap-row">
      <div class="gap-priority ${g[3].toLowerCase()}">${esc(g[3])}</div>
      <div class="gap-content">
        <div class="gap-title"><strong>${esc(g[0])} · ${esc(g[1])}</strong>${badge(g[4])}</div>
        <span class="muted">${esc(g[2])} · ${esc(g[6])}</span>
        <p>${esc(g[5])}</p>
      </div>
    </article>`
  ).join('') || '<div class="empty">Không có mục phù hợp bộ lọc.</div>';

  document.querySelector('#e2e').innerHTML = e2e.map((x, i) =>
    `<div class="trace-step">
      <div class="trace-number">${esc(x[0])}</div>
      <div class="trace-copy"><strong>${esc(x[1])}</strong><span>${esc(x[2])}</span><small>${esc(x[3])}</small></div>
      ${badge(x[4])}
      ${i < e2e.length - 1 ? '<div class="trace-line"></div>' : ''}
    </div>`
  ).join('');
}

function scheduleReconnect(reason) {
  clearTimeout(reconnectTimer);
  const retryMs = BACKOFF[Math.min(reconnectAttempt, BACKOFF.length - 1)];
  reconnectAttempt += 1;
  setConnection(reconnectAttempt >= 3 ? 'offline' : 'reconnecting', `${reason} Dữ liệu cuối cùng vẫn được giữ nguyên.`, retryMs);
  reconnectTimer = setTimeout(() => refreshLive(true), retryMs);
}

async function refreshLive(isReconnect = false) {
  if (requestInFlight) return;
  requestInFlight = true;
  clearTimeout(reconnectTimer);
  setConnection(
    isReconnect ? 'reconnecting' : (data?.meta?.bridgeConfigured ? 'reconnecting' : 'cache'),
    isReconnect ? `Lần thử reconnect #${reconnectAttempt + 1}.` : 'Đang kiểm tra nguồn dữ liệu…'
  );
  try {
    const response = await fetch(`/api/live?at=${Date.now()}`, { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const next = await response.json();
    data = next;
    const live = next.meta?.source === 'mcp-live' && next.meta?.fresh;
    if (live) {
      reconnectAttempt = 0;
      setConnection('live');
    } else if (next.meta?.bridgeConfigured && next.meta?.warning) {
      scheduleReconnect(next.meta.warning);
    } else {
      reconnectAttempt = 0;
      setConnection('cache');
    }
    render();
  } catch (error) {
    scheduleReconnect(`Không đọc được live data: ${error.message}`);
  } finally {
    requestInFlight = false;
    const button = document.querySelector('#refreshLive');
    if (button) {
      button.disabled = false;
      button.textContent = 'Refresh MCP';
    }
  }
}

async function heartbeat() {
  try {
    const response = await fetch(`/api/health?at=${Date.now()}`, { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    if (!data || data.meta?.bridgeConfigured) refreshLive(Boolean(reconnectAttempt));
  } catch (error) {
    scheduleReconnect(`Heartbeat thất bại: ${error.message}`);
  }
}

['statusFilter', 'priorityFilter', 'gateFilter', 'searchFilter'].forEach(id => {
  const el = document.getElementById(id);
  if (el) el.addEventListener(id === 'searchFilter' ? 'input' : 'change', () => data && render());
});

document.querySelector('#refreshLive')?.addEventListener('click', () => {
  reconnectAttempt = 0;
  refreshLive(false);
});

refreshLive();
refreshTimer = setInterval(() => refreshLive(false), 30000);
heartbeatTimer = setInterval(heartbeat, 15000);
