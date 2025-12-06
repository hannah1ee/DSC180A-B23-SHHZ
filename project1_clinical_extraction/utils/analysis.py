# utils/analysis.py
from collections import Counter

def get_top_medications(structured_data, top_n=5):
    all_meds = [
        m.lower().strip()  # Normalize to lowercase and trim whitespace
        for entry in structured_data
        for m in entry.get("medications", [])
        if isinstance(m, str)
    ]
    return Counter(all_meds).most_common(top_n)

def print_top_medications(top_meds):
    print("\nTop Medications Mentioned:")
    for med, count in top_meds:
        print(f" - {med}: {count}")
