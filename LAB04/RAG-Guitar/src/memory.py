"""
memory.py - Conversation Memory for English multi-turn dialogue.
"""

import config

FOLLOWUP_TRIGGERS = [
    "what about", "and", "how about", "why", "it", "this", "that", "compare",
    "difference between", "how much", "where to buy", "pros and cons", "instead"
]


class ConversationMemory:
    def __init__(self, max_turns=config.MEMORY_MAX_TURNS):
        self.max_turns = max_turns
        self.history = []

    def add_user(self, text: str):
        self.history.append({"role": "user", "content": text.strip()})
        self._trim()

    def add_assistant(self, text: str):
        self.history.append({"role": "assistant", "content": text.strip()})
        self._trim()

    def _trim(self):
        max_messages = self.max_turns * 2
        if len(self.history) > max_messages:
            self.history = self.history[-max_messages:]

    def get_context(self) -> str:
        if not self.history:
            return ""

        formatted = []
        for msg in self.history:
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted.append(f"{role}: {msg['content']}")
        return "\n".join(formatted)

    def is_followup(self, query: str) -> bool:
        if not self.history:
            return False

        q_lower = query.lower()
        if len(q_lower.split()) <= 4:
            return True

        return any(trigger in q_lower for trigger in FOLLOWUP_TRIGGERS)

    def clear(self):
        self.history = []
