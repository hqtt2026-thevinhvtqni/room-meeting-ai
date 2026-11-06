"""ROOM HOP — Work Management Dashboard (Flask, read-only).

Chạy:
    python work_dashboard/app.py
Mở:
    http://127.0.0.1:8055
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from flask import Flask, jsonify, render_template

from scanner import scan_all  # noqa: E402

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/api/works")
def api_works():
    return jsonify(scan_all())


if __name__ == "__main__":
    print("ROOM HOP Work Dashboard -> http://127.0.0.1:8055")
    app.run(host="127.0.0.1", port=8055, debug=False)
