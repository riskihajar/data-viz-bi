# Data Visualization and Business Intelligence — Student Performance / Dropout Analytics

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

- **literature-review/**  
  Folder utama yang berisi hasil pencarian paper, matriks literature review, dan arsip PDF referensi.

---

## Isi Folder `literature-review`

### Ringkasan file utama

| File / Folder | Deskripsi | Isi utama | Kegunaan |
|---|---|---|---|
| `student-dropout-analytics-10-paper.xlsx` | Daftar 10 paper kandidat | NO, Publisher, Topics, Tahun, Penulis, Judul, DOI, LINK | Basis awal seleksi paper |
| `matriks-literature-review-student-dropout-10-paper.xlsx` | Matriks sintesis 10 paper | Paper, Fokus, Variabel, Metode, Temuan, Gap/Keterbatasan | Membantu analisis perbandingan dan penarikan gap |
| `papers-pdf/` | Arsip PDF paper yang sudah divalidasi | 10 PDF + file ekstraksi teks pendukung | Referensi utama untuk membaca paper secara langsung |

### Daftar 10 paper kandidat

| No | Tahun | Paper | Fokus singkat |
|---|---:|---|---|
| 1 | 2023 | Using machine learning to predict student retention from socio-demographic characteristics and app-based engagement metrics | Prediksi retensi/dropout dari data sosiodemografis dan engagement |
| 2 | 2024 | Hybrid Approach to Predicting Learning Success Based on Digital Educational History for Timely Identification of At-Risk Students | Prediksi learning success dan identifikasi mahasiswa berisiko |
| 3 | 2022 | Early warning systems for more effective student counselling in higher education: Evidence from a Dutch field experiment | Evaluasi early warning system untuk counselling mahasiswa |
| 4 | 2024 | Enhancing the Early Student Dropout Prediction Model Through Clustering Analysis of Students’ Digital Traces | Clustering digital traces LMS untuk prediksi dropout |
| 5 | 2025 | Predicting Student Dropout from Day One: XGBoost-Based Early Warning System Using Pre-Enrollment Data | Early warning berbasis data pra-enrollment |
| 6 | 2022 | Assisting Educational Analytics with AutoML Functionalities | AutoML untuk educational analytics dan prediksi performa |
| 7 | 2020 | Precision education with statistical learning and deep learning: a case study in Taiwan | Prediksi dropout dan intervensi dini berbasis big data |
| 8 | 2023 | Multi-Class Phased Prediction of Academic Performance and Dropout in Higher Education | Prediksi performa/dropout multi-fase pada tahun pertama |
| 9 | 2024 | Study regarding the influence of a student’s personality and an LMS usage profile on learning performance using machine learning techniques | Pengaruh personality dan LMS usage terhadap performa belajar |
| 10 | 2025 | Crossing individual university boundaries: a comprehensive approach to predicting dropouts in the higher education system | Prediksi dropout lintas universitas pada level sistem |

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
- struktur awal untuk pengembangan draft tugas.

Tahap berikutnya yang dapat dikembangkan dari repository ini meliputi:

- seleksi **6 paper final** untuk literature review utama,
- penyusunan narasi LR berdasarkan paper terpilih,
- penarikan **research gap** secara lebih formal,
- pencarian dataset publik pendukung,
- pengembangan ide dashboard / visual analytics.

---

## Catatan

Repository ini disusun sebagai workspace akademik untuk mendukung tugas perkuliahan. Isi repository dapat berkembang dari sekadar literature review menjadi dasar untuk analisis lanjutan, visualisasi data, dan prototipe BI sederhana jika dibutuhkan pada tahap berikutnya.
