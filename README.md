# Data Visualization and Business Intelligence: Student Performance / Dropout Analytics

Repository ini berisi bahan kerja untuk tugas mata kuliah **Data Visualization and Business Intelligence (DVBI)** dengan tema:

> **Student Performance / Dropout Analytics**

Topik ini dipilih karena memiliki relevansi yang kuat dengan Business Intelligence dalam konteks pendidikan tinggi. Permasalahan dropout dan performa akademik mahasiswa dapat dianalisis menggunakan data akademik, data perilaku belajar, data sosiodemografis, serta data digital trace untuk menghasilkan insight yang mendukung **monitoring**, **early warning**, dan **pengambilan keputusan berbasis data**.

---

## Latar Belakang

Perguruan tinggi menghadapi tantangan dalam memantau performa mahasiswa dan mengidentifikasi mahasiswa yang berisiko mengalami penurunan performa atau dropout. Dalam konteks BI, data mahasiswa tidak hanya berfungsi sebagai arsip administratif, tetapi juga dapat diolah menjadi informasi strategis untuk:

- mengidentifikasi mahasiswa berisiko sejak dini,
- memantau performa akademik antar semester,
- memahami faktor-faktor yang memengaruhi dropout,
- mendukung intervensi akademik yang lebih tepat sasaran,
- menyediakan dasar bagi dashboard monitoring dan visual analytics.

Dengan demikian, topik ini tidak hanya relevan dari sisi analitik prediktif, tetapi juga cocok untuk pengembangan **dashboard BI** dan **visualisasi data** pada domain pendidikan tinggi.

---

## Tujuan Repository

Repository ini disusun untuk mendukung proses pengerjaan tugas, khususnya pada bagian:

1. **pencarian dan pengumpulan paper**,  
2. **penyusunan literature review**,  
3. **pembuatan matriks ringkasan paper**,  
4. **pengarsipan PDF referensi**,  
5. **penyiapan bahan untuk analisis lanjutan / dashboard BI**.

---

## Fokus Kajian

Fokus utama repository ini adalah pada tema berikut:

- **student performance analytics**,
- **student retention / dropout prediction**,
- **early warning system in higher education**,
- **educational data mining / learning analytics**,
- **relevansi hasil analitik terhadap Data Visualization dan Business Intelligence**.

Secara konseptual, repository ini menempatkan literature review bukan sebagai reproduksi eksperimen, melainkan sebagai **kajian domain, metode, variabel, temuan, dan research gap** dari paper-paper yang relevan.

---

## Struktur Repository

```text
.
├── README.md
├── assets/
├── data/
├── docs/
│   └── artikel-uts-ieee/
└── literature-review/
    ├── student-dropout-analytics-10-paper.xlsx
    ├── matriks-literature-review-student-dropout-10-paper.xlsx
    └── papers-pdf/
```

### Penjelasan folder

