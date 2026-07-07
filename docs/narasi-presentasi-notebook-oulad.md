# Narasi Presentasi Notebook OULAD Early Warning

Dokumen ini adalah naskah baca terpisah untuk presentasi notebook `notebooks/oulad_early_warning_dvbi_colab.ipynb`. Narasi ini tidak perlu dimasukkan ke cell notebook, karena notebook akan ditampilkan sebagai media visual dan eksekusi.

## Pembagian Presenter

| Presenter | Bagian Notebook | Fokus |
|---|---|---|
| Presenter 1 | Pembukaan sampai Section 5 | konteks masalah, dataset, pembentukan data, anti-leakage |
| Presenter 2 | Section 6 sampai Section 12 | EDA, split data, pipeline model, evaluasi, interpretasi model |
| Presenter 3 | Section 13 sampai Section 18 | knowledge-based risk layer, dashboard, insight BI, kesimpulan |

---

## Presenter 1 - Pembukaan dan Persiapan Data

### Pembukaan

Assalamualaikum warahmatullahi wabarakatuh, selamat pagi atau siang Bapak/Ibu dosen dan teman-teman semua.

Kami dari Kelompok 5 akan mempresentasikan notebook berjudul "Early Warning Risiko Mahasiswa OULAD". Fokus notebook ini adalah membangun sistem pendukung keputusan untuk mendeteksi mahasiswa yang berisiko gagal atau mengundurkan diri sejak minggu keempat perkuliahan.

Target yang digunakan adalah dua kelas. Kelas `AtRisk` mencakup mahasiswa dengan hasil akhir `Withdrawn` atau `Fail`, sedangkan kelas `Successful` mencakup mahasiswa dengan hasil akhir `Pass` atau `Distinction`.

Hasil model ini kami posisikan sebagai decision support. Model membantu memberi sinyal awal, lalu dosen atau pengelola program studi dapat memadukannya dengan konteks akademik sebelum menentukan bentuk intervensi.

### Section 1 - Persiapan Library

Pada bagian pertama, kami menyiapkan seluruh library yang dibutuhkan untuk pengolahan data, visualisasi, preprocessing, pemodelan, dan evaluasi.

Di sini kami juga menetapkan `RANDOM_STATE` agar eksperimen dapat direproduksi, serta `CUTOFF_DAY` sebesar 28. Nilai ini berarti seluruh fitur perilaku mahasiswa hanya dihitung sampai akhir minggu keempat.

Pembatasan waktu ini selaras dengan tujuan early warning, karena fitur yang digunakan merepresentasikan informasi yang tersedia sampai minggu keempat.

### Section 2 - Mengunduh Dataset OULAD

Pada bagian kedua, notebook mengunduh Open University Learning Analytics Dataset atau OULAD secara otomatis dari UCI Machine Learning Repository.

Langkah ini mendukung reproduksibilitas eksperimen, karena pengguna dapat menjalankan notebook dari runtime Google Colab baru tanpa mengunggah file secara manual. Jika file sudah tersedia di runtime, proses download akan dilewati.

Output pada section ini menunjukkan daftar file CSV yang berhasil ditemukan dan divalidasi.

### Section 3 - Membaca dan Memeriksa Data Sumber

Setelah dataset tersedia, notebook membaca tabel-tabel utama yang digunakan dalam analisis.

Tabel `studentInfo` berisi profil mahasiswa dan hasil akhir. Tabel `studentRegistration` berisi informasi tanggal registrasi. Tabel `assessments` memberi konteks tugas atau penilaian. Sementara `studentAssessment` dan `studentVle` menggambarkan aktivitas assessment serta aktivitas mahasiswa pada Virtual Learning Environment.

Tujuan section ini adalah memastikan struktur data sudah terbaca dengan benar sebelum dilakukan penggabungan dan agregasi.

### Section 4 - Membentuk Dataset Early Warning Minggu Ke-4

Pada section ini, data mentah diubah menjadi dataset analisis. Ini adalah preprocessing tahap pertama dalam notebook, yaitu preprocessing dari data mentah OULAD menjadi dataset early warning.

Unit analisis yang digunakan adalah satu mahasiswa pada satu module-presentation. Artinya, satu baris mewakili seorang mahasiswa dalam satu modul dan satu periode pembelajaran.

Assessment difilter menggunakan `date_submitted <= 28`, sedangkan aktivitas VLE difilter menggunakan `date <= 28`. Setelah itu, data diagregasi menjadi fitur seperti jumlah assessment, rata-rata skor, total klik VLE, jumlah hari aktif, dan aktivitas terakhir sampai hari ke-28.

Fitur seperti tanggal unregistration tidak digunakan sebagai prediktor karena informasi tersebut berada di luar cakupan early warning minggu keempat. Dengan begitu, fitur model tetap konsisten dengan skenario deteksi dini.

Jadi, preprocessing pada notebook ini dilakukan dalam dua level. Pertama, preprocessing data mentah menjadi dataset early warning pada Section 4. Kedua, preprocessing fitur untuk model machine learning pada Section 8.

