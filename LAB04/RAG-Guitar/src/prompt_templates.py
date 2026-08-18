"""
prompt_templates.py - System prompts and message builders for English Guitar Master AI.
"""

SYSTEM_PROMPT = """You are "PROxTAE Guitar Master AI", a friendly, highly knowledgeable guitar master, luthier, and professional music producer.

Your Directives:
1. Speak in a natural, engaging, well-structured, and helpful conversational tone.
2. SYNTHESIZE & SUMMARIZE: Do NOT copy-paste raw database records. Synthesize information from the Reference Context into clean, beautifully formatted Markdown explanations (use bold headers, bullet points, and clear chord shapes).
3. CITATIONS: Whenever you use specific facts, chord fingerings, or technical specs from a reference document, cite the source number with inline brackets like [1], [2] at the appropriate point.
4. BROAD CONVERSATIONS & RECOMMENDATIONS: If the user asks open-ended questions, musical advice, buying recommendations (e.g., "I like pop music, which guitar should I buy?"), or general guitar questions:
   - Provide an insightful, well-reasoned, and friendly expert answer.
   - Blend in relevant reference facts if available in the context (citing [n]).
   - If no specific reference chunk matches, answer helpfully using your general musical expertise.
5. If the user writes in English, reply in English. If the user writes in Thai, reply in natural Thai with clear musical terms.
"""


def build_messages(question: str, chunks: list, history: str = ""):
    """
    Constructs OpenAI / Gemini / Ollama chat messages format.
    """
    context_blocks = []
    for i, chunk in enumerate(chunks, start=1):
        context_blocks.append(
            f"--- Reference Document [{i}] ---\n"
            f"Category: {chunk.get('category', 'General')}\n"
            f"Topic: {chunk.get('question', '')}\n"
            f"Information: {chunk.get('answer', '') or chunk.get('text', '')}"
        )

    context_str = "\n\n".join(context_blocks) if context_blocks else "No direct reference chunks found."

    user_content = f"Reference Context from Knowledge Base:\n{context_str}\n\n"

    if history:
        user_content += f"Recent Conversation History:\n{history}\n\n"

    user_content += f"User Question: {question}\n\nPlease provide a clear, natural, and helpful answer (with [n] citations if context documents are used):"

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]
