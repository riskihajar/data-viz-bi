# Complete IEEE Article


# Early Warning of Students at Risk of Unsuccessful Course Outcomes in Week Four Using Supervised Learning and a Knowledge-Based Risk Layer on the Open University Learning Analytics Dataset

Muhammad Rizky Hajar, Alwie Muflich, Heri Santosa, Andi Sunyoto, Robert Marco

Department of Computer Science
Universitas Amikom Yogyakarta
Yogyakarta, Indonesia
Email: riskihajar@students.amikom.ac.id, alwiemuflich@students.amikom.ac.id, heri.sant@students.amikom.ac.id, andi@amikom.ac.id, robert.marco@amikom.ac.id

# Abstract

Final course outcomes provide important information for academic monitoring and early intervention planning. This study develops an early warning system for students at risk of unsuccessful course outcomes by the end of week four using the Open University Learning Analytics Dataset (OULAD). Each row represents one student in one module-presentation. The binary target is defined as `AtRisk` for `Withdrawn` and `Fail` outcomes and `Successful` for `Pass` and `Distinction`. Predictors are constructed from demographic data, initial registration, assessments, and Virtual Learning Environment activity available through day 28. The evaluation compares Logistic Regression, Random Forest, and XGBoost using a student-grouped hold-out test and 5-fold GroupKFold. Random Forest is selected because it achieves the highest cross-validation recall for `AtRisk` at 0.7107. On the hold-out test, the model achieves an accuracy of 0.7594, precision of 0.8007, recall of 0.7213, F1-score of 0.7589, and ROC-AUC of 0.8396. A knowledge-based risk layer combines model predictions with four early behavioral indicators to produce `High Risk`, `Medium Risk`, and `Low Risk` levels with reasons and intervention recommendations. The combined system increases recall to 0.7866 with a precision of 0.7043. The analytical results are presented through a static dashboard containing risk indicators, module-presentation priorities, dominant signals, and a student list for academic monitoring. This approach integrates prediction, rule-based interpretation, and visual decision support for early intervention at the course level.

# Keywords

academic risk prediction, course withdrawal, course failure, supervised learning, OULAD, early warning system

# I. Introduction

Course failure and withdrawal are important concerns in higher education because they are associated with learning outcomes, the quality of academic services, and the effectiveness of institutional decision-making. Previous research has shown that machine learning can predict student retention from sociodemographic characteristics and engagement metrics [1]. Early warning systems extend the value of prediction by identifying risk while academic intervention remains feasible [2]. Risk information during the first weeks gives lecturers, tutors, and program administrators time to design relevant follow-up actions.

Digital learning systems generate academic data and activity traces that can be used to characterize student engagement. These data include interactions with the Virtual Learning Environment (VLE), assessment participation, assessment performance, and initial registration information. Research on digital traces has shown that Learning Management System activity patterns can help explain variations in student performance and risk [3]. The Open University Learning Analytics Dataset (OULAD) provides such data in a relational structure covering student profiles, assessments, registration, and more than ten million VLE activity records [4].

The predictive value of a model depends on whether its inputs are available at the time of decision. Full-semester activity or unregistration status may provide strong information for retrospective classification, whereas early warning requires features already observed at prediction time. This study uses a day-28 cut-off to represent the end of week four. Assessments and VLE activity after the cut-off are excluded from the predictors, and unregistration status is treated as future information. This temporal restriction yields a performance estimate that more closely represents an early-intervention setting.

The literature indicates that risk detection must be connected to follow-up processes to create institutional value [2]. Machine learning models produce classes and probabilities, while stakeholders require risk reasons, priorities, and operationally interpretable recommendations. This need defines a research gap involving the integration of model evaluation, rule-based interpretation, and visual presentation for decision support.

This study aims to develop a binary classification of students at risk of unsuccessful course outcomes in week four, evaluate three supervised learning algorithms, and integrate the selected model with a knowledge-based risk layer. The system output is translated into a Business Intelligence dashboard for risk monitoring and intervention prioritization at the module-presentation level.

The study makes four contributions. First, it constructs an early warning dataset at the student-module-presentation level using a day-28 cut-off. Second, the evaluation uses an `id_student`-based split to maintain student independence between training and testing data. Third, the knowledge-based risk layer produces levels, reasons, and recommendations from model predictions and early behavior. Fourth, the dashboard transforms analytical outputs into indicators that support decisions by academic leaders, study programs, tutors, academic advisors, and counseling teams.

