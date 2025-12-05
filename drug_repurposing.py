# --- Import Libraries ---
import os, re, json, time
import pandas as pd
from collections import Counter
from tqdm import tqdm
from openai import OpenAI

# ---- API Key ----
os.environ["OPENAI_API_KEY"] = ""
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Load Data ---
df = pd.read_csv("lung_cancer_drug_repurposing.csv")
print(f"Loaded {len(df)} PubMed abstracts.")

# --- Extraction Process ---
def safe_json_extract(text):
    """
    Safely extracts JSON.

    Args:
        text (str): Raw output text from the LLM.
    Returns:
        dict: Parsed JSON if successful, or a dictionary with error info.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # If it fails, attempt to locate the first {...} JSON-like block
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        # If everything fails, return the raw text and an error message
        return {"raw_response": text, "error": "json_parse_failed"}

def extract_repurposing_info(abstract):
    """
    Sends a PubMed abstract to GPT to extract structured biomedical information
    related to drug repurposing.

    Args:
        abstract (str): The text of a PubMed abstract.
    Returns:
        dict: JSON-like structured data containing drugs, diseases, and mechanism info.
    """

    # Define the schema
    prompt = f"""
    You are a biomedical text-mining assistant.
    Read the PubMed abstract below and extract structured data
    about potential drug repurposing candidates.

    Return ONLY valid JSON in this exact structure:

    {{
      "disease": "string",
      "drugs_mentioned": ["string"],
      "repurposing_candidates": ["string"],
      "mechanism_of_action": "string or null",
      "summary": "one-sentence summary of finding"
    }}

    Abstract:
    {abstract}
    """

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.2  # low randomness → consistent outputs
        )

        text = response.output_text.strip()

        return safe_json_extract(text)

    except Exception as e:
        # Capture any exceptions (API errors, rate limits, etc.)
        return {"error": str(e)}

# --- Loops Through Abstracts With Saving Process ---
structured_data = []
save_path = "drug_repurposing_gpt.json"

def save_progress():
    with open(save_path, "w") as f:
        json.dump(structured_data, f, indent=2)

print("Starting LLM-based entity extraction...")

# Loop through PubMed abstracts stored in a DataFrame (df["Abstract"])
for i, abstract in enumerate(tqdm(df["Abstract"])):
    info = extract_repurposing_info(abstract)
    structured_data.append(info)

    # Every 10 abstracts, save progress
    if i % 10 == 0:
        save_progress()

    time.sleep(0.3)

save_progress()
print(f"Finished {len(structured_data)} abstracts. Saved to '{save_path}'.")

with open(save_path) as f:
    structured_data = json.load(f)

# --- Analysis: Top Mentioned Drugs ---
all_drugs = [
    d for entry in structured_data 
    for d in entry.get("drugs_mentioned", []) if isinstance(d, str)
]
top_drugs = Counter(all_drugs).most_common(10)
print("\nTop 10 Drugs Mentioned:")
for drug, count in top_drugs:
    print(f" - {drug}: {count}")

# --- Analysis: Drug Repurposing Candidates ---
candidates = [
    c for entry in structured_data 
    for c in entry.get("repurposing_candidates", []) if isinstance(c, str)
]

# Counts occurrences and list the top 10 most frequent candidate drugs
top_candidates = Counter(candidates).most_common(10)
print("\nTop 10 Repurposing Candidates:")
for drug, count in top_candidates:
    print(f" - {drug}: {count}")
