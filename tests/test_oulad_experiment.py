import csv

from src.oulad_experiment import apply_knowledge_risk_layer, run_experiment


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def base_row(**overrides):
    row = {
        "code_module": "AAA",
        "code_presentation": "2013J",
        "id_student": "1",
        "gender": "M",
        "region": "East Anglian Region",
        "highest_education": "A Level or Equivalent",
        "imd_band": "20-30%",
        "age_band": "0-35",
        "num_of_prev_attempts": "0",
        "studied_credits": "60",
        "disability": "N",
        "final_result": "Pass",
        "risk_label": "Successful",
        "date_registration": "-10",
        "date_unregistration": "",
        "has_unregistration": "0",
        "assessment_count": "5",
        "assessment_score_mean": "80.00",
        "assessment_score_max": "90.00",
        "assessment_score_min": "70.00",
        "vle_total_clicks": "500",
        "vle_active_days": "40",
        "vle_site_count": "10",
        "vle_last_activity_day": "100",
    }
    row.update(overrides)
    return row


def test_apply_knowledge_risk_layer_returns_expected_levels():
    assert apply_knowledge_risk_layer(base_row()) == "Low Risk"
    assert (
        apply_knowledge_risk_layer(
            base_row(
                assessment_count="1",
                assessment_score_mean="40.00",
                vle_total_clicks="50",
                has_unregistration="1",
            )
        )
        == "High Risk"
    )
    assert (
        apply_knowledge_risk_layer(
            base_row(assessment_count="1", assessment_score_mean="40.00", has_unregistration="0")
        )
        == "Medium Risk"
    )
    assert apply_knowledge_risk_layer(base_row(vle_total_clicks="50", has_unregistration="1")) == "Medium Risk"


def test_run_experiment_writes_report_and_predictions(tmp_path):
    rows = []
    for i in range(1, 41):
        rows.append(
            base_row(
                id_student=str(i),
                code_module="AAA" if i % 2 else "BBB",
                risk_label="AtRisk" if i <= 20 else "Successful",
                final_result="Fail" if i <= 20 else "Pass",
                has_unregistration="1" if i <= 20 else "0",
                date_unregistration="5" if i <= 20 else "",
                assessment_count="1" if i <= 20 else "5",
                assessment_score_mean="40.00" if i <= 20 else "80.00",
                assessment_score_max="50.00" if i <= 20 else "90.00",
                assessment_score_min="30.00" if i <= 20 else "70.00",
                vle_total_clicks="50" if i <= 20 else "500",
                vle_active_days="5" if i <= 20 else "40",
            )
        )

    csv_path = tmp_path / "oulad_binary.csv"
    predictions_path = tmp_path / "predictions.csv"
    report_path = tmp_path / "report.md"
    write_csv(csv_path, rows)

    summary = run_experiment(csv_path, predictions_output_path=predictions_path, report_output_path=report_path)

    assert summary["row_count"] == 40
    assert set(summary["model_results"]) == {"Logistic Regression", "Random Forest", "XGBoost"}
    assert summary["best_model"] in summary["model_results"]
    assert predictions_path.exists()
    assert report_path.exists()

    with open(predictions_path, newline="", encoding="utf-8") as f:
        predictions = list(csv.DictReader(f))

    assert predictions
    assert set(row["knowledge_risk_level"] for row in predictions).issubset(
        {"Low Risk", "Medium Risk", "High Risk"}
    )
    assert "## Performa Model" in report_path.read_text(encoding="utf-8")
