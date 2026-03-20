import os
import json
import logging
from google import genai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Client otomatis membaca GEMINI_API_KEY dari env
client = genai.Client()

def classify_lead_with_ai(full_name: str, message: str) -> dict:
    if not message:
        return {"category": "Cold", "score": 0, "reason": "No message provided"}

    prompt = f"""
    Analisis Lead:
    Nama: {full_name}
    Pesan: {message}
    Tugas: Tentukan kategori (Hot, Warm, Cold), skor (0-100), dan alasan singkat.
    Output: Harus JSON murni.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        logger.error(f"AI Error: {e}")
        return {
            "category": "Warm",
            "score": 50,
            "reason": "AI Temporary Unavailable"
        }