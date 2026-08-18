from __future__ import annotations

import codecs
from pathlib import Path
from typing import Iterator

from core.secretary import Secretary

DEFAULT_CHUNK_SIZE = 4 * 1024 * 1024  # 4 MB


def iter_utf8_text_chunks(
    file_path: str | Path,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> Iterator[str]:
    """
    Doc file theo chunk byte co dinh va decode UTF-8 an toan bang
    incremental decoder, khong bao gio cat giua mot ky tu multi-byte.

    Vi sao khong the dung `raw_bytes.decode("utf-8")` truc tiep tren
    tung chunk: bien gioi chunk 4MB la ranh gioi *byte*, khong phai
    ranh gioi *ky tu*. Neu byte cuoi cung cua mot chunk roi dung vao
    giua chuoi UTF-8 nhieu byte (vi du: dau tieng Viet, emoji), decode
    truc tiep se nem UnicodeDecodeError hoac (voi errors="ignore")
    am tham lam hong du lieu.

    IncrementalDecoder giai quyet dieu nay: no giu lai phan byte dang
    do trong buffer noi bo va ghep vao chunk ke tiep truoc khi decode,
    dam bao ket qua giong het viec decode toan bo file mot lan.
    """
    decoder = codecs.getincrementaldecoder("utf-8")(errors="strict")
    path = Path(file_path)

    with open(path, "rb") as f:
        while True:
            raw = f.read(chunk_size)
            if not raw:
                break
            text = decoder.decode(raw, final=False)
            if text:
                yield text

    # Flush bat ky byte con lai trong buffer decoder (final=True).
    # Neu file bi cat cut hoac khong phai UTF-8 hop le, loi se raise
    # o day thay vi bi nuot am tham.
    tail = decoder.decode(b"", final=True)
    if tail:
        yield tail


def import_file_into_secretary(
    file_path: str | Path,
    secretary: Secretary,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> dict:
    """
    Import mot file text lon vao Secretary, doc theo chunk + decode
    UTF-8 incremental, ghi tung chunk qua Secretary.append().

    Secretary tu no khong xu ly file — day la tang importer o ngoai,
    dung Secretary.append() nhu mot API "nguyen van", dung nhu thiet
    ke hien tai cua Secretary yeu cau.
    """
    chunks_written = 0
    for text_chunk in iter_utf8_text_chunks(file_path, chunk_size=chunk_size):
        secretary.append(text_chunk)
        chunks_written += 1
    return {"status": "READY", "chunks_written": chunks_written}
