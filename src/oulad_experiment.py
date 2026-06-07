from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import GroupKFold, GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier


CATEGORICAL_COLUMNS = [
    "gender",
    "region",
    "highest_education",
    "imd_band",
    "age_band",
    "disability",
    "code_module",
    "code_presentation",
]

NUMERIC_COLUMNS = [
    "num_of_prev_attempts",
    "studied_credits",
    "date_registration",
    "date_unregistration",
    "has_unregistration",
    "assessment_count",
    "assessment_score_mean",
    "assessment_score_max",
    "assessment_score_min",
    "vle_total_clicks",
    "vle_active_days",
    "vle_site_count",
    "vle_last_activity_day",
]

TARGET_COLUMN = "risk_label"
POSITIVE_LABEL = 1
LABEL_TO_NUMERIC = {"Successful": 0, "AtRisk": 1}
NUMERIC_TO_LABEL = {value: key for key, value in LABEL_TO_NUMERIC.items()}

ASSESSMENT_SCORE_THRESHOLD = 50.29
ASSESSMENT_COUNT_THRESHOLD = 2
VLE_CLICKS_THRESHOLD = 142
VLE_ACTIVE_DAYS_THRESHOLD = 11


def apply_knowledge_risk_layer(row: pd.Series | Dict[str, object]) -> str:
    assessment_score_low = float(row.get("assessment_score_mean", 0) or 0) < ASSESSMENT_SCORE_THRESHOLD
    assessment_count_low = float(row.get("assessment_count", 0) or 0) < ASSESSMENT_COUNT_THRESHOLD
    vle_clicks_low = float(row.get("vle_total_clicks", 0) or 0) < VLE_CLICKS_THRESHOLD
    vle_active_days_low = float(row.get("vle_active_days", 0) or 0) < VLE_ACTIVE_DAYS_THRESHOLD
    has_unregistration = int(float(row.get("has_unregistration", 0) or 0)) == 1

    academic_or_vle_risk_count = sum(
        [assessment_score_low, assessment_count_low, vle_clicks_low, vle_active_days_low]
    )

    if has_unregistration and academic_or_vle_risk_count >= 2:
        return "High Risk"
    if (not has_unregistration and academic_or_vle_risk_count >= 2) or (
        has_unregistration and academic_or_vle_risk_count >= 1
    ):
        return "Medium Risk"
    return "Low Risk"


def _risk_signals(row: pd.Series) -> str:
    signals: List[str] = []
    if float(row.get("assessment_score_mean", 0) or 0) < ASSESSMENT_SCORE_THRESHOLD:
        signals.append("low_assessment_score")
    if float(row.get("assessment_count", 0) or 0) < ASSESSMENT_COUNT_THRESHOLD:
        signals.append("low_assessment_count")
    if float(row.get("vle_total_clicks", 0) or 0) < VLE_CLICKS_THRESHOLD:
        signals.append("low_vle_clicks")
    if float(row.get("vle_active_days", 0) or 0) < VLE_ACTIVE_DAYS_THRESHOLD:
        signals.append("low_vle_active_days")
    if int(float(row.get("has_unregistration", 0) or 0)) == 1:
        signals.append("has_unregistration")
    return "|".join(signals) if signals else "none"


def _prepare_dataframe(csv_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in CATEGORICAL_COLUMNS:
        df[col] = df[col].fillna("Unknown").astype(str)
    df["knowledge_risk_level"] = df.apply(apply_knowledge_risk_layer, axis=1)
    df["knowledge_risk_signals"] = df.apply(_risk_signals, axis=1)
    return df


def _build_preprocessor() -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_COLUMNS),
            ("categorical", categorical_pipeline, CATEGORICAL_COLUMNS),
        ]
    )


