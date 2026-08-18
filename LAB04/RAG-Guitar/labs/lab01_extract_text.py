"""
LAB 01: Extract text and Q&A records from English Guitar Knowledge Base.
Saves parsed records to outputs/extracted_text.json

Run: python labs/lab01_extract_text.py
"""

import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.document_loader import load_qa_file


def main():
    print("=== Lab 01: Extract English Guitar Knowledge Base ===")
    print(f"Reading file: {config.SOURCE_FILE}")

    records = load_qa_file(config.SOURCE_FILE)
    print(f"Found a total of {len(records)} Q&A pairs")

    with open(config.EXTRACTED_TEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"Results saved to: {config.EXTRACTED_TEXT_FILE}")

    print("\nSample records:")
    for record in records[:2]:
        print(f"  - [{record['category']}] Q: {record['question']}")
        print(f"    A: {record['answer'][:80]}...\n")


if __name__ == "__main__":
    main()