# II. Related Works

Student dropout and academic performance analytics use academic, sociodemographic, and digital activity data to predict study continuation and learning outcomes. Early information, including sociodemographic characteristics, academic history, and digital engagement, has predictive value for student retention [1]. In OULAD, the target concerns the final course outcome for each student-module-presentation.

Early warning systems connect predictive results to intervention processes. Plak et al. showed that risk information should be accompanied by a follow-up design to influence academic outcomes [2]. Shou et al. used OULAD to predict student performance through a multidimensional time-series approach combining learning behavior, assessment scores, and demographic information. At 20% of the course duration, their daily MTAPSP model achieved an accuracy of 0.9179 and an F1-score of 0.9180 for a binary target contrasting `Pass` and `Distinction` with `Fail` and `Withdrawn` [5]. Their findings highlight the observation horizon as an important factor when interpreting early warning performance.

OULAD research has continued to combine assessment features, VLE activity, and student profiles. Jawad et al. applied Random Forest with SMOTE and obtained a testing accuracy of 0.892 in a 260-day scenario [6]. Balabied and Eid reported an accuracy and F1-score of 0.90 using Random Forest [7]. Ujkani et al. obtained an accuracy of 0.93 with a custom neural network [8], while the KANFormer proposed by Alnasyan et al. achieved an accuracy of 0.9459 and an F1-score of 0.9481 [9]. Shou et al. [5], Ujkani et al. [8], and Alnasyan et al. [9] used comparable target definitions. Differences in horizon, splitting, balancing, and model architecture still determine the context of comparison.

Hybrid approaches integrate multiple data sources to identify at-risk students [10]. Other studies cover XGBoost-based early warning [11], AutoML [12], precision education [13], phased prediction [14], LMS usage patterns [15], and cross-institutional analysis [16]. This diversity shows that features, observation horizons, and institutional contexts shape the interpretation of model performance.

This study is positioned at the integration of three components. Supervised learning generates risk probabilities, a knowledge-based risk layer translates probabilities and behavioral signals into reasons and priority levels, and a dashboard presents the results as visual decision support. The week-four cut-off maintains temporal alignment between the predictors and the intervention point. This integration connects technical evaluation with actionable academic monitoring requirements.

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

## G. Discussion and Limitations

The experimental results show the relationship between the decision objective and model selection. XGBoost performs best in accuracy and ROC-AUC, while Random Forest achieves the highest `AtRisk` recall in both cross-validation and the hold-out test. Performance near 0.76 represents an early scenario that uses only information available through day 28. This horizon provides more time for intervention while limiting the behavioral evidence available to the model.

The assessment threshold of zero indicates that some module-presentations have no submissions by week four. Future work can use module-presentation-specific thresholds or align the cut-off with assessment schedules. The knowledge layer increases recall by 0.0653 points and produces operational reasons such as low VLE activity or incomplete assessments. These reasons support verification using contextual information from lecturers and tutors.

The dashboard extends the model into Business Intelligence through risk aggregation, module-presentation comparison, and a student queue. The finding that 100% of GGG 2014J cases are prioritized signals the need to review group size, assessment schedules, and module characteristics before selecting an action.

The study is limited by the context of OULAD at the United Kingdom Open University, behavioral features represented as aggregates, baseline model configurations, and quartile thresholds that require expert validation. The evaluation measures detection performance, while the impact of interventions on successful course outcomes requires further research using institutional data and an intervention evaluation design.

# V. Conclusion

This study develops an early warning system for students at risk of unsuccessful course outcomes by the end of week four using OULAD. The dataset is constructed at the student-module-presentation level using demographic, initial registration, assessment, and VLE activity features available through day 28. The `id_student`-based split maintains student independence between the train-validation and hold-out test sets.

Random Forest is selected based on the highest cross-validation `AtRisk` recall of 0.7107. On the hold-out test, the model achieves an accuracy of 0.7594, precision of 0.8007, recall of 0.7213, F1-score of 0.7589, and ROC-AUC of 0.8396. The knowledge-based risk layer increases recall to 0.7866 by combining the model prediction with four early behavioral signals. The system produces risk levels, reasons, and recommendations that can be translated into an intervention queue.

