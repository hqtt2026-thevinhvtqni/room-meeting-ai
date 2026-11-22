const Workflow = window.RoomHopWorkflow;
if (!Workflow) throw new Error('workflow.js must load before app.js');

const scenarios = {
  browse: { label: 'Browse', steps: [
    ['Navigate', 'Mở Wikipedia (mô phỏng)', 'Mock page opened; no network request', 'Navigation'],
    ['Inspect', 'Kiểm tra trang mô phỏng', 'Mock page state inspected', 'DOM inspected'],
    ['Screenshot', 'Thử bước screenshot', 'Screenshot action simulated; no image file created', 'Screenshot simulated']
  ]},
  search: { label: 'Search', steps: [
    ['Navigate', 'Mở Wikipedia (mô phỏng)', 'Mock page opened; no network request', 'Navigation'],
    ['Inspect', 'Kiểm tra trang mô phỏng', 'Mock page state inspected', 'DOM inspected'],
    ['Type', 'Nhập từ khóa vào mock search', 'Mock input updated', 'Input completed'],
    ['Click', 'Kích hoạt mock search', 'Mock search state changed; no network request', 'Click target identified'],
    ['Extract', 'Hiển thị kết quả mẫu', 'Mock result cards rendered; not retrieved from a website', 'Result extracted'],
    ['Screenshot', 'Thử bước screenshot', 'Screenshot action simulated; no image file created', 'Screenshot simulated']
  ]},
  workflow: { label: 'Agent Workflow', steps: [
    ['Navigate', 'Mở Wikipedia (mô phỏng)', 'Mock page opened; no network request', 'Navigation'],
    ['Inspect', 'Kiểm tra trang mô phỏng', 'Mock page state inspected', 'DOM inspected'],
    ['Type', 'Nhập từ khóa vào mock search', 'Mock input updated', 'Input completed'],
    ['Click', 'Kích hoạt mock search', 'Mock search state changed; no network request', 'Click target identified'],
    ['Extract', 'Hiển thị kết quả mẫu', 'Mock result cards rendered; not retrieved from a website', 'Result extracted'],
    ['Screenshot', 'Thử bước screenshot', 'Screenshot action simulated; no image file created', 'Screenshot simulated'],
    ['Wait', 'Chờ trạng thái mô phỏng', 'Mock timer completed', 'Wait completed'],
    ['DONE', 'Hoàn tất kịch bản demo', 'Scripted demo finished; no real-world task was performed', 'Workflow complete']
  ]}
};

