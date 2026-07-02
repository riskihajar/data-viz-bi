# III. Methodology

## A. Research Design

Penelitian menggunakan desain supervised binary classification untuk mendeteksi risiko dropout pada akhir minggu keempat. Alur penelitian meliputi pengambilan dan audit OULAD, pembentukan fitur dengan batas temporal, exploratory data analysis, pemisahan data berbasis mahasiswa, pelatihan dan evaluasi model, pembentukan lapisan risiko berbasis aturan, serta penyajian indikator melalui dashboard Business Intelligence. Seluruh eksperimen menggunakan `random_state=42` untuk mendukung reproduktibilitas.

## B. Dataset and Unit of Analysis

Dataset yang digunakan adalah Open University Learning Analytics Dataset (OULAD) [4]. Arsip data diperoleh melalui UCI Machine Learning Repository dan berisi tabel `studentInfo`, `studentRegistration`, `assessments`, `studentAssessment`, `studentVle`, `courses`, dan `vle`. Tabel `studentInfo` memuat 32.593 baris, sedangkan `studentVle` memuat 10.655.280 catatan aktivitas.

Unit analisis adalah satu mahasiswa pada satu kombinasi `code_module` dan `code_presentation`. Satu baris data hasil olahan merepresentasikan satu student-module-presentation. Struktur ini mengikuti unit label pada `studentInfo` dan menjaga konsistensi penggabungan data registrasi, assessment, serta aktivitas VLE.

## C. Target Label and Temporal Boundary

Target dirumuskan sebagai klasifikasi biner. Label `AtRisk` diberikan kepada baris dengan `final_result` berupa `Withdrawn` atau `Fail`. Label `Successful` diberikan kepada baris dengan `final_result` berupa `Pass` atau `Distinction`. Dataset terdiri atas 17.208 baris `AtRisk` dan 15.385 baris `Successful`.

Horizon peringatan dini ditetapkan pada hari ke-28. Submission assessment dipilih dengan kondisi `date_submitted <= 28`, sedangkan aktivitas VLE dipilih dengan kondisi `date <= 28`. Informasi `date_unregistration`, `has_unregistration`, hasil akhir, dan aktivitas setelah hari ke-28 dikeluarkan dari fitur prediktor. Hasil akhir hanya digunakan untuk membentuk target evaluasi.

## D. Feature Construction

Fitur kategorikal mencakup `gender`, `region`, `highest_education`, `imd_band`, `age_band`, `disability`, `code_module`, dan `code_presentation`. Fitur numerik awal mencakup `num_of_prev_attempts`, `studied_credits`, dan `date_registration`.

Data `studentAssessment` dihubungkan dengan tabel `assessments` melalui `id_assessment` untuk memperoleh konteks module-presentation. Data sampai hari ke-28 diagregasi menjadi `assessment_count`, `assessment_score_mean`, `assessment_score_max`, dan `assessment_score_min`. Data `studentVle` sampai hari ke-28 diagregasi menjadi `vle_total_clicks`, `vle_active_days`, `vle_site_count`, dan `vle_last_activity_day`.

Nilai numerik dikonversi menggunakan `pd.to_numeric`; nilai yang tidak dapat dikonversi diperlakukan sebagai data hilang. Agregat perilaku yang belum memiliki aktivitas diisi dengan nol. Dalam alur pemodelan, data hilang pada fitur numerik diimputasi menggunakan median dan kemudian distandardisasi. Data hilang pada fitur kategorikal diimputasi menggunakan modus dan ditransformasikan dengan one-hot encoding. Seluruh transformasi dipelajari hanya dari data pelatihan.

## E. Data Splitting and Validation

Data dibagi menjadi 80% data latih-validasi dan 20% data uji hold-out menggunakan `GroupShuffleSplit`. Variabel `id_student` digunakan sebagai grup sehingga setiap mahasiswa ditempatkan secara eksklusif pada salah satu bagian. Data latih-validasi terdiri atas 26.122 baris dan data uji terdiri atas 6.471 baris. Pemeriksaan menunjukkan tidak ada mahasiswa yang muncul di kedua bagian.