- **assets/**  
  Folder untuk aset pendukung seperti gambar, screenshot, atau bahan visual lain jika diperlukan.

- **data/**  
  Folder yang dapat digunakan untuk menyimpan dataset publik atau data turunan yang akan dipakai pada tahap analisis/visualisasi berikutnya.

- **docs/**  
  Folder untuk draft penulisan, catatan, outline, atau dokumen turunan dari tugas utama.

- **docs/artikel-uts-ieee/**  
  Folder draft artikel UTS IEEE berbahasa Indonesia. Draft dibuat modular per section agar mudah diedit dan dijaga konsisten dengan arah penelitian akhir.

- **literature-review/**  
  Folder utama yang berisi hasil pencarian paper, matriks literature review, dan arsip PDF referensi.

---

## Isi Folder `literature-review`

### Ringkasan file utama

| File / Folder | Deskripsi | Isi utama | Kegunaan |
|---|---|---|---|
| `student-dropout-analytics-10-paper.xlsx` | Daftar 10 paper kandidat | NO, Publisher, Topics, Tahun, Penulis, Judul, DOI, LINK | Basis awal seleksi paper |
| `matriks-paper-student-dropout-10.xlsx` | Matriks ringkas 10 paper untuk presentasi/tinjauan cepat | No, Penulis, Q, Metode, Dataset, Hasil, Masalah, Kelemahan, Link DOI | Ringkasan cepat kontribusi paper, kualitas jurnal, dan DOI |
| `matriks-literature-review-student-dropout-10-paper.xlsx` | Matriks sintesis 10 paper | Paper, Fokus, Variabel, Metode, Temuan, Gap/Keterbatasan | Membantu analisis perbandingan dan penarikan gap |
| `papers-pdf/` | Arsip PDF paper yang sudah divalidasi | 10 PDF + file ekstraksi teks pendukung | Referensi utama untuk membaca paper secara langsung |

### Matriks literature review (inline)

| No | Paper | Fokus | Variabel | Metode | Temuan | Gap/Keterbatasan |
|---|---|---|---|---|---|---|
| 1 | Using machine learning to predict student retention from socio-demographic characteristics and app-based engagement metrics (2023) | Prediksi retensi/dropout mahasiswa dengan menggabungkan data sosiodemografis dan engagement aplikasi | sosiodemografis, interaksi layanan kampus, event engagement, interaksi sosial, data institusional awal | machine learning (gabungan macro, micro, meso-level predictors) | Kombinasi data institusional dan engagement mahasiswa mampu memprediksi dropout dengan baik sejak semester awal. | Data mentah tidak terbuka publik; konteks data spesifik aplikasi/universitas tertentu; fokus utama pada prediksi, belum pada dashboard BI. |
| 2 | Hybrid Approach to Predicting Learning Success Based on Digital Educational History for Timely Identification of At-Risk Students (2024) | Prediksi keberhasilan belajar dan identifikasi mahasiswa berisiko berbasis digital educational history | riwayat akademik digital, engagement, digital footprint, digital personality portrait | hybrid model, ensemble ML, Markov process | Kombinasi histori pendidikan dan data berjalan dapat meningkatkan identifikasi mahasiswa at-risk secara lebih dini. | Generalisasi model dibatasi oleh lingkungan pendidikan masing-masing; belum menonjolkan implementasi visual analytics/BI. |
| 3 | Early warning systems for more effective student counselling in higher education: Evidence from a Dutch field experiment (2022) | Evaluasi early warning system untuk mendukung counselling mahasiswa | risk score mahasiswa, dropout tahun pertama, performa akademik, intervensi konselor | early warning system, randomized field experiment | Sistem mampu mengidentifikasi mahasiswa berisiko, tetapi intervensi berbantuan EWS belum otomatis menurunkan dropout atau meningkatkan performa. | Prediksi saja tidak cukup; masih perlu actionable feedback dan strategi intervensi; visualisasi/BI belum dibahas mendalam. |
| 4 | Enhancing the Early Student Dropout Prediction Model Through Clustering Analysis of Students’ Digital Traces (2024) | Peningkatan model prediksi dropout melalui analisis clustering digital traces LMS | log LMS, aktivitas Moodle, pola interaksi belajar, performa akademik | PCA, UMAP, clustering (BIRCH, DBSCAN, GMM) | Digital traces dapat mengelompokkan mahasiswa berdasarkan pola aktivitas dan mengungkap korelasi kuat dengan performa/risiko dropout. | Fokus pada teknik analitik dan clustering; minim pembahasan penerjemahan hasil ke sistem BI/dashboard untuk pengambil keputusan. |
| 5 | Predicting Student Dropout from Day One: XGBoost-Based Early Warning System Using Pre-Enrollment Data (2025) | Prediksi dropout sejak awal masuk kuliah menggunakan data pra-enrollment | usia, GPA sekolah, admission status, kondisi ekonomi, tanggung jawab keluarga, variabel demografis | XGBoost classifier | Data pendaftaran awal saja sudah cukup untuk mendeteksi mahasiswa berisiko; model efektif untuk early intervention. | Hanya memakai pre-enrollment data sehingga belum menangkap dinamika perilaku selama kuliah; belum membahas integrasi visualisasi atau monitoring dashboard. |
| 6 | Assisting Educational Analytics with AutoML Functionalities (2022) | Pemanfaatan AutoML untuk educational analytics dan prediksi performa/kelulusan | performa mata kuliah sebelumnya, informasi akademik, lama studi, data mahasiswa | AutoML | AutoML membantu menemukan model dan parameter terbaik untuk memprediksi durasi kelulusan/performa mahasiswa. | Lebih kuat di sisi optimasi model daripada BI; keterkaitan dengan visualisasi dan decision support institusional belum banyak dibahas. |
| 7 | Precision education with statistical learning and deep learning: a case study in Taiwan (2020) | Prediksi risiko dropout dan intervensi dini berbasis big data pendidikan | ranking kelas, loan application, jumlah ketidakhadiran, latar belakang belajar, performa akademik | statistical learning, deep learning | Performa akademik, pinjaman mahasiswa, dan absensi menjadi prediktor penting dropout; intervensi dini dinilai penting. | Dataset berasal dari satu universitas; data tidak terbuka publik; orientasi masih dominan pada prediksi, belum pada BI/dashboard. |
| 8 | Multi-Class Phased Prediction of Academic Performance and Dropout in Higher Education (2023) | Prediksi performa akademik dan dropout secara bertahap sepanjang tahun pertama | data akademik, sosial-demografis, makroekonomi, fase waktu semester awal | Random Forest, beberapa algoritma ML, imbalanced handling | Waktu prediksi memengaruhi performa model; Random Forest memberi hasil terbaik di beberapa fase. | Fokus pada akurasi dan timing prediksi; belum banyak mengeksplor bagaimana output model dimanfaatkan dalam sistem visual monitoring. |
| 9 | Study regarding the influence of a student’s personality and an LMS usage profile on learning performance using machine learning techniques (2024) | Pengaruh personality dan pola penggunaan LMS terhadap performa belajar | prior academic performance, personality, academic engagement, LMS usage profile | machine learning interpretable models | Personality, engagement, dan performa awal dapat membantu identifikasi risiko kegagalan akademik. | Sampel relatif kecil dan spesifik; lebih fokus ke performa akademik dibanding dropout; implementasi BI/dashboard belum menjadi fokus utama. |
| 10 | Crossing individual university boundaries: a comprehensive approach to predicting dropouts in the higher education system (2025) | Prediksi dropout pada level sistem pendidikan tinggi lintas universitas | pre-enrollment data, performa akademik per semester, data transfer antar institusi, trajectory studi | machine learning pada administrative system-wide data | Data tingkat nasional meningkatkan cakupan analisis dropout; performa model membaik ketika data semester berjalan ditambahkan. | Data administratif besar dan tertutup; fokus pada prediksi sistemik, belum menjelaskan visual analytics atau dashboard decision support secara operasional. |

### Ringkasan koleksi PDF

| Status | Jumlah | Keterangan |
|---|---:|---|
| PDF tervalidasi | 10 | Semua paper target sudah tersedia di folder `papers-pdf/` |
| File ekstraksi teks (`.txt`) | 10 | Digunakan untuk membantu validasi isi PDF terhadap judul target |

Matriks dan arsip PDF ini digunakan untuk memudahkan proses sintesis literature review, pembandingan antar paper, dan penarikan research gap.

---

## Ringkasan Literatur

Dari proses pencarian awal, paper-paper yang terkumpul secara umum membahas beberapa tema besar berikut:

1. **prediksi dropout mahasiswa**,  
2. **prediksi performa akademik mahasiswa**,  
3. **early warning system untuk identifikasi mahasiswa berisiko**,  
4. **pemanfaatan LMS/digital traces dalam analitik pendidikan**,  
5. **penggunaan machine learning dalam konteks higher education analytics**.

Variabel yang sering muncul di dalam paper meliputi:
- performa akademik awal,
- data sosiodemografis,
- absensi,
- engagement LMS,
- riwayat akademik,
- faktor ekonomi dan keluarga,
- interaksi digital mahasiswa.

Metode yang umum digunakan antara lain:
- Logistic Regression,
- Random Forest,
- XGBoost,
- clustering,
- ensemble learning,
- deep learning,
- AutoML.

---

## Kaitan dengan Data Visualization dan Business Intelligence

Topik ini memiliki kaitan langsung dengan Data Visualization dan BI karena hasil analitik dari data mahasiswa dapat diterjemahkan menjadi:

- dashboard monitoring performa mahasiswa,
- visualisasi kelompok mahasiswa berisiko,
- analisis tren performa antar semester,
- ringkasan faktor utama penyebab dropout,
- early warning panel untuk mendukung pengambilan keputusan akademik.

Dengan kata lain, literature review pada repository ini menjadi dasar konseptual untuk menjawab pertanyaan:

> bagaimana data mahasiswa dapat diolah menjadi insight yang relevan untuk monitoring, deteksi dini, dan keputusan strategis di lingkungan perguruan tinggi?

---

## Status Pengerjaan Saat Ini

Saat ini repository telah mencakup:

- daftar awal **10 paper kandidat**,
- matriks literature review berbasis 10 paper,
- arsip PDF referensi yang telah divalidasi,
- struktur awal untuk pengembangan draft tugas,
- draft artikel UTS IEEE sampai bagian **Methodology**.

Tahap berikutnya yang dapat dikembangkan dari repository ini meliputi:

- eksperimen modeling supervised learning dengan minimal tiga algoritma,
- implementasi knowledge-based risk layer,
- penyusunan Results, Discussion, dan Conclusion untuk artikel akhir,
- pengembangan visualisasi atau dashboard early warning sebagai implikasi BI jika waktu memungkinkan.

## Update terbaru: OULAD sebagai dataset kerja utama

Dataset kerja utama yang saat ini dipilih adalah **Open University Learning Analytics Dataset (OULAD)** karena lebih aman terhadap syarat capstone dibanding dataset UCI sebelumnya.

## Output Eksperimen dan Dashboard

Pipeline OULAD saat ini sudah mencakup preprocessing dataset, eksperimen supervised binary classification, knowledge-based risk layer, dan dashboard DVBI untuk stakeholder akademik.

Output dashboard tersedia di:

- [`assets/dashboard/oulad-risk-dashboard.html`](assets/dashboard/oulad-risk-dashboard.html)

Dashboard ini ditujukan untuk pimpinan akademik, program studi, dosen wali/tutor, dan tim counselling. Fokusnya bukan evaluasi teknis model, tetapi monitoring risiko, intervention queue, prioritas module-presentation, alasan risiko, dan daftar mahasiswa yang perlu ditindaklanjuti.

Untuk menjalankan ulang pipeline:

```bash
PYTHONPATH=. python3 scripts/build_oulad_binary_dataset.py
PYTHONPATH=. python3 scripts/run_oulad_experiment.py
PYTHONPATH=. python3 scripts/build_oulad_dashboard.py
python3 -m http.server 8765
```

Lalu buka dashboard di:

```text
http://localhost:8765/assets/dashboard/oulad-risk-dashboard.html
```

## Draft Artikel UTS IEEE

Draft artikel UTS berada di folder [`docs/artikel-uts-ieee/`](docs/artikel-uts-ieee/). Draft ini disusun sebagai artikel ilmiah berbahasa Indonesia dengan format section yang mendekati IEEE Conference, tetapi masih dalam bentuk Markdown agar mudah diedit.

### File draft artikel

| File | Fungsi |
|---|---|
| [00-title-author.md](docs/artikel-uts-ieee/00-title-author.md) | Judul, author, afiliasi, email author, serta catatan dosen supervisi dan dosen kelas. |
| [01-abstract-keywords.md](docs/artikel-uts-ieee/01-abstract-keywords.md) | Abstract dan keywords. |
| [02-introduction.md](docs/artikel-uts-ieee/02-introduction.md) | Latar belakang, permasalahan, tujuan, dan kontribusi awal penelitian. |
| [03-related-works.md](docs/artikel-uts-ieee/03-related-works.md) | Sintesis penelitian terkait dengan sitasi IEEE. |
| [04-methodology.md](docs/artikel-uts-ieee/04-methodology.md) | Rancangan metodologi, dataset, target label, fitur, skenario model, dan knowledge-based risk layer. |
| [05-references.md](docs/artikel-uts-ieee/05-references.md) | Daftar referensi dalam gaya IEEE numerik. |
| [WRITING_RULES.md](docs/artikel-uts-ieee/WRITING_RULES.md) | Aturan penulisan yang wajib diikuti manusia maupun AI agent saat mengedit naskah. |
| [RESEARCH_DIRECTION.md](docs/artikel-uts-ieee/RESEARCH_DIRECTION.md) | Guardrail arah penelitian agar draft UTS, eksperimen lanjutan, dan artikel akhir tidak melenceng. |

### Arah penelitian yang dikunci

Artikel diarahkan sebagai **supervised binary classification** untuk deteksi risiko mahasiswa pada OULAD. Target utama tetap:

- `AtRisk` = `Withdrawn` + `Fail`
- `Successful` = `Pass` + `Distinction`

Model baseline untuk eksperimen lanjutan:

- Logistic Regression
- Random Forest
- XGBoost atau Gradient Boosting

Komponen knowledge-based yang disepakati adalah **rule-based risk layer** berbasis assessment, aktivitas VLE, dan sinyal unregistration. Dashboard dan clustering hanya diposisikan sebagai pengembangan lanjutan, bukan kontribusi utama artikel.

### Posisi DVBI dalam artikel

Karena mata kuliah berfokus pada **Data Visualization and Business Intelligence**, hasil model tidak boleh berhenti pada angka performa. Output penelitian harus diarahkan menjadi indikator monitoring dan decision support, misalnya:

- jumlah mahasiswa `AtRisk`;
- distribusi `High Risk`, `Medium Risk`, dan `Low Risk`;
- risiko per module-presentation;
- ringkasan aktivitas VLE rendah;
- ringkasan skor assessment rendah;
- daftar prioritas mahasiswa yang perlu monitoring akademik.

Dashboard penuh belum menjadi scope utama draft UTS. Untuk tahap akhir, dashboard dapat ditulis sebagai rancangan visual analytics atau implikasi BI, kecuali implementasinya benar-benar dibuat.

### Aturan penulisan yang wajib dijaga

Ringkasan aturan dari [`WRITING_RULES.md`](docs/artikel-uts-ieee/WRITING_RULES.md):

- level penomoran tidak boleh lebih dari 3 tingkat;
- paragraf harus mengalir naratif;
- sitasi memakai format IEEE dan urut sesuai kemunculan;
- struktur argumentasi mengikuti alur masalah, gap riset, solusi, kontribusi;
- jangan menggunakan tanda strip panjang pada naskah proposal, bahan seminar, atau hasil edit AI.

### Index dokumen `docs/`

| Judul dokumen | Deskripsi |
|---|---|
| [Draft Artikel UTS IEEE](docs/artikel-uts-ieee/) | Folder draft artikel UTS modular per section, termasuk writing rules dan research direction guardrail. |
| [Audit Dataset OULAD](docs/audit-dataset-oulad.md) | Audit sumber unduh, struktur tabel, distribusi label, missing values penting, dan verifikasi kelayakan OULAD terhadap syarat capstone. |
| [Preprocessing Plan OULAD: Binary Risk Framing](docs/preprocessing-plan-oulad-binary-risk.md) | Rencana preprocessing baseline OULAD, termasuk framing label `AtRisk` vs `Successful`, tabel sumber, fitur baseline, aturan preprocessing, dan command eksekusi. |
| [EDA Ringkas OULAD: Binary Risk Dataset](docs/eda-oulad-binary-risk.md) | Ringkasan EDA dari dataset turunan OULAD hasil preprocessing, mencakup ukuran data, distribusi label, distribusi `final_result`, dan statistik numerik utama. |
| [Kandidat Dataset untuk Capstone DVBI](docs/kandidat-dataset-capstone-dvbi.md) | Shortlist kandidat dataset yang dievaluasi untuk capstone, beserta alasan mengapa OULAD menjadi kandidat utama dibanding opsi lain. |
| [Catatan Arah Capstone DVBI](docs/catatan-arah-capstone-dvbi.md) | Catatan keputusan arah project, syarat capstone dari dosen, evaluasi dataset awal, dan implikasi metodologis sebelum masuk preprocessing. |
| [Ringkasan Dataset: Predict Students' Dropout and Academic Success](docs/ringkasan-dataset-uci-student-dropout.md) | Ringkasan dataset UCI yang sempat dipakai sebagai baseline pembanding, termasuk ukuran data, distribusi kelas, karakteristik fitur, dan keterbatasannya. |
| [Outline Slide: Student Performance / Dropout Analytics](docs/outline-presentasi-student-dropout-10-paper.md) | Outline presentasi literature review untuk topik student performance / dropout analytics dalam konteks DVBI. |

### Script data & preprocessing
- `scripts/download_oulad.py`: download dan extract dataset OULAD ke `data/oulad/`.
- `src/oulad_preprocessing.py`: builder dataset baseline OULAD.
- `scripts/build_oulad_binary_dataset.py`: runner untuk menghasilkan dataset turunan.
- `src/oulad_experiment.py`: pipeline eksperimen model dan knowledge-based risk layer.
- `scripts/run_oulad_experiment.py`: runner eksperimen Logistic Regression, Random Forest, dan XGBoost.
- `scripts/build_oulad_dashboard.py`: generator dashboard DVBI stakeholder.
- `src/oulad_eda.py`: helper untuk merangkum dataset turunan OULAD dan menghasilkan laporan markdown EDA.
- `scripts/run_oulad_eda.py`: runner untuk membuat `docs/eda-oulad-binary-risk.md`.
- `tests/test_oulad_preprocessing.py`: test otomatis untuk memverifikasi logika preprocessing baseline.
- `tests/test_oulad_eda.py`: test otomatis untuk memverifikasi ringkasan EDA dan generator laporan markdown.

### Framing awal yang dipakai
Framing baseline saat ini adalah:
- **binary risk classification**
- `AtRisk` = `Withdrawn` + `Fail`
- `Successful` = `Pass` + `Distinction`

### Output turunan
Script preprocessing menghasilkan file:
- `data/processed/oulad_binary_risk_dataset.csv`

File data mentah dan file hasil proses saat ini **di-ignore dari Git** agar repository tetap ringan; dokumentasi, script, dan test tetap dilacak dalam repository.

### Catatan download dataset
- Link sumber OULAD sudah dicatat di [Audit Dataset OULAD](docs/audit-dataset-oulad.md).
- Script download otomatis OULAD sudah tersedia di [`scripts/download_oulad.py`](scripts/download_oulad.py).
- Jalankan command berikut untuk download dan extract ulang dataset:

```bash
PYTHONPATH=. python3 scripts/download_oulad.py
```

---

## Catatan

Repository ini disusun sebagai workspace akademik untuk mendukung tugas perkuliahan. Isi repository dapat berkembang dari sekadar literature review menjadi dasar untuk analisis lanjutan, visualisasi data, dan prototipe BI sederhana jika dibutuhkan pada tahap berikutnya.
