# DSC180A-B23-SHHZ

Authors: Stephanie, Hannah, Haily, Zoey

This repository contains three major components for the DSC 180A B23 Capstone:

1. **Semantic Extraction of Patient–Doctor Interactions**  

2. **Drug Repurposing Literature Mining Across Four Diseases**  

3. **Ontology-Grounded Neuro-Symbolic Framework for Analyzing Pralsetinib Off-Target Effects**

---

## 1. Data Access

### A) PubMed Abstracts (Current Component)
Retrieved automatically via **NCBI E-utilities API** (Biopython)
Queries are constructed for the four diseases:
- Type II Diabetes
- Parkinson’s Disease
- Lung Cancer
- Alzheimer’s Disease

Query example:
```
("Alzheimer Disease"[MeSH Major Topic] OR Alzheimer*[Title/Abstract])  
AND ("Drug Repositioning"[MeSH Terms] OR repurpos* OR reposition* OR "drug rediscovery")  
AND hasabstract[text]  
AND english[Language]  
AND (1980:3000[pdat])  
```

Output stored as:  
`data/abstracts.csv`


### B) MTS-Dialog Dataset
Source:  
https://raw.githubusercontent.com/abachaa/MTS-Dialog/main/Main-Dataset/MTS-Dialog-TrainingSet.csv

Loaded directly via `pandas.read_csv`.

---

## 2. Software Requirements

### Python Version
Python 3.12

### Recommended Environment Setup
```bash
conda create -n dsc180 python=3.12 -y
conda activate dsc180

#Install Dependencies  
pip install pandas==2.2.2 \
    biopython>=1.81 \
    openai>=1.0.0 \
    python-dotenv>=1.0.0 \
    beautifulsoup4>=4.12.0 \
    matplotlib>=3.7.0 \
    numpy>=1.24.0 \
    requests>=2.31.0

pip install scispacy spacy tqdm

#Required Environment Variables  

export NCBI_EMAIL="your_email@ucsd.edu"
export OPENAI_API_KEY="your_api_key_here"
```
## 3. Running the Code

#### Step 1 — Fetch PubMed Abstracts
```python fetch_pubmed.py --query-file query_examples.txt --retmax 500 --out data/abstracts.csv```
#### Step 2 — Extract Drug Candidates (Cost-Controlled)
```
python openai_extract_candidates.py \
  --input data/abstracts.csv \
  --output data/openai_candidates_raw.csv \
  --limit 500 \
  --max-cost 2.00 \
  --model gpt-4o-mini \
  --verbose
```
#### Step 3 — Flatten & Summarize Results
```
python flatten_openai_json.py \
  --in data/openai_candidates_raw.csv \
  --out data/openai_candidates_table.csv \
  --summary data/candidate_summary.csv
```

## 4. Docker Usage
This repository includes a Dockerfile for containerized execution.  

**Build the Docker Image**  
`docer build -t dsc180a-b23 .`  

**Run the Container**  
The Dockerfile defaults to executing `main.py`:  
`docker run --rm dsc180a-b23`  

To mount local data:  
`docker run --rm -v $(pwd)/data:/app/data dsc180a-b23`  


## 5. Output Files
| File                                                                                         | Description                                        |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `data/abstracts.csv`                                                                         | PubMed PMIDs, titles, and abstracts                |
| `openai_candidates_raw.csv`                                                                  | One extracted JSON result per abstract             |
| `openai_candidates_table.csv`                                                                | Tidy table with drug, mechanism, stance, evidence  |
| `candidate_summary.csv`                                                                      | Aggregated candidate hit counts by stance          |
| (MTS-Dialog Component) `visit_summaries.csv`, `analysis_summary.csv`, `top5_medications.csv` | Structured dialogue summaries and analysis results |


## 6. Future Work

The repository will be expanded to include:
- GO-based functional enrichment modules
- HPO-based phenotype mapping for Pralsetinib
- Neuro-symbolic reasoning pipelines for off-target prediction  
These will integrate with existing extraction outputs.

## Citation
National Center for Biotechnology Information (NCBI). PubMed database.  
Abacha, A. B., & Demner-Fushman, D. (2023). MTS-Dialog: A Dataset for Medical Therapeutic Strategy Understanding.  
