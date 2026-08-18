"""
app.py - High-Performance FastAPI Web Server & API for Guitar Master RAG System
Provides both RESTful API for Web UI and static file serving.
"""

import os
import sys
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
from src.rag_pipeline import RAGPipeline

app = FastAPI(
    title="PROxTAE Guitar RAG Assistant",
    description="Vector Search & LLM-Powered Guitar Knowledge System",
    version="2.0.0",
)

# Enable CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Pipeline singleton
print("🎸 Initializing Guitar RAG Pipeline for Web Service...")
rag_pipeline = RAGPipeline()
print("✅ Guitar RAG Pipeline Ready!")

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)


class ChatRequest(BaseModel):
    query: str
    top_k: int = config.TOP_K


# Hotspot explanations for interactive 3D guitar
HOTSPOTS = {
    "headstock": {
        "title": "Headstock, Tuners & Truss Rod Access",
        "category": "Hardware & Tuning",
        "description": "Stratocaster 6-in-line headstock featuring sealed die-cast tuning pegs (14:1 gear ratio), synthetic bone nut (42mm), dual butterfly string guides, and bullet truss rod access for neck relief adjustment.",
        "specs": ["Tuning Pegs: 6-in-line Die-cast", "Nut: 42mm Synthetic Bone", "String Guide: Dual Wing/Butterfly", "Truss Rod: 4mm Hex Headstock Access"]
    },
    "neck": {
        "title": "Maple Neck, Fretboard & Frets",
        "category": "Tonewoods & Construction",
        "description": "Modern 'C' profile solid maple neck with 9.5\" radius fretboard, 21 nickel-silver medium-jumbo frets, and black dot position inlays. Fast playing action with satin urethane back finish.",
        "specs": ["Profile: Modern 'C'", "Radius: 9.5\" (241mm)", "Frets: 21 Medium Jumbo", "Inlays: Dot Markers (3,5,7,9,12,15,17,19,21)"]
    },
    "body": {
        "title": "Contoured Solid Alder Body & Joint",
        "category": "Guitar Construction",
        "description": "Classic double-cutaway ergonomic solid Alder body with rear belly cut and forearm contour. Secured via 4-bolt chrome neck plate with stamped serial engraving.",
        "specs": ["Body Wood: Solid Alder", "Finish: High-Gloss Polyurethane", "Neck Joint: 4-Bolt Sculpted Plate", "Strap Pins: Dual Vintage Buttons"]
    },
    "pickups": {
        "title": "Triple Single-Coil Pickup Set",
        "category": "Pickups & Electronics",
        "description": "3 staggered Alnico V single-coil pickups. Middle pickup is Reverse-Wound / Reverse-Polarity (RWRP) for hum-cancelling operation in selector positions 2 and 4.",
        "specs": ["Neck: 5.8kΩ (Warm & Woody)", "Middle: 6.2kΩ RWRP (Chime)", "Bridge: 6.8kΩ (Biting Lead)", "Magnets: Alnico V Pole Pieces"]
    },
    "bridge": {
        "title": "6-Saddle Synchronized Tremolo Bridge",
        "category": "Hardware & Bridge",
        "description": "Vintage-style synchronized vibrato bridge featuring 6 individually adjustable pressed steel saddles for string action and intonation tuning, screw-in tremolo arm, and steel sustain block.",
        "specs": ["Type: 6-Saddle Vintage Tremolo", "Saddles: Pressed Steel", "Block: High-Mass Zinc/Steel", "Springs: 3-5 Tension Springs in Rear Cavity"]
    },
    "tone": {
        "title": "Controls, 5-Way Switch & Output Jack",
        "category": "Electronics & Circuitry",
        "description": "Master volume potentiometer with dual 250k tone pots, 5-way pickup selector switch, and recessed top-mounted 1/4\" output jack cup mounted on a 3-ply parchment pickguard.",
        "specs": ["Pots: Master Volume, Tone 1 (Neck), Tone 2 (Middle/Bridge)", "Switch: 5-Way Blade", "Capacitor: 0.022µF Tone Cap", "Jack: 1/4\" Mono Recessed Cup"]
    }
}


@app.get("/api/health")
async def health_check():
    return {
        "status": "online",
        "service": "Guitar Lab RAG Assistant",
        "model": config.EMBEDDING_MODEL_NAME,
        "llm_provider": config.LLM_PROVIDER,
        "cache_enabled": config.USE_CACHE,
    }


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    query = req.query.strip()
    if not query:
        return JSONResponse(status_code=400, content={"error": "Query cannot be empty"})

    t0 = time.time()
    result = rag_pipeline.ask(query, top_k=req.top_k)
    elapsed_ms = round((time.time() - t0) * 1000, 2)

    # Format response for Web UI
    return {
        "query": query,
        "answer": result.get("answer", ""),
        "sources": result.get("sources", []),
        "retrieved": result.get("retrieved", []),
        "timings": result.get("timings", {}),
        "cached": result.get("cached", False),
        "cache_type": result.get("cache_type", "none"),
        "queries_used": result.get("queries_used", [query]),
        "llm_used": result.get("llm_used", True),
        "model_name": result.get("model_name", "Google Gemini AI (3.1-flash-lite)"),
        "total_server_time_ms": elapsed_ms,
    }


@app.get("/api/stats")
async def stats_endpoint():
    cache_stats = rag_pipeline.get_cache_stats()
    return {
        "embedding_model": config.EMBEDDING_MODEL_NAME,
        "embedding_dim": config.EMBEDDING_DIM,
        "chunk_size": config.CHUNK_SIZE,
        "top_k": config.TOP_K,
        "dense_weight": config.DENSE_WEIGHT,
        "bm25_weight": config.BM25_WEIGHT,
        "cache_stats": cache_stats,
        "total_chunks": len(rag_pipeline.retriever.chunks),
    }


@app.get("/api/hotspots/{part}")
async def get_hotspot(part: str):
    part_clean = part.lower().strip()
    if part_clean in HOTSPOTS:
        return HOTSPOTS[part_clean]
    return JSONResponse(status_code=404, content={"error": "Part not found"})


@app.post("/api/clear")
async def clear_memory():
    rag_pipeline.reset_memory()
    return {"status": "cleared", "message": "Conversation history cleared"}


# Mount static assets
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Guitar Lab RAG API is running. Please add index.html to static/ directory."}


if __name__ == "__main__":
    import uvicorn
    print("=" * 65)
    print("🎸 Starting Guitar Lab Web Server on http://localhost:8000")
    print("=" * 65)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
