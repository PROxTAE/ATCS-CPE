# -*- coding: utf-8 -*-
"""
Problem 07: Faithfulness & Critical Parameter Distortion in Guitar Generation
Demonstrates how retrieval can be 100% accurate, but an unconstrained LLM generator
subtly mutates critical musical specs (e.g. tuning the wrong string, modifying fret numbers,
or altering action measurements), leading to broken strings or harmonic cacophony.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import re
from data_loader import load_guitar_kb

DOCS = load_guitar_kb()


def find_target_doc():
    """Finds the guitar action and setup specification document."""
    for d in DOCS:
        if "action" in d["question"].lower() and "string height" in d["question"].lower():
            return d
    return DOCS[0]


def unfaithful_generator(context):
    """
    Simulated generation error:
    The LLM paraphrases the context but accidentally distorts critical numbers
    (e.g., changing 2.0mm to 2.0 inches, or changing 12th fret to 1st fret).
    """
    bad = context.replace("2.0mm", "2.0 inches (50 mm)")
    bad = bad.replace("1.5mm", "1.5 inches (38 mm)")
    bad = bad.replace("12th fret", "1st fret")
    return bad


def faithful_generator(context):
    """Grounded generator maintaining strict factual fidelity to retrieved context."""
    return context


def verify_faithfulness(ground_truth, generated):
    """
    Rule-based Faithfulness Guardrail:
    Extracts numerical measurements and critical tokens to check for hallucinated drift.
    """
    truth_numbers = set(re.findall(r"\b\d+(?:\.\d+)?(?:mm|cm|inches|th|st|nd|rd)?\b", ground_truth))
    gen_numbers = set(re.findall(r"\b\d+(?:\.\d+)?(?:mm|cm|inches|th|st|nd|rd)?\b", generated))

    mismatches = gen_numbers - truth_numbers
    if mismatches:
        return False, f"[FAIL: CRITICAL SPEC DISTORTION DETECTED: {mismatches} not in source!]"
    return True, "[PASS: 100% FAITHFUL - All measurements match retrieved source exactly]"


def run():
    print("=" * 80)
    print("PROBLEM 07: Faithfulness & Technical Distortion in Guitar Spec Generation")
    print("Pipeline Stage: Generation Post-processing & Fact Checking Stage")
    print("=" * 80)

    doc = find_target_doc()
    context = doc["answer"]

    print(f"Target Query : \"{doc['question']}\"")
    print("\n[GROUND TRUTH CONTEXT FROM KNOWLEDGE BASE]:")
    print(f"  \"{context}\"")

    # 1. Distorted Generation
    bad_output = unfaithful_generator(context)
    is_faithful_bad, bad_msg = verify_faithfulness(context, bad_output)

    print("\n[EXPERIMENT A] Unconstrained Generation (Alters Units & Frets):")
    print(f"  Generated Text : \"{bad_output}\"")
    print(f"  Audit Status   : {bad_msg}")

    # 2. Faithful Grounded Generation
    good_output = faithful_generator(context)
    is_faithful_good, good_msg = verify_faithfulness(context, good_output)

    print("\n[EXPERIMENT B] Grounded Faithful Generation (Enforces Numeric Invariance):")
    print(f"  Generated Text : \"{good_output}\"")
    print(f"  Audit Status   : {good_msg}")

    print("\n" + "=" * 80)
    print("ANALYSIS & RESOLUTION:")
    print("  [Root Cause] : โมเดล LLM ในระหว่างการ Paraphrase สับสนหน่วยวัด (mm เป็น inches)")
    print("                 ในงานเซ็ตอัพกีตาร์ ความคลาดเคลื่อนระดับมิลลิเมตรทำให้เครื่องดนตรีพังได้")
    print("  [Solution]   : 1. ใส่ Prompt Guardrail กำหนด Numeric Invariance ห้ามแปลงตัวเลขเด็ดขาด")
    print("                 2. มี Automated Fact Verification ตรวจสอบตัวเลขก่อนส่งให้ผู้ใช้")
    print("  [Code Trace] : LAB04/RAG-Guitar/evaluation/eval_generation.py (evaluate_faithfulness)")
    print("                 LAB04/RAG-Guitar/src/prompt_templates.py")
    print("=" * 80)


if __name__ == "__main__":
    run()
