import os
import sys

# Load .env file using pure standard library
_env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_file):
    with open(_env_file, "r", encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                _k = _k.strip()
                _v = _v.strip().strip("'\"")
                if _k and _v:
                    os.environ[_k] = _v

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

# ==========================================
# 1. Feature Flags & Pipeline Controls
# ==========================================
USE_CACHE = True             # Dual-Level Exact & Semantic Cache (< 5ms response time on repeat queries)
USE_HYBRID = True            # Hybrid Search: BM25 + Dense Semantic Vector (RRF)
USE_RERANK = False           # Cross-Encoder Reranking (optional, high accuracy)
USE_SELECTIVE_RERANK = True  # Selectively rerank only when score margin is close
USE_QUERY_TRANSFORM = False  # Query expansion / multi-query before search
USE_MEMORY = True            # Multi-turn conversation memory
USE_LLM = True               # LLM Answer Generation (False = fast direct retrieval)
SHOW_SOURCES = True          # Show citations and source line numbers
SHOW_DEBUG = True            # Show granular execution timings (ms) and scores

# ==========================================
# 2. File & Directory Paths
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_db")

# Source dataset and evaluation set
SOURCE_FILE = os.path.join(DATA_DIR, "guitar_knowledge_base.txt")
GOLDEN_SET_FILE = os.path.join(DATA_DIR, "guitar_golden_set.json")

# Pipeline artifacts & intermediate outputs
EXTRACTED_TEXT_FILE = os.path.join(OUTPUT_DIR, "extracted_text.json")
CHUNKS_FILE = os.path.join(OUTPUT_DIR, "chunks.json")
EMBEDDINGS_FILE = os.path.join(OUTPUT_DIR, "embeddings.npy")
RETRIEVAL_RESULTS_FILE = os.path.join(OUTPUT_DIR, "retrieval_results.json")
EVAL_RETRIEVAL_FILE = os.path.join(OUTPUT_DIR, "eval_retrieval.json")
EVAL_GENERATION_FILE = os.path.join(OUTPUT_DIR, "eval_generation.json")

# Vector DB & BM25 index files
FAISS_INDEX_FILE = os.path.join(VECTOR_DB_DIR, "guitar_faiss.index")
CHUNK_STORE_FILE = os.path.join(VECTOR_DB_DIR, "guitar_chunk_store.json")
BM25_INDEX_FILE = os.path.join(VECTOR_DB_DIR, "guitar_bm25.pkl")
INDEX_META_FILE = os.path.join(VECTOR_DB_DIR, "guitar_index_meta.json")
CACHE_FILE = os.path.join(VECTOR_DB_DIR, "query_cache.json")

# ==========================================
# 3. Embedding Model & Chunking Settings
# ==========================================
CHUNK_SIZE = 500             # Optimal character size for guitar technical facts and chord charts
CHUNK_OVERLAP = 60           # Overlap to prevent splitting chord tables
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"  # SOTA English retrieval model on MTEB benchmark
EMBEDDING_DIM = 384
NORMALIZE_EMBEDDINGS = True  # L2-normalization for exact Cosine Similarity with IndexFlatIP

# ==========================================
# 4. Search & Retrieval Settings
# ==========================================
TOP_K = 3                    # Number of top chunks passed to LLM
CANDIDATE_K = 15             # Number of initial candidates fetched before fusion / reranking
RRF_K = 60                   # RRF smoothing constant
DENSE_WEIGHT = 0.55          # Weight for Dense Semantic Search
BM25_WEIGHT = 0.45           # Weight for Keyword BM25 Search

# Reranker Settings
RERANK_MODEL_NAME = "BAAI/bge-reranker-v2-m3"
RERANK_THRESHOLD_DIFF = 0.15

# Query Transform Settings
QUERY_TRANSFORM_MODE = "multi_query"  # rewrite | multi_query | hyde
MULTI_QUERY_COUNT = 3

# ==========================================
# 5. LLM Provider Configuration
# ==========================================
LLM_PROVIDER = "gemini"      # "gemini" | "openai" | "ollama"
LLM_MODEL = "models/gemini-3.1-flash-lite-preview"  # Default Gemini model
LLM_TEMPERATURE = 0.2
LLM_MAX_TOKENS = 700

LLM_PROVIDERS = {
    "gemini": (
        "https://generativelanguage.googleapis.com/v1beta/openai/",
        "models/gemini-3.1-flash-lite-preview",
        "GEMINI_API_KEY",
    ),
    "openai": (
        "https://api.openai.com/v1",
        "gpt-4o-mini",
        "OPENAI_API_KEY",
    ),
    "ollama": (
        "http://localhost:11434/v1",
        "llama3.1:8b",
        None,
    ),
}

# ==========================================
# 6. Response & Memory Settings
# ==========================================
MEMORY_MAX_TURNS = 6
NO_CONTEXT_MESSAGE = "Sorry, no relevant information was found in the guitar knowledge base for this question."
DISCLAIMER = "🎸 Source: English Guitar Knowledge Base (LAB04: RAG-Guitar System)"

# Evaluation
EVAL_K_VALUES = [1, 3, 5, 10]
GOLDEN_SET_SIZE = 50

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)
