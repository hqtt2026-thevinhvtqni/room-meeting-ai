#!/usr/bin/env python3
"""Read-only, registry-driven static Dashboard Preview Host. Prototype; verify before deployment."""
from __future__ import annotations

import argparse
import html
import json
import mimetypes
import re
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ALLOWED_EXTENSIONS = {
    ".html", ".css", ".js", ".json", ".svg", ".png", ".jpg",
    ".jpeg", ".webp", ".ico", ".woff", ".woff2", ".ttf"
}
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,31}$")
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
    "X-Frame-Options": "SAMEORIGIN",
    # Existing pilot pages use inline script/style; remote sources remain forbidden.
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'self'",
    "Cache-Control": "no-store",
    "Cross-Origin-Resource-Policy": "same-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()"
}


class RegistryError(Exception):
    pass


def load_registry(registry_path: Path, repo_root: Path) -> dict:
    raw = json.loads(registry_path.read_text(encoding="utf-8"))
    if raw.get("schema_version") != "1.0" or not isinstance(raw.get("works"), list):
        raise RegistryError("Unsupported or malformed registry")
    repo_root = repo_root.resolve(strict=True)
    result = {}
    for item in raw["works"]:
        work_id = item.get("work_id")
        if not isinstance(work_id, str) or not SAFE_ID.fullmatch(work_id):
            raise RegistryError("Invalid work_id")
        if work_id in result:
            raise RegistryError("Duplicate work_id")
        if not isinstance(item.get("enabled"), bool):
            raise RegistryError("Invalid enabled flag")
        root_rel = item.get("dashboard_root")
        if not isinstance(root_rel, str) or not root_rel or Path(root_rel).is_absolute():
            raise RegistryError("Invalid dashboard_root")
        root = (repo_root / root_rel).resolve(strict=False)
        if not root.is_relative_to(repo_root):
            raise RegistryError("dashboard_root escapes repository")
        views = item.get("views")
        if not isinstance(views, dict) or not views:
            raise RegistryError("Invalid views")
        resolved_views = {}
        for view, entry in views.items():
            if not isinstance(view, str) or not SAFE_ID.fullmatch(view):
                raise RegistryError("Invalid view name")
            if not isinstance(entry, str):
                raise RegistryError("Invalid view entry")
            entry_path = Path(entry)
            if entry_path.is_absolute() or ".." in entry_path.parts:
                raise RegistryError("Invalid view path")
            resolved = (root / entry_path).resolve(strict=False)
            if not resolved.is_relative_to(root):
                raise RegistryError("View escapes dashboard root")
            resolved_views[view] = resolved
        freshness = item.get("freshness_status", "UNKNOWN")
        if freshness not in ("FRESH", "STALE", "UNKNOWN"):
            raise RegistryError("Invalid freshness_status")
        result[work_id] = {
            "display_name": str(item.get("display_name", work_id)),
            "enabled": item["enabled"],
            "root": root,
            "views": resolved_views,
            "source_revision": item.get("source_revision"),
            "freshness_status": freshness,
            "last_verified_at": item.get("last_verified_at")
        }
    return result


