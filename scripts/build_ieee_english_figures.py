from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "docs" / "artikel-ieee" / "figures"


def build_metric_comparison() -> None:
    models = ["Random Forest", "XGBoost", "Logistic Regression"]
    precision = [0.8007, 0.8154, 0.8034]
    recall = [0.7213, 0.7045, 0.6904]
    f1 = [0.7589, 0.7559, 0.7426]
    x = np.arange(len(models))
    width = 0.24

    fig, ax = plt.subplots(figsize=(4.1, 3.0), dpi=220)
    ax.bar(x - width, precision, width, label="Precision", color="#66c2a5")
    ax.bar(x, recall, width, label="Recall", color="#fc8d62")
    ax.bar(x + width, f1, width, label="F1-score", color="#8da0cb")
    ax.set_title("AtRisk Model Metrics")
    ax.set_xticks(x, models, rotation=12)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Model")
    ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.legend(fontsize=7, loc="upper right")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig-2a-metrics-comparison-en.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def build_confusion_matrix() -> None:
    cm = np.array([[2463, 610], [947, 2451]])
    fig, ax = plt.subplots(figsize=(4.1, 3.0), dpi=220)
    image = ax.imshow(cm, cmap="Blues")
    for row in range(2):
        for column in range(2):
            ax.text(column, row, f"{cm[row, column]:,}", ha="center", va="center",
                    color="white" if cm[row, column] > cm.max() / 2 else "#222222")
    ax.set_xticks([0, 1], ["Successful", "AtRisk"])
    ax.set_yticks([0, 1], ["Successful", "AtRisk"])
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix - Random Forest")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig-2b-confusion-matrix-en.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def build_dashboard() -> None:
    levels = ["High Risk", "Medium Risk", "Low Risk"]
    counts = [1816, 1979, 2676]
    colors = ["#d62828", "#f4a261", "#2a9d8f"]
    metrics = ["Precision", "Recall", "F1-score"]
    model = [0.8007, 0.7213, 0.7589]
    knowledge = [0.7043, 0.7866, 0.7432]
    cm = np.array([[2463, 610], [947, 2451]])

    fig = plt.figure(figsize=(7.2, 6.4), dpi=240, constrained_layout=True)
    grid = fig.add_gridspec(3, 3, height_ratios=[0.45, 1.5, 1.5])
    fig.suptitle("OULAD EARLY WARNING DASHBOARD - WEEK 4", fontsize=15, fontweight="bold")

    for index, (value, label) in enumerate([
        ("5,757", "Unique students"),
        ("3,795", "Intervention priority"),
        ("58.6%", "Priority rate"),
    ]):
        ax = fig.add_subplot(grid[0, index])
        ax.axis("off")
        ax.text(0.5, 0.62, value, ha="center", va="center", fontsize=18, fontweight="bold", color="#264653")
        ax.text(0.5, 0.18, label, ha="center", va="center", fontsize=8)
        ax.add_patch(plt.Rectangle((0.02, 0.02), 0.96, 0.96, fill=False, edgecolor="#a8dadc", linewidth=1.4))

    ax1 = fig.add_subplot(grid[1, 0])
    ax1.pie(counts, labels=levels, autopct="%1.1f%%", startangle=90, colors=colors, textprops={"fontsize": 7})
    ax1.set_title("Risk Level Distribution", fontsize=9)

    ax2 = fig.add_subplot(grid[1, 1:])
    x = np.arange(len(metrics))
    width = 0.34
    ax2.bar(x - width / 2, model, width, label="Random Forest", color="#457b9d")
    ax2.bar(x + width / 2, knowledge, width, label="RF + Knowledge Layer", color="#e76f51")
    ax2.set_xticks(x, metrics)
    ax2.set_ylim(0, 1)
    ax2.set_title("Model and Knowledge Layer", fontsize=9)
    ax2.legend(fontsize=7, loc="lower right")
    ax2.grid(axis="y", color="#dddddd", linewidth=0.5)

    ax3 = fig.add_subplot(grid[2, 0])
    image = ax3.imshow(cm, cmap="Blues")
    for row in range(2):
        for column in range(2):
            ax3.text(column, row, f"{cm[row, column]:,}", ha="center", va="center", fontsize=9,
                     color="white" if cm[row, column] > cm.max() / 2 else "#222222")
    ax3.set_xticks([0, 1], ["Successful", "AtRisk"], fontsize=7)
    ax3.set_yticks([0, 1], ["Successful", "AtRisk"], fontsize=7)
    ax3.set_xlabel("Predicted", fontsize=7)
    ax3.set_ylabel("Actual", fontsize=7)
    ax3.set_title("Random Forest Confusion Matrix", fontsize=9)
    fig.colorbar(image, ax=ax3, fraction=0.046, pad=0.04)

    ax4 = fig.add_subplot(grid[2, 1:])
    signals = ["Low assessment score", "High or Medium Risk", "High Risk"]
    values = [2341, 3795, 1816]
    ax4.barh(signals[::-1], values[::-1], color=["#d62828", "#e76f51", "#f4a261"])
    for index, value in enumerate(values[::-1]):
        ax4.text(value + 45, index, f"{value:,}", va="center", fontsize=8)
    ax4.set_xlim(0, 4200)
    ax4.set_xlabel("Student-module-presentations", fontsize=7)
    ax4.set_title("Priority and Dominant Signal", fontsize=9)
    ax4.grid(axis="x", color="#dddddd", linewidth=0.5)

    fig.savefig(FIGURE_DIR / "fig-4-dashboard-dvbi-en.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    build_metric_comparison()
    build_confusion_matrix()
    build_dashboard()
    print("Wrote English article figures")


if __name__ == "__main__":
    main()
