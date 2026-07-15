# Hasil Eksperimen OULAD Early Warning Binary Risk

Dokumen ini mencatat hasil eksperimen final untuk skenario early warning risiko gagal atau mengundurkan diri dari mata kuliah pada akhir minggu keempat. Angka di sini disinkronkan dengan artikel IEEE dan notebook OULAD terbaru.

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
| Logistic Regression | 0,7496 ± 0,0039 | 0,8090 ± 0,0059 | 0,6889 ± 0,0064 | 0,7442 ± 0,0059 | 0,8330 ± 0,0027 |
| Random Forest | 0,7524 ± 0,0013 | 0,7989 ± 0,0136 | **0,7107 ± 0,0085** | 0,7521 ± 0,0030 | 0,8362 ± 0,0023 |
| XGBoost | **0,7584 ± 0,0024** | **0,8215 ± 0,0096** | 0,6938 ± 0,0029 | **0,7522 ± 0,0039** | **0,8440 ± 0,0019** |

## Performa pada Hold-Out Test
| Model | Accuracy | Precision AtRisk | Recall AtRisk | F1 AtRisk | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0,7487 | 0,8034 | 0,6904 | 0,7426 | 0,8311 |
| Random Forest | 0,7594 | 0,8007 | **0,7213** | **0,7589** | 0,8396 |
| XGBoost | **0,7611** | **0,8154** | 0,7045 | 0,7559 | **0,8443** |

## Model Terpilih
Model final adalah **Random Forest** karena menghasilkan recall `AtRisk` tertinggi pada cross-validation dan hold-out test. Pemilihan ini sesuai dengan tujuan early warning yang memprioritaskan cakupan deteksi mahasiswa berisiko.

Confusion matrix Random Forest pada hold-out test:

| Aktual \ Prediksi | Successful | AtRisk |
|---|---:|---:|
| Successful | 2.463 | 610 |
| AtRisk | 947 | 2.451 |

## Knowledge-Based Risk Layer
Threshold kuartil bawah train-validation:
- `assessment_score_mean`: **0**
- `assessment_count`: **0**
- `vle_total_clicks`: **47**
- `vle_active_days`: **4**

Distribusi level risiko pada hold-out test:
- `High Risk`: **1.816**
- `Medium Risk`: **1.979**
- `Low Risk`: **2.676**

Perbandingan Random Forest dan sistem gabungan:

| Metrik | Random Forest | RF + Knowledge Layer |
|---|---:|---:|
| Accuracy | **0,7594** | 0,7146 |
| Precision AtRisk | **0,8007** | 0,7043 |
| Recall AtRisk | 0,7213 | **0,7866** |
| F1 AtRisk | **0,7589** | 0,7432 |

Knowledge layer meningkatkan recall dari **0,7213** menjadi **0,7866**. Perubahan tersebut memperluas cakupan deteksi dan menambah kasus yang masuk antrean verifikasi.

## Implikasi Visual Analytics
Dashboard early warning mengidentifikasi **3.795** student-module-presentation dalam antrean `High Risk` atau `Medium Risk`. Sinyal paling dominan adalah skor assessment rendah dengan **2.341** kasus. Module GGG presentation 2014J memiliki proporsi prioritas tertinggi pada hold-out test, yaitu **100%** kasus `High Risk` atau `Medium Risk`.

## Keterbatasan
- OULAD berasal dari konteks Open University di Inggris sehingga validitas eksternal perlu diuji ulang pada institusi lain.
- Fitur perilaku dibatasi pada agregasi sampai hari ke-28 dan belum memodelkan urutan temporal harian.
- Threshold knowledge layer berbasis kuartil train-validation dan perlu divalidasi bersama pakar akademik.
- Evaluasi mengukur performa deteksi; dampak intervensi terhadap retensi memerlukan studi lanjutan.
