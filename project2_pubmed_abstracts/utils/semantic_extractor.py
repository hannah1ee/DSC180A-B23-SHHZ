import asyncio, pandas as pd
from tqdm.asyncio import tqdm_asyncio
from semlib import Session
from semlib.cache import OnDiskCache
from config import MODEL_NAME, SAMPLE_N

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


async def process_single_abstract(session, abs_, index):
    """Run SemLib prompt safely for one abstract."""
    try:
        result = await session.prompt(template.format(abstract=abs_))
        return {"index": index, "output": str(result)}
    except Exception as e:
        return {"index": index, "output": f"Error: {e}"}


async def run_sem_extraction(df):
    """Run SemLib extraction with async progress bar."""
    session = Session(model=MODEL_NAME, cache=OnDiskCache("t2d_cache.db"))
    sample_abstracts = df["abstract"].head(SAMPLE_N).tolist()

    print(f"\nRunning SemLib extraction on {len(sample_abstracts)} abstracts...\n")

    # Create async tasks
    tasks = [
        process_single_abstract(session, abs_, i)
        for i, abs_ in enumerate(sample_abstracts, 1)
    ]

    # tqdm_asyncio gathers with live progress
    results = await tqdm_asyncio.gather(*tasks, desc="Extracting", total=len(tasks))
    return pd.DataFrame(results)