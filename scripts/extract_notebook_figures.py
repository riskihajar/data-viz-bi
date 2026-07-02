from __future__ import annotations

import base64
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "oulad_early_warning_dvbi_colab.ipynb"
OUTPUT_DIR = ROOT / "docs" / "artikel-ieee" / "figures"

FIGURES = {
    12: "fig-1-eda.png",
    22: "fig-2-model-evaluation.png",
    24: "fig-3-feature-importance.png",
    30: "fig-4-dashboard-dvbi.png",
}


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for cell_index, filename in FIGURES.items():
        outputs = notebook["cells"][cell_index].get("outputs", [])
        images = [
            output["data"]["image/png"]
            for output in outputs
            if "image/png" in output.get("data", {})
        ]
        if len(images) != 1:
            raise RuntimeError(
                f"Cell {cell_index} expected one PNG output, found {len(images)}"
            )
        encoded = images[0]
        if isinstance(encoded, list):
            encoded = "".join(encoded)
        target = OUTPUT_DIR / filename
        target.write_bytes(base64.b64decode(encoded))
        print(f"Wrote {target}")


if __name__ == "__main__":
    main()