### Section 5 - Validasi Anti-Leakage

Bagian ini memastikan seluruh fitur prediktor hanya berasal dari informasi yang tersedia pada atau sebelum hari ke-28.

Validasi anti-leakage membantu menjaga evaluasi tetap sesuai dengan kondisi nyata early warning. Fokusnya adalah memastikan model belajar dari informasi yang memang tersedia saat sistem memberi sinyal awal.

Output yang diharapkan adalah status lulus validasi serta daftar fitur kategorikal dan numerik yang digunakan untuk pemodelan.

Sampai di sini, bagian pertama sudah menyiapkan dataset yang siap dipakai untuk eksplorasi dan pemodelan.

---

## Presenter 2 - EDA, Model, dan Evaluasi

### Section 6 - Exploratory Data Analysis

Pada bagian EDA, kami melihat distribusi kelas target, missing values, serta pola awal antara mahasiswa `AtRisk` dan `Successful`.

Tujuan EDA adalah membaca distribusi data dan melihat pola awal yang berpotensi menjadi sinyal risiko pada empat minggu pertama.

Perbedaan yang diamati mencakup aktivitas assessment dan VLE, misalnya jumlah assessment yang dikumpulkan, skor assessment, total klik, dan jumlah hari aktif. Semua angka tetap dibaca dalam konteks cut-off hari ke-28.

### Section 7 - Pembagian Data Berdasarkan Mahasiswa

Setelah EDA, data dibagi menjadi train-validation dan hold-out test.

Pembagian dilakukan berdasarkan `id_student`, bukan baris acak biasa. Hal ini penting karena seorang mahasiswa bisa muncul lebih dari sekali jika mengambil lebih dari satu modul.

Dengan group-based split, mahasiswa yang sama ditempatkan hanya pada salah satu bagian data. Strategi ini membuat evaluasi lebih representatif untuk membaca performa pada mahasiswa yang berbeda.

### Section 8 - Pipeline Preprocessing dan Model

Pada section ini, notebook membangun pipeline preprocessing dan model. Ini adalah preprocessing tahap kedua, yaitu preprocessing fitur sebelum masuk ke algoritma machine learning.

Fitur numerik diimputasi dengan median dan distandardisasi. Fitur kategorikal diimputasi lalu diubah dengan one-hot encoding.

Semua transformasi dimasukkan ke dalam pipeline agar proses preprocessing hanya belajar dari data train pada setiap fold. Ini menjaga prosedur evaluasi tetap konsisten.

Tiga model yang dibandingkan adalah Logistic Regression, Random Forest, dan XGBoost. Logistic Regression digunakan sebagai baseline linear, Random Forest sebagai ensemble berbasis pohon, dan XGBoost sebagai boosting model untuk data tabular.

### Section 9 - Cross-Validation Lima Fold

Evaluasi awal dilakukan menggunakan lima fold cross-validation berbasis kelompok mahasiswa.

Metrik utama yang digunakan adalah recall untuk kelas `AtRisk`. Dalam konteks early warning, recall membantu melihat seberapa luas sistem menangkap mahasiswa yang berpotensi membutuhkan perhatian awal.

F1-score digunakan sebagai tie-breaker jika recall antar model berdekatan. Selain itu, notebook juga menampilkan accuracy, precision, dan ROC-AUC agar performa model tetap terbaca secara seimbang.

### Section 10 - Evaluasi Akhir pada Hold-Out Test

Setelah cross-validation, model terbaik dipilih berdasarkan recall `AtRisk` dan F1. Model tersebut kemudian dilatih ulang pada seluruh data train-validation.

Evaluasi akhir dilakukan pada hold-out test, yaitu data yang dipisahkan sejak awal dan tidak digunakan selama training maupun pemilihan model.

Bagian ini memberi gambaran performa model pada data uji yang terpisah. Output utamanya adalah tabel perbandingan metrik dan nama model terbaik.

### Section 11 - Visualisasi Evaluasi Model

Pada bagian ini, hasil evaluasi divisualisasikan agar mudah dibandingkan.

Notebook menampilkan grafik perbandingan metrik, confusion matrix, dan ROC curve.

Confusion matrix membantu melihat jenis prediksi yang benar dan keliru. Salah satu bagian yang dibaca adalah false negative kelas `AtRisk`, yaitu mahasiswa berisiko yang belum tertangkap oleh model.

### Section 12 - Faktor yang Memengaruhi Model Terbaik

Setelah model terbaik dipilih, notebook menampilkan fitur yang paling berpengaruh.

Jika model berbasis pohon, yang ditampilkan adalah feature importance. Jika modelnya Logistic Regression, yang ditampilkan adalah nilai absolut coefficient.

Bagian ini membantu menjelaskan fitur mana yang paling banyak berkontribusi dalam prediksi. Interpretasinya dibaca sebagai kontribusi prediktif dalam model, bukan sebagai hubungan sebab akibat.

Sampai bagian ini, notebook sudah menghasilkan model prediksi dan ringkasan evaluasi. Bagian berikutnya menerjemahkan hasil model menjadi level risiko dan indikator Business Intelligence.

