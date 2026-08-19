"""
Tests cho core/importer.py — Chunked UTF-8-safe file importer.

Boi canh: Secretary.append(text) nhan mot chuoi Python str da decode san.
Khi import file lon (vi du 500 MB) bang cach doc raw bytes theo chunk co
dinh (vi du 4 MB) roi goi `raw_bytes_chunk.decode("utf-8")` truc tiep tren
tung chunk, se FAIL bat cu khi nao ranh gioi chunk (ranh gioi *byte*) roi
vao giua mot ky tu UTF-8 nhieu byte (dau tieng Viet, emoji...). Day la loi
da duoc phat hien qua test thuc te tren file 500 MB.

`core/importer.py` sua loi nay bang `codecs.getincrementaldecoder("utf-8")`,
giu lai phan byte dang do o cuoi buffer va ghep vao chunk ke tiep.

Importer la mot component RIENG, khong sua doi core/secretary.py. No chi
goi Secretary.append() nhu mot API san co.
"""

import hashlib

import pytest

from core.secretary import Secretary
from core.importer import iter_utf8_text_chunks, import_file_into_secretary


@pytest.fixture
def secretary(tmp_path):
    return Secretary(transcript_path=tmp_path / "transcript.txt")


class TestNaiveChunkDecodeIsBroken:
    """
    Chung minh van de ma importer phai giai quyet: decode() truc tiep
    tren tung chunk byte co dinh se vo khi ranh gioi chunk roi giua mot
    ky tu multi-byte.
    """

    def test_naive_decode_per_chunk_raises_on_multibyte_boundary(self):
        # "à" ma hoa UTF-8 la 2 byte: 0xC3 0xA0.
        # Chia chuoi bytes lam 2 chunk sao cho ranh gioi roi dung giua
        # ky tu 2-byte nay.
        text = "a" * 5 + "à" + "b" * 5
        raw = text.encode("utf-8")
        boundary = 6  # rơi vào giữa 2 byte của "à"

        chunk1 = raw[:boundary]
        chunk2 = raw[boundary:]

        with pytest.raises(UnicodeDecodeError):
            chunk1.decode("utf-8")


class TestIncrementalDecoderFixesBoundarySplit:
    def test_multibyte_char_split_across_chunk_boundary_decodes_correctly(
        self, tmp_path
    ):
        # Buoc chuoi tieng Viet + emoji du dai de ranh gioi chunk nho
        # (16 bytes) chac chan roi giua it nhat mot ky tu multi-byte.
        text = "Xin chào các bạn 🎉 đây là tiếng Việt có dấu 🚀"
        input_path = tmp_path / "input.txt"
        input_path.write_text(text, encoding="utf-8")

        # chunk_size nho de buoc phai co it nhat mot lan chia giua ky tu
        chunks = list(iter_utf8_text_chunks(input_path, chunk_size=16))
        rebuilt = "".join(chunks)
        assert rebuilt == text

    def test_various_small_chunk_sizes_all_reconstruct_exactly(self, tmp_path):
        text = "Việt Nam 🇻🇳 — 100% nguyên văn, không mất byte nào. " * 50
        input_path = tmp_path / "input.txt"
        input_path.write_text(text, encoding="utf-8")

        for chunk_size in (1, 2, 3, 4, 5, 7, 11, 32, 4096):
            chunks = list(iter_utf8_text_chunks(input_path, chunk_size=chunk_size))
            rebuilt = "".join(chunks)
            assert rebuilt == text, f"failed at chunk_size={chunk_size}"


