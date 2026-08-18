"""
document_loader.py - Loads guitar knowledge base file and parses into Q&A records.
Supports single-line and multi-line structured answers (such as chord charts).
"""

import os


def load_qa_file(file_path: str):
    """
    Parses the guitar knowledge base text file into a list of dictionaries:
    - id: index
    - category: topic category
    - question: question string
    - answer: answer string (multi-line preserved)
    - line_no: line number in source file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    records = []
    category = "General Guitar"
    current_q = None
    current_q_line = None
    answer_lines = []

    def commit_record():
        nonlocal current_q, current_q_line, answer_lines
        if current_q and answer_lines:
            ans_text = "\n".join(answer_lines).strip()
            records.append({
                "id": len(records),
                "category": category,
                "question": current_q,
                "answer": ans_text,
                "line_no": current_q_line,
            })
        current_q = None
        current_q_line = None
        answer_lines = []

    for line_no, raw_line in enumerate(raw_lines, start=1):
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()

        if not stripped or stripped.startswith("#") or stripped.startswith("="):
            continue

        if stripped.startswith("[Category:") or stripped.startswith("[หมวด:"):
            commit_record()
            category = stripped.strip("[]").replace("Category:", "").replace("หมวด:", "").strip()
        elif stripped.startswith("Q:"):
            commit_record()
            current_q = stripped[2:].strip()
            current_q_line = line_no
        elif stripped.startswith("A:"):
            answer_lines.append(stripped[2:].strip())
        elif current_q is not None and answer_lines:
            # Multi-line continuation
            answer_lines.append(stripped)

    # Commit any remaining record
    commit_record()

    return records
