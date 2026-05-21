from pathlib import Path

from src.oulad_experiment import run_experiment


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "processed" / "oulad_binary_risk_dataset.csv"
PREDICTIONS_OUTPUT_PATH = ROOT / "data" / "processed" / "oulad_risk_predictions.csv"
REPORT_OUTPUT_PATH = ROOT / "docs" / "experiment-results-oulad-binary-risk.md"


if __name__ == "__main__":
    summary = run_experiment(
        INPUT_PATH,
        predictions_output_path=PREDICTIONS_OUTPUT_PATH,
        report_output_path=REPORT_OUTPUT_PATH,
    )
    print(f"Wrote predictions to {PREDICTIONS_OUTPUT_PATH}")
    print(f"Wrote experiment report to {REPORT_OUTPUT_PATH}")
    print(f"Best model: {summary['best_model']}")
