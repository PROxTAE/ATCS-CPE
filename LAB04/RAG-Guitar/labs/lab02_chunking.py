"""
LAB 02: การตัดแบ่งข้อความเป็น Chunks ย่อย (Text Chunking)
บันทึกผลลัพธ์ลงที่ outputs/chunks.json

วิธีรัน: python labs/lab02_chunking.py
"""

import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.document_loader import load_qa_file
from src.text_splitter import build_chunks


def main():
    print("=== Lab 02: Chunking Guitar Data ===")
    records = load_qa_file(config.SOURCE_FILE)
    print(f"จำนวน Q&A ต้นฉบับ: {len(records)}")

    chunks = build_chunks(records, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    print(f"แบ่งเป็น Chunks ได้ทั้งหมด: {len(chunks)} ชิ้น (Chunk size: {config.CHUNK_SIZE}, Overlap: {config.CHUNK_OVERLAP})")

    with open(config.CHUNKS_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"บันทึกผลลัพธ์ลงที่: {config.CHUNKS_FILE}")
    print("\nตัวอย่าง Chunk แรก:")
    print(f"  ID: {chunks[0]['chunk_id']}")
    print(f"  Category: {chunks[0]['category']}")
    print(f"  Text: {chunks[0]['text'][:80]}...")


if __name__ == "__main__":
    main()
