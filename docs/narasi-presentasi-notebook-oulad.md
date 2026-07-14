# Narasi Presentasi Notebook OULAD Early Warning

Naskah ini mengikuti urutan tampilan pada `notebooks/oulad_early_warning_dvbi_colab.ipynb`. Teks dapat dibaca langsung dengan tetap memberi ruang untuk menunjuk tabel atau grafik yang sedang tampil.

## Pembagian Presenter

| Presenter | Tampilan notebook | Fokus |
|---|---|---|
| Presenter 1 | Pembukaan sampai Section 5 | konteks penelitian, sumber data, konstruksi dataset, prediction horizon |
| Presenter 2 | Section 6 sampai Section 12 | EDA, data split, preprocessing, model selection, evaluasi |
| Presenter 3 | Section 13 sampai Section 18 | knowledge layer, alarm intervensi, dashboard, prioritas, kesimpulan |

---

## Presenter 1 - Konteks Penelitian dan Persiapan Data

### Cell Pembuka - Judul dan Ringkasan Penelitian

Assalamualaikum warahmatullahi wabarakatuh. Selamat pagi atau siang Bapak/Ibu dosen dan teman-teman.

Kami dari Kelompok 5 akan mempresentasikan penelitian berjudul “Early Warning Risiko Dropout Mahasiswa pada Minggu Keempat Menggunakan Supervised Learning dan KnowledgeBased Risk Layer pada Open University Learning Analytics Dataset”.

Penelitian ini menyusun early warning system untuk mengenali mahasiswa yang berisiko memperoleh hasil akhir `Withdrawn` atau `Fail` berdasarkan informasi yang tersedia sampai akhir minggu keempat. Data yang digunakan adalah OULAD, yang memuat profil mahasiswa, registrasi, assessment, dan aktivitas pada Virtual Learning Environment atau VLE.

Masalah prediksinya dirumuskan sebagai supervised binary classification. Kelas `AtRisk` berasal dari hasil akhir `Withdrawn` atau `Fail`, sedangkan kelas `Successful` berasal dari `Pass` atau `Distinction`.

Kami membandingkan Logistic Regression, Random Forest, dan XGBoost. Model dipilih melalui cross-validation dengan recall `AtRisk` sebagai metrik utama. Recall menunjukkan proporsi kasus `AtRisk` yang berhasil dikenali oleh model.

Keluaran penelitian terdiri dari evaluasi model, knowledge-based risk layer, dan dashboard monitoring. Hasilnya digunakan sebagai decision support untuk menyusun prioritas verifikasi dan tindak lanjut akademik.

### Cell Alur Analitik Penelitian

Diagram ini merangkum alurnya. Data sampai hari ke-28 masuk ke model klasifikasi biner. Model menghasilkan kelas prediksi dan `P(AtRisk)`, yaitu probabilitas kelas `AtRisk` menurut model.

Setelah itu, prediksi dipadukan dengan sinyal assessment dan aktivitas VLE. Gabungan tersebut membentuk prioritas `High Risk`, `Medium Risk`, atau `Low Risk`. Jadi, model memprediksi dua kelas, sementara tiga level risiko digunakan untuk mengatur prioritas tindak lanjut.

### Section 1 - Konfigurasi Analisis

Pada bagian ini kami menyiapkan library untuk pengolahan data, visualisasi, preprocessing, pemodelan, dan evaluasi.

`RANDOM_STATE` ditetapkan sebesar 42 agar data split dan komponen acak model dapat direproduksi. `CUTOFF_DAY` ditetapkan sebesar 28 sebagai observation horizon pada akhir minggu keempat.

Minggu keempat dipilih karena data perilaku awal sudah mulai terbentuk dan waktu untuk melakukan tindak lanjut masih tersedia. Dalam penelitian ini, hari ke-28 digunakan sebagai baseline horizon yang sama untuk seluruh eksperimen.

### Section 2 - Akuisisi Data OULAD

