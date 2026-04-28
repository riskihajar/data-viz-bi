# Audit Dataset OULAD

## Sumber unduh
- URL stabil terverifikasi: `https://analyse.kmi.open.ac.uk/open-dataset/download`
- Response header mengembalikan:
  - `Content-Disposition: attachment; filename=anonymisedData.zip`
  - `Content-Type: APPLICATION/ZIP`
  - `Content-Length: 46750706` bytes (~44.6 MB)
- File berhasil diunduh ke: `data/oulad/anonymisedData.zip`
- Dataset berhasil diekstrak di: `data/oulad/`

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
   - `studentRegistration` untuk sinyal registrasi/unregistration,
   - `studentAssessment` untuk performa penilaian,
   - `studentVle` untuk engagement LMS,
   - `vle` untuk tipe aktivitas pembelajaran,
   - `courses` dan `assessments` untuk konteks akademik;
4. handle missing values secara terkontrol, terutama `imd_band`, `date_registration`, `score`, dan `date_unregistration`;
5. baru lakukan encoding, scaling bila perlu, feature selection/engineering, lalu split data.

## Rekomendasi framing problem sebelum preprocessing
### Rekomendasi utama
Gunakan problem framing:
**student outcome classification berbasis engagement dan academic behavior pada OULAD**

### Formulasi paling aman
Ada dua opsi bagus:

1. **4-class classification**
   - target: `Pass`, `Withdrawn`, `Fail`, `Distinction`
   - kelebihan: paling faithful ke dataset asli
   - kekurangan: sedikit lebih kompleks

2. **3-class classification**
   - target: `Pass`, `Fail`, `Withdrawn`
   - perlakuan `Distinction`: gabung ke `Pass`
   - kelebihan: lebih sederhana untuk storytelling BI dan modeling awal
   - kekurangan: informasi distinction hilang sebagai kelas terpisah

### Saran praktis
Untuk capstone DVBI, paling aman mulai dari:
- **baseline utama: 3-class / atau binary risk framing yang mudah dijelaskan**, lalu
- simpan versi 4-class sebagai perluasan jika dibutuhkan.

Jika tujuan utama presentasi adalah **early warning dropout/risk analytics**, framing paling kuat justru:
- **binary classification**: `Withdrawn` vs `Non-withdrawn`
atau
- **binary classification**: `At-risk (Withdrawn + Fail)` vs `Successful (Pass + Distinction)`

Namun karena dosen meminta minimal 1.000 data per class, kedua framing binary ini juga tetap aman.

## Kesimpulan singkat
- **Ya, sekarang kita sudah punya basis kuat untuk masuk ke preprocessing OULAD.**
- Tetapi preprocessing sebaiknya dimulai **setelah problem framing final dikunci**.
- Dibanding opsi dataset sebelumnya, **OULAD sekarang adalah kandidat final paling aman dan paling kuat** untuk project ini.