Evaluasi cross-validation menggunakan 5-fold `GroupKFold` pada data latih-validasi. Pemilihan model didasarkan pada rata-rata recall kelas `AtRisk`, kemudian F1-score `AtRisk` digunakan sebagai penentu ketika nilai recall berdekatan. Setelah model terpilih, performa akhir dilaporkan pada data uji hold-out.

## F. Supervised Learning Models

Tiga algoritma dibandingkan. Logistic Regression digunakan sebagai pembanding linear dengan `class_weight='balanced'`. Random Forest menggunakan 250 pohon dan `class_weight='balanced'`. XGBoost menggunakan 200 estimator, kedalaman maksimum 4, learning rate 0,08, subsample 0,9, dan colsample 0,9. Nilai `scale_pos_weight` dihitung dari distribusi kelas pada data latih-validasi.

Metrik evaluasi mencakup accuracy, precision, recall, dan F1-score untuk kelas `AtRisk`, ROC-AUC, confusion matrix, serta ringkasan klasifikasi. Recall `AtRisk` menjadi kriteria utama karena sistem peringatan dini memprioritaskan cakupan mahasiswa berisiko yang dapat diarahkan pada proses verifikasi dan intervensi.

## G. Rule-Based Risk Layer

Lapisan risiko berbasis aturan menggunakan empat indikator: `assessment_score_mean`, `assessment_count`, `vle_total_clicks`, dan `vle_active_days`. Ambang batas dihitung dari kuartil bawah data latih-validasi. Prosedur ini menjaga ambang batas tetap independen dari data uji hold-out. Hasil perhitungan menghasilkan ambang batas skor assessment 0, jumlah assessment 0, total klik VLE 47, dan hari aktif VLE 4.

Sinyal risiko muncul ketika nilai indikator sama dengan atau lebih rendah dari ambang batas. Status `High Risk` diberikan ketika model memprediksi `AtRisk` dan mahasiswa memiliki minimal dua sinyal aturan. Status `Medium Risk` diberikan ketika model memprediksi `AtRisk` atau mahasiswa memiliki minimal dua sinyal aturan. Status `Low Risk` diberikan pada kondisi lainnya.

Setiap baris menghasilkan probabilitas `AtRisk`, jumlah sinyal, alasan risiko, dan rekomendasi intervensi. Aktivitas VLE rendah diarahkan pada pengingat dan monitoring akses. Assessment rendah atau belum dikerjakan diarahkan pada pendampingan akademik. Kombinasi minimal tiga sinyal diarahkan pada konseling atau tindak lanjut dosen wali.

Evaluasi sistem gabungan memetakan `High Risk` dan `Medium Risk` sebagai `AtRisk`. Perbandingan dengan model terpilih digunakan untuk mengukur perubahan cakupan deteksi, precision, dan kebutuhan verifikasi.

## H. Visual Analytics and Business Intelligence

Dashboard statis dibangun menggunakan Matplotlib dan Seaborn. Dashboard memuat KPI mahasiswa unik, jumlah dan persentase prioritas intervensi, distribusi level risiko, risiko per module-presentation, distribusi probabilitas, sinyal dominan, median aktivitas VLE dan assessment, confusion matrix, serta perbandingan model dengan lapisan risiko berbasis aturan.

Daftar prioritas diurutkan berdasarkan level risiko, probabilitas `AtRisk`, dan jumlah sinyal. Keluaran tersebut mendukung beberapa tingkat keputusan. Pimpinan akademik memperoleh gambaran skala risiko, program studi melihat konsentrasi risiko antar module-presentation, dan tutor atau dosen wali memperoleh alasan serta rekomendasi pada tingkat mahasiswa. Sistem diposisikan sebagai pendukung keputusan yang membantu pemangku kepentingan menetapkan tindak lanjut berdasarkan bukti analitik dan pertimbangan akademik.
