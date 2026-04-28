from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List


NUMERIC_COLUMNS = [
    "assessment_count",
    "assessment_score_mean",
    "vle_total_clicks",
    "vle_active_days",
]


def _read_csv(path: Path) -> Iterable[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        yield from csv.DictReader(f)


def _summarize_numbers(values: List[float]) -> Dict[str, float]:
    return {
        "min": min(values),
        "max": max(values),
        "mean": sum(values) / len(values),
    }


def summarize_binary_dataset(csv_path: str | Path) -> Dict[str, object]:
    csv_path = Path(csv_path)
    risk_distribution: Counter[str] = Counter()
    final_result_distribution: Counter[str] = Counter()
    modules = set()
    presentations = set()
    numeric_buckets: Dict[str, List[float]] = {col: [] for col in NUMERIC_COLUMNS}
    unregistration_count = 0
    row_count = 0

    for row in _read_csv(csv_path):
        row_count += 1
        risk_distribution[row["risk_label"]] += 1
        final_result_distribution[row["final_result"]] += 1
        modules.add(row["code_module"])
        presentations.add(row["code_presentation"])
        if row.get("has_unregistration") == "1":
            unregistration_count += 1
        for col in NUMERIC_COLUMNS:
            numeric_buckets[col].append(float(row[col]))

    numeric_summary = {col: _summarize_numbers(values) for col, values in numeric_buckets.items() if values}

    return {
        "row_count": row_count,
        "module_count": len(modules),
        "presentation_count": len(presentations),
        "risk_distribution": dict(risk_distribution),
        "final_result_distribution": dict(final_result_distribution),
        "numeric_summary": numeric_summary,
        "unregistration_rate": (unregistration_count / row_count) if row_count else 0,
    }


def write_markdown_report(summary: Dict[str, object], output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines: List[str] = [
        "# EDA Ringkas OULAD — Binary Risk Dataset",
        "",
        "## Ringkasan dataset",
        f"- Total row: **{summary['row_count']}**",
        f"- Total module: **{summary['module_count']}**",
        f"- Total presentation: **{summary['presentation_count']}**",
        f"- Unregistration rate: **{summary['unregistration_rate']:.2%}**",
        "",
        "## Distribusi label risiko",
    ]

    for label, count in summary["risk_distribution"].items():
        lines.append(f"- `{label}`: **{count}**")

    lines.extend(["", "## Distribusi final_result asli"])
    for label, count in summary["final_result_distribution"].items():
        lines.append(f"- `{label}`: **{count}**")

    lines.extend(["", "## Statistik numerik utama"])
    for col, stats in summary["numeric_summary"].items():
        lines.append(
            f"- `{col}` → min: **{stats['min']:.2f}**, max: **{stats['max']:.2f}**, mean: **{stats['mean']:.2f}**"
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
