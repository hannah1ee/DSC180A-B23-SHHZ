Parkinson’s Disease Drug Repurposing

This repository implements a three-stage biomedical text-mining pipeline for identifying potential drug-repurposing candidates for Parkinson’s disease using:
PubMed literature scraping
OpenAI LLM-powered semantic extraction
Classical NLP keyword & mechanism analysis

The workflow is inspired by real clinical dialog datasets such as the MTS-Dialog Patient–Doctor dataset.

Project Structure
├── pubmed_scraper.py                # Step 1 — Download PubMed abstracts
├── LLM_semantic_extraction.py       # Step 2 — LLM-based semantic analysis
├── keyword_rule_based_analysis.py   # Step 3 — Keyword/mechanism extraction
├── parkinsons_drug_repurposing.csv  # Output from Step 1
└── README.md

1. Overview of the Pipeline
         ┌────────────────────┐
         │  PubMed Scraper    │
         │ (pubmed_scraper)   │
         └─────────┬──────────┘
                   ▼
     parkinsons_drug_repurposing.csv
                   ▼
    ┌──────────────────────────────┐
    │ Semantic LLM Extraction      │
    │ (LLM_semantic_extraction)    │
    └──────────┬───────────────────┘
               │
               ▼
    ┌──────────────────────────────┐
    │ Keyword / Rule-Based NLP     │
    │ (keyword_rule_based_analysis)│
    └──────────────────────────────┘

2. Installation & Setup
Clone the repository
git clone https://github.com/yourusername/pd-drug-repurposing.git
cd pd-drug-repurposing

Create a Python environment
conda create -n repurpose python=3.12
conda activate repurpose

Install required libraries
pip install pandas biopython openai python-dotenv

3. Step-by-Step Instructions
STEP 1 — Scrape PubMed Abstracts
pubmed_scraper.py
This script retrieves PubMed abstracts matching:
Disease: Parkinson’s Disease
Topic: Drug repurposing
Years: 2020–2025
Language: English
It outputs parkinsons_drug_repurposing.csv.

Run:
python pubmed_scraper.py
Output produced:
parkinsons_drug_repurposing.csv

STEP 2 — LLM Semantic Extraction
LLM_semantic_extraction.py
semantic_analysis_openai
This script:
  Loads the PubMed CSV
  Sends each abstract to an OpenAI model
  Extracts structured information:
    Drug candidates
    Mechanisms
    Clinical application
    Repurposing potential (high/medium/low)

Key finding
Run:
export OPENAI_API_KEY="your_api_key"
python LLM_semantic_extraction.py

Outputs:
Console summaries of top drugs & mechanisms
Aggregated structured results (results_df in memory)

STEP 3 — Keyword & Mechanism Analysis
keyword_rule_based_analysis.py

This script applies classical NLP:
Matches Parkinson's-related drug classes
Extracts candidate drugs from titles
Counts mechanistic terms:
oxidative stress
inflammation
apoptosis
mitochondrial function
--> Saves a summary text report

Run:
python keyword_rule_based_analysis.py
Output file:
analysis_summary.txt
