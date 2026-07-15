## G. Discussion and Limitations

Hasil eksperimen memperlihatkan hubungan antara tujuan keputusan dan model selection. XGBoost unggul pada accuracy dan ROC-AUC, sementara Random Forest memperoleh recall `AtRisk` tertinggi pada cross-validation dan hold-out test. Performa sekitar 0,76 merepresentasikan skenario awal yang hanya menggunakan informasi sampai hari ke-28. Horizon ini menyediakan waktu intervensi lebih panjang sekaligus membatasi jumlah bukti perilaku yang tersedia bagi model.

Threshold assessment sebesar nol menunjukkan bahwa sebagian module-presentation belum memiliki submission sampai minggu keempat. Pengembangan berikutnya dapat menggunakan threshold per module-presentation atau menyesuaikan cut-off dengan jadwal assessment. Knowledge layer memperluas recall sebesar 0,0653 poin dan menghasilkan alasan operasional seperti aktivitas VLE rendah atau assessment yang belum dikerjakan. Alasan tersebut menjadi bahan verifikasi bersama informasi kontekstual dari dosen dan tutor.

Dashboard memperluas fungsi model menjadi Business Intelligence melalui agregasi risiko, perbandingan module-presentation, dan antrean mahasiswa. Temuan 100% prioritas pada GGG 2014J menjadi sinyal untuk meninjau ukuran kelompok, jadwal assessment, serta karakteristik modul sebelum menentukan tindakan.

Keterbatasan penelitian mencakup konteks OULAD di Open University Inggris, fitur perilaku yang masih berupa agregat, konfigurasi model baseline, dan threshold kuartil yang memerlukan validasi pakar. Evaluasi mengukur performa deteksi, sedangkan dampak intervensi terhadap keberhasilan mata kuliah memerlukan penelitian lanjutan dengan data institusi dan desain evaluasi intervensi.
