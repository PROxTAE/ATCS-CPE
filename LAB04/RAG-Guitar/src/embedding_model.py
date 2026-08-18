"""
embedding_model.py - Wrapper สำหรับโมเดลแปลงข้อความเป็น Vector (Embedding)
ใช้ sentence-transformers พร้อมรองรับ L2-Normalization สำหรับ Cosine Similarity
"""

import numpy as np
from sentence_transformers import SentenceTransformer
import config


class EmbeddingModel:
    _instance = None

    def __new__(cls, model_name=None):
        # Singleton pattern เพื่อโหลดโมเดลเข้าหน่วยความจำเพียงครั้งเดียว
        if cls._instance is None:
            cls._instance = super(EmbeddingModel, cls).__new__(cls)
            cls._instance.model_name = model_name or config.EMBEDDING_MODEL_NAME
            #print(f"[Embedding] กำลังโหลดโมเดล: {cls._instance.model_name}...")
            cls._instance.model = SentenceTransformer(cls._instance.model_name)
        return cls._instance

    def encode(self, texts, batch_size=64, show_progress_bar=False):
        """
        แปลงข้อความเดี่ยว (str) หรือหลายข้อความ (list[str]) ให้เป็น numpy array
        พร้อม normalize ให้ขนาดเวกเตอร์เท่ากับ 1.0 เพื่อใช้ Inner Product (Cosine Similarity)
        """
        single_input = isinstance(texts, str)
        if single_input:
            texts = [texts]

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress_bar,
            normalize_embeddings=config.NORMALIZE_EMBEDDINGS,
            convert_to_numpy=True,
        )

        embeddings = np.array(embeddings, dtype=np.float32)

        return embeddings[0] if single_input else embeddings

    def encode_query(self, query: str):
        """สำหรับ encode คำถาม 1 คำถาม"""
        return self.encode(query)
