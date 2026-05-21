# Research Direction Guardrail

Dokumen ini mengunci arah penelitian agar draft UTS, eksperimen lanjutan, dan artikel akhir tetap berada pada jalur yang sama.

## Arah Utama

Penelitian diarahkan sebagai supervised binary classification untuk mendeteksi risiko mahasiswa pada Open University Learning Analytics Dataset (OULAD). Target utama tetap `AtRisk` dan `Successful`, dengan definisi `AtRisk` sebagai gabungan `Withdrawn` dan `Fail`, sedangkan `Successful` sebagai gabungan `Pass` dan `Distinction`.

Kontribusi akhir yang perlu dijaga adalah integrasi model supervised learning dengan knowledge-based risk layer. Model machine learning digunakan untuk melakukan prediksi, sedangkan rule layer digunakan untuk memberi interpretasi risiko yang lebih mudah dipahami dalam konteks early warning dan Business Intelligence. Output analitik harus dapat diterjemahkan menjadi indikator monitoring akademik, bukan hanya berhenti pada metrik model.

## Batasan Agar Tidak Melenceng

Metode utama tidak boleh berubah menjadi clustering, forecasting, atau regresi. Clustering atau dashboard boleh disebut sebagai pengembangan lanjutan, tetapi bukan kontribusi utama artikel ini.

Dataset utama tetap OULAD. Dataset UCI dapat disebut sebagai pembanding historis dalam catatan proyek, tetapi tidak menjadi dataset eksperimen utama.

Model baseline yang dipertahankan untuk tahap eksperimen adalah Logistic Regression, Random Forest, dan XGBoost atau Gradient Boosting. Jika salah satu model tidak tersedia pada environment eksperimen, pengganti yang paling dekat adalah Gradient Boosting berbasis scikit-learn.

## Rule Layer yang Dikunci

Knowledge-based risk layer menggunakan indikator dari assessment, aktivitas VLE, dan sinyal unregistration. Threshold awal berbasis kuartil dataset hasil preprocessing:

| Indikator | Threshold awal | Makna risiko |
|---|---:|---|
| `assessment_score_mean` | `< 50.29` | skor assessment berada di kuartil bawah |
| `assessment_count` | `< 2` | partisipasi assessment sangat rendah |
| `vle_total_clicks` | `< 142` | total aktivitas VLE berada di kuartil bawah |
| `vle_active_days` | `< 11` | hari aktif VLE berada di kuartil bawah |
| `has_unregistration` | `= 1` | terdapat sinyal unregistration |

Status `High Risk` diberikan ketika mahasiswa memiliki sinyal unregistration dan minimal dua indikator akademik atau VLE berada pada kondisi risiko. Status `Medium Risk` diberikan ketika mahasiswa memiliki dua indikator risiko tanpa sinyal unregistration, atau satu indikator risiko dengan sinyal unregistration. Status `Low Risk` diberikan ketika kondisi tersebut tidak terpenuhi.

## Rencana Output DVBI

Output model dan rule layer perlu diarahkan menjadi indikator visual analytics. Indikator utama yang disarankan adalah jumlah mahasiswa `AtRisk`, distribusi `High Risk`, `Medium Risk`, dan `Low Risk`, risiko per module-presentation, aktivitas VLE rendah, skor assessment rendah, dan daftar prioritas mahasiswa yang perlu monitoring akademik.

Dashboard tidak menjadi scope utama draft UTS. Untuk artikel akhir, dashboard dapat diposisikan sebagai rancangan atau implikasi decision support, kecuali implementasinya benar-benar dibuat. Dengan batasan ini, artikel tetap konsisten sebagai penelitian supervised learning dengan interpretasi knowledge-based dalam konteks DVBI.

## Catatan Teknis untuk Eksperimen Akhir

Pipeline baseline saat ini sudah cukup untuk draft UTS, tetapi eksperimen akhir sebaiknya memperbaiki agregasi assessment. Agregasi `studentAssessment` perlu dihubungkan ke `assessments.csv` agar skor assessment dapat dihitung pada unit `code_module`, `code_presentation`, dan `id_student`. Hal ini menjaga konsistensi dengan unit analisis utama, yaitu satu mahasiswa pada satu module-presentation.

Hasil akhir artikel sebaiknya menambahkan bagian Results, Discussion, dan Conclusion setelah eksperimen dilakukan. Bagian Results harus membandingkan performa minimal tiga model, sedangkan Discussion harus menjelaskan kelebihan dan kekurangan model machine learning serta knowledge-based layer.
