# IV. Results

## A. Dataset and Validation Results

Dataset hasil olahan memuat 32.593 student-module-presentation dari 28.785 mahasiswa unik. Kelas `AtRisk` berjumlah 17.208 baris dan kelas `Successful` berjumlah 15.385 baris. Data latih-validasi memuat 26.122 baris, sedangkan data uji hold-out memuat 6.471 baris dengan 3.398 kasus `AtRisk` dan 3.073 kasus `Successful`. Pemisahan berbasis `id_student` memastikan tidak ada mahasiswa yang muncul pada kedua bagian data.

Komposisi target pada dataset pemodelan relatif berimbang, sehingga evaluasi model tidak berangkat dari dominasi satu kelas yang ekstrem. Keseimbangan ini menjadi titik awal yang penting karena tujuan penelitian bukan hanya memperoleh accuracy tinggi, tetapi juga menjaga kemampuan model mengenali mahasiswa yang masuk kelompok `AtRisk`.

![Fig. 1. Distribusi target pada dataset pemodelan.](figures/fig-1a-target-distribution.png)

Pemeriksaan kualitas data kemudian dilakukan sebelum model dilatih. Data hilang terutama muncul pada `imd_band`, dengan jumlah yang jauh lebih kecil pada `date_registration`. Dua kondisi tersebut ditangani dalam alur pemodelan berdasarkan data latih-validasi agar proses imputasi tidak dipengaruhi oleh data uji hold-out.

![Fig. 2. Data hilang pada fitur dataset pemodelan.](figures/fig-1b-missing-values.png)

## B. Cross-Validation Performance

Tabel I menunjukkan rata-rata hasil 5-fold GroupKFold. Random Forest menghasilkan recall `AtRisk` tertinggi sebesar 0,7126 dan F1-score 0,7536. XGBoost menghasilkan accuracy dan ROC-AUC tertinggi, masing-masing sebesar 0,7582 dan 0,8440. Berdasarkan kriteria pemilihan yang memprioritaskan recall, Random Forest dipilih sebagai model akhir.

**Table I. Hasil 5-Fold GroupKFold pada Data Latih-Validasi**

| Metrik | Logistic Regression | Random Forest | XGBoost |
|---|---:|---:|---:|
| Accuracy | 0,7484 ± 0,0033 | 0,7538 ± 0,0033 | **0,7582 ± 0,0041** |
| Precision AtRisk | 0,8081 ± 0,0063 | 0,7999 ± 0,0148 | **0,8217 ± 0,0093** |
| Recall AtRisk | 0,6871 ± 0,0038 | **0,7126 ± 0,0040** | 0,6931 ± 0,0033 |
| F1 AtRisk | 0,7427 ± 0,0043 | **0,7536 ± 0,0050** | 0,7519 ± 0,0028 |
| ROC-AUC | 0,8324 ± 0,0028 | 0,8362 ± 0,0026 | **0,8440 ± 0,0020** |

## C. Hold-Out Evaluation

Tabel II memperlihatkan performa pada data uji hold-out. Random Forest mencapai accuracy 0,7592, precision `AtRisk` 0,8032, recall 0,7172, F1-score 0,7578, dan ROC-AUC 0,8396. XGBoost menghasilkan accuracy 0,7633 dan ROC-AUC 0,8440, sedangkan recall `AtRisk` mencapai 0,7054. Logistic Regression menghasilkan recall terendah sebesar 0,6869.

**Table II. Performa Model pada Data Uji Hold-Out**

| Metrik | Logistic Regression | Random Forest | XGBoost |
|---|---:|---:|---:|
| Accuracy | 0,7476 | 0,7592 | **0,7633** |
| Precision AtRisk | 0,8040 | 0,8032 | **0,8186** |
| Recall AtRisk | 0,6869 | **0,7172** | 0,7054 |
| F1 AtRisk | 0,7408 | **0,7578** | **0,7578** |
| ROC-AUC | 0,8298 | 0,8396 | **0,8440** |

Ringkasan klasifikasi Random Forest menunjukkan precision 0,80, recall 0,72, dan F1-score 0,76 pada 3.398 kasus `AtRisk`. Pada 3.073 kasus `Successful`, precision mencapai 0,72, recall 0,81, dan F1-score 0,76. Rata-rata tertimbang F1-score mencapai 0,76. Perbandingan metrik antar model menempatkan Random Forest sebagai pilihan yang paling relevan untuk konteks peringatan dini karena recall `AtRisk` menjadi ukuran yang paling dekat dengan kebutuhan menemukan mahasiswa berisiko sejak awal.

![Fig. 3. Perbandingan metrik AtRisk pada data uji hold-out.](figures/fig-2a-metrics-comparison.png)

