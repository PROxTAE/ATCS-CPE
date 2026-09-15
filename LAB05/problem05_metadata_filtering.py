# -*- coding: utf-8 -*-
"""
Problem 05: Metadata Filtering in Guitar Knowledge Base
Demonstrates how pure similarity search without metadata filtering retrieves
inappropriate content (e.g. advanced jazz voicings for a beginner, or recommending
steel acoustic strings for a nylon classical guitar which physically damages the instrument).
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from data_loader import load_guitar_kb

DOCS = load_guitar_kb()


def search_kb(query, docs=DOCS, filter_meta=None, top_k=3):
    """
    Search with optional metadata filter dict (e.g. {'difficulty': 'Beginner', 'instrument': 'Classical'}).
    """
    tokens = set(query.lower().split())
    candidates = docs

    if filter_meta:
        for key, val in filter_meta.items():
            candidates = [d for d in candidates if d.get(key) == val]

    scored = []
    for d in candidates:
        text_tokens = set(d["text"].lower().split())
        score = sum(3 if t in d["question"].lower() else 1 for t in tokens if t in text_tokens)
        if score > 0:
            scored.append((score, d))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_k]]


def run():
    print("=" * 80)
    print("PROBLEM 05: Metadata Filtering (Skill Level, Instrument & Tuning Isolation)")
    print("Pipeline Stage: Retrieval Filtering & Search Scoping Stage")
    print("=" * 80)

    scenarios = [
        {
            "id": 1,
            "title": "String Selection for Classical Guitar",
            "query": "What strings should I buy for my guitar sound?",
            "danger": "Recommending high-tension steel strings on a classical guitar will snap or warp the neck!",
            "filter": {"instrument": "Classical"},
        },
        {
            "id": 2,
            "title": "Beginner asking how to play C chord",
            "query": "How to hold and play C chord for beginner first guitar",
            "danger": "Retrieving advanced jazz chord extensions or CAGED fret 8 barre chord frustrates beginners!",
            "filter": {"difficulty": "Beginner"},
        }
    ]

    for sc in scenarios:
        print(f"\n[SCENARIO {sc['id']}/2] {sc['title']}")
        print("-" * 80)
        print(f"User Query   : \"{sc['query']}\"")
        print(f"Domain Risk  : {sc['danger']}")

        # 1. Unfiltered Search
        unfiltered = search_kb(sc["query"], docs=DOCS, filter_meta=None, top_k=2)
        print("\n[RUN A] Pure Similarity Search (Without Metadata Filtering):")
        for i, d in enumerate(unfiltered, 1):
            print(f"  Result #{i}: [Diff: {d['difficulty']:<12} | Inst: {d['instrument']:<9}] Q: \"{d['question'][:55]}...\"")

        # 2. Filtered Search
        filtered = search_kb(sc["query"], docs=DOCS, filter_meta=sc["filter"], top_k=2)
        print(f"\n[RUN B] Scoped Similarity Search (With Metadata Filter: {sc['filter']}):")
        for i, d in enumerate(filtered, 1):
            print(f"  Result #{i}: [Diff: {d['difficulty']:<12} | Inst: {d['instrument']:<9}] Q: \"{d['question'][:55]}...\"")
        print("-" * 80)

    print("\n" + "=" * 80)
    print("ANALYSIS & RESOLUTION:")
    print("  [Root Cause] : คำถามกว้างๆ มักมีคะแนนเวกเตอร์ใกล้เคียงกันข้ามประเภทเครื่องดนตรี")
    print("                 การแนะนำสายเหล็กให้กีตาร์คลาสสิกทำให้คอกีตาร์หักหรืองอถาวรได้")
    print("  [Solution]   : ติดตั้ง Metadata Pre-filtering (instrument, difficulty, tuning) ก่อนค้นหา")
    print("  [Code Trace] : LAB04/RAG-Guitar/src/document_loader.py (Metadata Tagging)")
    print("                 LAB04/RAG-Guitar/src/vector_store.py (search_with_filter)")
    print("=" * 80)


if __name__ == "__main__":
    run()
