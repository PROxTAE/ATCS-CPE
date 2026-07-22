$labs = 1..10 | ForEach-Object { "LAB{0:D2}" -f $_ }
foreach ($lab in $labs) {
    New-Item -ItemType Directory -Force -Path $lab
    $readmeContent = @"
# `${lab}: [ชื่อใบงาน / Lab Title]

รายละเอียดของใบงาน `${lab} (Description of `${lab})

## สมาชิกผู้จัดทำ (Author)
- ชื่อ-นามสกุล (Name): นายนิธิศ มะโนรา
- รหัสนักศึกษา (Student ID): 116730462042-6

## รายละเอียดไฟล์ในโฟลเดอร์ (Folder Structure)
- Source Code (.ipynb หรือ .py)
- Dataset (ถ้ามี)
- report.pdf (รายงานผลการทดลองถ้ามี)
- README.md (ไฟล์คำอธิบาย)

## แหล่งอ้างอิงข้อมูล (Citations & References)
- [ระบุแหล่งที่มาของข้อมูล/โมเดล/โค้ดที่นำมาอ้างอิง หรือลิงก์ URL]
"@
    Set-Content -Path "$lab\README.md" -Value $readmeContent -Encoding utf8
}

New-Item -ItemType Directory -Force -Path "Final-Project\source_code"
New-Item -ItemType Directory -Force -Path "Final-Project\dataset"

Set-Content -Path "Final-Project\source_code\.gitkeep" -Value ""
Set-Content -Path "Final-Project\dataset\.gitkeep" -Value ""

$finalReadme = @"
# Final Project: [ชื่อโครงการ / Project Title]

รายละเอียดโครงงานวิจัย/โปรเจกต์สุดท้าย (Final Project Description)

## สมาชิกผู้จัดทำ (Author)
- ชื่อ-นามสกุล (Name): นายนิธิศ มะโนรา
- รหัสนักศึกษา (Student ID): 116730462042-6

## โครงสร้างโฟลเดอร์ (Folder Structure)
- ``source_code/`` - โฟลเดอร์เก็บโค้ดทั้งหมด
- ``dataset/`` - โฟลเดอร์เก็บข้อมูลหรือลิงก์ดาวน์โหลดข้อมูล
- ``report.pdf`` - รายงานโครงงานฉบับสมบูรณ์
- ``README.md`` - เอกสารอธิบายรายละเอียดโครงงาน

## แหล่งอ้างอิงข้อมูล (Citations & References)
- [ระบุแหล่งที่มาของข้อมูล/โมเดล/โค้ดที่นำมาอ้างอิง หรือลิงก์ URL]
"@

Set-Content -Path "Final-Project\README.md" -Value $finalReadme -Encoding utf8
