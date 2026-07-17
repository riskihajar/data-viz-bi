from __future__ import annotations

import base64
import json
from io import BytesIO
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "oulad_early_warning_dvbi_colab.ipynb"
OUTPUT_DIR = ROOT / "docs" / "artikel-ieee" / "figures"

FIGURES = {
    "5454c1cf": "fig-1-eda.png",
    "benchmark-metrics-visualization": "fig-5-oulad-benchmark.png",
    "e9d7d72e": "fig-2-model-evaluation.png",
    "bc3b705a": "fig-3-feature-importance.png",
    "f90b08a9": "fig-4-dashboard-dvbi.png",
}

EVALUATION_PANELS = (
    ("fig-2a-metrics-comparison.png", 0.000, 0.333),
    ("fig-2b-confusion-matrix.png", 0.333, 0.650),
    ("fig-2c-roc-curve.png", 0.655, 1.000),
)


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cells_by_id = {cell["id"]: cell for cell in notebook["cells"]}
    for cell_id, filename in FIGURES.items():
        outputs = cells_by_id[cell_id].get("outputs", [])
        images = [
            output["data"]["image/png"]
            for output in outputs
            if "image/png" in output.get("data", {})
        ]
        if len(images) != 1:
            raise RuntimeError(
                f"Cell {cell_id} expected one PNG output, found {len(images)}"
            )
        encoded = images[0]
        if isinstance(encoded, list):
            encoded = "".join(encoded)
        target = OUTPUT_DIR / filename
        target.write_bytes(base64.b64decode(encoded))
        print(f"Wrote {target}")

    evaluation = Image.open(OUTPUT_DIR / "fig-2-model-evaluation.png")
    for filename, left_ratio, right_ratio in EVALUATION_PANELS:
        left = round(left_ratio * evaluation.width)
        right = round(right_ratio * evaluation.width)
        panel = evaluation.crop((left, 0, right, evaluation.height))
        buffer = BytesIO()
        panel.save(buffer, format="PNG", optimize=True)
        target = OUTPUT_DIR / filename
        target.write_bytes(buffer.getvalue())
        print(f"Wrote {target}")


if __name__ == "__main__":
    main()