def _build_models(scale_pos_weight: float = 1.0) -> Dict[str, Pipeline]:
    return {
        "Logistic Regression": Pipeline(
            steps=[
                ("preprocess", _build_preprocessor()),
                (
                    "model",
                    LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
                ),
            ]
        ),
        "Random Forest": Pipeline(
            steps=[
                ("preprocess", _build_preprocessor()),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=200,
                        class_weight="balanced",
                        random_state=42,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        "XGBoost": Pipeline(
            steps=[
                ("preprocess", _build_preprocessor()),
                (
                    "model",
                    XGBClassifier(
                        n_estimators=150,
                        max_depth=4,
                        learning_rate=0.08,
                        subsample=0.9,
                        colsample_bytree=0.9,
                        scale_pos_weight=scale_pos_weight,
                        eval_metric="logloss",
                        random_state=42,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
    }


def _model_metrics(y_true: Iterable[int], y_pred: Iterable[int]) -> Dict[str, object]:
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=[POSITIVE_LABEL],
        average="binary",
        pos_label=POSITIVE_LABEL,
        zero_division=0,
    )
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_atrisk": precision,
        "recall_atrisk": recall,
        "f1_atrisk": f1,
        "confusion_matrix": matrix.tolist(),
    }


def run_experiment(
    csv_path: str | Path,
    predictions_output_path: str | Path | None = None,
    report_output_path: str | Path | None = None,
) -> Dict[str, object]:
    df = _prepare_dataframe(csv_path)
    feature_columns = CATEGORICAL_COLUMNS + NUMERIC_COLUMNS
    X = df[feature_columns]
    y = df[TARGET_COLUMN].map(LABEL_TO_NUMERIC)
    groups = df["id_student"]

    # Step 1: Hold-out test set (20%) split by student group
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    trainval_idx, test_idx = next(gss.split(X, y, groups))

    X_trainval, X_test = X.iloc[trainval_idx], X.iloc[test_idx]
    y_trainval, y_test = y.iloc[trainval_idx], y.iloc[test_idx]
    groups_trainval = groups.iloc[trainval_idx]
    test_index = df.index[test_idx]

    # Compute scale_pos_weight from trainval data
    n_positive = int((y_trainval == POSITIVE_LABEL).sum())
    n_negative = int((y_trainval == 0).sum())
    scale_pos_weight = n_negative / n_positive if n_positive > 0 else 1.0

    # Split statistics
    trainval_students = int(groups_trainval.nunique())
    test_students = int(groups.iloc[test_idx].nunique())
    trainval_label_dist = dict(Counter(y_trainval.map(NUMERIC_TO_LABEL)))
    test_label_dist = dict(Counter(y_test.map(NUMERIC_TO_LABEL)))

    # Step 2: 5-fold GroupKFold cross-validation on trainval set
    n_folds = 5
    gkf = GroupKFold(n_splits=n_folds)
    cv_scores: Dict[str, List[Dict[str, float]]] = {name: [] for name in _build_models(scale_pos_weight).keys()}

    for fold_train_idx, fold_val_idx in gkf.split(X_trainval, y_trainval, groups_trainval):
        X_fold_train = X_trainval.iloc[fold_train_idx]
        y_fold_train = y_trainval.iloc[fold_train_idx]
        X_fold_val = X_trainval.iloc[fold_val_idx]
        y_fold_val = y_trainval.iloc[fold_val_idx]

        for name, model in _build_models(scale_pos_weight).items():
            model.fit(X_fold_train, y_fold_train)
            y_fold_pred = model.predict(X_fold_val)
            cv_scores[name].append(_model_metrics(y_fold_val, y_fold_pred))

    # Aggregate CV results (mean ± std)
    cv_results: Dict[str, Dict[str, object]] = {}
    for name, fold_metrics in cv_scores.items():
        cv_results[name] = {}
        for metric in ["accuracy", "precision_atrisk", "recall_atrisk", "f1_atrisk"]:
            values = [fold[metric] for fold in fold_metrics]
            cv_results[name][f"{metric}_mean"] = round(float(np.mean(values)), 4)
            cv_results[name][f"{metric}_std"] = round(float(np.std(values)), 4)

    # Step 3: Final evaluation on hold-out test set (train on full trainval)
    model_results: Dict[str, Dict[str, object]] = {}
    trained_models: Dict[str, Pipeline] = {}
    for name, model in _build_models(scale_pos_weight=scale_pos_weight).items():
        model.fit(X_trainval, y_trainval)
        y_pred = model.predict(X_test)
        model_results[name] = _model_metrics(y_test, y_pred)
        trained_models[name] = model

    best_model_name = sorted(
        model_results,
        key=lambda name: (model_results[name]["recall_atrisk"], model_results[name]["f1_atrisk"]),
        reverse=True,
    )[0]
    best_model = trained_models[best_model_name]

    predictions = df.loc[test_index].copy()
    predicted_numeric = best_model.predict(X_test)
    predictions["predicted_risk_label"] = [NUMERIC_TO_LABEL[int(value)] for value in predicted_numeric]
    if hasattr(best_model, "predict_proba"):
        predictions["predicted_probability_atrisk"] = best_model.predict_proba(X_test)[:, 1]
    else:
        predictions["predicted_probability_atrisk"] = ""

    if predictions_output_path is not None:
        predictions_output_path = Path(predictions_output_path)
        predictions_output_path.parent.mkdir(parents=True, exist_ok=True)
        prediction_columns = [
            "code_module",
            "code_presentation",
            "id_student",
            "final_result",
            "risk_label",
            "predicted_risk_label",
            "predicted_probability_atrisk",
            "knowledge_risk_level",
            "knowledge_risk_signals",
        ]
        predictions[prediction_columns].to_csv(predictions_output_path, index=False)

    summary = {
        "row_count": len(df),
        "feature_count": len(feature_columns),
        "categorical_features": CATEGORICAL_COLUMNS,
        "numeric_features": NUMERIC_COLUMNS,
        "label_distribution": dict(Counter(df[TARGET_COLUMN])),
        "knowledge_risk_distribution": dict(Counter(df["knowledge_risk_level"])),
        "cv_results": cv_results,
        "cv_folds": n_folds,
        "model_results": model_results,
        "best_model": best_model_name,
        "split_strategy": "GroupShuffleSplit (holdout) + GroupKFold (CV), grouped by id_student",
        "split_ratio": "80/20 holdout; 5-fold CV on train set",
        "trainval_rows": len(X_trainval),
        "test_rows": len(X_test),
        "trainval_students": trainval_students,
        "test_students": test_students,
        "trainval_label_distribution": trainval_label_dist,
        "test_label_distribution": test_label_dist,
        "scale_pos_weight": round(scale_pos_weight, 4),
        "imbalance_handling": "class_weight='balanced' (LR, RF); scale_pos_weight (XGBoost)",
    }

    if report_output_path is not None:
        write_experiment_report(summary, report_output_path)

    return summary


def write_experiment_report(summary: Dict[str, object], output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Hasil Eksperimen OULAD Binary Risk",
        "",
        "## Ringkasan Dataset",
        f"- Total row: **{summary['row_count']}**",
        f"- Total fitur model: **{summary['feature_count']}**",
        "",
        "## Distribusi Label",
    ]
    for label, count in summary["label_distribution"].items():
        lines.append(f"- `{label}`: **{count}**")

    lines.extend(
        [
            "",
            "## Data Split",
            f"- Strategi: **{summary['split_strategy']}**",
            f"- Rasio: **{summary['split_ratio']}**",
            f"- Train+Validation: **{summary['trainval_rows']}** baris ({summary['trainval_students']} mahasiswa unik)",
            f"- Test (hold-out): **{summary['test_rows']}** baris ({summary['test_students']} mahasiswa unik)",
            f"- Distribusi label train+val: {summary['trainval_label_distribution']}",
            f"- Distribusi label test: {summary['test_label_distribution']}",
            "",
            "**Leakage prevention:** Split dilakukan berdasarkan `id_student` (GroupShuffleSplit untuk hold-out, GroupKFold untuk CV). Tidak ada mahasiswa yang muncul di training dan test/validation secara bersamaan.",
            "",
            "## Penanganan Imbalance",
            f"- Metode: **{summary['imbalance_handling']}**",
            f"- `scale_pos_weight` (XGBoost): **{summary['scale_pos_weight']}**",
            f"- Rasio kelas: AtRisk {summary['label_distribution'].get('AtRisk', 0)} vs Successful {summary['label_distribution'].get('Successful', 0)} (rasio ~1.12:1, near-balanced)",
            "",
            "## Ringkasan Fitur",
            "- Fitur kategorikal: "
            + ", ".join(f"`{col}`" for col in summary["categorical_features"]),
            "- Fitur numerik: " + ", ".join(f"`{col}`" for col in summary["numeric_features"]),
            "",
            f"## Cross-Validation ({summary['cv_folds']}-Fold GroupKFold)",
            "| Model | Accuracy | Precision AtRisk | Recall AtRisk | F1 AtRisk |",
            "|---|---:|---:|---:|---:|",
        ]
    )

    for model_name, metrics in summary["cv_results"].items():
        lines.append(
            f"| {model_name} | "
            f"{metrics['accuracy_mean']:.4f} ± {metrics['accuracy_std']:.4f} | "
            f"{metrics['precision_atrisk_mean']:.4f} ± {metrics['precision_atrisk_std']:.4f} | "
            f"{metrics['recall_atrisk_mean']:.4f} ± {metrics['recall_atrisk_std']:.4f} | "
            f"{metrics['f1_atrisk_mean']:.4f} ± {metrics['f1_atrisk_std']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Performa pada Hold-Out Test Set",
            "| Model | Accuracy | Precision AtRisk | Recall AtRisk | F1 AtRisk | Confusion Matrix [[TN, FP], [FN, TP]] |",
            "|---|---:|---:|---:|---:|---|",
        ]
    )

    for model_name, metrics in summary["model_results"].items():
        lines.append(
            f"| {model_name} | {metrics['accuracy']:.4f} | {metrics['precision_atrisk']:.4f} | "
            f"{metrics['recall_atrisk']:.4f} | {metrics['f1_atrisk']:.4f} | `{metrics['confusion_matrix']}` |"
        )

    lines.extend(
        [
            "",
            "## Model Terpilih",
            f"Model terbaik untuk kebutuhan early warning adalah **{summary['best_model']}**, dipilih berdasarkan recall kelas `AtRisk` dan F1-score kelas `AtRisk` sebagai tie-breaker.",
            "",
            "## Distribusi Knowledge-Based Risk Layer",
        ]
    )
    for label, count in summary["knowledge_risk_distribution"].items():
        lines.append(f"- `{label}`: **{count}**")

    lines.extend(
        [
            "",
            "## Implikasi Visual Analytics",
            "Hasil eksperimen dapat diterjemahkan menjadi indikator monitoring akademik, terutama jumlah mahasiswa `AtRisk`, distribusi `High Risk`, `Medium Risk`, dan `Low Risk`, perbandingan risiko antar module-presentation, serta daftar prioritas mahasiswa yang memiliki sinyal aktivitas VLE rendah, performa assessment rendah, atau unregistration.",
            "",
            "## Known Limitations",
            "- **Fitur `has_unregistration` dan `date_unregistration`** bersifat post-hoc: mahasiswa yang unregister secara definisi sudah dropout. Fitur ini dipertahankan untuk baseline karena memberikan sinyal yang relevan untuk knowledge-based layer, tetapi untuk skenario early prediction murni sebaiknya dieksklusi.",
            "- **Agregasi assessment dan VLE menggunakan data seluruh semester**, bukan cut-off temporal (misal minggu ke-4). Ini berarti model melihat seluruh trajectory mahasiswa, bukan prediksi dini.",
            "- **Split dilakukan berdasarkan `id_student`** untuk menghindari group leakage (mahasiswa yang sama muncul di train dan test pada module berbeda).",
        ]
    )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
