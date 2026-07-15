# Preprocessing Plan OULAD — Early Warning Binary Risk

Dokumen ini menyinkronkan preprocessing dengan arah riset terkini: early warning risiko gagal atau mengundurkan diri dari mata kuliah pada akhir minggu keempat.

## Framing
Problem dirumuskan sebagai **binary classification**:

- `AtRisk` = `Withdrawn` + `Fail`
- `Successful` = `Pass` + `Distinction`

Tujuan model adalah mendeteksi risiko hasil akhir mata kuliah `Withdrawn` atau `Fail` sedini mungkin menggunakan informasi yang sudah tersedia sampai hari ke-28.

## Unit Analisis
- **1 row = 1 student pada 1 module-presentation**

Unit ini mengikuti struktur `studentInfo` OULAD dan menjaga konsistensi join lintas tabel.

## Tabel Sumber
- `studentInfo.csv` -> label utama + demografi
- `studentRegistration.csv` -> tanggal registrasi awal
- `assessments.csv` -> konteks assessment per module-presentation
- `studentAssessment.csv` -> agregasi performa assessment sampai hari ke-28
- `studentVle.csv` -> agregasi engagement VLE sampai hari ke-28

## Horizon Temporal
Cut-off fitur ditetapkan pada **hari ke-28**.

Yang digunakan:
- `studentAssessment.date_submitted <= 28`
- `studentVle.date <= 28`

Yang dikeluarkan dari fitur prediktor:
- `date_unregistration`
- `has_unregistration`
- `final_result`
- assessment dan aktivitas VLE setelah hari ke-28

## Fitur Model Final
### Kategorikal
- `gender`
- `region`
- `highest_education`
- `imd_band`
- `age_band`
- `disability`
- `code_module`
- `code_presentation`

### Numerik
- `num_of_prev_attempts`
- `studied_credits`
- `date_registration`
- `assessment_count`
- `assessment_score_mean`
- `assessment_score_max`
- `assessment_score_min`
- `vle_total_clicks`
- `vle_active_days`
- `vle_site_count`
- `vle_last_activity_day`

## Aturan Preprocessing
1. `studentInfo` menjadi base table.
2. Target `risk_label` dibentuk dari `final_result`.
3. `studentAssessment` digabung dengan `assessments` melalui `id_assessment`.
4. Assessment diagregasi per `(code_module, code_presentation, id_student)` sampai hari ke-28.
5. `studentVle` diagregasi per `(code_module, code_presentation, id_student)` sampai hari ke-28.
6. Agregat assessment/VLE yang kosong diisi nol.
7. Missing value numerik diimputasi dalam pipeline model menggunakan median.
8. Missing value kategorikal diimputasi dalam pipeline model menggunakan modus.
9. Encoding kategorikal dilakukan dengan one-hot encoding.
10. Seluruh transformasi dipelajari dari data train-validation.

## Split dan Validasi
- Hold-out split: **80% train-validation** dan **20% test**
- Split menggunakan `GroupShuffleSplit` dengan grup `id_student`
- Cross-validation menggunakan **5-fold GroupKFold** pada train-validation
- Tujuan grouping: mahasiswa yang sama tidak muncul di train dan test/validation pada waktu yang sama

## Model dan Evaluasi
Algoritma pembanding:
- Logistic Regression
- Random Forest
- XGBoost

Metrik:
- Accuracy
- Precision `AtRisk`
- Recall `AtRisk`
- F1 `AtRisk`
- ROC-AUC
- Confusion matrix

Kriteria pemilihan model:
1. Recall `AtRisk`
2. F1 `AtRisk` sebagai pembanding berikutnya

## Knowledge-Based Risk Layer
Knowledge layer menggunakan empat indikator awal:
- `assessment_score_mean`
- `assessment_count`
- `vle_total_clicks`
- `vle_active_days`

Threshold dihitung dari kuartil bawah train-validation:
- skor assessment: **0**
- jumlah assessment: **0**
- total klik VLE: **47**
- hari aktif VLE: **4**

Aturan level:
- `High Risk`: model memprediksi `AtRisk` dan minimal dua sinyal aturan aktif
- `Medium Risk`: model memprediksi `AtRisk` atau minimal dua sinyal aturan aktif
- `Low Risk`: kondisi lainnya

## Output yang Digunakan
- Dataset early warning untuk modeling
- Evaluasi tiga model
- Model final Random Forest
- Evaluasi RF + Knowledge Layer
- Dashboard early warning OULAD
- Daftar prioritas intervensi akademik
