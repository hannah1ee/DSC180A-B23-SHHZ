# main.py
import os, time, json
import pandas as pd
from tqdm import tqdm
from config import OPENAI_API_KEY

from utils.extractor import extract_visit_info
from utils.analysis import get_top_medications, print_top_medications

# --- Set API key ---
os.environ["OPENAI_API_KEY"] = api_key=OPENAI_API_KEY

# --- Load dataset ---
url = "https://raw.githubusercontent.com/abachaa/MTS-Dialog/refs/heads/main/Main-Dataset/MTS-Dialog-TrainingSet.csv"
df = pd.read_csv(url)
print(f"Loaded {len(df)} conversations.")

# --- Process dialogues ---
structured_data = []
N = 250  # limit for testing

print(f"Extracting info from {N} dialogues...")
for dialogue in tqdm(df["dialogue"].head(N)):
    info = extract_visit_info(dialogue)
    structured_data.append(info)
    time.sleep(0.3)

# --- Save results ---
output_path = "outputs/structured_data.json"
with open(output_path, "w") as f:
    json.dump(structured_data, f, indent=2)

print(f"\nStructured data saved to: {output_path}")

# --- Run analysis ---
top_meds = get_top_medications(structured_data)
print_top_medications(top_meds)
