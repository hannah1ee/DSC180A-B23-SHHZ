# Project 2 – Literature Mining for Drug Repurposing

This project replicates a biomedical text-mining workflow designed to identify **potential drug repurposing candidates** from **PubMed abstracts** using the OpenAI API and semantic analysis techniques.  
It demonstrates how **large language models (LLMs)** like `gpt-4.1-mini` can automate the process of finding relationships between drugs and diseases, accelerating early-stage drug discovery.

---

## Overview

Thia system reads PubMed abstracts, prompts an LLM to extract structured data, and then aggregates the results from hundreds of papers.  
Each processed abstract produces a JSON entry with the following fields:

| **Field Name**           | **Description**                                                                                      |
|---------------------------|------------------------------------------------------------------------------------------------------|
| `disease`                | The primary disease or condition discussed in the abstract.                                          |
| `drugs_mentioned`        | A list of all drugs referenced within the study.                                                    |
| `repurposing_candidates` | Drugs identified or proposed as potential candidates for repurposing.                                |
| `mechanism_of_action`    | A brief description of each drug’s biological mechanism, if available in the text.                   |
| `summary`                | A concise, one-sentence overview summarizing the study’s findings and context.                      |

---

## Installation and Setup

### Clone this project

```bash
git clone https://github.com/HailyV/Neuro-Symbolic-Methods
cd Neuro-Symbolic-Methods/project2_literature_mining

conda create -n literature_mining python=3.10
conda activate literature_mining
pip install -r requirements.txt

export OPENAI_API_KEY="your_api_key"

python drug_repurposing.py
