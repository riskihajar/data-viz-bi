# IV. Results and Discussion

## A. Dataset and Validation Results

The preprocessed dataset contains 32,593 student-module-presentations from 28,785 unique students. The `AtRisk` class contains 17,208 rows and the `Successful` class contains 15,385 rows. The train-validation set contains 26,122 rows, while the hold-out test contains 6,471 rows with 3,398 `AtRisk` and 3,073 `Successful` cases. The `id_student`-based split produces zero student overlap. Missing values occur mainly in `imd_band` and in a small proportion of `date_registration`; both are handled within the pipeline using the training data in each fold.

## B. Cross-Validation Performance

Table I presents the 5-fold GroupKFold results. Random Forest achieves the highest mean `AtRisk` recall at 0.7107 and is selected as the final model according to the selection criterion. XGBoost achieves the highest accuracy, F1-score, and ROC-AUC at 0.7584, 0.7522, and 0.8440, respectively.

**Table I. 5-Fold GroupKFold Results on the Train-Validation Set**

| Metric | Logistic Regression | Random Forest | XGBoost |
|---|---:|---:|---:|
| Accuracy | 0.7496 ± 0.0039 | 0.7524 ± 0.0013 | **0.7584 ± 0.0024** |
| AtRisk Precision | 0.8090 ± 0.0059 | 0.7989 ± 0.0136 | **0.8215 ± 0.0096** |
| AtRisk Recall | 0.6889 ± 0.0064 | **0.7107 ± 0.0085** | 0.6938 ± 0.0029 |
| AtRisk F1 | 0.7442 ± 0.0059 | 0.7521 ± 0.0030 | **0.7522 ± 0.0039** |
| ROC-AUC | 0.8330 ± 0.0027 | 0.8362 ± 0.0023 | **0.8440 ± 0.0019** |

## C. Hold-Out Test Performance

On the hold-out test, Random Forest achieves an accuracy of 0.7594, `AtRisk` precision of 0.8007, recall of 0.7213, F1-score of 0.7589, and ROC-AUC of 0.8396. XGBoost achieves the highest accuracy and ROC-AUC, while Random Forest maintains the highest `AtRisk` recall. Of the 3,398 `AtRisk` cases, Random Forest identifies 2,451 and misses 947.

**Table II. Model Performance on the Hold-Out Test**

| Metric | Logistic Regression | Random Forest | XGBoost |
|---|---:|---:|---:|
| Accuracy | 0.7487 | 0.7594 | **0.7611** |
| AtRisk Precision | 0.8034 | 0.8007 | **0.8154** |
| AtRisk Recall | 0.6904 | **0.7213** | 0.7045 |
| AtRisk F1 | 0.7426 | **0.7589** | 0.7559 |
| ROC-AUC | 0.8311 | 0.8396 | **0.8443** |

Fig. 1 compares the metrics of the three models, Fig. 2 shows the Random Forest confusion matrix, and Fig. 3 presents the ROC curves. The three ROC curves are close. Random Forest is selected because the early warning objective prioritizes `AtRisk` detection coverage.

![Fig. 1. Model metric comparison on the hold-out test.](../figures/fig-2a-metrics-comparison.png)

![Fig. 2. Random Forest confusion matrix on the hold-out test.](../figures/fig-2b-confusion-matrix.png)

![Fig. 3. Model ROC curves on the hold-out test.](../figures/fig-2c-roc-curve.png)

## D. Feature Importance

Early behavioral signals dominate the Random Forest feature contributions. Total VLE clicks, last activity day, active days, and the number of accessed sites appear as the leading predictors, followed by assessment and registration features. Importance values indicate global predictive contributions; causal interpretation requires a causal research design.

![Fig. 4. Fifteen features with the highest Random Forest feature importance.](../figures/fig-3-feature-importance.png)

## E. Benchmark with OULAD Studies

Fig. 5 positions the results in the context of five OULAD studies. Shou et al. used the same binary target at 20% of course duration [5]. Jawad et al. used data through day 260 and SMOTE [6], Balabied and Eid used Random Forest [7], and Ujkani et al. [8] and Alnasyan et al. [9] combined `Fail` and `Withdrawn` as the at-risk group. The figure presents the reported values as a contextual benchmark because the studies differ in horizon, data split, balancing, and model.

![Fig. 5. Accuracy and F1-score benchmark for OULAD-based studies. The comparison is contextual because the studies use different horizons, data splits, balancing methods, and models.](../figures/fig-5-oulad-benchmark.png)

## F. Knowledge-Based Risk Layer and BI Output

The lower-quartile thresholds from the train-validation set are an assessment score of 0, an assessment count of 0, 47 total VLE clicks, and 4 active VLE days. The knowledge layer produces 1,816 `High Risk`, 1,979 `Medium Risk`, and 2,676 `Low Risk` cases. When `High Risk` and `Medium Risk` are mapped to an `AtRisk` alert, recall increases from 0.7213 to 0.7866, while precision changes from 0.8007 to 0.7043. This change expands alert coverage and increases the stakeholder verification workload.

**Table III. Model and Knowledge-Based Risk Layer Comparison**

| Metric | Random Forest | RF + Knowledge Layer |
|---|---:|---:|
| Accuracy | **0.7594** | 0.7146 |
| AtRisk Precision | **0.8007** | 0.7043 |
| AtRisk Recall | 0.7213 | **0.7866** |
| AtRisk F1 | **0.7589** | 0.7432 |

The dashboard in Fig. 6 identifies 3,795 student-module-presentations in the `High Risk` or `Medium Risk` queue. The most frequent signal is low assessment score, with 2,341 cases. The priority list contains anonymous identities, module-presentations, `AtRisk` probabilities, levels, signal counts, reasons, and recommendations. This structure connects technical evaluation with module-presentation monitoring and student-level follow-up.

![Fig. 6. OULAD early warning dashboard at the end of week four.](../figures/fig-4-dashboard-dvbi.png)
