# Narasi Presentasi — Early Warning Risiko Ketidakberhasilan Mahasiswa dalam Mata Kuliah
## Data Visualization and Business Intelligence

---

## Slide 1 — Judul

Assalamualaikum warahmatullahi wabarakatuh, selamat pagi/siang Bapak/Ibu dosen dan teman-teman semua.

Pada kesempatan ini kami dari Kelompok 5 akan mempresentasikan penelitian dengan judul "Early Warning Risiko Ketidakberhasilan Mahasiswa dalam Mata Kuliah pada Minggu Keempat Menggunakan Supervised Learning dan Knowledge-Based Risk Layer pada Open University Learning Analytics Dataset."

Presentasi ini disusun untuk mata kuliah Data Visualization and Business Intelligence. Anggota kelompok kami adalah Muhammad Rizky Hajar, Alwie Muflich, dan Heri Santosa, dari S2 PJJ Informatika, Konsentrasi Big Data dan Predictive Analytics, Universitas Amikom Yogyakarta.

---

## Slide 2 — Latar Belakang

Kegagalan dan pengunduran diri dari mata kuliah memerlukan perhatian dalam monitoring akademik. Kondisi tersebut berkaitan dengan capaian pembelajaran, efektivitas layanan akademik, dan evaluasi penyelenggaraan mata kuliah.

Institusi umumnya baru menyadari masalah ini setelah kondisi mahasiswa sudah sulit ditangani. Jika identifikasi risiko dapat dilakukan lebih awal, intervensi akademik dapat diarahkan secara lebih tepat sasaran.

Saat ini, data yang tersedia cukup kaya: data akademik, data registrasi, dan jejak digital dari aktivitas pembelajaran. Data-data ini membuka peluang untuk analisis berbasis machine learning.

Dalam konteks Data Visualization dan Business Intelligence, hasil prediksi harus diterjemahkan menjadi indikator yang dapat ditindaklanjuti, mudah dipantau, dan mendukung pengambilan keputusan akademik melalui dashboard monitoring.

---

## Slide 3 — Rumusan Masalah & Tujuan

Dari latar belakang tersebut, kami merumuskan tiga pertanyaan penelitian.

Pertama, bagaimana membangun model klasifikasi risiko ketidakberhasilan mahasiswa dalam mata kuliah menggunakan supervised learning. Kedua, bagaimana knowledge-based risk layer dapat memberikan interpretasi tambahan terhadap hasil prediksi. Dan ketiga, bagaimana keluaran model dapat dipetakan menjadi indikator pendukung keputusan dalam konteks Business Intelligence atau BI.

Tujuan penelitian ini ada tiga. Pertama, membangun model binary classification dengan tiga algoritma pembanding. Kedua, merancang knowledge-based risk layer berbasis aturan untuk menjelaskan faktor risiko. Dan ketiga, memetakan keluaran model menjadi indikator monitoring dan peringatan dini yang dapat menjadi bahan pertimbangan pihak akademik.

---

## Slide 4 — Dataset Penelitian

Dataset yang kami gunakan adalah Open University Learning Analytics Dataset, atau OULAD. Dataset ini dipilih karena menyediakan data akademik dan aktivitas pembelajaran digital yang relevan untuk analisis risiko mahasiswa.

OULAD terdiri dari empat tabel utama: studentInfo, studentRegistration, studentAssessment, dan studentVle. VLE adalah singkatan dari Virtual Learning Environment, yaitu platform pembelajaran daring tempat mahasiswa mengakses materi, forum, dan aktivitas akademik. Total data setelah preprocessing adalah 32.593 baris, di mana setiap baris merepresentasikan satu mahasiswa pada satu modul dan satu periode.

Dataset mencakup 7 modul dan 4 periode pembelajaran dari tahun 2013 sampai 2014. Distribusi labelnya cukup seimbang: 52,8 persen masuk kelas AtRisk, yaitu hasil mata kuliah Withdrawn atau Fail, dan 47,2 persen masuk kelas Successful, yaitu Pass atau Distinction. Final result tersebut berlaku pada satu mahasiswa dalam satu module-presentation.

