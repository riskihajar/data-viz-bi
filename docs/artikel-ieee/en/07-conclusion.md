# V. Conclusion

This study develops an early warning system for students at risk of unsuccessful course outcomes by the end of week four using OULAD. The dataset is constructed at the student-module-presentation level using demographic, initial registration, assessment, and VLE activity features available through day 28. The `id_student`-based split maintains student independence between the train-validation and hold-out test sets.

Random Forest is selected based on the highest cross-validation `AtRisk` recall of 0.7107. On the hold-out test, the model achieves an accuracy of 0.7594, precision of 0.8007, recall of 0.7213, F1-score of 0.7589, and ROC-AUC of 0.8396. The knowledge-based risk layer increases recall to 0.7866 by combining the model prediction with four early behavioral signals. The system produces risk levels, reasons, and recommendations that can be translated into an intervention queue.

The Business Intelligence dashboard presents the risk distribution, module-presentation priorities, dominant signals, model performance, and an anonymous student list for monitoring. The integration of supervised learning, a knowledge-based risk layer, and visual analytics produces decision support that connects prediction with academic follow-up processes.

Future work can compare week-four, week-eight, and week-twelve horizons; use module-presentation-specific thresholds; tune hyperparameters; and test external validity on other institutional datasets. Intervention impact evaluation is also required to measure the system's contribution to successful course completion.
