from pathlib import Path
import hashlib
from core.secretary import Secretary

path = Path("meetings/MEETING-2026-008/test_case_c_transcript.txt")

if path.exists():
    path.unlink()

secretary = Secretary(path)

block_a = "BLOCK-A\nDòng thứ hai A."
block_b = "\nBLOCK-B\n  Có khoảng trắng."
block_c = "\n\nBLOCK-C\nKết thúc."

expected = block_a + block_b + block_c

print("APPEND A:", secretary.append(block_a))
print("APPEND B:", secretary.append(block_b))
print("APPEND C:", secretary.append(block_c))

actual = secretary.read()

expected_bytes = expected.encode("utf-8")
actual_bytes = actual.encode("utf-8")

expected_sha = hashlib.sha256(expected_bytes).hexdigest()
actual_sha = hashlib.sha256(actual_bytes).hexdigest()

print("TEXT_IDENTICAL:", actual == expected)
print("BYTE_IDENTICAL:", actual_bytes == expected_bytes)
print("EXPECTED_BYTES:", len(expected_bytes))
print("ACTUAL_BYTES:", len(actual_bytes))
print("EXPECTED_SHA256:", expected_sha)
print("ACTUAL_SHA256:", actual_sha)
print("SHA_IDENTICAL:", expected_sha == actual_sha)

print("\n--- STORED CONTENT ---")
print(repr(actual))