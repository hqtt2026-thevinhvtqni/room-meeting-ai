"""Static contract checks; these do not simulate or certify a real browser."""
import json
from pathlib import Path

import server


ROOT = Path(server.ROOT)


def test_routes_json_has_expected_shape():
    routes = json.loads((ROOT / "manus-routes.json").read_text(encoding="utf-8"))
    assert isinstance(routes.get("routes"), list)
    assert routes["routes"]
    assert all(set(route) >= {"path", "title"} for route in routes["routes"])


def test_html_uses_only_local_assets_and_exposes_mock_boundary():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'href="styles.css"' in html
    assert 'rel="icon" href="data:,"' in html
    assert 'src="workflow.js"' in html
    assert 'src="app.js"' in html
    assert html.index('src="workflow.js"') < html.index('src="app.js"')
    assert "MOCK ONLY" in html
    assert "NO REAL CHROMIUM" in html
    assert "NO EXTERNAL API" in html


def test_html_has_primary_product_controls():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for element_id in ("tabs", "newTabBtn", "urlInput", "backBtn", "forwardBtn",
                       "reloadBtn", "taskInput", "taskError", "taskEcho", "runBtn",
                       "controlBtn", "timeline", "evidence", "passBox", "permissionFeedback"):
        assert f'id="{element_id}"' in html, f"Missing UI contract element: {element_id}"


def test_permissions_start_ungranted_and_are_demo_scoped():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    app = (ROOT / "app.js").read_text(encoding="utf-8")
    assert "Mặc định chưa cấp" in html
    assert "Granted for this demo only" in app
    assert "state.permissions[key] = !state.permissions[key]" in app
    assert "Workflow.missingPermissions" in app
    assert '"readPage": false' not in app  # permissions are built from explicit false values, not hard-coded grants


def test_evidence_contract_is_mock_only_and_has_no_artifact_claim():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    app = (ROOT / "app.js").read_text(encoding="utf-8")
    assert "SIMULATED EVIDENCE" in html
    assert "No screenshot file was created" in app
    assert "Workflow.buildMockEvidence" in app
    assert "DEMO COMPLETE" in html
    assert "PASS</strong>" not in html


def test_styles_define_mobile_responsive_breakpoint():
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert "@media(max-width:480px)" in css
    assert "@media(max-width:780px)" in css


def test_tab_close_control_is_operable_and_accessible():
    app = (ROOT / "app.js").read_text(encoding="utf-8")
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert 'class="tab-close" aria-label="Close tab"' in app
    assert "state.tabs.length <= 1" in app
    assert "event.stopPropagation()" in app
    assert ".tab-close:focus-visible" in css
