


"""
Load data from sex_q_a.txt and convert it into a list of dictionaries.
The original file format is:
    หมวด: category_name]
    Q: question_text
    A: answer_text
    (blank line separates each Q&A pair)

Since the actual data is in .txt format, we use "line_no" instead of page numbers
to reference the original location, so that we can still refer to the source text.
"""

import os

def load_qa_file(file_path):
    """
    read the .txt file and split it into individual question-answer pairs

    returns a list of dictionaries, each with the following keys:
        - id: the index of the question-answer pair (starting from 0)
        - category: the category to which the pair belongs
        - question: the question text
        - answer: the answer text
        - line_no: the line number of the "Q:" in the original file (used instead of page numbers)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    records = []
    current_category = "Unspecified Category"
    
    current_question = None
    current_answer_lines = []
    current_line_no = None
    parsing_answer = False

    def save_current_record():
        nonlocal current_question, current_answer_lines, current_line_no, parsing_answer
        if current_question is not None:
            answer = "\n".join(current_answer_lines).strip()
            records.append({
                "id": len(records),
                "category": current_category,
                "question": current_question,
                "answer": answer,
                "line_no": current_line_no,
            })
            current_question = None
            current_answer_lines = []
            current_line_no = None
            parsing_answer = False

    for line_no, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()

        if line.startswith("#"):
            continue

        if line.startswith("[หมวด"):
            save_current_record()
            current_category = line.strip("[]").replace("หมวด:", "").strip()
            continue

        if line.startswith("Q:"):
            save_current_record()
            current_question = line[len("Q:"):].strip()
            current_line_no = line_no
            parsing_answer = False
            continue

        if line.startswith("A:"):
            parsing_answer = True
            current_answer_lines.append(line[len("A:"):].strip())
            continue

        if parsing_answer:
            if line == "":
                save_current_record()
            else:
                current_answer_lines.append(raw_line.rstrip("\r\n"))

    save_current_record()
    return records





