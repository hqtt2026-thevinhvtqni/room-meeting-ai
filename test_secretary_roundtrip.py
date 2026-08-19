from pathlib import Path
from core.secretary import Secretary


if __name__ == "__main__":
    input_path = Path("transcript_test_input.txt")
    output_path = Path("transcript_test_output.txt")

    # Đọc nguyên bytes của file input
    with open(input_path, "rb") as f:
        original_bytes = f.read()

    # Decode UTF-8, không tự xử lý newline
    original_text = original_bytes.decode("utf-8")

    # Ghi qua Secretary
    s = Secretary(output_path)
    s.append(original_text)

    # Đọc lại
    read_text = s.read()
    export_text = s.export()

    # Đọc bytes output
    with open(output_path, "rb") as f:
        output_bytes = f.read()

    print("TEXT_IDENTICAL:", read_text == original_text)
    print("EXPORT_IDENTICAL:", export_text == original_text)
    print("BYTE_IDENTICAL:", output_bytes == original_bytes)
    print("INPUT_BYTES:", len(original_bytes))
    print("OUTPUT_BYTES:", len(output_bytes))
    print("CRLF_INPUT:", b"\r\n" in original_bytes)
    print("CRLF_OUTPUT:", b"\r\n" in output_bytes)
