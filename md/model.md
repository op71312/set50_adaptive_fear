ตกลงครับ เราจะใช้ **SET Trading Calendar ที่เราตรวจสอบแล้วเป็นปฏิทินกลาง** และคุณจะเป็นคนเขียนโค้ดเอง ผมจะช่วยกำหนดหน้าที่ของแต่ละ Cell ตามลำดับ โดยไม่เขียนโค้ดให้ก่อน

ผมเสนอให้สร้าง Notebook ใหม่ชื่อ `04_model_development.ipynb` แยกจาก Feature Engineering เพื่อไม่ให้กระทบข้อมูลเดิม

# **Notebook 04: Model Development**

แบ่งเป็น 6 Sections รวมประมาณ 20 Cells

## **Section 1 — Load & Inspect Master Dataset**

เป้าหมาย: โหลด Master Dataset และตรวจสอบความพร้อมก่อนสร้าง Modeling Dataset

| Cell | หน้าที่             | รายละเอียด                                                   |
| ---- | ------------------- | ------------------------------------------------------------ |
| 1    | Import Libraries    | pandas, numpy, matplotlib, seaborn, sklearn                  |
| 2    | Configuration       | กำหนด Path, ช่วง Train/Validation/Test, Features และ Target  |
| 3    | Load Master Dataset | โหลด `SET50_Master_Dataset.parquet`                          |
| 4    | Basic Inspection    | ตรวจสอบ Shape, Columns, Data Types, Date Range               |
| 5    | Data Integrity      | ตรวจสอบ Duplicate Date+Symbol, Missing Values และ Rank Range |

**ผลลัพธ์ Section 1:** Master Dataset ที่โหลดและตรวจสอบแล้ว โดยไม่แก้ไขข้อมูลต้นฉบับ

## **Section 2 — Target Alignment**

เป้าหมาย: สร้าง Target ให้ตรงกับวันซื้อขายถัดไปจริง

| Cell | หน้าที่                 | รายละเอียด                                                               |
| ---- | ----------------------- | ------------------------------------------------------------------------ |
| 6    | Load Trading Calendar   | โหลดปฏิทิน SET ที่เราตรวจสอบแล้ว                                         |
| 7    | Build Next Trading Date | สร้าง Mapping ระหว่าง Trading Date ปัจจุบันกับวันซื้อขายถัดไป            |
| 8    | Target Alignment        | จับคู่หุ้นในวัน t กับข้อมูลหุ้นตัวเดิมในวันซื้อขายถัดไป                  |
| 9    | Target Construction     | สร้าง Panic, FOMO, Normal ตามนิยามที่ตกลงกัน                             |
| 10   | Target Validation       | ตรวจสอบตัวอย่างการจับคู่วัน t และ t+1 รวมถึง Missing Data และ Membership |

**ข้อกำหนดสำคัญของ Section นี้**

1. วันที่ 11 ส.ค. → 13 ส.ค. 2026 ถือเป็นวันซื้อขายถัดไปตามปฏิทิน SET
2. ถ้าหุ้นไม่มีข้อมูลในวันซื้อขายถัดไปจริง ห้ามข้ามไปจับคู่วันอื่น
3. ใช้ `daily_return` และ `vol_z` ของวัน t+1 ในการสร้าง Target
4. วันสุดท้ายที่ไม่มีวันซื้อขายถัดไปใน Dataset จะไม่มี Target ที่นำไปฝึกได้
5. Target ที่สร้างขึ้นต้องเป็นผลลัพธ์ของวัน t+1 ไม่ใช่วัน t

## **Section 3 — Modeling Dataset**

เป้าหมาย: สร้างตารางสำหรับฝึกโมเดลโดยเฉพาะ

| Cell | หน้าที่                | รายละเอียด                                         |
| ---- | ---------------------- | -------------------------------------------------- |
| 11   | Feature Selection      | เลือก Features ทั้ง 6 ตัว                          |
| 12   | Dataset Assembly       | รวม Features, Target และ Target Date               |
| 13   | Missing Value Handling | คัดตัวอย่างที่ไม่มี Features หรือ Target ที่จำเป็น |
| 14   | Class Distribution     | ตรวจสอบจำนวนและสัดส่วน Panic, FOMO, Normal         |
| 15   | Save Modeling Dataset  | บันทึกเป็น `SET50_Modeling_Dataset.parquet`        |

โครงสร้างที่ต้องการ:

