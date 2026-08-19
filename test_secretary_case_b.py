from pathlib import Path
import hashlib
from core.secretary import Secretary


if __name__ == "__main__":
    path = Path("meetings/MEETING-2026-008/test_case_b_transcript.txt")

    if path.exists():
        path.unlink()

    secretary = Secretary(path)

    expected = (
        "Xu:\tĐây là TEST B.\n"
        "\n"
        "Claude:    nhiều khoảng trắng.\n"
        "Me:    khoảng trắng đầu dòng.\n"
        "  Vinh: hai space đầu dòng.\n"
        "Dòng có space cuối.  \n"
        "\n"
        "\n"
        "Emoji: 🧠 🚀 🔬\n"
        "Unicode: Việt Nam — Kinh Dịch — Ω — 中文\n"
        "---\n"
        "```text\n"
        "raw content\n"
        "```\n"
    )

    result = secretary.append(expected)
    actual = secretary.read()

    expected_bytes = expected.encode("utf-8")
    actual_bytes = actual.encode("utf-8")

    print("RESULT:", result)
    print("TEXT_IDENTICAL:", actual == expected)
    print("BYTE_IDENTICAL:", actual_bytes == expected_bytes)

    print("EXPECTED_BYTES:", len(expected_bytes))
    print("ACTUAL_BYTES:", len(actual_bytes))

    print(
        "EXPECTED_SHA256:",
        hashlib.sha256(expected_bytes).hexdigest()
    )

    print(
        "ACTUAL_SHA256:",
        hashlib.sha256(actual_bytes).hexdigest()
    )

    print("SHA_IDENTICAL:",
          hashlib.sha256(expected_bytes).hexdigest()
          == hashlib.sha256(actual_bytes).hexdigest())

    raw = path.read_bytes()

    print("CRLF:", b"\r\n" in raw)
    print("LF:", b"\n" in raw)

    print("\n--- STORED CONTENT ---")
    print(actual)