---

## Presenter 3 - Knowledge Layer, Dashboard, dan Kesimpulan

### Section 13 - Knowledge-Based Risk Layer

Pada section ini, hasil machine learning diterjemahkan menjadi kategori risiko yang lebih operasional.

Model menghasilkan prediksi dan probabilitas `AtRisk`. Knowledge-based risk layer menambahkan sinyal perilaku seperti skor assessment rendah, jumlah assessment rendah, total klik VLE rendah, dan jumlah hari aktif VLE rendah.

Threshold sinyal dihitung dari data train menggunakan kuartil bawah, sehingga aturan konsisten dengan alur evaluasi berbasis data latih dan data uji terpisah.

Aturannya adalah: `High Risk` diberikan ketika model memprediksi `AtRisk` dan terdapat minimal dua sinyal perilaku. `Medium Risk` diberikan ketika model memprediksi `AtRisk` atau terdapat minimal dua sinyal perilaku. Selain itu, mahasiswa masuk kategori `Low Risk`.

Keluaran bagian ini tidak hanya berupa label risiko, tetapi juga alasan risiko dan rekomendasi tindak lanjut.

### Section 14 - Evaluasi Sistem Gabungan

Setelah risk layer dibuat, notebook mengevaluasi sistem gabungan.

Untuk evaluasi, kategori `High Risk` dan `Medium Risk` dipetakan kembali sebagai `AtRisk`. Kemudian metriknya dibandingkan dengan model machine learning terbaik.

Penambahan knowledge layer dapat memperluas cakupan deteksi karena lebih banyak mahasiswa masuk antrean verifikasi. Di sisi lain, precision perlu dibaca bersama karena jumlah kasus yang perlu ditinjau juga dapat bertambah.

Keseimbangan antara recall dan precision dibaca bersama kapasitas institusi. Dengan begitu, daftar prioritas dapat disesuaikan dengan jumlah kasus yang realistis untuk ditindaklanjuti.

### Section 15 - Dashboard Statis DVBI

Bagian dashboard menyatukan hasil model, risk level, dan indikator monitoring dalam satu tampilan.

Dashboard menampilkan KPI, distribusi level risiko, risiko per module-presentation, probabilitas, sinyal dominan, pola perilaku berdasarkan level, dan confusion matrix.

Tujuannya adalah menerjemahkan output analitik menjadi informasi yang mudah dibaca oleh stakeholder. Pimpinan akademik dapat melihat skala risiko, program studi dapat melihat modul prioritas, dan dosen wali atau tutor dapat melihat daftar mahasiswa yang membutuhkan perhatian awal.

### Section 16 - Daftar Prioritas dan Insight Business Intelligence

Pada section ini, notebook menyusun daftar prioritas mahasiswa dengan level risiko tertinggi.

Mahasiswa diurutkan berdasarkan probabilitas risiko dan jumlah sinyal. Outputnya mencakup ID mahasiswa, level risiko, alasan risiko, dan rekomendasi tindakan.

Insight BI membantu menjawab tiga pertanyaan utama: area mana yang memiliki konsentrasi risiko lebih tinggi, sinyal risiko apa yang menonjol, dan siapa yang dapat diprioritaskan untuk tindak lanjut.

### Section 17 - Ekspor Hasil untuk Pelaporan

Bagian ini menyimpan hasil analisis ke file CSV.

File yang diekspor dapat digunakan untuk laporan, analisis lanjutan, atau bahan awal integrasi jika sistem dikembangkan menjadi dashboard operasional.

Dengan ekspor ini, notebook menyediakan output terstruktur yang bisa dipakai ulang setelah sesi analisis selesai.

### Section 18 - Kesimpulan dan Keterbatasan

Sebagai kesimpulan, notebook ini membandingkan tiga model supervised learning pada skenario early warning minggu keempat.

Model dipilih berdasarkan recall kelas `AtRisk`, karena tujuan sistem adalah memberi cakupan deteksi awal yang baik untuk mahasiswa berisiko. Setelah itu, knowledge-based risk layer menambahkan level risiko, alasan, dan rekomendasi agar hasil model lebih mudah dibaca oleh stakeholder.

Dashboard kemudian menerjemahkan keluaran tersebut menjadi indikator monitoring dan daftar prioritas tindak lanjut.

Keterbatasannya, label berasal dari hasil akhir, sementara prediktor dibatasi sampai hari ke-28. Threshold aturan berbasis kuartil data dan akan lebih kuat jika divalidasi bersama pakar akademik. Selain itu, OULAD berasal dari konteks Open University di Inggris, sehingga penerapan pada institusi lain perlu diawali dengan penyesuaian dan validasi lokal.

Secara keseluruhan, notebook ini memberi contoh integrasi machine learning, rule-based reasoning, dan dashboard BI sebagai decision support untuk monitoring mahasiswa berisiko.

Demikian presentasi notebook dari Kelompok 5. Terima kasih atas perhatian Bapak/Ibu dosen dan teman-teman semua. Wassalamualaikum warahmatullahi wabarakatuh.
