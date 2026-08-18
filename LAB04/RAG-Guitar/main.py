"""
main.py - Interactive CLI for English Guitar Master RAG System (LAB04: RAG-Guitar)
"""

import sys
import config
from src.rag_pipeline import RAGPipeline


def print_banner():
    print("=" * 70)
    print("  🎸  PROxTAE Guitar RAG Assistant (LAB04: RAG-Guitar)")
    print("  Comprehensive English Guitar Knowledge, Hardware, Theory & Chords")
    print("=" * 70)
    print("  Type your guitar question, or use special commands:")
    print("    - '/settings' : Display current pipeline feature flags")
    print("    - '/cache'    : View real-time Query Cache statistics")
    print("    - '/clear'    : Clear conversation memory history")
    print("    - 'exit'      : Quit program")
    print("-" * 70 + "\n")


def format_response(result: dict):
    print("\n" + "─" * 70)
    print("💬 Answer from Guitar Master AI:")
    print("─" * 70)
    print(result.get("answer", ""))

    # Performance Timings Breakdown
    if config.SHOW_DEBUG and "timings" in result:
        t = result["timings"]
        print("\n⏱️  [Performance Breakdown]:")
        if "cache_lookup_ms" in t:
            print(f"   • Cache Lookup : {t['cache_lookup_ms']} ms  -->  {t.get('status', '')}")
        else:
            print(f"   • Query Transform : {t.get('query_transform_ms', 0)} ms")
            print(f"   • Retrieval       : {t.get('retrieval_ms', 0)} ms")
            print(f"   • Generation      : {t.get('generation_ms', 0)} ms")
            print(f"   • Total Latency   : {t.get('total_ms', 0)} ms ({t.get('status', '')})")

    # Sources Citations
    if config.SHOW_SOURCES and result.get("sources"):
        print("\n📚 [Reference Sources]:")
        for s in result["sources"]:
            print(f"   [{s['n']}] Category: {s.get('category', 'General')} | Line: {s['line_no']} | Score: {s['score']}")
            print(f"       Topic: {s['question']}")
    print("─" * 70 + "\n")


def main():
    print_banner()
    print("⏳ Initializing Guitar RAG Pipeline (BAAI/bge-small-en-v1.5)...")
    try:
        rag = RAGPipeline()
    except Exception as e:
        print(f"❌ Initialization Error: {e}")
        print("💡 Please run 'python build_index.py' first.")
        return

    rag.show_settings()
    print("✅ System Ready! Ask any guitar question below:\n")

    while True:
        try:
            query = input("🎸 Ask Guitar Question > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Thank you for using Guitar Master RAG Assistant. Goodbye!")
            break

        if not query:
            continue

        if query.lower() in ("exit", "quit", "q"):
            print("👋 Goodbye!")
            break

        if query.lower() == "/settings":
            rag.show_settings()
            continue

        if query.lower() == "/cache":
            stats = rag.get_cache_stats()
            print("\n⚡ [Cache Statistics]:")
            for k, v in stats.items():
                print(f"   • {k}: {v}")
            print()
            continue

        if query.lower() == "/clear":
            rag.reset_memory()
            print("🧹 Conversation memory cleared.\n")
            continue

        # Query RAG Pipeline
        result = rag.ask(query)
        format_response(result)


if __name__ == "__main__":
    main()
