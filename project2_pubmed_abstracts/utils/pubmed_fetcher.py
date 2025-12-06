import pandas as pd
from Bio import Entrez
from config import MAX_CHARS, EMAIL

def fetch_pubmed_abstracts():
    Entrez.email = EMAIL
    query = (
        '("type 2 diabetes mellitus" OR "T2DM") '
        'AND ("drug repurposing" OR "drug repositioning" OR "therapeutic candidate" '
        'OR "antidiabetic mechanism" OR "AI drug discovery" OR "metabolic pathway")'
    )

    handle = Entrez.esearch(db="pubmed", term=query, retmax=100)
    record = Entrez.read(handle)
    ids = record["IdList"]

    handle = Entrez.efetch(db="pubmed", id=",".join(ids), rettype="abstract", retmode="xml")
    records = Entrez.read(handle)

    articles = []
    for article in records["PubmedArticle"]:
        try:
            pmid = article["MedlineCitation"]["PMID"]
            title = article["MedlineCitation"]["Article"]["ArticleTitle"]
            abstract = article["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]
            if isinstance(abstract, list):
                abstract = " ".join(abstract)
            articles.append({
                "pmid": pmid,
                "title": title,
                "abstract": abstract.strip()[:MAX_CHARS]
            })
        except KeyError:
            continue

    return pd.DataFrame(articles)
