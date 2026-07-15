# Catatan Arah Capstone DVBI

## Konteks Project
Project ini berada pada repo **Data Visualization and Business Intelligence (DVBI)** dengan tema utama:

- **Student Performance Analytics**
- **Early warning risiko gagal atau mengundurkan diri dari mata kuliah**
- **Visual analytics dan Business Intelligence untuk monitoring akademik**

## Keputusan Dataset Final
Dataset final yang digunakan adalah **Open University Learning Analytics Dataset (OULAD)**.

Alasan pemilihan:
1. OULAD memenuhi kebutuhan data tabular berskala besar untuk klasifikasi.
2. Dataset menyediakan data akademik, registrasi, assessment, dan aktivitas VLE.
3. Struktur multi-table mendukung analisis Business Intelligence dan visual analytics.
4. Distribusi label binary risk cukup besar untuk dua kelas utama.

Dataset UCI **Predict Students' Dropout and Academic Success** tetap diperlakukan sebagai referensi pembanding historis, bukan dataset final capstone.

## Framing Riset Terkini
Problem dirumuskan sebagai **supervised binary classification**:

- `AtRisk` = `Withdrawn` + `Fail`
- `Successful` = `Pass` + `Distinction`

Unit analisis adalah **1 mahasiswa pada 1 module-presentation**.

`final_result` merepresentasikan hasil pada module-presentation tersebut, sehingga target penelitian berada pada tingkat mata kuliah.

## Horizon Early Warning
Riset final menggunakan cut-off **hari ke-28** untuk merepresentasikan akhir minggu keempat.

Fitur yang digunakan hanya informasi yang tersedia sampai hari ke-28:
- demografi dan informasi modul,
- registrasi awal,
- agregasi assessment sampai hari ke-28,
- agregasi aktivitas VLE sampai hari ke-28.

Informasi masa depan dikeluarkan dari fitur prediktor:
- `date_unregistration`,
- `has_unregistration`,
- `final_result`,
- assessment dan aktivitas VLE setelah hari ke-28.

## Evaluasi Model
Tiga algoritma pembanding:
- Logistic Regression,
- Random Forest,
- XGBoost.

Skema evaluasi:
- 80% train-validation dan 20% hold-out test,
- split berbasis `id_student`,
- 5-fold GroupKFold pada train-validation.

Model final adalah **Random Forest** karena menghasilkan recall `AtRisk` tertinggi:
- cross-validation recall `AtRisk`: **0,7107**,
- hold-out recall `AtRisk`: **0,7213**.

## Knowledge-Based Risk Layer
Knowledge-based risk layer digunakan untuk menerjemahkan prediksi model menjadi:
- level risiko,
- alasan risiko,
- rekomendasi intervensi,
- antrean prioritas mahasiswa.

Sistem gabungan meningkatkan recall `AtRisk` dari **0,7213** menjadi **0,7866**, dengan perubahan precision dari **0,8007** menjadi **0,7043**.

## Output Final
Output utama project:
1. dataset early warning OULAD,
2. evaluasi tiga model supervised learning,
3. model Random Forest terpilih,
4. knowledge-based risk layer,
5. dashboard early warning OULAD,
6. artikel IEEE,
7. bahan presentasi final DVBI.

## Catatan Interpretasi
Performa model lebih rendah dibanding eksperimen yang memakai aktivitas seluruh semester atau status unregistration. Hal ini wajar karena riset final hanya memakai informasi sampai hari ke-28, sehingga evaluasi lebih dekat dengan skenario intervensi dini.