The Business Intelligence dashboard presents the risk distribution, module-presentation priorities, dominant signals, model performance, and an anonymous student list for monitoring. The integration of supervised learning, a knowledge-based risk layer, and visual analytics produces decision support that connects prediction with academic follow-up processes.

Future work can compare week-four, week-eight, and week-twelve horizons; use module-presentation-specific thresholds; tune hyperparameters; and test external validity on other institutional datasets. Intervention impact evaluation is also required to measure the system's contribution to successful course completion.

# References

[1] S. Matz et al., "Using machine learning to predict student retention from socio-demographic characteristics and app-based engagement metrics," *Scientific Reports*, 2023, doi: 10.1038/s41598-023-32484-w.

[2] S. Plak et al., "Early warning systems for more effective student counselling in higher education: Evidence from a Dutch field experiment," *Higher Education Quarterly*, 2022, doi: 10.1111/hequ.12298.

[3] J. Pecuchova and M. Drlik, "Enhancing the Early Student Dropout Prediction Model Through Clustering Analysis of Students' Digital Traces," *IEEE Access*, 2024, doi: 10.1109/ACCESS.2024.3486762.

[4] J. Kuzilek, M. Hlosta, and Z. Zdrahal, "Open University Learning Analytics dataset," *Scientific Data*, vol. 4, article no. 170171, 2017, doi: 10.1038/sdata.2017.171.

[5] Z. Shou, M. Xie, J. Mo, and H. Zhang, "Predicting Student Performance in Online Learning: A Multidimensional Time-Series Data Analysis Approach," *Applied Sciences*, vol. 14, no. 6, article no. 2522, 2024, doi: 10.3390/app14062522.

[6] K. Jawad, M. A. Shah, and M. Tahir, "Students' Academic Performance and Engagement Prediction in a Virtual Learning Environment Using Random Forest with Data Balancing," *Sustainability*, vol. 14, no. 22, article no. 14795, 2022, doi: 10.3390/su142214795.

[7] S. A. A. Balabied and H. F. Eid, "Utilizing Random Forest Algorithm for Early Detection of Academic Underperformance in Open Learning Environments," *PeerJ Computer Science*, vol. 9, article no. e1708, 2023, doi: 10.7717/peerj-cs.1708.

[8] B. Ujkani, D. Minkovska, and N. Hinov, "Course Success Prediction and Early Identification of At-Risk Students Using Explainable Artificial Intelligence," *Electronics*, vol. 13, no. 21, article no. 4157, 2024, doi: 10.3390/electronics13214157.

[9] B. Alnasyan, M. Basheri, M. Alassafi, and K. Alnasyan, "Kanformer: An Attention-Enhanced Deep Learning Model for Predicting Student Performance in Virtual Learning Environments," *Social Network Analysis and Mining*, vol. 15, article no. 25, 2025, doi: 10.1007/s13278-025-01446-7.

[10] T. Kustitskaya et al., "Hybrid Approach to Predicting Learning Success Based on Digital Educational History for Timely Identification of At-Risk Students," *Education Sciences*, 2024, doi: 10.3390/educsci14060657.

[11] M. Carballo-Mendivil et al., "Predicting Student Dropout from Day One: XGBoost-Based Early Warning System Using Pre-Enrollment Data," *Applied Sciences*, 2025, doi: 10.3390/app15169202.

[12] A. Garmpis et al., "Assisting Educational Analytics with AutoML Functionalities," *Computers*, 2022, doi: 10.3390/computers11060097.

[13] C. Y. Tsai et al., "Precision education with statistical learning and deep learning: a case study in Taiwan," *International Journal of Educational Technology in Higher Education*, 2020, doi: 10.1186/s41239-020-00186-2.

[14] M. V. Martins et al., "Multi-Class Phased Prediction of Academic Performance and Dropout in Higher Education," *Applied Sciences*, 2023, doi: 10.3390/app13084702.

[15] J. R. Rico-Juan et al., "Study regarding the influence of a student's personality and an LMS usage profile on learning performance using machine learning techniques," *Applied Intelligence*, 2024, doi: 10.1007/s10489-024-05483-1.

[16] J. Berens et al., "Crossing individual university boundaries: a comprehensive approach to predicting dropouts in the higher education system," *Higher Education*, 2025, doi: 10.1007/s10734-025-01509-w.
