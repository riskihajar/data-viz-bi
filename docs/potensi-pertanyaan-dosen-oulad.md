# Potensi Pertanyaan Dosen dan Jawaban

Dokumen ini disiapkan sebagai pegangan tanya jawab untuk presentasi notebook `oulad_early_warning_dvbi_colab.ipynb`.

## 1. Mengapa menggunakan OULAD?

**Jawaban:**
Kami menggunakan OULAD karena dataset ini menyediakan data yang relevan untuk learning analytics, yaitu profil mahasiswa, registrasi, assessment, aktivitas VLE, dan hasil akhir. Struktur datanya juga mendukung analisis Business Intelligence karena dapat dipetakan dari data mentah menjadi indikator monitoring risiko mahasiswa.

## 2. Mengapa target `AtRisk` digabung dari `Withdrawn` dan `Fail`?

**Jawaban:**
Karena tujuan sistem adalah early warning untuk mahasiswa yang berpotensi tidak berhasil menyelesaikan pembelajaran. `Withdrawn` dan `Fail` sama-sama menunjukkan kondisi yang membutuhkan perhatian akademik, sehingga keduanya digabung sebagai kelas `AtRisk`. Sementara `Pass` dan `Distinction` digabung sebagai `Successful`.

## 3. Mengapa hanya memakai data sampai hari ke-28?

**Jawaban:**
Hari ke-28 merepresentasikan akhir minggu keempat. Kami ingin membangun sistem peringatan dini, sehingga fitur harus berasal dari periode awal pembelajaran. Jika memakai data setelah minggu keempat, sistem menjadi kurang relevan untuk intervensi dini.

## 4. Mengapa `date_unregistration` tidak dipakai sebagai fitur?

**Jawaban:**
`date_unregistration` tidak digunakan karena merupakan informasi masa depan atau post-hoc. Jika fitur tersebut dimasukkan, model dapat mengetahui indikasi withdrawal secara langsung dan menyebabkan data leakage. Dalam sistem early warning, fitur harus tersedia sebelum keputusan atau kejadian risiko terjadi.

## 5. Apa yang dimaksud dengan data leakage dalam penelitian ini?

**Jawaban:**
Data leakage adalah kondisi ketika model menggunakan informasi yang seharusnya belum tersedia pada waktu prediksi. Contohnya menggunakan hasil akhir mahasiswa atau tanggal keluar sebagai prediktor. Ini bisa membuat performa model terlihat tinggi, tetapi tidak valid ketika diterapkan sebagai sistem prediksi awal.

## 6. Mengapa split data dilakukan berdasarkan `id_student`?

**Jawaban:**
Karena satu mahasiswa dapat muncul lebih dari sekali jika mengambil lebih dari satu modul atau presentation. Jika split dilakukan acak per baris, mahasiswa yang sama bisa muncul di train dan test. Dengan split berdasarkan `id_student`, evaluasi menjadi lebih adil karena mahasiswa yang diuji benar-benar belum pernah dilihat model.

## 7. Mengapa menggunakan tiga model: Logistic Regression, Random Forest, dan XGBoost?

**Jawaban:**
Ketiga model dipilih untuk membandingkan pendekatan yang berbeda. Logistic Regression menjadi baseline yang sederhana dan mudah diinterpretasi. Random Forest dapat menangkap hubungan non-linear dan menangani fitur campuran. XGBoost digunakan karena kuat untuk data tabular dan sering dipakai dalam klasifikasi prediktif.

## 8. Mengapa recall `AtRisk` dijadikan metrik utama?

**Jawaban:**
Dalam konteks early warning, kesalahan yang paling kritis adalah mahasiswa berisiko tetapi tidak terdeteksi. Itu disebut false negative. Recall `AtRisk` mengukur seberapa banyak mahasiswa berisiko yang berhasil ditangkap oleh model. Karena tujuan sistem adalah peringatan dini, recall menjadi prioritas utama.

## 9. Mengapa tidak memilih model dengan accuracy tertinggi?

**Jawaban:**
Accuracy tidak selalu cukup untuk kasus early warning. Model dengan accuracy tinggi bisa saja masih melewatkan banyak mahasiswa `AtRisk`. Kami memilih model berdasarkan recall `AtRisk` karena konteks masalah lebih menekankan cakupan deteksi mahasiswa berisiko daripada sekadar jumlah prediksi benar secara keseluruhan.

## 10. Apa konsekuensi jika recall dinaikkan?