Setelah model dipilih, pola kesalahan Random Forest diperiksa untuk memahami risiko operasionalnya. Model tersebut berhasil mengenali 2.437 kasus `AtRisk`, tetapi masih melewatkan 961 kasus yang seharusnya masuk kelompok berisiko. Temuan ini menunjukkan bahwa sistem sudah cukup kuat untuk menyaring sebagian besar mahasiswa berisiko, namun tetap membutuhkan lapisan prioritas dan verifikasi agar kasus yang belum terdeteksi dapat diminimalkan.

![Fig. 4. Confusion matrix Random Forest pada data uji hold-out.](figures/fig-2b-confusion-matrix.png)

Kurva ROC memberikan konteks tambahan terhadap perbedaan antar model. Ketiga kurva berada cukup berdekatan, sehingga selisih ROC-AUC perlu dibaca bersama tujuan keputusan. Dalam penelitian ini, kemampuan memperluas cakupan deteksi lebih diprioritaskan daripada memilih model hanya berdasarkan peringkat ROC-AUC.

![Fig. 5. Kurva ROC pada data uji hold-out.](figures/fig-2c-roc-curve.png)

Kontribusi fitur Random Forest memperlihatkan bahwa sinyal perilaku awal menjadi pembeda utama. Total klik VLE, hari aktivitas terakhir, jumlah hari aktif, dan ragam situs yang diakses muncul sebagai prediktor teratas, diikuti fitur assessment dan registrasi. Temuan ini selaras dengan tujuan peringatan dini karena model banyak bertumpu pada jejak engagement yang sudah tersedia sampai akhir minggu keempat. Nilai importance tetap ditafsirkan sebagai kontribusi prediktif, bukan bukti hubungan sebab akibat.

![Fig. 6. Lima belas fitur dengan feature importance tertinggi pada Random Forest.](figures/fig-3-feature-importance.png)

## D. Rule-Based Risk Layer

Ambang kuartil bawah data latih-validasi adalah skor assessment 0, jumlah assessment 0, total klik VLE 47, dan hari aktif VLE 4. Nilai nol pada indikator assessment menunjukkan bahwa sebagian mahasiswa belum mengumpulkan assessment sampai akhir minggu keempat. Lapisan risiko berbasis aturan menghasilkan 1.795 `High Risk`, 1.994 `Medium Risk`, dan 2.682 `Low Risk` pada data uji hold-out.

Tabel III membandingkan Random Forest dengan sistem gabungan. Lapisan risiko berbasis aturan meningkatkan recall dari 0,7172 menjadi 0,7849. Precision berubah dari 0,8032 menjadi 0,7039, sedangkan accuracy berubah dari 0,7592 menjadi 0,7136. Perubahan tersebut menunjukkan perluasan cakupan deteksi disertai peningkatan jumlah alarm yang memerlukan verifikasi oleh pemangku kepentingan akademik.

**Table III. Perbandingan Model dan Lapisan Risiko Berbasis Aturan**

| Metrik | Random Forest | RF + Lapisan Aturan |
|---|---:|---:|
| Accuracy | **0,7592** | 0,7136 |
| Precision AtRisk | **0,8032** | 0,7039 |
| Recall AtRisk | 0,7172 | **0,7849** |
| F1 AtRisk | **0,7578** | 0,7422 |

## E. Business Intelligence Output

Dashboard mengidentifikasi 3.789 student-module-presentation dalam antrean `High Risk` atau `Medium Risk`. Sinyal paling dominan adalah skor assessment rendah dengan 2.341 kasus. Module GGG presentation 2014J memiliki proporsi prioritas tertinggi pada data uji hold-out, yaitu 100% kasus `High Risk` atau `Medium Risk`. Indikator tersebut berfungsi sebagai sinyal untuk meninjau konteks modul dan kapasitas intervensi.

Daftar prioritas menyajikan identitas anonim mahasiswa, module-presentation, probabilitas `AtRisk`, level risiko, jumlah sinyal, alasan, dan rekomendasi. Struktur tersebut menghubungkan hasil model dengan tindakan seperti monitoring akses VLE, pendampingan assessment, serta konseling akademik.

Keluaran analitik kemudian disajikan ke dalam dashboard agar hasil model menjadi prioritas tindakan, bukan hanya angka evaluasi. Tampilan tersebut menghubungkan KPI risiko, level prioritas, konsentrasi module-presentation, distribusi probabilitas, sinyal dominan, perbandingan perilaku, confusion matrix, dan perubahan performa setelah lapisan risiko berbasis aturan. Dengan susunan ini, pengguna dapat bergerak dari ringkasan strategis menuju penelusuran kelompok atau mahasiswa yang membutuhkan tindak lanjut.

![Fig. 7. Dashboard peringatan dini OULAD pada akhir minggu keempat.](figures/fig-4-dashboard-dvbi.png)
