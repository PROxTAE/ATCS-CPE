"""
index_meta.py - ตรวจสอบความสดใหม่ของ Index (Dataset Fingerprint)
"""

import hashlib
import json
import os
import time
import config


def get_file_md5(file_path: str):
    if not os.path.exists(file_path):
        return ""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def save(num_chunks: int, file_path=config.INDEX_META_FILE):
    meta = {
        "source_file": config.SOURCE_FILE,
        "source_md5": get_file_md5(config.SOURCE_FILE),
        "embedding_model": config.EMBEDDING_MODEL_NAME,
        "chunk_size": config.CHUNK_SIZE,
        "chunk_overlap": config.CHUNK_OVERLAP,
        "total_chunks": num_chunks,
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def is_stale(file_path=config.INDEX_META_FILE) -> bool:
    if not os.path.exists(file_path):
        return True
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        current_md5 = get_file_md5(config.SOURCE_FILE)
        return (
            meta.get("source_md5") != current_md5
            or meta.get("embedding_model") != config.EMBEDDING_MODEL_NAME
            or meta.get("chunk_size") != config.CHUNK_SIZE
        )
    except Exception:
        return True
