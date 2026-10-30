#!/usr/bin/env python3
"""Validate Work 70 official document codes in DOC-040.

Uses only the Python standard library. Legacy references are preserved and
reported separately; they are not treated as newly issued codes.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

TYPE_CODES = {
    "BB", "QD", "LENH", "PL", "KH", "YC", "TK", "QT", "HD", "BC",
    "BM", "HS", "TB", "CV",
}
NEW_CODE_RE = re.compile(
    r"^(BB|QD|LENH|PL|KH|YC|TK|QT|HD|BC|BM|HS|TB|CV)-W70-(\\d{8})-(\\d{3})$"
)
DOC_ID_RE = re.compile(r"^\\|\\s*(DOC-\\d{3})\\s*\\|")


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def registered_doc_ids(register_text: str) -> set[str]:
    return {m.group(1) for line in register_text.splitlines()
            if (m := DOC_ID_RE.match(line))}


def validate(document_register: str, code_register: str) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    known_doc_ids = registered_doc_ids(document_register)
    seen_codes: set[str] = set()
    counts = {"records": 0, "legacy": 0, "new": 0, "issued": 0}

    in_table = False
    for line_no, line in enumerate(code_register.splitlines(), start=1):
        if line.startswith("| STT | Mã văn bản |"):
            in_table = True
            continue
        if not in_table or not line.startswith("|"):
            continue
        cells = split_table_row(line)
        if len(cells) < 12 or set(cells[0]) <= {"-", ":"}:
            continue

        serial, code, doc_id, type_code = cells[:4]
        title, issue_date, author, approver, related, status, canonical_path, evidence = cells[4:12]
        if code in {"—", "-", ""}:
            continue
        counts["records"] += 1

        if code in seen_codes:
            errors.append(f"line {line_no}: duplicate document code {code}")
        seen_codes.add(code)

        if doc_id not in known_doc_ids:
            errors.append(f"line {line_no}: DOC-ID {doc_id} is absent from Document Register")

        if status.startswith("LEGACY_REFERENCE"):
            counts["legacy"] += 1
            if status.split()[0] != "LEGACY_REFERENCE":
                errors.append(f"line {line_no}: malformed legacy status for {code}")
            continue

        match = NEW_CODE_RE.fullmatch(code)
        if not match:
            errors.append(f"line {line_no}: invalid new-code format {code}")
            continue

        prefix, date_text, sequence = match.groups()
        counts["new"] += 1
        if prefix != type_code:
            errors.append(
                f"line {line_no}: code prefix {prefix} does not match type column {type_code}"
            )
        try:
            datetime.strptime(date_text, "%Y%m%d")
        except ValueError:
            errors.append(f"line {line_no}: invalid issue date in {code}")
        if int(sequence) < 1:
            errors.append(f"line {line_no}: sequence must start at 001 in {code}")

        if status in {"ISSUED", "EFFECTIVE"}:
            counts["issued"] += 1
            if approver in {"—", "-", ""}:
                errors.append(f"line {line_no}: {status} record {code} has no approver")
            if evidence in {"—", "-", ""}:
                errors.append(f"line {line_no}: {status} record {code} has no issuance evidence")

    if not known_doc_ids:
        errors.append("Document Register contains no recognizable DOC-ID rows")
    return errors, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-root", type=Path,
                        default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    register_path = args.work_root / "00_ROOT" / "DOCUMENT_REGISTER.md"
    code_path = args.work_root / "00_ROOT" / "DOC-040_SO-DANG-KY-MA-VAN-BAN_OFFICIAL-DOCUMENT-CODE-REGISTER.md"

    try:
        register_text = register_path.read_text(encoding="utf-8")
        code_text = code_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"BLOCKED: cannot read required input: {exc}", file=sys.stderr)
        return 2

    errors, counts = validate(register_text, code_text)
    print(
        "Records: {records}; legacy references: {legacy}; new codes: {new}; "
        "issued/effective: {issued}".format(**counts)
    )
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: document-code register structure and uniqueness checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
