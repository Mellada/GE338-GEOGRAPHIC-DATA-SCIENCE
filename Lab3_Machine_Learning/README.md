# GE338 Lab 3: Land Use Classification (Sukhothai)

## พื้นที่ศึกษา

จังหวัดสุโขทัย ประเทศไทย
ข้อมูล: Sentinel-2 Surface Reflectance ปี 2023
ความละเอียด: 10 เมตร

---

# ภารกิจที่ 1: Training Strategy

## จะใช้ประเภทที่ดินกี่ Class?

ใช้ 4 Class ได้แก่

| Class       | คำอธิบาย                       |
| ----------- | ------------------------------ |
| Urban       | พื้นที่เมือง สิ่งปลูกสร้าง ถนน |
| Water       | แหล่งน้ำ                       |
| Agriculture | พื้นที่เกษตรกรรม               |
| Bare_soil   | ดินเปล่า                       |

เลือก 4 class เพื่อให้แยกพื้นที่เกษตรและพื้นที่ชุ่มน้ำได้ชัดเจน

---

## จะหา Training Samples อย่างไร?

ใช้การ digitize จุดตัวอย่างด้วยตนเองใน Google Earth Engine
อ้างอิงภาพ True color และ False color
กระจายจุดให้ครอบคลุมพื้นที่ศึกษา

จำนวน training samples = 400 จุด

---

## จะแบ่ง Train/Validation อย่างไร?

ใช้ random split 80/20

| Dataset    | จำนวน |
| ---------- | ----- |
| Train      | 327   |
| Validation | 73    |

ข้อดี:

* ง่ายและเหมาะกับข้อมูลน้อย

ข้อเสีย:

* มี spatial autocorrelation
* accuracy อาจสูงกว่าความจริง

---

## Feature ที่ใช้มีอะไรบ้าง?

Spectral Bands:
B2, B3, B4, B8, B11, B12

Spectral Indices:
NDVI, NDWI, NDBI, BSI

เหตุผล:

* NDVI แยกพืช
* NDWI แยกน้ำ
* NDBI แยกเมือง
* BSI แยกดินเปล่า

---

# ภารกิจที่ 2: เปรียบเทียบอัลกอริทึม

ทดลอง 3 อัลกอริทึม

* Random Forest
* CART
* SVM

## ผลการเปรียบเทียบ

| Model         | Overall Accuracy | Kappa |
| ------------- | ---------------- | ----- |
| Random Forest | 0.849            | 0.798 |
| CART          | 0.876            | 0.824 |
| SVM           | 0.849            | 0.798 |

CART ให้ค่า accuracy สูงที่สุด

---

# ภารกิจที่ 3: Feature Importance

Feature ที่สำคัญที่สุดคือ NDWI และ NDVI

| Rank | Feature |
| ---- | ------- |
| 1    | NDWI    |
| 2    | NDVI    |
| 3    | B12     |
| 4    | B11     |
| 5    | B4      |
| 6    | B2      |
| 7    | B3      |
| 8    | B8      |
| 9    | BSI     |
| 10   | NDBI    |

NDWI สำคัญเพราะแยกน้ำได้ดี
NDVI ช่วยแยกพืช
SWIR bands ช่วยแยกดินและ built-up

---

# ภารกิจที่ 4: ความไม่แน่นอนของโมเดล

Class ที่สับสนมากที่สุดคือ
Agriculture และ Bare_soil

สาเหตุ:

* spectral signature คล้ายกัน
* พื้นที่เกษตรหลังเก็บเกี่ยวมีลักษณะเหมือนดินเปล่า

---

# คำถามเพิ่มเติม

## ถ้าเพิ่ม Training Samples อีก 2 เท่า Accuracy จะเพิ่มหรือไม่?

คาดว่า accuracy จะเพิ่มขึ้น โดยเฉพาะ Urban class
เนื่องจากโมเดลมีข้อมูลเรียนรู้มากขึ้น

---

## Spatial Autocorrelation มีผลอย่างไร?

training samples อยู่ใกล้กัน
ทำให้ accuracy สูงเกินจริง
validation ไม่เป็นอิสระ

---

## Class ที่โมเดลทำได้แย่ที่สุดคืออะไร?

Bare_soil

วิธีปรับปรุง:

* เพิ่ม training samples
* ใช้ภาพช่วงฤดูแล้ง
* เพิ่ม texture feature

---

## ถ้าทำพื้นที่อื่น ต้องเปลี่ยนอะไร?

ต้องเปลี่ยน:

* ROI
* Training samples
* seasonal period

ใช้ซ้ำได้:

* code structure
* feature selection
* algorithm

---

# สรุปผล

CART ให้ผลดีที่สุด
Accuracy สูงสุด = 0.876

Random Forest และ SVM ให้ผลใกล้เคียงกัน

Spectral indices ช่วยเพิ่มความแม่นยำ
Agriculture และ Bare soil สับสนมากที่สุด
