# Ringkasan Dataset — Predict Students' Dropout and Academic Success

## Dataset yang dipilih
- **Nama:** Predict Students' Dropout and Academic Success
- **Sumber:** UCI Machine Learning Repository
- **DOI:** 10.24432/C5MC89
- **Lisensi:** CC BY 4.0
- **URL dataset:** https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success
- **File lokal utama:** `data/uci-student-dropout/data.csv`
- **Arsip unduhan:** `data/uci-student-dropout/predict-students-dropout-and-academic-success.zip`

## Alasan pemilihan
Dataset ini paling cocok dengan tema repository kita karena:
1. langsung relevan dengan **student dropout / academic success**,
2. bersifat **tabular** dan siap dipakai untuk klasifikasi,
3. berasal dari sumber publik yang kredibel,
4. sudah banyak dipakai pada studi academic performance / early warning,
5. cukup kaya fitur untuk analisis BI, EDA, visualisasi, dan baseline machine learning.

## Deskripsi singkat
Dataset ini berisi data mahasiswa dari institusi pendidikan tinggi, menggabungkan informasi:
- saat pendaftaran/enrollment,
- faktor akademik awal,
- faktor demografis dan sosial-ekonomi,
- performa akademik semester 1 dan semester 2.

Setiap baris merepresentasikan **1 mahasiswa**.
Target klasifikasi terdiri dari 3 kelas:
- `Dropout`
- `Enrolled`
- `Graduate`

## Ringkasan ukuran dataset
- **Jumlah baris:** 4.424
- **Jumlah kolom:** 37
- **Jumlah fitur:** 36
- **Target:** 1 kolom (`Target`)
- **Ukuran file CSV:** 533.230 bytes
- **Delimiter:** `;`

## Distribusi kelas target
- **Graduate:** 2.209
- **Dropout:** 1.421
- **Enrolled:** 794

Catatan:
- Dataset ini **multi-class classification**.
- Distribusi target **imbalanced**, karena kelas `Graduate` paling dominan dan `Enrolled` paling kecil.

## Karakteristik fitur
Fitur dalam dataset mencakup beberapa kelompok besar:

### 1. Data demografis / identitas dasar
Contoh:
- `Marital status`
- `Gender`
- `Age at enrollment`
- `Nacionality`
- `International`

### 2. Data pendaftaran / akademik awal
Contoh:
- `Application mode`
- `Application order`
- `Course`
- `Previous qualification`
- `Previous qualification (grade)`
- `Admission grade`
- `Daytime/evening attendance`

### 3. Data keluarga / sosial-ekonomi
Contoh:
- `Mother's qualification`
- `Father's qualification`
- `Mother's occupation`
- `Father's occupation`
- `Debtor`
- `Tuition fees up to date`
- `Scholarship holder`

### 4. Data performa akademik semester 1
Contoh:
- `Curricular units 1st sem (enrolled)`
- `Curricular units 1st sem (evaluations)`
- `Curricular units 1st sem (approved)`
- `Curricular units 1st sem (grade)`

### 5. Data performa akademik semester 2
Contoh:
- `Curricular units 2nd sem (enrolled)`
- `Curricular units 2nd sem (evaluations)`
- `Curricular units 2nd sem (approved)`
- `Curricular units 2nd sem (grade)`

### 6. Variabel makroekonomi
Contoh:
- `Unemployment rate`
- `Inflation rate`
- `GDP`

## Temuan inspeksi awal
### Missing values
- Dari inspeksi file CSV, **tidak ditemukan missing value kosong eksplisit** pada kolom.
- Namun ini **belum berarti bersih sepenuhnya**, karena tetap perlu dicek:
  - apakah ada nilai kode kategori yang perlu dipetakan,
  - apakah ada nilai nol yang sebenarnya bermakna “tidak ada” atau “belum tersedia”,
  - apakah ada kolom yang secara semantik perlu diperlakukan sebagai kategorikal meski tersimpan sebagai integer.

### Ringkasan numerik awal
- **Age at enrollment**: min 17, max 70, mean 23,27
- **Admission grade**: min 95, max 190, mean 126,98
- **Curricular units 1st sem (approved)**: min 0, max 26, mean 4,71
- **Curricular units 1st sem (grade)**: min 0, max 18,875, mean 10,64
- **Curricular units 2nd sem (approved)**: min 0, max 20, mean 4,44
- **Curricular units 2nd sem (grade)**: min 0, max 18,5714, mean 10,23

## Kekuatan dataset
1. **Sangat relevan** dengan case yang sudah kita pilih.
2. Sumber **publik dan terdokumentasi**.
3. Cocok untuk **multi-class classification**.
4. Mencakup kombinasi fitur yang bagus untuk:
   - EDA,
   - dashboard BI,
   - feature importance,
   - segmentasi awal mahasiswa berisiko.
5. Target bisnis/akademiknya jelas: **early warning dan monitoring mahasiswa berisiko**.

## Keterbatasan dataset
1. Ukuran dataset **4.424 baris**, jadi cukup baik untuk tugas, tetapi tidak sangat besar.
2. Ada banyak fitur kategorikal yang dikodekan sebagai angka, sehingga **harus diperlakukan hati-hati** agar tidak salah dianggap numerik murni.
3. Terdapat fitur semester 1 dan semester 2, sehingga nanti kita perlu memutuskan:
   - apakah memakai semua fitur,
   - atau mensimulasikan skenario **early prediction** hanya dari data enrollment / semester awal.
4. Distribusi kelas tidak seimbang, sehingga perlu perhatian pada evaluasi model dan kemungkinan handling imbalance.
5. Dataset berasal dari konteks institusi tertentu, sehingga generalisasi ke kampus lain tetap terbatas.

## Implikasi untuk tugas DVBI
Dataset ini cocok dipakai untuk dua arah sekaligus:

### A. Arah analitik / machine learning
- klasifikasi status mahasiswa (`Dropout`, `Enrolled`, `Graduate`),
- perbandingan beberapa algoritma,
- evaluasi confusion matrix, F1-score, dan recall per kelas.

### B. Arah business intelligence / visual analytics
- dashboard distribusi status mahasiswa,
- visualisasi faktor risiko utama,
- profil mahasiswa dropout vs graduate,
- monitoring performa semester 1 dan semester 2,
- segmentasi mahasiswa untuk early warning.

## Kesimpulan
Dataset **Predict Students' Dropout and Academic Success** layak dipakai sebagai dataset utama untuk project ini karena paling selaras dengan topik **Student Performance / Dropout Analytics** dan cukup siap untuk tahap berikutnya.

Dengan demikian, langkah setelah ini yang paling tepat adalah:
1. menetapkan **scope analisis** (full features vs early prediction scenario),
2. menentukan **kolom kategorikal vs numerik**,
3. menyusun **rencana preprocessing dataset** secara eksplisit.
