# Evaluasi Model dan Knowledge-Based System untuk Early Warning OULAD

**Mata Kuliah:** Data Visualization and Business Intelligence  
**Kelompok:** 5  
**Program Studi:** S2 PJJ Informatika, Konsentrasi Big Data dan Predictive Analytics  
**Institusi:** Universitas Amikom Yogyakarta

| Nama | NIM |
|---|---|
| Muhammad Rizky Hajar | 24.55.2714 |
| Alwie Muflich | 24.55.2667 |
| Heri Santosa | 24.55.2676 |

Dokumen ini menjelaskan rangkaian analisis pada notebook `oulad_early_warning_dvbi_colab.ipynb`, mulai dari perumusan kasus bisnis hingga penyajian insight Business Intelligence.

## Persiapan Analisis

“Pada bagian awal, kami menyiapkan lingkungan eksperimen dengan mengimpor library untuk pengolahan data, visualisasi, preprocessing, pemodelan, dan evaluasi. Seluruh proses menggunakan `random_state` yang sama agar hasil dapat direproduksi. Batas data ditetapkan sampai hari ke-28 untuk merepresentasikan kondisi akhir minggu ke-4.”

## 1. Kasus Bisnis

“Kasus yang kami pilih adalah identifikasi dini mahasiswa berisiko gagal atau mengundurkan diri. Tujuannya bukan menggantikan keputusan dosen, tetapi membantu stakeholder akademik menentukan mahasiswa yang perlu diperhatikan lebih dahulu.”

Target dibentuk menjadi dua kelas. `AtRisk` menggabungkan `Withdrawn` dan `Fail`, sedangkan `Successful` menggabungkan `Pass` dan `Distinction`.

## 2. Dataset

“Kami menggunakan Open University Learning Analytics Dataset atau OULAD. Dataset ini terdiri dari beberapa tabel relasional yang memuat profil mahasiswa, registrasi, assessment, dan aktivitas pada Virtual Learning Environment.”

Notebook mengunduh dataset otomatis agar eksperimen dapat direproduksi dari runtime Google Colab baru tanpa upload manual.

## 3. Preprocessing Minggu Ke-4

“Unit analisis kami adalah satu mahasiswa pada satu module-presentation. Assessment dihubungkan ke konteks modul melalui `id_assessment`, kemudian assessment dan VLE hanya dihitung sampai hari ke-28.”

“Kami tidak menggunakan `date_unregistration`, `has_unregistration`, atau hasil akhir sebagai fitur. Informasi tersebut dapat membocorkan kondisi masa depan dan membuat performa model terlihat tidak realistis.”

## 4. EDA

“EDA digunakan untuk melihat distribusi kelas, missing values, dan perbedaan pola awal. Fokusnya adalah apakah mahasiswa AtRisk menunjukkan aktivitas assessment atau VLE yang berbeda pada empat minggu pertama.”

Angka pada grafik harus dibaca dari hasil notebook terbaru, bukan dihafalkan dari eksperimen lama yang memakai seluruh semester.

## 5. Pembagian Data

“Data dibagi 80 persen untuk train-validation dan 20 persen untuk hold-out test. Pembagian dilakukan berdasarkan `id_student`, sehingga mahasiswa yang sama tidak muncul pada train dan test walaupun mengambil beberapa modul.”

Lima fold `GroupKFold` digunakan pada data train untuk mengukur kestabilan model.

## 6. Model dan Evaluasi

“Tiga algoritma dibandingkan: Logistic Regression sebagai baseline linear, Random Forest sebagai ensemble berbasis pohon, dan XGBoost sebagai boosting.”

Metrik yang ditampilkan adalah accuracy, precision, recall, F1 kelas `AtRisk`, ROC-AUC, confusion matrix, dan classification report.

“Recall AtRisk menjadi metrik utama karena mahasiswa berisiko yang tidak terdeteksi merupakan kesalahan paling kritis dalam early warning. Jika recall sama, F1 digunakan sebagai pembanding berikutnya.”

