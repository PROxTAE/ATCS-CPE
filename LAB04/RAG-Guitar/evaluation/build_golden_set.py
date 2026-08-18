"""
build_golden_set.py - Builds standard English Evaluation Golden Set for Guitar RAG.
Saves to data/guitar_golden_set.json
"""

import json
import os
import random
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.document_loader import load_qa_file
from src.vector_store import load_chunk_store


def main():
    print("=== Build Golden Evaluation Set for English Guitar RAG ===")
    records = load_qa_file(config.SOURCE_FILE)
    chunks = load_chunk_store(config.CHUNK_STORE_FILE)

    record_to_chunks = {}
    for c in chunks:
        rid = c["record_id"]
        if rid not in record_to_chunks:
            record_to_chunks[rid] = []
        record_to_chunks[rid].append(c["chunk_id"])

    cat_records = {}
    for r in records:
        cat = r["category"]
        if cat not in cat_records:
            cat_records[cat] = []
        cat_records[cat].append(r)

    selected_records = []
    num_samples = min(config.GOLDEN_SET_SIZE, len(records))

    per_cat = max(1, num_samples // len(cat_records))
    for cat, recs in cat_records.items():
        sample_size = min(len(recs), per_cat)
        selected_records.extend(random.sample(recs, sample_size))

    if len(selected_records) < num_samples:
        remaining = [r for r in records if r not in selected_records]
        needed = num_samples - len(selected_records)
        selected_records.extend(random.sample(remaining, min(needed, len(remaining))))

    golden_set = []
    for item in selected_records:
        rel_chunk_ids = record_to_chunks.get(item["id"], [])
        golden_set.append({
            "id": len(golden_set),
            "record_id": item["id"],
            "category": item["category"],
            "query": item["question"],
            "relevant_chunk_ids": rel_chunk_ids,
            "reference_answer": item["answer"],
        })

    os.makedirs(os.path.dirname(config.GOLDEN_SET_FILE), exist_ok=True)
    with open(config.GOLDEN_SET_FILE, "w", encoding="utf-8") as f:
        json.dump(golden_set, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {len(golden_set)} golden evaluation samples at {config.GOLDEN_SET_FILE}")


if __name__ == "__main__":
    main()
