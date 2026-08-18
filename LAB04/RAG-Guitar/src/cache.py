"""
cache.py - High-Performance Query & Semantic Caching for RAG Pipeline
ช่วยลด Latency จาก ~500-2000ms เหลือ < 5ms เมื่อคำถามเคยถูกประมวลผลแล้ว
"""

import json
import os
import time
import numpy as np


class QueryCache:
    """
    ระบบแคช 2 ระดับ:
    1. Exact Match Cache (O(1) lookup จาก String Hash / Normalization)
    2. Semantic Cache (Cosine Similarity threshold > 0.95 เพื่อตอบคำถามที่มีความหมายเหมือนกัน)
    """

    def __init__(self, cache_file=None, max_size=200, semantic_threshold=0.96):
        self.cache_file = cache_file
        self.max_size = max_size
        self.semantic_threshold = semantic_threshold
        self.cache = {}  # query_norm -> { "response": ..., "embedding": ..., "timestamp": ..., "hits": ... }
        self.hits_count = 0
        self.miss_count = 0
        self.load()

    def _normalize(self, query: str) -> str:
        return " ".join(query.strip().lower().split())

    def get(self, query: str, query_embedding=None):
        norm_q = self._normalize(query)

        # 1. Exact Match Cache Check
        if norm_q in self.cache:
            entry = self.cache[norm_q]
            entry["hits"] += 1
            self.hits_count += 1
            res = dict(entry["response"])
            res["cached"] = True
            res["cache_type"] = "exact"
            return res

        # 2. Semantic Similarity Cache Check (ถ้ามี embedding)
        if query_embedding is not None and len(self.cache) > 0:
            best_score = -1.0
            best_entry = None
            q_vec = np.array(query_embedding, dtype=np.float32)
            q_norm = np.linalg.norm(q_vec)
            if q_norm > 1e-6:
                q_vec = q_vec / q_norm

                for k, entry in self.cache.items():
                    if "embedding" in entry and entry["embedding"] is not None:
                        c_vec = np.array(entry["embedding"], dtype=np.float32)
                        c_norm = np.linalg.norm(c_vec)
                        if c_norm > 1e-6:
                            c_vec = c_vec / c_norm
                            sim = float(np.dot(q_vec, c_vec))
                            if sim > best_score:
                                best_score = sim
                                best_entry = entry

                if best_score >= self.semantic_threshold and best_entry is not None:
                    best_entry["hits"] += 1
                    self.hits_count += 1
                    res = dict(best_entry["response"])
                    res["cached"] = True
                    res["cache_type"] = f"semantic (similarity: {best_score:.3f})"
                    return res

        self.miss_count += 1
        return None

    def put(self, query: str, response: dict, query_embedding=None):
        norm_q = self._normalize(query)
        if len(self.cache) >= self.max_size:
            # Evict least frequently used / oldest
            lfu_key = min(self.cache.keys(), key=lambda k: (self.cache[k]["hits"], self.cache[k]["timestamp"]))
            del self.cache[lfu_key]

        # Convert embedding to list if numpy
        emb_list = query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding

        # Save clean response without temporary timings
        clean_response = {
            "answer": response.get("answer", ""),
            "sources": response.get("sources", []),
            "no_context": response.get("no_context", False),
        }

        self.cache[norm_q] = {
            "response": clean_response,
            "embedding": emb_list,
            "timestamp": time.time(),
            "hits": 0,
        }

    def save(self):
        if not self.cache_file:
            return
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def load(self):
        if not self.cache_file or not os.path.exists(self.cache_file):
            return
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                self.cache = json.load(f)
        except Exception:
            self.cache = {}

    def get_stats(self):
        total = self.hits_count + self.miss_count
        hit_rate = (self.hits_count / total * 100) if total > 0 else 0.0
        return {
            "cached_entries": len(self.cache),
            "hits": self.hits_count,
            "misses": self.miss_count,
            "hit_rate_percent": round(hit_rate, 2),
        }
