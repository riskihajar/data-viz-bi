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
Cross-validation lima fold digunakan untuk melihat kestabilan performa model pada beberapa pembagian data. Dengan skema ini, hasil evaluasi tidak bergantung pada satu split saja. Karena menggunakan group-based fold, mahasiswa yang sama tidak muncul di train dan validation pada fold yang sama. Hasil cross-validation juga dilaporkan dalam bentuk rata-rata dan standar deviasi.

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

## 31. Jika dosen bertanya: rasio data split yang digunakan berapa?

**Jawaban:**
Rasio split yang digunakan adalah 80% train-validation dan 20% hold-out test. Secara jumlah, train-validation berisi 26.122 baris, sedangkan hold-out test berisi 6.471 baris. Split dilakukan menggunakan `GroupShuffleSplit` dengan `id_student` sebagai grup, sehingga mahasiswa yang sama tidak muncul di train dan test sekaligus.

## 32. Jika dosen bertanya: mengapa tidak memakai 70:20:10?

**Jawaban:**
Kami tidak memakai 70:20:10 karena validasi tidak dibuat sebagai satu validation set statis. Bagian 80% train-validation masih dievaluasi menggunakan 5-fold `GroupKFold`, sehingga setiap bagian data bergantian menjadi validation. Dengan begitu, data training tetap lebih banyak, evaluasi lebih stabil, dan 20% hold-out test tetap disimpan sebagai data uji akhir yang belum dipakai saat training maupun pemilihan model.

## 33. Jika dosen bertanya: apakah ada standar deviasi hasil model?

**Jawaban:**
Ada. Standar deviasi diambil dari hasil 5-fold `GroupKFold` cross-validation. Untuk model final Random Forest, hasilnya adalah accuracy 0,7538 ± 0,0033, precision `AtRisk` 0,7999 ± 0,0148, recall `AtRisk` 0,7126 ± 0,0040, F1 `AtRisk` 0,7536 ± 0,0050, dan ROC-AUC 0,8362 ± 0,0026. Nilai standar deviasi yang kecil menunjukkan performa model relatif stabil antar fold.

## 34. Jika dosen bertanya: sudah berapa kali eksperimen dijalankan?

**Jawaban:**
Untuk validasi, setiap model dijalankan dalam skema 5-fold cross-validation. Artinya setiap model dilatih dan divalidasi 5 kali pada fold yang berbeda. Karena ada tiga model, yaitu Logistic Regression, Random Forest, dan XGBoost, total proses cross-validation adalah 15 fit evaluasi. Setelah model terbaik dipilih, model final dilatih ulang pada seluruh train-validation dan diuji sekali pada hold-out test.

## 35. Jika dosen bertanya: random seed yang digunakan berapa?

**Jawaban:**
Random seed yang digunakan adalah 42 melalui variabel `RANDOM_STATE = 42`. Seed ini dipakai pada `GroupShuffleSplit` dan model yang memiliki komponen random seperti Random Forest dan XGBoost. Tujuannya agar pembagian data dan hasil eksperimen dapat direproduksi.

## 36. Jika dosen bertanya: apakah `Fail` dan `Withdrawn` sebenarnya sama?

**Jawaban:**
Secara akademik, `Fail` dan `Withdrawn` tidak sama. `Fail` berarti mahasiswa menyelesaikan proses tetapi tidak lulus, sedangkan `Withdrawn` berarti mahasiswa keluar atau berhenti dari modul. Namun dalam konteks early warning, keduanya sama-sama menunjukkan kondisi tidak berhasil atau membutuhkan perhatian akademik, sehingga digabung menjadi kelas `AtRisk`.

## 37. Jika dosen bertanya: mengapa cut-off hari ke-28, bukan minggu ke-2 atau minggu ke-8?

**Jawaban:**
Hari ke-28 dipilih sebagai kompromi antara cukup awal untuk intervensi dan cukup data untuk membaca pola perilaku mahasiswa. Jika terlalu awal, misalnya minggu ke-2, data aktivitas dan assessment mungkin masih terlalu sedikit. Jika terlalu akhir, misalnya minggu ke-8, prediksi menjadi kurang bernilai sebagai early warning karena waktu intervensinya semakin pendek.

## 38. Jika dosen bertanya: apakah dataset mengalami class imbalance?

**Jawaban:**
Distribusi kelas tidak terlalu ekstrem. Dataset hasil preprocessing memiliki 17.208 baris `AtRisk` dan 15.385 baris `Successful`. Namun kami tetap mengantisipasi perbedaan kelas dengan memakai `class_weight='balanced'` pada Logistic Regression dan Random Forest, serta `scale_pos_weight` pada XGBoost.

