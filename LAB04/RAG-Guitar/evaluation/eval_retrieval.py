"""
eval_retrieval.py - Benchmarks and compares retrieval methods (Dense FAISS, BM25, Hybrid Weighted RRF) on English Guitar dataset.
Saves metrics to outputs/eval_retrieval.json
"""

import json
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from evaluation.metrics import hit_at_k, ndcg_at_k, reciprocal_rank
from src.hybrid_retriever import HybridRetriever


def evaluate_method(retriever, golden_set, method_name, k_values=[1, 3, 5, 10]):
    total = len(golden_set)
    hits = {k: 0 for k in k_values}
    mrrs = []
    ndcgs = {3: [], 5: []}
    latencies = []

    orig_hybrid = config.USE_HYBRID
    orig_rerank = config.USE_RERANK

    if method_name == "Dense (FAISS Cosine Similarity)":
        config.USE_HYBRID = False
        config.USE_RERANK = False
    elif method_name == "BM25 (Keyword Okapi)":
        config.USE_HYBRID = True
        config.USE_RERANK = False
    elif method_name == "Hybrid (Dense + BM25 Weighted RRF)":
        config.USE_HYBRID = True
        config.USE_RERANK = False

    for item in golden_set:
        query = item["query"]
        relevant_ids = item["relevant_chunk_ids"]

        t0 = time.time()
        if method_name == "BM25 (Keyword Okapi)":
            b_res = retriever.search_bm25(query, top_k=max(k_values))
            retrieved_chunks = [{"chunk_id": cid} for cid, _ in b_res]
        else:
            retrieved_chunks = retriever.retrieve(query, top_k=max(k_values))
        elapsed_ms = (time.time() - t0) * 1000
        latencies.append(elapsed_ms)

        retrieved_ids = [c["chunk_id"] for c in retrieved_chunks]

        for k in k_values:
            hits[k] += hit_at_k(retrieved_ids, relevant_ids, k=k)

        mrrs.append(reciprocal_rank(retrieved_ids, relevant_ids))
        ndcgs[3].append(ndcg_at_k(retrieved_ids, relevant_ids, k=3))
        ndcgs[5].append(ndcg_at_k(retrieved_ids, relevant_ids, k=5))

    config.USE_HYBRID = orig_hybrid
    config.USE_RERANK = orig_rerank

    return {
        "method": method_name,
        "sample_size": total,
        "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
        "hit_at_1": round(hits[1] / total, 4),
        "hit_at_3": round(hits[3] / total, 4),
        "hit_at_5": round(hits[5] / total, 4),
        "hit_at_10": round(hits[10] / total, 4),
        "mrr": round(sum(mrrs) / total, 4),
        "ndcg_at_3": round(sum(ndcgs[3]) / total, 4),
        "ndcg_at_5": round(sum(ndcgs[5]) / total, 4),
    }


def main():
    print("=" * 75)
    print("📊 Retrieval Evaluation & Latency Benchmark (BAAI/bge-small-en-v1.5)")
    print("=" * 75)

    if not os.path.exists(config.GOLDEN_SET_FILE):
        from evaluation.build_golden_set import main as build_gs
        build_gs()

    with open(config.GOLDEN_SET_FILE, "r", encoding="utf-8") as f:
        golden_set = json.load(f)

    print(f"Loaded {len(golden_set)} evaluation test queries.\n")

    retriever = HybridRetriever()

    methods = [
        "Dense (FAISS Cosine Similarity)",
        "BM25 (Keyword Okapi)",
        "Hybrid (Dense + BM25 Weighted RRF)",
    ]

    all_results = []
    for m in methods:
        print(f"Evaluating: {m}...")
        res = evaluate_method(retriever, golden_set, m)
        all_results.append(res)
        print(f"  -> Hit@1: {res['hit_at_1']*100:.1f}% | Hit@3: {res['hit_at_3']*100:.1f}% | MRR: {res['mrr']:.3f} | Latency: {res['avg_latency_ms']} ms\n")

    with open(config.EVAL_RETRIEVAL_FILE, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print("=" * 75)
    print(f"✅ Evaluation results saved to {config.EVAL_RETRIEVAL_FILE}")
    print("=" * 75)


if __name__ == "__main__":
    main()
