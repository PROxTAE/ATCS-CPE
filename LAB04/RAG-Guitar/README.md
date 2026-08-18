# 🎸 Guitar Master RAG Assistant (Web UI & CLI Specialized Pipeline)

A state-of-the-art, high-performance **Retrieval-Augmented Generation (RAG)** system with a **Cyberpunk/Studio 3D Web UI** and **Interactive CLI**, built for **English Guitar Knowledge, Hardware Engineering, Tonewoods, Electronics, Playing Techniques, and Chord Voicings**.

---

## 📌 Table of Contents
1. [System Overview & Architecture](#1-system-overview--architecture)
2. [Dual Operation Modes (Web UI vs CLI)](#2-dual-operation-modes-web-ui-vs-cli)
3. [Web UI Components & Features](#3-web-ui-components--features)
4. [Client-Server Communication & API Protocol](#4-client-server-communication--api-protocol)
5. [Embedding Model & Search Pipeline](#5-embedding-model--search-pipeline)
6. [Benchmark & Evaluation Metrics](#6-benchmark--evaluation-metrics)
7. [Installation & Execution Guide](#7-installation--execution-guide)
8. [Step-by-Step Labs Guide (Labs 01 to 07)](#8-step-by-step-labs-guide-labs-01-to-07)

---

## 1. System Overview & Architecture

The Guitar Master RAG System connects a specialized **500 Q&A (512 chunks)** English knowledge base with:
- **Vector Embedding**: `BAAI/bge-small-en-v1.5` (384-dimensional dense vectors with L2 normalization)
- **Vector Index**: FAISS `IndexFlatIP` (Exact Cosine Similarity)
- **Keyword Search**: BM25Okapi with English stopword filtering and token memoization
- **Rank Fusion**: Weighted Reciprocal Rank Fusion ($0.55 \times \text{Dense} + 0.45 \times \text{BM25}$)
- **Caching Layer**: Dual-level Exact String Match & Semantic Cosine Cache ($Sim > 0.96$) delivering **$< 2.5\text{ ms}$** response latency.

---

## 2. Dual Operation Modes (Web UI vs CLI)

The system supports two execution modes:

```text
                                 ┌───────────────────────────────┐
                                 │   User Interface Selection    │
                                 └──────────────┬────────────────┘
                                                │
                     ┌──────────────────────────┴──────────────────────────┐
                     ▼                                                     ▼
      ┌─────────────────────────────┐                       ┌─────────────────────────────┐
      │   Mode 1: Interactive CLI   │                       │     Mode 2: Modern Web UI   │
      │      (Terminal / Bash)      │                       │     (Browser on Port 8000)  │
      │       python main.py        │                       │        python app.py        │
      └──────────────┬──────────────┘                       └──────────────┬──────────────┘
                     │                                                     │
                     │                                                     ▼
                     │                                      ┌─────────────────────────────┐
                     │                                      │   FastAPI Server (REST)     │
                     │                                      │   POST /api/chat            │
                     │                                      │   GET  /api/stats           │
                     │                                      │   GET  /api/hotspots/{part} │
                     │                                      └──────────────┬──────────────┘
                     │                                                     │
                     └──────────────────────────┬──────────────────────────┘
                                                │
                                                ▼
                                 ┌───────────────────────────────┐
                                 │   RAGPipeline Orchestrator    │
                                 │  (Cache -> Hybrid -> Gen)     │
                                 └───────────────────────────────┘
```

---

## 3. Web UI Components & Features

Designed with a sleek, studio black and glowing orange aesthetic:

1. **Interactive 3D Guitar Hero Stage**:
   - Dynamic 3D perspective tilt reacting to mouse position
   - Interactive HUD Pins: `[NECK]`, `[BODY]`, `[TONE]`, `[BRIDGE]`, `[PICKUPS]` opening real-time spec popovers and AI prompt triggers.
2. **Real-Time Chat Interface**:
   - Markdown rendering (bold, lists, chord tablature, tables) with automatic citation badge generation (`[1]`, `[2]`)
   - Quick prompt suggestion chips
   - Direct clear conversation memory button.
3. **Vector Database Ranking & Search Results**:
   - Displays real-time top-ranked document chunks ($01, 02, 03, 04$)
   - Progress bar showing cosine similarity score ($0.96, 0.89, \dots$)
   - Category tags (`Stratocaster`, `Acoustic`, `Pickups`, `Chords`, `Setup`)
   - `VIEW SOURCE` modal displaying complete chunk contents, line numbers, and similarity metrics.
4. **Query Analytics Panel**:
   - Live query string, model name (`BAAI/bge-small-en-v1.5`), total chunks ($512$), search latency ($22.2\text{ ms}$), and Cache status ($\text{HIT} / \text{MISS}$).
5. **Interactive Vector Constellation**:
   - HTML5 Canvas particle network animation demonstrating vector embeddings space.

---

## 4. Client-Server Communication & API Protocol

The web frontend (`static/app.js`) communicates asynchronously via JSON over HTTP:

| Method | Endpoint | Description | Request Body | Response Payload |
|---|---|---|---|---|
| `POST` | `/api/chat` | Main RAG inquiry | `{"query": "...", "top_k": 4}` | `{"answer": "...", "sources": [...], "retrieved": [...], "timings": {...}, "cached": bool}` |
| `GET` | `/api/stats` | Pipeline statistics | None | `{"embedding_model": "...", "total_chunks": 512, "cache_stats": {...}}` |
| `GET` | `/api/hotspots/{part}` | 3D Guitar part details | None | `{"title": "...", "category": "...", "description": "...", "specs": [...]}` |
| `POST` | `/api/clear` | Reset conversation memory | None | `{"status": "cleared"}` |
| `GET` | `/api/health` | Health & Readiness | None | `{"status": "online", "model": "..."}` |

---

## 5. Embedding Model & Search Pipeline

| Stage | Technology | Latency | Benefit |
|---|---|---|---|
| **Query Caching** | LRU Exact & Semantic Cosine Cache | $< 2.5\text{ ms}$ | Sub-millisecond instant answers for repeat queries |
| **Dense Search** | `BAAI/bge-small-en-v1.5` + FAISS `IndexFlatIP` | $\sim 22\text{ ms}$ | Captures deep semantic meaning & guitar concepts |
| **Keyword Search** | BM25Okapi with Stopwords Filter | $0.87\text{ ms}$ | Pinpoint keyword matching for chord names (e.g. `C#m7`) |
| **Rank Fusion** | Weighted RRF ($0.55\text{ Dense} + 0.45\text{ BM25}$) | $< 1\text{ ms}$ | Optimal combination yielding 100% Hit@1 accuracy |

---

## 6. Benchmark & Evaluation Metrics

Evaluated on the 50-query Golden Test Set:

| Retrieval Method | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR | Latency |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **BM25 (Keyword Okapi)** | 94.0% | 100.0% | 100.0% | 100.0% | 0.970 | **0.87 ms** |
| **Dense (FAISS BGE Cosine)** | **100.0%** | **100.0%** | **100.0%** | **100.0%** | **1.000** | **22.2 ms** |
| **Hybrid (Dense + BM25 RRF)** ⭐ | **100.0%** | **100.0%** | **100.0%** | **100.0%** | **1.000** | **27.3 ms** |
| **Query Cache (Hit Mode)** ⚡ | **100.0%** | **100.0%** | **100.0%** | **100.0%** | **1.000** | **< 2.5 ms** |

- **Answer Citation Rate**: **100.0%**
- **Average Generation Latency**: **78.95 ms**

---

## 7. Installation & Execution Guide

### Prerequisites
```bash
pip install fastapi uvicorn faiss-cpu sentence-transformers rank-bm25 openai numpy
```

### Build Index
```bash
cd d:\Protae\LearningZone\3yTrem1\AdvanceML\LAB\LAB04\RAG-Guitar
python build_index.py
```

### Option A: Run Web UI Application (Recommended)
```bash
python app.py
```
Open your browser at: **`http://localhost:8000`**

### Option B: Run Interactive Terminal CLI
```bash
python main.py
```

---

## 8. Step-by-Step Labs Guide (Labs 01 to 07)

```bash
python labs/lab01_extract_text.py      # Extract Q&A records to JSON
python labs/lab02_chunking.py          # Chunk text with metadata
python labs/lab03_create_embeddings.py # Compute BGE embeddings
python labs/lab04_create_vector_db.py  # Construct FAISS Vector DB
python labs/lab05_query_embedding.py   # Test query embedding
python labs/lab06_similarity_search.py # Test semantic search
python labs/lab07_complete_retrieval.py# Run end-to-end RAG pipeline
```
