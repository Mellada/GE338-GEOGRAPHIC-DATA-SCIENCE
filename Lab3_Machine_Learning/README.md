# GE338 - Lab 3: Machine Learning Land Use Classification (Sukhothai)

## Study Area

พื้นที่ศึกษา: จังหวัดสุโขทัย ประเทศไทย
ข้อมูลดาวเทียม: Sentinel-2 Surface Reflectance (2023)
ความละเอียดเชิงพื้นที่: 10 เมตร

---

# 1. Training Strategy

## จำนวน Class และนิยาม

ใช้ทั้งหมด 4 Class:

| Class       | คำอธิบาย                         |
| ----------- | -------------------------------- |
| Urban       | พื้นที่สิ่งปลูกสร้าง เมือง ถนน   |
| Water       | แหล่งน้ำ เช่น แม่น้ำ อ่างเก็บน้ำ |
| Agriculture | พื้นที่เกษตรกรรม พืชไร่ นาข้าว   |
| Bare_soil   | ดินเปล่า พื้นที่ไม่มีพืชคลุม     |

เลือก 4 class เพื่อให้แยกประเภทหลักของพื้นที่ชุ่มน้ำและเกษตรกรรมได้ชัดเจน

---

## วิธีสร้าง Training Samples

ใช้วิธี:

* Digitize จุดตัวอย่างด้วยตนเองใน Google Earth Engine
* อ้างอิงภาพ False Color และ True Color
* กระจายจุดให้ครอบคลุมพื้นที่ศึกษา

จำนวน Training samples ทั้งหมด: 400 จุด

---

## Train / Validation Split

ใช้การแบ่งแบบสุ่ม:

* Train: 80%
* Validation: 20%

| Dataset    | จำนวน |
| ---------- | ----- |
| Train      | 327   |
| Validation | 73    |

ข้อดีของ random split:

* ง่ายและเหมาะกับข้อมูลขนาดเล็ก
* ลด bias จากตำแหน่ง

ข้อเสีย:

* มี spatial autocorrelation
* accuracy อาจสูงกว่าความจริง

---

## Feature Selection

ใช้ทั้ง Spectral Bands และ Spectral Indices

### Spectral Bands

* B2 (Blue)
* B3 (Green)
* B4 (Red)
* B8 (NIR)
* B11 (SWIR1)
* B12 (SWIR2)

### Spectral Indices

* NDVI
* NDWI
* NDBI
* BSI

เหตุผล:

* NDVI แยกพืช
* NDWI แยกน้ำ
* NDBI แยกเมือง
* BSI แยกดินเปล่า

---

# 2. Algorithm Comparison

ทดสอบ 3 อัลกอริทึม:

* Random Forest
* CART
* SVM

## ผลการเปรียบเทียบ

| Model         | Overall Accuracy | Kappa |
| ------------- | ---------------- | ----- |
| Random Forest | 0.849            | 0.798 |
| CART          | 0.876            | 0.824 |
| SVM           | 0.849            | 0.798 |

ผลลัพธ์:

* CART ให้ค่า Accuracy สูงสุด
* Random Forest และ SVM ให้ผลใกล้เคียงกัน
* CART ทำงานดีใน dataset ขนาดเล็ก

ดังนั้น CART เป็นโมเดลที่ดีที่สุดสำหรับ dataset นี้

---

# 3. Confusion Matrix (Random Forest)

| Reference \ Predicted | Urban | Water | Agriculture | Bare_soil |
| --------------------- | ----- | ----- | ----------- | --------- |
| Urban                 | 14    | 0     | 0           | 1         |
| Water                 | 0     | 21    | 0           | 0         |
| Agriculture           | 0     | 0     | 14          | 4         |
| Bare_soil             | 2     | 2     | 2           | 13        |

Class ที่สับสนมากที่สุด:

* Agriculture vs Bare_soil

สาเหตุ:

* spectral signature คล้ายกัน
* พื้นที่เกษตรหลังเก็บเกี่ยวมีลักษณะเหมือนดินเปล่า

---

# 4. Feature Importance (Random Forest)

อันดับความสำคัญ:

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

Interpretation:

* NDWI สำคัญที่สุด เพราะช่วยแยกน้ำได้ดี
* NDVI ช่วยแยกพืช
* SWIR bands ช่วยแยกดินและ built-up
* NDBI มีความสำคัญต่ำ เนื่องจาก built-up ในพื้นที่มีน้อย

---

# 5. Model Uncertainty

Class ที่โมเดลสับสนมากที่สุด:

* Agriculture และ Bare soil

พื้นที่ที่ไม่แน่ใจ:

* พื้นที่เกษตรช่วงหลังเก็บเกี่ยว
* พื้นที่ดินแห้ง

Confidence ของโมเดล:

* Water มีความแม่นยำสูง
* Urban มีจำนวนตัวอย่างน้อย ทำให้ความไม่แน่นอนสูง

---

# 6. Effect of Increasing Training Samples

หากเพิ่ม Training samples เป็น 2 เท่า:

* คาดว่า Accuracy จะเพิ่มขึ้น
* โดยเฉพาะ Urban class
* ลด confusion ระหว่าง Agriculture และ Bare soil

เหตุผล:

* โมเดลเรียนรู้ pattern ได้ดีขึ้น
* ลด bias

---

# 7. Spatial Autocorrelation

Training points อยู่ใกล้กัน
ส่งผลให้:

* Accuracy สูงเกินจริง
* validation ไม่อิสระ

วิธีแก้:

* spatial cross-validation
* แยกพื้นที่ training / testing

---

# 8. Worst Performing Class

Bare soil ทำได้แย่ที่สุด

วิธีปรับปรุง:

* เพิ่ม training samples
* เพิ่ม dry season image
* ใช้ texture features

---

# 9. Transfer to Other Area

ต้องเปลี่ยน:

* ROI
* Training samples
* seasonal period

ใช้ซ้ำได้:

* code structure
* feature selection
* algorithm setup

---

# 10. Conclusion

* CART ให้ผลดีที่สุดใน dataset นี้
* Random Forest มีข้อดีด้าน interpretability
* Spectral indices ช่วยเพิ่ม accuracy
* Agriculture และ Bare soil สับสนมากที่สุด
* การเพิ่ม training samples จะช่วยปรับปรุงผลลัพธ์

Accuracy สูงสุดที่ได้:
0.876 (CART)

โมเดลที่เลือก:
CART

