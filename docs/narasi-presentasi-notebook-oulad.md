# Narasi Presentasi Notebook OULAD Early Warning

Naskah ini mengikuti urutan tampilan pada `notebooks/oulad_early_warning_dvbi_colab.ipynb`. Teks dapat dibaca langsung dengan tetap memberi ruang untuk menunjuk tabel atau grafik yang sedang tampil. Catatan **Cursor** dibaca dalam hati sebagai arahan visual untuk presenter.

## Pembagian Presenter

| Presenter | Tampilan notebook | Fokus |
|---|---|---|
| Presenter 1 | Pembukaan sampai Section 5 | konteks penelitian, sumber data, konstruksi dataset, prediction horizon |
| Presenter 2 | Section 6 sampai Section 12 | EDA, data split, preprocessing, model selection, evaluasi |
| Presenter 3 | Section 13 sampai Section 18 | knowledge layer, alarm intervensi, dashboard, prioritas, kesimpulan |

---

## Presenter 1 - Konteks Penelitian dan Persiapan Data

### Cell Pembuka - Judul dan Ringkasan Penelitian

> **Cursor:** Sorot baris **Judul**, lalu pindahkan ke heading **Ringkasan Penelitian** ketika mulai menjelaskan konteks riset.

Assalamualaikum warahmatullahi wabarakatuh. Selamat sore Pak Andi dan teman-teman.

Kami dari Kelompok 5 akan mempresentasikan penelitian berjudul “Early Warning Risiko Dropout Mahasiswa pada Minggu Keempat Menggunakan Supervised Learning dan KnowledgeBased Risk Layer pada Open University Learning Analytics Dataset”.

Penelitian ini menyusun early warning system untuk mengenali mahasiswa yang berisiko memperoleh hasil akhir `Withdrawn` atau `Fail` berdasarkan informasi yang tersedia sampai akhir minggu keempat. Data yang digunakan adalah OULAD, yang memuat profil mahasiswa, registrasi, assessment, dan aktivitas pada Virtual Learning Environment atau VLE.

Masalah prediksinya dirumuskan sebagai supervised binary classification. Kelas `AtRisk` berasal dari hasil akhir `Withdrawn` atau `Fail`, sedangkan kelas `Successful` berasal dari `Pass` atau `Distinction`.

Kami membandingkan Logistic Regression, Random Forest, dan XGBoost. Model dipilih melalui cross-validation dengan recall `AtRisk` sebagai metrik utama. Recall menunjukkan proporsi kasus `AtRisk` yang berhasil dikenali oleh model.

> **Cursor:** Sorot paragraf terakhir Ringkasan Penelitian pada frasa **evaluasi model, knowledge-based risk layer, dan dashboard**.

Keluaran penelitian terdiri dari evaluasi model, knowledge-based risk layer, dan dashboard monitoring. Hasilnya digunakan sebagai decision support untuk menyusun prioritas verifikasi dan tindak lanjut akademik.

### Cell Alur Analitik Penelitian

> **Cursor:** Ikuti diagram dari **Data hingga hari ke-28**, turun ke **Klasifikasi biner**, lalu ke **Prioritas intervensi**.

Diagram ini merangkum alurnya. Data sampai hari ke-28 masuk ke model klasifikasi biner. Model menghasilkan kelas prediksi dan `P(AtRisk)`, yaitu probabilitas kelas `AtRisk` menurut model.

Setelah itu, prediksi dipadukan dengan sinyal assessment dan aktivitas VLE. Gabungan tersebut membentuk prioritas `High Risk`, `Medium Risk`, atau `Low Risk`. Jadi, model memprediksi dua kelas, sementara tiga level risiko digunakan untuk mengatur prioritas tindak lanjut.

### Section 1 - Konfigurasi Analisis

> **Cursor:** Sorot Markdown **Alasan cut-off**, kemudian jalankan pandangan ke output `random state 42; horizon observasi 28 hari`.

Pada bagian ini kami menyiapkan library untuk pengolahan data, visualisasi, preprocessing, pemodelan, dan evaluasi.

`RANDOM_STATE` ditetapkan sebesar 42 agar data split dan komponen acak model dapat direproduksi. `CUTOFF_DAY` ditetapkan sebesar 28 sebagai observation horizon pada akhir minggu keempat.

