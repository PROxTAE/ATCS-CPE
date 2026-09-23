# AdvanceML-2026: Laboratory & Project Hub

คลังรวบรวมใบงานและโครงงานวิจัย รายวิชา **Advanced Machine Learning (Deep Learning & NLP)**  
ภาคการศึกษาที่ 1 ปีการศึกษา 2569 | ภาควิชาวิศวกรรมคอมพิวเตอร์ คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเทคโนโลยีราชมงคลธัญบุรี

---

## ข้อมูลผู้จัดทำ (Author Information)
- **ชื่อ-นามสกุล:** นายนิธิศ มะโนรา (Mr. Nithit Manora)
- **รหัสนักศึกษา:** 116730462042-6
- **สาขาวิชา:** วิศวกรรมคอมพิวเตอร์ (CPE)

---

## 1. แดชบอร์ดสรุปใบงานที่จัดทำแล้ว (Completed Laboratories)

| โฟลเดอร์ | หัวข้อ / ระบบที่พัฒนา (Topic & System) | เทคโนโลยีหลัก (Key Stack) | สถานะ (Status) |
|:---|:---|:---|:---:|
| **[LAB03](./LAB03/)** | RAG System I: Guitar Chord & Music Theory Chatbot | Multilingual-E5, FAISS CPU, FastAPI | `[Completed]` |
| **[LAB04](./LAB04/)** | English Guitar RAG System & 3D Interactive Web UI | BGE-Small-EN, BM25+Dense RRF, Gemini LLM, Three.js | `[Completed]` |
| **[LAB05](./LAB05/)** | RAG System Development II: Problem Simulation Suite | 10 RAG Failure Simulations, Hybrid LLM Evaluation | `[Completed]` |
| **[LAB07](./LAB07/)** | **Module 08: Travel Recommendation & Feedback Service (Final Project Subtree)** | FastAPI, Recommendation Builder, User Feedback Loop, OpenAPI v1.0.0, Docker | `[Completed]` |

> *หมายเหตุ: สำหรับใบงานอื่นๆ จะดำเนินการอัปเดตเพิ่มเติมเมื่อจัดทำเสร็จสิ้นในแต่ละรอบ*

---

## 2. ไกด์ไลน์และสรุปสาระสำคัญของแต่ละแล็บ (Lab Guides & Highlights)

---

### [LAB03: ระบบถาม-ตอบความรู้คอร์ดกีตาร์ด้วย RAG Pipeline ขั้นพื้นฐาน](./LAB03/README.md)
* **สถานะ:** `[Completed]`
* **แนวคิดหลัก:** พัฒนาระบบ Retrieval-Augmented Generation (RAG) สำหรับตอบคำถามทฤษฎีดนตรีและสืบค้นคอร์ดเพลงจากฐานข้อมูล CSV ขนาดใหญ่
* **สถาปัตยกรรมและเทคโนโลยี:**
  - **Embedding:** `intfloat/multilingual-e5-large` รองรับหลายภาษา
  - **Vector Store:** FAISS IndexFlatIP (Cosine Similarity)
  - **Interface:** FastAPI Web Service ให้บริการ REST API และหน้าเว็บแชท
* **เอกสารฉบับเต็ม:** อ่านรายละเอียดเพิ่มเติมได้ที่ [LAB03/README.md](./LAB03/README.md)

---

### [LAB04: English Guitar RAG System & 3D Interactive Web UI](./LAB04/README.md)
* **สถานะ:** `[Completed]`
* **แนวคิดหลัก:** ยกระดับประสิทธิภาพการสืบค้นความรู้กีตาร์สู่ระดับ High-Accuracy ด้วยชุดข้อมูลภาษาอังกฤษมาตรฐาน 501 รายการ พร้อมอินเทอร์เฟซ 3D Studio ล้ำสมัย
* **จุดเด่นสำคัญ:**
  - **Embedding ประสิทธิภาพสูงสุด:** `BAAI/bge-small-en-v1.5` (384 มิติ) ความแม่นยำ Hit@1 = 100% บน Benchmark
  - **Hybrid Retrieval:** ผสานการค้นหาแบบ Dense Vector (FAISS) และ Sparse Keyword (BM25 Okapi) ด้วย Reciprocal Rank Fusion (RRF)
  - **3D Interactive Stage:** หน้าเว็บโมเดล 3D กีตาร์แบบ Interactive Tilt พร้อมหมุดสเปกเทคนิค 5 จุด
  - **Speed & Caching:** มี Caching Layer ลดเวลาตอบสนองซ้ำเหลือต่ำกว่า 2.5 ms
  - **LLM Integration:** เชื่อมต่อ Gemini / OpenAI API สำหรับสังเคราะห์คำตอบพร้อม Citation Badges
