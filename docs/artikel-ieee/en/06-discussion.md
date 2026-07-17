## G. Discussion and Limitations

The experimental results show the relationship between the decision objective and model selection. XGBoost performs best in accuracy and ROC-AUC, while Random Forest achieves the highest `AtRisk` recall in both cross-validation and the hold-out test. Performance near 0.76 represents an early scenario that uses only information available through day 28. This horizon provides more time for intervention while limiting the behavioral evidence available to the model.

The assessment threshold of zero indicates that some module-presentations have no submissions by week four. Future work can use module-presentation-specific thresholds or align the cut-off with assessment schedules. The knowledge layer increases recall by 0.0653 points and produces operational reasons such as low VLE activity or incomplete assessments. These reasons support verification using contextual information from lecturers and tutors.

The dashboard extends the model into Business Intelligence through risk aggregation, module-presentation comparison, and a student queue. The finding that 100% of GGG 2014J cases are prioritized signals the need to review group size, assessment schedules, and module characteristics before selecting an action.

The study is limited by the context of OULAD at the United Kingdom Open University, behavioral features represented as aggregates, baseline model configurations, and quartile thresholds that require expert validation. The evaluation measures detection performance, while the impact of interventions on successful course outcomes requires further research using institutional data and an intervention evaluation design.
