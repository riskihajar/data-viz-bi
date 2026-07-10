# Audit Gaya Pertanyaan Dosen dan Rencana Penguatan Notebook OULAD

Dokumen ini adalah bahan latihan presentasi dan backlog perbaikan untuk notebook `notebooks/oulad_early_warning_dvbi_colab.ipynb`. Tujuannya bukan menambah klaim baru, melainkan memastikan setiap klaim pada notebook dapat ditelusuri ke data, proses, dan outputnya.

## Sumber dan batas pembacaan

Sumber utama: rekaman [Data Visualization and Business Intelligence - BI1](https://www.youtube.com/watch?v=tpZ8UTIaOA4), diakses 10 Juli 2026. Timestamp di bawah merujuk pada subtitle otomatis bahasa Indonesia, sehingga istilah yang salah dikenali suara ditulis ulang secara teknis bila maknanya jelas.

Rekaman berisi beberapa kelompok dengan topik berbeda. Yang diambil adalah pola pertanyaan dan arahan dosen, bukan isi atau kesimpulan proyek kelompok lain.

## Arah dan gaya pertanyaan dosen

| Pola yang teramati | Bukti rekaman | Makna praktis untuk presentasi |
|---|---|---|
| Mulai dari angka/objek yang baru ditampilkan, lalu menanyakan konsistensinya. | 00:37:34-00:38:14: dosen menanyakan mengapa kelas prediksi dua, tetapi tampilan risiko menjadi tiga. | Jangan hanya menyebut hasil. Tunjukkan hubungan input -> model -> output dan nyatakan mana yang merupakan kelas model, mana yang merupakan kategori operasional. |
| Memeriksa arti probabilitas, *confidence score*, dan keputusan kelas. | 00:45:48-00:47:34: dosen meminta memastikan nilai yang dipakai dan menyandingkannya dengan keputusan kelas. | Sebutkan dengan presisi `P(AtRisk)`, kelas hasil `predict`, threshold keputusan, serta fungsi probabilitas dalam prioritas. Jangan menyamakan probabilitas dengan kepastian atau memakai istilah confidence tanpa definisi. |
| Meminta presenter mengingat proses preprocessing dan rasio kelas, bukan hanya membacakan slide. | 00:47:44-00:48:36: dosen bertanya preprocessing apa saja dan proses untuk kelas tidak seimbang. | Setiap anggota harus hafal: sumber data, unit analisis, kelas dan rasionya, missing-value treatment, encoding, scaling, serta alasan tidak/ya melakukan balancing. |
| Menguji urutan split, validasi, dan test set. | 01:57:55-02:00:11: dosen menelusuri posisi 5-fold CV setelah split 80:20 dan membedakan validation fold dengan hold-out test. | Jelaskan alur secara berurutan dan gunakan istilah yang konsisten: 80% `train-validation`, 20% `hold-out test`; lima fold hanya di 80%; test disentuh sekali setelah seleksi model. |
| Memeriksa konsistensi antara preprocessing, metrik, dan simpulan. | 02:04:55-02:06:23: dosen mengoreksi alasan memakai F1 untuk data tidak seimbang setelah kelompok menerapkan SMOTE. | Semua narasi harus menyebut data pada tahap yang tepat. Jangan menjadikan alasan sebelum transformasi sebagai alasan metrik/evaluasi sesudah transformasi tanpa penjelasan. |
| Meminta dasar pilihan metode dari bentuk masalah/data. | 02:08:16-02:08:49: dosen menegaskan klasifikasi harus dijelaskan dari label kategorikal. | Jawab dengan rantai: target akhir kategorikal -> target dibentuk biner -> tugasnya supervised binary classification -> model pembanding dipilih untuk tujuan tersebut. |
| Meminta perbandingan yang adil dengan penelitian sebelumnya. | 02:06:25-02:07:35: dosen meminta metrik yang digunakan penelitian lain ditampilkan agar pembandingan setara; nilai yang tidak dilaporkan dibiarkan kosong. | Jangan menyatakan model lebih baik hanya karena satu angka. Tampilkan metrik yang sebanding dan batasinya: dataset, target, horizon minggu ke-4, dan split dapat berbeda. |
| Mengarahkan feature importance sebagai bukti yang perlu diperiksa, bukan hiasan. | 02:07:39-02:08:13: dosen menanyakan feature selection dan mengarahkan penggunaan feature importance Random Forest. | Tampilkan fitur penting, tetapi jawab bahwa ini kontribusi prediktif/asosiasi, bukan sebab-akibat. Kaitkan dengan alasan pada antrean intervensi. |

### Ringkasan gaya jawab yang diharapkan

Dosen cenderung melakukan *drill-down*: meminta satu angka atau istilah di slide, menanyakan asalnya, lalu menelusuri apakah keputusan setelahnya konsisten. Format jawaban yang aman adalah: **definisi singkat -> lokasi/proses pembentukannya -> angka atau output yang terlihat -> konsekuensi dan batasan**. Bila angka belum terlihat, buka cell/output terkait, jangan menebak.

## Audit notebook saat ini

| Area yang kemungkinan diuji | Bukti yang sudah ada di notebook | Status | Risiko saat presentasi | Penyesuaian yang diperlukan |
|---|---|---|---|---|
| Mengapa klasifikasi? | Markdown pembuka dan bagian 4 menetapkan `AtRisk` vs `Successful`; `risk_label` dipetakan ke 0/1. | Kuat | Presenter dapat terjebak menyebut level High/Medium/Low sebagai kelas model. | Tegaskan diagram dua tahap dan gunakan istilah yang sama pada narasi, dashboard, dan jawaban. |
| Target dan anti-leakage | Bagian 4-5 menjelaskan `final_result` hanya label dan `date_unregistration` dikeluarkan; fitur dibatasi hari ke-28. | Kuat | Dosen dapat bertanya kapan setiap fitur tersedia. | Tambahkan satu tabel ringkas: kolom, tersedia sebelum hari ke-28?, dipakai sebagai fitur/label/grup, alasan. |
| Preprocessing | Bagian 6 dan 8 menjelaskan missing value, median imputation, one-hot encoding, scaling, dan pipeline. | Kuat | Terlalu tersebar; anggota bisa tidak hafal urutannya. | Tambahkan cell Markdown "Checklist preprocessing" tepat sebelum pipeline. |
| Distribusi kelas dan balancing | EDA mencetak distribusi kelas; model memakai `class_weight='balanced'`/`scale_pos_weight`; tidak ada SMOTE. | Cukup | Harus mampu membedakan *class weighting* dari resampling dan menjelaskan mengapa tidak memakai SMOTE. | Tambahkan rasio aktual train/test, alasan keputusan, dan pernyataan bahwa rebalancing hanya dipelajari dari train/fold bila kelak diuji. |
| Split dan validasi | Bagian 7, 9, dan kode memakai `GroupShuffleSplit` 80:20 lalu `GroupKFold(5)` hanya pada train; assert overlap nol. | Kuat secara teknis | Paling rawan salah ucap: fold validation disebut test atau hold-out dipakai memilih model. | Tambahkan diagram alur dan tampilkan `80% -> 5 fold` serta `20% -> sekali di akhir`. |
| Pemilihan model | CV diringkas berdasarkan recall lalu F1; test disimpan untuk generalisasi akhir. | Kuat | Narasi dapat keliru karena tabel test juga diurutkan berdasarkan recall. | Ubah teks penjelas tabel menjadi eksplisit: urutan test hanya tampilan; `best_model_name` berasal dari `cv_summary`, bukan test. |
| Probabilitas vs prediksi kelas | Kode menyimpan `predicted_atrisk = predict(...)` dan `probability_atrisk = predict_proba(...)[:, 1]`. | Ada, tetapi perlu dipertegas | Dashboard dan tabel mengandung probabilitas tanpa menyatakan kelas positif/threshold. | Tambahkan Markdown definisi `P(AtRisk)`, kelas positif = 1, dan `predict` menggunakan threshold bawaan estimator (umumnya 0,5); jangan menyebutnya calibrated confidence. |
| Knowledge layer | Bagian 13 dan fungsi `add_knowledge_layer` membedakan klasifikasi biner dari grouping rule-based; aturan High/Medium/Low eksplisit. | Cukup kuat | Dosen dapat bertanya mengapa 2 kelas menjadi 3 level dan apakah ini clustering. | Tambahkan flow diagram dan tabel contoh satu baris: prediksi ML, probabilitas, jumlah sinyal, rule yang aktif, dan level akhir. |
| Evaluasi knowledge layer | Bagian 14 membandingkan model murni dengan High+Medium sebagai `AtRisk`, termasuk confusion matrix. | Kuat | Perlu menjelaskan bahwa evaluasi gabungan mengubah definisi alarm, sehingga recall/precision berubah. | Beri judul grafik yang lebih eksplisit: "Alarm intervensi (High atau Medium) vs label AtRisk" dan tambahkan satu kalimat trade-off. |
| Feature importance dan rekomendasi | Bagian 12 menunjukkan importance; bagian 13/16 memberi alasan dan rekomendasi. | Cukup | Mudah disalahartikan sebagai penyebab dropout. | Tambahkan disclaimer tepat di bawah grafik: importance adalah asosiasi prediktif global; alasan per mahasiswa berasal dari rule layer, bukan penjelasan kausal. |
| Benchmark paper terdahulu | Bagian 10 sudah memiliki benchmark dan catatan perbedaan dataset/horizon/target. | Cukup | Klaim "lebih baik" dapat melampaui bukti. | Tambahkan kolom kompatibilitas: target, horizon, split, dan metrik; gunakan kata "konteks benchmark", bukan ranking langsung. |

## Naskah jawaban inti yang wajib dikuasai

### Mengapa dua kelas, tetapi dashboard memiliki tiga level risiko?

Model melakukan klasifikasi biner: `Successful` = 0 dan `AtRisk` = 1. Sesudah model menghasilkan prediksi, probabilitas `P(AtRisk)`, dan empat sinyal perilaku awal, knowledge layer mengubahnya menjadi prioritas operasional `High`, `Medium`, atau `Low Risk`. Jadi tiga level bukan kelas baru dari model dan bukan clustering; itu aturan tindak lanjut. Untuk evaluasi alarm, `High` dan `Medium` sementara dipetakan kembali menjadi `AtRisk`, lalu precision dan recall dibandingkan dengan model murni.

### Apa tepatnya arti `probability_atrisk`?

Nilai tersebut adalah keluaran `predict_proba(... )[:, 1]`, yaitu probabilitas kelas positif `AtRisk` dari model final. Prediksi biner berasal dari `predict`; pada konfigurasi saat ini tidak ada threshold keputusan khusus yang dituning, sehingga keputusan mengikuti threshold bawaan estimator. Probabilitas dipakai untuk mengurutkan prioritas, sedangkan level risiko ditentukan bersama prediksi dan rule sinyal perilaku. Nilai itu belum dikalibrasi khusus, sehingga sebutannya probabilitas risiko model, bukan kepastian atau *calibrated confidence*.

### Bagaimana pembagian 80:20 dan 5-fold berjalan?

Unit analisis adalah student-module-presentation, sementara satu mahasiswa dapat muncul lebih dari sekali. Pertama, `GroupShuffleSplit` membagi mahasiswa: 80% train-validation dan 20% hold-out test, dengan overlap `id_student` harus nol. Kedua, hanya 80% train-validation dibagi lagi oleh `GroupKFold` menjadi lima putaran; di setiap putaran sekitar empat fold melatih dan satu fold memvalidasi model. Rata-rata dan standar deviasi lima validasi memilih model berdasarkan recall `AtRisk`, dengan F1 sebagai tie-breaker. Setelah itu model terpilih dilatih pada seluruh 80% dan diuji sekali pada 20% hold-out. Hold-out tidak menentukan pemenang model.

### Mengapa memilih recall AtRisk, bukan accuracy tertinggi?

Tujuan early warning adalah meminimalkan mahasiswa berisiko yang terlewat, yaitu false negative. Recall `AtRisk` mengukur cakupan deteksi tersebut. Precision, F1, confusion matrix, dan ROC-AUC tetap dilaporkan agar beban false positive dan performa umum tetap terlihat. Dataset cukup dekat seimbang, tetapi class weight diterapkan pada model yang mendukungnya; ini berbeda dengan SMOTE dan tidak mengubah baris data menjadi sintetis.

## Rencana penyesuaian notebook

Urutan ini mengikuti risiko terbesar berdasarkan rekaman. Statusnya adalah backlog; belum berarti perubahan telah dilakukan.

1. **Prioritas 1 - Tambahkan cell Markdown "Peta keputusan" sebelum EDA.** Isi: target akhir -> fitur sampai hari ke-28 -> klasifikasi `AtRisk`/`Successful` -> `P(AtRisk)` dan prediksi -> knowledge rules -> High/Medium/Low -> antrean intervensi. Tambahkan kalimat tegas: tiga level bukan hasil clustering.

2. **Prioritas 1 - Tambahkan cell Markdown dan diagram teks split/evaluasi sebelum bagian split.** Tampilkan `data -> 80% train-validation -> GroupKFold 5 -> pilih model`, serta `20% hold-out -> evaluasi final sekali`. Cantumkan pengelompokan dengan `id_student` dan overlap nol.

3. **Prioritas 1 - Perjelas cell probabilitas dan knowledge layer.** Dokumentasikan kelas positif `AtRisk=1`, sumber `predict_proba[:, 1]`, fungsi `predict`, dan bahwa threshold kuartil hanya untuk sinyal aturan. Ubah semua kata "confidence" menjadi "probabilitas risiko model" kecuali saat menjelaskan perbedaan istilah.

4. **Prioritas 2 - Tambahkan checklist preprocessing dan keputusan ketidakseimbangan kelas.** Satu tabel ringkas berisi missing value, encoding, scaling, class weight, dan keputusan tidak memakai SMOTE. Angka distribusi aktual harus ditarik dari output runtime, bukan diketik manual.

5. **Prioritas 2 - Perkuat auditability output.** Tampilkan satu contoh mahasiswa anonim yang memperlihatkan `predicted_atrisk`, `probability_atrisk`, empat sinyal, `risk_signal_count`, level, dan rekomendasi. Ini menjawab pertanyaan "mengapa sistem menandainya?" tanpa mengklaim kausalitas.

6. **Prioritas 2 - Perbaiki label visual.** Judul grafik knowledge layer harus menyebut definisi alarm `High + Medium`; grafik probability menyebut `P(AtRisk)`, bukan confidence. Letakkan disclaimer feature importance tepat di bawah grafiknya.

7. **Prioritas 3 - Rapikan benchmark paper.** Tampilkan metrik yang sama bila tersedia dan `-` bila tidak tersedia. Tambahkan konteks target, horizon, serta desain evaluasi agar tidak menyiratkan perbandingan apple-to-apple ketika desainnya berbeda.

8. **Prioritas 3 - Latihan tanya jawab berbasis layar.** Bagi peran: satu orang membuka cell target/split/preprocessing, satu orang menjelaskan model dan metrik, satu orang menjelaskan dashboard dan batasan. Latihan harus menggunakan angka yang muncul saat runtime, bukan hafalan angka dari dokumen.

## Kriteria selesai sebelum presentasi

- Setiap anggota dapat menjelaskan alur 80:20 lalu 5-fold tanpa menyebut validation sebagai hold-out test.
- Di notebook terlihat perbedaan antara dua kelas model dan tiga level prioritas, termasuk definisi `P(AtRisk)`.
- Ada bukti visual untuk preprocessing, rasio kelas, anti-leakage, overlap grup nol, dan trade-off precision-recall.
- Setiap perbandingan paper menyebut keterbatasan kesetaraan dataset, target, horizon, dan metrik.
- Tidak ada klaim kausal dari feature importance atau probability.
