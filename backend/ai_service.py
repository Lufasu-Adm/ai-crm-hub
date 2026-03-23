import json
import logging
from typing import Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

client = genai.Client()

def classify_lead_with_ai(full_name: str, message: str) -> Dict[str, Any]:
    """
    Classifies a sales lead based on the message content using LLM.
    Returns a dictionary with 'category', 'score', and 'reason'.
    """
    if not message or not message.strip():
        logger.warning(f"Empty message received for lead: {full_name}")
        return {"category": "Cold", "score": 0, "reason": "Empty message provided."}

    prompt = f"""
    Analyze the following sales lead and classify their intent.

    Lead Name: {full_name}
    Message: "{message.strip()}"

    Classification Rules:
    - HOT (80-100): High urgency, mentions large volume/enterprise, requests invoice/pricing immediately.
    - WARM (40-79): Inquires about features, requests demo/brochure, general interest without strict timeline.
    - COLD (0-39): Generic greeting, spam, irrelevant, or unclear intent.

    Output strictly in JSON format with the following keys:
    - "category": string ("Hot", "Warm", or "Cold")
    - "score": integer (0 to 100)
    - "reason": string (A concise 1-sentence explanation)
    """

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1
            )
        )
        
        result = json.loads(response.text)
        
        # Defensive programming: ensure keys exist to prevent KeyError in main.py
        return {
            "category": result.get("category", "Warm"),
            "score": result.get("score", 50),
            "reason": result.get("reason", "Analyzed successfully.")
        }

    except json.JSONDecodeError as e:
        logger.error(f"JSON Parsing Error for lead {full_name}: {e} | Raw Response: {response.text}")
        return {"category": "Warm", "score": 50, "reason": "AI response validation failed."}
        
    except Exception as e:
        logger.error(f"Gemini API Error for lead {full_name}: {e}", exc_info=True)
        return {"category": "Warm", "score": 50, "reason": "Service temporarily unavailable."}