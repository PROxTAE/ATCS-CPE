# AdvanceML-2026

Repository สำหรับจัดเก็บ LAB และ Final Project วิชา **Advance Machine Learning**
ประจำภาคการศึกษาที่ 1 ปีการศึกษา 2569

## รายละเอียดโฟลเดอร์ (Folder Structure)
- **LAB01** - **LAB10**: โฟลเดอร์เก็บรายงานผลการทดลองรายสัปดาห์
  - [LAB03](file:///d:/Protae/LearningZone/3yTrem1/AdvanceML/LAB/LAB03/README.md) - ระบบสืบค้นและตอบคำถามเกี่ยวกับคอร์ดกีตาร์และทฤษฎีดนตรีด้วย RAG (FastAPI Web Chatbot + FAISS)
- **Final-Project**: โฟลเดอร์เก็บรายงานโครงงานวิจัย/โปรเจกต์สุดท้าย

## รายละเอียด LAB03 (LAB03 Overview)
**ระบบถาม-ตอบความรู้คอร์ดกีตาร์ด้วย RAG (Retrieval-Augmented Generation)**
* **โมเดลและคลังเวกเตอร์**: ใช้ `intfloat/multilingual-e5-large` ในการสร้างเวกเตอร์ประโยค และทำดัชนีด้วย **FAISS CPU (Cosine Similarity)**
* **ฐานข้อมูลแบบไฮบริด**: รองรับการถามตอบทฤษฎีดนตรีทั่วไป และการเข้าถึงคอร์ดเพลงจากรหัสเพลง/แนวเพลงผ่านไฟล์ CSV ขนาดใหญ่
* **การแสดงผล**: ทำงานผ่าน FastAPI Web Service แสดงผลกล่องแชทแนว Glassmorphism พร้อมแก้ไขการขึ้นบรรทัดใหม่ในการจับคอร์ดสายกีตาร์แต่ละเส้นอย่างถูกต้อง

## สมาชิกผู้จัดทำ (Author)
- ชื่อ-นามสกุล (Name): นายนิธิศ มะโนรา
- รหัสนักศึกษา (Student ID): 116730462042-6

## แหล่งอ้างอิง (References)
- **Guitar Chord Database CSV**: https://www.gigasheet.com/sample-data/guitar-chord-database
- **guitar-chords-db-json**: https://github.com/szaza/guitar-chords-db-json
- **chord-collection**: https://github.com/T-vK/chord-collection
- **PDF Lesson Book & manual**: [Learn-and-Master-Guitar](https://www.learnandmaster.com/resources/Learn-and-Master-Guitar-Lesson-Book.pdf), [manual_beginner_guitar](https://nextlevelguitar.com/resources/pdf/manual_beginner_guitar.pdf)
