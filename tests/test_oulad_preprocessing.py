from pathlib import Path
import csv

from src.oulad_preprocessing import build_binary_risk_dataset, classify_risk


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def test_classify_risk_maps_final_result_to_binary_label():
    assert classify_risk("Withdrawn") == "AtRisk"
    assert classify_risk("Fail") == "AtRisk"
    assert classify_risk("Pass") == "Successful"
    assert classify_risk("Distinction") == "Successful"


def test_build_binary_risk_dataset_merges_info_registration_assessment_and_vle(tmp_path):
    data_dir = tmp_path / "oulad"

    write_csv(
        data_dir / "studentInfo.csv",
        [
            {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "id_student": "1",
                "gender": "M",
                "region": "East Anglian Region",
                "highest_education": "A Level or Equivalent",
                "imd_band": "",
                "age_band": "0-35",
                "num_of_prev_attempts": "0",
                "studied_credits": "60",
                "disability": "N",
                "final_result": "Withdrawn",
            },
            {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "id_student": "2",
                "gender": "F",
                "region": "Scotland",
                "highest_education": "HE Qualification",
                "imd_band": "20-30%",
                "age_band": "35-55",
                "num_of_prev_attempts": "1",
                "studied_credits": "120",
                "disability": "N",
                "final_result": "Pass",
            },
        ],
    )

    write_csv(
        data_dir / "studentRegistration.csv",
        [
            {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "id_student": "1",
                "date_registration": "-10",
                "date_unregistration": "5",
            },
            {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "id_student": "2",
                "date_registration": "-12",
                "date_unregistration": "",
            },
        ],
    )

    write_csv(
        data_dir / "studentAssessment.csv",
        [
            {
                "id_assessment": "100",
                "id_student": "1",
                "date_submitted": "1",
                "is_banked": "0",
                "score": "40",
            },
            {
                "id_assessment": "101",
                "id_student": "1",
                "date_submitted": "10",
                "is_banked": "0",
                "score": "60",
            },
            {
                "id_assessment": "102",
                "id_student": "2",
                "date_submitted": "2",
                "is_banked": "0",
                "score": "80",
            },
        ],
    )

    write_csv(
        data_dir / "studentVle.csv",
        [
            {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "id_student": "1",
                "id_site": "9",
                "date": "1",
                "sum_click": "3",
            },
            {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "id_student": "1",
                "id_site": "10",
                "date": "2",
                "sum_click": "7",
            },
            {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "id_student": "2",
                "id_site": "11",
                "date": "2",
                "sum_click": "5",
            },
        ],
    )

    rows = build_binary_risk_dataset(data_dir)

    assert len(rows) == 2

    by_student = {row["id_student"]: row for row in rows}

    assert by_student["1"]["risk_label"] == "AtRisk"
    assert by_student["1"]["imd_band"] == "Unknown"
    assert by_student["1"]["has_unregistration"] == "1"
    assert by_student["1"]["assessment_count"] == "2"
    assert by_student["1"]["assessment_score_mean"] == "50.00"
    assert by_student["1"]["vle_total_clicks"] == "10"
    assert by_student["1"]["vle_active_days"] == "2"

    assert by_student["2"]["risk_label"] == "Successful"
    assert by_student["2"]["imd_band"] == "20-30%"
    assert by_student["2"]["has_unregistration"] == "0"
    assert by_student["2"]["assessment_count"] == "1"
    assert by_student["2"]["assessment_score_mean"] == "80.00"
    assert by_student["2"]["vle_total_clicks"] == "5"
    assert by_student["2"]["vle_active_days"] == "1"


def test_build_binary_risk_dataset_writes_output_csv(tmp_path):
    data_dir = tmp_path / "oulad"
    output_path = tmp_path / "processed" / "binary_risk_dataset.csv"

    write_csv(
        data_dir / "studentInfo.csv",
        [
            {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "id_student": "7",
                "gender": "M",
                "region": "London",
                "highest_education": "A Level or Equivalent",
                "imd_band": "10-20",
                "age_band": "0-35",
                "num_of_prev_attempts": "0",
                "studied_credits": "60",
                "disability": "N",
                "final_result": "Fail",
            }
        ],
    )
    write_csv(
        data_dir / "studentRegistration.csv",
        [
            {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "id_student": "7",
                "date_registration": "-5",
                "date_unregistration": "",
            }
        ],
    )
    write_csv(
        data_dir / "studentAssessment.csv",
        [
            {
                "id_assessment": "100",
                "id_student": "7",
                "date_submitted": "1",
                "is_banked": "0",
                "score": "55",
            }
        ],
    )
    write_csv(
        data_dir / "studentVle.csv",
        [
            {
                "code_module": "AAA",
                "code_presentation": "2013J",
                "id_student": "7",
                "id_site": "9",
                "date": "1",
                "sum_click": "4",
            }
        ],
    )

    rows = build_binary_risk_dataset(data_dir, output_path=output_path)

    assert len(rows) == 1
    assert output_path.exists()

    with open(output_path, newline="", encoding="utf-8") as f:
        written = list(csv.DictReader(f))

    assert written[0]["id_student"] == "7"
    assert written[0]["risk_label"] == "AtRisk"
