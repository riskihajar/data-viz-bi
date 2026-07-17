# III. Methodology

## A. Research Design

This study uses supervised binary classification to identify students at risk of unsuccessful course outcomes by the end of week four. The workflow includes OULAD auditing, feature construction with a temporal cut-off, exploratory data analysis, student-grouped splitting, model evaluation, a knowledge-based risk layer, and a Business Intelligence dashboard. All experiments use `random_state=42`.

## B. Dataset and Unit of Analysis

The Open University Learning Analytics Dataset (OULAD) [4] was obtained from the UCI Machine Learning Repository. The analysis uses the `studentInfo`, `studentRegistration`, `assessments`, `studentAssessment`, `studentVle`, `courses`, and `vle` tables. `studentInfo` contains 32,593 rows, while `studentVle` contains 10,655,280 activity records.

Each preprocessed row represents one student in one combination of `code_module` and `code_presentation`. This student-module-presentation unit follows the label structure in `studentInfo` and supports the consistent integration of registration, assessment, and VLE data.

## C. Target Label and Temporal Cut-off

The target is formulated as a binary classification at the course level. The `AtRisk` label is assigned to rows whose `final_result` is `Withdrawn` or `Fail`. The `Successful` label is assigned to rows whose `final_result` is `Pass` or `Distinction`. These statuses describe a student's outcome in a specific module-presentation. The dataset contains 17,208 `AtRisk` rows and 15,385 `Successful` rows.

The early warning horizon is set at day 28. Assessment submissions are selected using `date_submitted <= 28`, and VLE activity is selected using `date <= 28`. The `date_unregistration`, `has_unregistration`, final outcome, and activity after day 28 are excluded from the predictors. The final outcome is used only to construct the evaluation target.

## D. Feature Construction

Categorical features include `gender`, `region`, `highest_education`, `imd_band`, `age_band`, `disability`, `code_module`, and `code_presentation`. Initial numeric features include `num_of_prev_attempts`, `studied_credits`, and `date_registration`.

The `studentAssessment` data are joined with `assessments` through `id_assessment` to obtain the module-presentation context. Data through day 28 are aggregated into `assessment_count`, `assessment_score_mean`, `assessment_score_max`, and `assessment_score_min`. The `studentVle` data through day 28 are aggregated into `vle_total_clicks`, `vle_active_days`, `vle_site_count`, and `vle_last_activity_day`.

Numeric values are converted with `pd.to_numeric`, and values that cannot be converted are treated as missing values. Behavioral aggregates with no recorded activity are filled with zero. Within the modeling pipeline, missing numeric values are imputed with the median and then standardized. Missing categorical values are imputed with the mode and transformed using one-hot encoding. All transformations are learned within the pipeline from the training data.

## E. Data Splitting and Validation

The data are divided into 80% train-validation and 20% hold-out test sets using `GroupShuffleSplit`. The `id_student` variable is used as the group, ensuring that each student occurs exclusively in one partition. The train-validation set contains 26,122 rows and the test set contains 6,471 rows. The verification found zero student overlap.

Cross-validation uses 5-fold `GroupKFold` on the train-validation set. Model selection is based on the mean recall for the `AtRisk` class, with the `AtRisk` F1-score used as a tie-breaker. Final performance is then reported on the hold-out test.

## F. Supervised Learning Models

Three algorithms are compared. Logistic Regression is used as a linear baseline with `class_weight='balanced'`. Random Forest uses 250 trees and `class_weight='balanced'`. XGBoost uses 200 estimators, a maximum depth of 4, a learning rate of 0.08, a subsample ratio of 0.9, and a colsample ratio of 0.9. The `scale_pos_weight` value is calculated from the train-validation class distribution.

Evaluation metrics include accuracy, precision, recall, and F1-score for the `AtRisk` class, ROC-AUC, a confusion matrix, and a classification report. `AtRisk` recall is the primary criterion because the early warning setting prioritizes the coverage of at-risk students who can be directed to verification and intervention processes.

## G. Knowledge-Based Risk Layer

The knowledge-based risk layer uses four indicators: `assessment_score_mean`, `assessment_count`, `vle_total_clicks`, and `vle_active_days`. Thresholds are calculated from the lower quartile of the train-validation data, keeping them independent of the hold-out test. The calculation produces thresholds of 0 for assessment score, 0 for assessment count, 47 for total VLE clicks, and 4 for active VLE days.

A risk signal is activated when an indicator is at or below its threshold. `High Risk` is assigned when the model predicts `AtRisk` and the student has at least two rule signals. `Medium Risk` is assigned when the model predicts `AtRisk` or the student has at least two rule signals. `Low Risk` is assigned otherwise.

Each row produces an `AtRisk` probability, a signal count, risk reasons, and an intervention recommendation. Low VLE activity leads to access reminders and monitoring. Low or missing assessment participation leads to academic support. A combination of at least three signals leads to counseling or follow-up by an academic advisor.

The combined system is evaluated by mapping `High Risk` and `Medium Risk` to `AtRisk` and measuring changes in detection coverage, precision, and verification workload.

## H. Visual Analytics and Business Intelligence

The static dashboard is constructed with Matplotlib and Seaborn. It presents KPIs for unique students, the number and percentage prioritized for intervention, the risk-level distribution, risk by module-presentation, the probability distribution, dominant signals, median VLE and assessment activity, a confusion matrix, and a comparison between the model and the knowledge layer.

The priority list is sorted by risk level, `AtRisk` probability, and signal count. The output supports decisions at several levels. Academic leaders obtain an overview of risk scale, study programs see concentrations of risk across module-presentations, and tutors or academic advisors receive student-level reasons and recommendations. The system serves as decision support for stakeholder follow-up based on analytical evidence and academic judgment.
