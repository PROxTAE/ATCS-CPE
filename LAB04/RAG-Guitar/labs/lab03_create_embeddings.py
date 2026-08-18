"""
LAB 03: การสร้าง Embedding Vectors จาก Chunks ข้อความ
บันทึกผลลัพธ์เป็นไฟล์ NumPy ที่ outputs/embeddings.npy

วิธีรัน: python labs/lab03_create_embeddings.py
"""

import json
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.embedding_model import EmbeddingModel


def main():
    print("=== Lab 03: Create Embeddings ===")
    if not os.path.exists(config.CHUNKS_FILE):
        print(f"❌ ไม่พบไฟล์ {config.CHUNKS_FILE} กรุณารัน lab02 ก่อน")
        return

    with open(config.CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [c["text"] for c in chunks]
    print(f"กำลังแปลงข้อความ {len(texts)} Chunks เป็นเวกเตอร์ ด้วยโมเดล {config.EMBEDDING_MODEL_NAME}...")

    embedding_model = EmbeddingModel()
    embeddings = embedding_model.encode(texts, batch_size=64, show_progress_bar=True)
    np.save(config.EMBEDDINGS_FILE, embeddings)

    print(f"บันทึก Embeddings ที่: {config.EMBEDDINGS_FILE}")
    print(f"มิติของเวกเตอร์: {embeddings.shape[0]} แถว × {embeddings.shape[1]} มิติ")


if __name__ == "__main__":
    main()
