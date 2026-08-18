"""
Tests cho Secretary v0.3 — Raw Transcript Record Keeper.

Contract:
    Secretary.append(text) -> {"status": "READY"}
    Secretary.read() -> str
    Secretary.export() -> str

Secretary KHONG duoc: nhan dien speaker, parse cau lenh, sua whitespace,
doi CRLF->LF, them timestamp/metadata, tu tao summary, giu reference toi
Meeting, import MeetingManager/Governance/Discussion/IntentRouter.
"""

import ast
import inspect

import pytest

from core.secretary import Secretary


@pytest.fixture
def secretary(tmp_path):
    return Secretary(transcript_path=tmp_path / "transcript.txt")


class TestSecretaryAppendReturnsReady:
    def test_append_returns_ready_status(self, secretary):
        result = secretary.append("Xu: Toi de xuat phuong an A.")
        assert result == {"status": "READY"}


class TestSecretaryReadRoundTrip:
    def test_append_then_read_is_identical(self, secretary):
        block = "Xu: Toi de xuat phuong an A."
        secretary.append(block)
        assert secretary.read() == block

    def test_multiline_block_preserved_exactly(self, secretary):
        block = (
            "Xu: Toi de xuat phuong an A.\n\n"
            "Claude: Toi dong y.\n\n"
            "Vinh: Giu nguyen phuong an nay.\n"
            "    Dong nay co indent."
        )
        secretary.append(block)
        assert secretary.read() == block

    def test_leading_and_trailing_whitespace_preserved(self, secretary):
        block = "   leading spaces\ntrailing spaces   \n"
        secretary.append(block)
        assert secretary.read() == block

    def test_blank_lines_preserved(self, secretary):
        block = "line one\n\n\nline two"
        secretary.append(block)
        assert secretary.read() == block

    def test_unicode_preserved(self, secretary):
        block = "Vinh: Xin chào các bạn, đây là tiếng Việt có dấu — 100% nguyên văn."
        secretary.append(block)
        assert secretary.read() == block

    def test_crlf_preserved_not_converted_to_lf(self, secretary):
        block = "line one\r\nline two\r\nline three"
        secretary.append(block)
        assert secretary.read() == block
        assert "\r\n" in secretary.read()

    def test_lf_not_converted_to_crlf(self, secretary):
        block = "line one\nline two"
        secretary.append(block)
        assert secretary.read() == block
        assert "\r\n" not in secretary.read()

    def test_read_on_empty_transcript_returns_empty_string(self, secretary):
        assert secretary.read() == ""


class TestSecretaryAppendDoesNotInsertContent:
    """append() khong tu chen bat ky ky tu nao — caller kiem soat separator."""

    def test_no_separator_auto_inserted_between_appends(self, secretary):
        secretary.append("AAA")
        secretary.append("BBB")
        assert secretary.read() == "AAABBB"

    def test_caller_controlled_newline_separator(self, secretary):
        secretary.append("AAA\n")
        secretary.append("BBB\n")
        assert secretary.read() == "AAA\nBBB\n"

    def test_caller_controlled_blank_line_separator(self, secretary):
        secretary.append("AAA\n\n")
        secretary.append("BBB\n")
        assert secretary.read() == "AAA\n\nBBB\n"

    def test_no_timestamp_added_to_transcript(self, secretary):
        secretary.append("hello world")
        content = secretary.read()
        assert content == "hello world"

    def test_no_metadata_or_speaker_label_added(self, secretary):
        block = "hello world"
        secretary.append(block)
        # append() khong duoc tu them nhan speaker/metadata neu caller khong dua vao
        assert secretary.read() == block

    def test_does_not_alter_delete_request_into_action(self, secretary):
        secretary.append("Xoa meetings di.")
        assert secretary.read() == "Xoa meetings di."

    def test_handles_empty_string_append(self, secretary):
        result = secretary.append("")
        assert result == {"status": "READY"}
        assert secretary.read() == ""


class TestSecretaryExport:
    def test_export_equals_read(self, secretary):
        block = "Xu: noi dung.\nClaude: dong y."
        secretary.append(block)
        assert secretary.export() == secretary.read()

    def test_export_does_not_add_summary_text(self, secretary):
        secretary.append("noi dung bat ky")
        exported = secretary.export()
        assert "tóm tắt" not in exported.lower()
        assert "summary" not in exported.lower()


class TestSecretaryPublicApiIsMinimal:
    def test_public_api_is_exactly_append_read_export(self):
        public_methods = {
            name
            for name in dir(Secretary)
            if not name.startswith("_") and callable(getattr(Secretary, name))
        }
        assert public_methods == {"append", "read", "export"}


class TestSecretaryNeverInterprets:
    def test_secretary_module_does_not_import_forbidden_modules(self):
        """
        Kiem tra tinh (khong phai runtime): secretary.py khong duoc import
        MeetingManager/Governance/Discussion/IdentityResolution/IntentRouter
        duoi bat ky hinh thuc nao.
        """
        import core.secretary as secretary_module

        source = inspect.getsource(secretary_module)
        tree = ast.parse(source)
        imported_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    imported_names.add(node.module)
                for alias in node.names:
                    imported_names.add(alias.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imported_names.add(alias.name)

        forbidden = {
            "MeetingManager", "meeting_manager",
            "Governance", "governance", "AuthorizationEngine",
            "Discussion", "discussion",
            "IdentityResolution", "identity_resolution",
            "IntentRouter", "LlamaIntentRouter", "intent_router",
            "llama_intent_router", "gemini_intent_router",
        }
        assert imported_names.isdisjoint(forbidden), imported_names & forbidden

    def test_secretary_instance_has_no_meeting_reference(self, secretary):
        forbidden_attr_names = {"meeting", "meeting_dir", "meeting_manager"}
        actual_attrs = set(vars(secretary).keys())
        assert actual_attrs.isdisjoint(forbidden_attr_names), actual_attrs & forbidden_attr_names