Minggu keempat dipilih karena data perilaku awal sudah mulai terbentuk dan waktu untuk melakukan tindak lanjut masih tersedia. Dalam penelitian ini, hari ke-28 digunakan sebagai baseline horizon yang sama untuk seluruh eksperimen.

### Section 2 - Akuisisi Data OULAD

> **Cursor:** Sorot `DATA_URL` dan `EXPECTED_FILES`, lalu arahkan ke output **Tujuh tabel sumber dimuat**.

Notebook mengambil arsip OULAD dari UCI Machine Learning Repository. File kemudian diekstrak dan diperiksa berdasarkan daftar tabel yang dibutuhkan.

Output menunjukkan tujuh tabel sumber tersedia. Lima tabel digunakan langsung dalam konstruksi dataset analisis, sedangkan tabel lain tetap diverifikasi sebagai bagian dari arsip OULAD.

### Section 3 - Struktur Dataset

> **Cursor:** Sorot tabel ringkasan ukuran sumber, kemudian tunjuk preview `studentInfo` dan `studentRegistration` secara bergantian.

Bagian ini memperlihatkan struktur tabel yang digunakan. `studentInfo` menyediakan profil mahasiswa dan `final_result`. `studentRegistration` menyediakan waktu registrasi. `assessments` menghubungkan assessment dengan modul dan presentation. `studentAssessment` mencatat submission dan skor, sedangkan `studentVle` mencatat aktivitas akses pada VLE.

Preview di bawah tabel ringkasan memperlihatkan sumber label hasil akhir dan informasi registrasi. Nilai tanggal pada OULAD dinyatakan relatif terhadap awal perkuliahan, sehingga nilai negatif menunjukkan kejadian sebelum hari pertama modul.

### Section 4 - Konstruksi Dataset Early Warning Minggu Keempat

> **Cursor:** Sorot `KEYS = ['code_module', 'code_presentation', 'id_student']`, kemudian arahkan ke pembentukan `base` dan `risk_label`.

Pada bagian ini dataset dibentuk dengan tiga key: kode modul, kode presentation, dan ID mahasiswa. Kombinasi tersebut membentuk unit analisis `student-module-presentation`, yaitu satu mahasiswa pada satu modul dan satu periode penyelenggaraan.

Kolom `risk_label` kemudian dibentuk dari `final_result`. Hasil `Withdrawn` dan `Fail` diberi label `AtRisk`. Hasil `Pass` dan `Distinction` diberi label `Successful`.

> **Cursor:** Turunkan ke `reg_features` dan sorot `date_registration`.

Setelah target terbentuk, fitur registrasi mengambil `date_registration` berdasarkan tiga key yang sama.

> **Cursor:** Sorot pembentukan `assessment_early`, filter `date_submitted <= CUTOFF_DAY`, lalu blok `assessment_features`.

Data submission kemudian dihubungkan dengan konteks modul dan presentation. Baris assessment dibatasi sampai hari ke-28, lalu diringkas menjadi jumlah assessment serta mean, maximum, dan minimum score untuk setiap unit analisis.

> **Cursor:** Lanjutkan ke pembentukan `vle_early`, filter `date <= CUTOFF_DAY`, lalu blok `vle_features`.

Aktivitas VLE juga dibatasi sampai hari ke-28. Data tersebut diringkas menjadi total clicks, active days, jumlah site yang diakses, dan hari aktivitas terakhir.

> **Cursor:** Sorot blok `dataset` yang menggabungkan `base`, `reg_features`, `assessment_features`, dan `vle_features`.

Empat bagian tersebut kemudian digabungkan menjadi dataset analisis: profil dan target dari `base`, fitur registrasi, fitur assessment, serta fitur VLE.

> **Cursor:** Pertahankan tampilan pada blok merging sambil menjelaskan fungsi setiap kelompok predictor. Daftar lengkapnya akan terlihat pada output feature matrix di Section 5.

Predictor profil terdiri dari enam attribute. `gender` merepresentasikan gender mahasiswa. `region` menunjukkan wilayah tempat tinggal. `highest_education` menunjukkan pendidikan tertinggi sebelum mengikuti modul. `imd_band` merepresentasikan kelompok tingkat deprivation wilayah. `age_band` menunjukkan kelompok usia, dan `disability` mencatat status disabilitas. Attribute tersebut memberi konteks profil mahasiswa pada pola prediksi.