const evidenceMeta = {
  Navigation: { title: 'Mock navigation event', detail: 'Virtual page state changed; no request was sent.' },
  'DOM inspected': { title: 'Mock page inspection', detail: 'Only the local mock page state was inspected.' },
  'Input completed': { title: 'Mock input event', detail: 'The search phrase was placed in the local mock UI.' },
  'Click target identified': { title: 'Mock click event', detail: 'A local scripted state transition was run.' },
  'Result extracted': { title: 'Mock result display', detail: 'Sample cards are mock content, not website results.' },
  'Screenshot simulated': { title: 'Screenshot action (not captured)', detail: 'No screenshot file was created; this is a simulated action only.' }
};
const permissionNames = {
  readPage: 'Read mock page', inspect: 'Inspect mock UI', click: 'Click in demo',
  type: 'Type in demo', wait: 'Wait in demo', extract: 'Show mock results',
  screenshot: 'Screenshot action (demo only)'
};
const emptyPermissions = () => Object.fromEntries(Object.keys(permissionNames).map((key) => [key, false]));
let state = {
  scenario: 'search', running: false, control: 'agent', tab: 1,
  tabs: [{ id: 1, title: 'Wikipedia (mock)', url: 'https://wikipedia.org' }],
  history: [], evidence: [], timer: null, task: '', query: '', permissions: emptyPermissions()
};
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
}
function activeTab() { return state.tabs.find((tab) => tab.id === state.tab) || state.tabs[0]; }
function renderTabs() {
  $('#tabs').innerHTML = state.tabs.map((tab) =>
    `<div class="tab ${tab.id === state.tab ? 'active' : ''}" data-tab="${tab.id}">◉ ${escapeHtml(tab.title)}<span class="tab-close" aria-hidden="true">×</span></div>`
  ).join('');
  $$('.tab').forEach((element) => element.addEventListener('click', () => {
    state.tab = Number(element.dataset.tab); renderTabs(); renderBrowser();
  }));
}
function renderBrowser(mode = 'ready') {
  const tab = activeTab();
  $('#urlInput').value = tab.url;
  if (mode === 'loading') {
    $('#browserContent').innerHTML = '<div class="loading"><div class="spinner"></div>MOCK NAVIGATION IN PROGRESS · NO NETWORK</div>';
    $('#pageState').textContent = 'LOADING · MOCK'; return;
  }
  $('#pageState').textContent = 'READY · MOCK';
  if (tab.url.includes('search')) {
    const query = escapeHtml(state.query || 'ROOM-HOP');
    $('#browserContent').innerHTML = `<div class="mock-site"><div class="wiki-top"><div class="wiki-logo">W</div><div class="wiki-name">WIKIPEDIA · MOCK</div><div class="wiki-search">${query} 🔍</div></div><div class="search-result"><h2>Mock results for: <mark>${query}</mark></h2><p><b>${query}</b> — sample result card (not retrieved from a website).</p><p><b>ROOM-HOP Browser demo</b> — local mock content.</p><p><b>Agent browsing example</b> — scripted sample content.</p></div></div>`;
  } else {
    $('#browserContent').innerHTML = '<div class="mock-site"><div class="wiki-top"><div class="wiki-logo">W</div><div class="wiki-name">WIKIPEDIA · MOCK</div><div class="wiki-search">Mock search only</div></div><div class="wiki-body"><div class="wiki-side">Main page<br>Contents<br>Current events<br>Random article</div><div class="wiki-main"><h2>Wikipedia mock page</h2><p>This local illustration is not connected to Wikipedia or the Internet.</p><p><span class="highlight">No real page was fetched.</span></p></div></div></div>';
  }
}
function setTaskError(message) {
  $('#taskError').textContent = message || '';
  $('#taskError').hidden = !message;
  $('#taskInput').setAttribute('aria-invalid', message ? 'true' : 'false');
}
function renderEvidence() {
  const list = $('#evidence'); list.replaceChildren();
  Object.entries(evidenceMeta).forEach(([id, meta]) => {
    const item = state.evidence.find((entry) => entry.id === id);
    const row = document.createElement('li'); row.className = item ? 'done' : '';
    const title = document.createElement('strong'); title.textContent = meta.title;
    const detail = document.createElement('small'); detail.textContent = item ? item.detail : 'No simulated event yet';
    row.append(title, detail);
    if (item) {
      const provenance = document.createElement('small'); provenance.className = 'evidence-provenance';
      provenance.textContent = `${item.type.toUpperCase()} · ${item.status.toUpperCase()} · ${item.sourceLabel} · ${item.timestamp} · artifact: none`;
      row.append(provenance);
    }
    list.append(row);
  });
  $('#evidenceCount').textContent = `${state.evidence.length} / ${Object.keys(evidenceMeta).length} mock events`;
  const complete = Workflow.isDemoComplete(state.history, scenarios[state.scenario].steps.length) && !state.running;
  $('#passBox').classList.toggle('hidden', !complete);
  if (complete) $('#passDetail').textContent = 'Script finished · simulated only · no real-world verification';
}
function renderTimeline() {
  const list = $('#timeline'); list.replaceChildren();
  if (!state.history.length) {
    const empty = document.createElement('li'); empty.className = 'empty-timeline'; empty.textContent = 'Demo events will appear here'; list.append(empty);
  } else {
    state.history.forEach((item, index) => {
      const row = document.createElement('li'); row.className = item.status; row.dataset.seq = String(index);
      const title = document.createElement('strong'); title.textContent = `${item.status === 'running' ? '→ ' : '✓ '}${item.action}`;
      const time = document.createElement('small'); time.textContent = `${item.time} · ${item.description}`;
      const detail = document.createElement('span'); detail.textContent = item.detail;
      row.append(title, time, detail); list.append(row);
    });
  }
  $('#timelineCount').textContent = `${state.history.length} mock event${state.history.length === 1 ? '' : 's'}`;
}
function renderPermissions() {
  $$('.permission-toggle').forEach((button) => {
    const key = button.dataset.permission; const granted = state.permissions[key] === true;
    button.setAttribute('aria-pressed', String(granted));
    button.textContent = granted ? 'Revoke demo' : 'Grant for demo';
    button.disabled = state.running;
    document.querySelector(`[data-permission-status="${key}"]`).textContent = granted ? 'Granted for this demo only' : 'Not granted';
  });
}
function renderSummary() {
  const steps = scenarios[state.scenario].steps;
  const done = state.history.filter((item) => item.status === 'success').length;
  const current = state.history[state.history.length - 1];
  $('#progressValue').textContent = `${done} / ${steps.length} actions`;
  $('#progressBar').style.width = `${Math.round(done / steps.length * 100)}%`;
  if (!state.running && !state.history.length) {
    $('#currentAction').textContent = 'Ready when you are';
    $('#currentHumanAction').textContent = 'Task will select a scripted demo';
    $('#actionState').textContent = 'IDLE'; $('#actionState').className = 'state-pill idle';
    $('#nextAction').textContent = '→ Review demo permissions';
    $('#agentStateLabel').textContent = 'Connected · MOCK';
    $('#sessionState').textContent = 'Demo is ready'; $('#sessionSubstate').textContent = 'No real agent is connected';
  } else if (current) {
    $('#currentAction').textContent = current.action; $('#currentHumanAction').textContent = current.description;
    $('#actionState').textContent = current.status === 'running' ? 'RUNNING · DEMO' : state.running ? 'IN PROGRESS' : 'DEMO DONE';
    $('#actionState').className = `state-pill ${current.status === 'running' ? 'running' : state.running ? 'success' : 'done'}`;
    const next = steps[state.history.length]; $('#nextAction').textContent = next ? `→ ${next[1]}` : '→ Finish mock script';
    $('#agentStateLabel').textContent = state.running ? 'Working · MOCK' : 'Demo done';
    $('#sessionState').textContent = state.running ? 'Demo script is running' : 'Demo script complete';
    $('#sessionSubstate').textContent = state.running ? `Task: ${state.task}` : 'No real-world task was performed';
  }
  $('#runBtn').disabled = state.running || state.control === 'human';
  $('#controlStatus').textContent = state.control === 'agent' ? '● Demo control' : '● Human control';
  $('#controlLabel').textContent = state.control === 'agent' ? '● Demo control' : '● Human control';
  $('#controlBtn').textContent = state.control === 'agent' ? 'Take control' : 'Give control to Agent';
}
function render() {
  renderTabs(); renderBrowser(); renderTimeline(); renderEvidence(); renderPermissions(); renderSummary();
  $$('.demo-choice').forEach((button) => button.classList.toggle('selected', button.dataset.scenario === state.scenario));
}
function addStep(index) {
  const steps = scenarios[state.scenario].steps;
  if (index >= steps.length) { finish(); return; }
  const [action, description, baseDetail, evidenceId] = steps[index];
  let detail = baseDetail; let humanDescription = description;
  if (action === 'Type') { detail = `Mock query entered: ${state.query}`; humanDescription = `Nhập từ khóa “${state.query}” vào giao diện mô phỏng`; }
  else if (action === 'Extract') detail = `Sample cards rendered for “${state.query}”; no website was queried`;
  state.history.push({ action, description: humanDescription, detail, evidence: evidenceId, status: 'running', time: new Date().toISOString() });
  renderTimeline(); renderSummary();
  if (action === 'Navigate') {
    renderBrowser('loading'); state.timer = setTimeout(() => { renderBrowser(); markStep(index); }, 400);
  } else if (action === 'Type') {
    state.timer = setTimeout(() => {
      activeTab().url = `https://wikipedia.org/wiki/Special:Search?search=${encodeURIComponent(state.query)}`;
      $('#urlInput').value = activeTab().url; markStep(index);
    }, 250);
  } else if (action === 'Click') {
    state.timer = setTimeout(() => {
      activeTab().url = `https://wikipedia.org/wiki/Special:Search?search=${encodeURIComponent(state.query)}`;
      renderBrowser(); markStep(index);
    }, 250);
  } else state.timer = setTimeout(() => markStep(index), action === 'Screenshot' ? 250 : 200);
}
function markStep(index) {
  const item = state.history[index]; item.status = 'success';
  if (item.evidence && evidenceMeta[item.evidence] && !state.evidence.some((entry) => entry.id === item.evidence)) {
    state.evidence.push(Workflow.buildMockEvidence(item.evidence, evidenceMeta[item.evidence].title, evidenceMeta[item.evidence].detail));
  }
  renderTimeline(); renderEvidence(); renderSummary();
  state.timer = setTimeout(() => addStep(index + 1), 200);
}
function finish() {
  state.running = false; renderTimeline(); renderEvidence(); renderPermissions(); renderSummary();
  $('#runBtn').innerHTML = '<span>↻</span> Run demo again';
}
function run() {
  if (state.running || state.control === 'human') return;
  state.history = []; state.evidence = []; $('#taskEcho').hidden = true;
  const taskResult = Workflow.resolveTask($('#taskInput').value, state.scenario);
  if (!taskResult.ok) {
    setTaskError(taskResult.error); renderTimeline(); renderEvidence(); renderSummary(); $('#taskInput').focus(); return;
  }
  setTaskError(''); state.scenario = taskResult.scenario; state.task = taskResult.task; state.query = taskResult.query;
  state.permissions = Workflow.permissionsForScenario(taskResult.scenario, state.permissions);
  const missing = Workflow.missingPermissions(taskResult.scenario, state.permissions);
  if (missing.length) {
    render();
    $('#permissionFeedback').textContent = `Chưa cấp quyền demo cần thiết: ${missing.map((key) => permissionNames[key]).join(', ')}.`;
    document.querySelector(`[data-permission="${missing[0]}"]`).focus(); return;
  }
  $('#permissionFeedback').textContent = '';
  state.tabs = [{ id: 1, title: 'Wikipedia (mock)', url: 'https://wikipedia.org' }]; state.tab = 1;
  state.running = true;
  $('#taskEcho').textContent = `DEMO REQUEST: ${state.task}`; $('#taskEcho').hidden = false;
  $('#runBtn').innerHTML = '<span>◌</span> Running mock demo';
  renderTabs(); renderTimeline(); renderEvidence(); renderPermissions(); renderSummary(); addStep(0);
}
function reset() {
  clearTimeout(state.timer); state.running = false; state.history = []; state.evidence = [];
  state.task = ''; state.query = ''; state.permissions = emptyPermissions();
  state.tabs = [{ id: 1, title: 'Wikipedia (mock)', url: 'https://wikipedia.org' }]; state.tab = 1;
  $('#taskEcho').hidden = true; $('#taskEcho').textContent = '';
  $('#runBtn').innerHTML = '<span>▶</span> Run demo'; setTaskError(''); $('#permissionFeedback').textContent = ''; render();
}

