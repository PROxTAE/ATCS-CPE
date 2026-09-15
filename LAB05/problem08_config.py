# -*- coding: utf-8 -*-
"""
Problem 08: RAG Pipeline Configuration Matrix for Guitar Assistant
Demonstrates how component toggles (Hybrid BM25+Dense, Cross-Encoder Re-ranker,
Cross-Lingual Translation, LLM Generator vs Raw Top-K, Multi-Turn Memory) dictate
system performance, memory footprint, and generation behavior.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from data_loader import load_guitar_kb

DOCS = load_guitar_kb()

GUITAR_RAG_CONFIG = {
    "KB_SOURCE": "data/guitar_knowledge_base.txt",
    "TOTAL_RECORDS": len(DOCS),
    "EMBEDDING_MODEL": "BAAI/bge-small-en-v1.5 (384-dim)",
    "USE_HYBRID_RETRIEVAL": True,
    "USE_CROSS_ENCODER_RERANK": True,
    "USE_CROSS_LINGUAL_TRANSLATION": True,
    "USE_LLM_GENERATION": True,
    "USE_CONVERSATION_MEMORY": True,
    "STRICT_CHORD_NORMALIZATION": True,
    "SHOW_SOURCE_CITATIONS": True,
}


def print_active_pipeline(config):
    print("\n[ACTIVE PIPELINE EXECUTION SEQUENCE]")
    print("-" * 80)
    step = 1

    if config.get("USE_CONVERSATION_MEMORY"):
        print(f"  Step {step}: [MEMORY] Multi-Turn Conversation Buffer tracks prior fret context")
        step += 1

    if config.get("STRICT_CHORD_NORMALIZATION"):
        print(f"  Step {step}: [PREPROCESSING] Canonical Chord Normalizer (CΔ7 -> Cmaj7, Gbm -> F#m)")
        step += 1

    if config.get("USE_CROSS_LINGUAL_TRANSLATION"):
        print(f"  Step {step}: [TRANSLATION] Cross-Lingual Engine maps Thai query to English terms")
        step += 1

    if config.get("USE_HYBRID_RETRIEVAL"):
        print(f"  Step {step}: [RETRIEVAL] Hybrid RRF: FAISS Dense (Cosine) + BM25 Okapi (Sparse)")
    else:
        print(f"  Step {step}: [RETRIEVAL] Single Dense Stream (FAISS IndexFlatIP only)")
    step += 1

    if config.get("USE_CROSS_ENCODER_RERANK"):
        print(f"  Step {step}: [RE-RANKER] Cross-Encoder resolves polysemous terms ('Bridge' / 'Pick')")
        step += 1
    else:
        print(f"  Step {step}: [RE-RANKER] Bypassed (Optimized for lower latency)")
        step += 1

    if config.get("USE_LLM_GENERATION"):
        print(f"  Step {step}: [GENERATOR] LLM API synthesizes structured Thai markdown with chord grids")
    else:
        print(f"  Step {step}: [GENERATOR] Raw Top-K Direct Retrieval (Unformatted text snippet)")
    step += 1

    if config.get("SHOW_SOURCE_CITATIONS"):
        print(f"  Step {step}: [CITATIONS] Provenance verified and attached with Doc ID badges")
        step += 1


def run():
    print("=" * 80)
    print("PROBLEM 08: RAG System Configuration Matrix (Guitar Domain)")
    print("Pipeline Stage: System Architecture & Orchestration Stage")
    print("=" * 80)

    print("\n[CONFIG PARAMETERS TABLE]")
    print("+----------------------------------+--------------------------------------------+")
    print("| Config Key                       | Active Value                               |")
    print("+----------------------------------+--------------------------------------------+")
    for k, v in GUITAR_RAG_CONFIG.items():
        print(f"| {k:<32} | {str(v):<42} |")
    print("+----------------------------------+--------------------------------------------+")

    print_active_pipeline(GUITAR_RAG_CONFIG)

    print("\n[SYSTEM OPERATION MODES COMPARISON]")
    print("-" * 80)
    print("Mode 1: Ultra-Low Latency Mode (Hybrid=False, Re-rank=False, LLM=False):")
    print("  - Target Response Time : ~2.5 ms (Exact Vector Cache Match)")
    print("  - Output Characteristics: Raw Top-1 chunk text snippet")

    print("\nMode 2: High-Accuracy Studio Web Mode (Hybrid=True, Re-rank=True, LLM=True):")
    print("  - Target Response Time : ~250 - 350 ms (Full LLM Synthesis)")
    print("  - Output Characteristics: Formatted Thai Markdown, 6-string diagrams & verified citations")

    print("\n" + "=" * 80)
    print("ANALYSIS & RESOLUTION:")
    print("  [Root Cause] : สถาปัตยกรรม RAG มีหลาย Component หากเขียนผูกติดกันจะสลับโหมดได้ยาก")
    print("                 การเปิดทุกโมดูลพร้อมกันตลอดเวลาทำให้ระบบช้าลงโดยไม่จำเป็นในกรณีคำถามง่ายๆ")
    print("  [Solution]   : ออกแบบ Centralized Config File ควบคุมการเปิด/ปิด Component แบบแยกส่วน")
    print("  [Code Trace] : LAB04/RAG-Guitar/config.py (USE_HYBRID, USE_RERANKER, USE_LLM, USE_MEMORY)")
    print("                 LAB04/RAG-Guitar/src/rag_pipeline.py")
    print("=" * 80)


if __name__ == "__main__":
    run()
