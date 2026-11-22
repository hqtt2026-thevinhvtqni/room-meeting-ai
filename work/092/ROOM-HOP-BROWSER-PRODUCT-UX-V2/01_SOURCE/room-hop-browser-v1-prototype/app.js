const Workflow = window.RoomHopWorkflow;
if (!Workflow) throw new Error('workflow.js must load before app.js');

const scenarios = {
  browse: { label: 'Browse demo', steps: [
    ['Navigate', 'Mở trang mẫu (mô phỏng)', 'Local fixture state changed; no network request', 'Navigation'],
    ['Inspect', 'Kiểm tra fixture cục bộ', 'Only the local mock view was inspected', 'DOM inspected'],
    ['Screenshot', 'Mô phỏng bước screenshot', 'Screenshot action simulated; no image file created', 'Screenshot simulated']
  ]},
  search: { label: 'Search demo', steps: [
    ['Navigate', 'Mở trang mẫu (mô phỏng)', 'Local fixture state changed; no network request', 'Navigation'],
    ['Inspect', 'Kiểm tra fixture cục bộ', 'Only the local mock view was inspected', 'DOM inspected'],
    ['Type', 'Nhập từ khóa vào fixture', 'Local mock input updated', 'Input completed'],
    ['Click', 'Kích hoạt tìm kiếm mô phỏng', 'Local mock state changed; no network request', 'Click target identified'],
    ['Extract', 'Hiển thị dữ liệu mẫu', 'Fixture cards rendered; no website was queried', 'Result extracted'],
    ['Screenshot', 'Mô phỏng bước screenshot', 'Screenshot action simulated; no image file created', 'Screenshot simulated']
  ]},
  workflow: { label: 'TEST_ONLY workflow', steps: [
    ['Navigate', 'Mở trang mẫu (mô phỏng)', 'Local fixture state changed; no network request', 'Navigation'],
    ['Inspect', 'Kiểm tra fixture cục bộ', 'Only the local mock view was inspected', 'DOM inspected'],
    ['Type', 'Nhập từ khóa vào fixture', 'Local mock input updated', 'Input completed'],
    ['Click', 'Kích hoạt tìm kiếm mô phỏng', 'Local mock state changed; no network request', 'Click target identified'],
    ['Extract', 'Hiển thị dữ liệu mẫu', 'Fixture cards rendered; no website was queried', 'Result extracted'],
    ['Screenshot', 'Mô phỏng bước screenshot', 'Screenshot action simulated; no image file created', 'Screenshot simulated'],
    ['Wait', 'Chờ timer cục bộ', 'Local test timer completed', 'Wait completed'],
    ['DONE', 'Kết thúc fixture', 'TEST_ONLY script finished; no real-world task was performed', 'Workflow complete']
  ]}
};

