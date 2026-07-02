# Audit Dataset OULAD

## Sumber unduh
- URL stabil terverifikasi: `https://analyse.kmi.open.ac.uk/open-dataset/download`
- Response header mengembalikan:
  - `Content-Disposition: attachment; filename=anonymisedData.zip`
  - `Content-Type: APPLICATION/ZIP`
  - `Content-Length: 46750706` bytes (~44.6 MB)
- File berhasil diunduh ke: `data/oulad/anonymisedData.zip`
- Dataset berhasil diekstrak di: `data/oulad/`

## Cara download ulang via script
```bash
PYTHONPATH=. python3 scripts/download_oulad.py
```

Opsi tambahan:
- download saja tanpa extract:
```bash
PYTHONPATH=. python3 scripts/download_oulad.py --no-extract
```
- paksa download ulang dan extract ulang:
```bash
PYTHONPATH=. python3 scripts/download_oulad.py --force
```

## File hasil ekstraksi
- `assessments.csv` — 206 rows, 6 cols
- `courses.csv` — 22 rows, 3 cols
- `studentAssessment.csv` — 173,912 rows, 5 cols
- `studentInfo.csv` — 32,593 rows, 12 cols
- `studentRegistration.csv` — 32,593 rows, 5 cols
- `studentVle.csv` — 10,655,280 rows, 6 cols
- `vle.csv` — 6,364 rows, 6 cols

## Struktur tabel
### assessments.csv
- Columns: `code_module`, `code_presentation`, `id_assessment`, `assessment_type`, `date`, `weight`

### courses.csv
- Columns: `code_module`, `code_presentation`, `module_presentation_length`

### studentAssessment.csv
- Columns: `id_assessment`, `id_student`, `date_submitted`, `is_banked`, `score`

### studentInfo.csv
- Columns: `code_module`, `code_presentation`, `id_student`, `gender`, `region`, `highest_education`, `imd_band`, `age_band`, `num_of_prev_attempts`, `studied_credits`, `disability`, `final_result`

### studentRegistration.csv
- Columns: `code_module`, `code_presentation`, `id_student`, `date_registration`, `date_unregistration`

### studentVle.csv
- Columns: `code_module`, `code_presentation`, `id_student`, `id_site`, `date`, `sum_click`

### vle.csv
- Columns: `id_site`, `code_module`, `code_presentation`, `activity_type`, `week_from`, `week_to`

## Distribusi target utama `studentInfo.final_result`
- `Pass`: **12,361**
- `Withdrawn`: **10,156**
- `Fail`: **7,052**
- `Distinction`: **3,024**

## Verifikasi syarat capstone
Untuk skenario **tabular classification** dengan target `final_result`:
- semua kelas **> 1.000** data ✅
- total data `studentInfo` = **32,593** ✅
- tersedia fitur demografis + registrasi + assessment + aktivitas VLE ✅

Kesimpulan: **OULAD lolos syarat capstone secara aman untuk klasifikasi.**

## Cakupan dataset
- Unique module: **7** → `AAA`, `BBB`, `CCC`, `DDD`, `EEE`, `FFF`, `GGG`
- Unique presentation: **4** → `2013B`, `2013J`, `2014B`, `2014J`

## Missing values penting
### studentInfo.csv
- `imd_band`: **1,111** missing
- kolom lain: **0** missing terdeteksi

### studentRegistration.csv
- `date_registration`: **45** missing
- `date_unregistration`: **22,521** missing

Catatan: `date_unregistration` kemungkinan besar missing karena banyak student tidak unregister, jadi ini belum tentu masalah kualitas data.

Catatan final: `date_unregistration` tetap diaudit sebagai kolom sumber, tetapi tidak digunakan sebagai prediktor pada eksperimen final karena merepresentasikan informasi masa depan untuk skenario early warning hari ke-28.

### studentAssessment.csv
- `score`: **173** missing

### studentVle.csv
- tidak ditemukan missing kosong berbasis parsing CSV sederhana pada kolom inti

## Statistik `studentVle.sum_click`
- Count: **10,655,280**
- Min: **1**
- Max: **6,977**
- Mean: **3.7169**

## Implikasi metodologis
OULAD adalah **multi-table dataset**, jadi preprocessing tidak bisa langsung disamakan dengan dataset tabular tunggal seperti UCI sebelumnya.

Urutan logis preprocessing nanti:
1. tentukan **unit analisis final**: paling aman `1 row = 1 student pada 1 module-presentation`;
2. gunakan `studentInfo` sebagai base table karena label `final_result` sudah tersedia;
3. join / agregasi dari:
   - `studentRegistration` untuk konteks registrasi,
   - `studentAssessment` untuk performa penilaian,
   - `studentVle` untuk engagement LMS,
   - `vle` untuk tipe aktivitas pembelajaran,
   - `courses` dan `assessments` untuk konteks akademik;
4. handle missing values secara terkontrol, terutama `imd_band`, `date_registration`, `score`, dan `date_unregistration`;
5. baru lakukan encoding, scaling bila perlu, feature selection/engineering, lalu split data.

## Framing problem final
### Arah utama
Gunakan problem framing:
**early warning student risk classification berbasis engagement dan academic behavior pada OULAD**

### Formulasi final
Target binary risk:
- `AtRisk` = `Withdrawn` + `Fail`
- `Successful` = `Pass` + `Distinction`

Horizon prediksi dibatasi sampai hari ke-28. Assessment dan aktivitas VLE setelah hari ke-28 tidak dipakai sebagai fitur. `date_unregistration`, `has_unregistration`, dan `final_result` juga tidak dipakai sebagai prediktor.

Formulasi ini menjaga evaluasi tetap selaras dengan kondisi intervensi dini: model hanya melihat informasi yang tersedia pada saat prediksi.

## Kesimpulan singkat
- **OULAD menjadi dataset final** untuk project ini.
- Framing final menggunakan binary risk early warning dengan cut-off hari ke-28.
- Dibanding opsi dataset sebelumnya, **OULAD adalah pilihan paling aman dan paling kuat** untuk capstone DVBI.