Notebook mengambil arsip OULAD dari UCI Machine Learning Repository. File kemudian diekstrak dan diperiksa berdasarkan daftar tabel yang dibutuhkan.

Output menunjukkan tujuh tabel sumber tersedia. Lima tabel digunakan langsung dalam konstruksi dataset analisis, sedangkan tabel lain tetap diverifikasi sebagai bagian dari arsip OULAD.

### Section 3 - Struktur Dataset

Bagian ini memperlihatkan struktur tabel yang digunakan. `studentInfo` menyediakan profil mahasiswa dan `final_result`. `studentRegistration` menyediakan waktu registrasi. `assessments` menghubungkan assessment dengan modul dan presentation. `studentAssessment` mencatat submission dan skor, sedangkan `studentVle` mencatat aktivitas akses pada VLE.

Preview di bawah tabel ringkasan memperlihatkan sumber label hasil akhir dan informasi registrasi. Nilai tanggal pada OULAD dinyatakan relatif terhadap awal perkuliahan, sehingga nilai negatif menunjukkan kejadian sebelum hari pertama modul.

### Section 4 - Konstruksi Dataset Early Warning Minggu Keempat

Pada bagian ini tabel sumber digabungkan menjadi dataset analisis. Unit analisisnya adalah `student-module-presentation`, yaitu satu mahasiswa pada satu modul dan satu periode penyelenggaraan. Seorang mahasiswa dapat memiliki lebih dari satu baris ketika mengikuti modul atau presentation yang berbeda.

Assessment dibatasi pada `date_submitted` sampai hari ke-28. Aktivitas VLE juga dibatasi sampai hari ke-28, kemudian diringkas menjadi total klik, jumlah hari aktif, jumlah site yang diakses, dan hari aktivitas terakhir.

Target `risk_label` dibentuk dari `final_result`. Informasi tersebut digunakan sebagai label pembelajaran, sementara predictor berasal dari profil, registrasi, assessment awal, dan aktivitas VLE awal.

Output menampilkan jejak dari data assessment dan VLE menuju aggregated features, kemudian preview dataset hasil penggabungan. Dataset yang terbentuk berisi 32.593 `student-module-presentation` dari 28.785 mahasiswa unik.

Nilai nol pada behavioral features menunjukkan tidak adanya aktivitas atau submission yang tercatat sampai cut-off. Karena itu, nilai nol pada skor assessment dibaca bersama jumlah assessment, bukan sebagai bukti bahwa mahasiswa memperoleh nilai ujian nol.

### Section 5 - Prediction Horizon Validation

Prediction horizon menetapkan informasi yang tersedia ketika prediksi dibuat. Di sini seluruh predictor dibatasi pada informasi yang tersedia sampai hari ke-28.

Tabel pada layar membedakan peran setiap jenis data. `risk_label` menjadi target, `id_student` digunakan untuk grouping saat split, dan `final_result` menjadi sumber pembentukan label. `date_unregistration` tidak masuk ke feature matrix karena kolom tersebut berkaitan dengan kejadian pengunduran diri.

Feature matrix terdiri dari delapan categorical features dan sebelas numerical features. Daftar ini menjadi batas eksplisit atribut yang masuk ke pipeline model.

Selanjutnya, kami masuk ke eksplorasi data dan proses pemodelan.

---

## Presenter 2 - Eksplorasi, Pemodelan, dan Evaluasi

### Section 6 - Eksplorasi Data

Exploratory Data Analysis digunakan untuk membaca distribusi target, missing values, dan pola awal pada behavioral features.

Dataset memiliki 17.208 baris `AtRisk` dan 15.385 baris `Successful`, sehingga proporsinya relatif berdekatan. Median total klik VLE pada kelas `AtRisk` adalah 92, sedangkan pada kelas `Successful` adalah 298. Median hari aktifnya masing-masing 7 dan 16 hari.

