# Pemilihan Dataset untuk Capstone DVBI

## Tujuan dokumen
Dokumen ini mencatat proses pemilihan dataset yang **aman terhadap syarat capstone dosen** sambil mempertahankan tema project:
- **Student Performance / Dropout Analytics**

## Ringkasan syarat capstone yang relevan
Untuk jalur **tabular classification**, target minimalnya adalah:
- **minimal 1.000 data per class**
- minimal **3 algoritma berbeda**
- jumlah fitur perlu cukup layak untuk analisis

## Kandidat 1 — Open University Learning Analytics Dataset (OULAD)
### Status
**Dataset final yang dipakai**

### Sumber
- Situs dataset: https://analyse.kmi.open.ac.uk/open_dataset
- Paper dataset: Kuzilek, Hlosta, Zdrahal (2017)
- Referensi repo analisis yang memuat ringkasan ukuran data:
  - https://github.com/tranmink/OULAD
  - https://github.com/shshen-closer/Open-University-Learning-Analytics-dataset
  - https://github.com/SinanCavusoglu/Open-University-Learning-Analytics-Dataset

### Ringkasan ukuran yang terverifikasi dari referensi
Dari README repositori analisis OULAD, ditemukan ringkasan berikut:
- `studentInfo`: **32.593** baris
- `studentVLE`: **10.655.280** baris log interaksi
- data mencakup mahasiswa, course, assessment, dan aktivitas VLE
- outcome menggunakan `final_result`

### Label / kelas target
README analisis menyebut outcome `final_result` dengan kelas:
- `Pass`
- `Withdraw`
- `Fail`
- `Distinction`

Distribusi yang disebut pada referensi analisis:
- **42% Pass**
- **25% Withdraw**
- **23% Fail**
- **10% Distinction**

### Evaluasi terhadap syarat dosen
Jika memakai total `studentInfo` = **32.593** dan distribusi di atas, maka estimasi jumlah per kelas kira-kira:
- Pass ≈ 13.689
- Withdraw ≈ 8.148
- Fail ≈ 7.496
- Distinction ≈ 3.259

Artinya:
- semua kelas **melewati 1.000 data per class** ✅
- total data jauh di atas 5.000 ✅
- jumlah data dan fitur sangat memadai untuk BI + modeling ✅

### Kelebihan
1. Sangat kuat untuk capstone secara ukuran data.
2. Masih sangat relevan dengan tema student performance / dropout / retention.
3. Mendukung banyak arah analisis:
   - klasifikasi hasil akhir mahasiswa,
   - early warning,
   - analisis engagement LMS,
   - dashboard BI berbasis perilaku belajar.
4. Dataset kaya karena ada gabungan:
   - profil mahasiswa,
   - registrasi,
   - assessment,
   - VLE clickstream.

### Risiko / catatan
1. Dataset lebih kompleks daripada UCI sebelumnya.
2. Preprocessing akan lebih berat karena multi-table dan perlu join/agregasi.
3. Untuk eksperimen final, target direformulasi menjadi binary risk:
   - `AtRisk` = `Withdrawn` + `Fail`
   - `Successful` = `Pass` + `Distinction`
4. Horizon early warning final dibatasi sampai hari ke-28, sehingga fitur masa depan seperti status unregistration tidak dipakai sebagai prediktor.

### Penilaian akhir
**Dipilih sebagai dataset final karena paling kuat untuk analisis early warning, dashboard BI, dan storytelling intervensi dini.**

---

## Kandidat 2 — UCI Predict Students' Dropout and Academic Success
### Status
**Relevan tema, tetapi tidak paling aman untuk capstone**

### Ringkasan
- total baris: **4.424**
- kelas:
  - `Dropout`: 1.421
  - `Graduate`: 2.209
  - `Enrolled`: 794

### Evaluasi terhadap syarat dosen
- `Enrolled` < 1.000 ❌
- total baris < 5.000 ❌

### Penilaian akhir
Masih berguna sebagai baseline / pembanding, tetapi **kurang aman sebagai dataset final**.

---

## Kandidat 3 — turunan Kaggle/Hugging Face dari dataset student dropout / academic success
### Contoh yang ditemukan
- `jason1966/adilshamim8_predict-students-dropout-and-academic-success`
- `Mitul1999/student-academic-success-and-demographics-dataset`
- `jason1966/abdullah0a_student-dropout-analysis-and-prediction-dataset`

### Catatan
Saat ini metadata yang terlihat menunjukkan ukuran kecil atau menengah, misalnya:
- `size_categories: 1K<n<10K`
- beberapa tampak merupakan rehost / mirror dataset yang sudah ada

### Evaluasi sementara
- belum ada bukti kuat bahwa dataset-dataset ini **lebih baik dari OULAD** untuk memenuhi syarat capstone;
- sebagian berisiko hanya merupakan salinan dari dataset yang sama seperti UCI atau dataset kecil lain;
- perlu verifikasi isi sebelum dijadikan kandidat serius.

### Penilaian akhir
**Kandidat cadangan saja**, bukan prioritas utama.

---

## Keputusan final
### Dataset yang digunakan
**Open University Learning Analytics Dataset (OULAD)**

### Alasan utama
- paling aman terhadap syarat dosen,
- tetap satu tema dengan project kita,
- sangat kaya untuk kebutuhan Data Visualization dan Business Intelligence,
- mendukung minimal 3 algoritma dengan dataset yang cukup besar,
- cukup kuat untuk dibawa ke analisis, dashboard, dan storytelling BI.

## Keputusan kerja yang disarankan
1. Gunakan **OULAD** sebagai dataset final.
2. Pakai formulasi binary risk untuk early warning:
   - `AtRisk` = `Withdrawn` + `Fail`
   - `Successful` = `Pass` + `Distinction`
3. Batasi fitur prediktor sampai hari ke-28 agar evaluasi sesuai dengan skenario intervensi dini.
4. Simpan dataset UCI sebelumnya sebagai pembanding historis, bukan pilihan final.

## Kesimpulan singkat
Jika tujuan project adalah **aman terhadap syarat capstone dan tetap konsisten dengan tema early warning**, maka **OULAD adalah dataset final yang digunakan**.
