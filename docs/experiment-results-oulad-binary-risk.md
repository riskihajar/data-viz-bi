# Hasil Eksperimen OULAD Early Warning Binary Risk

Dokumen ini mencatat hasil eksperimen final untuk skenario early warning risiko dropout mahasiswa pada akhir minggu keempat. Angka di sini disinkronkan dengan artikel IEEE dan notebook OULAD terbaru.

## Ringkasan Dataset
- Total baris: **32.593** student-module-presentation
- Mahasiswa unik: **28.785**
- Unit analisis: **1 mahasiswa pada 1 module-presentation**
- Horizon fitur: **hari ke-28**

## Distribusi Label
- `AtRisk`: **17.208** baris (`Withdrawn` + `Fail`)
- `Successful`: **15.385** baris (`Pass` + `Distinction`)

## Data Split
- Strategi: **GroupShuffleSplit (hold-out) + 5-fold GroupKFold**
- Grouping: **`id_student`**
- Train-validation: **26.122** baris
- Hold-out test: **6.471** baris
- Distribusi hold-out test: **3.398 `AtRisk`** dan **3.073 `Successful`**
- Overlap mahasiswa antara train-validation dan hold-out test: **0**

## Fitur Model
- Fitur kategorikal: `gender`, `region`, `highest_education`, `imd_band`, `age_band`, `disability`, `code_module`, `code_presentation`
- Fitur numerik: `num_of_prev_attempts`, `studied_credits`, `date_registration`, `assessment_count`, `assessment_score_mean`, `assessment_score_max`, `assessment_score_min`, `vle_total_clicks`, `vle_active_days`, `vle_site_count`, `vle_last_activity_day`
- Fitur masa depan yang dikeluarkan dari prediktor: `date_unregistration`, `has_unregistration`, `final_result`, dan aktivitas setelah hari ke-28

## Cross-Validation (5-Fold GroupKFold)
| Model | Accuracy | Precision AtRisk | Recall AtRisk | F1 AtRisk | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0,7484 ± 0,0033 | 0,8081 ± 0,0063 | 0,6871 ± 0,0038 | 0,7427 ± 0,0043 | 0,8324 ± 0,0028 |
| Random Forest | 0,7538 ± 0,0033 | 0,7999 ± 0,0148 | **0,7126 ± 0,0040** | **0,7536 ± 0,0050** | 0,8362 ± 0,0026 |
| XGBoost | **0,7582 ± 0,0041** | **0,8217 ± 0,0093** | 0,6931 ± 0,0033 | 0,7519 ± 0,0028 | **0,8440 ± 0,0020** |

## Performa pada Hold-Out Test
| Model | Accuracy | Precision AtRisk | Recall AtRisk | F1 AtRisk | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0,7476 | 0,8040 | 0,6869 | 0,7408 | 0,8298 |
| Random Forest | 0,7592 | 0,8032 | **0,7172** | **0,7578** | 0,8396 |
| XGBoost | **0,7633** | **0,8186** | 0,7054 | **0,7578** | **0,8440** |

## Model Terpilih
Model final adalah **Random Forest** karena menghasilkan recall `AtRisk` tertinggi pada cross-validation dan hold-out test. Pemilihan ini sesuai dengan tujuan early warning yang memprioritaskan cakupan deteksi mahasiswa berisiko.

Confusion matrix Random Forest pada hold-out test:

| Aktual \ Prediksi | Successful | AtRisk |
|---|---:|---:|
| Successful | 2.476 | 597 |
| AtRisk | 961 | 2.437 |

## Knowledge-Based Risk Layer
Threshold kuartil bawah train-validation:
- `assessment_score_mean`: **0**
- `assessment_count`: **0**
- `vle_total_clicks`: **47**
- `vle_active_days`: **4**

Distribusi level risiko pada hold-out test:
- `High Risk`: **1.795**
- `Medium Risk`: **1.994**
- `Low Risk`: **2.682**

Perbandingan Random Forest dan sistem gabungan:

| Metrik | Random Forest | RF + Knowledge Layer |
|---|---:|---:|
| Accuracy | **0,7592** | 0,7136 |
| Precision AtRisk | **0,8032** | 0,7039 |
| Recall AtRisk | 0,7172 | **0,7849** |
| F1 AtRisk | **0,7578** | 0,7422 |

Knowledge layer meningkatkan recall dari **0,7172** menjadi **0,7849**. Peningkatan ini memperluas cakupan deteksi, dengan konsekuensi precision turun karena lebih banyak kasus masuk antrean verifikasi.

## Implikasi Visual Analytics
Dashboard early warning mengidentifikasi **3.789** student-module-presentation dalam antrean `High Risk` atau `Medium Risk`. Sinyal paling dominan adalah skor assessment rendah dengan **2.341** kasus. Module GGG presentation 2014J memiliki proporsi prioritas tertinggi pada hold-out test, yaitu **100%** kasus `High Risk` atau `Medium Risk`.

## Keterbatasan
- OULAD berasal dari konteks Open University di Inggris sehingga validitas eksternal perlu diuji ulang pada institusi lain.
- Fitur perilaku dibatasi pada agregasi sampai hari ke-28 dan belum memodelkan urutan temporal harian.
- Threshold knowledge layer berbasis kuartil train-validation dan perlu divalidasi bersama pakar akademik.
- Evaluasi mengukur performa deteksi; dampak intervensi terhadap retensi memerlukan studi lanjutan.
