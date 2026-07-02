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
| Batas temporal | Fitur hanya memakai data yang tersedia sampai hari ke-28 |
| Skala fitur beragam | Klik VLE, hari aktif, dan skor assessment memiliki rentang nilai berbeda |

---

## Slide 6 — Preprocessing Data

**Unit analisis:** 1 mahasiswa × 1 module × 1 presentation

| Sumber | Fitur yang dibentuk |
|---|---|
| studentInfo | gender, region, highest_education, imd_band, age_band, disability, num_of_prev_attempts, studied_credits |
| studentRegistration | date_registration |
| studentAssessment | assessment_count, assessment_score_mean/max/min |
| studentVle | vle_total_clicks, vle_active_days, vle_site_count, vle_last_activity_day |

- **Total fitur model:** 8 kategorikal + 11 numerik
- **Label:** AtRisk = Withdrawn + Fail; Successful = Pass + Distinction
- **Fitur masa depan dikeluarkan:** `date_unregistration`, `has_unregistration`, hasil akhir, dan aktivitas setelah hari ke-28

---

## Slide 7 — Metode Penelitian

**Supervised Binary Classification:**
- Logistic Regression (model dasar, mudah diinterpretasi)
- Random Forest (non-linear, fitur campuran)
- XGBoost (*gradient boosting*, banyak digunakan pada data tabular)

**Evaluasi:** Accuracy, Precision, Recall, F1 — fokus Recall AtRisk (meminimalkan mahasiswa berisiko yang terlewat)

**Knowledge-Based Risk Layer:**
- Rule-based scoring berdasarkan: assessment score, assessment count, VLE clicks, VLE active days
- Output: High Risk / Medium Risk / Low Risk + alasan risiko

**Split:** 80% train+validation, 20% test — dikelompokkan berdasarkan mahasiswa agar tidak ada mahasiswa yang sama di train dan test

**Validasi:** 5-fold cross-validation pada train set → menghasilkan mean ± std untuk menilai konsistensi performa model, sekaligus mengatur agar setiap data pernah menjadi validation tepat satu kali

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
- **Fokus penelitian ini:** menghubungkan prediksi ML + rule-based ke indikator BI

---

## Slide 9 — Hasil Evaluasi Model

**Cross-Validation (5-Fold, dikelompokkan per mahasiswa):**

Setiap fold: ~20.900 baris train, ~5.200 baris validation. Tidak ada mahasiswa yang sama di train dan validation pada fold yang sama.

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 74.84% ± 0.33% | 80.81% ± 0.63% | 68.71% ± 0.38% | 74.27% ± 0.43% |
| **Random Forest** | 75.38% ± 0.33% | 79.99% ± 1.48% | **71.26% ± 0.40%** | **75.36% ± 0.50%** |
| XGBoost | **75.82% ± 0.41%** | **82.17% ± 0.93%** | 69.31% ± 0.33% | 75.19% ± 0.28% |

→ XGBoost unggul pada accuracy, sedangkan Random Forest memiliki recall AtRisk tertinggi sehingga lebih sesuai untuk early warning.

**Test Set (20%, 6.471 baris, 5.757 mahasiswa):**

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 74.76% | 80.40% | 68.69% | 74.08% |
| **Random Forest** | 75.92% | 80.32% | **71.72%** | **75.78%** |
| XGBoost | **76.33%** | **81.86%** | 70.54% | **75.78%** |

- **Model terpilih:** Random Forest (recall tertinggi pada test set)
- False negative kelas AtRisk: 961 dari 3.398 kasus AtRisk belum terdeteksi

**Data Split:**
- Train+Validation: 26.122 baris (23.028 mahasiswa unik)
- Test: 6.471 baris (5.757 mahasiswa unik)
- Pembobotan kelas proporsional pada ketiga model

**Knowledge-Based Risk Layer:**
| Level | Jumlah | Persentase |
|---|---:|---:|
| High Risk | 1.795 | 27.7% |
| Medium Risk | 1.994 | 30.8% |
| Low Risk | 2.682 | 41.4% |

---

## Slide 10 — Analisis Hasil

**Feature Importance (Random Forest):**

Fitur dengan kontribusi tertinggi didominasi sinyal perilaku awal:
- total klik VLE
- hari aktivitas terakhir VLE
- jumlah hari aktif VLE
- jumlah situs VLE yang diakses
- fitur assessment dan registrasi

→ Aktivitas awal di VLE dan assessment menjadi sinyal utama yang membantu model membedakan mahasiswa berisiko.

**Knowledge Layer vs Model:**

| Metrik | Random Forest | RF + Knowledge Layer |
|---|---:|---:|
| Accuracy | **75.92%** | 71.36% |
| Precision AtRisk | **80.32%** | 70.39% |
| Recall AtRisk | 71.72% | **78.49%** |
| F1 AtRisk | **75.78%** | 74.22% |

→ Knowledge layer meningkatkan recall dan memperluas cakupan mahasiswa yang masuk antrean verifikasi.

---

## Slide 11 — Implikasi Business Intelligence

**Dari prediksi ke pendukung keputusan:**
- Jumlah mahasiswa AtRisk per module → prioritas monitoring prodi
- Distribusi High/Medium/Low Risk → alokasi sumber daya untuk *counselling*
- Sinyal risiko (skor assessment rendah, assessment belum dikerjakan, klik VLE rendah, hari aktif rendah) → alasan yang bisa dibaca dosen wali
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
1. Ketiga model menunjukkan performa yang relatif konsisten pada 5-fold CV; XGBoost unggul pada accuracy/ROC-AUC, sedangkan Random Forest terpilih berdasarkan recall AtRisk
2. Split berdasarkan identitas mahasiswa mengurangi risiko data leakage antar split
3. Knowledge-based risk layer meningkatkan recall dari 71,72% menjadi 78,49% dengan konsekuensi precision turun
4. Kombinasi ML + rule-based menghasilkan label prediksi, alasan risiko, dan prioritas monitoring dalam satu keluaran terpadu

**Saran:**
1. Validasi threshold knowledge layer dengan data semester baru
2. Tambahkan fitur temporal harian atau mingguan untuk membaca dinamika engagement
3. Integrasikan output ke LMS institusi jika ingin dikembangkan sebagai dashboard operasional
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
