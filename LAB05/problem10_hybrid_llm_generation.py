# -*- coding: utf-8 -*-
"""
Problem 10: Raw Top-K Retrieval vs LLM Generation & Hybrid Knowledge Mode
Demonstrates the user's primary breakthrough in the Guitar RAG project:
1. Failure of pure retrieval without LLM: rigid pattern dump of raw chunks without formatting or explanation.
2. Cross-lingual generation: English KB synthesized into fluent, step-by-step Thai explanations.
3. Hybrid Mode: Answering strictly grounded queries from the Guitar KB with citations, while
   smoothly handling general music theory and conversational questions.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from data_loader import load_guitar_kb

DOCS = load_guitar_kb()


def retrieve_top_k(query, docs=DOCS, top_k=2):
    """Retrieves top-k documents matching query tokens."""
    tokens = set(query.lower().split())
    scored = []
    for d in docs:
        score = sum(3 if t in d["question"].lower() else 1 for t in tokens if t in d["text"].lower())
        if score > 0:
            scored.append((score, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_k]]


def mode_without_llm(query, context):
    """
    Simulates the system without an LLM (Pattern Dump):
    Dumps raw, disconnected chunk patterns directly from the database.
    """
    if not context:
        return "[SYSTEM ERROR]: No matching top-k chunks found in database."

    output = ["[RAW RETRIEVAL DUMP (No LLM Synthesis - Direct Snippet)]"]
    for i, doc in enumerate(context, 1):
        output.append(f"  --- Chunk Result #{i} (ID: {doc['id']}) ---")
        output.append(f"  Category : {doc['category']}")
        output.append(f"  Content  : {doc['answer']}")
    return "\n".join(output)


def mode_with_llm_hybrid(query, context, query_type="kb_grounded"):
    """
    Simulates the system with LLM API (Gemini / OpenAI):
    - Synthesizes English chunks into clear, pedagogical Thai explanations.
    - Formats chord fingering with clean steps and visual fret cues.
    - Operates in Hybrid Mode: blends domain KB with general conversational assistance.
    """
    if query_type == "kb_grounded" and context:
        best_doc = context[0]
        if "f (f major)" in best_doc["question"].lower():
            return f"""[LLM SYNTHESIZED RESPONSE WITH CITATIONS]
