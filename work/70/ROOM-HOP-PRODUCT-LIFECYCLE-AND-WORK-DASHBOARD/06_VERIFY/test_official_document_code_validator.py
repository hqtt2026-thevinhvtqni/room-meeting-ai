import unittest
from validate_official_document_codes import validate

REGISTER = """| DOC-034 | P2 | 31 | Minutes | 00_ROOT/BIEN_BAN.md | DOC-001 | ACTIVE | Minutes |
| DOC-040 | P0 | 10 | Code Register | 00_ROOT/DOC-040.md | DOC-039 | ACTIVE | Ledger |
"""

def ledger(rows):
    header = "| STT | Mã văn bản | DOC-ID | Loại | Tiêu đề | Ngày cấp | Người soạn | Người ban hành/phê duyệt | Văn bản liên quan/gốc | Trạng thái | Đường dẫn chuẩn | Bằng chứng |"
    separator = "|---:|---|---|---|---|---|---|---|---|---|---|---|"
    return "\n".join([header, separator, *rows])

class ValidatorTests(unittest.TestCase):
    def test_legacy_reference_is_allowed_but_not_counted_as_new(self):
        row = "| 001 | BB-70-001 | DOC-034 | BB | Minutes | 2026-10-30 | Xu | Vinh | D70-011 | LEGACY_REFERENCE — historical | 00_ROOT/BIEN_BAN.md | Original minutes |"
        errors, counts = validate(REGISTER, ledger([row]))
        self.assertEqual(errors, [])
        self.assertEqual(counts, {"records": 1, "legacy": 1, "new": 0, "issued": 0})

    def test_valid_new_code(self):
        row = "| 002 | BB-W70-20261030-001 | DOC-034 | BB | Minutes | 2026-10-30 | Xu | Vinh | D70-011 | ISSUED | 00_ROOT/BIEN_BAN.md | Approval evidence |"
        errors, counts = validate(REGISTER, ledger([row]))
        self.assertEqual(errors, [])
        self.assertEqual(counts["issued"], 1)

    def test_accepts_expanded_document_type_codes(self):
        rows = [
            "| 002 | QDY-W70-20261031-001 | DOC-034 | QDY | Rules | 2026-10-31 | Xu | Vinh | — | DRAFT | 00_ROOT/DOC-034.md | — |",
            "| 003 | TC-W70-20261031-001 | DOC-040 | TC | Standard | 2026-10-31 | Xu | Vinh | — | DRAFT | 00_ROOT/DOC-040.md | — |",
            "| 004 | NQ-W70-20261031-001 | DOC-034 | NQ | Resolution | 2026-10-31 | Xu | Vinh | — | DRAFT | 00_ROOT/DOC-034.md | — |",
            "| 005 | TTR-W70-20261031-001 | DOC-034 | TTR | Submission | 2026-10-31 | Xu | Vinh | — | DRAFT | 00_ROOT/DOC-034.md | — |",
            "| 006 | CT-W70-20261031-001 | DOC-034 | CT | Program | 2026-10-31 | Xu | Vinh | — | DRAFT | 00_ROOT/DOC-034.md | — |",
            "| 007 | PA-W70-20261031-001 | DOC-034 | PA | Proposal | 2026-10-31 | Xu | Vinh | — | DRAFT | 00_ROOT/DOC-034.md | — |",
            "| 008 | PH-W70-20261031-001 | DOC-034 | PH | Form slip | 2026-10-31 | Xu | Vinh | — | DRAFT | 00_ROOT/DOC-034.md | — |",
            "| 009 | HDONG-W70-20261031-001 | DOC-034 | HDONG | Contract | 2026-10-31 | Xu | Vinh | — | DRAFT | 00_ROOT/DOC-034.md | — |"
        ]
        errors, counts = validate(REGISTER, ledger(rows))
        self.assertEqual(errors, [])
        self.assertEqual(counts["new"], 8)

    def test_rejects_unknown_type_prefix(self):
        row = "| 004 | ABC-W70-20261031-001 | DOC-034 | ABC | Unknown | 2026-10-31 | Xu | Vinh | — | DRAFT | 00_ROOT/DOC-034.md | — |"
        errors, _ = validate(REGISTER, ledger([row]))
        self.assertTrue(any("invalid new-code format" in e for e in errors))

    def test_rejects_prefix_type_column_mismatch(self):
        row = "| 005 | QDY-W70-20261031-001 | DOC-034 | QD | Wrong type | 2026-10-31 | Xu | Vinh | — | DRAFT | 00_ROOT/DOC-034.md | — |"
        errors, _ = validate(REGISTER, ledger([row]))
        self.assertTrue(any("does not match type column" in e for e in errors))

    def test_rejects_invalid_format_and_unknown_doc_id(self):
        row = "| 002 | BB-W70-20260230-000 | DOC-099 | BB | Minutes | 2026-02-30 | Xu | — | — | DRAFT | — | — |"
        errors, _ = validate(REGISTER, ledger([row]))
        self.assertTrue(any("absent from Document Register" in e for e in errors))
        self.assertTrue(any("invalid issue date" in e for e in errors))
        self.assertTrue(any("sequence must start at 001" in e for e in errors))

    def test_rejects_duplicate_code(self):
        row = "| 002 | BB-W70-20261030-001 | DOC-034 | BB | Minutes | 2026-10-30 | Xu | Vinh | D70-011 | DRAFT | 00_ROOT/BIEN_BAN.md | — |"
        errors, _ = validate(REGISTER, ledger([row, row]))
        self.assertTrue(any("duplicate document code" in e for e in errors))

    def test_issued_requires_approver_and_evidence(self):
        row = "| 002 | BB-W70-20261030-001 | DOC-034 | BB | Minutes | 2026-10-30 | Xu | — | D70-011 | ISSUED | 00_ROOT/BIEN_BAN.md | — |"
        errors, _ = validate(REGISTER, ledger([row]))
        self.assertTrue(any("has no approver" in e for e in errors))
        self.assertTrue(any("has no issuance evidence" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