Riwayat studi menggunakan `num_of_prev_attempts` untuk menunjukkan jumlah percobaan sebelumnya pada modul dan `studied_credits` untuk menunjukkan beban kredit yang diambil mahasiswa.

Konteks perkuliahan menggunakan `code_module` untuk membedakan modul serta `code_presentation` untuk membedakan periode penyelenggaraan. Kedua attribute membantu model membaca variasi pola antar-modul dan antar-periode.

Fitur registrasi menggunakan `date_registration` untuk menunjukkan waktu registrasi relatif terhadap awal perkuliahan. Nilai negatif berarti registrasi dilakukan sebelum hari pertama module-presentation.

Fitur assessment terdiri dari empat attribute. `assessment_count` menunjukkan jumlah submission sampai hari ke-28. `assessment_score_mean` merangkum rata-rata score, `assessment_score_max` menunjukkan score tertinggi, dan `assessment_score_min` menunjukkan score terendah pada periode tersebut.

Aktivitas VLE juga terdiri dari empat attribute. `vle_total_clicks` menunjukkan intensitas akses, `vle_active_days` menunjukkan konsistensi hari aktif, `vle_site_count` menunjukkan jumlah bagian VLE yang diakses, dan `vle_last_activity_day` menunjukkan waktu aktivitas terakhir sampai prediction horizon.

Secara keseluruhan, model menggunakan 19 predictors: enam attribute profil, dua riwayat studi, dua konteks perkuliahan, satu registrasi, empat assessment, dan empat aktivitas VLE.

> **Cursor:** Turunkan ke daftar `behavior_cols`, lalu sorot baris `dataset[behavior_cols] = dataset[behavior_cols].fillna(0)`.

Behavioral features yang belum memiliki catatan sampai hari ke-28 diisi dengan nilai nol. Pada data assessment, nilai tersebut dibaca bersama `assessment_count` untuk melihat apakah mahasiswa sudah melakukan submission.

> **Cursor:** Pada output, tunjuk preview assessment mentah, assessment features, aktivitas VLE mentah, dan VLE features sesuai urutan tampilannya.

Empat output pertama memperlihatkan perubahan data harian menjadi aggregated features per `student-module-presentation`. Preview assessment menampilkan submission dan score sampai hari ke-28, kemudian tabel berikutnya menampilkan hasil agregasinya. Urutan yang sama ditampilkan untuk aktivitas VLE.

> **Cursor:** Arahkan ke output **Unit analisis** dan **Mahasiswa unik**, lalu tunjuk preview **Analysis dataset setelah merging dan aggregation**.

Dataset yang terbentuk berisi 32.593 `student-module-presentation` dari 28.785 mahasiswa unik. Preview terakhir menyatukan final result, risk label, registration day, assessment, dan aktivitas VLE dalam satu tampilan.

### Section 5 - Prediction Horizon Validation

> **Cursor:** Sorot tabel **Tipe data yang digunakan**, terutama baris Target label, Identitas grouping, dan Informasi setelah kejadian.

Prediction horizon menetapkan informasi yang tersedia ketika prediksi dibuat. Di sini seluruh predictor dibatasi pada informasi yang tersedia sampai hari ke-28.

Tabel pada layar membedakan peran setiap jenis data. `risk_label` menjadi target, `id_student` digunakan untuk grouping saat split, dan `final_result` menjadi sumber pembentukan label. Feature matrix mengecualikan `date_unregistration` karena kolom tersebut berkaitan dengan kejadian pengunduran diri.

Feature matrix terdiri dari delapan categorical features dan sebelas numerical features. Daftar ini menjadi batas eksplisit atribut yang masuk ke pipeline model.

> **Cursor:** Arahkan ke output daftar `Categorical features` dan `Numerical features` sebelum berpindah presenter.

Selanjutnya, kami masuk ke eksplorasi data dan proses pemodelan.

---

## Presenter 2 - Eksplorasi, Pemodelan, dan Evaluasi

### Section 6 - Eksplorasi Data

