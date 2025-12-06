import asyncio, re, pandas as pd
from semlib import Session
from semlib.cache import OnDiskCache
from .config import MODEL_NAME, SAMPLE_N

template = (
    "You are a biomedical literature analysis assistant.\n"
    "Below is an abstract from a PubMed paper related to **Type 2 Diabetes Mellitus (T2DM)**.\n\n"
    "{abstract}\n\n"
    "Your task is to identify **drugs, compounds, or therapeutic agents** mentioned as being "
    "repurposed, tested, or proposed as treatments for Type 2 Diabetes. For each, briefly summarize:\n"
    "- its proposed mechanism or biological rationale\n"
    "- the context (e.g., anti-inflammatory, insulin sensitization, β-cell protection)\n\n"
    "Format your response as plain text bullet points, for example:\n"
    "- DrugName: short description of mechanism or rationale"
)

async def run_sem_extraction(df):
    session = Session(model=MODEL_NAME, cache=OnDiskCache("t2d_cache.db"))
    sample_abstracts = df["abstract"].head(SAMPLE_N).tolist()
    results = []

    for i, abs_ in enumerate(sample_abstracts, 1):
        try:
            result = await session.prompt(template.format(abstract=abs_))
            results.append({"index": i, "output": str(result)})
        except Exception as e:
            results.append({"index": i, "output": f"Error: {e}"})

    return pd.DataFrame(results)