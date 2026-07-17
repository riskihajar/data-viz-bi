from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "docs" / "artikel-ieee" / "figures"


def build_figure(language: str) -> Path:
    english = language == "en"
    labels = [
        "Shou et al. [5]\n20% course, MTAPSP",
        "Jawad et al. [6]\n260 days + SMOTE, RF",
        "Balabied and Eid [7]\nBinary, RF",
        "Ujkani et al. [8]\nAt-risk binary, custom NN",
        "Alnasyan et al. [9]\nAt-risk binary, KANFormer",
        ("This study\nDay 28, group split, RF" if english else
         "Penelitian ini\nHari ke-28, group split, RF"),
    ]
    accuracy = np.array([0.9179, 0.8920, 0.9000, 0.9300, 0.9459, 0.7594])
    f1 = np.array([0.9180, np.nan, 0.9000, 0.9600, 0.9481, 0.7589])
    y = np.arange(len(labels))

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.2})
    fig, ax = plt.subplots(figsize=(3.25, 3.35), dpi=300)
    ax.axhspan(4.55, 5.45, color="#e8f1ee", zorder=0)

    ax.scatter(accuracy, y - 0.12, s=28, marker="o", color="#287271", label="Accuracy", zorder=3)
    valid_f1 = ~np.isnan(f1)
    ax.scatter(f1[valid_f1], y[valid_f1] + 0.12, s=31, marker="D", color="#e76f51", label="F1-score", zorder=3)
    ax.text(0.985, 1.12, "N/A", ha="right", va="center", fontsize=6.5, color="#666666")

    for index, value in enumerate(accuracy):
        ax.text(value + 0.004, index - 0.12, f"{value:.4f}", va="center", fontsize=6.2, color="#1f4f4e")
    for index, value in enumerate(f1):
        if not np.isnan(value):
            ax.text(value + 0.004, index + 0.12, f"{value:.4f}", va="center", fontsize=6.2, color="#8f3d2b")

    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0.72, 1.00)
    ax.set_xticks([0.75, 0.80, 0.85, 0.90, 0.95, 1.00])
    ax.set_xlabel("Reported score" if english else "Reported score")
    ax.grid(axis="x", color="#d7d7d7", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.legend(loc="lower left", frameon=False, ncol=2, bbox_to_anchor=(0.0, 1.01))
    ax.tick_params(axis="y", length=0, pad=4)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#777777")

    for tick in ax.get_yticklabels():
        if tick.get_text().startswith("This study" if english else "Penelitian ini"):
            tick.set_fontweight("bold")

    output = FIGURE_DIR / ("fig-5-oulad-benchmark-en.png" if english else "fig-5-oulad-benchmark.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {output}")
    return output


def main() -> None:
    build_figure("id")
    build_figure("en")


if __name__ == "__main__":
    main()
