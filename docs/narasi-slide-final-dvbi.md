# Narasi Presentasi — Analisis Risiko Dropout Mahasiswa
## Data Visualization and Business Intelligence

---

## Slide 1 — Judul

Assalamualaikum warahmatullahi wabarakatuh, selamat pagi/siang Bapak/Ibu dosen dan teman-teman semua.

Pada kesempatan ini kami dari Kelompok 5 akan mempresentasikan penelitian dengan judul "Analisis Risiko Dropout Mahasiswa Menggunakan Supervised Learning dan Knowledge-Based Risk Layer pada Open University Learning Analytics Dataset."

Presentasi ini disusun untuk mata kuliah Data Visualization and Business Intelligence. Anggota kelompok kami adalah Muhammad Rizky Hajar, Alwie Muflich, dan Heri Santosa, dari S2 PJJ Informatika, Konsentrasi Big Data dan Predictive Analytics, Universitas Amikom Yogyakarta.

---

## Slide 2 — Latar Belakang

Dropout mahasiswa merupakan permasalahan serius dalam pengelolaan pendidikan tinggi. Ketika mahasiswa gagal menyelesaikan studi, dampaknya meluas pada efektivitas layanan akademik dan evaluasi kinerja institusi secara keseluruhan.

Institusi umumnya baru menyadari masalah ini setelah kondisi mahasiswa sudah sulit ditangani. Jika identifikasi risiko dapat dilakukan lebih awal, intervensi akademik dapat diarahkan secara lebih tepat sasaran.

Saat ini, data yang tersedia cukup kaya: data akademik, data registrasi, dan jejak digital dari aktivitas pembelajaran. Data-data ini membuka peluang untuk analisis berbasis machine learning.

Dalam konteks Data Visualization dan Business Intelligence, hasil prediksi harus diterjemahkan menjadi indikator yang dapat ditindaklanjuti, mudah dipantau, dan mendukung pengambilan keputusan akademik melalui dashboard monitoring.

---

## Slide 3 — Rumusan Masalah & Tujuan

Dari latar belakang tersebut, kami merumuskan tiga pertanyaan penelitian.

Pertama, bagaimana membangun model klasifikasi risiko dropout mahasiswa menggunakan supervised learning. Kedua, bagaimana knowledge-based risk layer dapat memberikan interpretasi tambahan terhadap hasil prediksi. Dan ketiga, bagaimana keluaran model dapat dipetakan menjadi indikator pendukung keputusan dalam konteks Business Intelligence atau BI.

Tujuan penelitian ini ada tiga. Pertama, membangun model binary classification dengan tiga algoritma pembanding. Kedua, merancang knowledge-based risk layer berbasis aturan untuk menjelaskan faktor risiko. Dan ketiga, memetakan keluaran model menjadi indikator monitoring dan peringatan dini yang dapat menjadi bahan pertimbangan pihak akademik.

---

## Slide 4 — Dataset Penelitian

Dataset yang kami gunakan adalah Open University Learning Analytics Dataset, atau OULAD. Dataset ini dipilih karena menyediakan data akademik dan aktivitas pembelajaran digital yang relevan untuk analisis risiko mahasiswa.

OULAD terdiri dari empat tabel utama: studentInfo, studentRegistration, studentAssessment, dan studentVle. VLE adalah singkatan dari Virtual Learning Environment, yaitu platform pembelajaran daring tempat mahasiswa mengakses materi, forum, dan aktivitas akademik. Total data setelah preprocessing adalah 32.593 baris, di mana setiap baris merepresentasikan satu mahasiswa pada satu modul dan satu periode.

Dataset mencakup 7 modul dan 4 periode pembelajaran dari tahun 2013 sampai 2014. Distribusi labelnya cukup seimbang: 52,8 persen masuk kelas AtRisk, yaitu mahasiswa yang Withdrawn atau Fail, dan 47,2 persen masuk kelas Successful, yaitu mahasiswa yang Pass atau Distinction.

---

## Slide 5 — Tantangan Data

Sebelum masuk ke pemodelan, ada beberapa tantangan data yang perlu ditangani.

Pertama, data berasal dari empat tabel yang berbeda dan perlu digabungkan ke satu unit analisis. Kedua, tabel studentVle memiliki lebih dari 10 juta baris yang harus diagregasi per mahasiswa. Ketiga, ada missing value pada kolom indeks deprivasi yang kami isi dengan kategori Unknown. Keempat, sekitar 30,9 persen mahasiswa memiliki sinyal unregistration, yang menjadi indikator penting sekaligus tantangan tersendiri. Dan kelima, skala fitur sangat beragam, misalnya klik VLE bisa mencapai 24 ribu sedangkan assessment count hanya 0 sampai 14.

