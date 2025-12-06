import os, nest_asyncio

# ============================================
# ENVIRONMENT & SEMLIB CONFIG
# ============================================
nest_asyncio.apply()

os.environ["OPENAI_API_KEY"] = "my-key"
os.environ["SEMLIB_DEFAULT_MODEL"] = "openai/gpt-4.1-mini"
os.environ["SEMLIB_MAX_CONCURRENCY"] = "3"

# Runtime constants
BATCH_SIZE   = 20
PAUSE_SEC    = 5
MAX_RETRIES  = 5
MAX_CHARS    = 8000
SAMPLE_N     = 50
MODEL_NAME   = "openai/gpt-4.1-mini"
EMAIL        = "hal131@ucsd.edu"