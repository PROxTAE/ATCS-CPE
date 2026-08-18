"""
LAB 06: Semantic similarity search using FAISS (Cosine Similarity on Normalized BGE Embeddings).
Saves results to outputs/retrieval_results.json

Run: python labs/lab06_similarity_search.py
"""

import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.embedding_model import EmbeddingModel
from src.vector_store import VectorStore, load_chunk_store


def main():
    print("=== Lab 06: Semantic Similarity Search (FAISS Dense Search) ===")
    test_query = "How do you adjust the truss rod to fix fret buzz?"
    print(f"Query: {test_query}\n")

    chunks = load_chunk_store(config.CHUNK_STORE_FILE)
    store = VectorStore()
    store.load(config.FAISS_INDEX_FILE)

    embedding_model = EmbeddingModel()
    q_vec = embedding_model.encode_query(test_query)

    scores, indices = store.search(q_vec, top_k=3)

    results = []
    print("Top 3 Semantic Retrieval Results:")
    for rank, (score, idx) in enumerate(zip(scores, indices), start=1):
        chunk = chunks[idx]
        print(f"  [{rank}] Cosine Similarity: {score:.4f} | Category: {chunk['category']}")
        print(f"      Q: {chunk['question']}")
        print(f"      A: {chunk['answer'][:120]}...\n")
        results.append({
            "rank": rank,
            "score": float(score),
            "chunk_id": chunk["chunk_id"],
            "question": chunk["question"],
            "answer": chunk["answer"],
        })

    with open(config.RETRIEVAL_RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
