# Analisis Risiko Dropout Mahasiswa Menggunakan Supervised Learning dan Knowledge-Based Risk Layer pada OULAD
## Data Visualization and Business Intelligence

---

## Slide 1 — Judul

- **Judul:** Analisis Risiko Dropout Mahasiswa Menggunakan Supervised Learning dan Knowledge-Based Risk Layer pada Open University Learning Analytics Dataset
- **Kelompok 5:**
  - Muhammad Rizky Hajar (24.55.2714)
  - Alwie Muflich (24.55.2667)
  - Heri Santosa (24.55.2676)
- **Program:** S2 PJJ Informatika — Konsentrasi Big Data & Predictive Analytics
- **Universitas Amikom Yogyakarta**
- **Dosen Pengampu:** Robert Marco, M.T., Ph.D
- **Dosen Supervisi:** Dr. Andi Sunyoto, M.Kom

---

## Slide 2 — Latar Belakang

- Dropout mahasiswa merupakan permasalahan serius dalam pengelolaan pendidikan tinggi
- Dampak: capaian akademik mahasiswa, efektivitas layanan, dan evaluasi kinerja institusi
- Identifikasi dini mahasiswa berisiko memungkinkan intervensi tepat sasaran sebelum terlambat
- Saat ini tersedia data akademik, registrasi, dan jejak digital yang dapat diolah
- Dalam konteks DVBI: hasil analitik harus diterjemahkan menjadi indikator yang dapat ditindaklanjuti untuk monitoring dan pengambilan keputusan

---

## Slide 3 — Rumusan Masalah & Tujuan

**Rumusan Masalah:**
1. Bagaimana membangun model klasifikasi risiko dropout mahasiswa menggunakan supervised learning?
2. Bagaimana knowledge-based risk layer dapat memberikan interpretasi tambahan terhadap hasil prediksi?
3. Bagaimana keluaran model dapat dipetakan menjadi indikator pendukung keputusan dalam konteks BI?

**Tujuan:**
1. Membangun model binary classification (AtRisk vs Successful) dengan 3 algoritma
2. Merancang knowledge-based risk layer untuk menjelaskan faktor risiko
3. Memetakan keluaran ke indikator monitoring dan peringatan dini

---

## Slide 4 — Dataset Penelitian

- **Dataset:** Open University Learning Analytics Dataset (OULAD)
- **Ukuran:** 32.593 student-module-presentation
- **Sumber tabel:** studentInfo, studentRegistration, studentAssessment, studentVle
- **Module:** 7 modul (AAA, BBB, CCC, DDD, EEE, FFF, GGG)
- **Presentation:** 4 periode (2013B, 2013J, 2014B, 2014J)
- **Distribusi label:**
  - AtRisk (Withdrawn + Fail): 17.208 (52.8%)
  - Successful (Pass + Distinction): 15.385 (47.2%)

---

## Slide 5 — Tantangan Data

| Tantangan | Detail |
|---|---|
| Multi-table join | 4 tabel berbeda perlu digabung ke satu unit analisis |
| Volume besar | studentVle memiliki >10 juta baris yang harus diagregasi |
| Missing value | Indeks deprivasi kosong pada sebagian data → diisi "Unknown" |
| Sinyal unregistration | 30.9% mahasiswa memiliki tanggal unregistration |
| Skala fitur beragam | Klik VLE (0–24.139) vs assessment count (0–14) |

---

## Slide 6 — Preprocessing Data

**Unit analisis:** 1 mahasiswa × 1 module × 1 presentation

| Sumber | Fitur yang dibentuk |
|---|---|
| studentInfo | gender, region, highest_education, imd_band, age_band, disability, num_of_prev_attempts, studied_credits |
| studentRegistration | date_registration, date_unregistration, has_unregistration |
| studentAssessment | assessment_count, assessment_score_mean/max/min |
| studentVle | vle_total_clicks, vle_active_days, vle_site_count, vle_last_activity_day |

- **Total fitur:** 21 (8 kategorikal + 13 numerik)
- **Label:** AtRisk = Withdrawn + Fail; Successful = Pass + Distinction

---

