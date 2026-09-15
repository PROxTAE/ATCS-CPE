# -*- coding: utf-8 -*-
"""
data_loader.py - Shared Guitar Knowledge Base Loader for LAB05
Parses guitar_knowledge_base.txt into structured Q&A records with domain metadata.
"""

import os
import re

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "guitar_knowledge_base.txt")
_CATEGORY_RE = re.compile(r"\[Category:\s*(.+?)\]")


def load_guitar_kb(path=DATA_PATH):
    """
    Loads and parses the guitar knowledge base.
    Returns:
        List of dicts:
            id (int): sequential unique ID
            category (str): Guitar topic category
            question (str): The query or question
            answer (str): The detailed answer/explanation
            text (str): Combined question and answer
            difficulty (str): 'Beginner', 'Intermediate', or 'Advanced'
            instrument (str): 'Acoustic', 'Electric', 'Classical', or 'Universal'
            has_chord_voicings (bool): True if content involves chords / fret fingerings
    """
    if not os.path.exists(path):
        # Fallback to LAB04 path if run from a different location
        fallback_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "LAB04",
            "RAG-Guitar",
            "data",
            "guitar_knowledge_base.txt"
        )
        if os.path.exists(fallback_path):
            path = fallback_path
        else:
            raise FileNotFoundError(f"Knowledge base not found at {path}")

    with open(path, "r", encoding="utf-8") as f:
        raw_content = f.read()

    entries = []
    # Split by double newline or block patterns
    blocks = re.split(r"\n\s*\n", raw_content)

    for block in blocks:
        block = block.strip()
        if not block or block.startswith("#"):
            continue

        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if len(lines) < 2:
            continue

        category = "General Guitar Knowledge"
        q_text = None
        a_lines = []

        for line in lines:
            if line.startswith("[Category:"):
                m = _CATEGORY_RE.match(line)
                if m:
                    category = m.group(1).strip()
            elif line.startswith("Q:"):
                q_text = line[2:].strip()
            elif line.startswith("A:"):
                a_lines.append(line[2:].strip())
            elif q_text is not None:
                # Continuation of the answer
                a_lines.append(line)

        if not q_text or not a_lines:
            continue

        answer = " ".join(a_lines).strip()
        full_text = f"{q_text} {answer}"

        # Inferred Domain Metadata
        lower_text = full_text.lower()
        if any(w in lower_text for w in ["beginner", "first guitar", "basic chord", "open chord", "holding the pick", "string name"]):
            difficulty = "Beginner"
        elif any(w in lower_text for w in ["sweep picking", "drop-2", "diminished 7th", "modes", "phrygian", "tapping", "jazz"]):
            difficulty = "Advanced"
        else:
            difficulty = "Intermediate"

        if "acoustic" in lower_text or "dreadnought" in lower_text or "nylon" in lower_text:
            instrument = "Acoustic"
        elif "electric" in lower_text or "pickup" in lower_text or "humbucker" in lower_text or "amplifier" in lower_text:
            instrument = "Electric"
        elif "classical" in lower_text or "flamenco" in lower_text:
            instrument = "Classical"
        else:
            instrument = "Universal"

        has_chord_voicings = any(ch in lower_text for ch in ["chord", "voicing", "fret", "finger", "barre", "tab", "e|", "b|"])

        entries.append({
            "id": len(entries),
            "category": category,
            "question": q_text,
            "answer": answer,
            "text": full_text,
            "difficulty": difficulty,
            "instrument": instrument,
            "has_chord_voicings": has_chord_voicings
        })

    return entries


def get_categories(entries=None):
    """Returns sorted list of unique categories."""
    entries = entries if entries is not None else load_guitar_kb()
    return sorted(set(e["category"] for e in entries))


if __name__ == "__main__":
    data = load_guitar_kb()
    print(f"Loaded {len(data)} Guitar Q&A entries.")
    print("Categories found:", len(get_categories(data)))
    for c in get_categories(data):
        count = sum(1 for d in data if d["category"] == c)
        print(f" - {c}: {count} records")
    print(f"Sample Entry #0:\n Question: {data[0]['question']}\n Difficulty: {data[0]['difficulty']} | Instrument: {data[0]['instrument']}")