Median skor assessment kelas `AtRisk` tampil nol karena banyak mahasiswa belum memiliki submission sampai hari ke-28. Angka ini menggambarkan pola data pada horizon tersebut dan dibaca bersama assessment count.

Perbedaan pada grafik merupakan pola deskriptif dalam dataset. Pengaruh setiap feature terhadap prediksi akan dibaca kembali setelah model dilatih.

### Section 7 - Data Split Design

Data kemudian dibagi menjadi 80 persen train-validation dan 20 persen hold-out test menggunakan `GroupShuffleSplit` berdasarkan `id_student`.

Grouping diperlukan karena satu mahasiswa dapat muncul pada beberapa `student-module-presentation`. Seluruh baris milik mahasiswa yang sama ditempatkan pada satu bagian data.

Output menunjukkan 26.122 baris pada train-validation dan 6.471 baris pada hold-out test, dengan overlap mahasiswa sebesar nol. Proporsi `AtRisk` juga serupa, yaitu 52,9 persen pada train-validation dan 52,5 persen pada test.

Diagram berikutnya menunjukkan bahwa lima fold hanya diterapkan pada bagian train-validation. Hold-out test digunakan setelah model final dipilih.

### Section 8 - Pipeline Preprocessing dan Model

Numerical features diproses dengan median imputation dan standardization. Categorical features diproses dengan most-frequent imputation dan one-hot encoding.

Seluruh transformasi ditempatkan di dalam pipeline. Dengan susunan ini, nilai imputasi, skala, dan kategori dipelajari dari training fold pada setiap putaran cross-validation.

Class weighting digunakan untuk menyeimbangkan kontribusi kelas sesuai distribusi training data tanpa membuat sampel sintetis. Karena distribusi kelas cukup dekat, pengaruh pembobotannya juga terbatas.

Tiga model yang dibandingkan adalah Logistic Regression sebagai baseline linear, Random Forest sebagai ensemble decision tree, dan XGBoost sebagai gradient-boosted trees. Konfigurasinya dibuat tetap agar tahap ini berfungsi sebagai perbandingan baseline.

### Section 9 - Model Selection with Cross-Validation

Setiap model dievaluasi dengan lima fold berbasis kelompok mahasiswa. Pada setiap putaran, empat fold digunakan untuk training dan satu fold untuk validation.

Random Forest memperoleh mean recall `AtRisk` tertinggi sebesar 0,7107. XGBoost memperoleh recall 0,6938 dan Logistic Regression 0,6889. Berdasarkan kriteria yang ditetapkan sejak awal, Random Forest dipilih sebagai model final.

Metrik lain tetap diperhatikan. XGBoost memiliki mean ROC-AUC tertinggi sebesar 0,8440, sementara Random Forest memperoleh 0,8362. Hasil ini menunjukkan bahwa pemilihan model mengikuti prioritas recall pada konteks early warning, sekaligus mempertahankan metrik lain sebagai pembanding.

Standard deviation antar-fold juga ditampilkan untuk melihat variasi performa. Selisih antar-model pada baseline ini cukup kecil, sehingga hasilnya dibaca sebagai dasar model selection dalam ruang eksperimen yang diuji.

### Section 10 - Evaluasi Generalisasi pada Hold-Out Test

Setelah dipilih melalui cross-validation, Random Forest dilatih kembali menggunakan seluruh train-validation dan dievaluasi pada hold-out test.

Pada test set, Random Forest menghasilkan accuracy 0,7594, precision `AtRisk` 0,8007, recall `AtRisk` 0,7213, F1-score 0,7589, dan ROC-AUC 0,8396.

Recall 0,7213 berarti sekitar 72 persen baris `AtRisk` pada hold-out test berhasil dikenali. Precision 0,8007 berarti sekitar 80 persen prediksi `AtRisk` sesuai dengan label aktual.

Tabel juga menampilkan hasil dua model lain untuk memberi konteks evaluasi. Pemilihan Random Forest tetap berasal dari hasil cross-validation; angka test digunakan untuk membaca generalisasi akhir.

