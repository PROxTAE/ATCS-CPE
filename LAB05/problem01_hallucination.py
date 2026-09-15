# -*- coding: utf-8 -*-
"""
Problem 01: Hallucination & Out-of-Scope Generation in Guitar RAG
Demonstrates how an unconstrained LLM generates plausible-sounding yet impossible
guitar chord voicings or answers queries completely outside the guitar domain
when the retriever returns no supporting context.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from data_loader import load_guitar_kb

DOCS = load_guitar_kb()


def retrieve(query, top_k=3, score_threshold=2):
    """Simple term-frequency retriever for simulation."""
    query_tokens = query.lower().split()
    scored = []
    for doc in DOCS:
        match_score = sum(tok in doc["text"].lower() for tok in query_tokens)
        if match_score >= score_threshold:
            scored.append((match_score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def unconstrained_generator(query, context):
    """Simulated hallucination: Generates an answer even when context is empty or irrelevant."""
    if not context:
        if "chord" in query.lower() or "fret" in query.lower():
            return (
                "To play this chord, place your 1st finger on Fret 1 (all 6 strings), "
                "stretch your 3rd finger to Fret 12, 4th finger on Fret 14, and press string 3 with your chin.\n"
                "    [FAILURE REASON]: Anatomically impossible fingering fabricated without KB evidence!"
            )
        return (
            "A roundtrip ticket to Tokyo currently costs around 18,500 THB via Thai Airways.\n"
            "    [FAILURE REASON]: Completely out of guitar domain, fabricated without KB evidence!"
        )
    return context[0]["answer"]


def grounded_rag_generator(query, context):
    """Constrained Grounded Generation: Refuses to hallucinate when context is absent."""
    if not context:
        return (
            "[REFUSAL - GROUNDED]: ไม่พบข้อมูลที่น่าเชื่อถือใน Guitar Knowledge Base สำหรับคำถามนี้\n"
            "    ระบบปฏิเสธการตอบเพื่อป้องกันการสร้างฟอร์มคอร์ดหรือสเปกการตั้งสายที่ผิดพลาด"
        )
    return f"[VERIFIED IN KB]: {context[0]['answer']}"


def run():
    print("=" * 80)
    print("PROBLEM 01: Hallucination & Scope Constraints in Guitar RAG")
    print("Pipeline Stage: Generation & Output Guardrails Stage")
    print("=" * 80)

    test_queries = [
        ("Out-of-Scope (Non-Guitar)", "ตั๋วเครื่องบินไปโตเกียวราคาเท่าไหร่"),
        ("Out-of-Scope (Impossible Chord)", "How to play Cmaj13sus2 with 8 fingers on fret 12"),
        ("In-Scope (Guitar Knowledge Base)", "What is C major chord open position fingering"),
    ]

    for idx, (label, query) in enumerate(test_queries, 1):
        ctx = retrieve(query, top_k=2)
        print(f"\n[TEST CASE {idx}/3] {label}")
        print("-" * 80)
        print(f"User Query     : \"{query}\"")
        retrieved_titles = [d["question"] for d in ctx]
        print(f"Retrieved Docs : {retrieved_titles if retrieved_titles else 'None (0 matches found)'}")

        print("\n[OUTPUT A] Unconstrained Generator (Without Guardrails):")
        print(f"  {unconstrained_generator(query, ctx)}")

        print("\n[OUTPUT B] Grounded RAG Generator (With Faithfulness Guardrails):")
        print(f"  {grounded_rag_generator(query, ctx)}")
        print("-" * 80)

    print("\n" + "=" * 80)
    print("ANALYSIS & RESOLUTION:")
    print("  [Root Cause] : โมเดล LLM พยายามเดาหรือแต่งคำตอบขึ้นมาเอง (Plausible Hallucination)")
    print("                 เมื่อในคลังความรู้ไม่มีข้อมูล ในโดเมนดนตรีอาจทำให้ผู้เรียนบาดเจ็บได้")
    print("  [Solution]   : 1. ตั้งค่า System Prompt ให้ตอบเฉพาะข้อมูลใน Context เท่านั้น")
    print("                 2. กำหนด Similarity Threshold หากคะแนนต่ำกว่าเกณฑ์ให้ปฏิเสธการตอบ")
    print("  [Code Trace] : LAB04/RAG-Guitar/src/prompt_templates.py (GUITAR_SYSTEM_PROMPT)")
    print("                 LAB04/RAG-Guitar/config.py (SIMILARITY_THRESHOLD = 0.45)")
    print("=" * 80)


if __name__ == "__main__":
    run()
