"""
metrics.py - ฟังก์ชันคำนวณ Metric การประเมินผลการค้นหา (Hit@k, MRR, nDCG, Precision@k, Recall@k)
"""

import math


def hit_at_k(retrieved_ids, relevant_ids, k=3):
    """
    Hit@k = 1 หากมี Relevant Document อย่างน้อย 1 รายการอยู่ใน Top-k
    """
    top_k_items = retrieved_ids[:k]
    for doc_id in relevant_ids:
        if doc_id in top_k_items:
            return 1.0
    return 0.0


def precision_at_k(retrieved_ids, relevant_ids, k=3):
    """
    Precision@k = (จำนวน Relevant Documents ใน Top-k) / k
    """
    if k == 0:
        return 0.0
    top_k_items = retrieved_ids[:k]
    hits = sum(1 for doc_id in top_k_items if doc_id in relevant_ids)
    return hits / k


def recall_at_k(retrieved_ids, relevant_ids, k=3):
    """
    Recall@k = (จำนวน Relevant Documents ใน Top-k) / (จำนวน Relevant Documents ทั้งหมด)
    """
    if not relevant_ids:
        return 0.0
    top_k_items = retrieved_ids[:k]
    hits = sum(1 for doc_id in top_k_items if doc_id in relevant_ids)
    return hits / len(relevant_ids)


def reciprocal_rank(retrieved_ids, relevant_ids):
    """
    MRR (Reciprocal Rank) = 1 / (อันดับแรกที่พบ Relevant Document)
    """
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved_ids, relevant_ids, k=3):
    """
    nDCG@k = DCG@k / IDCG@k
    """
    dcg = 0.0
    for rank, doc_id in enumerate(retrieved_ids[:k], start=1):
        rel = 1.0 if doc_id in relevant_ids else 0.0
        dcg += rel / math.log2(rank + 1)

    idcg = sum(1.0 / math.log2(r + 1) for r in range(1, min(len(relevant_ids), k) + 1))
    return (dcg / idcg) if idcg > 0 else 0.0