## Slide 7 — Metode Penelitian

**Supervised Binary Classification:**
- Logistic Regression (model dasar, mudah diinterpretasi)
- Random Forest (non-linear, fitur campuran)
- XGBoost (*gradient boosting*, unggul pada data tabular)

**Evaluasi:** Accuracy, Precision, Recall, F1 — fokus Recall AtRisk (meminimalkan mahasiswa berisiko yang terlewat)

**Knowledge-Based Risk Layer:**
- Rule-based scoring berdasarkan: assessment score, assessment count, VLE clicks, VLE active days, sinyal unregistration
- Output: High Risk / Medium Risk / Low Risk + alasan risiko

**Split:** 80% train+validation, 20% test — dikelompokkan berdasarkan mahasiswa agar tidak ada mahasiswa yang sama di train dan test

**Validasi:** 5-fold cross-validation pada train set → menghasilkan mean ± std untuk membuktikan stabilitas model, sekaligus memastikan setiap data pernah menjadi validation tepat satu kali

**Imbalance Handling:** Pembobotan kelas proporsional pada ketiga algoritma

---

## Slide 8 — Tinjauan Pustaka

- 10 paper relevan (2020–2025) dianalisis
- Metode dominan: Random Forest, XGBoost, clustering, deep learning, AutoML
- Variabel umum: performa akademik, demografi, *engagement* LMS, jejak digital
- **Gap utama yang ditemukan:**
  - Penelitian sebelumnya fokus pada prediksi dan metrik model
  - Visual analytics untuk pengambil keputusan belum dikembangkan secara operasional
  - Kaitan antara model, monitoring, dan action plan intervensi masih terbuka
- **Kontribusi penelitian ini:** menghubungkan prediksi ML + rule-based langsung ke indikator BI

---

## Slide 9 — Hasil Evaluasi Model

**Cross-Validation (5-Fold, dikelompokkan per mahasiswa):**

Setiap fold: ~20.900 baris train, ~5.200 baris validation. Tidak ada mahasiswa yang sama di train dan validation pada fold yang sama.

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 93.65% ± 0.29% | 97.39% ± 0.22% | 90.41% ± 0.74% | 93.77% ± 0.33% |
| Random Forest | 94.19% ± 0.28% | 97.76% ± 0.27% | 91.10% ± 0.60% | 94.31% ± 0.32% |
| **XGBoost** | **94.41% ± 0.31%** | **97.82% ± 0.18%** | **91.47% ± 0.67%** | **94.53% ± 0.34%** |

→ Standar deviasi rendah (~0.3–0.7%) menunjukkan performa stabil di seluruh fold.

**Test Set (20%, 6.471 baris, 5.757 mahasiswa):**

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 93.09% | 97.34% | 89.29% | 93.14% |
| **Random Forest** | **93.77%** | **97.65%** | **90.32%** | **93.84%** |
| XGBoost | 93.94% | 98.02% | 90.29% | 94.00% |

- **Model terpilih:** Random Forest (recall tertinggi pada test set)
- Tingkat kegagalan deteksi: hanya 329 dari 3.398 mahasiswa AtRisk yang tidak terdeteksi (9,7%)

**Data Split:**
- Train+Validation: 26.122 baris (23.028 mahasiswa unik)
- Test: 6.471 baris (5.757 mahasiswa unik)
- Pembobotan kelas proporsional pada ketiga model

**Knowledge-Based Risk Layer:**
| Level | Jumlah | Persentase |
|---|---:|---:|
| Low Risk | 22.168 | 68.0% |
| High Risk | 6.508 | 20.0% |
| Medium Risk | 3.917 | 12.0% |

---

## Slide 10 — Analisis Hasil

**Feature Importance (XGBoost Top 5):**

| Rank | Fitur | Importance |
|---|---|---:|
| 1 | assessment_count | 0.371 |
| 2 | vle_last_activity_day | 0.132 |
| 3 | has_unregistration | 0.081 |
| 4 | date_unregistration | 0.060 |
| 5 | assessment_score_mean | 0.052 |

→ Partisipasi assessment dan aktivitas terakhir di VLE adalah prediktor terkuat.

