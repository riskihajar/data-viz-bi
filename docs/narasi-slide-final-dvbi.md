# Narasi Presentasi — Analisis Risiko Dropout Mahasiswa
## Data Visualization and Business Intelligence

---

## Slide 1 — Judul

Assalamualaikum warahmatullahi wabarakatuh, selamat pagi/siang Bapak/Ibu dosen dan teman-teman semua.

Pada kesempatan ini kami dari Kelompok 5 akan mempresentasikan penelitian dengan judul "Analisis Risiko Dropout Mahasiswa Menggunakan Supervised Learning dan Knowledge-Based Risk Layer pada Open University Learning Analytics Dataset."

Presentasi ini disusun untuk mata kuliah Data Visualization and Business Intelligence. Anggota kelompok kami adalah Muhammad Rizky Hajar, Alwie Muflich, dan Heri Santosa, dari S2 PJJ Informatika, Konsentrasi Big Data dan Predictive Analytics, Universitas Amikom Yogyakarta.

---

## Slide 2 — Latar Belakang

Dropout mahasiswa merupakan permasalahan serius dalam pengelolaan pendidikan tinggi. Ketika mahasiswa gagal menyelesaikan studi, dampaknya tidak hanya pada mahasiswa itu sendiri, tetapi juga pada efektivitas layanan akademik dan evaluasi kinerja institusi secara keseluruhan.

Permasalahannya, institusi biasanya baru menyadari masalah ini setelah kondisi mahasiswa sudah terlambat untuk ditangani. Padahal, jika identifikasi risiko bisa dilakukan lebih awal, intervensi akademik dapat diarahkan secara lebih tepat sasaran.

Saat ini, data yang tersedia cukup kaya: data akademik, data registrasi, dan digital traces dari aktivitas pembelajaran. Data-data ini membuka peluang untuk analisis berbasis machine learning.

Namun dalam konteks Data Visualization dan Business Intelligence, tantangannya bukan hanya membangun model prediksi. Hasil prediksi harus diterjemahkan menjadi indikator yang actionable, mudah dipantau, dan dapat mendukung pengambilan keputusan akademik melalui dashboard monitoring.

---

## Slide 3 — Rumusan Masalah & Tujuan

Dari latar belakang tersebut, kami merumuskan tiga pertanyaan penelitian.

Pertama, bagaimana membangun model klasifikasi risiko dropout mahasiswa menggunakan supervised learning. Kedua, bagaimana knowledge-based risk layer dapat memberikan interpretasi tambahan terhadap hasil prediksi. Dan ketiga, bagaimana keluaran model dapat dipetakan menjadi indikator decision support dalam konteks BI.

Tujuan penelitian ini ada tiga. Pertama, membangun model binary classification dengan tiga algoritma pembanding. Kedua, merancang knowledge-based risk layer berbasis aturan untuk menjelaskan faktor risiko. Dan ketiga, memetakan keluaran model menjadi indikator monitoring early warning yang bisa digunakan oleh pihak akademik.

---

## Slide 4 — Dataset Penelitian

Dataset yang kami gunakan adalah Open University Learning Analytics Dataset, atau OULAD. Dataset ini dipilih karena menyediakan data akademik dan aktivitas pembelajaran digital yang relevan untuk analisis risiko mahasiswa.

OULAD terdiri dari empat tabel utama: studentInfo, studentRegistration, studentAssessment, dan studentVle. Total data setelah preprocessing adalah 32.593 baris, di mana setiap baris merepresentasikan satu mahasiswa pada satu modul dan satu periode.

Dataset mencakup 7 modul dan 4 periode pembelajaran dari tahun 2013 sampai 2014. Distribusi labelnya cukup seimbang: 52,8 persen masuk kelas AtRisk, yaitu mahasiswa yang Withdrawn atau Fail, dan 47,2 persen masuk kelas Successful, yaitu mahasiswa yang Pass atau Distinction.

---

## Slide 5 — Tantangan Data

Sebelum masuk ke pemodelan, ada beberapa tantangan data yang perlu ditangani.

Pertama, data berasal dari empat tabel yang berbeda dan perlu digabungkan ke satu unit analisis. Kedua, tabel studentVle memiliki lebih dari 10 juta baris yang harus diagregasi per mahasiswa. Ketiga, ada missing value pada kolom imd_band yang kami isi dengan kategori Unknown. Keempat, sekitar 30,9 persen mahasiswa memiliki sinyal unregistration, yang menjadi indikator penting tapi juga tantangan tersendiri. Dan kelima, skala fitur sangat beragam, misalnya klik VLE bisa mencapai 24 ribu sedangkan assessment count hanya 0 sampai 14.

---

## Slide 6 — Preprocessing Data

Unit analisis yang kami gunakan adalah satu mahasiswa kali satu modul kali satu presentation.

