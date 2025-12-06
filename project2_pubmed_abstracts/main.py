import asyncio, pandas as pd
from utils.pubmed_fetcher import fetch_pubmed_abstracts
from utils.semantic_extractor import run_sem_extraction
from utils.postprocess import filter_and_categorize
from utils.keyword_baseline import run_keyword_baseline

async def run_pipeline():
    print("\n[1] Fetching PubMed abstracts...")
    df = fetch_pubmed_abstracts()
    print(f"Retrieved {len(df)} abstracts.")

    print("\n[2] Running SemLib extraction...")
    sem_df = await run_sem_extraction(df)

    print("\n[3] Filtering & categorizing drug candidates...")
    df_drugs = filter_and_categorize(sem_df)
    df_drugs.to_csv("output/t2d_semantic_results.csv", index=False)

    for cat in df_drugs["category"].unique():
        subset = df_drugs[df_drugs["category"] == cat]["raw_term"].tolist()
        print(f"\n{cat} ({len(subset)}):")
        print(", ".join(subset))

    print("\n[4] Running microbiome keyword baseline...")
    kw_df = run_keyword_baseline()
    print(f"Keyword extraction complete ({len(kw_df)} results).")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