> **Cursor:** Tunjuk grafik distribusi target, lalu grafik missing values. Setelah itu arahkan ke tabel median perilaku di bawah grafik.

Exploratory Data Analysis digunakan untuk membaca distribusi target, missing values, dan pola awal pada behavioral features.

Dataset memiliki 17.208 baris `AtRisk` dan 15.385 baris `Successful`, sehingga proporsinya relatif berdekatan. Median total klik VLE pada kelas `AtRisk` adalah 92, sedangkan pada kelas `Successful` adalah 298. Median hari aktifnya masing-masing 7 dan 16 hari.

Median skor assessment kelas `AtRisk` tampil nol karena banyak mahasiswa belum memiliki submission sampai hari ke-28. Angka ini menggambarkan pola data pada horizon tersebut dan dibaca bersama assessment count.

Perbedaan pada grafik merupakan pola deskriptif dalam dataset. Pengaruh setiap feature terhadap prediksi akan dibaca kembali setelah model dilatih.

### Section 7 - Data Split Design

> **Cursor:** Ikuti diagram dari **Seluruh student-module-presentation** menuju cabang **80% train-validation** dan **20% hold-out test**.

Data kemudian dibagi menjadi 80 persen train-validation dan 20 persen hold-out test menggunakan `GroupShuffleSplit` berdasarkan `id_student`.

Grouping diperlukan karena satu mahasiswa dapat muncul pada beberapa `student-module-presentation`. Seluruh baris milik mahasiswa yang sama ditempatkan pada satu bagian data.

Output menunjukkan 26.122 baris pada train-validation dan 6.471 baris pada hold-out test, dengan overlap mahasiswa sebesar nol. Proporsi `AtRisk` juga serupa, yaitu 52,9 persen pada train-validation dan 52,5 persen pada test.

> **Cursor:** Sorot tiga baris output: ukuran split, **Overlap mahasiswa: 0**, dan distribusi train-test.

Diagram berikutnya menunjukkan lima fold pada bagian train-validation. Setelah model final dipilih, hold-out test digunakan untuk evaluasi generalisasi.

### Section 8 - Pipeline Preprocessing dan Model

> **Cursor:** Sorot tabel **Ringkasan preprocessing** dari numerical features sampai class imbalance.

Numerical features diproses dengan median imputation dan standardization. Categorical features diproses dengan most-frequent imputation dan one-hot encoding.

Seluruh transformasi ditempatkan di dalam pipeline. Dengan susunan ini, nilai imputasi, skala, dan kategori dipelajari dari training fold pada setiap putaran cross-validation.

Class weighting menyesuaikan kontribusi kedua kelas berdasarkan distribusi training data. Proporsi kelas yang berdekatan menghasilkan bobot yang juga berdekatan.

Tiga model yang dibandingkan adalah Logistic Regression sebagai baseline linear, Random Forest sebagai ensemble decision tree, dan XGBoost sebagai gradient-boosted trees. Konfigurasinya dibuat tetap agar tahap ini berfungsi sebagai perbandingan baseline.

> **Cursor:** Arahkan ke dictionary `models`, lalu tunjuk nama ketiga model pada output.

### Section 9 - Model Selection with Cross-Validation

> **Cursor:** Sorot Markdown pada kalimat **Recall AtRisk menjadi metrik seleksi utama**, kemudian arahkan ke tabel `cv_summary`.

Setiap model dievaluasi dengan lima fold berbasis kelompok mahasiswa. Pada setiap putaran, empat fold digunakan untuk training dan satu fold untuk validation.

Random Forest memperoleh mean recall `AtRisk` tertinggi sebesar 0,7107. XGBoost memperoleh recall 0,6938 dan Logistic Regression 0,6889. Berdasarkan kriteria yang ditetapkan sejak awal, Random Forest dipilih sebagai model final.

XGBoost memiliki mean ROC-AUC tertinggi sebesar 0,8440, sementara Random Forest memperoleh 0,8362. Tabel ini memperlihatkan hasil setiap model pada beberapa metrik, dengan recall `AtRisk` sebagai dasar model selection.

> **Cursor:** Gerakkan horizontal pada baris Random Forest dari `recall_mean` ke `recall_std`, lalu bandingkan dengan dua baris di bawahnya.

