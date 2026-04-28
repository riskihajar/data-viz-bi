# Catatan Arah Capstone DVBI

## Konteks project
Project ini berada pada repo **Data Visualization and Business Intelligence (DVBI)** dengan tema utama:
- **Student Performance / Dropout Analytics**

Tema ini tetap dipertahankan sebagai arah kerja utama. Namun, pemilihan dataset dan formulasi problem harus mengikuti **syarat capstone dari dosen** agar project tidak salah arah.

## Syarat capstone dari dosen
### Data Tabular dan Image
- **Klasifikasi:** minimal **1.000 data per class**
- **Forecasting:** minimal **5.000 baris data**
- **Regresi:** minimal **5.000 baris data**
- **Clustering:** minimal **5.000 baris data**

### Text Mining
- minimal **10.000 baris data**

### Ketentuan tambahan
- minimal menggunakan **tiga algoritma** yang berbeda
- perlu mempertimbangkan **jumlah fitur**

## Implikasi untuk project ini
Karena tema yang dipilih adalah **student performance / dropout analytics**, jalur yang paling relevan adalah:
- **tabular classification**
- dengan dataset yang cukup besar dan distribusi kelas yang memenuhi syarat dosen

## Evaluasi dataset UCI yang sempat dipilih
Dataset: **Predict Students' Dropout and Academic Success** (UCI)

Ringkasan cepat:
- total baris: **4.424**
- total fitur: **36**
- target: `Dropout`, `Enrolled`, `Graduate`
- distribusi kelas:
  - `Dropout`: **1.421**
  - `Graduate`: **2.209**
  - `Enrolled`: **794**

## Kesimpulan evaluasi dataset UCI
Dataset UCI ini **relevan secara tema**, tetapi **belum aman sebagai dataset final capstone** karena:
1. pada formulasi **3-class classification**, kelas `Enrolled` hanya **794**, sehingga **tidak memenuhi** syarat minimal **1.000 data per class**;
2. total baris **4.424**, sehingga **tidak memenuhi** syarat 5.000 baris jika nanti project bergeser ke regresi / clustering / forecasting;
3. dataset ini tetap berguna sebagai referensi baseline dan bahan eksplorasi awal, tetapi **bukan kandidat final paling aman** untuk capstone.

## Arah keputusan ke depan
Agar project tidak kehilangan konteks, keputusan kerja berikut dikunci:
1. **Tema tetap:** Student Performance / Dropout Analytics
2. **Prioritas problem type:** tabular classification
3. **Dataset final harus memenuhi syarat capstone**, terutama:
   - minimal 1.000 data per class untuk klasifikasi
   - jumlah fitur cukup memadai untuk analisis dan visualisasi
4. Dataset UCI yang sudah diunduh diperlakukan sebagai:
   - referensi pembanding,
   - baseline eksplorasi,
   - bukan pilihan final sebelum ada verifikasi kandidat dataset lain.

## Konsekuensi metodologis
Sebelum masuk preprocessing, kita harus menyelesaikan urutan berikut:
1. shortlist kandidat dataset yang sesuai syarat capstone;
2. verifikasi jumlah baris, jumlah kelas, distribusi label, dan jumlah fitur;
3. pilih satu dataset final yang paling aman;
4. baru setelah itu menyusun preprocessing plan.

## Catatan kerja
Jika suatu dataset sangat relevan secara tema tetapi tidak memenuhi syarat jumlah data/class, dataset tersebut tidak langsung dijadikan dataset final capstone tanpa justifikasi atau persetujuan dosen.
