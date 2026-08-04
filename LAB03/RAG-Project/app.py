import os
import sys
import re
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Solve the problem of Windows console not showing Thai text
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
from src.retriever import Retriever

app = FastAPI(title="Guitar Chords & Music Theory RAG Web UI")

# Global retriever and song dataframe instances
retriever = None
df_songs = None

def load_songs_csv():
    global df_songs
    if os.path.exists(config.SONGS_CSV_FILE):
        try:
            print(f"Loading songs database from: {config.SONGS_CSV_FILE} ...")
            df_songs = pd.read_csv(config.SONGS_CSV_FILE, low_memory=False)
            print(f"Loaded {len(df_songs)} songs from CSV successfully.")
        except Exception as e:
            print(f"Failed to load songs CSV: {e}")
    else:
        print(f"Warning: Songs CSV file not found at: {config.SONGS_CSV_FILE}")

@app.on_event("startup")
def startup_event():
    global retriever
    load_songs_csv()
    # Check if vector db files exist
    if not os.path.exists(config.FAISS_INDEX_FILE) or not os.path.exists(config.CHUNK_STORE_FILE):
        print(f"Warning: Vector database files not found. They must be created before queries can be processed.")
        return
    retriever = Retriever(
        model_name=config.EMBEDDING_MODEL_NAME,
        index_path=config.FAISS_INDEX_FILE,
        chunk_store_path=config.CHUNK_STORE_FILE,
    )

class ChatRequest(BaseModel):
    query: str

def search_song_by_query(query: str):
    if df_songs is None:
        return None
    
    # 1. Search by exact ID match if user query contains digits
    digits = re.findall(r'\b\d+\b', query)
    if digits:
        for digit in digits:
            sub = df_songs[df_songs['id'].astype(str) == str(digit)]
            if not sub.empty:
                return {
                    "type": "exact_song",
                    "data": sub.iloc[0].to_dict()
                }

    # 2. Search by Genre if user mentions main genres
    genres_to_check = ['pop', 'metal', 'rock', 'electronic', 'punk', 'blues', 'jazz', 'country', 'folk']
    matched_genre = None
    for g in genres_to_check:
        if g in query.lower():
            matched_genre = g
            break
            
    if matched_genre:
        sub = df_songs[df_songs['genres'].str.contains(matched_genre, na=False, case=False)].head(5)
        if not sub.empty:
            return {
                "type": "genre_list",
                "genre": matched_genre,
                "data": sub.to_dict(orient="records")
            }
            
    return None

@app.post("/api/chat")
async def chat(request: ChatRequest):
    global retriever
    if retriever is None:
        if os.path.exists(config.FAISS_INDEX_FILE) and os.path.exists(config.CHUNK_STORE_FILE):
            retriever = Retriever(
                model_name=config.EMBEDDING_MODEL_NAME,
                index_path=config.FAISS_INDEX_FILE,
                chunk_store_path=config.CHUNK_STORE_FILE,
            )
        else:
            raise HTTPException(status_code=500, detail="Vector database files are missing. Please run lab scripts first.")
    
    query = request.query.strip()
    if not query:
        return {"query": query, "results": []}
    
    try:
        results = []
        
        # Try CSV song lookup first (Hybrid Search)
        song_match = search_song_by_query(query)
        if song_match:
            if song_match["type"] == "exact_song":
                song_data = song_match["data"]
                # Clean up chords format for presentation
                raw_chords = str(song_data.get('chords', ''))
                chords_formatted = raw_chords.replace('<', '\n<').strip()
                
                results.append({
                    "score": 1.0,
                    "category": "คอร์ดเพลง (จากคลัง CSV)",
                    "question": f"คอร์ดและแนวทางการเล่นสำหรับ เพลง ID {song_data.get('id')}",
                    "answer": f"นี่คือคอร์ดเพลง ID {song_data.get('id')} ที่พบในฐานข้อมูลครับ:\n\n{chords_formatted}\n\n• แนวเพลง: {song_data.get('genres')}\n• ศิลปิน: {song_data.get('artist_id')}\n• ปีที่จำหน่าย: {song_data.get('release_date', 'N/A')}",
                    "line_no": int(song_data.get('id', 0))
                })
            elif song_match["type"] == "genre_list":
                songs_list = []
                for s in song_match["data"]:
                    songs_list.append(f"• **เพลง ID {s['id']}** | คอร์ดตัวอย่าง: {str(s['chords'])[:60]}... | ศิลปิน: {s['artist_id']}")
                
                results.append({
                    "score": 1.0,
                    "category": "แนะนำเพลงตามสไตล์ (จากคลัง CSV)",
                    "question": f"แนะนำเพลงสไตล์ {song_match['genre'].upper()}",
                    "answer": f"พบเพลงแนว {song_match['genre'].upper()} ในคลังคอร์ดเพลงที่น่าสนใจดังนี้ครับ:\n\n" + "\n".join(songs_list) + "\n\n(คุณสามารถค้นหาคอร์ดเต็มของแต่ละเพลงได้โดยการพิมพ์ถามเป็นตัวเลข เช่น 'เพลง 2' หรือ 'ขอดูคอร์ดเพลง ID 2')",
                    "line_no": 0
                })

        # Retrieve general theory & chord fingerings from Vector DB
        vector_results = retriever.retrieve(query, top_k=3)
        results.extend(vector_results)
        
        # Sort results so the song match (score 1.0) is always first
        results = sorted(results, key=lambda x: x["score"], reverse=True)
        
        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files folder
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at root
@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    print("Starting Web Server at http://127.0.0.1:8000 ...")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
