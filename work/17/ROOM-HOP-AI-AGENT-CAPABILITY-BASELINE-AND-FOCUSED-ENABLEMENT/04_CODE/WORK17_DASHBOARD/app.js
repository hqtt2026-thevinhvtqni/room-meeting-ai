let data = null;
let refreshTimer;
let heartbeatTimer;
let reconnectTimer;
let reconnectAttempt = 0;
let requestInFlight = false;
const BACKOFF = [5000, 10000, 20000, 40000, 60000];
const $ = (selector) => document.querySelector(selector);
const tone = (s) => ({OPEN:'amber',BLOCKED:'red','NOT VERIFIED':'slate',CONFLICT:'red',PARTIAL:'amber',REFRESHED:'teal','IN PROGRESS':'amber','NOT STARTED':'slate',PENDING:'slate',LOCKED:'red','DESIGN ONLY':'slate'}[s] || 'slate');
function esc(value) {
  return String(value ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}
const badge = (s) => '<span class="badge ' + tone(s) + '">' + esc(s) + '</span>';

function validClientPayload(v) {
  const obj = (x) => x !== null && typeof x === 'object' && !Array.isArray(x);
  const str = (x) => typeof x === 'string';
  const num = (x) => typeof x === 'number' && Number.isFinite(x);
  if (!obj(v) || !obj(v.meta) || !Number.isFinite(Date.parse(v.meta.syncedAt || ''))) return false;
  if (!obj(v.summary) || !['works','mirrors','agentsRead','p0Open'].every(k => num(v.summary[k]))) return false;
  if (!obj(v.portfolio) || !['works','mirrors','missingMirrors'].every(k => num(v.portfolio[k]))) return false;
  if (!Array.isArray(v.gates) || !v.gates.every(x => obj(x) && ['id','name','state','detail'].every(k => str(x[k])))) return false;
  return [[v.agents,4],[v.members,4],[v.gaps,7],[v.e2e,5]].every(([rows,n]) =>
    Array.isArray(rows) && rows.every(row => Array.isArray(row) && row.length === n && row.every(str))
  );
}

function setConnection(state, message = '', retryMs = 0) {
  const el = $('#liveStatus');
  const alert = $('#connectionAlert');
  const button = $('#refreshLive');
  if (!el || !alert) return;
  const labels = {
    live: ['MCP LIVE', 'Nguồn MCP thật đã qua kiểm tra schema và freshness'],
    cache: ['MCP CACHE', 'Đang dùng dữ liệu cache; không phải dữ liệu live'],
    reconnecting: ['MCP RECONNECTING', 'Đang tự động thử kết nối lại'],
    offline: ['MCP OFFLINE', 'Mất kết nối MCP · dữ liệu cache cuối vẫn được giữ']
  };
  const [label, fallback] = labels[state] || labels.cache;
  const timestamp = data?.meta?.syncedAt ? new Date(data.meta.syncedAt).toLocaleString('vi-VN') : 'chưa có timestamp';
  el.className = `live-status state-${state}`;
  el.innerHTML = `<span class="live-led"></span><div><strong>${label}</strong><span>${esc(message || fallback)}</span></div><small>${esc(timestamp)}</small>`;
  if (state === 'live' || (state === 'cache' && !message)) {
    alert.hidden = true;
  } else {
    alert.hidden = false;
    alert.className = `connection-alert alert-${state}`;
    alert.innerHTML = `<span class="alert-icon">${state === 'offline' ? '!' : '↻'}</span><div><strong>${state === 'offline' ? 'MCP connection lost' : 'MCP data warning'}</strong><span>${esc(message || 'Dashboard đang giữ dữ liệu cache.')} ${retryMs ? `Lần thử tiếp theo sau ${Math.ceil(retryMs / 1000)}s.` : ''}</span></div>`;
  }
  if (button) {
    button.disabled = requestInFlight;
    button.textContent = requestInFlight ? 'Đang đồng bộ…' : 'Refresh MCP';
  }
}

function render() {
  if (!data || !validClientPayload(data)) throw new Error('Payload không hợp lệ; từ chối render');
  const status = $('#statusFilter')?.value || 'all';
  const priority = $('#priorityFilter')?.value || 'all';
  const gate = $('#gateFilter')?.value || 'all';
  const q = ($('#searchFilter')?.value || '').toLowerCase();
  const { summary, gates, portfolio, agents, members, gaps, e2e } = data;

  const kpis = $('#kpis');
  if (kpis) kpis.innerHTML = [
    [summary.works, 'Works in Sandbox', 'MCP summary'],
    [`${summary.mirrors} / ${summary.works}`, 'GitHub mirrors', `${portfolio.missingMirrors} missing · P1`],
    [`${summary.agentsRead} / 13`, 'Agent types read', '0 with E2+'],
    [summary.p0Open, 'P0 gaps open', 'G3 blocked']
  ].map(([n,l,s]) => `<div class="kpi"><strong>${esc(n)}</strong><span>${esc(l)}</span><small>${esc(s)}</small></div>`).join('');

  const gateEl = $('#gates');
  if (gateEl) gateEl.innerHTML = gates.filter(x => gate === 'all' || x.id === gate)
    .map(x => `<div class="gate-row"><span class="gate-id">${esc(x.id)}</span><div class="gate-main"><strong>${esc(x.name)}</strong><span>${esc(x.detail)}</span></div>${badge(x.state)}</div>`).join('');

  const coverage = portfolio.works > 0 ? Math.round((portfolio.mirrors / portfolio.works) * 100) : 0;
  const portfolioEl = $('#portfolio');
  if (portfolioEl) portfolioEl.innerHTML = `
    <div class="ring" style="background: conic-gradient(var(--teal) 0 ${coverage}%, #dce9e8 ${coverage}% 100%)"><div><strong>${coverage}%</strong><span>mirror coverage</span></div></div>
    <div class="portfolio-stats"><div><strong>${portfolio.works}</strong><span>Sandbox registry</span></div><div><strong>${portfolio.mirrors}</strong><span>GitHub workfolders</span></div><div><strong>${portfolio.missingMirrors}</strong><span>mirror missing</span></div></div>
    <div class="portfolio-note">Work 17 exists in Sandbox and GitHub work/17; global parity is not implied by this dashboard.</div>`;

  const agentsEl = $('#agents');
  if (agentsEl) agentsEl.innerHTML = `<table><thead><tr><th>Agent type</th><th>Evidence</th><th>Finding</th><th>Source</th></tr></thead><tbody>${agents.map(a => `<tr><td>${esc(a[0])}</td><td>${badge(a[1])}</td><td>${esc(a[2])}</td><td><code>${esc(a[3])}</code></td></tr>`).join('')}</tbody></table>`;

  const membersEl = $('#members');
  if (membersEl) membersEl.innerHTML = members.map(m => `<div class="member-row"><div class="avatar">${esc(m[0].slice(-2))}</div><div><strong>${esc(m[0])} · ${esc(m[1])}</strong><span>${esc(m[2])}</span><span>${esc(m[3])}</span></div></div>`).join('');

  const filtered = gaps.filter(g =>
    (status === 'all' || g[4] === status) &&
    (priority === 'all' || g[3] === priority) &&
    (gate === 'all' || g[6] === gate) &&
    (!q || g.join(' ').toLowerCase().includes(q))
  );
  const gapCount = $('#gapCount');
  if (gapCount) gapCount.textContent = `${filtered.length} SHOWN / ${gaps.length} TOTAL`;
  const gapsEl = $('#gaps');
  if (gapsEl) gapsEl.innerHTML = filtered.map(g => `
    <article class="gap-row"><div class="gap-priority ${esc(g[3].toLowerCase())}">${esc(g[3])}</div>
    <div class="gap-content"><div class="gap-title"><strong>${esc(g[0])} · ${esc(g[1])}</strong>${badge(g[4])}</div>
    <span class="muted">${esc(g[2])} · ${esc(g[6])}</span><p>${esc(g[5])}</p></div></article>`).join('') || '<div class="empty">Không có mục phù hợp bộ lọc.</div>';

  const e2eEl = $('#e2e');
  if (e2eEl) e2eEl.innerHTML = e2e.map((x,i) => `
    <div class="trace-step"><div class="trace-number">${esc(x[0])}</div><div class="trace-copy"><strong>${esc(x[1])}</strong><span>${esc(x[2])}</span><small>${esc(x[3])}</small></div>${badge(x[4])}${i < e2e.length - 1 ? '<div class="trace-line"></div>' : ''}</div>`).join('');
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
  setConnection(isReconnect ? 'reconnecting' : 'cache', isReconnect ? `Lần thử reconnect #${reconnectAttempt + 1}.` : 'Đang kiểm tra nguồn dữ liệu…');
  try {
    const response = await fetch(`/api/live?at=${Date.now()}`, { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const next = await response.json();
    if (!validClientPayload(next)) throw new Error('Payload /api/live sai schema; giữ nguyên dữ liệu cũ');
    data = next;
    const live = next.meta?.source === 'mcp-live' && next.meta?.fresh === true;
    if (live) {
      reconnectAttempt = 0;
      setConnection('live');
    } else if (next.meta?.bridgeConfigured && next.meta?.warning) {
      scheduleReconnect(next.meta.warning);
    } else {
      reconnectAttempt = 0;
      setConnection('cache', next.meta?.source === 'mcp-stub' ? 'Local stub replay — không phải MCP thật.' : '');
    }
    render();
  } catch (error) {
    scheduleReconnect(`Không xác minh được dữ liệu: ${error.message}`);
  } finally {
    requestInFlight = false;
    const button = $('#refreshLive');
    if (button) {
      button.disabled = false;
      button.textContent = 'Refresh MCP';
    }
  }
}

async function heartbeat() {
  try {
    const response = await fetch(`/api/health?at=${Date.now()}`, { cache: 'no-store' });
    const health = await response.json();
    if (!response.ok || !health.ok) throw new Error(health.cacheError || `HTTP ${response.status}`);
    if (!data || data.meta?.bridgeConfigured) refreshLive(Boolean(reconnectAttempt));
  } catch (error) {
    scheduleReconnect(`Health check: ${error.message}`);
  }
}

['statusFilter', 'priorityFilter', 'gateFilter', 'searchFilter'].forEach(id => {
  const el = document.getElementById(id);
  if (el) el.addEventListener(id === 'searchFilter' ? 'input' : 'change', () => data && render());
});
$('#refreshLive')?.addEventListener('click', () => {
  reconnectAttempt = 0;
  refreshLive(false);
});

refreshLive();
refreshTimer = setInterval(() => refreshLive(false), 30000);
heartbeatTimer = setInterval(heartbeat, 15000);