Dari tabel studentInfo, kami mengambil fitur demografis seperti gender, region, highest education, age band, dan disability. Dari studentRegistration, kami membentuk fitur tanggal registrasi dan flag has_unregistration. Dari studentAssessment, kami agregasi menjadi assessment count, rata-rata skor, skor maksimum, dan skor minimum. Dan dari studentVle, kami agregasi menjadi total klik, jumlah hari aktif, jumlah site yang diakses, dan hari aktivitas terakhir.

Total fitur yang terbentuk adalah 21, terdiri dari 8 fitur kategorikal dan 13 fitur numerik. Label target dirumuskan sebagai binary: AtRisk untuk Withdrawn dan Fail, Successful untuk Pass dan Distinction.

---

## Slide 7 — Metode Penelitian

Metode utama yang kami gunakan adalah supervised binary classification dengan tiga algoritma. Logistic Regression sebagai baseline yang mudah diinterpretasi. Random Forest untuk menangani hubungan non-linear dan fitur campuran. Dan XGBoost sebagai state-of-the-art untuk data tabular.

Evaluasi menggunakan Accuracy, Precision, Recall, dan F1-score, dengan fokus pada Recall kelas AtRisk. Alasannya, dalam konteks early warning, kita ingin meminimalkan jumlah mahasiswa berisiko yang terlewat oleh model.

Selain model machine learning, kami merancang knowledge-based risk layer berbasis aturan. Layer ini menggunakan indikator assessment score, assessment count, aktivitas VLE, dan sinyal unregistration untuk menghasilkan tingkat risiko High, Medium, atau Low, beserta alasan spesifik risiko masing-masing mahasiswa.

Untuk data split, kami menggunakan 80 persen data sebagai train plus validation dan 20 persen sebagai hold-out test. Seluruh split dilakukan berdasarkan id_student menggunakan GroupShuffleSplit, sehingga tidak ada mahasiswa yang sama muncul di train dan test. Ini penting untuk mencegah group leakage.

Validasi dilakukan melalui 5-fold GroupKFold cross-validation pada train set. Dengan skema ini, setiap data pernah menjadi validation tepat satu kali, dan kami mendapatkan mean serta standar deviasi yang membuktikan stabilitas performa model.

Untuk penanganan imbalance, Logistic Regression dan Random Forest menggunakan class_weight balanced, sedangkan XGBoost menggunakan scale_pos_weight yang dihitung dari rasio kelas pada data training.

---

## Slide 8 — Tinjauan Pustaka

Kami menganalisis 10 paper relevan dari tahun 2020 sampai 2025 yang membahas prediksi dropout dan performa akademik mahasiswa.

Metode yang dominan digunakan adalah Random Forest, XGBoost, clustering, deep learning, dan AutoML. Variabel yang umum mencakup performa akademik, demografi, engagement LMS, dan digital traces.

Dari review tersebut, kami menemukan gap utama. Pertama, sebagian besar paper berhenti di level prediksi dan metrik model. Kedua, visual analytics untuk pengambil keputusan belum dibahas secara operasional. Dan ketiga, kaitan antara model prediksi, monitoring berkala, dan action plan intervensi masih lemah.

Kontribusi penelitian ini adalah menjembatani gap tersebut: menggabungkan prediksi machine learning dengan rule-based risk layer, lalu memetakan hasilnya ke indikator BI yang bisa digunakan oleh stakeholder akademik.

---

## Slide 9 — Hasil Evaluasi Model

Pertama, hasil cross-validation 5-fold GroupKFold. Setiap fold menggunakan sekitar 20.900 baris sebagai training dan 5.200 baris sebagai validation, dengan jaminan tidak ada mahasiswa yang sama di train dan validation pada fold yang sama.

Hasilnya, Logistic Regression mencapai accuracy 93,65 persen dengan standar deviasi 0,29. Random Forest mencapai 94,19 persen plus minus 0,28. Dan XGBoost mencapai 94,41 persen plus minus 0,31. Standar deviasi yang rendah, di bawah 0,7 persen untuk semua metrik, menunjukkan bahwa performa ketiga model stabil dan bukan kebetulan dari satu kali split.

Kedua, evaluasi pada hold-out test set yang terdiri dari 6.471 baris dan 5.757 mahasiswa yang tidak pernah dilihat model selama training. Pada test set ini, Random Forest memiliki recall tertinggi yaitu 90,32 persen, sehingga dipilih sebagai model utama untuk kebutuhan early warning. Miss rate-nya hanya 9,7 persen, artinya dari 3.398 mahasiswa AtRisk, hanya 329 yang tidak terdeteksi.

Untuk knowledge-based risk layer, dari 32.593 total data: 22.168 terklasifikasi Low Risk, 6.508 High Risk, dan 3.917 Medium Risk.

---

## Slide 10 — Analisis Hasil

