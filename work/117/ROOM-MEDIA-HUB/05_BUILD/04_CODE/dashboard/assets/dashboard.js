/* W117 Dashboard — client logic
 * Data source: data/snapshot.json (canonical snapshot)
 * Rules: no invented progress / no invented agent online status
 */

(function () {
  "use strict";

  const DATA_URL = "data/snapshot.json";

  function statusClass(s) {
    s = (s || "").toUpperCase();
    if (s.includes("IN_PROGRESS") || s.includes("ACKNOWLEDGED + IN_PROGRESS")) return "s-progress";
    if (s.includes("ACKNOWLEDGED")) return "s-ack";
    if (s.includes("DONE") || s.includes("PASS")) return "s-done";
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
      <span class="badge badge-auth">DASHBOARD BUILD ${auth.dashboard_build}</span>
      <span class="badge badge-not">PRODUCT BUILD ${auth.product_build}</span>
    `;
    el("header-meta").innerHTML = `
      Source of truth: TASK_BOARD.md + NHAT_KY_THI_CONG.md<br/>
      Snapshot: ${data.meta.snapshot_at} · ${data.meta.generated_by}
    `;
  }

  function renderOverview(data) {
    const o = data.overview;
    el("overview-cards").innerHTML = `
      <div class="card">
        <h3>Work Status</h3>
        <div class="value" style="font-size:1.1rem;color:var(--green)">Dashboard Authorized</div>
        <div class="sub">Product BUILD: ${o.product_status}</div>
      </div>
      <div class="card">
        <h3>Dashboard Tasks</h3>
        <div class="value">${o.dashboard_tasks_ack_in_progress} / ${o.dashboard_tasks_total}</div>
        <div class="sub">ACK + IN_PROGRESS (Go)</div>
      </div>
      <div class="card">
        <h3>Product Tasks</h3>
        <div class="value" style="color:var(--muted)">${o.product_tasks_authorized} / ${o.product_tasks_total}</div>
        <div class="sub">NOT AUTHORIZED / BLOCKED</div>
      </div>
      <div class="card">
        <h3>Primary Builder</h3>
        <div class="value" style="font-size:1.15rem">${o.primary_builder}</div>
        <div class="sub">ACK recorded ${o.primary_builder_ack}</div>
      </div>
    `;
  }

  function renderTasks(list, tbodyId) {
    const tbody = el(tbodyId);
    tbody.innerHTML = list.map(t => `
      <tr>
        <td><code>${t.id}</code></td>
        <td>${t.title}</td>
        <td>${t.owner}</td>
        <td><span class="status ${statusClass(t.status)}">${t.status}</span></td>
      </tr>
    `).join("");
  }

  function renderAgents(agents) {
    el("agents-grid").innerHTML = agents.map(a => `
      <div class="agent-card">
        <h4>${a.name}</h4>
        <div class="role">${a.role}</div>
        <div><span class="status ${statusClass(a.status)}">${a.status}</span></div>
        <div class="evidence">Evidence: ${a.evidence}</div>
      </div>
    `).join("");
  }

  function renderTimeline(items) {
    el("timeline").innerHTML = items.map(t => `
      <div class="timeline-item">
        <div class="time">${t.time}</div>
        <div class="actor">${t.actor}</div>
        <div class="desc">${t.desc}</div>
      </div>
    `).join("");
  }

  function renderProvenance(data) {
    el("provenance").innerHTML = `
      <strong>Provenance</strong><br/>
      Data snapshot taken from canonical files at <code>${data.meta.snapshot_at}</code> by ${data.meta.generated_by}.<br/>
      Sources: ${data.meta.sources.map(s => `<code>${s}</code>`).join(" · ")}<br/>
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
      if (!data.dashboard_tasks || data.dashboard_tasks.length !== 9) {
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
