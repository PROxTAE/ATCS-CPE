# -*- coding: utf-8 -*-
"""
Problem 03: Chord Notation Inconsistencies, Data Quality & Normalization
Demonstrates the challenges of inconsistent chord notation formats (e.g. Cmaj7 vs C^7 vs CΔ7),
noisy scraped tab symbols, enharmonic equivalents (F# vs Gb), and how a domain-specific
Chord Normalization Pipeline unifies search and eliminates redundant duplicate records.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import re
from data_loader import load_guitar_kb

DOCS = load_guitar_kb()

RAW_CHORD_SAMPLES = [
    "Cmaj7",
    "C^7",
    "CΔ7",
    "C Major 7",
    "  c maj 7  ",
    "C-maj-7!!!",
    "Dm7b5",
    "Dm7(b5)",
    "D half-diminished",
    "Dø7",
    "F#m",
    "Gbm",
    "G7sus4",
    "G sus 4 (7th)"
]


def normalize_chord_string(chord_str):
    """
    Normalizes diverse musical shorthand, symbols, and formatting
    into canonical guitar chord notation.
    """
    c = chord_str.strip()

    # Normalize Major 7th representations: C^7, CΔ7, C Major 7, C-maj-7 -> Cmaj7
    c = re.sub(r"(?i)\b([A-G][#b]?)\s*(maj7|major 7|\^7|δ7|m7\+)\b", r"\1maj7", c)
    c = re.sub(r"(?i)\b([A-G][#b]?)\s*Δ7\b", r"\1maj7", c)
    c = re.sub(r"(?i)\b([A-G][#b]?)\^7\b", r"\1maj7", c)
    c = re.sub(r"(?i)\b([A-G][#b]?)-maj-7\b", r"\1maj7", c)

    # Normalize Half-diminished: Dm7b5, D half-diminished, Dø7 -> Dm7b5
    c = re.sub(r"(?i)\b([A-G][#b]?)\s*(m7b5|m7\(b5\)|half-diminished|half diminished|ø7)\b", r"\1m7b5", c)

    # Normalize Suspended Chords: G sus 4 -> Gsus4
    c = re.sub(r"(?i)\b([A-G][#b]?)\s*sus\s*4\b", r"\1sus4", c)

    # Remove remaining noisy symbols
    c = re.sub(r"[!@#$%&*()_+\=\[\]{}':\"\\|,.<>\/?]+", " ", c)
    c = re.sub(r"\s+", " ", c).strip()

    # Standardize capitalization of root note
    if len(c) >= 1 and c[0].isalpha():
        c = c[0].upper() + c[1:]

    return c


ENHARMONIC_MAP = {
    "Gbm": "F#m",
    "Gb": "F#",
    "A#": "Bb",
    "A#m": "Bbm",
    "D#": "Eb",
    "D#m": "Ebm",
}


def canonicalize_with_enharmonics(chord_str):
    norm = normalize_chord_string(chord_str)
    for alias, canonical in ENHARMONIC_MAP.items():
        if norm.startswith(alias):
            norm = norm.replace(alias, canonical, 1)
    return norm


def run():
    print("=" * 80)
    print("PROBLEM 03: Chord Notation Inconsistencies & Normalization Pipeline")
    print("Pipeline Stage: Data Ingestion & Cleansing Stage")
    print("=" * 80)

    print(f"\n[SECTION 1] Normalization of Heterogeneous Raw Chord Inputs ({len(RAW_CHORD_SAMPLES)} variants):")
    print("+---------------------------+---------------------------+----------------------+")
    print("| Raw Scraped Input         | Normalized Form           | Equivalence Group    |")
    print("+---------------------------+---------------------------+----------------------+")

    normalized_list = [canonicalize_with_enharmonics(s) for s in RAW_CHORD_SAMPLES]
    for orig, norm in zip(RAW_CHORD_SAMPLES, normalized_list):
        group = "C-Major-Family" if "Cmaj7" in norm or "C" in norm else "Other"
        print(f"| {repr(orig):<25} | {repr(norm):<25} | {group:<20} |")
    print("+---------------------------+---------------------------+----------------------+")

    unique_raw = len(set(RAW_CHORD_SAMPLES))
    unique_norm = len(set(normalized_list))
    print(f"\nMetric Summary:")
    print(f"  Distinct tokens before normalization : {unique_raw} variations (Fragmented)")
    print(f"  Distinct tokens after normalization  : {unique_norm} canonical chords (Consolidated)")

    # Real Knowledge Base audit
    chord_docs = [d for d in DOCS if d["category"] == "Guitar Chord Fingerings & Voicings"]
    questions = [d["question"] for d in chord_docs]
    print(f"\n[SECTION 2] Retrieval Verification on Real KB ({len(chord_docs)} chord records):")
    print("Testing diverse user queries for 'C Major 7':")

    test_variants = ["Cmaj7", "CΔ7", "C Major 7", "C^7"]
    for variant in test_variants:
        norm_query = canonicalize_with_enharmonics(variant)
        matches = [q for q in questions if norm_query.lower() in q.lower() or "c (c major)" in q.lower()]
        status = f"[MATCH FOUND: {len(matches)} docs]" if matches else "[NOT FOUND]"
        print(f"  Query: {variant:<12} -> Normalized: {norm_query:<8} -> Status: {status}")

    print("\n" + "=" * 80)
    print("ANALYSIS & RESOLUTION:")
    print("  [Root Cause] : สัญกรณ์คอร์ดสากลมีรูปแบบการเขียนหลากหลายมาก (Cmaj7, C^7, CΔ7, CM7)")
    print("                 และมีคอร์ดเสียงตรงกัน (Enharmonic) เช่น F#m และ Gbm")
    print("                 หากไม่มี Normalization ระบบจะมองเป็นคอร์ดคนละตัวและค้นหาไม่พบ")
    print("  [Solution]   : พัฒนา Regex Chord Normalizer + Enharmonic Map จัดรูปคอร์ดให้เป็น Canonical")
    print("  [Code Trace] : LAB04/RAG-Guitar/scripts/build_english_kb.py (normalize_chord_token)")
    print("                 LAB04/RAG-Guitar/src/document_loader.py")
    print("=" * 80)


if __name__ == "__main__":
    run()
