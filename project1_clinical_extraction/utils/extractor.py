# utils/extractor.py
from openai import OpenAI
from config import OPENAI_API_KEY
from utils.json_utils import safe_json_extract
import os

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_visit_info(dialogue):
    """
    Sends a patient–doctor conversation to the LLM and extracts structured medical info.
    """
    prompt = f"""
    Extract the following structured data from the conversation.
    Return ONLY valid JSON — no explanations or extra text.

    {{
      "chief_complaint": "string",
      "family_illnesses": ["string"],
      "medications": ["string"],
      "small_talk": true/false,
      "doctor_advice": "string"
    }}

    Conversation:
    {dialogue}
    """

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.2
        )
        return safe_json_extract(response.output_text.strip())
    except Exception as e:
        return {"error": str(e)}