Standard deviation antar-fold menunjukkan variasi performa pada lima validation fold. Pada recall `AtRisk`, Random Forest mencatat standard deviation sebesar 0,0085.

### Section 10 - Evaluasi Generalisasi pada Hold-Out Test

> **Cursor:** Sorot output **Model terpilih berdasarkan cross-validation: Random Forest**, lalu pindahkan ke baris Random Forest pada tabel test.

Setelah dipilih melalui cross-validation, Random Forest dilatih kembali menggunakan seluruh train-validation dan dievaluasi pada hold-out test.

Pada test set, Random Forest menghasilkan accuracy 0,7594, precision `AtRisk` 0,8007, recall `AtRisk` 0,7213, F1-score 0,7589, dan ROC-AUC 0,8396.

Recall 0,7213 berarti sekitar 72 persen baris `AtRisk` pada hold-out test berhasil dikenali. Precision 0,8007 berarti sekitar 80 persen prediksi `AtRisk` sesuai dengan label aktual.

> **Cursor:** Pada classification report, tunjuk baris `AtRisk` dan kolom precision, recall, serta support.

Tabel juga menampilkan hasil dua model lain sebagai pembanding. Hasil cross-validation menentukan Random Forest sebagai model final, kemudian angka test menunjukkan performanya pada hold-out data.

### Cell Benchmark Penelitian Sebelumnya

> **Cursor:** Tunjuk kolom **Skenario** lebih dahulu, lalu baca sel metrik yang tersedia pada setiap penelitian.

Bagian ini menyandingkan metrik penelitian dengan lima paper OULAD yang terbit dalam rentang 2022 sampai 2025.

Shou menggunakan multidimensional time-series dan MTAPSP harian pada 20 persen durasi course. Pada skenario dengan kelompok `Pass` serta `Distinction` dan kelompok `Fail` serta `Withdrawn`, model tersebut menghasilkan accuracy 0,9179 dan F1-score 0,9180. Jawad memakai 260 hari dan SMOTE. Balabied menggunakan klasifikasi biner dengan Random Forest. Ujkani menggabungkan `Fail` dan `Withdrawn` sebagai at-risk. Alnasyan menggunakan target biner yang sama dengan penelitian ini melalui KANFormer. Kolom skenario membantu membaca setiap angka bersama prediction horizon, split, balancing, dan model yang digunakan.

### Section 11 - Visualisasi Evaluasi Model

> **Cursor:** Mulai dari grafik perbandingan metrik, pindah ke confusion matrix Random Forest, lalu akhiri pada ROC curve.

Visualisasi pertama membandingkan metrik ketiga model pada hold-out test. Confusion matrix menunjukkan prediksi benar dan salah dari Random Forest, termasuk false negative, yaitu kasus `AtRisk` yang diprediksi `Successful`.

ROC curve memperlihatkan kemampuan model membedakan kedua kelas pada berbagai decision threshold. Nilai ROC-AUC Random Forest pada hold-out test adalah 0,8396.

Ketiga tampilan ini dibaca bersama: recall menggambarkan cakupan deteksi, precision menggambarkan ketepatan alarm, dan confusion matrix menunjukkan jumlah kasus konkret di setiap kategori.

### Section 12 - Feature Importance of the Final Model

> **Cursor:** Tunjuk lima bar teratas pada grafik, kemudian arahkan ke lima baris teratas tabel feature importance.

Karena model finalnya Random Forest, kontribusi feature dibaca melalui `feature_importances_`.

Feature dengan importance tertinggi adalah total klik VLE, hari aktivitas terakhir, jumlah hari aktif VLE, jumlah site VLE, dan tanggal registrasi. Assessment score juga muncul dalam kelompok feature dengan kontribusi besar.

Feature importance menunjukkan kontribusi prediktif global di dalam model. Nilai ini membantu memahami pola yang digunakan model, sementara alasan pada level mahasiswa akan dibentuk melalui aturan pada knowledge layer.

> **Cursor:** Kembali ke Markdown **Interpretasi** dan sorot frasa **kontribusi prediktif global** sebelum berpindah presenter.

Sampai bagian ini, penelitian sudah menghasilkan model klasifikasi dan evaluasi generalisasi. Selanjutnya, output model diterjemahkan menjadi prioritas monitoring akademik.

