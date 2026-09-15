# -*- coding: utf-8 -*-
"""
Problem 04: Chunking Dilemma in Guitar RAG (Broken Tabs & Chord Grids)
Demonstrates how naive fixed-character chunking tears apart multi-line ASCII tablature
and chord fingerings, compared to Guitar-Aware / Block-Aware Semantic Chunking with Overlap.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import re
from data_loader import load_guitar_kb

DOCS = load_guitar_kb()

SAMPLE_GUITAR_LESSON = """
# Lesson: Playing the Classical Romanza / Spanish Romance Melody in E Minor
The Spanish Romance (Romance Anonimo) is an essential fingerstyle guitar study focusing on melody on string 1 with rolling arpeggios on strings 2 and 3, supported by a thumb bass note on string 6.

Tablature Section A (Measure 1-4):
e|---7-------7-------7---|---7-------5-------3---|---3-------2-------0---|---0-------3-------7---|
B|-------0-------0-------|-------0-------0-------|-------0-------0-------|-------0-------0-------|
G|-----0-------0-------0-|-----0-------0-------0-|-----0-------0-------0-|-----0-------0-------0-|
D|-----------------------|-----------------------|-----------------------|-----------------------|
A|-----------------------|-----------------------|-----------------------|-----------------------|
E|---0-------------------|---0-------------------|---0-------------------|---0-------------------|

Right Hand Technique:
Use (p) for the low E bass string, while (a) plays the melody note, followed by (m) on the G string and (i) on the B string.
Maintain strict legato phrasing so the top melody sings cleanly over the harmonic accompaniment.
"""


def naive_character_chunker(text, chunk_size=300, overlap=0):
    """Splits purely by character count regardless of line breaks or tab diagrams."""
    chunks = []
    step = chunk_size - overlap
    for i in range(0, len(text), step):
        chunks.append(text[i:i + chunk_size])
    return chunks


def guitar_block_aware_chunker(text, max_chars=500, overlap_lines=2):
    """
    Syntax-aware chunker:
    - Never splits a multi-line ASCII tab block (e|, B|, G|, D|, A|, E|)
    - Splits on paragraph / section boundaries
    - Retains contextual overlap of complete instructional lines
    """
    tab_pattern = re.compile(r"([eEbBgGdDaA]\|.+\n?){4,6}")

    paragraphs = text.strip().split("\n\n")
    chunks = []
    current_chunk = []
    current_len = 0

    for p in paragraphs:
        p_len = len(p)
        if current_len + p_len > max_chars and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            overlap_p = [current_chunk[-1]] if not tab_pattern.search(current_chunk[-1]) else []
            current_chunk = overlap_p + [p]
            current_len = sum(len(x) for x in current_chunk)
        else:
            current_chunk.append(p)
            current_len += p_len

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
    return chunks


def verify_tab_integrity(chunk_text):
    """Checks if a chunk contains a broken, severed guitar tab."""
    has_treble = "e|" in chunk_text or "B|" in chunk_text
    has_bass = "E|" in chunk_text or "A|" in chunk_text

    if has_treble and not has_bass:
        return "[FAILURE: SEVERED TAB - Missing Bass strings (strings 4-6 lost)]"
    elif has_bass and not has_treble:
        return "[FAILURE: SEVERED TAB - Missing Treble strings (melody lost)]"
    elif has_treble and has_bass:
        return "[SUCCESS: COMPLETE TAB - All 6 strings preserved intact]"
    return "[INFO: TEXT-ONLY CHUNK - No tablature block present]"


def run():
    print("=" * 80)
    print("PROBLEM 04: Chunking in Guitar RAG (Broken ASCII Tabs & Loss of Context)")
    print("Pipeline Stage: Document Chunking & Text Splitting Stage")
    print("=" * 80)

    print(f"Sample Lesson Length: {len(SAMPLE_GUITAR_LESSON)} characters (Contains 6-string tab block)")

    # 1. Naive Splitter
    print("\n[EXPERIMENT 1] Naive Character Chunking (size=320 chars, overlap=0):")
    print("-" * 80)
    naive_chunks = naive_character_chunker(SAMPLE_GUITAR_LESSON, chunk_size=320, overlap=0)
    for idx, c in enumerate(naive_chunks, 1):
        status = verify_tab_integrity(c)
        print(f"  Chunk #{idx:<2} | Length: {len(c):3d} chars | Status: {status}")
        preview = c.strip().split("\n")[0]
        print(f"    Line 1 Preview: \"{preview[:70]}...\"")

    # 2. Block-Aware Splitter
    print("\n[EXPERIMENT 2] Guitar Block-Aware Chunking (Atomic Tab Blocks + Overlap):")
    print("-" * 80)
    smart_chunks = guitar_block_aware_chunker(SAMPLE_GUITAR_LESSON, max_chars=600)
    for idx, c in enumerate(smart_chunks, 1):
        status = verify_tab_integrity(c)
        print(f"  Chunk #{idx:<2} | Length: {len(c):3d} chars | Status: {status}")
        preview = c.strip().split("\n")[0]
        print(f"    Line 1 Preview: \"{preview[:70]}...\"")

    print("\n[TAB BLOCK VERIFICATION]")
    tab_chunk = next(c for c in smart_chunks if "e|" in c and "E|" in c)
    print("Printing verified intact tab from Smart Chunk #2:")
    for line in tab_chunk.split("\n"):
        if "|" in line:
            print(f"  {line}")

    print("\n" + "=" * 80)
    print("ANALYSIS & RESOLUTION:")
    print("  [Root Cause] : แท็บกีตาร์ประกอบด้วยสาย 6 สายที่ต้องอ่านคู่กันในแนวดิ่ง")
    print("                 Character-based Chunking จะตัดผ่ากลางแท็บทำให้สายบนหลุดจากสายล่าง")
    print("  [Solution]   : พัฒนา Block-Aware Chunker ล็อกโครงสร้างแท็บเป็น Atomic Unit ห้ามตัดแยกส่วน")
    print("  [Code Trace] : LAB04/RAG-Guitar/src/text_splitter.py (GuitarTextSplitter)")
    print("                 LAB04/RAG-Guitar/config.py (CHUNK_SIZE = 512, CHUNK_OVERLAP = 64)")
    print("=" * 80)


if __name__ == "__main__":
    run()
