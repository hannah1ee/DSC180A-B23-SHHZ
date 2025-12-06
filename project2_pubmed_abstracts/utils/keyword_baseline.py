import re, requests, pandas as pd
from pydantic import BaseModel

class Finding(BaseModel):
    term: str
    sentence: str

def run_keyword_baseline():
    query = "Type 2 Diabetes AND gut microbiome AND (treatment OR metabolites)"
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    r = requests.get(f"{base}esearch.fcgi?db=pubmed&term={query}&retmax=50&retmode=json")
    ids = r.json()["esearchresult"]["idlist"]

    fetch = requests.get(f"{base}efetch.fcgi?db=pubmed&id={','.join(ids)}&rettype=abstract&retmode=text").text
    abstract_blocks = [a.strip() for a in re.split(r"PMID-\\s*\\d+", fetch) if a.strip()]
    min_len = min(len(ids), len(abstract_blocks))
    df = pd.DataFrame([{"pmid": ids[i], "abstract": abstract_blocks[i]} for i in range(min_len)])

    keywords = [
        "metformin","probiotic","butyrate","berberine",
        "resveratrol","curcumin","microbiota","insulin",
        "inflammation","short-chain fatty","therapy","compound"
    ]

    hits = []
    for abs_ in df["abstract"]:
        for sent in re.split(r'(?<=[.!?]) +', abs_):
            for k in keywords:
                if re.search(rf"\\b{k}\\w*\\b", sent, re.I):
                    hits.append(Finding(term=k.capitalize(), sentence=sent.strip()))

    if hits:
        out = pd.DataFrame([h.dict() for h in hits]).drop_duplicates()
        out.to_csv("output/t2d_microbiome_findings.csv", index=False)
        return out
    else:
        return pd.DataFrame()
