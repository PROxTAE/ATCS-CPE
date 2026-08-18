"""
LAB 04: การสร้าง FAISS Vector Database สำหรับค้นหาความคล้ายคลึงทางความหมาย
บันทึก Index ที่ vector_db/guitar_faiss.index และ Chunk Store ที่ vector_db/guitar_chunk_store.json

วิธีรัน: python labs/lab04_create_vector_db.py
"""

import json
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.vector_store import VectorStore, save_chunk_store


def main():
    print("=== Lab 04: Create FAISS Vector Database ===")
    if not os.path.exists(config.EMBEDDINGS_FILE) or not os.path.exists(config.CHUNKS_FILE):
        print("❌ ไม่พบไฟล์ Embeddings หรือ Chunks กรุณารัน lab02 และ lab03 ก่อน")
        return

    embeddings = np.load(config.EMBEDDINGS_FILE)
    with open(config.CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"โหลด Embeddings: {embeddings.shape}")
    print(f"โหลด Chunks: {len(chunks)} รายการ")

    store = VectorStore()
    store.build(embeddings)
    store.save(config.FAISS_INDEX_FILE)
    save_chunk_store(chunks, config.CHUNK_STORE_FILE)

    print(f"สร้าง FAISS Index สำเร็จที่: {config.FAISS_INDEX_FILE}")
    print(f"บันทึก Chunk Store ที่: {config.CHUNK_STORE_FILE}")


if __name__ == "__main__":
    main()
