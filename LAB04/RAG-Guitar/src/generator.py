"""
generator.py - LLM Answer Generation (Gemini, OpenAI, Ollama) and Fast Direct Retrieval (NoLLM)
"""

import os
from openai import OpenAI
import config
from src.prompt_templates import build_messages


class LLM:
    """LLM client via OpenAI-compatible interface (supports Gemini / OpenAI / Ollama)"""

    def __init__(self):
        provider = config.LLM_PROVIDER
        base_url, default_model, key_name = config.LLM_PROVIDERS.get(provider, config.LLM_PROVIDERS["gemini"])

        self.model = config.LLM_MODEL or default_model
        
        # Resolve API Key
        if provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY") or ""
        else:
            api_key = "ollama-no-key"

        self.client = OpenAI(base_url=base_url, api_key=api_key or "placeholder")

    def chat(self, messages: list):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=config.LLM_TEMPERATURE,
            max_tokens=config.LLM_MAX_TOKENS,
        )
        return response.choices[0].message.content.strip()


class NoLLM:
    """Fast direct retrieval mode without calling an external LLM API"""
    model = "Fast-Direct-Retrieved-Mode"

    def chat(self, messages: list):
        user_message = messages[-1]["content"]
        if "Reference Context:" not in user_message:
            return config.NO_CONTEXT_MESSAGE

        parts = user_message.split("Reference Context:")[1].split("User Question:")[0].strip()
        first_doc = parts.split("\n\n")[0]
        return f"{first_doc}\n\n[Retrieved directly from English Guitar Knowledge Base]"


def get_llm():
    if not config.USE_LLM:
        return NoLLM()

    try:
        provider = config.LLM_PROVIDER
        if provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                return NoLLM()
        elif provider == "openai":
            if not os.getenv("OPENAI_API_KEY"):
                return NoLLM()
        return LLM()
    except Exception:
        return NoLLM()


class Generator:
    def __init__(self, llm):
        self.llm = llm

    def generate(self, question: str, chunks: list, history: str = ""):
        is_real_llm = isinstance(self.llm, LLM)
        
        # If NoLLM mode and no chunks, return fallback
        if not is_real_llm and not chunks:
            return {
                "answer": config.NO_CONTEXT_MESSAGE,
                "sources": [],
                "no_context": True,
                "llm_used": False,
                "model_name": "Direct Retrieval (NoLLM)"
            }

        messages = build_messages(question, chunks, history)

        try:
            answer = self.llm.chat(messages)
        except Exception as e:
            if chunks:
                top_c = chunks[0]
                answer = f"[{top_c.get('category', 'Guitar')}] {top_c.get('answer', '')}"
            else:
                answer = f"I could not retrieve information for this query. ({e})"

        if config.DISCLAIMER and config.DISCLAIMER not in answer and is_real_llm:
            answer = f"{answer}\n\n{config.DISCLAIMER}"

        return {
            "answer": answer.strip(),
            "sources": self.build_sources(chunks) if chunks else [],
            "no_context": False if (chunks or is_real_llm) else True,
            "llm_used": is_real_llm,
            "model_name": getattr(self.llm, "model", "Gemini AI" if is_real_llm else "Direct Retrieval (NoLLM)")
        }

    def build_sources(self, chunks: list):
        sources = []
        for i, chunk in enumerate(chunks, start=1):
            ans = chunk.get("answer", "")
            txt = chunk.get("text", "")
            content = ans if ans else txt
            sources.append({
                "n": i,
                "chunk_id": chunk["chunk_id"],
                "category": chunk.get("category", ""),
                "question": chunk.get("question", ""),
                "answer": ans,
                "text": txt,
                "content": content,
                "line_no": chunk.get("line_no", 0),
                "score": round(float(chunk["score"]), 4) if "score" in chunk else 0.95,
            })
        return sources
