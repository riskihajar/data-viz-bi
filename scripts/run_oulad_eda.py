from pathlib import Path

from src.oulad_eda import summarize_binary_dataset, write_markdown_report


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "processed" / "oulad_binary_risk_dataset.csv"
OUTPUT_PATH = ROOT / "docs" / "eda-oulad-binary-risk.md"


if __name__ == "__main__":
    summary = summarize_binary_dataset(INPUT_PATH)
    write_markdown_report(summary, OUTPUT_PATH)
    print(f"Wrote EDA report to {OUTPUT_PATH}")