---

## Presenter 3 - Knowledge Layer, Dashboard, dan Kesimpulan

### Section 13 - Knowledge-Based Risk Layer

> **Cursor:** Sorot Markdown **Aturan**, kemudian tunjuk blok kode `signal_map`, `high`, dan `medium`.

Random Forest menghasilkan prediksi kelas dan `P(AtRisk)`. Knowledge-based risk layer menggabungkan hasil tersebut dengan empat sinyal: skor assessment, partisipasi assessment, total klik VLE, dan hari aktif VLE.

Threshold sinyal dihitung dari kuartil bawah train-validation. Pada output ini threshold-nya adalah skor assessment 0, assessment count 0, total klik VLE 47, dan hari aktif VLE 4.

Aturan `High Risk` memerlukan prediksi `AtRisk` dan minimal dua sinyal. `Medium Risk` diberikan ketika salah satu kondisi tersebut terpenuhi. Baris lainnya masuk `Low Risk`.

Hasil pada hold-out test terdiri dari 1.816 baris `High Risk`, 1.979 `Medium Risk`, dan 2.676 `Low Risk`. Tabel contoh memperlihatkan hubungan antara prediksi model, probabilitas, jumlah sinyal, alasan, level risiko, dan rekomendasi.

> **Cursor:** Ikuti satu baris pada tabel contoh dari `predicted_atrisk` menuju `probability_atrisk`, `risk_signal_count`, level, alasan, dan rekomendasi.

`P(AtRisk)` merupakan probabilitas yang dihasilkan Random Forest dan digunakan untuk mengurutkan prioritas. Probability calibration dicatat sebagai tahap pengembangan berikutnya.

### Section 14 - Evaluasi Alarm Intervensi

> **Cursor:** Sorot tabel perbandingan pada kolom precision, recall, dan F1; kemudian pindah ke confusion matrix alarm. Tunjuk matriks dari kiri atas, kanan atas, kiri bawah, lalu kanan bawah.

Untuk mengevaluasi alarm, `High Risk` dan `Medium Risk` dipetakan sebagai alarm `AtRisk`. Hasilnya dibandingkan dengan prediksi Random Forest sebelum aturan diterapkan.

Pada confusion matrix ini, `AtRisk` menjadi kelas positif. Angka 1.951 merupakan true negative, yaitu aktual `Successful` dan diprediksi `Successful`. Angka 1.122 merupakan false positive, yaitu aktual `Successful` dan diprediksi `AtRisk`.

Pada baris berikutnya, 725 merupakan false negative, yaitu aktual `AtRisk` dan diprediksi `Successful`. Angka 2.673 merupakan true positive, yaitu aktual `AtRisk` dan diprediksi `AtRisk`.

Kolom prediksi `Successful` berjumlah 2.676 dan sesuai dengan jumlah `Low Risk`. Kolom prediksi `AtRisk` berjumlah 3.795, berasal dari 1.816 `High Risk` ditambah 1.979 `Medium Risk`.

Dari 3.398 kasus aktual `AtRisk`, sebanyak 2.673 masuk ke dalam alarm. Hasil ini memberikan recall sebesar 78,66 persen. Dari 3.795 alarm `AtRisk`, sebanyak 2.673 sesuai dengan kelas aktual dan menghasilkan precision sebesar 70,43 persen.

Knowledge layer pada konfigurasi ini memperluas cakupan deteksi sekaligus menambah antrean yang perlu diverifikasi. Angka recall dan precision tersebut memberi gambaran trade-off operasional dari aturan yang digunakan.

### Section 15 - Dashboard Monitoring Akademik

> **Cursor:** Sapukan cursor dari tiga KPI di bagian atas, kemudian ikuti panel dashboard dari kiri ke kanan dan dari atas ke bawah.

Dashboard merangkum hasil pada hold-out test. KPI di bagian atas menunjukkan mahasiswa unik, jumlah `student-module-presentation` yang masuk prioritas, dan persentasenya.

Panel berikutnya memperlihatkan distribusi level risiko serta proporsi High dan Medium Risk per module-presentation. Panel perilaku menampilkan distribusi `P(AtRisk)`, frekuensi sinyal, serta median aktivitas per level risiko.

