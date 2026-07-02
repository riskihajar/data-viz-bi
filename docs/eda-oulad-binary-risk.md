# EDA Ringkas OULAD — Audit Awal Binary Risk Dataset

Dokumen ini merangkum EDA awal pada dataset turunan OULAD sebelum horizon early warning final dikunci. Angka `unregistration` dan statistik aktivitas sepanjang semester tetap dicatat sebagai audit data sumber, tetapi eksperimen final membatasi fitur prediktor sampai hari ke-28 dan tidak menggunakan `date_unregistration` maupun `has_unregistration` sebagai prediktor.

## Ringkasan dataset
- Total row: **32593**
- Total module: **7**
- Total presentation: **4**
- Unregistration rate: **30.90%**

## Distribusi label risiko
- `Successful`: **15385**
- `AtRisk`: **17208**

## Distribusi final_result asli
- `Pass`: **12361**
- `Withdrawn`: **10156**
- `Fail`: **7052**
- `Distinction`: **3024**

## Statistik numerik utama
- `assessment_count` → min: **0.00**, max: **14.00**, mean: **5.33**
- `assessment_score_mean` → min: **0.00**, max: **100.00**, mean: **57.65**
- `vle_total_clicks` → min: **0.00**, max: **24139.00**, mean: **1215.14**
- `vle_active_days` → min: **0.00**, max: **286.00**, mean: **55.48**
