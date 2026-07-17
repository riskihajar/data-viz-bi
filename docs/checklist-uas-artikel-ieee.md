# Checklist UAS Artikel IEEE

Sumber instruksi: `/Users/riskihajar/Downloads/UAS S2 PJJ Data Visualization and Business Intelligence GENAP 2025-2026.pdf`

Artefak yang diaudit:

- `docs/artikel-ieee/Artikel IEEE - Early Warning OULAD.pdf`
- `docs/artikel-ieee/Artikel IEEE - Early Warning OULAD.docx`
- `docs/artikel-ieee/IEEE Article - Early Warning OULAD.pdf`
- `docs/artikel-ieee/IEEE Article - Early Warning OULAD.docx`
- sumber Markdown pada `docs/artikel-ieee/`

Status menggunakan tiga kategori: `[x]` terpenuhi, `[~]` terpenuhi sebagian atau perlu konfirmasi, dan `[ ]` belum terpenuhi.

## A. Isi Final Draft

- [x] Title tersedia dan konsisten dengan target hasil akhir mata kuliah OULAD.
- [x] Author tersedia: Muhammad Rizky Hajar, Alwie Muflich, Heri Santosa, Andi Sunyoto, dan Robert Marco.
- [x] Affiliation setiap author memuat `Department of Computer Science` dan `Universitas Amikom Yogyakarta`.
- [x] Email tersedia untuk seluruh author.
- [x] Abstract tersedia.
- [x] Keywords tersedia.
- [x] Introduction tersedia.
- [x] Related Works tersedia.
- [x] Methodology tersedia.
- [x] Results and Discussion tersedia sebagai Section IV dengan pembahasan dan keterbatasan pada subsection G.
- [x] Conclusion tersedia.
- [x] References tersedia dan menggunakan penomoran IEEE.
- [x] Susunan `Results and Discussion` mengikuti struktur instruksi UAS.

## B. Kesesuaian Substansi

- [x] Topik berkaitan langsung dengan Data Visualization and Business Intelligence melalui supervised learning, knowledge-based risk layer, dashboard, visual analytics, dan decision support.
- [x] Penelitian menggunakan hasil eksperimen kelompok sendiri pada OULAD.
- [x] Target penelitian dijelaskan pada tingkat `student-module-presentation`: `AtRisk` untuk `Withdrawn` atau `Fail`, serta `Successful` untuk `Pass` atau `Distinction`.
- [x] Artikel memuat metode, hasil terukur, visualisasi, pembahasan, keterbatasan, dan implikasi Business Intelligence.
- [~] Klaim `ready submitted` memerlukan pemeriksaan akhir bahasa, template, similarity, dan paket file sebelum dapat dinyatakan terpenuhi.

## C. Author dan Afiliasi

- [x] Seluruh anggota kelompok dicantumkan sebagai author.
- [x] Kedua dosen pengampu dicantumkan sebagai author.
- [~] Urutan author mahasiswa harus dikonfirmasi sebagai urutan kontribusi: Muhammad Rizky Hajar, Alwie Muflich, lalu Heri Santosa.
- [x] Author dosen dicantumkan setelah anggota kelompok: Andi Sunyoto dan Robert Marco.
- [x] Nama afiliasi sesuai instruksi UAS.

## D. Format IEEE

- [x] PDF menggunakan halaman Letter, tata letak dua kolom, caption figure/table, sitasi numerik, dan daftar referensi bergaya IEEE.
- [x] Halaman judul memuat author block, affiliation, dan email.
- [x] DOCX menggunakan US Letter, margin conference IEEE (atas 0,75 inci, bawah 1 inci, kiri dan kanan 0,625 inci), dua kolom dengan jarak 0,25 inci, Times New Roman, body text 10 pt, title 24 pt, serta sitasi numerik.
- [x] `Results` dan `Discussion` telah digabung menjadi Section IV.
- [x] Seluruh tabel dan figure ditempatkan selebar satu kolom; pemeriksaan render enam halaman tidak menemukan clipping, overflow, atau section break penuh lebar.
- [~] Unduhan langsung template conference IEEE ditolak oleh server IEEE saat audit. Geometri dan style telah dicocokkan dengan spesifikasi conference IEEE; perbandingan langsung dengan file template resmi tetap dilakukan ketika template tersedia.

## E. Bahasa dan Similarity

- [x] Versi Bahasa Indonesia tersedia.
- [x] Versi English tersedia sebagai DOCX dan PDF terpisah dengan struktur, angka, sitasi, dan visual yang diselaraskan dengan versi Bahasa Indonesia.
- [x] Proofreading akademik versi Bahasa Indonesia telah dilakukan pada struktur, konsistensi istilah, angka, caption, dan alur pembahasan.
- [x] Proofreading awal versi English telah dilakukan pada struktur, konsistensi istilah, angka, caption, dan alur pembahasan.
- [ ] Similarity versi Bahasa Indonesia < 20% belum memiliki laporan Turnitin.
- [ ] Similarity versi English < 20% belum memiliki laporan Turnitin.
- [ ] Parafrasa dan sitasi perlu diperbaiki apabila salah satu hasil Turnitin mencapai 20% atau lebih.

