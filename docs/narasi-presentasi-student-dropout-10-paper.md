# Narasi Presentasi — Student Performance / Dropout Analytics
## Literature Review 10 Paper

---

## Slide 1 — Judul Presentasi

Assalamualaikum warahmatullahi wabarakatuh, selamat pagi/siang/sore Bapak/Ibu dan teman-teman semua.

Pada kesempatan ini kami dari Kelompok 5 akan mempresentasikan hasil literature review dengan judul **Student Performance / Dropout Analytics**.

Presentasi ini disusun untuk mata kuliah **Data Visualization and Business Intelligence**.
Anggota kelompok kami adalah **Muhammad Rizky Hajar**, **Alwie Muflich**, dan **Heri Santosa**, dari **S2 PJJ Informatika Konsentrasi Big Data dan Predictive Analytics, Universitas Amikom Yogyakarta**.

Pada review ini, kami menganalisis **10 paper** yang relevan untuk memahami bagaimana penelitian-penelitian terbaru membahas prediksi performa mahasiswa, risiko dropout, serta peluang pengembangannya ke arah dashboard dan decision support.

---

## Slide 2 — Latar Belakang

Latar belakang topik ini berangkat dari fakta bahwa **dropout mahasiswa** merupakan isu penting dalam evaluasi kualitas pendidikan tinggi.
Ketika mahasiswa gagal dipantau sejak awal, institusi biasanya baru menyadari masalah setelah kondisinya sudah cukup terlambat untuk ditangani secara efektif.

Karena itu, perguruan tinggi membutuhkan **identifikasi dini mahasiswa berisiko** agar intervensi akademik bisa dilakukan lebih cepat dan lebih tepat sasaran.
Saat ini, peluang tersebut semakin terbuka karena tersedia banyak sumber data, mulai dari **data akademik**, **data sosiodemografis**, hingga **digital traces** seperti aktivitas di LMS.

Dalam konteks **DVBI**, tantangannya bukan hanya membangun model prediksi, tetapi juga bagaimana hasil prediksi tersebut diterjemahkan menjadi **insight yang mudah dipantau**, mudah dipahami, dan dapat membantu pengambil keputusan akademik melalui visualisasi dan dashboard.

---

## Slide 3 — Tujuan Literature Review

Tujuan dari literature review ini ada empat.

Pertama, kami ingin **mengidentifikasi bagaimana paper-paper yang dipilih membahas student performance dan student dropout**.
Kedua, kami ingin **membandingkan variabel, metode, temuan, dan keterbatasan** dari 10 paper tersebut.
Ketiga, kami ingin **menemukan research gap** yang relevan dengan bidang **Data Visualization and Business Intelligence**.
Dan keempat, kami ingin **menyusun dasar konseptual** untuk pengembangan **dashboard early warning mahasiswa**.

Jadi, review ini tidak hanya berhenti pada ringkasan isi paper, tetapi diarahkan untuk mendukung kebutuhan analisis dan visualisasi dalam konteks BI.

---

## Slide 4 — Metodologi Review

Metodologi review kami disusun berdasarkan **10 paper** yang relevan dengan topik **student performance** dan **student dropout**.
Agar tetap aktual, fokus seleksi diarahkan pada paper dengan rentang tahun **2020 sampai 2025**.

Setiap paper kemudian dibandingkan berdasarkan beberapa aspek utama, yaitu **tujuan studi**, **variabel yang digunakan**, **metode analisis atau model yang dipakai**, **temuan utama**, serta **keterbatasan penelitian**.

Dengan pendekatan ini, kami ingin melihat pola umum dari literatur yang ada, sekaligus menemukan area yang masih terbuka untuk dikembangkan, khususnya pada sisi **visual analytics**, **monitoring**, dan **dashboard BI**.

---

## Slide 5 — Dataset Review

Dari sisi dataset review, total terdapat **10 paper** yang kami analisis.
Rentang publikasinya berada pada periode **2020 hingga 2025**, sehingga cukup merepresentasikan arah penelitian terkini.

