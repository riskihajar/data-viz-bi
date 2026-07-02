# Research Direction Guardrail

Dokumen ini menjaga konsistensi antara notebook eksperimen, artikel IEEE, dashboard, dan bahan presentasi.

## Arah Utama

Penelitian menggunakan supervised binary classification untuk early warning risiko dropout mahasiswa pada akhir minggu keempat. Dataset utama adalah OULAD dengan target `AtRisk` dan `Successful`. `AtRisk` mencakup `Withdrawn` dan `Fail`, sedangkan `Successful` mencakup `Pass` dan `Distinction`.

Kontribusi penelitian adalah integrasi supervised learning, knowledge-based risk layer, dan visual decision support. Model menghasilkan probabilitas risiko, rule layer memberikan level dan alasan, sedangkan dashboard menerjemahkan hasil menjadi indikator monitoring serta prioritas intervensi.

## Batasan Metodologis

Metode utama tetap klasifikasi biner. Clustering, forecasting, dan regresi berada di luar ruang lingkup. Fitur prediktor hanya menggunakan informasi yang tersedia sampai hari ke-28. Status unregistration, hasil akhir, dan aktivitas setelah cut-off dikeluarkan dari fitur.

Logistic Regression, Random Forest, dan XGBoost menjadi algoritma pembanding. Pemilihan model menggunakan recall `AtRisk` pada 5-fold GroupKFold, dengan F1-score sebagai tie-breaker. Hold-out test digunakan untuk pelaporan performa akhir.

## Knowledge-Based Risk Layer

Threshold dihitung dari kuartil bawah data train-validation:

| Indikator | Threshold |
|---|---:|
| `assessment_score_mean` | `<= 0` |
| `assessment_count` | `<= 0` |
| `vle_total_clicks` | `<= 47` |
| `vle_active_days` | `<= 4` |

`High Risk` diberikan ketika model memprediksi `AtRisk` dan terdapat minimal dua sinyal. `Medium Risk` diberikan ketika model memprediksi `AtRisk` atau terdapat minimal dua sinyal. `Low Risk` diberikan pada kondisi lainnya.

## Output DVBI

Output utama meliputi evaluasi tiga model, model Random Forest terpilih, evaluasi knowledge layer, dashboard statis, dan daftar prioritas intervensi. Dashboard memuat KPI risiko, distribusi level, risiko per module-presentation, sinyal dominan, pola assessment dan VLE, confusion matrix, serta rekomendasi tindakan.

## Sumber Angka

Seluruh angka pada artikel, presentasi, dan dokumentasi harus berasal dari output terbaru `notebooks/oulad_early_warning_dvbi_colab.ipynb`. Laporan baseline seluruh semester digunakan sebagai catatan historis dan tidak menjadi sumber hasil penelitian final.