Bagian bawah dashboard menghubungkan tampilan monitoring dengan evaluasi model melalui confusion matrix dan perbandingan metrik model terhadap alarm intervensi.

> **Cursor:** Berhenti pada judul panel **Model ML vs Alarm Intervensi** saat menjelaskan hubungan antara monitoring dan evaluasi.

Seluruh angka pada dashboard ini merupakan hasil evaluasi hold-out, sehingga fungsinya dalam penelitian adalah demonstrasi tampilan monitoring pada data uji.

### Section 16 - Prioritas Intervensi dan Temuan Utama

> **Cursor:** Sorot output **TEMUAN UTAMA UNTUK INTERVENSI AKADEMIK**, lalu tunjuk baris pertama sampai ketiga secara berurutan.

Daftar prioritas mengambil baris `High Risk` dan `Medium Risk`, kemudian mengurutkannya berdasarkan level, `P(AtRisk)`, dan jumlah sinyal.

Output menghasilkan 3.795 `student-module-presentation` dalam antrean. Sinyal yang paling sering muncul adalah skor assessment rendah dengan 2.341 kasus.

Output juga menunjukkan module-presentation dengan proporsi prioritas tertinggi dan sinyal risiko yang paling sering muncul pada hold-out test.

Tabel dua puluh baris teratas menunjukkan bahwa probabilitas, alasan risiko, dan rekomendasi dapat ditelusuri untuk setiap unit analisis. Dalam penerapan akademik, ID yang sama dapat diringkas kembali jika seorang mahasiswa muncul pada lebih dari satu modul.

> **Cursor:** Pada tabel prioritas, ikuti satu baris secara utuh dari `id_student` sampai `recommended_action`, lalu akhiri pada alasan dan rekomendasi.

### Section 17 - Ekspor Artefak Analisis

> **Cursor:** Tunjuk ketiga nama file pada tabel **Artefak analisis yang diekspor**.

Notebook mengekspor tiga file CSV: evaluasi model, evaluasi knowledge layer, dan daftar prioritas intervensi.

Artefak tersebut menyimpan hasil utama dalam format terstruktur sehingga dapat digunakan kembali untuk pemeriksaan hasil atau pengembangan dashboard berikutnya.

### Section 18 - Kesimpulan dan Keterbatasan

> **Cursor:** Sorot paragraf **Kesimpulan** mulai dari tiga model pembanding, Random Forest, metrik hold-out, knowledge-based risk layer, lalu dashboard.

Penelitian ini membandingkan Logistic Regression, Random Forest, dan XGBoost menggunakan supervised binary classification untuk mengenali risiko `Withdrawn` atau `Fail` berdasarkan informasi sampai minggu keempat.

Random Forest dipilih karena memperoleh mean recall `AtRisk` tertinggi pada cross-validation. Pada hold-out test, model menghasilkan recall `AtRisk` 0,7213 dan precision `AtRisk` 0,8007.

Knowledge-based risk layer menggabungkan prediksi model dengan sinyal assessment dan VLE untuk membentuk tiga level prioritas beserta alasan dan rekomendasi. Dashboard menyajikan hasil tersebut sebagai indikator monitoring dan prioritas intervensi.

> **Cursor:** Turunkan ke daftar **Keterbatasan** dan tunjuk kelima poin secara berurutan: target dan horizon, aturan operasional, trade-off metrik, pengembangan model, lalu validasi institusi.

Pada bagian ini, target berasal dari hasil akhir dan predictors dibatasi sampai hari ke-28. Level risiko serta threshold kuartil berfungsi sebagai aturan operasional, sedangkan feature importance menunjukkan kontribusi prediktif dalam model.

Perubahan recall dibaca bersama precision dan jumlah kasus dalam antrean intervensi. Ruang pengembangan berikutnya mencakup probability calibration, hyperparameter tuning, optimasi classification threshold, dan evaluasi fairness. Penerapan pada institusi lain dilanjutkan melalui validasi dengan data dan proses akademik setempat karena OULAD merepresentasikan konteks Open University di Inggris.

Demikian presentasi dari Kelompok 5. Terima kasih atas perhatian Pak Andi dan teman-teman. Wassalamualaikum warahmatullahi wabarakatuh.