---

## Slide 6 — Preprocessing Data

Unit analisis yang kami gunakan adalah satu mahasiswa kali satu modul kali satu presentation.

Dari tabel studentInfo, kami mengambil fitur demografis seperti gender, region, highest education, age band, dan disability. Dari studentRegistration, kami membentuk fitur tanggal registrasi dan flag has_unregistration. Dari studentAssessment, kami agregasi menjadi assessment count, rata-rata skor, skor maksimum, dan skor minimum. Dan dari studentVle, kami agregasi menjadi total klik, jumlah hari aktif, jumlah site yang diakses, dan hari aktivitas terakhir.

Total fitur yang terbentuk adalah 21, terdiri dari 8 fitur kategorikal dan 13 fitur numerik. Label target dirumuskan sebagai binary: AtRisk untuk Withdrawn dan Fail, Successful untuk Pass dan Distinction.

---

## Slide 7 — Metode Penelitian

Metode utama yang kami gunakan adalah supervised binary classification dengan tiga algoritma. Logistic Regression sebagai model dasar yang mudah diinterpretasi. Random Forest untuk menangani hubungan non-linear dan fitur campuran. Dan XGBoost sebagai algoritma gradient boosting yang banyak digunakan pada data tabular.

Evaluasi menggunakan Accuracy, Precision, Recall, dan F1-score, dengan fokus pada Recall kelas AtRisk. Alasannya, dalam konteks peringatan dini, kami ingin meminimalkan jumlah mahasiswa berisiko yang terlewat oleh model.

Selain model machine learning, kami merancang knowledge-based risk layer berbasis aturan. Layer ini menggunakan indikator assessment score, assessment count, aktivitas VLE, dan sinyal unregistration untuk menghasilkan tingkat risiko High, Medium, atau Low, beserta alasan spesifik risiko masing-masing mahasiswa.

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

Hasilnya, Logistic Regression mencapai accuracy 93,65 persen dengan standar deviasi 0,29. Random Forest mencapai 94,19 persen plus minus 0,28. Dan XGBoost mencapai 94,41 persen plus minus 0,31. Standar deviasi yang rendah, di bawah 0,7 persen untuk semua metrik, mengindikasikan bahwa performa ketiga model relatif konsisten pada skema validasi ini.

Kedua, evaluasi pada test set yang terdiri dari 6.471 baris dan 5.757 mahasiswa yang tidak muncul pada data training. Pada test set ini, Random Forest memiliki recall tertinggi yaitu 90,32 persen, sehingga dipilih sebagai model utama untuk skenario peringatan dini. False negative rate pada kelas AtRisk sebesar 9,7 persen, artinya dari 3.398 mahasiswa AtRisk, terdapat 329 yang tidak teridentifikasi oleh model.

Untuk knowledge-based risk layer, dari 32.593 total data: 22.168 terklasifikasi Low Risk, 6.508 High Risk, dan 3.917 Medium Risk.

---

## Slide 10 — Analisis Hasil

Dari feature importance XGBoost, lima fitur paling berpengaruh adalah: assessment count dengan importance 0,37, hari aktivitas terakhir VLE 0,13, sinyal unregistration 0,08, tanggal unregistration 0,06, dan rata-rata skor assessment 0,05. Artinya, partisipasi dalam assessment dan aktivitas terakhir di VLE menjadi fitur yang paling dominan dalam model.

Dari sisi modul, CCC pada periode 2014B memiliki risiko tertinggi dengan 65 persen mahasiswa masuk kategori AtRisk, diikuti CCC 2014J sebesar 60,1 persen dan DDD 2014B sebesar 59,8 persen.

Temuan dari cross-tabulation antara knowledge layer dan prediksi model menunjukkan pola yang konsisten: untuk mahasiswa yang dikategorikan High Risk oleh rule layer, model memprediksi 100 persen dari mereka sebagai AtRisk. Untuk Medium Risk, agreement-nya 99,1 persen.

Selain itu, model memberi sinyal AtRisk pada 1.105 kasus di kelompok Low Risk. Ini menunjukkan bahwa pendekatan berbasis model dapat memberikan sinyal tambahan di luar aturan yang dirancang secara manual.

---

## Slide 11 — Implikasi Business Intelligence

Hasil prediksi kami petakan menjadi indikator pendukung keputusan.

