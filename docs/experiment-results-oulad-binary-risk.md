# Hasil Eksperimen OULAD Binary Risk

## Ringkasan Dataset
- Total row: **32593**
- Total fitur model: **21**

## Distribusi Label
- `Successful`: **15385**
- `AtRisk`: **17208**

## Data Split
- Strategi: **GroupShuffleSplit (holdout) + GroupKFold (CV), grouped by id_student**
- Rasio: **80/20 holdout; 5-fold CV on train set**
- Train+Validation: **26122** baris (23028 mahasiswa unik)
- Test (hold-out): **6471** baris (5757 mahasiswa unik)
- Distribusi label train+val: {'Successful': 12312, 'AtRisk': 13810}
- Distribusi label test: {'Successful': 3073, 'AtRisk': 3398}

**Leakage prevention:** Split dilakukan berdasarkan `id_student` (GroupShuffleSplit untuk hold-out, GroupKFold untuk CV). Tidak ada mahasiswa yang muncul di training dan test/validation secara bersamaan.

## Penanganan Imbalance
- Metode: **class_weight='balanced' (LR, RF); scale_pos_weight (XGBoost)**
- `scale_pos_weight` (XGBoost): **0.8915**
- Rasio kelas: AtRisk 17208 vs Successful 15385 (rasio ~1.12:1, near-balanced)

## Ringkasan Fitur
- Fitur kategorikal: `gender`, `region`, `highest_education`, `imd_band`, `age_band`, `disability`, `code_module`, `code_presentation`
- Fitur numerik: `num_of_prev_attempts`, `studied_credits`, `date_registration`, `date_unregistration`, `has_unregistration`, `assessment_count`, `assessment_score_mean`, `assessment_score_max`, `assessment_score_min`, `vle_total_clicks`, `vle_active_days`, `vle_site_count`, `vle_last_activity_day`

## Cross-Validation (5-Fold GroupKFold)
| Model | Accuracy | Precision AtRisk | Recall AtRisk | F1 AtRisk |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.9365 ± 0.0029 | 0.9739 ± 0.0022 | 0.9041 ± 0.0074 | 0.9377 ± 0.0033 |
| Random Forest | 0.9419 ± 0.0028 | 0.9776 ± 0.0027 | 0.9110 ± 0.0060 | 0.9431 ± 0.0032 |
| XGBoost | 0.9441 ± 0.0031 | 0.9782 ± 0.0018 | 0.9147 ± 0.0067 | 0.9453 ± 0.0034 |

## Performa pada Hold-Out Test Set
| Model | Accuracy | Precision AtRisk | Recall AtRisk | F1 AtRisk | Confusion Matrix [[TN, FP], [FN, TP]] |
|---|---:|---:|---:|---:|---|
| Logistic Regression | 0.9309 | 0.9734 | 0.8929 | 0.9314 | `[[2990, 83], [364, 3034]]` |
| Random Forest | 0.9377 | 0.9765 | 0.9032 | 0.9384 | `[[2999, 74], [329, 3069]]` |
| XGBoost | 0.9394 | 0.9802 | 0.9029 | 0.9400 | `[[3011, 62], [330, 3068]]` |

## Model Terpilih
Model terbaik untuk kebutuhan early warning adalah **Random Forest**, dipilih berdasarkan recall kelas `AtRisk` dan F1-score kelas `AtRisk` sebagai tie-breaker.

## Distribusi Knowledge-Based Risk Layer
- `Low Risk`: **22168**
- `High Risk`: **6508**
- `Medium Risk`: **3917**

## Implikasi Visual Analytics
Hasil eksperimen dapat diterjemahkan menjadi indikator monitoring akademik, terutama jumlah mahasiswa `AtRisk`, distribusi `High Risk`, `Medium Risk`, dan `Low Risk`, perbandingan risiko antar module-presentation, serta daftar prioritas mahasiswa yang memiliki sinyal aktivitas VLE rendah, performa assessment rendah, atau unregistration.

## Known Limitations
- **Fitur `has_unregistration` dan `date_unregistration`** bersifat post-hoc: mahasiswa yang unregister secara definisi sudah dropout. Fitur ini dipertahankan untuk baseline karena memberikan sinyal yang relevan untuk knowledge-based layer, tetapi untuk skenario early prediction murni sebaiknya dieksklusi.
- **Agregasi assessment dan VLE menggunakan data seluruh semester**, bukan cut-off temporal (misal minggu ke-4). Ini berarti model melihat seluruh trajectory mahasiswa, bukan prediksi dini.
- **Split dilakukan berdasarkan `id_student`** untuk menghindari group leakage (mahasiswa yang sama muncul di train dan test pada module berbeda).