Model dan nilai evaluasi diperoleh dari hasil eksperimen. Nilai false negative pada confusion matrix menunjukkan mahasiswa `AtRisk` yang tidak berhasil dideteksi oleh model.

## 7. Model Terbaik dan Interpretasi

“Model terbaik dipilih otomatis berdasarkan recall AtRisk dan F1. Feature importance atau coefficient ditampilkan untuk menjelaskan fitur yang paling banyak berkontribusi terhadap prediksi.”

Feature importance bukan bukti hubungan sebab-akibat. Visual tersebut hanya menjelaskan penggunaan fitur oleh model.

## 8. Knowledge-Based System

“Model machine learning menghasilkan probabilitas, tetapi probabilitas saja belum menjelaskan tindakan. Karena itu kami menambahkan knowledge-based risk layer.”

Threshold skor assessment, jumlah assessment, total klik VLE, dan hari aktif VLE dihitung dari kuartil bawah data train. Aturannya adalah:

- `High Risk`: model memprediksi AtRisk dan terdapat minimal dua sinyal perilaku.
- `Medium Risk`: model memprediksi AtRisk atau terdapat minimal dua sinyal perilaku.
- `Low Risk`: kondisi lainnya.

“Setiap mahasiswa memperoleh level, alasan risiko, dan rekomendasi. Aktivitas VLE rendah diarahkan pada pengingat dan monitoring akses. Masalah assessment diarahkan pada pendampingan akademik. Banyak sinyal sekaligus diarahkan pada konseling atau tindak lanjut dosen wali.”

## 9. Evaluasi Sistem Gabungan

“High dan Medium Risk dipetakan menjadi AtRisk untuk mengevaluasi knowledge layer. Kami membandingkan precision, recall, dan F1 sistem gabungan dengan model terbaik.”

Jika recall naik tetapi precision turun, jelaskan bahwa sistem menemukan lebih banyak mahasiswa berisiko dengan konsekuensi bertambahnya alarm yang perlu diverifikasi.

## 10. Dashboard DVBI

“Dashboard menyatukan KPI jumlah mahasiswa, antrean intervensi, distribusi level risiko, risiko per module-presentation, probabilitas, sinyal dominan, pola perilaku, confusion matrix, dan perbandingan sistem.”

Penggunaan dashboard berdasarkan stakeholder:

- Pimpinan akademik melihat skala risiko dan kebutuhan sumber daya.
- Program studi melihat module-presentation dengan konsentrasi risiko tertinggi.
- Tutor dan dosen wali melihat alasan serta daftar mahasiswa prioritas.
- Tim konseling menggunakan rekomendasi sebagai titik awal tindak lanjut.

## 11. Insight Business Intelligence

“Insight BI menjawab tiga pertanyaan: di mana risiko terkonsentrasi, faktor apa yang dominan, dan siapa yang perlu ditindaklanjuti terlebih dahulu.”

Module-presentation dan sinyal dominan dihitung otomatis dari hasil analisis. Korelasi dan feature importance tidak boleh ditafsirkan langsung sebagai hubungan sebab-akibat.

## 12. Rekomendasi

- Prioritaskan `High Risk`, lalu `Medium Risk` dengan probabilitas dan jumlah sinyal tertinggi.
- Sesuaikan intervensi dengan alasan risiko.
- Pantau perubahan aktivitas setelah intervensi.
- Validasi threshold bersama dosen atau pengelola akademik sebelum penerapan nyata.
- Evaluasi kapasitas tim karena recall tinggi dapat menambah beban tindak lanjut.

## 13. Keterbatasan dan Kesimpulan

“OULAD berasal dari konteks Open University di Inggris, sehingga model perlu divalidasi ulang sebelum digunakan pada institusi lain. Threshold aturan juga masih berbasis kuartil data dan belum menggantikan pengetahuan pakar.”

“Kesimpulannya, tugas ini tidak berhenti pada evaluasi model. Prediksi diterjemahkan menjadi knowledge-based system, dashboard, insight, dan prioritas tindakan. Seluruh hasil berfungsi sebagai decision support dan keputusan akhir tetap berada pada manusia.”