const evidenceMeta = {
  Navigation: { title: 'TEST_ONLY navigation event', detail: 'Virtual local state changed; no request was sent.' },
  'DOM inspected': { title: 'TEST_ONLY fixture inspection', detail: 'Only the local mock state was inspected.' },
  'Input completed': { title: 'TEST_ONLY input event', detail: 'Text was placed in the local mock UI.' },
  'Click target identified': { title: 'TEST_ONLY click event', detail: 'A local scripted state transition was run.' },
  'Result extracted': { title: 'TEST_ONLY sample display', detail: 'Sample cards are local fixture content, not website results.' },
  'Screenshot simulated': { title: 'Screenshot action (not captured)', detail: 'No screenshot file was created; this is a simulated action only.' }
};
const permissionNames = {
  readPage: 'Read mock page', inspect: 'Inspect mock UI', click: 'Click in demo',
  type: 'Type in demo', wait: 'Wait in demo', extract: 'Show mock results', screenshot: 'Screenshot action (test only)'
};
const emptyPermissions = () => Object.fromEntries(Object.keys(permissionNames).map((key) => [key, false]));
const state = {
  scenario: 'search', running: false, control: 'test', tab: 1,
  tabs: [{ id: 1, title: 'Local fixture', url: 'https://wikipedia.org' }],
  history: [], evidence: [], timer: null, task: '', query: '', permissions: emptyPermissions()
};
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
}
function activeTab() { return state.tabs.find((tab) => tab.id === state.tab) || state.tabs[0]; }
function renderTabs({ focusTabId = null } = {}) {
  const tabList = $('#tabs');
  tabList.replaceChildren();
  for (const tab of state.tabs) {
    const selected = tab.id === state.tab;
    const select = document.createElement('button');
    select.type = 'button'; select.className = `tab${selected ? ' active' : ''}`; select.id = `mock-tab-${tab.id}`;
    select.setAttribute('role', 'tab'); select.setAttribute('aria-selected', String(selected));
    select.setAttribute('aria-controls', 'browserContent'); select.tabIndex = selected ? 0 : -1;
    select.setAttribute('aria-label', `Select TEST_ONLY tab: ${tab.title}`);
    select.textContent = `◉ ${tab.title}`;
    select.addEventListener('click', () => {
      state.tab = tab.id; renderTabs({ focusTabId: tab.id }); renderBrowser();
    });
    select.addEventListener('keydown', (event) => {
      const tabs = state.tabs;
      const index = tabs.findIndex((entry) => entry.id === tab.id);
      let nextIndex = null;
      if (event.key === 'ArrowRight') nextIndex = (index + 1) % tabs.length;
      else if (event.key === 'ArrowLeft') nextIndex = (index - 1 + tabs.length) % tabs.length;
      else if (event.key === 'Home') nextIndex = 0;
      else if (event.key === 'End') nextIndex = tabs.length - 1;
      if (nextIndex === null) return;
      event.preventDefault(); state.tab = tabs[nextIndex].id;
      renderTabs({ focusTabId: state.tab }); renderBrowser();
    });
    tabList.append(select);
  }
  const closeButton = $('#closeTabBtn');
  closeButton.disabled = state.tabs.length <= 1 || state.running;
  closeButton.setAttribute('aria-label', `Close current TEST_ONLY tab: ${activeTab().title}`);
  closeButton.title = `Close current TEST_ONLY tab: ${activeTab().title}`;
  $('#newTabBtn').disabled = state.running;
  $('#browserContent').setAttribute('aria-labelledby', `mock-tab-${state.tab}`);
  if (focusTabId !== null) document.getElementById(`mock-tab-${focusTabId}`)?.focus({ preventScroll: true });
}
function closeCurrentTab() {
  if (state.tabs.length <= 1 || state.running) return;
  const closedIndex = state.tabs.findIndex((tab) => tab.id === state.tab);
  state.tabs = state.tabs.filter((tab) => tab.id !== state.tab);
  state.tab = state.tabs[Math.min(closedIndex, state.tabs.length - 1)].id;
  renderTabs({ focusTabId: state.tab }); renderBrowser();
}
function renderBrowser(mode = 'ready') {
  const tab = activeTab();
  const content = $('#browserContent');
  $('#urlInput').value = tab.url;
  if (mode === 'loading') {
    content.setAttribute('aria-busy', 'true');
    content.innerHTML = '<div class="loading"><div class="spinner" aria-hidden="true"></div>TEST_ONLY LOCAL STATE UPDATE · NO NETWORK</div>';
    $('#pageState').textContent = 'TEST_ONLY · LOCAL UPDATE'; return;
  }
  content.setAttribute('aria-busy', 'false');
  $('#pageState').textContent = 'DISCONNECTED · TEST_ONLY LOCAL VIEW';
  if (tab.url === 'about:blank') {
    content.innerHTML = '<div class="blank-fixture"><strong>Empty TEST_ONLY tab</strong><p>No site is loaded or contacted.</p></div>'; return;
  }
  if (tab.url.includes('search')) {
    const query = escapeHtml(state.query || 'ROOM-HOP');
    content.innerHTML = `<div class="mock-site"><div class="wiki-top"><div class="wiki-logo">W</div><div class="wiki-name">LOCAL FIXTURE</div><div class="wiki-search">${query} · TEST_ONLY</div></div><div class="search-result"><h2>Sample fixture cards for: <mark>${query}</mark></h2><p><b>${query}</b> — local test sample; not retrieved from a website.</p><p><b>ROOM-HOP UI fixture</b> — local sample content only.</p><p><b>Scripted workflow example</b> — no agent execution.</p></div></div>`;
  } else {
    content.innerHTML = '<div class="mock-site"><div class="wiki-top"><div class="wiki-logo">W</div><div class="wiki-name">LOCAL FIXTURE · TEST_ONLY</div><div class="wiki-search">Local mock state</div></div><div class="wiki-body"><div class="wiki-side">Fixture section<br>Sample contents<br>Local examples<br>No external page</div><div class="wiki-main"><h2>Local browser-view fixture</h2><p>This illustration is local UI content, not a fetched page.</p><p><span class="highlight">Runtime disconnected · no network request.</span></p></div></div></div>';
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
    const detail = document.createElement('small'); detail.textContent = item ? item.detail : 'No TEST_ONLY event yet';
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
  if (complete) $('#passDetail').textContent = 'TEST_ONLY script finished · no real-world task or verification';
}
function renderTimeline() {
  const list = $('#timeline'); list.replaceChildren();
  if (!state.history.length) {
    const empty = document.createElement('li'); empty.className = 'empty-timeline'; empty.textContent = 'No simulated events'; list.append(empty);
  } else {
    state.history.forEach((item, index) => {
      const row = document.createElement('li'); row.className = item.status; row.dataset.seq = String(index);
      const title = document.createElement('strong'); title.textContent = `${item.status === 'running' ? 'RUNNING · TEST_ONLY' : 'SIMULATED · TEST_ONLY'} · ${item.action}`;
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
    button.textContent = granted ? 'Disable test' : 'Enable for test';
    button.setAttribute('aria-label', `${granted ? 'Disable' : 'Enable'} TEST_ONLY permission: ${permissionNames[key]}`);
    button.disabled = state.running;
    document.querySelector(`[data-permission-status="${key}"]`).textContent = granted ? 'Enabled for this test only' : 'Not enabled';
  });
}
function renderSummary() {
  const steps = scenarios[state.scenario].steps;
  const done = state.history.filter((item) => item.status === 'success').length;
  const current = state.history[state.history.length - 1];
  const complete = Workflow.isDemoComplete(state.history, steps.length) && !state.running;
  const uiState = Workflow.getDemoUiState({ running: state.running, held: state.control === 'human', complete });
  $('#progressValue').textContent = `${done} / ${steps.length} steps`;
  const progress = $('.progress-track'); progress.setAttribute('aria-valuemax', String(steps.length)); progress.setAttribute('aria-valuenow', String(done));
  $('#progressBar').style.width = `${Math.round(done / steps.length * 100)}%`;
  $('#agentStateLabel').textContent = 'DISCONNECTED';
  if (!state.running && !state.history.length) {
    $('#currentAction').textContent = 'No runtime action';
    $('#currentHumanAction').textContent = 'Preview a TEST_ONLY scenario';
    $('#actionState').textContent = uiState.activity;
    $('#actionState').className = `state-pill ${state.control === 'human' ? 'held' : 'idle'}`;
    $('#nextAction').textContent = '→ Review TEST_ONLY permissions';
    $('#sessionState').textContent = state.control === 'human' ? 'TEST_ONLY demo held' : 'Runtime disconnected';
    $('#sessionSubstate').textContent = 'No real agent or browser session';
  } else if (current) {
    $('#currentAction').textContent = current.action;
    $('#currentHumanAction').textContent = current.description;
    $('#actionState').textContent = uiState.activity;
    $('#actionState').className = `state-pill ${state.running ? 'running' : complete ? 'done' : 'held'}`;
    const next = steps[state.history.length];
    $('#nextAction').textContent = next ? `→ ${next[1]}` : complete ? '→ TEST_ONLY script finished' : '→ No runtime action';
    $('#sessionState').textContent = state.running ? 'TEST_ONLY script running locally' : complete ? 'TEST_ONLY demo complete' : 'Runtime disconnected';
    $('#sessionSubstate').textContent = state.running ? 'No agent connected; local timer only' : 'No real-world task was performed';
  }
  $('#runBtn').disabled = !uiState.canRun;
  $('#runBtn').innerHTML = state.running ? '<span aria-hidden="true">◌</span> TEST_ONLY script running' : complete ? '<span aria-hidden="true">↻</span> Run TEST_ONLY again' : '<span aria-hidden="true">▶</span> Run TEST_ONLY demo';
  $('#controlStatus').textContent = state.control === 'human' ? 'TEST_ONLY script held' : 'TEST_ONLY script ready';
  $('#controlLabel').textContent = state.control === 'human' ? 'TEST_ONLY held by user' : 'TEST_ONLY ready';
  $('#controlBtn').textContent = state.control === 'human' ? 'Resume TEST_ONLY demo' : 'Hold TEST_ONLY demo';
  $('#controlBtn').setAttribute('aria-pressed', String(state.control === 'human'));
  $('#controlBtn').disabled = state.running;
}
function render() {
  renderTabs(); renderBrowser(); renderTimeline(); renderEvidence(); renderPermissions(); renderSummary();
  $$('.demo-choice').forEach((button) => {
    const selected = button.dataset.scenario === state.scenario;
    button.classList.toggle('selected', selected); button.setAttribute('aria-pressed', String(selected));
  });
}
function addStep(index) {
  const steps = scenarios[state.scenario].steps;
  if (index >= steps.length) { finish(); return; }
  const [action, description, baseDetail, evidenceId] = steps[index];
  let detail = baseDetail; let humanDescription = description;
  if (action === 'Type') { detail = `Mock query entered: ${state.query}`; humanDescription = `Nhập từ khóa “${state.query}” vào fixture cục bộ`; }
  else if (action === 'Extract') detail = `Local sample cards rendered for “${state.query}”; no website was queried`;
  state.history.push({ action, description: humanDescription, detail, evidence: evidenceId, status: 'running', time: new Date().toISOString() });
  renderTimeline(); renderSummary();
  if (action === 'Navigate') {
    renderBrowser('loading'); state.timer = setTimeout(() => { renderBrowser(); markStep(index); }, 250);
  } else if (action === 'Type') {
    state.timer = setTimeout(() => {
      activeTab().url = `https://wikipedia.org/wiki/Special:Search?search=${encodeURIComponent(state.query)}`;
      $('#urlInput').value = activeTab().url; markStep(index);
    }, 150);
  } else if (action === 'Click') {
    state.timer = setTimeout(() => {
      activeTab().url = `https://wikipedia.org/wiki/Special:Search?search=${encodeURIComponent(state.query)}`;
      renderBrowser(); markStep(index);
    }, 150);
  } else state.timer = setTimeout(() => markStep(index), 150);
}
function markStep(index) {
  const item = state.history[index]; item.status = 'success';
  if (item.evidence && evidenceMeta[item.evidence] && !state.evidence.some((entry) => entry.id === item.evidence)) {
    state.evidence.push(Workflow.buildMockEvidence(item.evidence, evidenceMeta[item.evidence].title, evidenceMeta[item.evidence].detail));
  }
  renderTimeline(); renderEvidence(); renderSummary();
  state.timer = setTimeout(() => addStep(index + 1), 100);
}
function finish() {
  state.running = false; renderTimeline(); renderEvidence(); renderPermissions(); renderSummary();
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
    render(); $('#permissionFeedback').textContent = `Chưa bật quyền TEST_ONLY cần thiết: ${missing.map((key) => permissionNames[key]).join(', ')}.`;
    document.querySelector(`[data-permission="${missing[0]}"]`).focus(); return;
  }
  $('#permissionFeedback').textContent = '';
  state.tabs = [{ id: 1, title: 'Local fixture', url: 'https://wikipedia.org' }]; state.tab = 1;
  state.running = true;
  $('#taskEcho').textContent = `TEST_ONLY REQUEST: ${state.task}`; $('#taskEcho').hidden = false;
  renderTabs(); renderTimeline(); renderEvidence(); renderPermissions(); renderSummary(); addStep(0);
}
function reset() {
  clearTimeout(state.timer); state.running = false; state.history = []; state.evidence = [];
  state.task = ''; state.query = ''; state.permissions = emptyPermissions(); state.control = 'test';
  state.tabs = [{ id: 1, title: 'Local fixture', url: 'https://wikipedia.org' }]; state.tab = 1;
  $('#taskEcho').hidden = true; $('#taskEcho').textContent = '';
  $('#permissionFeedback').textContent = ''; setTaskError(''); render();
}
function selectInfoTab(button, { focus = false } = {}) {
  const panelId = button.dataset.panel;
  $$('.secondary-tab').forEach((tab) => {
    const selected = tab === button;
    tab.classList.toggle('active', selected); tab.setAttribute('aria-selected', String(selected)); tab.tabIndex = selected ? 0 : -1;
  });
  $$('.secondary-panel').forEach((panel) => {
    const selected = panel.id === panelId;
    panel.classList.toggle('hidden', !selected); panel.hidden = !selected;
  });
  if (focus) button.focus();
}

$('#runBtn').addEventListener('click', run);
$('#resetBtn').addEventListener('click', reset);
$('#taskInput').addEventListener('input', () => setTaskError(''));
$('#taskInput').addEventListener('keydown', (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') { event.preventDefault(); run(); }
});
$('#controlBtn').addEventListener('click', () => {
  if (state.running) return;
  state.control = state.control === 'test' ? 'human' : 'test'; renderSummary();
});
$$('.permission-toggle').forEach((button) => button.addEventListener('click', () => {
  if (state.running) return;
  const key = button.dataset.permission; state.permissions[key] = !state.permissions[key];
  $('#permissionFeedback').textContent = ''; renderPermissions();
}));
$('#newTabBtn').addEventListener('click', () => {
  if (state.running) return;
  const id = Math.max(0, ...state.tabs.map((tab) => tab.id)) + 1;
  state.tabs.push({ id, title: `Test tab ${id}`, url: 'about:blank' }); state.tab = id;
  renderTabs({ focusTabId: id }); renderBrowser();
});
$('#closeTabBtn').addEventListener('click', closeCurrentTab);
$('#reloadBtn').addEventListener('click', () => {
  renderBrowser('loading'); clearTimeout(state.timer); state.timer = setTimeout(() => renderBrowser(), 250);
});
$('#backBtn').addEventListener('click', () => { activeTab().url = 'https://wikipedia.org'; renderBrowser(); });
$('#forwardBtn').addEventListener('click', () => {
  activeTab().url = `https://wikipedia.org/wiki/Special:Search?search=${encodeURIComponent(state.query || 'ROOM-HOP')}`; renderBrowser();
});
$('#urlInput').addEventListener('keydown', (event) => {
  if (event.key === 'Enter') { event.preventDefault(); activeTab().url = event.target.value; renderBrowser(); }
});
$$('.demo-choice').forEach((button) => button.addEventListener('click', () => {
  if (state.running) return;
  const scenario = button.dataset.scenario;
  if (scenarios[scenario]) state.scenario = scenario;
  reset();
}));
$$('.secondary-tab').forEach((button) => {
  button.addEventListener('click', () => selectInfoTab(button));
  button.addEventListener('keydown', (event) => {
    const tabs = $$('.secondary-tab'); const index = tabs.indexOf(button); let next = null;
    if (event.key === 'ArrowRight') next = tabs[(index + 1) % tabs.length];
    else if (event.key === 'ArrowLeft') next = tabs[(index - 1 + tabs.length) % tabs.length];
    else if (event.key === 'Home') next = tabs[0]; else if (event.key === 'End') next = tabs[tabs.length - 1];
    if (next) { event.preventDefault(); selectInfoTab(next, { focus: true }); }
  });
});
$('#railCollapse').addEventListener('click', () => {
  const rail = $('.agent-rail'); const collapsed = rail.classList.toggle('compact');
  $('#railCollapse').setAttribute('aria-expanded', String(!collapsed));
});
render();
