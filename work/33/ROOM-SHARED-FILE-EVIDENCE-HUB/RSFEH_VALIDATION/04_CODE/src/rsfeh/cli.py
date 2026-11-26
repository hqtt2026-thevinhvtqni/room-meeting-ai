"""CLI entry for RSFEH."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .store import RSFEHError, Store


def _default_root() -> Path:
    env = os.environ.get("RSFEH_ROOT")
    if env:
        return Path(env)
    return Path.cwd() / "rsfeh_data"


def _print_json(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def cmd_init(args: argparse.Namespace) -> int:
    store = Store(args.root)
    store.init()
    store.close()
    print(f"Initialized RSFEH at {Path(args.root).resolve()}")
    return 0


def cmd_put(args: argparse.Namespace) -> int:
    store = Store(args.root)
    try:
        data = Path(args.path).read_bytes()
        meta = store.put(
            data,
            original_name=args.name or Path(args.path).name,
            agent=args.agent,
            media_type=args.media_type,
            work_id=args.work_id,
            evidence_ref=args.evidence_ref,
            notes=args.notes,
        )
        _print_json(meta)
        return 0
    except RSFEHError as e:
        print(f"ERROR [{e.code}]: {e}", file=sys.stderr)
        return 1
    finally:
        store.close()


def cmd_get(args: argparse.Namespace) -> int:
    store = Store(args.root)
    try:
        data = store.get_bytes(args.file_id, agent=args.agent)
        if args.out:
            Path(args.out).write_bytes(data)
            print(f"Wrote {len(data)} bytes to {args.out}")
        else:
            sys.stdout.buffer.write(data)
        return 0
    except RSFEHError as e:
        print(f"ERROR [{e.code}]: {e}", file=sys.stderr)
        return 1
    finally:
        store.close()


def cmd_list(args: argparse.Namespace) -> int:
    store = Store(args.root)
    try:
        rows = store.list_files(work_id=args.work_id, status=args.status, limit=args.limit)
        _print_json(rows)
        return 0
    except RSFEHError as e:
        print(f"ERROR [{e.code}]: {e}", file=sys.stderr)
        return 1
    finally:
        store.close()


def cmd_search(args: argparse.Namespace) -> int:
    store = Store(args.root)
    try:
        rows = store.search(args.query, work_id=args.work_id, limit=args.limit)
        _print_json(rows)
        return 0
    except RSFEHError as e:
        print(f"ERROR [{e.code}]: {e}", file=sys.stderr)
        return 1
    finally:
        store.close()


def cmd_verify(args: argparse.Namespace) -> int:
    store = Store(args.root)
    try:
        detail = store.verify(args.file_id, agent=args.agent)
        _print_json(detail)
        return 0
    except RSFEHError as e:
        print(f"ERROR [{e.code}]: {e}", file=sys.stderr)
        return 1
    finally:
        store.close()


def cmd_link(args: argparse.Namespace) -> int:
    store = Store(args.root)
    try:
        meta = store.link_work(
            args.file_id, args.work_id, evidence_ref=args.evidence_ref, agent=args.agent
        )
        _print_json(meta)
        return 0
    except RSFEHError as e:
        print(f"ERROR [{e.code}]: {e}", file=sys.stderr)
        return 1
    finally:
        store.close()


def cmd_audit(args: argparse.Namespace) -> int:
    store = Store(args.root)
    try:
        rows = store.audit_tail(limit=args.limit)
        _print_json(rows)
        return 0
    except RSFEHError as e:
        print(f"ERROR [{e.code}]: {e}", file=sys.stderr)
        return 1
    finally:
        store.close()


def cmd_meta(args: argparse.Namespace) -> int:
    store = Store(args.root)
    try:
        meta = store.get_meta(args.file_id)
        _print_json(meta)
        return 0
    except RSFEHError as e:
        print(f"ERROR [{e.code}]: {e}", file=sys.stderr)
        return 1
    finally:
        store.close()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="rsfeh",
        description="ROOM Shared File & Evidence Hub (Work 33)",
    )
    p.add_argument(
        "--root",
        default=str(_default_root()),
        help="RSFEH root directory (or set RSFEH_ROOT)",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_agent(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--agent", default="system", help="Acting agent identity string")

    s = sub.add_parser("init", help="Initialize empty store")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("put", help="Store a file")
    add_agent(s)
    s.add_argument("path", help="Local file path to store")
    s.add_argument("--name", help="Override original name")
    s.add_argument("--media-type", dest="media_type")
    s.add_argument("--work-id", dest="work_id")
    s.add_argument("--evidence-ref", dest="evidence_ref")
    s.add_argument("--notes")
    s.set_defaults(func=cmd_put)

    s = sub.add_parser("get", help="Retrieve file bytes")
    add_agent(s)
    s.add_argument("file_id")
    s.add_argument("--out", help="Write to path instead of stdout")
    s.set_defaults(func=cmd_get)

    s = sub.add_parser("list", help="List files")
    s.add_argument("--work-id", dest="work_id")
    s.add_argument("--status", default="active")
    s.add_argument("--limit", type=int, default=100)
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("search", help="Search by name/sha/id/work")
    s.add_argument("query")
    s.add_argument("--work-id", dest="work_id")
    s.add_argument("--limit", type=int, default=50)
    s.set_defaults(func=cmd_search)

    s = sub.add_parser("verify", help="Verify integrity of a file")
    add_agent(s)
    s.add_argument("file_id")
    s.set_defaults(func=cmd_verify)

    s = sub.add_parser("link", help="Link file to a Work ID")
    add_agent(s)
    s.add_argument("file_id")
    s.add_argument("work_id")
    s.add_argument("--evidence-ref", dest="evidence_ref")
    s.set_defaults(func=cmd_link)

    s = sub.add_parser("audit", help="Show recent audit events")
    s.add_argument("--limit", type=int, default=50)
    s.set_defaults(func=cmd_audit)

    s = sub.add_parser("meta", help="Show file metadata")
    s.add_argument("file_id")
    s.set_defaults(func=cmd_meta)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
