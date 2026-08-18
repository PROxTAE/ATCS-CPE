"""
rerankers.py - จัดอันดับผลลัพธ์ Chunks ใหม่ด้วย Cross-Encoder เพื่อความแม่นยำสูงสุด
"""

import config


class CrossEncoderReranker:
    def __init__(self, model_name=None):
        self.model_name = model_name or config.RERANK_MODEL_NAME
        self.model = None

    def _load_model(self):
        if self.model is None:
            try:
                from sentence_transformers import CrossEncoder
                self.model = CrossEncoder(self.model_name)
            except Exception as e:
                #print(f"[Reranker] ไม่สามารถโหลด {self.model_name}: {e}")
                self.model = False

    def rerank(self, query: str, chunks: list, top_k=config.TOP_K):
        if not chunks:
            return []

        self._load_model()
        if not self.model:
            return chunks[:top_k]

        # สร้างคู่ (Query, Document Text)
        pairs = [[query, chunk["text"]] for chunk in chunks]
        scores = self.model.predict(pairs)

        for chunk, score in zip(chunks, scores):
            chunk["rerank_score"] = float(score)
            chunk["score"] = float(score)

        sorted_chunks = sorted(chunks, key=lambda c: c["rerank_score"], reverse=True)
        return sorted_chunks[:top_k]


def get_reranker():
    if not config.USE_RERANK:
        return None
    return CrossEncoderReranker()