**Jawaban:**
Biasanya precision dapat turun. Artinya, lebih banyak mahasiswa masuk daftar risiko, tetapi tidak semuanya benar-benar `AtRisk`. Dalam konteks akademik, ini berarti tim perlu melakukan verifikasi lebih banyak. Trade-off ini harus disesuaikan dengan kapasitas dosen wali, tutor, atau tim konseling.

## 11. Mengapa perlu knowledge-based risk layer jika sudah ada machine learning?

**Jawaban:**
Machine learning memberikan prediksi dan probabilitas, tetapi belum selalu mudah dijelaskan sebagai alasan tindakan. Knowledge-based risk layer menerjemahkan hasil model dan sinyal perilaku menjadi level risiko, alasan, dan rekomendasi. Ini membuat output lebih operasional untuk pengambil keputusan.

## 12. Bagaimana aturan `High Risk`, `Medium Risk`, dan `Low Risk` dibuat?

**Jawaban:**
Aturan dibuat dari kombinasi prediksi model dan jumlah sinyal perilaku. `High Risk` diberikan jika model memprediksi `AtRisk` dan mahasiswa memiliki minimal dua sinyal risiko. `Medium Risk` diberikan jika model memprediksi `AtRisk` atau memiliki minimal dua sinyal risiko. Selain itu mahasiswa masuk `Low Risk`.

## 13. Mengapa threshold knowledge layer memakai kuartil bawah?

**Jawaban:**
Kuartil bawah digunakan sebagai baseline berbasis data untuk mengidentifikasi mahasiswa dengan perilaku relatif rendah dibandingkan kelompok train. Threshold dihitung dari data train agar tidak mengambil informasi dari data test. Namun threshold ini tetap perlu divalidasi dengan pakar akademik jika diterapkan di institusi nyata.

## 14. Apakah feature importance berarti penyebab dropout?

**Jawaban:**
Tidak. Feature importance menunjukkan kontribusi fitur terhadap prediksi model, bukan hubungan sebab akibat. Misalnya aktivitas VLE rendah berkontribusi dalam membedakan mahasiswa berisiko, tetapi tidak otomatis berarti aktivitas rendah adalah penyebab tunggal dropout. Analisis kausal membutuhkan desain penelitian khusus.

## 15. Apa peran dashboard dalam konteks DVBI?

**Jawaban:**
Dashboard menerjemahkan output model menjadi informasi yang dapat dipantau. Dalam konteks DVBI, dashboard membantu stakeholder melihat jumlah mahasiswa berisiko, distribusi level risiko, area module-presentation yang perlu perhatian, sinyal risiko dominan, dan daftar prioritas intervensi.

## 16. Siapa stakeholder yang menggunakan dashboard ini?

**Jawaban:**
Pimpinan akademik dapat melihat skala risiko dan kebutuhan sumber daya. Program studi dapat melihat modul dengan konsentrasi risiko tinggi. Dosen wali atau tutor dapat melihat daftar mahasiswa prioritas dan alasan risikonya. Tim konseling dapat menggunakan rekomendasi sebagai titik awal tindak lanjut.

## 17. Apa keterbatasan utama penelitian ini?

**Jawaban:**
Pertama, dataset berasal dari konteks Open University di Inggris, sehingga perlu validasi ulang sebelum diterapkan di institusi lain. Kedua, threshold knowledge layer masih berbasis kuartil data, belum hasil validasi pakar. Ketiga, model hanya membaca asosiasi prediktif, bukan hubungan kausal. Keempat, recall yang lebih tinggi dapat meningkatkan beban verifikasi.

## 18. Apakah model ini bisa langsung diterapkan di kampus?

**Jawaban:**
Belum langsung. Model ini adalah prototype decision support. Untuk penerapan nyata, perlu validasi menggunakan data institusi sendiri, penyesuaian fitur LMS, validasi threshold oleh pakar akademik, serta evaluasi apakah intervensi berdasarkan output model benar-benar membantu mahasiswa.

## 19. Mengapa menggunakan supervised learning, bukan clustering?

**Jawaban:**
Karena dataset memiliki label hasil akhir mahasiswa, yaitu `Withdrawn`, `Fail`, `Pass`, dan `Distinction`. Dengan label tersebut, supervised learning lebih sesuai untuk membangun model prediksi. Clustering bisa digunakan sebagai analisis tambahan untuk segmentasi, tetapi bukan fokus utama penelitian ini.

