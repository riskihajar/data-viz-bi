# V. Conclusion

Penelitian ini mengembangkan early warning risiko gagal atau mengundurkan diri dari mata kuliah pada akhir minggu keempat menggunakan OULAD. Dataset dibentuk pada unit student-module-presentation dengan fitur demografis, registrasi awal, assessment, dan aktivitas VLE sampai hari ke-28. Pemisahan berbasis `id_student` menjaga independensi mahasiswa antara train-validation dan hold-out test.

Random Forest dipilih berdasarkan recall `AtRisk` cross-validation tertinggi sebesar 0,7107. Pada hold-out test, model menghasilkan accuracy 0,7594, precision 0,8007, recall 0,7213, F1-score 0,7589, dan ROC-AUC 0,8396. Knowledge-based risk layer meningkatkan recall menjadi 0,7866 dengan menggabungkan prediksi model dan empat sinyal perilaku awal. Sistem menghasilkan level risiko, alasan, dan rekomendasi yang dapat diterjemahkan menjadi antrean intervensi.

Dashboard Business Intelligence menyajikan distribusi risiko, prioritas module-presentation, sinyal dominan, performa model, dan daftar mahasiswa anonim untuk monitoring. Integrasi supervised learning, knowledge-based risk layer, dan visual analytics menghasilkan decision support yang menghubungkan prediksi dengan proses tindak lanjut akademik.

Pengembangan berikutnya dapat membandingkan horizon minggu keempat, kedelapan, dan kedua belas; menggunakan threshold per module-presentation; melakukan tuning hyperparameter; serta menguji validitas eksternal pada data institusi lain. Evaluasi dampak intervensi juga diperlukan untuk mengukur kontribusi sistem terhadap keberhasilan mahasiswa menyelesaikan mata kuliah.
