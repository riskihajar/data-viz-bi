import csv
from pathlib import Path

from src.oulad_eda import summarize_binary_dataset, write_markdown_report


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def test_summarize_binary_dataset_returns_label_distribution_and_numeric_stats(tmp_path):
    csv_path = tmp_path / "binary.csv"
    write_csv(
        csv_path,
        [
            {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "id_student": "1",
                "final_result": "Withdrawn",
                "risk_label": "AtRisk",
                "assessment_count": "2",
                "assessment_score_mean": "50.00",
                "vle_total_clicks": "10",
                "vle_active_days": "2",
                "has_unregistration": "1",
            },
            {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "id_student": "2",
                "final_result": "Pass",
                "risk_label": "Successful",
                "assessment_count": "1",
                "assessment_score_mean": "80.00",
                "vle_total_clicks": "5",
                "vle_active_days": "1",
                "has_unregistration": "0",
            },
            {
                "code_module": "BBB",
                "code_presentation": "2014B",
                "id_student": "3",
                "final_result": "Fail",
                "risk_label": "AtRisk",
                "assessment_count": "3",
                "assessment_score_mean": "40.00",
                "vle_total_clicks": "20",
                "vle_active_days": "4",
                "has_unregistration": "1",
            },
        ],
    )

    summary = summarize_binary_dataset(csv_path)

    assert summary["row_count"] == 3
    assert summary["risk_distribution"] == {"AtRisk": 2, "Successful": 1}
    assert summary["final_result_distribution"] == {"Withdrawn": 1, "Pass": 1, "Fail": 1}
    assert summary["module_count"] == 2
    assert summary["presentation_count"] == 2
    assert summary["numeric_summary"]["assessment_count"]["mean"] == 2.0
    assert summary["numeric_summary"]["vle_total_clicks"]["max"] == 20.0
    assert summary["numeric_summary"]["assessment_score_mean"]["min"] == 40.0
    assert summary["unregistration_rate"] == 2 / 3


def test_write_markdown_report_creates_expected_sections(tmp_path):
    output_path = tmp_path / "report.md"
    summary = {
        "row_count": 3,
        "module_count": 2,
        "presentation_count": 2,
        "risk_distribution": {"AtRisk": 2, "Successful": 1},
        "final_result_distribution": {"Withdrawn": 1, "Pass": 1, "Fail": 1},
        "numeric_summary": {
            "assessment_count": {"min": 1.0, "max": 3.0, "mean": 2.0},
            "assessment_score_mean": {"min": 40.0, "max": 80.0, "mean": 56.67},
            "vle_total_clicks": {"min": 5.0, "max": 20.0, "mean": 11.67},
            "vle_active_days": {"min": 1.0, "max": 4.0, "mean": 2.33},
        },
        "unregistration_rate": 2 / 3,
    }

    write_markdown_report(summary, output_path)

    content = output_path.read_text(encoding="utf-8")
    assert "# EDA Ringkas OULAD — Binary Risk Dataset" in content
    assert "## Distribusi label risiko" in content
    assert "AtRisk" in content
    assert "## Statistik numerik utama" in content
