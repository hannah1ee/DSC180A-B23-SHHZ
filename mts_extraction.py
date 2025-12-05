# ---- Import Libraries ----
from openai import OpenAI
import os, json, re, time
from tqdm import tqdm
from collections import Counter
import pandas as pd

# ---- MTS Dataset ----
url = "https://raw.githubusercontent.com/abachaa/MTS-Dialog/refs/heads/main/Main-Dataset/MTS-Dialog-TrainingSet.csv"
df = pd.read_csv(url)

# ---- API Key ----
os.environ["OPENAI_API_KEY"] = ""

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- Extraction Process ----
def safe_json_extract(text):
    """
    Safely extracts JSON from an LLM response.

    Args:
        text (str): Raw model output that may contain JSON.
    Returns:
        dict: Parsed JSON object or a fallback dictionary including an error message.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # If parsing fails, try to extract the first {...} JSON-like block
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        # If all parsing fails, return raw text and flag error
        return {"raw_response": text, "error": "JSON parse failed"}

def extract_visit_info(dialogue):
    """
    Sends a patient–doctor conversation to the LLM and extracts
    structured medical information in JSON.

    Args:
        dialogue (str): The full text of a patient–doctor conversation.
    Returns:
        dict: Structured data including complaint, medications, etc.
    """

    # Define the schema
    prompt = f"""
    Extract the following structured data from the conversation.
    Return **only** valid JSON — no explanations or extra text.

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
        # Calls the OpenAI model
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.2 # low randomness → consistent outputs
        )

        text = response.output_text.strip()

        # Safely parse the JSON
        return safe_json_extract(text)

    except Exception as e:
        # Return the error message if the call fails
        return {"error": str(e)}

# ---- Main Processing Loop ----
structured_data = []

# Iterate through the first 50~ patient–doctor dialogues
N = 50                                   # Adjust N based on token usage or API credits
for d in tqdm(df["dialogue"].head(N)):
    info = extract_visit_info(d)         # Extract structured info for one dialogue
    structured_data.append(info)         
    time.sleep(0.3)                      

# ---- Post-processing: medication frequency analysis ----

# Flatten all medication lists from the structured data
all_meds = [
    m for d in structured_data 
    for m in d.get("medications", []) 
    if isinstance(m, str)
]

# Find the top 5 most frequently mentioned medications
top5 = Counter(all_meds).most_common(5)
