# core/groq_config.py - Doc GROQ_API_KEY tu .env, dung chung cho cac file llama_chat*.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "Chua co GROQ_API_KEY trong file .env. "
        "Copy .env.example thanh .env va dien key that vao (console.groq.com)."
    )


def get_groq_client() -> Groq:
    """Tra ve 1 Groq client da duoc cau hinh key tu .env."""
    return Groq(api_key=GROQ_API_KEY)
