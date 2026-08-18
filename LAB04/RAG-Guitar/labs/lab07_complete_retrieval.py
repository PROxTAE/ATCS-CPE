"""
LAB 07: End-to-End English Guitar RAG Pipeline (Hybrid Search + Caching + Fast Generation)

Run: python labs/lab07_complete_retrieval.py
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.rag_pipeline import RAGPipeline


def main():
    print("=== Lab 07: Complete English Guitar RAG Pipeline ===")
    rag = RAGPipeline()
    rag.show_settings()

    test_questions = [
        "How do you play the C Major chord on guitar?",
        "What are the tonal differences between Sitka Spruce and Cedar soundboards?",
        "What causes fret buzz and how do you troubleshoot it?",
    ]

    for q in test_questions:
        print("\n" + "=" * 65)
        print(f"🎸 Query: {q}")
        print("-" * 65)
        result = rag.ask(q)

        print(f"💬 Answer:\n{result['answer']}\n")
        print(f"⏱️ Timings Breakdown: {result.get('timings', {})}")

        if result.get("sources"):
            print("\n📚 Reference Sources:")
            for s in result["sources"][:2]:
                print(f"  [{s['n']}] Category: {s.get('category', '')} | Q: {s['question']} (Score: {s['score']})")


if __name__ == "__main__":
    main()
