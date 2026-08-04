import os
import json
import sys
from pypdf import PdfReader

# Ensure stdout uses UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "guitar_rag_dataset.txt")

CHORDS_JSON = os.path.join(DATA_DIR, "chord-collection-master", "chords.json")
PDF_DIR = os.path.join(DATA_DIR, "guitar-course-pdf")
PDF_FILE = os.path.join(PDF_DIR, "manual_beginner_guitar.pdf")

def parse_chords():
    print("Parsing chords.json...")
    if not os.path.exists(CHORDS_JSON):
        print(f"Error: {CHORDS_JSON} not found!")
        return []

    with open(CHORDS_JSON, "r", encoding="utf-8") as f:
        chords_data = json.load(f)

    records = []
    # We want to extract common chords to keep it lightweight
    common_suffixes = ["", "m", "7", "maj7", "m7", "sus4", "sus2", "add9", "6"]
    roots = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    allowed_chords = {f"{root}{suffix}" for root in roots for suffix in common_suffixes}

    count = 0
    for chord_name, variations in chords_data.items():
        if chord_name not in allowed_chords:
            continue
        
        # Take the first variation (standard position)
        if not variations:
            continue
        var = variations[0]
        positions = var.get("positions", [])
        if len(positions) < 6:
            continue
            
        strings_desc = []
        string_names = ["สาย 6 (E ต่ำ)", "สาย 5 (A)", "สาย 4 (D)", "สาย 3 (G)", "สาย 2 (B)", "สาย 1 (E สูง)"]
        for idx, pos in enumerate(positions):
            if pos == "x":
                strings_desc.append(f"{string_names[idx]}: อุดสาย/ไม่ต้องดีด (x)")
            elif pos == "0":
                strings_desc.append(f"{string_names[idx]}: สายเปล่า (0)")
            else:
                strings_desc.append(f"{string_names[idx]}: กดเฟรต {pos}")

        q_a = (
            "[หมวด: วิธีจับคอร์ดกีตาร์]\n"
            f"Q: วิธีจับคอร์ด {chord_name} ทำอย่างไร\n"
            f"A: วิธีจับคอร์ด {chord_name} มีลักษณะการวางนิ้วและดีดสายดังนี้:\n"
            + "\n".join([f"- {s}" for s in strings_desc]) + "\n"
        )
        records.append(q_a)
        count += 1

    print(f"Extracted {count} chord Q&A pairs.")
    return records

def parse_pdf():
    print("Parsing manual_beginner_guitar.pdf...")
    if not os.path.exists(PDF_FILE):
        print(f"Error: {PDF_FILE} not found!")
        return []

    records = []
    try:
        reader = PdfReader(PDF_FILE)
        max_pages = min(len(reader.pages), 20)
        for page_num in range(max_pages):
            text = reader.pages[page_num].extract_text()
            if not text or len(text.strip()) < 100:
                continue
            
            clean_text = " ".join(text.split())
            q_a = (
                "[หมวด: บทเรียนและเทคนิคการฝึกกีตาร์สำหรับมือใหม่]\n"
                f"Q: คู่มือการฝึกกีตาร์เบื้องต้น หน้าที่ {page_num + 1} อธิบายเรื่องอะไรบ้าง\n"
                f"A: ข้อมูลเนื้อหาในคู่มือหน้า {page_num + 1} มีดังนี้:\n{clean_text}\n"
            )
            records.append(q_a)
    except Exception as e:
        print(f"Error reading PDF: {e}")

    print(f"Extracted {len(records)} page contents from PDF.")
    return records

def main():
    print("=== Processing Guitar RAG Dataset ===")
    chord_records = parse_chords()
    pdf_records = parse_pdf()
    
    all_records = chord_records + pdf_records
    
    if not all_records:
        print("No records generated!")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(all_records))

    print(f"Successfully wrote {len(all_records)} items to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