Dari feature importance XGBoost, lima fitur paling berpengaruh adalah: assessment_count dengan importance 0,37, vle_last_activity_day 0,13, has_unregistration 0,08, date_unregistration 0,06, dan assessment_score_mean 0,05. Artinya, partisipasi dalam assessment dan aktivitas terakhir di VLE menjadi prediktor terkuat apakah mahasiswa berisiko atau tidak.

Dari sisi modul, CCC pada periode 2014B memiliki risiko tertinggi dengan 65 persen mahasiswa masuk kategori AtRisk, diikuti CCC 2014J sebesar 60,1 persen dan DDD 2014B sebesar 59,8 persen.

Yang menarik adalah cross-tabulation antara knowledge layer dan prediksi model. Untuk mahasiswa yang dikategorikan High Risk oleh rule layer, model memprediksi 100 persen dari mereka sebagai AtRisk. Untuk Medium Risk, agreement-nya 99,1 persen. Ini menunjukkan bahwa kedua pendekatan saling menguatkan.

Namun model juga menangkap 1.105 kasus yang oleh rule layer dikategorikan Low Risk tetapi diprediksi AtRisk. Ini menunjukkan bahwa model machine learning mampu mendeteksi pola risiko yang tidak tertangkap oleh aturan threshold sederhana.

---

## Slide 11 — Implikasi Business Intelligence

Hasil prediksi tidak berhenti sebagai angka metrik. Kami memetakannya menjadi indikator decision support.

Jumlah mahasiswa AtRisk per module menjadi dasar prioritas monitoring prodi. Distribusi High, Medium, dan Low Risk membantu alokasi resource untuk tim counselling. Sinyal risiko seperti skor assessment rendah, aktivitas VLE rendah, atau unregistration memberikan alasan spesifik yang bisa langsung dibaca oleh dosen wali. Dan intervention queue menyediakan daftar mahasiswa yang perlu ditindaklanjuti berdasarkan urutan prioritas.

Dari sisi stakeholder, pimpinan akademik mendapatkan overview risiko per module. Program studi dapat mengidentifikasi modul yang bermasalah. Dosen wali atau tutor mendapatkan daftar mahasiswa prioritas beserta alasan risiko masing-masing. Dan tim counselling mendapatkan sinyal early warning untuk ditindaklanjuti.

Dashboard monitoring akademik telah kami implementasi sebagai prototype yang menampilkan seluruh indikator tersebut.

---

## Slide 12 — Kesimpulan & Saran

Sebagai kesimpulan, pertama, ketiga model menunjukkan performa yang stabil melalui 5-fold cross-validation dengan standar deviasi di bawah 0,7 persen. XGBoost terbaik pada tahap CV, sedangkan Random Forest terpilih berdasarkan recall tertinggi pada hold-out test.

Kedua, seluruh split dilakukan berdasarkan id_student sehingga tidak ada data leakage. Evaluasi yang kami lakukan valid secara metodologis.

Ketiga, knowledge-based risk layer menunjukkan konsistensi tinggi dengan prediksi model, dengan agreement 99 sampai 100 persen pada level High dan Medium Risk.

Dan keempat, kombinasi machine learning dan rule-based menghasilkan output yang bukan hanya label prediksi, tetapi juga alasan risiko dan prioritas monitoring yang bisa langsung digunakan stakeholder.

Untuk saran pengembangan, pertama, validasi threshold knowledge layer dengan data semester baru. Kedua, tambahkan temporal features per minggu untuk mendukung early prediction yang lebih awal. Ketiga, integrasikan output ke LMS institusi sebagai dashboard real-time. Dan keempat, lakukan evaluasi efektivitas intervensi berdasarkan output model.

Demikian presentasi dari kami. Terima kasih atas perhatiannya. Wassalamualaikum warahmatullahi wabarakatuh.

---

## Slide 13 — Dashboard

Ini adalah tampilan dashboard monitoring risiko akademik yang telah kami implementasi. Di bagian atas terdapat overview jumlah mahasiswa yang dipantau, prediksi AtRisk, dan distribusi level risiko.

Di tengah ada segmentasi risiko beserta ringkasan keputusan dan prioritas tindakan. Di bawahnya terdapat breakdown per module-presentation dan daftar prioritas intervensi yang menampilkan ID mahasiswa, level risiko, skor prioritas, alasan utama, dan rekomendasi tindakan.

Filter module di atas memungkinkan stakeholder untuk melihat data spesifik per module, dan seluruh panel akan terupdate sesuai filter yang dipilih.

---

## Slide 14 — Referensi

Ini adalah daftar referensi utama yang kami gunakan dalam penelitian ini, terdiri dari 10 paper dan dataset OULAD. Seluruh referensi menggunakan format IEEE dan tersedia dalam arsip PDF yang telah divalidasi.
