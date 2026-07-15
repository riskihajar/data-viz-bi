# IV. Results

## A. Dataset and Validation Results

Dataset hasil preprocessing memuat 32.593 student-module-presentation dari 28.785 mahasiswa unik. Kelas `AtRisk` berjumlah 17.208 baris dan kelas `Successful` berjumlah 15.385 baris. Train-validation memuat 26.122 baris, sedangkan hold-out test memuat 6.471 baris dengan 3.398 kasus `AtRisk` dan 3.073 kasus `Successful`. Pemisahan berbasis `id_student` menghasilkan overlap mahasiswa sebesar nol.

Komposisi target pada dataset pemodelan relatif berimbang, sehingga evaluasi model tidak berangkat dari dominasi satu kelas yang ekstrem. Keseimbangan ini menjadi titik awal yang penting karena tujuan penelitian bukan hanya memperoleh accuracy tinggi, tetapi juga menjaga kemampuan model mengenali mahasiswa yang masuk kelompok `AtRisk`.

![Fig. 1. Distribusi target pada dataset pemodelan.](figures/fig-1a-target-distribution.png)

Pemeriksaan kualitas data kemudian dilakukan sebelum model dilatih. Missing value terutama muncul pada `imd_band`, dengan jumlah yang jauh lebih kecil pada `date_registration`. Dua kondisi tersebut ditangani di dalam pipeline berdasarkan data train-validation agar proses imputasi tidak membawa informasi dari hold-out test.

![Fig. 2. Missing value pada fitur dataset pemodelan.](figures/fig-1b-missing-values.png)

## B. Cross-Validation Performance

Tabel I menunjukkan rata-rata hasil 5-fold GroupKFold. Random Forest menghasilkan recall `AtRisk` tertinggi sebesar 0,7107. XGBoost menghasilkan accuracy, F1-score, dan ROC-AUC tertinggi, masing-masing sebesar 0,7584, 0,7522, dan 0,8440. Berdasarkan kriteria pemilihan yang memprioritaskan recall, Random Forest dipilih sebagai model final.

**Table I. Hasil 5-Fold GroupKFold pada Train-Validation**

| Metrik | Logistic Regression | Random Forest | XGBoost |
|---|---:|---:|---:|
| Accuracy | 0,7496 ± 0,0039 | 0,7524 ± 0,0013 | **0,7584 ± 0,0024** |
| Precision AtRisk | 0,8090 ± 0,0059 | 0,7989 ± 0,0136 | **0,8215 ± 0,0096** |
| Recall AtRisk | 0,6889 ± 0,0064 | **0,7107 ± 0,0085** | 0,6938 ± 0,0029 |
| F1 AtRisk | 0,7442 ± 0,0059 | 0,7521 ± 0,0030 | **0,7522 ± 0,0039** |
| ROC-AUC | 0,8330 ± 0,0027 | 0,8362 ± 0,0023 | **0,8440 ± 0,0019** |

## C. Hold-Out Test Performance

Tabel II memperlihatkan performa pada hold-out test. Random Forest mencapai accuracy 0,7594, precision `AtRisk` 0,8007, recall 0,7213, F1-score 0,7589, dan ROC-AUC 0,8396. XGBoost menghasilkan accuracy 0,7611 dan ROC-AUC 0,8443, sedangkan recall `AtRisk` berada pada 0,7045. Logistic Regression menghasilkan recall 0,6904.

**Table II. Performa Model pada Hold-Out Test**

| Metrik | Logistic Regression | Random Forest | XGBoost |
|---|---:|---:|---:|
| Accuracy | 0,7487 | 0,7594 | **0,7611** |
| Precision AtRisk | 0,8034 | 0,8007 | **0,8154** |
| Recall AtRisk | 0,6904 | **0,7213** | 0,7045 |
| F1 AtRisk | 0,7426 | **0,7589** | 0,7559 |
| ROC-AUC | 0,8311 | 0,8396 | **0,8443** |

Classification report Random Forest menunjukkan precision 0,80, recall 0,72, dan F1-score 0,76 pada 3.398 kasus `AtRisk`. Pada 3.073 kasus `Successful`, precision mencapai 0,72, recall 0,81, dan F1-score 0,76. Weighted average F1-score mencapai 0,76. Perbandingan metrik antar model menempatkan Random Forest sebagai pilihan yang paling relevan untuk konteks early warning karena recall `AtRisk` menjadi ukuran yang paling dekat dengan kebutuhan menemukan mahasiswa berisiko sejak awal.

![Fig. 3. Perbandingan metrik AtRisk pada hold-out test.](figures/fig-2a-metrics-comparison.png)

Setelah model dipilih, pola kesalahan Random Forest diperiksa untuk memahami risiko operasionalnya. Model tersebut berhasil mengenali 2.451 kasus `AtRisk` dan melewatkan 947 kasus yang masuk kelompok berisiko. Hasil ini menggambarkan cakupan deteksi model sebelum keluaran prediksi diterjemahkan menjadi prioritas intervensi.

![Fig. 4. Confusion matrix Random Forest pada hold-out test.](figures/fig-2b-confusion-matrix.png)

Kurva ROC memberikan konteks tambahan terhadap perbedaan antar model. Ketiga kurva berada cukup berdekatan, sehingga selisih ROC-AUC perlu dibaca bersama tujuan keputusan. Dalam penelitian ini, kemampuan memperluas cakupan deteksi lebih diprioritaskan daripada memilih model hanya berdasarkan peringkat ROC-AUC.

