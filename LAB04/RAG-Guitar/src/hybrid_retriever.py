"""
hybrid_retriever.py - English Hybrid Search (Dense FAISS + BM25Okapi with Weighted RRF)
Optimized with token caching and guitar-domain specific vocabulary normalization.
"""

import os
import pickle
import re
from functools import lru_cache

from rank_bm25 import BM25Okapi

import config
from src.embedding_model import EmbeddingModel
from src.vector_store import VectorStore, load_chunk_store

# English Tokenization Regex (words, numbers, chord symbols e.g. C#m7, F#dim, Dsus4, G/B)
WORD_PATTERN = re.compile(r"[A-Za-z0-9#\+\-]+|(?:\b[A-G][#b]?(?:maj|min|m|dim|aug|sus|add)?[0-9]?(?:/[A-G][#b]?)?\b)", re.IGNORECASE)

# Standard English stopwords to filter out for sharper BM25 scoring
ENGLISH_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "with",
    "by", "about", "against", "between", "into", "through", "during", "before",
    "after", "above", "below", "from", "up", "down", "is", "are", "was", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did", "how",
    "what", "why", "when", "where", "which", "who", "whom", "this", "that"
}


@lru_cache(maxsize=15000)
def tokenize_word(word: str) -> str:
    return word.strip().lower()


def tokenize(text: str):
    """
    Tokenizes text for BM25 search.
    Preserves guitar chord symbols and technical terms while removing common stopwords.
    """
    tokens = []
    for match in WORD_PATTERN.finditer(text):
        token = tokenize_word(match.group())
        if token and token not in ENGLISH_STOPWORDS and len(token) > 1:
            tokens.append(token)
        elif token in ("c", "d", "e", "f", "g", "a", "b"):  # Single-letter key chords
            tokens.append(token)
    return tokens


def build_bm25(chunks):
    """Builds BM25 index from chunks with category and question boosting"""
    corpus = []
    for chunk in chunks:
        # Boost category and question text for high relevance
        boosted_text = f"{chunk['category']} {chunk['question']} {chunk['question']} {chunk['text']}"
        corpus.append(tokenize(boosted_text))
    return BM25Okapi(corpus)


def save_bm25(bm25, file_path=config.BM25_INDEX_FILE):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        pickle.dump(bm25, f)


def load_bm25(chunks, file_path=config.BM25_INDEX_FILE):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)
    bm25 = build_bm25(chunks)
    save_bm25(bm25, file_path)
    return bm25


def weighted_rrf(ranked_lists_with_weights, rrf_k=config.RRF_K):
    """
    Combines ranked lists using Weighted Reciprocal Rank Fusion.
    """
    scores = {}
    details = {}

    for ranked_list, weight in ranked_lists_with_weights:
        for rank, chunk_id in enumerate(ranked_list, start=1):
            rrf_score = weight * (1.0 / (rrf_k + rank))
            scores[chunk_id] = scores.get(chunk_id, 0.0) + rrf_score

            if chunk_id not in details:
                details[chunk_id] = {}
            details[chunk_id][f"rank_w{weight}"] = rank

    sorted_items = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_items, details


class HybridRetriever:
    """
    Hybrid Retriever supporting Dense (FAISS IndexFlatIP), BM25 Keyword Search,
    Weighted RRF, and Selective Reranking.
    """

    def __init__(self, reranker=None):
        self.chunks = load_chunk_store(config.CHUNK_STORE_FILE)
        self.chunk_by_id = {c["chunk_id"]: c for c in self.chunks}

        self.vector_store = VectorStore()
        self.vector_store.load(config.FAISS_INDEX_FILE)

        self.bm25 = load_bm25(self.chunks)
        self.embedding_model = EmbeddingModel()
        self.reranker = reranker

    def search_dense(self, query: str, top_k=config.CANDIDATE_K):
        q_vec = self.embedding_model.encode_query(query)
        scores, indices = self.vector_store.search(q_vec, top_k=top_k)
        valid_pairs = []
        for s, idx in zip(scores, indices):
            if idx != -1 and idx < len(self.chunks):
                valid_pairs.append((int(idx), float(s)))
        return valid_pairs

    def search_bm25(self, query: str, top_k=config.CANDIDATE_K):
        tokens = tokenize(query)
        if not tokens:
            return []
        bm25_scores = self.bm25.get_scores(tokens)
        top_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:top_k]
        return [(idx, float(bm25_scores[idx])) for idx in top_indices if bm25_scores[idx] > 0]

    def retrieve(self, query: str, top_k=config.TOP_K, extra_queries=None):
        all_queries = [query]
        if extra_queries:
            all_queries.extend(extra_queries)

        if not config.USE_HYBRID:
            # Dense only
            dense_results = self.search_dense(query, top_k=top_k)
            retrieved = []
            for chunk_id, score in dense_results:
                chunk = dict(self.chunk_by_id[chunk_id])
                chunk["score"] = score
                chunk["retrieval_method"] = "dense_only"
                retrieved.append(chunk)
            return retrieved

        # Hybrid Search (Dense + BM25)
        dense_ranked = []
        bm25_ranked = []

        for q in all_queries:
            d_res = self.search_dense(q, top_k=config.CANDIDATE_K)
            dense_ranked.extend([cid for cid, _ in d_res])

            b_res = self.search_bm25(q, top_k=config.CANDIDATE_K)
            bm25_ranked.extend([cid for cid, _ in b_res])

        def unique_list(seq):
            seen = set()
            return [x for x in seq if not (x in seen or seen.add(x))]

        unique_dense = unique_list(dense_ranked)
        unique_bm25 = unique_list(bm25_ranked)

        ranked_lists_with_weights = [
            (unique_dense, config.DENSE_WEIGHT),
            (unique_bm25, config.BM25_WEIGHT),
        ]
        fused_items, _ = weighted_rrf(ranked_lists_with_weights)

        candidates = []
        for chunk_id, rrf_score in fused_items[:config.CANDIDATE_K]:
            chunk = dict(self.chunk_by_id[chunk_id])
            chunk["score"] = rrf_score
            chunk["rrf_score"] = rrf_score
            candidates.append(chunk)

        # Selective Reranker
        if config.USE_RERANK and self.reranker and len(candidates) > 1:
            should_rerank = True
            if config.USE_SELECTIVE_RERANK and len(candidates) >= 2:
                margin = candidates[0]["score"] - candidates[1]["score"]
                if margin > config.RERANK_THRESHOLD_DIFF:
                    should_rerank = False

            if should_rerank:
                candidates = self.reranker.rerank(query, candidates, top_k=top_k)
            else:
                candidates = candidates[:top_k]
        else:
            candidates = candidates[:top_k]

        return candidates