คำแนะนำวิธีจับคอร์ด F Major (ฉบับมือใหม่ & การฝึกคอร์ดทาบ)
(สืบค้นและอ้างอิงจากฐานข้อมูลความรู้กีตาร์ [Doc ID: #{best_doc['id']}])

โครงสร้างคอร์ด: F Major ประกอบด้วยโน้ต F - A - C (Major Triad)

ตารางตำแหน่งการวางนิ้ว (Fret Pattern: 1-3-3-2-1-1):
  - สาย 6 (E ต่ำ) : เฟรต 1 -- นิ้วชี้ (ทาบทุกสาย)
  - สาย 5 (A)     : เฟรต 3 -- นิ้วนาง
  - สาย 4 (D)     : เฟรต 3 -- นิ้วก้อย
  - สาย 3 (G)     : เฟรต 2 -- นิ้วกลาง
  - สาย 2 (B)     : เฟรต 1 -- นิ้วชี้ (ส่วนหนึ่งของการทาบ)
  - สาย 1 (E สูง) : เฟรต 1 -- นิ้วชี้ (ส่วนหนึ่งของการทาบ)

เทคนิคแก้ปัญหาสายบอด:
  1. ให้เอียงนิ้วชี้ใช้ด้านข้างของนิ้วกดสายเล็กน้อย จะได้เนื้อกระดูกที่แข็งกว่า
  2. วางนิ้วชี้ให้ชิดสันเฟรตเหล็กมากที่สุด จะใช้แรงกดน้อยลง 50%
  3. ดันข้อศอกซ้ายเข้าหาลำตัวเล็กน้อยเพื่อสร้างแรงงัดธรรมชาติโดยไม่ต้องบีบข้อมือ

[Provenance / Citation]: Guitar Knowledge Base - Chords Section Line #45"""

        elif "action" in best_doc["question"].lower():
            return f"""[LLM SYNTHESIZED RESPONSE WITH CITATIONS]
วิธีตรวจสอบและแก้ไขสายกีตาร์ที่สูงเกินไป (High Action Setup Guide)
(สืบค้นและอ้างอิงจากคลังความรู้ช่างกีตาร์ [Doc ID: #{best_doc['id']}])

ความสูงของสาย (Action) มาตรฐานวัดที่เฟรต 12:
  - กีตาร์ไฟฟ้า : สาย 6 สูงประมาณ 1.5 - 2.0 mm, สาย 1 ประมาณ 1.0 - 1.5 mm
  - กีตาร์โปร่ง : สาย 6 สูงประมาณ 2.0 - 2.5 mm, สาย 1 ประมาณ 1.5 - 2.0 mm

ขั้นตอนการแก้ไข:
  1. ตรวจสอบความโค้งของคอกีตาร์ (Truss Rod) ขันตามเข็มนาฬิกาหากคอแอ่นไปข้างหน้า
  2. ปรับลดความสูงของ Saddle (หย่องหลัง)
  3. ตรวจสอบร่อง Nut (หย่องบน) ให้พอดี

[Provenance / Citation]: Guitar Maintenance & Setup Guide"""

        else:
            return f"""[LLM SYNTHESIZED RESPONSE]
{best_doc['answer']}
(อ้างอิงจาก Doc ID: #{best_doc['id']})"""

    elif query_type == "conversational_hybrid":
        return """[CONVERSATIONAL HYBRID AI MODE (Open Domain Music Advice)]
คำแนะนำสำหรับมือใหม่ฝึกเปลี่ยนคอร์ดวงกว้าง (คอร์ดวนยอดฮิต: C - G - Am - F):

เพลงที่แนะนำสำหรับฝึก:
  1. 'Let It Be' - The Beatles (จังหวะปานกลาง เปลี่ยนคอร์ดลงจังหวะหนึ่งชัดเจน)
  2. 'ยิ้ม' - Scrubb (จังหวะฟังสบาย คอร์ดวนต่อเนื่อง)
  3. 'Stand By Me' - Ben E. King (ฝึกการเคาะจังหวะดีดลงสม่ำเสมอ)

คำแนะนำเพิ่มเติม:
  หากยังกดคอร์ด F ทาบเต็มตัวไม่ทัน สามารถใช้คอร์ด Fmaj7 (xx3210) หรือ F Easy Form (xx3211) แทนชั่วคราวได้ครับ"""


def run():
    print("=" * 80)
    print("PROBLEM 10: Raw Top-K Retrieval vs LLM Generation & Hybrid Knowledge Mode")
    print("Pipeline Stage: Generation & Multi-turn Conversational Stage")
    print("=" * 80)

    scenarios = [
        {
            "id": 1,
            "label": "Specific Guitar Question (Thai Query -> English KB)",
            "query": "how do you play f major chord guitar",
            "type": "kb_grounded"
        },
        {
            "id": 2,
            "label": "Conversational / Hybrid Question (Open Domain Music Advice)",
            "query": "ช่วยแนะนำเพลงง่ายๆ สำหรับฝึกเปลี่ยนคอร์ด C G Am F หน่อยครับ",
            "type": "conversational_hybrid"
        }
    ]

    for sc in scenarios:
        print(f"\n[SCENARIO {sc['id']}/2] {sc['label']}")
        print("-" * 80)
        print(f"User Query : \"{sc['query']}\"")
        ctx = retrieve_top_k(sc["query"], DOCS, top_k=1)

        print("\n--- [MODE 1] WITHOUT LLM (Raw Top-K Retrieval Dump) ---")
        print(mode_without_llm(sc["query"], ctx))

        print("\n--- [MODE 2 & 3] WITH LLM GENERATOR & HYBRID MODE ---")
        print(mode_with_llm_hybrid(sc["query"], ctx, query_type=sc["type"]))
        print("-" * 80)

    print("\n" + "=" * 80)
    print("ANALYSIS & RESOLUTION:")
    print("  [Root Cause] : การไม่มี LLM ทำให้คำตอบเป็นเพียงการยก Chunk ดิบๆ มาแปะต่อกัน (Pattern Dump)")
    print("                 ไม่มีการสังเคราะห์ขั้นตอน ไม่สามารถตอบเป็นภาษาไทย และไม่สามารถตอบเรื่องทั่วไปได้")
    print("  [Solution]   : เชื่อมต่อ LLM API สังเคราะห์ภาษาไทย จัดฟอร์แมต Markdown แนบ Citation [Doc ID]")
    print("                 และเปิดโหมด Hybrid ตอบคำถามทั่วไปได้อย่างเป็นธรรมชาติ")
    print("  [Code Trace] : โหมดไม่ใช้ LLM : LAB04/RAG-Guitar/src/generator.py (class NoLLM, บรรทัด 40-52)")
    print("                 โหมดใช้ LLM API: LAB04/RAG-Guitar/src/generator.py (class LLM, บรรทัด 11-38)")
    print("                 System Prompt  : LAB04/RAG-Guitar/src/prompt_templates.py (GUITAR_SYSTEM_PROMPT)")
    print("=" * 80)


if __name__ == "__main__":
    run()
