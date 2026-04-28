from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional


OUTPUT_COLUMNS = [
    "code_module",
    "code_presentation",
    "id_student",
    "gender",
    "region",
    "highest_education",
    "imd_band",
    "age_band",
    "num_of_prev_attempts",
    "studied_credits",
    "disability",
    "final_result",
    "risk_label",
    "date_registration",
    "date_unregistration",
    "has_unregistration",
    "assessment_count",
    "assessment_score_mean",
    "assessment_score_max",
    "assessment_score_min",
    "vle_total_clicks",
    "vle_active_days",
    "vle_site_count",
    "vle_last_activity_day",
]


def classify_risk(final_result: str) -> str:
    if final_result in {"Withdrawn", "Fail"}:
        return "AtRisk"
    if final_result in {"Pass", "Distinction"}:
        return "Successful"
    raise ValueError(f"Unknown final_result: {final_result!r}")


def _read_csv(path: Path) -> Iterable[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        yield from csv.DictReader(f)


def _student_key(row: Dict[str, str]) -> tuple[str, str, str]:
    return (row["code_module"], row["code_presentation"], row["id_student"])


def _safe_int(value: str, default: int = 0) -> int:
    if value == "" or value is None:
        return default
    return int(value)


def _safe_float(value: str) -> Optional[float]:
    if value == "" or value is None:
        return None
    return float(value)


def build_binary_risk_dataset(data_dir: str | Path, output_path: str | Path | None = None) -> List[Dict[str, str]]:
    data_dir = Path(data_dir)

    registrations: Dict[tuple[str, str, str], Dict[str, str]] = {}
    for row in _read_csv(data_dir / "studentRegistration.csv"):
        registrations[_student_key(row)] = row

    assessment_scores: Dict[str, List[float]] = defaultdict(list)
    for row in _read_csv(data_dir / "studentAssessment.csv"):
        score = _safe_float(row.get("score", ""))
        if score is not None:
            assessment_scores[row["id_student"]].append(score)

    vle_stats: Dict[tuple[str, str, str], Dict[str, object]] = defaultdict(
        lambda: {"total_clicks": 0, "days": set(), "sites": set(), "last_day": None}
    )
    for row in _read_csv(data_dir / "studentVle.csv"):
        key = _student_key(row)
        stat = vle_stats[key]
        clicks = _safe_int(row.get("sum_click", "0"), default=0)
        day = _safe_int(row.get("date", "0"), default=0)
        stat["total_clicks"] += clicks
        stat["days"].add(day)
        stat["sites"].add(row["id_site"])
        if stat["last_day"] is None or day > stat["last_day"]:
            stat["last_day"] = day

    output_rows: List[Dict[str, str]] = []
    for row in _read_csv(data_dir / "studentInfo.csv"):
        key = _student_key(row)
        registration = registrations.get(key, {})
        scores = assessment_scores.get(row["id_student"], [])
        vle = vle_stats.get(key, {"total_clicks": 0, "days": set(), "sites": set(), "last_day": None})

        imd_band = row["imd_band"] if row["imd_band"] else "Unknown"
        date_unregistration = registration.get("date_unregistration", "")
        enriched = {
            "code_module": row["code_module"],
            "code_presentation": row["code_presentation"],
            "id_student": row["id_student"],
            "gender": row["gender"],
            "region": row["region"],
            "highest_education": row["highest_education"],
            "imd_band": imd_band,
            "age_band": row["age_band"],
            "num_of_prev_attempts": row["num_of_prev_attempts"],
            "studied_credits": row["studied_credits"],
            "disability": row["disability"],
            "final_result": row["final_result"],
            "risk_label": classify_risk(row["final_result"]),
            "date_registration": registration.get("date_registration", ""),
            "date_unregistration": date_unregistration,
            "has_unregistration": "1" if date_unregistration != "" else "0",
            "assessment_count": str(len(scores)),
            "assessment_score_mean": f"{(sum(scores) / len(scores)):.2f}" if scores else "0.00",
            "assessment_score_max": f"{max(scores):.2f}" if scores else "0.00",
            "assessment_score_min": f"{min(scores):.2f}" if scores else "0.00",
            "vle_total_clicks": str(vle["total_clicks"]),
            "vle_active_days": str(len(vle["days"])),
            "vle_site_count": str(len(vle["sites"])),
            "vle_last_activity_day": "" if vle["last_day"] is None else str(vle["last_day"]),
        }
        output_rows.append(enriched)

    output_rows.sort(key=lambda r: (r["code_module"], r["code_presentation"], int(r["id_student"])))

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
            writer.writeheader()
            writer.writerows(output_rows)

    return output_rows
