# -*- coding: utf-8 -*-
"""
main.py - Main Runner for LAB05: Guitar RAG System Development II
Demonstrates 10 core problem scenarios and solutions encountered in the Guitar RAG system.

Usage:
    python main.py          # Interactive Menu
    python main.py <1-10>   # Run specific problem directly (e.g. python main.py 2)
    python main.py all      # Run all problems sequentially
"""

import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from problem01_hallucination import run as problem01
from problem02_vocab_crosslingual import run as problem02
from problem03_chord_data_quality import run as problem03
from problem04_chunking_guitar import run as problem04
from problem05_metadata_filtering import run as problem05
from problem06_reranking import run as problem06
from problem07_faithfulness import run as problem07
from problem08_config import run as problem08
from problem09_evaluation import run as problem09
from problem10_hybrid_llm_generation import run as problem10

PROBLEMS = {
    1: ("Hallucination & Scope", "Out-of-scope queries & preventing fabricated chords", problem01),
    2: ("Vocab & Cross-Lingual", "Thai query against English Guitar KB & LLM translation", problem02),
    3: ("Chord Data Quality", "Inconsistent chord notations (Cmaj7/C^7/CΔ7) & normalizer", problem03),
    4: ("Chunking & Broken Tabs", "ASCII tablatures torn apart by naive character chunking", problem04),
    5: ("Metadata Filtering", "Stratifying by skill level, nylon vs steel, and tunings", problem05),
    6: ("Polysemy & Re-ranking", "Musical homonyms ('Bridge', 'Pick', 'Scale') & 2nd stage", problem06),
    7: ("Musical Faithfulness", "Factual distortion in critical tuning & action millimeters", problem07),
    8: ("RAG System Config", "Modular pipeline architecture & component matrix", problem08),
    9: ("Quantitative Evaluation", "Hit@k, MRR benchmarks & golden set evaluation", problem09),
    10: ("Top-K vs LLM & Hybrid", "Overcoming raw chunk dumps with LLM & Hybrid chatbot", problem10),
}


def print_banner():
    print("=" * 80)
    print("  LAB05: GUITAR RAG SYSTEM DEVELOPMENT II - PROBLEM SIMULATION SUITE")
    print("  Author: Nithit Manora (Student ID: 116730462042-6)")
    print("  Course: Advanced Machine Learning / Deep Learning (CPE)")
    print("  Domain: English Guitar Knowledge Base (500 Q&A) & Hybrid LLM Generator")
    print("=" * 80)


def print_menu():
    print("\nSelect a problem simulation to run:")
    print("-" * 80)
    for num, (title, desc, _) in PROBLEMS.items():
        print(f"  [{num:2d}] {title:<25} : {desc}")
    print("  [all] Run all 10 problem simulations sequentially")
    print("  [ q ] Quit / Exit")
    print("-" * 80)


def run_problem(choice):
    if choice in PROBLEMS:
        title, _, func = PROBLEMS[choice]
        print(f"\n>>> Executing Problem {choice:02d}: {title}...\n")
        func()
        print("\n" + "=" * 80)
    else:
        print(f"[ERROR]: Invalid selection: {choice}")


def run_all():
    print("\n>>> EXECUTING ALL 10 GUITAR RAG SIMULATIONS SEQUENTIALLY...\n")
    for num in sorted(PROBLEMS.keys()):
        run_problem(num)


def main():
    print_banner()

    if len(sys.argv) > 1:
        arg = sys.argv[1].strip().lower()
        if arg == "all":
            run_all()
            return
        elif arg.isdigit():
            choice = int(arg)
            if choice in PROBLEMS:
                run_problem(choice)
                return
            else:
                print(f"[ERROR]: Problem number must be between 1 and {len(PROBLEMS)}")
                return
        else:
            print(f"[NOTICE]: Unknown argument '{arg}'. Starting interactive mode.")

    while True:
        print_menu()
        user_input = input("Enter selection (1-10, all, q): ").strip().lower()
        if user_input in ["q", "quit", "exit"]:
            print("\n[EXIT]: Exiting Guitar RAG Lab 05 Suite.")
            break
        elif user_input == "all":
            run_all()
            break
        elif user_input.isdigit():
            val = int(user_input)
            if val in PROBLEMS:
                run_problem(val)
            else:
                print(f"[ERROR]: Enter a valid number between 1 and {len(PROBLEMS)}.")
        else:
            print("[ERROR]: Invalid command. Enter a number (1-10), 'all', or 'q'.")


if __name__ == "__main__":
    main()
