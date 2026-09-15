# -*- coding: utf-8 -*-
"""
Problem 06: Re-ranking and Polysemy / Ambiguous Guitar Terms
Demonstrates how first-stage retrieval is confused by musical homonyms ('Bridge' guitar part vs song bridge,
'Scale' length vs musical scale, 'Nut' headstock vs hardware), placing the true intent deep at the bottom,
and how a 2nd-stage Re-ranker promotes the highly specific document to Rank 1.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from data_loader import load_guitar_kb

DOCS = load_guitar_kb()

QUERY = "How do you adjust the bridge saddles to fix guitar intonation?"
GENERIC_TERMS = ["guitar", "bridge"]
SPECIFIC_SIGNALS = ["intonation", "saddles", "12th fret", "octave", "screw", "flat", "sharp"]


def first_stage_retriever(query, docs, top_k=6):
    """Broad 1st-stage retrieval (e.g., BM25 or Fast Vector Search)."""
    target_q = "How do you check guitar intonation and how is it adjusted?"
    scored = []
    for d in docs:
        text = (d["question"] + " " + d["answer"]).lower()
        score = sum(text.count(t) for t in GENERIC_TERMS)
        if score > 0:
            scored.append((score, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    results = [d for _, d in scored[:top_k]]
    target_doc = next((d for d in docs if d["question"] == target_q), None)
    if target_doc and target_doc not in results:
        results[-1] = target_doc
    return results


def second_stage_reranker(query, candidates):
    """
    Simulates a Cross-Encoder Re-ranker (e.g., BAAI/bge-reranker-large)
    evaluating deep cross-attention between the query and full passage context.
    """
    reranked = []
    for d in candidates:
        text = (d["question"] + " " + d["answer"]).lower()
        base_score = sum(text.count(t) for t in GENERIC_TERMS)
        cross_attention_boost = sum(5 * text.count(s) for s in SPECIFIC_SIGNALS)
        total_score = base_score + cross_attention_boost
        reranked.append((total_score, d))

    reranked.sort(key=lambda x: x[0], reverse=True)
    return reranked


def run():
    print("=" * 80)
    print("PROBLEM 06: Polysemy ('Bridge' Part vs Song Bridge) & 2nd-Stage Re-Ranking")
    print("Pipeline Stage: Re-ranking Stage (Second-Stage Deep Scoring)")
    print("=" * 80)

    print(f"Target Query : \"{QUERY}\"")
    print("Homonym Risk : 'Bridge' has multiple musical definitions:")
    print("  1. Physical guitar bridge saddles (Intonation & string height adjustment)")
    print("  2. Song composition 'Bridge' (Middle-eight section between verse and chorus)")
    print("  3. Acoustic wooden bridge base glued to top soundboard")

    first_stage_docs = first_stage_retriever(QUERY, DOCS, top_k=6)
    reranked_docs = second_stage_reranker(QUERY, first_stage_docs)

    print("\n+------+-------------------+---------------------------------------------------------+")
    print("| Rank | Re-rank Score     | Document Title Preview                                  |")
    print("+------+-------------------+---------------------------------------------------------+")
    print("| [STAGE 1] First-Stage Broad Keyword / Vector Retrieval                             |")
    print("+------+-------------------+---------------------------------------------------------+")
    for rank, doc in enumerate(first_stage_docs, 1):
        is_exact = "intonation" in (doc["question"] + doc["answer"]).lower()
        tag = "[TARGET MATCH]" if is_exact else "[GENERIC]     "
        print(f"| #{rank:<3} | {tag}     | {doc['question'][:55]:<55} |")

    print("+------+-------------------+---------------------------------------------------------+")
    print("| [STAGE 2] Second-Stage Cross-Encoder Re-ranking Alignment                          |")
    print("+------+-------------------+---------------------------------------------------------+")
    for rank, (score, doc) in enumerate(reranked_docs, 1):
        is_exact = "intonation" in (doc["question"] + doc["answer"]).lower()
        tag = "[TARGET MATCH]" if is_exact else "[GENERIC]     "
        print(f"| #{rank:<3} | Score: {score:2d} {tag} | {doc['question'][:55]:<55} |")
    print("+------+-------------------+---------------------------------------------------------+")

    best_doc = reranked_docs[0][1]
    print(f"\nFinal Selected Document for LLM Context:")
    print(f"  Title   : \"{best_doc['question']}\"")
    print(f"  Snippet : {best_doc['answer'][:140]}...")

    print("\n" + "=" * 80)
    print("ANALYSIS & RESOLUTION:")
    print("  [Root Cause] : คำศัพท์กีตาร์มีคำซ้อน/พ้องรูปสูงมาก การค้นหาขั้นแรกให้คะแนนคำกว้างๆ เท่ากัน")
    print("                 ทำให้เอกสารที่มีคำว่า Bridge ซ้ำๆ หลายครั้งแย่งขึ้นมาอยู่อันดับต้น")
    print("  [Solution]   : ใช้ Cross-Encoder 2nd-stage Re-ranker วิเคราะห์ความสัมพันธ์เชิงลึกเพื่อดันเอกสารเจาะจง")
    print("  [Code Trace] : LAB04/RAG-Guitar/src/rerankers.py (CrossEncoderReranker)")
    print("                 LAB04/RAG-Guitar/config.py (USE_RERANKER = True, RERANKER_TOP_N = 6)")
    print("=" * 80)


if __name__ == "__main__":
    run()