---

## Slide 5 — Tantangan Data

Sebelum masuk ke pemodelan, ada beberapa tantangan data yang perlu ditangani.

Pertama, data berasal dari empat tabel yang berbeda dan perlu digabungkan ke satu unit analisis. Kedua, tabel studentVle memiliki lebih dari 10 juta baris yang harus diagregasi per mahasiswa. Ketiga, ada missing value pada kolom indeks deprivasi yang perlu ditangani di dalam pipeline. Keempat, penelitian ini membatasi fitur sampai hari ke-28, sehingga informasi masa depan seperti unregistration dan aktivitas setelah cut-off harus dikeluarkan. Dan kelima, skala fitur sangat beragam, sehingga pipeline perlu menangani fitur numerik dan kategorikal secara konsisten.

---

## Slide 6 — Preprocessing Data

Unit analisis yang kami gunakan adalah satu mahasiswa kali satu modul kali satu presentation.

Dari tabel studentInfo, kami mengambil fitur demografis seperti gender, region, highest education, age band, dan disability. Dari studentRegistration, kami menggunakan tanggal registrasi awal. Dari studentAssessment, kami agregasi menjadi assessment count, rata-rata skor, skor maksimum, dan skor minimum sampai hari ke-28. Dan dari studentVle, kami agregasi menjadi total klik, jumlah hari aktif, jumlah site yang diakses, dan hari aktivitas terakhir sampai hari ke-28.

Fitur masa depan seperti date unregistration, flag has unregistration, hasil akhir, dan aktivitas setelah hari ke-28 tidak digunakan sebagai prediktor. Label target dirumuskan sebagai binary: AtRisk untuk Withdrawn dan Fail, Successful untuk Pass dan Distinction.

---

## Slide 7 — Metode Penelitian

Metode utama yang kami gunakan adalah supervised binary classification dengan tiga algoritma. Logistic Regression sebagai model dasar yang mudah diinterpretasi. Random Forest untuk menangani hubungan non-linear dan fitur campuran. Dan XGBoost sebagai algoritma gradient boosting yang banyak digunakan pada data tabular.

Evaluasi menggunakan Accuracy, Precision, Recall, dan F1-score, dengan fokus pada Recall kelas AtRisk. Alasannya, dalam konteks peringatan dini, kami ingin meminimalkan jumlah mahasiswa berisiko yang terlewat oleh model.

Selain model machine learning, kami merancang knowledge-based risk layer berbasis aturan. Layer ini menggunakan indikator assessment score, assessment count, total klik VLE, dan jumlah hari aktif VLE untuk menghasilkan tingkat risiko High, Medium, atau Low, beserta alasan spesifik risiko masing-masing mahasiswa.

Untuk data split, kami menggunakan 80 persen data sebagai train plus validation dan 20 persen sebagai test. Seluruh split dikelompokkan berdasarkan mahasiswa, sehingga tidak ada mahasiswa yang sama muncul di train dan test.

Validasi dilakukan melalui 5-fold cross-validation pada train set. Dengan skema ini, setiap data pernah menjadi validation tepat satu kali, dan kami mendapatkan mean serta standar deviasi yang menunjukkan stabilitas performa model.

Untuk penanganan imbalance, ketiga algoritma menggunakan pembobotan kelas proporsional agar model tidak bias terhadap kelas mayoritas.

---

## Slide 8 — Tinjauan Pustaka

Kami menganalisis 10 paper relevan dari tahun 2020 sampai 2025 yang membahas prediksi dropout dan performa akademik mahasiswa.

Metode yang dominan digunakan adalah Random Forest, XGBoost, clustering, deep learning, dan AutoML. Variabel yang umum mencakup performa akademik, demografi, engagement Learning Management System (LMS), dan jejak digital.