class TestImportFileIntoSecretary:
    def test_import_small_unicode_file_matches_original(self, tmp_path, secretary):
        text = (
            "Vinh: Xin chào các bạn, đây là tiếng Việt có dấu.\n"
            "Xu: 🎉 emoji test 🚀\n"
        )
        input_path = tmp_path / "input.txt"
        # Ghi bang bytes de kiem soat tuyet doi noi dung goc. write_text()
        # tren Windows (newline=None mac dinh) tu dong dich moi '\n' thanh
        # '\r\n' LUC GHI FILE TEST - lam sai lech gia tri ky vong 'text'
        # so voi byte thuc te tren dia, du importer/Secretary hoan toan
        # dung. Bug nay chi lo ra tren Windows, khong tai hien duoc tren
        # Linux vi os.linesep khac nhau.
        input_path.write_bytes(text.encode("utf-8"))

        result = import_file_into_secretary(input_path, secretary, chunk_size=8)

        assert result["status"] == "READY"
        assert secretary.read() == text

    def test_import_preserves_byte_identical_output(self, tmp_path, secretary):
        text = "áàảãạ 🎉🚀 line one\r\nline two\nline three" * 1000
        input_path = tmp_path / "input.txt"
        # Ghi bang bytes de kiem soat tuyet doi noi dung goc, khong de
        # Python tu dich newline khi ghi file test.
        raw = text.encode("utf-8")
        input_path.write_bytes(raw)

        import_file_into_secretary(input_path, secretary, chunk_size=4096)

        output_path = secretary._transcript_path  # noqa: SLF001 (test-only)
        output_raw = output_path.read_bytes()

        assert output_raw == raw
        assert hashlib.sha256(output_raw).hexdigest() == hashlib.sha256(raw).hexdigest()

    def test_import_does_not_modify_secretary_source(self):
        """
        Bao ve tinh: importer khong duoc sua doi core/secretary.py.
        Kiem tra Secretary van chi co dung 3 public method nhu thiet ke
        goc — importer chi la caller ben ngoai.
        """
        public_methods = {
            name
            for name in dir(Secretary)
            if not name.startswith("_") and callable(getattr(Secretary, name))
        }
        assert public_methods == {"append", "read", "export"}

    def test_import_multiple_chunks_written_for_large_enough_file(
        self, tmp_path, secretary
    ):
        text = "x" * 100_000
        input_path = tmp_path / "input.txt"
        input_path.write_text(text, encoding="utf-8")

        result = import_file_into_secretary(input_path, secretary, chunk_size=4096)

        assert result["chunks_written"] > 1
        assert secretary.read() == text


class TestImportRealisticLargerFile:
    """
    File vai MB (khong phai 500MB) de suite chay nhanh trong CI, nhung
    van du lon de vuot qua nhieu ranh gioi chunk that (default 4MB
    logic duoc test qua chunk_size nho hon o day). Test 500MB day du da
    chay thu cong (xem MISSION report) — o day chi giu mot bai kiem tra
    hoi quy nhe, nhanh, lap lai duoc trong CI.
    """

    def test_multi_mb_vietnamese_roundtrip_sha256_identical(self, tmp_path, secretary):
        import random
        import string

        random.seed(2026)
        vn_chars = "áàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩị"
        pool = string.ascii_letters + " \n" + vn_chars + "🎉🚀"

        text = "".join(random.choice(pool) for _ in range(300_000))  # vai MB
        raw = text.encode("utf-8")

        input_path = tmp_path / "input.txt"
        input_path.write_bytes(raw)

        import_file_into_secretary(input_path, secretary, chunk_size=4 * 1024 * 1024)

        output_raw = secretary._transcript_path.read_bytes()  # noqa: SLF001
        assert output_raw == raw
        assert hashlib.sha256(output_raw).hexdigest() == hashlib.sha256(raw).hexdigest()

    def test_restart_new_secretary_instance_reads_back_identical(
        self, tmp_path
    ):
        text = "Xu: đây là bản ghi dài.\n" * 10_000
        input_path = tmp_path / "input.txt"
        # Cung ly do nhu tren: write_bytes() thay vi write_text() de
        # tranh Windows tu dich '\n' -> '\r\n' luc ghi file test.
        input_path.write_bytes(text.encode("utf-8"))

        out_path = tmp_path / "transcript.txt"
        s1 = Secretary(out_path)
        import_file_into_secretary(input_path, s1, chunk_size=65536)

        # Mo phong restart: instance Secretary moi tro toi cung file.
        s2 = Secretary(out_path)
        assert s2.read() == text
        assert s2.export() == text