Jumlah mahasiswa AtRisk per module dapat menjadi dasar prioritas monitoring prodi. Distribusi High, Medium, dan Low Risk dapat membantu pertimbangan alokasi sumber daya untuk tim counselling. Sinyal risiko seperti skor assessment rendah, aktivitas VLE rendah, atau unregistration memberikan alasan spesifik yang dapat ditinjau oleh dosen wali. Antrean intervensi menyediakan daftar prioritas mahasiswa yang berpotensi membutuhkan tindak lanjut, yang efektivitasnya perlu dievaluasi pada implementasi berikutnya.

Dari sisi pemangku kepentingan: pimpinan akademik mendapatkan ringkasan risiko per module, program studi dapat meninjau modul dengan tingkat risiko tinggi, dosen wali atau tutor mendapatkan daftar mahasiswa prioritas beserta alasan risiko, dan tim counselling mendapatkan sinyal awal untuk dipertimbangkan dalam tindak lanjut.

Dashboard monitoring akademik telah kami implementasi sebagai purwarupa yang menampilkan seluruh indikator tersebut.

---

## Slide 12 — Kesimpulan & Saran

Sebagai kesimpulan, pertama, ketiga model menunjukkan performa yang relatif konsisten melalui 5-fold cross-validation dengan standar deviasi di bawah 0,7 persen. XGBoost terbaik pada tahap cross-validation, sedangkan Random Forest terpilih berdasarkan recall tertinggi pada test set.

Kedua, seluruh split dikelompokkan berdasarkan identitas mahasiswa sehingga mahasiswa yang sama tidak muncul pada train dan test. Skema ini mengurangi risiko data leakage antar split.

Ketiga, knowledge-based risk layer menunjukkan konsistensi tinggi dengan prediksi model pada data yang dianalisis, dengan agreement 99 sampai 100 persen pada level High dan Medium Risk.

Dan keempat, kombinasi machine learning dan rule-based dapat menghasilkan label prediksi, alasan risiko, dan prioritas monitoring dalam satu keluaran terpadu.

Untuk saran pengembangan: pertama, validasi threshold knowledge layer dengan data semester baru. Kedua, tambahkan fitur temporal per minggu untuk mendukung prediksi yang lebih awal. Ketiga, integrasikan keluaran ke LMS institusi jika ingin dikembangkan sebagai dashboard operasional. Dan keempat, lakukan evaluasi efektivitas intervensi berdasarkan keluaran model.

Demikian presentasi dari kami. Kami berharap pendekatan ini dapat menjadi langkah awal untuk mendukung monitoring akademik yang lebih proaktif, sehingga institusi memiliki dasar analitik tambahan dalam mendampingi mahasiswa berisiko.

---

## Slide 13 — Dashboard

Ini adalah tampilan dashboard monitoring risiko akademik yang telah kami implementasi.

Di bagian atas terdapat lima KPI utama: jumlah mahasiswa yang dipantau, prediksi AtRisk beserta indikator tren dibanding periode sebelumnya, jumlah High Risk, Medium Risk, dan unregistration rate.

Baris kedua menampilkan segmentasi risiko mahasiswa dengan panduan tindakan untuk setiap level, serta ringkasan keputusan yang membantu pengelola meninjau langkah prioritas.

Baris ketiga berisi tiga panel: prioritas tindakan, ko-occurensi sinyal risiko yang menunjukkan berapa mahasiswa memiliki satu, dua, hingga lima sinyal aktif bersamaan, dan perbandingan risiko antar module yang disertai jumlah volume mahasiswa.

Di bawahnya terdapat panel tren risiko per periode yang menunjukkan pergerakan AtRisk rate dari 2013B hingga 2014J beserta referensi benchmark, serta panel profil mahasiswa berhasil yang menampilkan rata-rata aktivitas VLE dan skor assessment sebagai gambaran pola engagement.

Bagian terakhir berisi dua tabel: area akademik prioritas yang menampilkan breakdown per module-presentation, dan daftar prioritas intervensi yang mencakup ID mahasiswa, level risiko, skor prioritas, hari terakhir aktif di VLE, alasan utama, dan rekomendasi tindakan.

Filter module di toolbar memungkinkan pemangku kepentingan melihat data spesifik per module, dan seluruh panel akan berubah sesuai filter yang dipilih.

---

## Slide 14 — Referensi

Ini adalah daftar referensi utama yang kami gunakan dalam penelitian ini, terdiri dari 10 paper dan dataset OULAD. Seluruh referensi disusun menggunakan format IEEE.

Demikian Paparana Kami dari Kelompok 5, Terima kasih atas perhatiannya. Wassalamualaikum warahmatullahi wabarakatuh.
