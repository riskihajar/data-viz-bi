# III. Methodology

## A. Research Design

Penelitian ini dirancang sebagai penelitian supervised learning untuk klasifikasi risiko mahasiswa. Fokus metodologi mencakup pemilihan dataset, preprocessing, pembentukan fitur, rancangan model, knowledge-based risk layer, dan pemetaan keluaran model ke indikator Business Intelligence. Dengan alur tersebut, penelitian tidak hanya menyiapkan prediksi risiko, tetapi juga menyiapkan cara membaca hasil prediksi sebagai dasar monitoring akademik.

Alur penelitian yang direncanakan terdiri dari lima tahap utama. Tahap pertama adalah pemilihan dan audit dataset. Tahap kedua adalah preprocessing dan pembentukan dataset tabular. Tahap ketiga adalah pemodelan supervised learning menggunakan beberapa algoritma baseline. Tahap keempat adalah penambahan knowledge-based risk layer. Tahap kelima adalah evaluasi dan interpretasi hasil untuk mendukung kebutuhan early warning dan Business Intelligence. Dengan pembatasan tersebut, metode utama penelitian ditempatkan sebagai supervised binary classification, sedangkan dashboard dan clustering diperlakukan sebagai pengembangan lanjutan.

## B. Dataset

Dataset yang digunakan adalah Open University Learning Analytics Dataset (OULAD) [4]. Dataset ini dipilih karena memiliki data akademik dan aktivitas pembelajaran digital yang relevan untuk analisis risiko mahasiswa. OULAD terdiri dari beberapa tabel, antara lain `studentInfo`, `studentRegistration`, `studentAssessment`, dan `studentVle`. Berdasarkan audit awal, tabel `studentInfo` memiliki 32.593 baris, sedangkan `studentVle` memiliki lebih dari 10 juta catatan aktivitas pembelajaran.

Unit analisis yang digunakan adalah satu mahasiswa pada satu kombinasi `code_module` dan `code_presentation`. Dengan demikian, satu baris dataset hasil preprocessing merepresentasikan satu student-module-presentation. Unit ini dipilih karena sesuai dengan struktur label pada `studentInfo` dan memungkinkan penggabungan data registrasi, assessment, serta aktivitas VLE secara konsisten.

## C. Target Label

Target penelitian dirumuskan sebagai klasifikasi biner. Label `AtRisk` diberikan untuk mahasiswa dengan `final_result` berupa `Withdrawn` atau `Fail`. Label `Successful` diberikan untuk mahasiswa dengan `final_result` berupa `Pass` atau `Distinction`. Formulasi ini dipilih karena lebih sesuai dengan tujuan early warning dibandingkan klasifikasi multi-kelas penuh.

Berdasarkan dataset hasil preprocessing, jumlah data pada kelas `AtRisk` adalah 17.208 baris, sedangkan kelas `Successful` adalah 15.385 baris. Distribusi ini menunjukkan bahwa kedua kelas memiliki jumlah data yang memadai untuk skenario klasifikasi biner.

## D. Feature Construction

Fitur dibentuk dari beberapa sumber data. Dari `studentInfo`, fitur yang digunakan mencakup gender, region, highest education, IMD band, age band, jumlah percobaan sebelumnya, jumlah kredit yang dipelajari, dan disability. Dari `studentRegistration`, fitur utama yang digunakan adalah tanggal registrasi, tanggal unregistration, serta flag `has_unregistration`.

Dari `studentAssessment`, fitur diagregasi menjadi jumlah assessment, rata-rata skor, skor maksimum, dan skor minimum. Agregasi assessment dirancang untuk dihubungkan dengan tabel `assessments` agar perhitungan skor mengikuti unit `code_module`, `code_presentation`, dan `id_student`. Dari `studentVle`, fitur diagregasi menjadi total klik, jumlah hari aktif, jumlah site yang diakses, dan hari aktivitas terakhir. Nilai `imd_band` yang kosong diisi dengan kategori `Unknown`, sedangkan nilai numerik hasil agregasi disiapkan agar dapat digunakan oleh model supervised learning.

## E. Supervised Learning Scenario

Skenario supervised learning yang direncanakan menggunakan minimal tiga algoritma pembanding. Algoritma baseline pertama adalah Logistic Regression karena dapat memberikan model awal yang sederhana dan mudah diinterpretasikan. Algoritma kedua adalah Random Forest karena mampu menangani hubungan non-linear dan fitur campuran pada data tabular, serta sering digunakan pada penelitian prediksi performa akademik bertahap [9]. Algoritma ketiga adalah XGBoost atau Gradient Boosting karena sering digunakan pada kasus klasifikasi tabular dan telah digunakan dalam studi prediksi dropout berbasis data pra-enrollment [6].

Evaluasi model dirancang menggunakan pembagian data train-test dan metrik seperti accuracy, precision, recall, F1-score, dan confusion matrix. Karena tujuan penelitian berkaitan dengan deteksi mahasiswa berisiko, metrik recall untuk kelas `AtRisk` perlu diberi perhatian khusus agar model tidak terlalu banyak melewatkan mahasiswa yang berpotensi gagal atau withdrawn.

