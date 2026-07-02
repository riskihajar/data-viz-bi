# VI. Conclusion

Penelitian ini mengembangkan sistem peringatan dini risiko dropout mahasiswa pada akhir minggu keempat menggunakan OULAD. Dataset dibentuk pada unit student-module-presentation dengan fitur demografis, registrasi awal, assessment, dan aktivitas VLE sampai hari ke-28. Pemisahan berbasis `id_student` menjaga independensi mahasiswa antara data latih-validasi dan data uji hold-out.

Random Forest dipilih berdasarkan recall `AtRisk` cross-validation tertinggi sebesar 0,7126. Pada data uji hold-out, model menghasilkan accuracy 0,7592, precision 0,8032, recall 0,7172, F1-score 0,7578, dan ROC-AUC 0,8396. Lapisan risiko berbasis aturan meningkatkan recall menjadi 0,7849 dengan menggabungkan prediksi model dan empat sinyal perilaku awal. Sistem menghasilkan level risiko, alasan, dan rekomendasi yang dapat disusun menjadi antrean intervensi.

Dashboard Business Intelligence menyajikan distribusi risiko, prioritas module-presentation, sinyal dominan, performa model, dan daftar mahasiswa anonim untuk monitoring. Integrasi supervised learning, lapisan risiko berbasis aturan, dan visual analytics menghasilkan dasar pendukung keputusan yang menghubungkan prediksi dengan proses tindak lanjut akademik.

Pengembangan berikutnya dapat membandingkan horizon minggu keempat, kedelapan, dan kedua belas; menggunakan ambang per module-presentation; melakukan tuning hyperparameter; serta menguji validitas eksternal pada data institusi lain. Evaluasi dampak intervensi juga diperlukan untuk mengukur kontribusi sistem terhadap keberlanjutan studi mahasiswa.
