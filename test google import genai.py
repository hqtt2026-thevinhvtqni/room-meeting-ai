import os
from dotenv import load_dotenv
from google import genai

load_dotenv() # đọc file .env

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Chưa có GEMINI_API_KEY trong .env")
    exit()

client = genai.Client(api_key=api_key)

try:
    # Test list model + gọi thử 1 câu
    print("🔑 Key OK, đang gọi Gemini...")
    response = client.models.generate_content(
        model="gemini-2.0-flash", # model rẻ, nhanh để test
        contents="Chào Gemini, trả lời đúng 1 câu: 2+2 bằng mấy?"
    )
    print(f"✅ Thành công! Gemini trả lời: {response.text}")
    
    # Check quota
    print("\n📊 Key hoạt động bình thường, có thể dùng cho ROOM HOP.")

except Exception as e:
    print(f"⛔ Lỗi: {e}")
    if "API_KEY_INVALID" in str(e):
        print("-> Key sai hoặc chưa enable Generative Language API")
    elif "quota" in str(e).lower():
        print("-> Hết quota miễn phí, đợi reset hoặc đổi project")