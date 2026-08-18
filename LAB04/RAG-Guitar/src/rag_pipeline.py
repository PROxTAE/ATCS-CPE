"""
rag_pipeline.py - End-to-End High-Performance RAG Pipeline for English Guitar Knowledge Base.
Connects QueryCache -> QueryTransformer -> HybridRetriever -> Generator -> Memory
"""

import time
import config
from src.cache import QueryCache
from src.embedding_model import EmbeddingModel
from src.generator import Generator, get_llm
from src.hybrid_retriever import HybridRetriever
from src.memory import ConversationMemory
from src.query_transform import QueryTransformer
from src.rerankers import get_reranker


class RAGPipeline:
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.cache = QueryCache(config.CACHE_FILE) if config.USE_CACHE else None
        self.retriever = HybridRetriever(reranker=get_reranker())
        self.llm = get_llm()
        self.transformer = QueryTransformer(self.llm)
        self.generator = Generator(self.llm)
        self.memory = ConversationMemory()

    def ask(self, query: str, top_k=config.TOP_K):
        t0 = time.time()
        q_emb = None

        # 0. Cache Check
        if config.USE_CACHE and self.cache is not None:
            q_emb = self.embedding_model.encode_query(query)
            cached_res = self.cache.get(query, query_embedding=q_emb)
            if cached_res is not None:
                total_time = round((time.time() - t0) * 1000, 2)
                cached_res["queries_used"] = [query]
                # Preserve retrieved chunks from cache or sources
                if not cached_res.get("retrieved"):
                    cached_res["retrieved"] = cached_res.get("sources", [])
                cached_res["timings"] = {
                    "cache_lookup_ms": total_time,
                    "total_ms": total_time,
                    "status": f"⚡ CACHE HIT ({cached_res.get('cache_type', 'exact')})"
                }
                return cached_res

        # 1. Query Transformation
        t_trans_start = time.time()
        history = self.memory.get_context() if config.USE_MEMORY else ""
        transform_history = history if self.memory.is_followup(query) else ""
        queries = self.transformer.transform(query, transform_history)
        t_trans_ms = round((time.time() - t_trans_start) * 1000, 2)

        # 2. Hybrid Retrieval
        t_ret_start = time.time()
        chunks = self.retriever.retrieve(
            queries[0],
            top_k=top_k,
            extra_queries=queries[1:],
        )
        t_ret_ms = round((time.time() - t_ret_start) * 1000, 2)

        # 3. LLM Answer Generation
        t_gen_start = time.time()
        result = self.generator.generate(query, chunks, history)
        t_gen_ms = round((time.time() - t_gen_start) * 1000, 2)

        # 4. Memory Update
        if config.USE_MEMORY and not result.get("no_context", False):
            self.memory.add_user(query)
            self.memory.add_assistant(result["answer"])

        total_ms = round((time.time() - t0) * 1000, 2)

        result["queries_used"] = queries
        result["retrieved"] = chunks
        result["timings"] = {
            "query_transform_ms": t_trans_ms,
            "retrieval_ms": t_ret_ms,
            "generation_ms": t_gen_ms,
            "total_ms": total_ms,
            "status": "MISS (Full Pipeline Execution)"
        }

        # 5. Cache Put (Save with retrieved chunks)
        if config.USE_CACHE and self.cache is not None and not result.get("no_context", False):
            if q_emb is None:
                q_emb = self.embedding_model.encode_query(query)
            self.cache.put(query, result, query_embedding=q_emb)
            self.cache.save()

        return result

    def search_only(self, query: str, top_k=config.TOP_K):
        queries = self.transformer.transform(query)
        return self.retriever.retrieve(queries[0], top_k=top_k, extra_queries=queries[1:])

    def reset_memory(self):
        self.memory.clear()

    def get_cache_stats(self):
        return self.cache.get_stats() if self.cache else {}

    def show_settings(self):
        settings = [
            ("⚡ Dual-Level Query Cache", config.USE_CACHE),
            ("🔍 Hybrid Search (Dense + BM25)", config.USE_HYBRID),
            ("🎯 Cross-Encoder Reranker", config.USE_RERANK),
            ("⚡ Selective Reranking", config.USE_SELECTIVE_RERANK),
            ("🔄 Query Transformation", config.USE_QUERY_TRANSFORM),
            ("💬 Conversation Memory", config.USE_MEMORY),
            ("🤖 LLM Answer Generation", config.USE_LLM),
        ]
        print("\n" + "=" * 60)
        print("  🎸 Guitar RAG System (English) Configuration Status")
        print("=" * 60)
        for name, enabled in settings:
            status = "✅ ENABLED " if enabled else "❌ DISABLED"
            print(f"  {status:<16} : {name}")
        print("=" * 60 + "\n")
