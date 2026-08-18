from pathlib import Path
import hashlib

from core.secretary import Secretary

path = Path("test_long_transcript.txt")
secretary = Secretary(path)

# Tạo block lớn: nhiều dòng + Unicode + khoảng trắng
blocks = []

for i in range(1, 10001):
    blocks.append(
        f"Agent-{i}: Đây là dòng kiểm thử Secretary v0.3 — "
        f"Việt Nam — Kinh Dịch — 🧠 🚀 🔬 — "
        f"  khoảng trắng  cuối  \n"
    )

expected = "".join(blocks)

result = secretary.append(expected)
actual = secretary.read()

expected_bytes = expected.encode("utf-8")
actual_bytes = path.read_bytes()

print("RESULT:", result)
print("EXPECTED_CHARS:", len(expected))
print("ACTUAL_CHARS:", len(actual))
print("EXPECTED_BYTES:", len(expected_bytes))
print("ACTUAL_BYTES:", len(actual_bytes))

print("TEXT_IDENTICAL:", actual == expected)
print("BYTE_IDENTICAL:", actual_bytes == expected_bytes)

expected_sha = hashlib.sha256(expected_bytes).hexdigest()
actual_sha = hashlib.sha256(actual_bytes).hexdigest()

print("EXPECTED_SHA256:", expected_sha)
print("ACTUAL_SHA256:", actual_sha)
print("SHA_IDENTICAL:", expected_sha == actual_sha)

print("LINES:", actual.count("\n"))