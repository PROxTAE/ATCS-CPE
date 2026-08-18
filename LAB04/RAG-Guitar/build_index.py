"""
build_index.py - สร้าง Vector Database (FAISS) และ BM25 Index สำหรับฐานความรู้กีตาร์
รันไฟล์นี้เมื่อมีการอัปเดตข้อมูลใน data/guitar_knowledge_base.txt หรือเปลี่ยนโมเดล Embedding
"""

import json
import time
import numpy as np

import config
from src import index_meta
from src.document_loader import load_qa_file
from src.embedding_model import EmbeddingModel
from src.hybrid_retriever import build_bm25, save_bm25
from src.text_splitter import build_chunks
from src.vector_store import VectorStore, save_chunk_store


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    print("=" * 60)
    print("🎸 Build Index: Guitar Knowledge Base RAG System")
    print("=" * 60)
    print(f"Source file : {config.SOURCE_FILE}")
    print(f"Model       : {config.EMBEDDING_MODEL_NAME}")
    print(f"Chunk size  : {config.CHUNK_SIZE} (Overlap: {config.CHUNK_OVERLAP})")
    print("-" * 60)

    start_time = time.time()

    # Step 1: โหลดคู่คำถาม-คำตอบทั้งหมด
    print("[1/5] 📥 กำลังอ่านไฟล์ความรู้กีตาร์...")
    records = load_qa_file(config.SOURCE_FILE)
    if not records:
        print("❌ ไม่พบข้อมูล Q&A ในไฟล์")
        return

    save_json(records, config.EXTRACTED_TEXT_FILE)
    print(f"      -> โหลดสำเร็จ {len(records)} คู่คำถาม-คำตอบ (บันทึกที่ {config.EXTRACTED_TEXT_FILE})")

    # Step 2: ทำ Chunking
    print("[2/5] ✂️  กำลังตัดแบ่ง Chunks...")
    chunks = build_chunks(records, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    save_json(chunks, config.CHUNKS_FILE)
    print(f"      -> สร้างได้ทั้งหมด {len(chunks)} Chunks")

    # Step 3: สร้าง Embeddings (Normalized สำหรับ Cosine Similarity)
    print("[3/5] 🧠 กำลังคำนวณ Embedding Vectors...")
    t_emb = time.time()
    texts = [chunk["text"] for chunk in chunks]
    embedding_model = EmbeddingModel()
    embeddings = embedding_model.encode(texts, batch_size=64, show_progress_bar=True)
    np.save(config.EMBEDDINGS_FILE, embeddings)
    emb_time = time.time() - t_emb
    print(f"      -> สำเร็จ {embeddings.shape[0]} vectors × {embeddings.shape[1]} dims (ใช้เวลา {emb_time:.2f} วินาที)")

    if len(embeddings) != len(chunks):
        print(f"❌ ข้อผิดพลาด: จำนวน vectors ({len(embeddings)}) ไม่ตรงกับจำนวน chunks ({len(chunks)})")
        return

    # Step 4: สร้าง FAISS Index
    print("[4/5] 🗄️  กำลังสร้าง FAISS Index (IndexFlatIP)...")
    store = VectorStore()
    store.build(embeddings)
    store.save(config.FAISS_INDEX_FILE)
    save_chunk_store(chunks, config.CHUNK_STORE_FILE)
    print(f"      -> บันทึก FAISS Index ที่ {config.FAISS_INDEX_FILE}")

    # Step 5: สร้าง BM25 Index
    print("[5/5] 🔎 กำลังสร้าง BM25 Index...")
    bm25 = build_bm25(chunks)
    save_bm25(bm25, config.BM25_INDEX_FILE)
    print(f"      -> บันทึก BM25 Index ที่ {config.BM25_INDEX_FILE}")

    # บันทึก Metadata
    index_meta.save(len(chunks))

    total_time = time.time() - start_time
    print("=" * 60)
    print(f"✨ สร้าง Index ทั้งหมดสำเร็จเรียบร้อยในเวลา {total_time:.2f} วินาที!")
    print("🚀 สามารถรันระบบได้ด้วยคำสั่ง: python main.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