### Cell Benchmark Penelitian Sebelumnya

Bagian ini menyandingkan metrik notebook dengan angka yang dilaporkan dalam tiga penelitian sebelumnya.

Tanda kosong menunjukkan metrik yang tidak dilaporkan pada paper terkait. Perbandingan ini digunakan sebagai konteks literatur karena dataset, target, prediction horizon, dan desain evaluasinya berbeda. Oleh karena itu, grafik dibaca per metrik yang tersedia dan tidak digunakan untuk menentukan peringkat penelitian.

### Section 11 - Visualisasi Evaluasi Model

Visualisasi pertama membandingkan metrik ketiga model pada hold-out test. Confusion matrix menunjukkan prediksi benar dan salah dari Random Forest, termasuk false negative, yaitu kasus `AtRisk` yang diprediksi `Successful`.

ROC curve memperlihatkan kemampuan model membedakan kedua kelas pada berbagai decision threshold. Nilai ROC-AUC Random Forest pada hold-out test adalah 0,8396.

Ketiga tampilan ini dibaca bersama: recall menggambarkan cakupan deteksi, precision menggambarkan ketepatan alarm, dan confusion matrix menunjukkan jumlah kasus konkret di setiap kategori.

### Section 12 - Feature Importance of the Final Model

Karena model finalnya Random Forest, kontribusi feature dibaca melalui `feature_importances_`.

Feature dengan importance tertinggi adalah total klik VLE, hari aktivitas terakhir, jumlah hari aktif VLE, jumlah site VLE, dan tanggal registrasi. Assessment score juga muncul dalam kelompok feature dengan kontribusi besar.

Feature importance menunjukkan kontribusi prediktif global di dalam model. Nilai ini membantu memahami pola yang digunakan model, sementara alasan pada level mahasiswa akan dibentuk melalui aturan pada knowledge layer.

Sampai bagian ini, penelitian sudah menghasilkan model klasifikasi dan evaluasi generalisasi. Selanjutnya, output model diterjemahkan menjadi prioritas monitoring akademik.

---

## Presenter 3 - Knowledge Layer, Dashboard, dan Kesimpulan

### Section 13 - Knowledge-Based Risk Layer

Random Forest menghasilkan prediksi kelas dan `P(AtRisk)`. Knowledge-based risk layer menggabungkan hasil tersebut dengan empat sinyal: skor assessment, partisipasi assessment, total klik VLE, dan hari aktif VLE.

Threshold sinyal dihitung dari kuartil bawah train-validation. Pada output ini threshold-nya adalah skor assessment 0, assessment count 0, total klik VLE 47, dan hari aktif VLE 4.

Aturan `High Risk` memerlukan prediksi `AtRisk` dan minimal dua sinyal. `Medium Risk` diberikan ketika salah satu kondisi tersebut terpenuhi. Baris lainnya masuk `Low Risk`.

Hasil pada hold-out test terdiri dari 1.816 baris `High Risk`, 1.979 `Medium Risk`, dan 2.676 `Low Risk`. Tabel contoh memperlihatkan hubungan antara prediksi model, probabilitas, jumlah sinyal, alasan, level risiko, dan rekomendasi.

`P(AtRisk)` merupakan probabilitas yang dihasilkan Random Forest. Nilai tersebut digunakan untuk pengurutan prioritas dan belum melalui probability calibration khusus.

### Section 14 - Evaluasi Alarm Intervensi

Untuk mengevaluasi alarm, `High Risk` dan `Medium Risk` dipetakan sebagai alarm `AtRisk`. Hasilnya dibandingkan dengan prediksi Random Forest sebelum aturan diterapkan.

Confusion matrix alarm menunjukkan 2.673 kasus `AtRisk` terdeteksi dan 725 kasus terlewat. Dari angka tersebut, recall alarm sekitar 78,7 persen. Sebanyak 1.122 baris `Successful` juga masuk ke dalam alarm, sehingga precision turun menjadi sekitar 70,4 persen.

