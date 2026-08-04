import os
import sys
import subprocess
import argparse

# Ensure console supports UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

def run_script(script_path):
    print(f"\n[main.py] Running: {script_path} ...")
    result = subprocess.run([sys.executable, script_path], capture_output=False)
    if result.returncode != 0:
        print(f"[main.py] Error: Script {script_path} failed with exit code {result.returncode}")
        return False
    return True

def rebuild_database():
    print("=== Rebuilding Vector Database ===")
    
    # 1. Prepare consolidated data
    if not run_script("scripts/prepare_guitar_data.py"):
        return False
        
    # 2. Run Labs 1-4 to extract, chunk, embed, and build index
    labs = [
        "labs/lab01_extract_text.py",
        "labs/lab02_chunking.py",
        "labs/lab03_create_embeddings.py",
        "labs/lab04_create_vector_db.py",
    ]
    
    for lab in labs:
        if not run_script(lab):
            print(f"[main.py] Database build stopped at {lab}")
            return False
            
    print("\n=== Vector Database Rebuild Completed Successfully ===")
    return True

def start_server():
    print("\n=== Starting Web Application Server ===")
    # Running app.py which starts uvicorn
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n[main.py] Server stopped by user.")

def start_cli():
    print("\n=== Starting Guitar Chords RAG System CLI Mode ===")
    
    # Check if database exists, if not rebuild it
    db_index = os.path.join("vector_db", "document.index")
    db_store = os.path.join("vector_db", "chunk_store.json")
    
    if not os.path.exists(db_index) or not os.path.exists(db_store):
        print("[main.py] Vector database files missing. Rebuilding first...")
        if not rebuild_database():
            print("[main.py] Failed to build database. Aborting.")
            return

    # Add project path to sys.path to ensure local imports work
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    import config
    import pandas as pd
    import re
    from src.retriever import Retriever
    
    # Load songs CSV
    df_songs = None
    if os.path.exists(config.SONGS_CSV_FILE):
        try:
            print(f"Loading songs database from: {config.SONGS_CSV_FILE} ...")
            df_songs = pd.read_csv(config.SONGS_CSV_FILE, low_memory=False)
            print(f"Loaded {len(df_songs)} songs from CSV successfully.")
        except Exception as e:
            print(f"Failed to load songs CSV: {e}")
    else:
        print(f"Warning: Songs CSV file not found at: {config.SONGS_CSV_FILE}")

    # Load Retriever
    print("Initializing Retriever model...")
    try:
        retriever = Retriever(
            model_name=config.EMBEDDING_MODEL_NAME,
            index_path=config.FAISS_INDEX_FILE,
            chunk_store_path=config.CHUNK_STORE_FILE,
        )
        print("Retriever initialized successfully.")
    except Exception as e:
        print(f"Error initializing Retriever: {e}")
        return

    print("\n" + "="*60)
    print("Welcome to the Guitar Chords RAG System CLI!")
    print("You can search for song chords (e.g. 'เพลง 15', 'pop') or ask general theory questions (e.g. 'วิธีจับคอร์ด C').")
    print("Type 'exit', 'quit', or 'q' to end the session.")
    print("="*60 + "\n")

    while True:
        try:
            query = input("Ask a question: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting CLI...")
            break

        if not query:
            continue

        if query.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        print(f"\nSearching for: '{query}'...")
        results = []

        # 1. Exact ID or Genre match from CSV (Hybrid Search)
        if df_songs is not None:
            # Match exact ID
            digits = re.findall(r'\b\d+\b', query)
            exact_match = None
            if digits:
                for digit in digits:
                    sub = df_songs[df_songs['id'].astype(str) == str(digit)]
                    if not sub.empty:
                        exact_match = sub.iloc[0].to_dict()
                        break
            
            if exact_match:
                raw_chords = str(exact_match.get('chords', ''))
                chords_formatted = raw_chords.replace('<', '\n<').strip()
                results.append({
                    "score": 1.0,
                    "category": "คอร์ดเพลง (จากคลัง CSV)",
                    "question": f"คอร์ดและแนวทางการเล่นสำหรับ เพลง ID {exact_match.get('id')}",
                    "answer": f"นี่คือคอร์ดเพลง ID {exact_match.get('id')} ที่พบในฐานข้อมูล:\n\n{chords_formatted}\n\n• แนวเพลง: {exact_match.get('genres')}\n• ศิลปิน: {exact_match.get('artist_id')}\n• ปีที่จำหน่าย: {exact_match.get('release_date', 'N/A')}",
                    "line_no": int(exact_match.get('id', 0))
                })
            else:
                # Match Genre
                genres_to_check = ['pop', 'metal', 'rock', 'electronic', 'punk', 'blues', 'jazz', 'country', 'folk']
                matched_genre = None
                for g in genres_to_check:
                    if g in query.lower():
                        matched_genre = g
                        break
                if matched_genre:
                    sub = df_songs[df_songs['genres'].str.contains(matched_genre, na=False, case=False)].head(5)
                    if not sub.empty:
                        songs_list = []
                        for s in sub.to_dict(orient="records"):
                            songs_list.append(f"• **เพลง ID {s['id']}** | คอร์ดตัวอย่าง: {str(s['chords'])[:60]}... | ศิลปิน: {s['artist_id']}")
                        results.append({
                            "score": 1.0,
                            "category": "แนะนำเพลงตามสไตล์ (จากคลัง CSV)",
                            "question": f"แนะนำเพลงสไตล์ {matched_genre.upper()}",
                            "answer": f"พบเพลงแนว {matched_genre.upper()} ในคลังคอร์ดเพลงที่น่าสนใจดังนี้:\n\n" + "\n".join(songs_list) + "\n\n(คุณสามารถค้นหาคอร์ดเต็มของแต่ละเพลงได้โดยการพิมพ์ถามเป็นตัวเลข เช่น 'เพลง 2' หรือ 'ขอดูคอร์ดเพลง ID 2')",
                            "line_no": 0
                        })

        # 2. Retrieve from Vector DB
        try:
            vector_results = retriever.retrieve(query, top_k=3)
            # Standardize output format
            for item in vector_results:
                results.append({
                    "score": item.get("score", 0.0),
                    "category": item.get("category", "ทฤษฎีดนตรี / วิธีจับคอร์ด"),
                    "question": item.get("question", ""),
                    "answer": item.get("answer", ""),
                    "line_no": item.get("line_no", 0)
                })
        except Exception as e:
            print(f"Error during vector store retrieval: {e}")

        # Sort results so the song match (score 1.0) is always first
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        if not results:
            print("No relevant results found.")
            continue

        print(f"\n--- Found {len(results)} results ---")
        for i, res in enumerate(results):
            print(f"\n[{i+1}] [{res['category']}] (Score: {res['score']:.4f})")
            print(f"Question: {res['question']}")
            print(f"Answer:\n{res['answer']}")
            print("-" * 60)
        print()

def main():
    parser = argparse.ArgumentParser(description="Guitar Chords RAG System Controller")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the Vector Database index from raw data")
    parser.add_argument("--server", action="store_true", help="Only start the FastAPI web server")
    args = parser.parse_args()

    # Determine actions
    if args.rebuild:
        rebuild_database()
        return

    if args.server:
        start_server()
        return

    # Default action: Enter CLI mode
    start_cli()

if __name__ == "__main__":
    main()
