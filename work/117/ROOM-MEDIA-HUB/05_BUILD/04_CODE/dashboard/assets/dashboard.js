/* W117 Dashboard — client logic
 * Data source: data/snapshot.json (canonical snapshot)
 * Rules: no invented progress / no invented agent online status
 * Security: all data-driven strings are HTML-escaped before insertion (Vibe fix, 2026-11-17)
 */

(function () {
  "use strict";

  const DATA_URL = "data/snapshot.json";

  // Escape untrusted/data-provided strings before any innerHTML insertion.
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function statusClass(s) {
    s = (s || "").toUpperCase();
    if (s.includes("DONE") || s.includes("PASS")) return "s-done";
    if (s.includes("IN_PROGRESS") || s.includes("ACKNOWLEDGED + IN_PROGRESS")) return "s-progress";
    if (s.includes("ACKNOWLEDGED")) return "s-ack";
    if (s.includes("BLOCKED")) return "s-blocked";
    if (s.includes("NOT AUTHORIZED") || s.includes("NOT READY") || s.includes("NOT RUN")) return "s-notauth";
    if (s.includes("PLANNED")) return "s-planned";
    if (s.includes("UNCONFIRMED") || s.includes("NOT VERIFIED")) return "s-unconfirmed";
    if (s.includes("ACTIVE") || s.includes("AUTHORITY")) return "s-ack";
    return "s-notauth";
  }

  function el(id) { return document.getElementById(id); }

  function renderHeader(data) {
    const auth = data.meta.authorization;
    el("header-badges").innerHTML = `
      <span class="badge badge-auth">DASHBOARD BUILD ${esc(auth.dashboard_build)}</span>
      <span class="badge badge-not">PRODUCT BUILD ${esc(auth.product_build)}</span>
    `;
    el("header-meta").innerHTML = `
      Source of truth: TASK_BOARD.md + NHAT_KY_THI_CONG.md<br/>
      Snapshot: ${esc(data.meta.snapshot_at)} · ${esc(data.meta.generated_by)}
    `;
  }

  // KPI values are derived from the task arrays themselves, not hand-written.
  function deriveKpis(data) {
    const dash = data.dashboard_tasks || [];
    const prod = data.product_tasks || [];
    const dashDone = dash.filter(t => (t.status || "").toUpperCase().includes("DONE")).length;
    const dashInProgress = dash.filter(t => {
      const s = (t.status || "").toUpperCase();
      return s.includes("IN_PROGRESS") && !s.includes("DONE");
    }).length;
    const dashUnconfirmed = dash.filter(t => (t.status || "").toUpperCase().includes("UNCONFIRMED")).length;
    const prodNotAuth = prod.filter(t => (t.status || "").toUpperCase().includes("NOT AUTHORIZED")).length;
    return { dashDone, dashInProgress, dashUnconfirmed, prodNotAuth, dashTotal: dash.length, prodTotal: prod.length };
  }

  function renderOverview(data) {
    const o = data.overview;
    const k = deriveKpis(data);
    el("overview-cards").innerHTML = `
      <div class="card">
        <h3>Work Status</h3>
        <div class="value" style="font-size:1.1rem;color:var(--green)">Dashboard Authorized</div>
        <div class="sub">Product BUILD: ${esc(o.product_status)}</div>
      </div>
      <div class="card">
        <h3>Dashboard Tasks</h3>
        <div class="value">${k.dashDone} / ${k.dashTotal}</div>
        <div class="sub">DONE (implementation) · ${k.dashInProgress} IN_PROGRESS · ${k.dashUnconfirmed} DISPATCH UNCONFIRMED</div>
      </div>
      <div class="card">
        <h3>Product Tasks</h3>
        <div class="value" style="color:var(--muted)">${k.prodTotal - k.prodNotAuth} / ${k.prodTotal}</div>
        <div class="sub">${k.prodNotAuth} NOT AUTHORIZED · rest PLANNED / BLOCKED / NOT READY / NOT RUN / IN_PROGRESS (docs only)</div>
      </div>
      <div class="card">
        <h3>Primary Builder</h3>
        <div class="value" style="font-size:1.15rem">${esc(o.primary_builder)}</div>
        <div class="sub">ACK recorded ${esc(o.primary_builder_ack)}</div>
      </div>
    `;
  }

  function renderTasks(list, tbodyId) {
    const tbody = el(tbodyId);
    tbody.innerHTML = list.map(t => `
      <tr>
        <td><code>${esc(t.id)}</code></td>
        <td>${esc(t.title)}</td>
        <td>${esc(t.owner)}</td>
        <td><span class="status ${statusClass(t.status)}">${esc(t.status)}</span></td>
      </tr>
    `).join("");
  }

  function renderAgents(agents) {
    el("agents-grid").innerHTML = agents.map(a => `
      <div class="agent-card">
        <h4>${esc(a.name)}</h4>
        <div class="role">${esc(a.role)}</div>
        <div><span class="status ${statusClass(a.status)}">${esc(a.status)}</span></div>
        <div class="evidence">Evidence: ${esc(a.evidence)}</div>
      </div>
    `).join("");
  }

  function renderTimeline(items) {
    el("timeline").innerHTML = items.map(t => `
      <div class="timeline-item">
        <div class="time">${esc(t.time)}</div>
        <div class="actor">${esc(t.actor)}</div>
        <div class="desc">${esc(t.desc)}</div>
      </div>
    `).join("");
  }

  function renderProvenance(data) {
    el("provenance").innerHTML = `
      <strong>Provenance</strong><br/>
      Data snapshot taken from canonical files at <code>${esc(data.meta.snapshot_at)}</code> by ${esc(data.meta.generated_by)}.<br/>
      Sources: ${data.meta.sources.map(s => `<code>${esc(s)}</code>`).join(" · ")}<br/>
      This Dashboard does not claim live synchronization. Refresh requires regenerating the snapshot from Sandbox.
    `;
  }

  function bindNav() {
    document.querySelectorAll("#main-nav button").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll("#main-nav button").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        document.querySelectorAll("main > section").forEach(s => s.classList.add("hidden"));
        el("view-" + btn.dataset.view).classList.remove("hidden");
      });
    });
  }

  function showError(msg) {
    const box = el("load-error");
    box.textContent = msg;
    box.classList.remove("hidden");
  }

  async function boot() {
    bindNav();
    try {
      const res = await fetch(DATA_URL, { cache: "no-store" });
      if (!res.ok) throw new Error("HTTP " + res.status + " when loading " + DATA_URL);
      const data = await res.json();

      // Basic integrity checks (client-side)
      if (!data.dashboard_tasks || data.dashboard_tasks.length !== 10) {
        console.warn("Unexpected dashboard_tasks length");
      }
      if (!data.product_tasks || data.product_tasks.length !== 13) {
        console.warn("Unexpected product_tasks length");
      }

      renderHeader(data);
      renderOverview(data);
      renderTasks(data.dashboard_tasks, "dash-tasks-body");
      renderTasks(data.product_tasks, "product-tasks-body");
      renderAgents(data.agents);
      renderTimeline(data.timeline);
      renderProvenance(data);
    } catch (err) {
      showError("Failed to load dashboard data: " + err.message + ". Open via a local server (python run.py) so fetch can read data/snapshot.json.");
      console.error(err);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