* **เอกสารฉบับเต็ม:** อ่านรายละเอียดเพิ่มเติมได้ที่ [LAB04/README.md](./LAB04/README.md)

---

### [LAB05: Guitar RAG System Development II (Problem Simulation Suite)](./LAB05/README.md)
* **สถานะ:** `[Completed]`
* **แนวคิดหลัก:** วิเคราะห์และจำลอง 10 ปัญหาสำคัญที่พบจริงในการพัฒนาระบบ RAG (อ้างอิงโจทย์ DL-05 อ.อนุรักษ์ พรหมโคตร) โดยปรับบริบทเข้ากับโดเมนกีตาร์และแก้ปัญหาจริงของโปรเจกต์
* **ปัญหาสำคัญที่จำลองและแก้ไขสำเร็จ:**
  - **Cross-Lingual Gap:** ปัญหาผู้ใช้ถามภาษาไทยแต่คลังความรู้เป็นภาษาอังกฤษ แก้ด้วย LLM Translation + Dense Retrieval
  - **Top-K Pattern Dump vs LLM:** แก้ปัญหาการดึงข้อความดิบมาแปะ ด้วยการใช้ LLM จัดฟอร์แมต Markdown แจกแจงการวางนิ้ว 6 สาย พร้อมโหมด Hybrid คุยเรื่องทั่วไปได้
  - **Chord Notation Discrepancies:** แก้ปัญหาคอร์ดเขียนได้หลายแบบ (`Cmaj7`, `C^7`, `CΔ7`) และคอร์ดเสียงเหมือนกัน (`Gbm` / `F#m`) ด้วย Regex Chord Normalizer
  - **Broken ASCII Tablatures:** แก้ปัญหาการตัด Chunk ผ่ากลางแท็บ 6 สาย ด้วย Block-Aware Chunker
  - **Polysemy & Re-ranking:** แก้ปัญหาคำพ้องรูป ("Bridge" สะพานสาย vs ท่อนบริดจ์เพลง) ด้วย Cross-Encoder 2nd-stage Re-ranker
* **การรันโปรแกรม:** รองรับทั้ง Interactive Menu (`python main.py`), รันเจาะจงรายปัญหา (`python main.py <1-10>`), หรือรันทั้งหมด (`python main.py all`)
* **เอกสารฉบับเต็ม:** อ่านรายละเอียดเพิ่มเติมได้ที่ [LAB05/README.md](./LAB05/README.md)

---

