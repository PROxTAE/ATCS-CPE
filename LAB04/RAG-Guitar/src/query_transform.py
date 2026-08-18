"""
query_transform.py - Query Transformation (Multi-Query, Rewrite, HyDE) for English Guitar Q&A.
"""

import config


class QueryTransformer:
    def __init__(self, llm):
        self.llm = llm

    def transform(self, query: str, history: str = ""):
        if not config.USE_QUERY_TRANSFORM:
            return [query]

        mode = config.QUERY_TRANSFORM_MODE

        if mode == "multi_query":
            return self._multi_query(query)
        elif mode == "rewrite":
            return self._rewrite(query, history)
        elif mode == "hyde":
            return self._hyde(query)

        return [query]

    def _multi_query(self, query: str):
        prompt = (
            f"You are an expert guitar technician and instructor. Generate {config.MULTI_QUERY_COUNT - 1} diverse alternative search queries "
            f"or rephrasings for searching a specialized guitar knowledge base, preserving the exact intent of the original query:\n"
            f"Original Query: {query}\n"
            f"Output only the alternative queries, one per line, without numbering, bullets, or extra text."
        )
        try:
            response = self.llm.chat([{"role": "user", "content": prompt}])
            lines = [l.strip().lstrip("0123456789.-*• ") for l in response.split("\n") if l.strip()]
            queries = [query] + lines[:config.MULTI_QUERY_COUNT - 1]
            return queries
        except Exception:
            return [query]

    def _rewrite(self, query: str, history: str = ""):
        prompt = (
            f"Rewrite the following guitar-related user question into a clear, standalone, highly specific search query suitable for semantic vector search.\n"
            f"Context History: {history}\n"
            f"Question: {query}\n"
            f"Output only the single rewritten query string."
        )
        try:
            response = self.llm.chat([{"role": "user", "content": prompt}])
            rewritten = response.strip()
            return [rewritten] if rewritten else [query]
        except Exception:
            return [query]

    def _hyde(self, query: str):
        prompt = (
            f"Write a concise hypothetical answer paragraph for the following guitar question:\n"
            f"Question: {query}\n"
            f"Hypothetical Answer:"
        )
        try:
            hypo_doc = self.llm.chat([{"role": "user", "content": prompt}])
            return [query, hypo_doc.strip()]
        except Exception:
            return [query]