**Modul dengan Risiko Tertinggi:**

| Module-Presentation | % AtRisk |
|---|---:|
| CCC-2014B | 65.0% |
| CCC-2014J | 60.1% |
| DDD-2014B | 59.8% |

**Cross-tab Knowledge Layer vs Model:**

| Knowledge Level | Predicted AtRisk | Predicted Successful | Agreement |
|---|---:|---:|---|
| High Risk | 1.288 | 0 | 100% → AtRisk |
| Medium Risk | 750 | 7 | 99.1% → AtRisk |
| Low Risk | 1.105 | 3.321 | 75.0% → Successful |

→ Knowledge layer dan model sangat konsisten di area High/Medium Risk. Model menangkap 1.105 kasus tambahan pada kelompok Low Risk yang teridentifikasi AtRisk melalui pola data yang lebih kompleks.

---

## Slide 11 — Implikasi Business Intelligence

**Dari prediksi ke pendukung keputusan:**
- Jumlah mahasiswa AtRisk per module → prioritas monitoring prodi
- Distribusi High/Medium/Low Risk → alokasi sumber daya untuk *counselling*
- Sinyal risiko (skor assessment rendah, aktivitas VLE rendah, sinyal unregistration) → alasan yang bisa dibaca dosen wali
- Antrean intervensi: daftar prioritas mahasiswa yang berpotensi membutuhkan tindak lanjut, yang efektivitasnya dapat dievaluasi pada implementasi berikutnya

**Stakeholder:**
- Pimpinan akademik → ringkasan risiko per module
- Program studi → identifikasi modul bermasalah
- Dosen wali/tutor → daftar mahasiswa prioritas + alasan
- Tim *counselling* → sinyal peringatan dini

**Dashboard telah diimplementasi sebagai purwarupa monitoring akademik.**

---

## Slide 12 — Kesimpulan & Saran

**Kesimpulan:**
1. Ketiga model menunjukkan performa stabil melalui 5-fold CV (std < 0.7%), dengan XGBoost terbaik di CV dan Random Forest terpilih berdasarkan recall tertinggi pada test set
2. Split berdasarkan identitas mahasiswa memastikan tidak ada data leakage; evaluasi valid secara metodologis
3. Knowledge-based risk layer konsisten dengan model (agreement 99–100% untuk High/Medium Risk)
4. Kombinasi ML + rule-based menghasilkan label prediksi, alasan risiko, dan prioritas monitoring dalam satu keluaran terpadu

**Saran:**
1. Validasi threshold knowledge layer dengan data semester baru
2. Tambahkan temporal features (per-minggu) untuk early prediction lebih awal
3. Integrasikan output ke LMS institusi sebagai dashboard real-time
4. Lakukan evaluasi efektivitas intervensi berbasis output model

---

## Slide 13 — Dashboard

- Tampilan utama: ringkasan risiko seluruh mahasiswa
- Breakdown risiko per module-presentation
- Antrean intervensi: daftar mahasiswa prioritas tinggi
- Detail sinyal risiko per mahasiswa individu

---

## Slide 14 — Referensi Utama

- [1] Aulck et al., "Using ML to predict student retention from socio-demographic characteristics and app-based engagement metrics," 2023
- [2] Karpenko et al., "Hybrid approach to predicting learning success based on digital educational history," 2024
- [3] Delnoij et al., "Early warning systems for more effective student counselling in higher education," 2022
- [4] Kuzilek et al., "Open University Learning Analytics Dataset," Scientific Data, 2017
- [5] Alturki & Aldraiweesh, "Predicting student dropout from day one: XGBoost-based early warning system," 2025
- [6] Karlos et al., "Assisting educational analytics with AutoML functionalities," 2022
- [7] Chung & Lee, "Precision education with statistical learning and deep learning," 2020
- [8] Sarker et al., "Multi-class phased prediction of academic performance and dropout," 2023
- [9] Iatrellis et al., "Study regarding the influence of personality and LMS usage profile on learning performance," 2024
- [10] Berens et al., "Crossing individual university boundaries: a comprehensive approach to predicting dropouts," 2025


