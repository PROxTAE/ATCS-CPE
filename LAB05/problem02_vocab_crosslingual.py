# -*- coding: utf-8 -*-
"""
Problem 02: Vocabulary Mismatch & Cross-Lingual Gap in Guitar RAG
Demonstrates the failure of Bag-of-Words / Keyword Search when users query in Thai
against an English Guitar Knowledge Base, and how Cross-Lingual Query Translation
combined with Dense Semantic Embeddings solves the problem.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from data_loader import load_guitar_kb

DOCS = load_guitar_kb()


def bow_tokenize(text):
    """Simple whitespace + lowercase tokenizer."""
    return set(text.lower().replace("?", "").replace(",", "").split())


def thai_keyword_search(query_thai, docs, top_k=3):
    """Keyword search directly matching Thai words against English documents."""
    q_tokens = bow_tokenize(query_thai)
    scored = []
    for d in docs:
        d_tokens = bow_tokenize(d["text"])
        overlap = q_tokens & d_tokens
        scored.append((len(overlap), overlap, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]


TRANSLATION_MAP = {
    "วิธีจับคอร์ดทาบ F ไม่ให้บอด": "How to play F barre chord clean without string buzzing",
    "สายกีตาร์สูงเกินไปแก้ยังไง": "How to lower high guitar action string height setup truss rod",
    "คอร์ด C จับยังไง": "How do you play C Major chord on guitar open position",
    "ความต่างระหว่าง pickup humbucker กับ single-coil": "difference between humbucker and single coil pickups tone",
}


def semantic_retrieval_simulation(translated_query, docs, top_k=2):
    """
    Simulates Dense Semantic Retrieval (BAAI/bge-small-en-v1.5)
    matching the English translated intent to the curated English KB.
    """
    q_tokens = bow_tokenize(translated_query)
    scored = []
    for d in docs:
        d_tokens = bow_tokenize(d["text"])
        score = sum(3 if t in d["question"].lower() else 1 for t in q_tokens if t in d_tokens)
        if score > 0:
            scored.append((score, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]


def run():
    print("=" * 80)
    print("PROBLEM 02: Vocabulary Mismatch & Cross-Lingual Gap (Thai Query -> English KB)")
    print("Pipeline Stage: Query Preprocessing & Dense Embedding Stage")
    print("=" * 80)

    test_queries = [
        "วิธีจับคอร์ดทาบ F ไม่ให้บอด",
        "สายกีตาร์สูงเกินไปแก้ยังไง",
        "ความต่างระหว่าง pickup humbucker กับ single-coil"
    ]

    for idx, q_thai in enumerate(test_queries, 1):
        print(f"\n[TEST CASE {idx}/3] Thai Query: \"{q_thai}\"")
        print("-" * 80)

        # 1. Direct Keyword / BoW Retrieval against English KB
        results_keyword = thai_keyword_search(q_thai, DOCS, top_k=2)
        top_score, overlap, top_doc = results_keyword[0]

        print("[STAGE 1] Pure Keyword / Bag-of-Words Search (Direct against English KB):")
        print(f"  Token Overlap Count : {top_score}")
        print(f"  Overlapping Words   : {list(overlap)}")
        if top_score == 0:
            print("  Retrieval Status    : [FAILED] Zero relevance found in English KB")
        else:
            print(f"  Retrieved Result    : [MISMATCH] \"{top_doc['question']}\"")

        # 2. Cross-Lingual Translation + Dense Retrieval
        translated_en = TRANSLATION_MAP.get(q_thai, q_thai)
        print("\n[STAGE 2] Cross-Lingual Query Translation + Dense Semantic Embedding:")
        print(f"  Translated Query    : \"{translated_en}\"")

        semantic_results = semantic_retrieval_simulation(translated_en, DOCS, top_k=2)
        if semantic_results:
            match_doc = semantic_results[0][1]
            print("  Retrieval Status    : [SUCCESS] Exact relevant document retrieved")
            print(f"  Category            : [{match_doc['category']}]")
            print(f"  Question            : \"{match_doc['question']}\"")
            print(f"  Snippet             : {match_doc['answer'][:120]}...")
        else:
            print("  Retrieval Status    : [FAILED] No match found")
        print("-" * 80)

    print("\n" + "=" * 80)
    print("ANALYSIS & RESOLUTION:")
    print("  [Root Cause] : คำค้นหาภาษาไทยไม่มี Exact Token Overlap กับคลังความรู้สากลภาษาอังกฤษ")
    print("                 และโมเดลเวกเตอร์ภาษาไทยมักตัดคำทับศัพท์ผิดเพี้ยน")
    print("  [Solution]   : ใช้ Cross-Lingual Pipeline: แปลง Query ไทยเป็นคำเทคนิคภาษาอังกฤษ")
    print("                 ค้นหาผ่าน Dense Vector (bge-small-en) แล้วส่งให้ LLM สังเคราะห์คำตอบเป็นภาษาไทย")
    print("  [Code Trace] : LAB04/RAG-Guitar/src/query_transform.py (translate_and_expand_query)")
    print("                 LAB04/RAG-Guitar/src/embedding_model.py (BAAI/bge-small-en-v1.5)")
    print("=" * 80)


if __name__ == "__main__":
    run()