![Fig. 5. Kurva ROC pada hold-out test.](figures/fig-2c-roc-curve.png)

Kontribusi fitur Random Forest memperlihatkan bahwa sinyal perilaku awal menjadi pembeda utama. Total klik VLE, hari aktivitas terakhir, jumlah hari aktif, dan ragam situs yang diakses muncul sebagai prediktor teratas, diikuti fitur assessment dan registrasi. Temuan ini selaras dengan tujuan early warning karena model banyak bertumpu pada jejak engagement yang sudah tersedia sampai akhir minggu keempat. Nilai importance tetap dibaca sebagai kontribusi prediktif, bukan bukti hubungan sebab akibat.

![Fig. 6. Lima belas fitur dengan feature importance tertinggi pada Random Forest.](figures/fig-3-feature-importance.png)

## D. Benchmark with OULAD Studies

Tabel III membandingkan hasil penelitian dengan lima studi yang memakai OULAD. Shou et al. mengevaluasi MTAPSP harian pada 20% durasi course dengan target `Pass` serta `Distinction` terhadap `Fail` serta `Withdrawn` [5]. Jawad et al. menggunakan data sampai 260 hari dan SMOTE [6]. Balabied dan Eid menggunakan split 80:20 pada klasifikasi biner [7]. Ujkani et al. dan Alnasyan et al. menggabungkan `Fail` serta `Withdrawn` sebagai kelompok at-risk [8], [9]. Perbedaan horizon, desain split, balancing, dan arsitektur model menjadi konteks pembacaan angka.

**Table III. Benchmark Hasil pada Penelitian Berbasis OULAD**

| Penelitian | Skenario | Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---:|---:|---:|---:|---:|
| Shou et al. [5] | 20% durasi course, target biner | MTAPSP (daily) | 0,9179 | - | - | 0,9180 | - |
| Jawad et al. [6] | 260 hari + SMOTE | Random Forest | 0,8920 | - | - | - | 0,9600 |
| Balabied dan Eid [7] | Klasifikasi biner | Random Forest | 0,9000 | 0,9000 | 0,9000 | 0,9000 | - |
| Ujkani et al. [8] | `Fail` + `Withdrawn` sebagai at-risk | Custom Neural Network | 0,9300 | 0,9500 | 0,9700 | 0,9600 | - |
| Alnasyan et al. [9] | `Pass` + `Distinction` vs `Fail` + `Withdrawn` | KANFormer | 0,9459 | 0,9495 | 0,9482 | 0,9481 | 0,9835 |
| Penelitian ini | Cut-off hari ke-28, group split | Random Forest | 0,7594 | 0,8007 | 0,7213 | 0,7589 | 0,8396 |

## E. Knowledge-Based Risk Layer

Threshold kuartil bawah data train-validation adalah skor assessment 0, jumlah assessment 0, total klik VLE 47, dan hari aktif VLE 4. Nilai nol pada indikator assessment menunjukkan bahwa sebagian mahasiswa belum mengumpulkan assessment sampai akhir minggu keempat. Knowledge layer menghasilkan 1.816 `High Risk`, 1.979 `Medium Risk`, dan 2.676 `Low Risk` pada hold-out test.

Tabel IV membandingkan Random Forest dengan sistem gabungan. Knowledge layer meningkatkan recall dari 0,7213 menjadi 0,7866. Precision berubah dari 0,8007 menjadi 0,7043, sedangkan accuracy berubah dari 0,7594 menjadi 0,7146. Perubahan tersebut menunjukkan perluasan cakupan deteksi disertai peningkatan jumlah alarm yang memerlukan verifikasi stakeholder.

**Table IV. Perbandingan Model dan Knowledge-Based Risk Layer**

| Metrik | Random Forest | RF + Knowledge Layer |
|---|---:|---:|
| Accuracy | **0,7594** | 0,7146 |
| Precision AtRisk | **0,8007** | 0,7043 |
| Recall AtRisk | 0,7213 | **0,7866** |
| F1 AtRisk | **0,7589** | 0,7432 |

## F. Business Intelligence Output

Dashboard mengidentifikasi 3.795 student-module-presentation dalam antrean `High Risk` atau `Medium Risk`. Sinyal paling dominan adalah skor assessment rendah dengan 2.341 kasus. Module GGG presentation 2014J memiliki proporsi prioritas tertinggi pada hold-out test, yaitu 100% kasus `High Risk` atau `Medium Risk`. Indikator tersebut berfungsi sebagai sinyal untuk peninjauan konteks modul dan kapasitas intervensi.

Daftar prioritas menyajikan identitas anonim mahasiswa, module-presentation, probabilitas `AtRisk`, level risiko, jumlah sinyal, alasan, dan rekomendasi. Struktur tersebut menghubungkan hasil model dengan tindakan seperti monitoring akses VLE, pendampingan assessment, serta konseling akademik.

Keluaran analitik kemudian diterjemahkan ke dalam dashboard agar hasil model dapat dibaca sebagai prioritas tindakan, bukan hanya sebagai angka evaluasi. Tampilan tersebut menghubungkan KPI risiko, level prioritas, konsentrasi module-presentation, distribusi probabilitas, sinyal dominan, perbandingan perilaku, confusion matrix, dan trade-off setelah knowledge layer. Dengan susunan ini, pengguna dapat bergerak dari ringkasan strategis menuju penelusuran kelompok atau mahasiswa yang membutuhkan tindak lanjut.

![Fig. 7. Dashboard early warning OULAD pada akhir minggu keempat.](figures/fig-4-dashboard-dvbi.png)
