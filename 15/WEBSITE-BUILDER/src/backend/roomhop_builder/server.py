"""Local dev entrypoint for the Work 15 backend.

Usage:
    python -m roomhop_builder.server          # binds 127.0.0.1:8020 (dev only)

Binds loopback only, never 0.0.0.0, and is not a production deployment
path (issue #34 forbids deploying to production).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running directly from a checkout without installing the package.
_BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from .api import create_app  # noqa: E402
from .evidence import compute_code_version  # noqa: E402
from .service import BuilderService  # noqa: E402

DEV_PORT = 8020


def build_service() -> BuilderService:
    repo_root = _BACKEND_ROOT
    return BuilderService(code_version=compute_code_version(repo_root))


app = create_app(build_service())


def main() -> None:
    try:
        import uvicorn
    except ImportError:  # pragma: no cover
        print("uvicorn is required for the dev server: pip install uvicorn", file=sys.stderr)
        raise SystemExit(2)
    print(f"[work15-backend] dev-only, loopback; ports: builder/service default "
          f"(NullBuilderPort / RefusedRuntimePort)")
    uvicorn.run(app, host="127.0.0.1", port=DEV_PORT, log_level="info")


if __name__ == "__main__":
    main()