class PreviewHandler(BaseHTTPRequestHandler):
    server_version = "ROOM-HOP-Preview/0.1"

    def _reply(self, status: int, body: bytes, content_type: str = "text/plain; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        for key, value in SECURITY_HEADERS.items():
            self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_POST(self): self._reply(405, b"Method Not Allowed")
    def do_PUT(self): self._reply(405, b"Method Not Allowed")
    def do_PATCH(self): self._reply(405, b"Method Not Allowed")
    def do_DELETE(self): self._reply(405, b"Method Not Allowed")
    def do_OPTIONS(self): self._reply(405, b"Method Not Allowed")
    def __getattr__(self, name):
        if name.startswith("do_"):
            return lambda: self._reply(405, b"Method Not Allowed")
        raise AttributeError(name)
    def do_HEAD(self): self._serve()
    def do_GET(self): self._serve()

    def log_message(self, fmt, *args):
        # Never log query strings, authorization headers or arbitrary request headers.
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _serve(self):
        decoded = unquote(urlsplit(self.path).path)
        if "\\" in decoded or "\x00" in decoded or any(p == ".." for p in decoded.split("/")):
            self._reply(400, b"Bad Request")
            return
        parts = [p for p in decoded.split("/") if p]
        if parts == ["healthz"]:
            payload = json.dumps({
                "service": "room-hop-preview-host",
                "status": "ok",
                "enabled_work_count": sum(1 for item in self.server.registry.values() if item["enabled"]),
                "mode": "read_only"
            }).encode("utf-8")
            self._reply(200, payload, "application/json; charset=utf-8")
            return
        if len(parts) == 2 and parts[0] == "work" and parts[1] in self.server.registry and not decoded.endswith("/"):
            self.send_response(308)
            self.send_header("Location", decoded + "/")
            for key, value in SECURITY_HEADERS.items():
                self.send_header(key, value)
            self.end_headers()
            return
        if len(parts) == 3 and parts[0] == "work" and parts[2] in self.server.registry.get(parts[1], {}).get("views", {}) and not decoded.endswith("/"):
            self.send_response(308)
            self.send_header("Location", decoded + "/")
            for key, value in SECURITY_HEADERS.items():
                self.send_header(key, value)
            self.end_headers()
            return
        if not parts:
            rows = "".join(
                "<li><a href='/work/" + html.escape(wid, quote=True) + "/'>"
                + html.escape(wid) + " — " + html.escape(item["display_name"])
                + "</a></li>"
                for wid, item in sorted(self.server.registry.items()) if item["enabled"]
            )
            body = ("<!doctype html><html><head><meta charset='utf-8'><title>ROOM-HOP Preview</title>"
                    "</head><body><h1>ROOM-HOP Dashboard Preview</h1><ul>" + rows
                    + "</ul></body></html>").encode("utf-8")
            self._reply(200, body, "text/html; charset=utf-8")
            return
        if len(parts) < 2 or parts[0] != "work":
            self._reply(404, b"Not Found")
            return
        work_id = parts[1]
        item = self.server.registry.get(work_id)
        if not item or not item["enabled"]:
            self._reply(404, b"Work Not Found")
            return
        if len(parts) == 2:
            view = "execution" if "execution" in item["views"] else next(iter(item["views"]))
            target = item["views"][view]
        elif parts[2] in item["views"]:
            view = parts[2]
            suffix = parts[3:]
            target = item["views"][view]
            if suffix:
                target = target.parent.joinpath(*suffix).resolve(strict=False)
        else:
            self._reply(404, b"View Not Found")
            return
        root = item["root"].resolve(strict=False)
        try:
            resolved = target.resolve(strict=True)
            if not resolved.is_relative_to(root) or not resolved.is_file():
                raise ValueError("outside root or not a file")
        except (OSError, ValueError):
            self._reply(404, b"Preview Asset Not Found")
            return
        if resolved.suffix.lower() not in ALLOWED_EXTENSIONS:
            self._reply(403, b"File Type Forbidden")
            return
        try:
            data = resolved.read_bytes()
        except OSError:
            self._reply(404, b"Preview Asset Not Found")
            return
        mime, _ = mimetypes.guess_type(str(resolved))
        if not mime:
            mime = "application/octet-stream"
        if mime.startswith("text/") or mime in ("application/javascript", "application/json", "image/svg+xml"):
            mime += "; charset=utf-8"
        if resolved.suffix.lower() == ".html":
            revision = html.escape(str(item["source_revision"] or "UNKNOWN"))
            freshness = html.escape(str(item["freshness_status"]))
            verified = html.escape(str(item["last_verified_at"] or "UNKNOWN"))
            generated = datetime.now(timezone.utc).isoformat()
            view_label = html.escape(view)
            banner = (
                "<aside style='margin:0;padding:8px 12px;background:#fff4d6;color:#503b00;"
                "font:12px/1.5 sans-serif;border-bottom:1px solid #e0c77a'>"
                "<b>PREVIEW / READ-ONLY</b> · Work " + html.escape(work_id)
                + " · View " + view_label + " · Source revision " + revision
                + " · Freshness " + freshness + " · Last verified " + verified
                + " · Rendered " + html.escape(generated) + "</aside>"
            )
            try:
                page = data.decode("utf-8")
                if re.search(r"</body\s*>", page, flags=re.IGNORECASE):
                    page = re.sub(r"</body\\s*>", banner + "</body>", page, count=1, flags=re.IGNORECASE)
                else:
                    page = banner + page
                data = page.encode("utf-8")
            except UnicodeDecodeError:
                self._reply(500, b"Dashboard HTML encoding is not UTF-8")
                return
        self._reply(200, data, mime)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--repo-root", default=".", type=Path)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8060, type=int)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve(strict=True)
    registry_path = args.registry.resolve(strict=True)
    if not registry_path.is_file():
        raise SystemExit("Registry file not found")
    registry = load_registry(registry_path, repo_root)
    if not any(item["enabled"] for item in registry.values()):
        raise SystemExit("No enabled Work dashboards")
    class Server(ThreadingHTTPServer):
        daemon_threads = True
    httpd = Server((args.host, args.port), PreviewHandler)
    httpd.registry = registry
    print(f"Preview Host listening on http://{args.host}:{args.port}/")
    print("Read-only mode: GET/HEAD only; private access layer required for remote devices.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
