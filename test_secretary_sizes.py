from pathlib import Path
import hashlib
import time

from core.secretary import Secretary



if __name__ == "__main__":
    TEST_DIR = Path("secretary_size_tests")
    TEST_DIR.mkdir(exist_ok=True)

    TARGETS = [
        5 * 1024 * 1024,
        10 * 1024 * 1024,
        50 * 1024 * 1024,
    ]


    def build_content(target_bytes: int) -> str:
        """
        Tạo text Unicode đủ lớn để đạt gần/đúng target byte.
        Dùng UTF-8 và có newline, Unicode, emoji để test thực tế hơn.
        """
        unit = (
            "Xu: Secretary v0.3 LONG SIZE TEST — "
            "Việt Nam — Kinh Dịch — 🧠 🚀 🔬 — "
            "ROOM HOP transcript integrity.\n"
        )

        unit_bytes = len(unit.encode("utf-8"))

        repeats = target_bytes // unit_bytes
        remainder = target_bytes - (repeats * unit_bytes)

        content = unit * repeats

        if remainder:
            raw = unit.encode("utf-8")
            content += raw[:remainder].decode("utf-8", errors="ignore")

        # Điều chỉnh lại nếu decode UTF-8 làm hụt vài bytes.
        while len(content.encode("utf-8")) < target_bytes:
            content += "X"

        # Cắt chính xác về target byte.
        data = content.encode("utf-8")[:target_bytes]

        # Đảm bảo không cắt giữa một UTF-8 character.
        content = data.decode("utf-8", errors="ignore")

        return content


    def run_test(target_bytes: int):
        label = f"{target_bytes / (1024 * 1024):.0f}MB"

        path = TEST_DIR / f"transcript_{label}.txt"

        if path.exists():
            path.unlink()

        print()
        print("=" * 70)
        print(f"TEST: {label}")
        print("=" * 70)

        print("Generating content...")

        expected = build_content(target_bytes)
        expected_bytes = expected.encode("utf-8")

        print("EXPECTED_BYTES:", len(expected_bytes))

        start = time.perf_counter()

        secretary = Secretary(path)
        result = secretary.append(expected)

        write_time = time.perf_counter() - start

        print("RESULT:", result)
        print("WRITE_TIME_SEC:", round(write_time, 3))

        start = time.perf_counter()

        actual = secretary.read()
        actual_bytes = path.read_bytes()

        read_time = time.perf_counter() - start

        expected_sha = hashlib.sha256(expected_bytes).hexdigest()
        actual_sha = hashlib.sha256(actual_bytes).hexdigest()

        print("ACTUAL_BYTES:", len(actual_bytes))
        print("EXPECTED_CHARS:", len(expected))
        print("ACTUAL_CHARS:", len(actual))

        print("TEXT_IDENTICAL:", actual == expected)
        print("BYTE_IDENTICAL:", actual_bytes == expected_bytes)

        print("EXPECTED_SHA256:", expected_sha)
        print("ACTUAL_SHA256:", actual_sha)
        print("SHA_IDENTICAL:", expected_sha == actual_sha)

        print("READ_TIME_SEC:", round(read_time, 3))

        print("PASS:",
              len(actual_bytes) == len(expected_bytes)
              and actual_bytes == expected_bytes
              and expected_sha == actual_sha)

        return {
            "target": label,
            "expected": len(expected_bytes),
            "actual": len(actual_bytes),
            "text": actual == expected,
            "bytes": actual_bytes == expected_bytes,
            "sha": expected_sha == actual_sha,
            "write_sec": round(write_time, 3),
            "read_sec": round(read_time, 3),
        }


    results = []

    for target in TARGETS:
        results.append(run_test(target))


    print()
    print()
    print("=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    for r in results:
        print(
            f"{r['target']:>5} | "
            f"expected={r['expected']:,} | "
            f"actual={r['actual']:,} | "
            f"text={r['text']} | "
            f"bytes={r['bytes']} | "
            f"sha={r['sha']} | "
            f"write={r['write_sec']}s | "
            f"read={r['read_sec']}s"
        )