## F. Knowledge-Based Risk Layer

Knowledge-based risk layer dirancang sebagai lapisan tambahan berbasis aturan yang berjalan setelah fitur risiko terbentuk. Lapisan ini tidak menggantikan model supervised learning, tetapi berfungsi sebagai mekanisme interpretasi dan pendukung keputusan. Aturan disusun berdasarkan indikator yang relevan secara akademik, seperti engagement VLE, performa assessment, dan sinyal unregistration. Masukan utama lapisan ini adalah `assessment_score_mean`, `assessment_count`, `vle_total_clicks`, `vle_active_days`, `vle_last_activity_day`, dan `has_unregistration`.

Output knowledge-based layer dirancang dalam tiga tingkat, yaitu `High Risk`, `Medium Risk`, dan `Low Risk`. Threshold awal ditentukan menggunakan kuartil bawah dari dataset hasil preprocessing. Skor assessment dianggap rendah apabila `assessment_score_mean` kurang dari 50,29. Partisipasi assessment dianggap sangat rendah apabila `assessment_count` kurang dari 2. Aktivitas VLE dianggap rendah apabila `vle_total_clicks` kurang dari 142 atau `vle_active_days` kurang dari 11. Sinyal unregistration ditandai ketika `has_unregistration` bernilai 1.

Mahasiswa diberi indikator `High Risk` apabila memiliki sinyal unregistration dan minimal dua indikator akademik atau VLE berada pada kondisi risiko. Mahasiswa diberi indikator `Medium Risk` apabila memiliki dua indikator risiko tanpa sinyal unregistration, atau satu indikator risiko dengan sinyal unregistration. Mahasiswa diberi indikator `Low Risk` apabila kondisi `High Risk` dan `Medium Risk` tidak terpenuhi. Threshold tersebut bersifat baseline awal dan dapat dievaluasi ulang setelah eksperimen model dilakukan.

Integrasi dengan model supervised learning dilakukan dengan menempatkan knowledge-based layer sebagai penjelas hasil prediksi. Jika model memprediksi mahasiswa sebagai `AtRisk`, rule layer digunakan untuk menunjukkan indikator yang mendukung prediksi tersebut. Jika model memprediksi mahasiswa sebagai `Successful` tetapi rule layer memberi status `High Risk`, data mahasiswa tersebut dapat ditandai sebagai kasus yang perlu ditinjau ulang dalam dashboard atau analisis lanjutan. Dalam konteks decision support, status `High Risk` diarahkan sebagai prioritas monitoring tinggi, `Medium Risk` sebagai mahasiswa yang perlu observasi berkala, dan `Low Risk` sebagai mahasiswa yang cukup dipantau secara reguler. Dengan cara ini, keluaran sistem tidak hanya berupa label prediksi, tetapi juga alasan risiko yang dapat dibaca oleh pihak akademik.

Kelebihan pendekatan knowledge-based adalah hasilnya mudah dijelaskan kepada pihak akademik, dapat dihubungkan dengan dashboard, dan membantu menerjemahkan keluaran model menjadi indikator tindakan. Kekurangannya adalah aturan dapat bersifat kaku, bergantung pada ambang batas yang ditentukan, dan perlu divalidasi ulang jika konteks data atau kebijakan akademik berubah. Oleh karena itu, lapisan aturan ini dirancang sebagai pelengkap model data-driven, bukan sebagai satu-satunya mekanisme prediksi.

## G. Visual Analytics and BI Scenario

Keluaran model dirancang sebagai dasar indikator monitoring akademik, sehingga hasil klasifikasi tidak hanya dipahami sebagai metrik teknis, tetapi juga sebagai informasi pendukung keputusan. Rancangan visual analytics memuat jumlah mahasiswa `AtRisk`, distribusi `High Risk`, `Medium Risk`, dan `Low Risk`, perbandingan risiko antar module-presentation, ringkasan aktivitas VLE, serta ringkasan performa assessment. Indikator tersebut dapat digunakan untuk membantu pihak akademik melihat prioritas intervensi tanpa harus membaca seluruh detail teknis model.

Dashboard berperan sebagai media penyajian indikator decision support, sedangkan kontribusi metodologis tetap berfokus pada supervised binary classification dan knowledge-based risk layer. Dengan posisi tersebut, visual analytics menjadi bentuk pemanfaatan hasil analitik. Evaluasi tidak hanya melihat accuracy, precision, recall, dan F1-score, tetapi juga apakah keluaran risiko dapat dipetakan menjadi indikator yang actionable untuk monitoring akademik.

## H. Research Scenario

Skenario penelitian diarahkan untuk membandingkan beberapa algoritma supervised learning, menganalisis fitur yang paling berkontribusi terhadap risiko, dan mengintegrasikan prediksi model dengan knowledge-based risk layer. Hasil yang diharapkan adalah model klasifikasi risiko yang dapat dijelaskan dan dapat menjadi dasar visualisasi early warning dalam konteks Business Intelligence.
