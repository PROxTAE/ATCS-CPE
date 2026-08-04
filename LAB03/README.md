# LAB03: ระบบสืบค้นและตอบคำถามคอร์ดกีตาร์และทฤษฎีดนตรี (Guitar Chords & Music Theory RAG System)

ระบบแชทบอทตอบคำถามเกี่ยวกับวิธีจับคอร์ดกีตาร์ แนะนำเพลงตามแนวเพลง และทฤษฎีดนตรีทั่วไป โดยใช้สถาปัตยกรรม **RAG (Retrieval-Augmented Generation)** ร่วมกับฐานข้อมูลแบบไฮบริด (Hybrid Search) ทั้งแบบ Vector Database (FAISS + E5 Multilingual Model) และการค้นหาเชิงโครงสร้างจาก CSV

---

## 👥 ผู้จัดทำ (Author)
- **ชื่อ-นามสกุล (Name):** นายนิธิศ มะโนรา
- **รหัสนักศึกษา (Student ID):** 116730462042-6

---

## 🌟 ฟีเจอร์เด่นของระบบ (Key Features)
1. **Hybrid Retrieval Search**:
   * **Vector Search**: ค้นหาข้อมูลเชิงคุณภาพ (วิธีจับคอร์ดกีตาร์, ความรู้ทฤษฎีดนตรีทั่วไป, เทคนิคการซ้อมจาก PDF คู่มือ) โดยใช้โมเดล Embedding `intfloat/multilingual-e5-large` ร่วมกับดัชนี **FAISS (CPU)**
   * **CSV Song Lookup**: ค้นหาคอร์ดของเพลงตามชื่อแนวเพลง (เช่น Pop, Rock, Metal) หรือค้นหาตามรหัสเพลง (Song ID) ได้โดยตรงผ่านฐานข้อมูล CSV ขนาดใหญ่ [ สามารถโหลด Dataset ได้ที่ Guitar Chord Database ](https://www.gigasheet.com/sample-data/guitar-chord-database)
2. **Interactive UI (Glassmorphic Design)**:
   * หน้าเว็บเพจออกแบบด้วยเทคนิค Glassmorphism ที่สวยงาม คลีน และรองรับการตอบสนองทุกขนาดหน้าจอ (Responsive Web Design)
   * แสดงข้อความแชทประวัติสนทนาพร้อมรักษาฟอร์แมตแผนภาพการจับสายกีตาร์อย่างถูกต้องด้วยการตั้งค่า `white-space: pre-wrap`
   * หน้าต่างด้านซ้าย (Retrieved Sources Sidebar) แสดงข้อมูลเอกสารอ้างอิงที่ระบบค้นพบจริง ๆ จากฐานข้อมูล พร้อมคะแนนความคล้ายคลึง (Cosine Similarity Score) และตำแหน่งบรรทัดต้นฉบับ
3. **CLI Mode & Web UI**:
   * รองรับการใช้งานผ่านหน้าต่างคอนโซล (CLI Command line) เพื่อทดสอบแบบรวดเร็ว และรันผ่าน FastAPI Web Server สำหรับใช้งานผ่านหน้าเว็บบราวเซอร์

---

## 📂 รายละเอียดโครงสร้างไฟล์ในระบบ (Folder Structure)

```text
RAG-Project/
├── config.py                 # ตั้งค่าโฟลเดอร์ พารามิเตอร์การแบ่ง chunk และการตั้งค่าโมเดล
├── app.py                    # FastAPI Web Server สำหรับให้บริการ API แชทและหน้าเว็บ UI
├── main.py                   # ตัวควบคุมหลัก (Controller) สำหรับสั่ง Rebuild ฐานข้อมูล, เปิด CLI หรือเปิด Server
├── requirements.txt          # รายการแพ็กเกจไลบรารีที่จำเป็นต้องใช้
│
├── data/                     # โฟลเดอร์เก็บข้อมูลดิบ (Raw Data)
│   ├── guitar_q_a.txt        # ไฟล์ถาม-ตอบความรู้ทั่วไปเกี่ยวกับกีตาร์และการดูแลรักษา
│   ├── guitar_rag_dataset.txt# ไฟล์ชุดข้อมูลหลักที่ consolidated จาก JSON และ PDF
│   ├── guitar-course-pdf/    # แหล่งเก็บคู่มือ PDF สำหรับทำความเข้าใจการฝึกหัดเบื้องต้น
│   ├── chord-collection-.../ # ข้อมูลพิกัดคอร์ดในรูปแบบ JSON
│   └── *.csv                 # ฐานข้อมูลเพลงและคอร์ดเพลงขนาดใหญ่ (> 270MB)
│
├── labs/                     # สคริปต์ขั้นการทำงาน (Pipeline ขั้นตอนที่ 1 - 7)
│   ├── lab01_extract_text.py # ดึงข้อมูลดิบจาก Text/PDF แปลงเป็น JSON โครงสร้าง
│   ├── lab02_chunking.py     # แบ่งข้อความเป็น Chunk ย่อยตามขนาดที่กำหนด (Chunk Size)
│   ├── lab03_create_embeddings.py # แปลงเนื้อความใน Chunk เป็น Vector ด้วยโมเดล E5
│   ├── lab04_create_vector_db.py  # สร้างไฟล์ดัชนี FAISS index และเก็บสารบัญลง JSON
│   └── lab05 - lab07...      # สคริปต์สำหรับการจำลองการเรียกค้นข้อมูล (Query/Similarity Search)
│
├── src/                      # โมดูลและคลาสทำงานหลัก
│   ├── document_loader.py    # โค้ดแปลงเนื้อหา Q&A และคู่มือให้อยู่ในโครงสร้าง Record
│   ├── text_splitter.py      # ตัวแบ่งข้อความขนาดใหญ่พร้อมควบคุมระยะเหลื่อม (Overlap)
│   ├── embedding_model.py    # โค้ดดึงโมเดลและแปลงประโยคเป็นเวกเตอร์
│   ├── retriever.py          # เครื่องมือค้นหาความคล้ายคลึงของเวกเตอร์และลำดับความสำคัญ
│   └── vector_store.py       # จัดเก็บข้อมูลและแปลงเวกเตอร์ลงในดัชนีของ FAISS
│
├── static/                   # ไฟล์หน้าบ้าน (Frontend Static Assets)
│   ├── index.html            # หน้าเว็บเพจหลัก
│   ├── script.js             # ควบคุมการทำงานของปุ่ม คีย์ข้อความ และแสดงผล API แชท
│   └── style.css             # ตกแต่งหน้าตาแชทบ็อต แอนิเมชัน และสีแบบ Glassmorphism
│
└── vector_db/                # ไฟล์ผลลัพธ์ฐานข้อมูลเวกเตอร์ (Vector Database)
    ├── chunk_store.json      # แหล่งเก็บข้อมูลดิบและเมทาดาต้าของแต่ละ Chunk
    └── document.index        # ไฟล์ดัชนีเวกเตอร์ที่แปลงโดย FAISS สำหรับทำ Similarity Search
```

---

## 🛠️ วิธีการใช้งานและการติดตั้ง (Setup & Execution)

### 1. ติดตั้งไลบรารีที่จำเป็น (Installation)
ก่อนเริ่มต้นรันระบบ กรุณาตรวจสอบให้แน่ใจว่าติดตั้ง Python 3.10 ขึ้นไป และติดตั้งแพ็กเกจใน `requirements.txt` แล้ว:
```bash
pip install -r requirements.txt
```

### 2. การสร้างฐานข้อมูลเวกเตอร์ใหม่ (Rebuild Database)
หากต้องการประมวลผลข้อมูลดิบใน `data/` ใหม่ หรือมีการเปลี่ยนข้อมูลการทำงานของคอร์ด สามารถสั่งสร้างเวกเตอร์เบสใหม่ทั้งหมดได้โดยรัน:
```bash
python main.py --rebuild
```
ระบบจะรัน Pipeline ตั้งแต่ Lab 1 ถึง Lab 4 โดยอัตโนมัติ เพื่อสร้างฐานข้อมูล FAISS ไว้ในโฟลเดอร์ `vector_db/`

### 3. การรันในโหมดควบคุมผ่าน Command Line (CLI Mode)
พิมพ์คำสั่งนี้เพื่อเปิดโหมดตอบคำถามผ่านเทอร์มินัล:
```bash
python main.py
```

### 4. การเปิดใช้งาน Web Application (Server Mode)
หากต้องการเข้าใช้งานโปรแกรมผ่านเว็บบราวเซอร์ที่เป็นหน้าตาแชทบ็อตสุดพรีเมียม ให้เปิดเซิร์ฟเวอร์ด้วยคำสั่ง:
```bash
python main.py --server
# หรือรันตรงผ่าน app.py: python app.py
```
จากนั้นเปิดบราวเซอร์ไปที่หน้าลิงก์: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📖 แหล่งอ้างอิงข้อมูล (Citations & References)
-- ** Guitar Chord Database CSV **: [https://www.gigasheet.com/sample-data/guitar-chord-database](https://www.gigasheet.com/sample-data/guitar-chord-database)
- **guitar-chords-db-json**: [https://github.com/szaza/guitar-chords-db-json](https://github.com/szaza/guitar-chords-db-json)
- **chord-collection**: [https://github.com/T-vK/chord-collection](https://github.com/T-vK/chord-collection)
- **Learn and Master Guitar Lesson Book (PDF)**: [https://www.learnandmaster.com/resources/Learn-and-Master-Guitar-Lesson-Book.pdf](https://www.learnandmaster.com/resources/Learn-and-Master-Guitar-Lesson-Book.pdf)
- **Manual Beginner Guitar (PDF)**: [https://nextlevelguitar.com/resources/pdf/manual_beginner_guitar.pdf](https://nextlevelguitar.com/resources/pdf/manual_beginner_guitar.pdf)