Topik utama yang muncul di dalam paper-paper tersebut mencakup **dropout prediction**, **academic performance**, **early warning system**, dan **educational analytics**.
Sumber publikasinya juga cukup beragam, berasal dari publisher seperti **Springer, MDPI, Wiley, IEEE**, dan beberapa sumber ilmiah lainnya.

Selain itu, seluruh PDF referensi untuk 10 paper ini sudah tersedia dan tervalidasi, sehingga proses review dilakukan berdasarkan dokumen yang lengkap dan konsisten.

---

## Slide 6 — Variabel yang Paling Sering Muncul

Berdasarkan hasil review, ada beberapa variabel yang paling sering muncul dalam penelitian-penelitian ini.

Yang pertama adalah **performa akademik awal**, misalnya nilai awal, IP, atau hasil evaluasi semester awal.
Kedua adalah **data sosiodemografis**, seperti usia, gender, status sosial, atau latar belakang ekonomi tertentu.
Ketiga adalah **pre-enrollment data**, yaitu data sebelum mahasiswa masuk atau pada saat pendaftaran.
Kemudian ada **absensi dan status kehadiran**, yang sering muncul sebagai indikator kedisiplinan dan keterlibatan.
Selain itu, banyak paper juga menggunakan **LMS usage** atau **digital traces**, misalnya frekuensi login, akses materi, dan interaksi pada platform pembelajaran.
Lalu ada **engagement mahasiswa**, serta faktor lain seperti **ekonomi, keluarga, dan riwayat studi**.

Secara umum, variabel-variabel ini menunjukkan bahwa risiko dropout tidak ditentukan oleh satu faktor saja, tetapi oleh kombinasi antara **akademik, perilaku belajar, dan konteks personal mahasiswa**.

---

## Slide 7 — Metode yang Digunakan

Dari sisi metode, mayoritas paper menggunakan pendekatan **machine learning** untuk memprediksi dropout maupun performa akademik mahasiswa.

Beberapa metode yang paling sering muncul adalah **Random Forest** dan **XGBoost**, karena keduanya cukup kuat untuk data tabular dan sering memberikan performa yang baik.
Selain itu, ada juga penelitian yang menggunakan **clustering analysis** untuk mengidentifikasi pola perilaku mahasiswa, bukan hanya klasifikasi langsung.
Beberapa paper menerapkan **deep learning**, terutama ketika struktur data dan jumlah datanya mendukung.
Ada juga pendekatan **AutoML** untuk otomatisasi pemilihan model dan tuning, serta **ensemble** atau **hybrid model** untuk meningkatkan akurasi.
Sebagian penelitian bahkan sudah mengarah pada **experimental early warning system**.

Dari sini terlihat bahwa fokus utama penelitian masih banyak berada pada **pemilihan model dan peningkatan performa prediksi**.

---

## Slide 8 — Ringkasan Temuan Utama

Secara umum, ada beberapa temuan utama yang cukup konsisten di antara 10 paper yang kami review.

Pertama, banyak paper menunjukkan bahwa **prediksi mahasiswa berisiko dapat dilakukan sejak awal studi**, sehingga intervensi tidak harus menunggu sampai kondisi mahasiswa memburuk.
Kedua, baik **data akademik** maupun **data perilaku digital** sama-sama berkontribusi terhadap performa model.
Ketiga, **aktivitas LMS** dan **engagement mahasiswa** sering muncul sebagai indikator yang kuat dalam mendeteksi risiko.
Keempat, beberapa paper menegaskan bahwa akurasi model meningkat ketika **data semester berjalan** ditambahkan, karena model mendapat gambaran perilaku yang lebih aktual.
Namun yang perlu dicatat, **early warning system membantu identifikasi mahasiswa berisiko, tetapi tidak otomatis menjamin keberhasilan intervensi**.

Artinya, prediksi hanyalah langkah awal. Nilai manfaatnya baru benar-benar terasa jika hasil prediksi dihubungkan dengan tindakan nyata dari institusi.

---

## Slide 9 — Perbandingan 10 Paper secara Umum

