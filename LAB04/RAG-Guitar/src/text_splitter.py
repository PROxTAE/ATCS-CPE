"""
text_splitter.py - แบ่งเนื้อหาคำตอบยาวๆ ออกเป็น Chunks ย่อย
คงบริบทของหมวดหมู่และคำถามไว้ในทุก Chunk เพื่อเพิ่มความแม่นยำในการค้นหา
"""


def split_text(text: str, chunk_size: int, chunk_overlap: int):
    """
    ตัดข้อความออกเป็นส่วนๆ โดยพยายามไม่ตัดกลางบรรทัดหรือกลางย่อหน้า
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    lines = text.split("\n")
    current_chunk = []
    current_length = 0

    for line in lines:
        line_len = len(line) + 1
        if current_length + line_len > chunk_size and current_chunk:
            chunk_str = "\n".join(current_chunk).strip()
            if chunk_str:
                chunks.append(chunk_str)
            # รักษา overlap จากบรรทัดหลังๆ
            overlap_lines = []
            overlap_len = 0
            for l in reversed(current_chunk):
                if overlap_len + len(l) + 1 <= chunk_overlap:
                    overlap_lines.insert(0, l)
                    overlap_len += len(l) + 1
                else:
                    break
            current_chunk = overlap_lines
            current_length = sum(len(l) + 1 for l in current_chunk)

        current_chunk.append(line)
        current_length += line_len

    if current_chunk:
        chunk_str = "\n".join(current_chunk).strip()
        if chunk_str:
            chunks.append(chunk_str)

    return chunks if chunks else [text]


def build_chunks(records, chunk_size=450, chunk_overlap=60):
    """
    สร้าง list ของ Chunk พร้อมแนบ Metadata ละเอียด
    """
    all_chunks = []
    chunk_id = 0

    for record in records:
        answer = record["answer"]
        text_parts = split_text(answer, chunk_size, chunk_overlap)
        total_parts = len(text_parts)

        for idx, part in enumerate(text_parts):
            # Rich context representation สำหรับ Embedding & Retrieval
            retrieval_text = f"[{record['category']}] คำถาม: {record['question']} คำตอบ: {part}"

            all_chunks.append({
                "chunk_id": chunk_id,
                "record_id": record["id"],
                "category": record["category"],
                "question": record["question"],
                "answer": part,
                "text": retrieval_text,
                "line_no": record["line_no"],
                "chunk_index": idx,
                "total_chunks": total_parts,
            })
            chunk_id += 1

    return all_chunks
