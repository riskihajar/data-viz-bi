from pathlib import Path

from src.oulad_preprocessing import build_binary_risk_dataset


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "oulad"
OUTPUT_PATH = ROOT / "data" / "processed" / "oulad_binary_risk_dataset.csv"


if __name__ == "__main__":
    rows = build_binary_risk_dataset(DATA_DIR, output_path=OUTPUT_PATH)
    print(f"Wrote {len(rows)} rows to {OUTPUT_PATH}")