Jika dibandingkan secara umum, mayoritas paper memang berfokus pada **prediksi risiko dropout** atau **performa akademik mahasiswa**.
Namun ada perbedaan pada jenis data yang dijadikan fokus.

Sebagian paper lebih menitikberatkan pada **data pra-kuliah** atau **pre-enrollment**, sehingga lebih menekankan prediksi awal.
Sebagian lainnya lebih fokus pada **data aktivitas selama kuliah**, seperti nilai semester, absensi, dan penggunaan LMS.
Ada juga paper yang mencoba memahami **pola perilaku mahasiswa melalui clustering**, sehingga orientasinya lebih eksploratif.
Sementara itu, beberapa paper menekankan **optimasi model**, misalnya melalui **AutoML** atau **hybrid approach**.

Kalau kita tarik benang merahnya, orientasi penelitian masih dominan di sisi **model**, **akurasi**, dan **eksperimen prediksi**, sedangkan sisi pemanfaatan hasil untuk monitoring manajerial belum terlalu kuat.

---

## Slide 10 — Research Gap

Nah, dari hasil review ini, kami melihat beberapa **research gap** yang penting.

Pertama, sebagian besar paper **berhenti pada level prediksi**, dan belum banyak yang masuk ke tahap **pemanfaatan hasil prediksi dalam dashboard BI**.
Kedua, aspek **visual analytics** untuk pengambil keputusan akademik juga belum dibahas secara operasional. Jadi, modelnya ada, tetapi bagaimana hasilnya dipantau secara rutin oleh program studi atau pimpinan akademik masih belum jelas.
Ketiga, banyak dataset yang digunakan bersifat **tertutup** dan berasal dari **satu institusi**, sehingga generalisasi hasil penelitian menjadi terbatas.
Keempat, hubungan antara **model prediksi**, **monitoring berkala**, dan **action plan intervensi** juga masih belum terhubung kuat.

Di sinilah muncul peluang untuk pendekatan **DVBI**, yaitu pendekatan yang tidak hanya fokus pada prediksi, tetapi juga pada **monitoring, visualisasi, segmentasi risiko, dan decision support**.

---

## Slide 11 — Implikasi untuk Dashboard BI

Berdasarkan gap tersebut, ada implikasi yang cukup jelas untuk pengembangan **dashboard BI**.

Hasil prediksi dropout seharusnya tidak berhenti sebagai angka akurasi model atau label klasifikasi saja, tetapi perlu diterjemahkan menjadi **indikator yang mudah dipantau** oleh pihak akademik.
Misalnya, dashboard dapat menampilkan **tren risiko dropout**, **faktor dominan yang memengaruhi risiko**, serta **segmentasi mahasiswa berisiko** berdasarkan angkatan, program studi, atau pola engagement.
Visualisasi yang interaktif juga akan membantu pimpinan program studi atau bagian akademik untuk melihat **prioritas intervensi** dengan lebih cepat.

Dengan kata lain, integrasi antara **analytics** dan **dashboard** menjadi nilai tambah yang penting, dan inilah area yang menurut kami masih belum banyak dibahas secara mendalam di paper-paper sebelumnya.

---

## Slide 12 — Kesimpulan dan Arah Lanjutan

Sebagai kesimpulan, literature review ini menunjukkan bahwa **student dropout analytics** merupakan area yang sangat kuat dan relevan untuk **predictive analytics di pendidikan tinggi**.
Variabel yang sering digunakan mencakup **performa akademik**, **demografi**, **engagement**, dan **digital traces**.
Metode yang dominan meliputi **Random Forest**, **XGBoost**, **clustering**, **deep learning**, dan **AutoML**.

Namun, gap utamanya masih berada pada **integrasi hasil analitik ke dalam dashboard BI dan visual decision support**.
Karena itu, arah lanjutan yang kami usulkan adalah **merumuskan desain dashboard early warning** untuk monitoring mahasiswa berisiko, sehingga hasil analitik tidak hanya informatif secara teknis, tetapi juga bermanfaat secara praktis bagi pengambil keputusan akademik.

Sekian presentasi dari kami. Terima kasih.
