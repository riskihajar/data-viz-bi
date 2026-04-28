# Preprocessing Plan OULAD — Binary Risk Framing

## Framing yang dipilih
Rekomendasi yang dipakai untuk tahap awal capstone DVBI adalah:

> **binary classification**: `AtRisk` vs `Successful`

Mapping label:
- `AtRisk` = `Withdrawn` + `Fail`
- `Successful` = `Pass` + `Distinction`

Alasan pemilihan:
1. paling mudah dijelaskan untuk konteks **early warning / risk analytics**;
2. tetap aman terhadap syarat dosen karena dua kelas sangat besar;
3. lebih cepat untuk baseline BI + modeling;
4. masih bisa diperluas nanti ke 3-class atau 4-class.

## Unit analisis
- **1 row = 1 student pada 1 module-presentation**

Ini konsisten dengan struktur `studentInfo` OULAD dan paling aman untuk join lintas tabel.

## Tabel sumber
- `studentInfo.csv` → label utama + demografi
- `studentRegistration.csv` → sinyal registrasi / unregistration
- `studentAssessment.csv` → agregasi performa penilaian
- `studentVle.csv` → agregasi engagement LMS

## Fitur baseline yang dibentuk
### Dari `studentInfo`
- `gender`
- `region`
- `highest_education`
- `imd_band`
- `age_band`
- `num_of_prev_attempts`
- `studied_credits`
- `disability`
- `final_result`
- `risk_label`

### Dari `studentRegistration`
- `date_registration`
- `date_unregistration`
- `has_unregistration`

### Dari `studentAssessment`
- `assessment_count`
- `assessment_score_mean`
- `assessment_score_max`
- `assessment_score_min`

### Dari `studentVle`
- `vle_total_clicks`
- `vle_active_days`
- `vle_site_count`
- `vle_last_activity_day`

## Aturan preprocessing baseline
1. `studentInfo` dijadikan **base table**.
2. `imd_band` kosong diisi `Unknown`.
3. `date_unregistration` diubah menjadi flag `has_unregistration`.
4. `studentAssessment` diagregasi per `id_student` untuk baseline awal.
5. `studentVle` diagregasi per `(code_module, code_presentation, id_student)`.
6. Output disimpan ke:
   - `data/processed/oulad_binary_risk_dataset.csv`

## Script
- Builder: `src/oulad_preprocessing.py`
- Runner: `scripts/build_oulad_binary_dataset.py`
- Test: `tests/test_oulad_preprocessing.py`

## Command eksekusi
```bash
PYTHONPATH=. python3 scripts/build_oulad_binary_dataset.py
```

## Validasi minimum
```bash
PYTHONPATH=. pytest tests/test_oulad_preprocessing.py -q
```

## Catatan metodologis
Preprocessing ini adalah **baseline teragregasi awal**, belum versi final untuk seluruh eksperimen. Pengembangan berikutnya bisa mencakup:
- agregasi assessment berbasis waktu,
- agregasi VLE per minggu atau per activity type,
- feature engineering untuk early prediction,
- encoding kategorikal dan dataset split untuk modeling.

## Output yang diharapkan untuk tahap berikutnya
Setelah file baseline terbentuk, kita sudah bisa lanjut ke:
1. EDA distribusi label dan fitur,
2. visualisasi BI awal,
3. pemilihan 3 algoritma baseline,
4. eksperimen modeling pertama.
