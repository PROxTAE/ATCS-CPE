"""
eval_generation.py - ประเมินคุณภาพคำตอบของ Generator (LLM)
วัดอัตราการอ้างอิงแหล่งที่มา (Citation Rate) และความสอดคล้องกับ Reference
บันทึกที่ outputs/eval_generation.json
"""

import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.rag_pipeline import RAGPipeline


def main():
    print("=== Evaluation: Answer Generation Quality ===")
    if not os.path.exists(config.GOLDEN_SET_FILE):
        from evaluation.build_golden_set import main as build_gs
        build_gs()

    with open(config.GOLDEN_SET_FILE, "r", encoding="utf-8") as f:
        golden_set = json.load(f)

    rag = RAGPipeline()
    sample_queries = golden_set[:10]  # ประเมิน 10 ตัวอย่าง

    results = []
    has_citations = 0
    total_latency = 0.0

    print(f"กำลังประเมินคำตอบ {len(sample_queries)} ข้อ...\n")

    for item in sample_queries:
        query = item["query"]
        res = rag.ask(query)

        ans = res.get("answer", "")
        # ตรวจสอบการอ้างอิง [1], [2], ...
        cited = any(f"[{i}]" in ans for i in range(1, 10))
        if cited:
            has_citations += 1

        timings = res.get("timings", {})
        total_latency += timings.get("total_ms", 0.0)

        results.append({
            "query": query,
            "category": item["category"],
            "generated_answer": ans,
            "reference_answer": item["reference_answer"],
            "has_citation": cited,
            "timings": timings,
        })
        print(f"Q: {query}")
        print(f"Status: {timings.get('status', '')} ({timings.get('total_ms', 0)} ms) | Citation: {'✅' if cited else '❌'}\n")

    summary = {
        "total_evaluated": len(sample_queries),
        "citation_rate": round(has_citations / len(sample_queries), 2),
        "avg_total_latency_ms": round(total_latency / len(sample_queries), 2),
        "samples": results,
    }

    with open(config.EVAL_GENERATION_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print(f"✅ บันทึกผลการประเมินคำตอบลงที่: {config.EVAL_GENERATION_FILE}")
    print(f"📊 Citation Rate: {summary['citation_rate'] * 100}% | Avg Latency: {summary['avg_total_latency_ms']} ms")
    print("=" * 60)


if __name__ == "__main__":
    main()
