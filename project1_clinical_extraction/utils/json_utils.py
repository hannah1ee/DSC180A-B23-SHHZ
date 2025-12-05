# utils/json_utils.py
import json, re

def safe_json_extract(text):
    """
    Safely parses LLM output as JSON, with error fallback.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        return {"raw_response": text, "error": "JSON parse failed"}