$('#runBtn').addEventListener('click', run);
$('#taskInput').addEventListener('input', () => setTaskError(''));
$('#controlBtn').addEventListener('click', () => { state.control = state.control === 'agent' ? 'human' : 'agent'; renderSummary(); });
$$('.permission-toggle').forEach((button) => button.addEventListener('click', () => {
  if (state.running) return;
  const key = button.dataset.permission; state.permissions[key] = !state.permissions[key];
  $('#permissionFeedback').textContent = ''; renderPermissions();
}));
$('#newTabBtn').addEventListener('click', () => {
  if (state.running) return;
  const id = Math.max(0, ...state.tabs.map((tab) => tab.id)) + 1;
  state.tabs.push({ id, title: 'New Tab (mock)', url: 'about:blank' }); state.tab = id; renderTabs(); renderBrowser();
});
$('#reloadBtn').addEventListener('click', () => { renderBrowser('loading'); setTimeout(() => renderBrowser(), 300); });
$('#backBtn').addEventListener('click', () => { activeTab().url = 'https://wikipedia.org'; renderBrowser(); });
$('#forwardBtn').addEventListener('click', () => {
  activeTab().url = `https://wikipedia.org/wiki/Special:Search?search=${encodeURIComponent(state.query || 'ROOM-HOP')}`; renderBrowser();
});
$('#urlInput').addEventListener('keydown', (event) => {
  if (event.key === 'Enter') { activeTab().url = event.target.value; renderBrowser(); }
});
$$('.demo-choice').forEach((button) => button.addEventListener('click', () => {
  if (state.running) return; state.scenario = button.dataset.scenario; reset();
}));
$$('.secondary-tab').forEach((button) => button.addEventListener('click', () => {
  $$('.secondary-tab').forEach((element) => element.classList.remove('active'));
  button.classList.add('active'); $$('.secondary-panel').forEach((panel) => panel.classList.add('hidden'));
  $('#'+button.dataset.panel).classList.remove('hidden');
}));
$('#railCollapse').addEventListener('click', () => document.querySelector('.agent-rail').classList.toggle('compact'));
render();

// Make the visible mock tab-close affordance operable and accessible.
renderTabs = function renderTabsWithClosableButtons() {
  $('#tabs').innerHTML = state.tabs.map((tab) =>
    `<div class="tab ${tab.id === state.tab ? 'active' : ''}" data-tab="${tab.id}"><span>◉ ${escapeHtml(tab.title)}</span><button type="button" class="tab-close" aria-label="Close tab" title="Close tab" ${state.tabs.length === 1 ? 'disabled' : ''}>×</button></div>`
  ).join('');
  $$('.tab').forEach((element) => {
    const id = Number(element.dataset.tab);
    element.addEventListener('click', (event) => {
      if (event.target.closest('.tab-close')) return;
      state.tab = id; renderTabs(); renderBrowser();
    });
    element.querySelector('.tab-close').addEventListener('click', (event) => {
      event.stopPropagation();
      if (state.tabs.length <= 1) return;
      const closedIndex = state.tabs.findIndex((tab) => tab.id === id);
      state.tabs = state.tabs.filter((tab) => tab.id !== id);
      if (state.tab === id) state.tab = state.tabs[Math.min(closedIndex, state.tabs.length - 1)].id;
      renderTabs(); renderBrowser();
    });
  });
};
renderTabs();
