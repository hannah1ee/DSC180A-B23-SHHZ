# MTS - Dialog  & Pubmed Literature Pipeline

This repository contains three scripts designed to extract and analyze biomedical information from PubMed literature for identifying drug repurposing candidates for Parkinson's Disease, and uses semlib as well to analyze biomedical information.

---

## Files Overview

| File | Description |
|------|-------------|
| `pubmed_scraper.py` | Retrieves PubMed abstracts related to Parkinson's Disease and drug repurposing using Biopython's Entrez API. |
| `LLM_semantic_extraction.py` | Extracts structured information (drug candidates, mechanisms, repurposing potential) from abstracts using OpenAI LLMs. |
| `keyword_rule_based_analysis.py` | Applies classical NLP techniques to extract drug classes and mechanistic terms from the literature. |

---

## Dependencies

You will need Python 3.9+ and the following packages:
```bash
pip install -r requirements.txt
```
Or install manually:
```bash
pip install pandas==2.2.2 biopython openai python-dotenv
```

---

## Environment Variables

The LLM extraction script uses OpenAI models, so you must set your API key:
```bash
export OPENAI_API_KEY="your-api-key"
```
The default model is set to `gpt-4`. You can adjust this in the configuration section of `LLM_semantic_extraction.py`.

---

## Data Access
### PubMed Literature Scraping

The script retrieves abstracts via the NCBI Entrez API. Set your email in the script (for Entrez compliance):
```python
Entrez.email = "youremail@domain.com"
```

Query parameters:

| Parameter | Value |
|-----------|-------|
| Disease | Parkinson's Disease |
| Topic | Drug repurposing |
| Years | 2020–2025 |
| Language | English |

No manual download is required — data is fetched automatically.

---

## How to Run
### 1. PubMed Scraper

This script retrieves PubMed abstracts matching the search criteria.
```bash
python pubmed_scraper.py
```

**Output files:**
- `parkinsons_drug_repurposing.csv` – raw PubMed abstracts

---

### 2. LLM Semantic Extraction

This script sends each abstract to an OpenAI model and extracts structured information.
```bash
python LLM_semantic_extraction.py
```

**Output:**
- Console summaries of top drugs and mechanisms
- Aggregated structured results with repurposing potential ratings (high/medium/low)

---

### 3. Keyword & Mechanism Analysis

This script applies rule-based NLP to extract drug classes and mechanistic terms.
```bash
python keyword_rule_based_analysis.py
```

**Output files:**
- `analysis_summary.txt` – keyword and mechanism frequency analysis

**Mechanistic terms tracked:**
- Oxidative stress
- Inflammation
- Apoptosis
- Mitochondrial function

---

## Reproducibility Summary
To reproduce the full pipeline:

1. **Clone this repository**
```bash
git clone https://github.com/yourusername/DSC-180A-B23-SHHZ.git
cd DSC-180A-B23-SHHZ
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Export your API key**
```bash
export OPENAI_API_KEY="your-api-key"
```

4. **Run each script sequentially**
```bash
python pubmed_scraper.py
python LLM_semantic_extraction.py
python keyword_rule_based_analysis.py
```

5. **Verify the generated output files**

| File | Description |
|------|-------------|
| `parkinsons_drug_repurposing.csv` | Raw PubMed abstracts |
| `analysis_summary.txt` | Final keyword/mechanism analysis report |

## Docker Environment

To use the pre-built Docker image:
```bash
docker pull ghcr.io/stephanieyyue/dsc-180a-syyue
```

On DSMLP:
```bash
launch.sh -i ghcr.io/stephanieyyue/dsc-180a-syyue -W DSC180A_FA25_A00
```
