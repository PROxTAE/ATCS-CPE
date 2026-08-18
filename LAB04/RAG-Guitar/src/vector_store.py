"""
vector_store.py - จัดการ FAISS Index สำหรับ Dense Semantic Search
ใช้ IndexFlatIP (Cosine Similarity) ทำงานร่วมกับ L2-Normalized Vectors
"""

import json
import os
import faiss
import numpy as np


class VectorStore:
    def __init__(self):
        self.index = None

    def build(self, embeddings: np.ndarray):
        """
        สร้าง FAISS Index แบบ Flat Inner Product (Cosine Similarity)
        """
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(np.ascontiguousarray(embeddings, dtype=np.float32))
        return self.index

    def search(self, query_vector: np.ndarray, top_k=10):
        """
        ค้นหาเวกเตอร์ที่ใกล้เคียงที่สุด คืนค่า (scores, indices)
        scores คือ Cosine Similarity (ค่าสูงสุด = 1.0)
        """
        if self.index is None:
            raise ValueError("FAISS Index ยังไม่ได้ถูกสร้างหรือโหลด")

        q_vec = np.ascontiguousarray(query_vector.reshape(1, -1), dtype=np.float32)
        scores, indices = self.index.search(q_vec, top_k)
        return scores[0], indices[0]

    def save(self, file_path: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        faiss.write_index(self.index, file_path)

    def load(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"ไม่พบไฟล์ Index: {file_path}")
        self.index = faiss.read_index(file_path)
        return self.index


def save_chunk_store(chunks: list, file_path: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)


def load_chunk_store(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ไม่พบไฟล์ Chunk Store: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