Dari review tersebut, kami melihat beberapa ruang pengembangan. Pertama, banyak penelitian masih berfokus pada prediksi dan metrik model. Kedua, visual analytics untuk pengambil keputusan belum selalu dibahas secara operasional. Dan ketiga, kaitan antara model prediksi, monitoring berkala, dan rencana intervensi masih dapat dikembangkan lebih lanjut.

Fokus penelitian ini adalah menghubungkan prediksi machine learning dengan rule-based risk layer, lalu memetakan hasilnya ke indikator BI yang relevan bagi pemangku kepentingan akademik.

---

## Slide 9 — Hasil Evaluasi Model

Pertama, hasil cross-validation 5-fold yang dikelompokkan per mahasiswa. Setiap fold menggunakan sekitar 20.900 baris sebagai training dan 5.200 baris sebagai validation, dengan pengaturan agar mahasiswa yang sama tidak muncul di train dan validation pada fold yang sama.

Hasil cross-validation menunjukkan bahwa XGBoost memiliki accuracy dan ROC-AUC tertinggi, yaitu accuracy 75,84 persen dan ROC-AUC 84,40 persen. Random Forest memiliki recall AtRisk tertinggi, yaitu 71,07 persen, sehingga dipilih sesuai tujuan early warning yang memprioritaskan cakupan mahasiswa berisiko.

Kedua, evaluasi dilakukan pada hold-out test yang terdiri dari 6.471 baris, dengan 3.398 kasus AtRisk dan 3.073 kasus Successful. Random Forest yang telah dipilih melalui cross-validation menghasilkan recall AtRisk 72,13 persen. Dari 3.398 kasus AtRisk, model berhasil mengenali 2.451 kasus dan melewatkan 947 kasus.

Untuk knowledge-based risk layer pada hold-out test, terdapat 1.816 High Risk, 1.979 Medium Risk, dan 2.676 Low Risk.

---

## Slide 10 — Analisis Hasil

Feature importance Random Forest menunjukkan bahwa sinyal perilaku awal menjadi pembeda utama. Total klik VLE, hari aktivitas terakhir, jumlah hari aktif, dan jumlah site yang diakses muncul sebagai fitur teratas. Fitur assessment dan registrasi juga berkontribusi, tetapi hasil ini tetap dibaca sebagai kontribusi prediktif, bukan hubungan sebab akibat.

Pada knowledge layer, threshold kuartil bawah train-validation adalah skor assessment 0, jumlah assessment 0, total klik VLE 47, dan hari aktif VLE 4. Nilai ini membantu mengubah prediksi model menjadi alasan risiko yang bisa dibaca lebih operasional.

Ketika High Risk dan Medium Risk dipetakan sebagai AtRisk, recall berubah dari 72,13 persen menjadi 78,66 persen. Angka tersebut menunjukkan cakupan kasus AtRisk yang masuk ke dalam alarm intervensi.

Precision berubah dari 80,07 persen menjadi 70,43 persen. Perubahan recall dan precision dibaca bersama kapasitas tim akademik dalam melakukan verifikasi.

---

## Slide 11 — Implikasi Business Intelligence

Hasil prediksi kami petakan menjadi indikator pendukung keputusan.

Jumlah mahasiswa AtRisk per module dapat menjadi dasar prioritas monitoring prodi. Distribusi High, Medium, dan Low Risk dapat membantu pertimbangan alokasi sumber daya untuk tim counselling. Sinyal risiko seperti skor assessment rendah, assessment belum dikerjakan, klik VLE rendah, atau hari aktif rendah memberikan alasan spesifik yang dapat ditinjau oleh dosen wali. Antrean intervensi menyediakan daftar prioritas mahasiswa yang berpotensi membutuhkan tindak lanjut, yang efektivitasnya perlu dievaluasi pada implementasi berikutnya.

