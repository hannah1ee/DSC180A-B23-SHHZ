# DSC180A-B23-SHHZ

**Authors:** Hannah Lee, Haily Vuong, Stephanie Yue, Hannah Lee, Haily Vuong, Zoey He  
**Mentors:**  Justin Eldridge, Murali Krishnam, Raju Pusapati

This repository contains two major components for the DSC 180A B23 Capstone:

1. **Semantic Extraction of Patient–Doctor Interactions**  
tools for parsing patient–doctor dialogues and producing structured outputs
2. **Drug Repurposing Literature Mining Across Four Diseases**  
automated retrieval and semantic extraction of abstracts related to drug repurposing across four diseases
---

## 1. Data Access

### A) PubMed Abstracts
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

This repository contains **two runnable projects**, each with its `main.py` script.

For both projects, the only required user action is:  
1. Open the `config.py` file inside the project folder
2. Add your API key(s) or configuration values
3. Run:  
`python main.py`

#### Project 1 - Clinical Semantic Extraction
**Directory:** `project1_clinical_extraction/`  

**Purpose:**  
Runs SemLib-style extraction on patient–doctor interactions, producing:  
- structured clinical concept summaries
- medication lists
- symptoms and SDoH extractions
- aggregated clinical analysis tables

Key files:
```
project1_clinical_extraction/
│ main.py # orchestrates extraction + analysis pipeline
│ config.py # user edits API keys + settings here
│ outputs/ # final CSV outputs stored here
└── utils/
analysis.py # computes summary statistics
extractor.py # handles semantic extraction
json_utils.py # formatting + saving utilities
```
**To run Project 1:**  
```
cd project1_clinical_extraction
python main.py
```

Outputs will appear in `project1_clinical_extraction/outputs/`.  

#### Project 2 - PubMed Abstract Extraction & Semantic Analysis
**Directory:** `project2_pubmed_abstracts/`  

**Purpose:**  
- Fetches PubMed abstracts for diseases defined in `config.py`
- Runs keyword baseline
- Runs SemLib/OpenAI semantic extraction
- Postprocesses outputs into final CSV tables

Key files:
```
project2_pubmed_abstracts/
│ main.py # orchestrates full PubMed pipeline
│ config.py # user edits API keys + disease list + output paths
│ output/ # all final CSVs saved here
└── utils/
pubmed_fetcher.py # handles Entrez API fetching
semantic_extractor.py# runs AI-based semantic extraction
keyword_baseline.py # keyword-only comparison
postprocess.py # result cleaning + table generation
```
**To run Project 2:**  
```
cd project2_pubmed_abstracts
python main.py
```

Outputs will appear in `project2_pubmed_abstracts/output/`.

## 4. Docker Usage
This repository includes a Dockerfile for containerized execution.  

**Build the Docker Image**  
`docer build -t dsc180a-b23 .`  

**Run the Container**  
The Dockerfile defaults to executing `main.py`:  
`docker run --rm dsc180a-b23`  

To mount local data:  
`docker run --rm -v $(pwd)/data:/app/data dsc180a-b23`  

## GitHub Container Registry (GHCR) Image
Docker images are automatically built and pushed using GitHub Actions.  

Latest image:  
`ghcr.io/hannah1ee/dsc180a-b23:latest`  
Commit‑specific image:  
`ghcr.io/hannah1ee/dsc180a-b23:<commit-sha>`  
Pull the image:  
`docker pull ghcr.io/hannah1ee/dsc180a-b23:latest`  
Run it:  
`docker run --rm ghcr.io/hannah1ee/dsc180a-b23:latest`  

## 5. Future Work

The repository will be expanded to include:
- GO-based functional enrichment modules
- HPO-based phenotype mapping for Pralsetinib
- Neuro-symbolic reasoning pipelines for off-target prediction  
These will integrate with existing extraction outputs.

## Citation
National Center for Biotechnology Information (NCBI). PubMed database.  
Abacha, A. B., & Demner-Fushman, D. (2023). MTS-Dialog: A Dataset for Medical Therapeutic Strategy Understanding.  