## 39. Jika dosen bertanya: kenapa Random Forest dipilih padahal XGBoost memiliki accuracy dan ROC-AUC lebih tinggi?

**Jawaban:**
Karena tujuan utama sistem adalah early warning, metrik yang diprioritaskan adalah recall `AtRisk`, bukan accuracy atau ROC-AUC saja. XGBoost memang memiliki accuracy dan ROC-AUC tertinggi, tetapi Random Forest menghasilkan recall `AtRisk` lebih tinggi. Artinya Random Forest lebih banyak menangkap mahasiswa yang benar-benar berisiko, sehingga lebih sesuai dengan tujuan intervensi dini.

## 40. Jika dosen bertanya: apakah model bisa menjelaskan alasan mahasiswa dianggap berisiko?

**Jawaban:**
Bisa, tetapi penjelasannya dibantu oleh dua lapisan. Model machine learning menghasilkan prediksi, probabilitas, dan feature importance untuk melihat fitur yang berkontribusi. Knowledge-based risk layer kemudian menerjemahkan sinyal perilaku menjadi alasan yang lebih operasional, misalnya skor assessment rendah, jumlah assessment rendah, total klik VLE rendah, atau hari aktif VLE rendah.

## 41. Jika dosen bertanya: apakah `id_student` digunakan sebagai fitur model?

**Jawaban:**
Tidak. `id_student` tidak digunakan sebagai prediktor. Kolom tersebut hanya digunakan sebagai grup saat data split dan cross-validation. Tujuannya agar mahasiswa yang sama tidak muncul di train dan test atau train dan validation sekaligus. Jika `id_student` dipakai sebagai fitur, model berisiko menghafal identitas mahasiswa, bukan mempelajari pola akademik dan aktivitas.

## 42. Jika dosen bertanya: risiko false positive dalam sistem ini apa?

**Jawaban:**
False positive berarti mahasiswa yang sebenarnya `Successful`, tetapi diprediksi atau ditandai sebagai `AtRisk`. Risikonya adalah tim akademik melakukan verifikasi pada mahasiswa yang sebenarnya tidak bermasalah. Karena itu output sistem tidak dipakai sebagai keputusan final, melainkan sebagai daftar prioritas untuk dicek lebih lanjut.

## 43. Jika dosen bertanya: risiko false negative dalam sistem ini apa?

**Jawaban:**
False negative berarti mahasiswa yang sebenarnya `AtRisk`, tetapi diprediksi sebagai `Successful`. Ini lebih kritis dalam early warning karena mahasiswa tersebut bisa tidak masuk daftar intervensi. Oleh karena itu penelitian ini memprioritaskan recall `AtRisk`, agar sebanyak mungkin mahasiswa berisiko dapat terdeteksi.

## 44. Jika dosen bertanya: mengapa threshold knowledge layer memakai kuartil bawah?

**Jawaban:**
Kuartil bawah dipakai karena memberi batas berbasis distribusi data, bukan angka asumsi manual. Mahasiswa yang berada pada kuartil bawah untuk indikator seperti aktivitas VLE atau assessment dianggap memiliki perilaku yang relatif rendah dibandingkan kelompok train. Threshold dihitung dari data train-validation agar tidak mengambil informasi dari hold-out test.

## 45. Jika dosen bertanya: apakah hasil model bisa langsung digeneralisasi ke kampus lain?

**Jawaban:**
Belum tentu. Dataset OULAD berasal dari konteks Open University di Inggris, sehingga pola aktivitas, struktur modul, sistem assessment, dan karakteristik mahasiswa bisa berbeda dengan kampus lain. Untuk penerapan di kampus lain, model perlu divalidasi ulang menggunakan data institusi tersebut.

## 46. Jika dosen bertanya: dashboard menampilkan semua mahasiswa atau hanya test set?

**Jawaban:**
Pada eksperimen ini dashboard dibuat dari hold-out test agar evaluasi tetap objektif dan tidak mencampur data yang dipakai untuk training. Dalam implementasi nyata, alur yang sama dapat diterapkan pada data mahasiswa aktif, lalu dashboard menampilkan daftar mahasiswa yang sedang berjalan untuk kebutuhan monitoring dan intervensi.

## 47. Jika dosen bertanya: apakah etis menandai mahasiswa sebagai berisiko?

**Jawaban:**
Etis jika digunakan sebagai alat bantu intervensi positif, bukan untuk menghukum atau memberi label permanen kepada mahasiswa. Output model harus diperlakukan sebagai sinyal awal yang diverifikasi oleh manusia. Selain itu, penerapan nyata perlu memperhatikan privasi data, transparansi penggunaan, dan evaluasi fairness agar tidak merugikan kelompok mahasiswa tertentu.