Dari sisi pemangku kepentingan: pimpinan akademik mendapatkan ringkasan risiko per module, program studi dapat meninjau modul dengan tingkat risiko tinggi, dosen wali atau tutor mendapatkan daftar mahasiswa prioritas beserta alasan risiko, dan tim counselling mendapatkan sinyal awal untuk dipertimbangkan dalam tindak lanjut.

Dashboard monitoring akademik telah kami implementasi sebagai purwarupa yang menampilkan seluruh indikator tersebut.

---

## Slide 12 — Kesimpulan & Saran

Sebagai kesimpulan, pertama, ketiga model menunjukkan performa yang relatif konsisten melalui 5-fold cross-validation. XGBoost unggul pada accuracy dan ROC-AUC, sedangkan Random Forest terpilih berdasarkan recall AtRisk tertinggi.

Kedua, seluruh split dikelompokkan berdasarkan identitas mahasiswa sehingga mahasiswa yang sama tidak muncul pada train dan test. Skema ini mengurangi risiko data leakage antar split.

Ketiga, knowledge-based risk layer meningkatkan recall dari 72,13 persen menjadi 78,66 persen, disertai perubahan precision dan jumlah kasus dalam antrean verifikasi.

Dan keempat, kombinasi machine learning dan rule-based dapat menghasilkan label prediksi, alasan risiko, dan prioritas monitoring dalam satu keluaran terpadu.

Untuk saran pengembangan: pertama, validasi threshold knowledge layer dengan data semester baru. Kedua, tambahkan fitur temporal harian atau mingguan untuk membaca dinamika engagement. Ketiga, integrasikan keluaran ke LMS institusi jika ingin dikembangkan sebagai dashboard operasional. Dan keempat, lakukan evaluasi efektivitas intervensi berdasarkan keluaran model.

Demikian presentasi dari kami. Kami berharap pendekatan ini dapat menjadi langkah awal untuk mendukung monitoring akademik yang lebih proaktif, sehingga institusi memiliki dasar analitik tambahan dalam mendampingi mahasiswa berisiko.

---

## Slide 13 — Dashboard

Ini adalah tampilan dashboard monitoring risiko akademik yang telah kami implementasi.

Di bagian atas terdapat KPI utama seperti jumlah mahasiswa yang dipantau, jumlah prioritas intervensi, distribusi level risiko, dan ringkasan performa sistem.

Baris kedua menampilkan segmentasi risiko mahasiswa dengan panduan tindakan untuk setiap level, serta ringkasan keputusan yang membantu pengelola meninjau langkah prioritas.

Baris ketiga berisi tiga panel: prioritas tindakan, ko-occurensi sinyal risiko yang menunjukkan berapa mahasiswa memiliki satu, dua, hingga lima sinyal aktif bersamaan, dan perbandingan risiko antar module yang disertai jumlah volume mahasiswa.

Di bawahnya terdapat panel tren risiko per periode yang menunjukkan pergerakan AtRisk rate dari 2013B hingga 2014J beserta referensi benchmark, serta panel profil mahasiswa berhasil yang menampilkan rata-rata aktivitas VLE dan skor assessment sebagai gambaran pola engagement.

Bagian terakhir berisi dua tabel: area akademik prioritas yang menampilkan breakdown per module-presentation, dan daftar prioritas intervensi yang mencakup ID mahasiswa, level risiko, skor prioritas, hari terakhir aktif di VLE, alasan utama, dan rekomendasi tindakan.

Filter module di toolbar memungkinkan pemangku kepentingan melihat data spesifik per module, dan seluruh panel akan berubah sesuai filter yang dipilih.

---

## Slide 14 — Referensi

Ini adalah daftar referensi utama yang kami gunakan dalam penelitian ini, terdiri dari 10 paper dan dataset OULAD. Seluruh referensi disusun menggunakan format IEEE.

Demikian Paparana Kami dari Kelompok 5, Terima kasih atas perhatiannya. Wassalamualaikum warahmatullahi wabarakatuh.