## 20. Bagaimana menangani missing value?

**Jawaban:**
Missing value ditangani di dalam pipeline preprocessing. Fitur numerik diimputasi menggunakan median, sedangkan fitur kategorikal diimputasi lalu diubah menggunakan one-hot encoding. Dengan pipeline, proses imputasi dilakukan hanya berdasarkan data train pada setiap fold sehingga tidak menyebabkan leakage.

## 21. Mengapa memakai cross-validation lima fold?

**Jawaban:**
Cross-validation lima fold digunakan untuk melihat kestabilan performa model pada beberapa pembagian data. Dengan skema ini, hasil evaluasi tidak bergantung pada satu split saja. Karena menggunakan group-based fold, mahasiswa yang sama tidak muncul di train dan validation pada fold yang sama.

## 22. Apa arti false negative dalam confusion matrix?

**Jawaban:**
False negative berarti mahasiswa yang sebenarnya `AtRisk`, tetapi diprediksi sebagai `Successful`. Dalam early warning, false negative penting karena mahasiswa tersebut tidak masuk daftar prioritas, padahal sebenarnya membutuhkan perhatian.

## 23. Apa arti false positive dalam konteks ini?

**Jawaban:**
False positive berarti mahasiswa yang sebenarnya `Successful`, tetapi diprediksi sebagai `AtRisk`. Konsekuensinya, mahasiswa tersebut bisa masuk daftar verifikasi atau intervensi meskipun tidak benar-benar gagal. Ini tidak ideal, tetapi dalam konteks early warning masih dapat diterima selama proses tindak lanjut dilakukan sebagai verifikasi, bukan keputusan final.

## 24. Mengapa hasil model disebut decision support?

**Jawaban:**
Karena sistem tidak menggantikan keputusan manusia. Model hanya memberi sinyal risiko, alasan, dan prioritas. Keputusan akhir tetap perlu mempertimbangkan konteks akademik, komunikasi dengan mahasiswa, dan penilaian dosen atau pengelola program studi.

## 25. Apa kontribusi utama penelitian ini?

**Jawaban:**
Kontribusi utamanya adalah menggabungkan supervised learning, knowledge-based risk layer, dan dashboard BI dalam satu alur. Jadi hasilnya tidak berhenti pada metrik model, tetapi diterjemahkan menjadi level risiko, alasan, rekomendasi, dan daftar prioritas yang dapat digunakan untuk monitoring akademik.

## 26. Jika dosen bertanya: apa yang paling penting dari hasil penelitian ini?

**Jawaban:**
Poin paling penting adalah bahwa data awal pembelajaran, terutama aktivitas VLE dan assessment sampai minggu keempat, sudah dapat digunakan untuk membangun sinyal risiko. Namun, hasil tersebut harus diperlakukan sebagai alat bantu monitoring, bukan keputusan otomatis.

## 27. Jika dosen bertanya: mengapa precision turun setelah knowledge layer?

**Jawaban:**
Precision turun karena knowledge layer memperluas cakupan deteksi. Lebih banyak mahasiswa masuk kategori `High` atau `Medium Risk`, sehingga recall naik, tetapi sebagian tambahan tersebut merupakan false positive. Ini adalah trade-off yang umum pada sistem early warning.

## 28. Jika dosen bertanya: bagaimana mengevaluasi manfaat intervensi?

**Jawaban:**
Manfaat intervensi perlu dievaluasi dengan data lanjutan, misalnya membandingkan mahasiswa yang mendapat tindak lanjut dengan yang tidak, atau melihat perubahan aktivitas setelah intervensi. Untuk evaluasi yang lebih kuat, bisa digunakan desain eksperimen atau quasi-experiment.

## 29. Jika dosen bertanya: apakah model adil untuk semua kelompok mahasiswa?

**Jawaban:**
Pada notebook ini fokus evaluasi masih pada performa prediksi umum. Untuk penerapan nyata, perlu evaluasi fairness berdasarkan kelompok seperti gender, region, disability, atau kategori sosial ekonomi. Ini penting agar model tidak menghasilkan bias yang merugikan kelompok tertentu.

## 30. Jika dosen bertanya: pengembangan berikutnya apa?

**Jawaban:**
Pengembangan berikutnya adalah validasi dengan data institusi sendiri, menambahkan fitur temporal mingguan, melakukan evaluasi fairness, menguji dampak intervensi, dan mengintegrasikan output ke LMS atau dashboard operasional kampus.