Knowledge layer pada konfigurasi ini memperluas cakupan deteksi sekaligus menambah antrean yang perlu diverifikasi. Angka recall dan precision tersebut memberi gambaran trade-off operasional dari aturan yang digunakan.

### Section 15 - Dashboard Monitoring Akademik

Dashboard merangkum hasil pada hold-out test. KPI di bagian atas menunjukkan mahasiswa unik, jumlah `student-module-presentation` yang masuk prioritas, dan persentasenya.

Panel berikutnya memperlihatkan distribusi level risiko serta proporsi High dan Medium Risk per module-presentation. Panel perilaku menampilkan distribusi `P(AtRisk)`, frekuensi sinyal, serta median aktivitas per level risiko.

Bagian bawah dashboard menghubungkan tampilan monitoring dengan evaluasi model melalui confusion matrix dan perbandingan metrik model terhadap alarm intervensi.

Seluruh angka pada dashboard ini merupakan hasil evaluasi hold-out, sehingga fungsinya dalam penelitian adalah demonstrasi tampilan monitoring pada data uji.

### Section 16 - Prioritas Intervensi dan Temuan Utama

Daftar prioritas mengambil baris `High Risk` dan `Medium Risk`, kemudian mengurutkannya berdasarkan level, `P(AtRisk)`, dan jumlah sinyal.

Output menghasilkan 3.795 `student-module-presentation` dalam antrean. Sinyal yang paling sering muncul adalah skor assessment rendah dengan 2.341 kasus.

Module GGG presentation 2014J memiliki proporsi High dan Medium Risk tertinggi pada hold-out test. Persentase pada bagian ini menggambarkan komposisi sampel test untuk module-presentation tersebut, sehingga pembacaannya perlu disertai jumlah observasi ketika digunakan untuk keputusan operasional.

Tabel dua puluh baris teratas menunjukkan bahwa probabilitas, alasan risiko, dan rekomendasi dapat ditelusuri untuk setiap unit analisis. Dalam penerapan akademik, ID yang sama dapat diringkas kembali jika seorang mahasiswa muncul pada lebih dari satu modul.

### Section 17 - Ekspor Artefak Analisis

Notebook mengekspor tiga file CSV: evaluasi model, evaluasi knowledge layer, dan daftar prioritas intervensi.

Artefak tersebut menyimpan hasil utama dalam format terstruktur sehingga dapat digunakan kembali untuk pemeriksaan hasil atau pengembangan dashboard berikutnya.

### Section 18 - Kesimpulan dan Keterbatasan

Penelitian ini membandingkan tiga model supervised binary classification untuk mengenali risiko `Withdrawn` atau `Fail` berdasarkan informasi sampai minggu keempat.

Random Forest dipilih karena memperoleh mean recall `AtRisk` tertinggi pada cross-validation. Pada hold-out test, model menghasilkan recall 0,7213 dan precision 0,8007. Knowledge-based risk layer kemudian mengubah hasil model dan sinyal perilaku menjadi tiga level prioritas beserta alasan dan rekomendasi.

Hasil penelitian menunjukkan bagaimana prediksi, aturan berbasis pengetahuan, dan visualisasi BI dapat disusun menjadi alur decision support. Hasilnya masih berada dalam konteks eksperimen OULAD.

Keterbatasan penelitian mencakup threshold aturan yang masih berupa baseline berbasis kuartil, probabilitas yang belum dikalibrasi, hyperparameter yang belum dituning, dan fairness antarkelompok yang belum dievaluasi. OULAD juga berasal dari konteks Open University di Inggris, sehingga penerapan pada institusi lain memerlukan validasi menggunakan data dan proses akademik setempat.

Demikian presentasi dari Kelompok 5. Terima kasih atas perhatian Bapak/Ibu dosen dan teman-teman. Wassalamualaikum warahmatullahi wabarakatuh.