| Date | Symbol | Target_Date | daily_return | momentum_20d | vol_z | VolRank | CorrRank | LiquidityRank | Target |
| ---- | ------ | ----------- | ------------ | ------------ | ----- | ------- | -------- | ------------- | ------ |
| t    | ADVANC | t+1         | ...          | ...          | ...   | ...     | ...      | ...           | Normal |
| t    | AOT    | t+1         | ...          | ...          | ...   | ...     | ...      | ...           | Panic  |
| t+1  | ADVANC | t+2         | ...          | ...          | ...   | ...     | ...      | ...           | FOMO   |

หมายเหตุ: `Corr_60d` ไม่ใช่ Feature ที่เราเลือกใช้ในโมเดลรุ่นแรก จึงไม่ต้องนำเข้ามาใน X

## **Section 4 — Train / Validation / Test Split**

เป้าหมาย: แบ่งข้อมูลตามเวลาโดยไม่มี Look-ahead Bias

| Cell | หน้าที่          | รายละเอียด                              |
| ---- | ---------------- | --------------------------------------- |
| 16   | Temporal Split   | แบ่งตาม Target_Date                     |
| 17   | Split Validation | ตรวจสอบช่วงเวลาและจำนวนตัวอย่างแต่ละชุด |

กำหนดเบื้องต้น:

| Dataset    | Target Date |
| ---------- | ----------- |
| Train      | 2016–2022   |
| Validation | 2023–2024   |
| Test       | 2025–2026   |

สำคัญ: เราแบ่งตาม `Target_Date` ไม่ใช่ `Date` ของ Features

## **Section 5 — Model Training**

เป้าหมาย: ฝึก Softmax Regression

| Cell | หน้าที่               | รายละเอียด                                |
| ---- | --------------------- | ----------------------------------------- |
| 18   | Feature Scaling       | StandardScaler โดย Fit เฉพาะ Train        |
| 19   | Model Training        | Multinomial Logistic Regression           |
| 20   | Hyperparameter Tuning | ปรับ Regularization และ C ด้วย Validation |

โมเดลใช้สมการ:

\\[ P(Y=k\mid X)= \frac{\exp(\beta\_{0,k}+\beta_k^TX)} {\sum\_{j=1}^{3}\exp(\beta\_{0,j}+\beta_j^TX)} \\]

เริ่มต้นด้วย L2 Regularization และไม่เปิด Class Weight โดยอัตโนมัติ

## **Section 6 — Model Evaluation**

เป้าหมาย: ประเมินความสามารถในการทำนาย

| Cell | หน้าที่               | รายละเอียด                             |
| ---- | --------------------- | -------------------------------------- |
| 21   | Validation Evaluation | ประเมิน Log Loss, Macro F1             |
| 22   | Confusion Matrix      | ดูการจำแนกผิดของแต่ละ Class            |
| 23   | Probability Analysis  | ตรวจสอบความน่าจะเป็นทั้งสามสถานะ       |
| 24   | Calibration           | Multiclass Brier Score และ Calibration |
| 25   | Final Test Evaluation | ประเมิน Test ด้วยโมเดลที่เลือกแล้ว     |

## **ภาพรวม Workflow**

**01**

**Load Master Dataset**

โหลดและตรวจสอบข้อมูล

**02**

**Target Alignment**

จับคู่วันซื้อขาย t กับ t+1

**03**

**Modeling Dataset**

สร้าง X และ Y

**04**

**Temporal Split**

แบ่ง Train / Validation / Test

**05**

**Softmax Training**

ฝึกและเลือกโมเดล

**06**

**Evaluation**

ประเมินผลบน Test

Complete

## **ข้อควรระวังที่ผมอยากล็อกไว้ก่อน**

มี 3 เรื่องที่ไม่ควรมองข้าม:

1. **Universe:** Target ต้องตรวจสอบการเป็นสมาชิก SET50 ในวันทำนายด้วย เราควรตกลงว่าจะใช้เฉพาะหุ้นที่เป็นสมาชิกทั้งวัน t และ t+1 หรือไม่
2. **Target Date:** ต้องเก็บไว้เสมอ เพราะใช้แบ่ง Dataset ตามเวลา
3. **Missing Features:** อย่าแทน NaN ด้วย 0 โดยอัตโนมัติ โดยเฉพาะ Rank เพราะ 0 เป็นค่าที่มีความหมายจริง

**ผมแนะนำให้เริ่มทีละ Cell** โดยเริ่ม Cell 1–5 ก่อน เมื่อคุณเขียนเสร็จแล้วส่งผลลัพธ์มาให้ผมตรวจ จากนั้นเราค่อยไป Section 2 โดยเฉพาะ Target Alignment ซึ่งเป็นหัวใจของงานวิจัยนี้ครับ