import zipfile
from pathlib import Path

from scripts.download_oulad import extract_zip


EXPECTED_FILES = {
    "assessments.csv",
    "courses.csv",
    "studentAssessment.csv",
    "studentInfo.csv",
    "studentRegistration.csv",
    "studentVle.csv",
    "vle.csv",
}


def test_extract_zip_extracts_expected_files(tmp_path):
    zip_path = tmp_path / "anonymisedData.zip"
    output_dir = tmp_path / "oulad"

    with zipfile.ZipFile(zip_path, "w") as zf:
        for name in EXPECTED_FILES:
            zf.writestr(name, "header\nvalue\n")

    extract_zip(zip_path, output_dir)

    extracted = {p.name for p in output_dir.iterdir()}
    assert EXPECTED_FILES.issubset(extracted)


def test_extract_zip_skips_when_files_already_exist(tmp_path, capsys):
    zip_path = tmp_path / "anonymisedData.zip"
    output_dir = tmp_path / "oulad"
    output_dir.mkdir(parents=True, exist_ok=True)

    for name in EXPECTED_FILES:
        (output_dir / name).write_text("ready", encoding="utf-8")

    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("dummy.csv", "x\n")

    extract_zip(zip_path, output_dir)

    captured = capsys.readouterr()
    assert "Skip extract" in captured.out
