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

### 1. `student-dropout-analytics-10-paper.xlsx`
Berisi daftar **10 paper kandidat** yang relevan dengan topik student performance / dropout analytics, lengkap dengan metadata utama seperti:
- publisher,
- topics,
- tahun,
- penulis,
- judul,
- DOI,
- link.

### 2. `matriks-literature-review-student-dropout-10-paper.xlsx`
Berisi matriks ringkasan paper dalam format:
- **No**
- **Paper**
- **Fokus**
- **Variabel**
- **Metode**
- **Temuan**
- **Gap/Keterbatasan**

Matriks ini digunakan untuk memudahkan proses sintesis literature review dan penarikan research gap.

### 3. `papers-pdf/`
Berisi arsip PDF paper yang sudah dikumpulkan dan divalidasi terhadap daftar paper target. File dinamai menggunakan pola nomor urut agar mudah dicocokkan dengan matriks dan daftar referensi.

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