## F. Jumlah Halaman

- [x] Artikel Bahasa Indonesia berjumlah 6 halaman pada US Letter.
- [x] Pemadatan mempertahankan metrik model, confusion matrix, feature importance, benchmark OULAD, knowledge-based risk layer, dan dashboard.
- [x] Versi English berjumlah 6 halaman dengan struktur dan isi yang sama.
- [~] Instruksi meminta satu PDF gabungan Bahasa Indonesia dan English. Interpretasi paling aman adalah 5-6 halaman per versi, sehingga PDF gabungan berjumlah sekitar 10-12 halaman. Konfirmasi kepada dosen diperlukan apabila batas 5-6 halaman dimaksudkan untuk seluruh file gabungan.

Strategi layout yang telah diterapkan:

1. `Results` dan `Discussion` berada dalam satu section.
2. Benchmark OULAD dan knowledge-layer comparison diringkas dengan konteks horizon, target, dan metrik tetap tersedia.
3. Setiap tabel dan figure berada dalam satu kolom agar aliran layout dua kolom tetap konsisten.
4. Gambar evaluasi dipisahkan menjadi perbandingan metrik, confusion matrix, dan kurva ROC agar setiap panel terbaca pada lebar kolom.

## G. Referensi

- [x] Seluruh 16 judul referensi ditulis dalam English.
- [x] Seluruh referensi berasal dari jurnal dan memiliki DOI.
- [~] Daftar memuat jurnal bereputasi yang lazim terindeks Scopus, termasuk `Scientific Reports`, `Scientific Data`, `IEEE Access`, dan `Applied Intelligence`. Bukti indeks serta quartile harus dicatat berdasarkan tahun publikasi atau tahun penilaian yang digunakan.
- [ ] Buat tabel verifikasi referensi berisi nomor referensi, jurnal, status Scopus, quartile, tahun quartile, dan URL bukti.
- [x] Referensi `[1]` sampai `[16]` seluruhnya muncul di badan artikel dan terdeteksi pada PDF hasil render.

Referensi utama yang dapat dipakai saat presentasi:

1. Kuzilek et al. `[4]` sebagai sumber resmi dataset OULAD.
2. Shou et al. `[5]` sebagai benchmark early prediction berbasis OULAD.
3. Alnasyan et al. `[9]` sebagai benchmark terbaru dengan target biner yang sama.

## H. Status Publikasi

- [ ] Seluruh author perlu menyatakan bahwa naskah belum tersubmit ke penerbit tertentu.
- [ ] Pastikan tidak ada submission aktif, manuscript ID, atau perjanjian eksklusif dengan penerbit.

## I. Dua File Pengumpulan

- [ ] File 1: satu PDF final gabungan versi Bahasa Indonesia dan English. Penggabungan ditunda sampai kedua versi disetujui.
- [ ] Susunan File 1 ditetapkan konsisten, disarankan Bahasa Indonesia terlebih dahulu lalu English.
- [ ] File 1 diperiksa: bookmark atau pemisah versi jelas, halaman lengkap, figure tajam, dan tidak ada halaman kosong yang tidak disengaja.
- [ ] File 2: satu PDF gabungan hasil Turnitin versi Bahasa Indonesia dan English.
- [ ] File 2 memperlihatkan identitas dokumen dan similarity masing-masing versi dengan nilai di bawah 20%.
- [ ] Nama kedua file dibuat jelas dan konsisten dengan nama kelompok atau judul singkat penelitian.

## J. Pengumpulan Waskita

- [ ] Jadwal dan batas waktu dari Admisi dikonfirmasi; instruksi menyebut pukul 23:59 WIB.
- [ ] Setiap anggota kelompok mengunggah dua file yang sama ke Waskita.
- [ ] File yang diunggah dibuka kembali untuk memastikan tidak rusak dan merupakan revisi final.
- [ ] Bukti pengumpulan disimpan oleh setiap anggota.

## Ringkasan Kesiapan

Artikel Bahasa Indonesia dan English masing-masing telah memiliki substansi penelitian, struktur ilmiah, author, affiliation, visualisasi, referensi, dan layout IEEE dua kolom sepanjang 6 halaman. Keduanya tersedia sebagai output terpisah. Tahap berikutnya adalah review kelompok, pemeriksaan Turnitin di bawah 20% untuk setiap bahasa, lalu penggabungan artikel dan laporan Turnitin sesuai instruksi pengumpulan.