### [LAB07: Module 08 — Travel Recommendation & User Feedback Service (Final Project Subtree)](./LAB07/README.md)
* **สถานะ:** `[Completed]`
* **บทบาทและหน้าที่:** ด่านสังเคราะห์ขั้นสุดท้าย (Final Synthesis & Action Planning Engine) ในโครงงานหลัก **[SafetyTravel Assistant (travel-safety-ai)](https://github.com/PROxTAE/travel-safety-ai)** โดยรับผลลัพธ์จาก Decision Engine (M07), Data Integration Corridor (M05), และ Risk Knowledge (M06) ผ่าน AI Agent (M03) เพื่อสังเคราะห์เป็นคำแนะนำการเดินทางที่ปฏิบัติได้จริง
* **จุดเด่นสำคัญ:**
  - **Actionable Guidance:** สังเคราะห์คำแนะนำ 4 ระดับ (🟢 `NORMAL` · 🟡 `CHANGE_ROUTE` · 🟠 `DELAY` · 🔴 `AVOID`) พร้อม Action Checklist, Packing List, และ Risk Rationale
  - **Continuous Feedback Loop:** ระบบรับคะแนน (1–5 ดาว) และฟีดแบ็กจากผู้ใช้ เพื่อเก็บเป็น Benchmark Data สำหรับการ Retrain โมเดล
  - **Official Emergency Directory:** ระบบบริการค้นหาเบอร์โทรฉุกเฉินระดับชาติ (191, 1669, 1155, 1193) ตามพิกัดจริง (Zero-Mock)
  - **Contract Compliance:** ปฏิบัติตาม OpenAPI v1.0.0 และมี Unit / Contract Test Cases ผ่าน 100%
* **เอกสารฉบับเต็ม:** อ่านรายละเอียดเพิ่มเติมและดูแผนผังการเชื่อมต่อโมดูลได้ที่ [LAB07/README.md](./LAB07/README.md)

---

## 3. โครงสร้างโฟลเดอร์ในภาพรวม (Repository Structure)

```text
AdvanceML-LAB/
├── LAB03/                           # ใบงานที่ 3: Guitar Chord RAG (Completed)
│   ├── RAG-Project/                 # ซอร์สโค้ดระบบ FastAPI + E5 Embeddings
│   └── README.md                    # เอกสารอธิบาย LAB03
├── LAB04/                           # ใบงานที่ 4: English Guitar RAG & 3D Web UI (Completed)
│   ├── RAG-Guitar/                  # ซอร์สโค้ดระบบ RAG-Guitar แบบเต็มรูปแบบ
│   └── README.md                    # เอกสารสรุปรายงานผล LAB04 ฉบับสมบูรณ์
├── LAB05/                           # ใบงานที่ 5: RAG Problem Simulation Suite (Completed)
│   ├── data/                        # ฐานข้อมูลความรู้ 501 Q&A
│   ├── main.py                      # CLI Runner เมนูรันการทดสอบ 1-10
│   ├── problem01 - 10               # สคริปต์จำลองและแก้ไขปัญหา 10 ขั้นตอน
│   └── README.md                    # รายงานการวิเคราะห์ปัญหา 10 ข้อตามโจทย์อาจารย์
├── LAB07/                           # ใบงานที่ 7: Final Project Module 08 Subtree (Completed)
│   ├── module-08-recommendation/    # Git Subtree จาก services/recommendation ใน travel-safety-ai
│   └── README.md                    # เอกสารอธิบายภาพรวม Module 08 และการเชื่อมต่อทั้ง 8 โมดูล
└── README.md                        # แดชบอร์ดสรุปภาพรวมและไกด์ไลน์ (ไฟล์นี้)
```

---

## 4. คำสั่งเริ่มต้นใช้งานด่วน (Quick Start)

### ทดสอบรัน LAB04 (Modern 3D Web UI):
```powershell
cd LAB04/RAG-Guitar
pip install -r requirements.txt
python app.py
# เข้าใช้งานผ่านเว็บเบราว์เซอร์ที่: http://localhost:8000
```

### ทดสอบรัน LAB05 (RAG Problem Simulation CLI):
```powershell
cd LAB05
# รันเมนูแบบ Interactive CLI
python main.py

# หรือรันทุกปัญหาต่อเนื่องกันทั้งหมด
python main.py all
```

### ทดสอบรัน LAB07 (Module 08 Recommendation Tests):
```powershell
cd LAB07/module-08-recommendation
uv run pytest
```

---

## 5. แหล่งอ้างอิง (References)
- **Main Project Repository:** [SafetyTravel Assistant (travel-safety-ai)](https://github.com/PROxTAE/travel-safety-ai)
- **Course Repository:** [Advanced Topic in Computer Software Course (อ.อนุรักษ์ พรหมโคตร)](https://github.com/aproot-en/Advanced-Topic-in-Computer-Software-Course)
- **Embedding Benchmarks:** [MTEB (Massive Text Embedding Benchmark)](https://huggingface.co/spaces/mteb/leaderboard)
- **Guitar Theory & Chords:** [Gigasheet Chord Database](https://www.gigasheet.com/sample-data/guitar-chord-database), [Learn & Master Guitar](https://www.learnandmaster.com/resources/Learn-and-Master-Guitar-Lesson-Book.pdf)
