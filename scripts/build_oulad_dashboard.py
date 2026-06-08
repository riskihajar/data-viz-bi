from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.oulad_experiment import apply_knowledge_risk_layer, run_experiment


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "processed" / "oulad_binary_risk_dataset.csv"
PREDICTIONS_PATH = ROOT / "data" / "processed" / "oulad_risk_predictions.csv"
DASHBOARD_PATH = ROOT / "assets" / "dashboard" / "oulad-risk-dashboard.html"


def _counter_to_items(counter: Counter) -> list[dict[str, object]]:
    return [{"label": key, "value": value} for key, value in counter.items()]


def _module_summary(df: pd.DataFrame) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, object]] = {}
    for module, group in df.groupby("code_module"):
        total = len(group)
        risk_counts = Counter(group["knowledge_risk_level"])
        atrisk_count = int((group["risk_label"] == "AtRisk").sum())
        grouped[module] = {
            "module": module,
            "total": total,
            "atrisk": atrisk_count,
            "atrisk_rate": round(atrisk_count / total * 100, 2),
            "high": risk_counts.get("High Risk", 0),
            "medium": risk_counts.get("Medium Risk", 0),
            "low": risk_counts.get("Low Risk", 0),
        }
    return sorted(grouped.values(), key=lambda row: row["atrisk_rate"], reverse=True)


def _presentation_summary(df: pd.DataFrame) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for (module, presentation), group in df.groupby(["code_module", "code_presentation"]):
        total = len(group)
        high = int((group["knowledge_risk_level"] == "High Risk").sum())
        medium = int((group["knowledge_risk_level"] == "Medium Risk").sum())
        atrisk = int((group["risk_label"] == "AtRisk").sum())
        rows.append(
            {
                "module": module,
                "presentation": presentation,
                "total": total,
                "atrisk_rate": round(atrisk / total * 100, 2),
                "priority_rate": round((high + medium) / total * 100, 2),
                "high": high,
                "medium": medium,
            }
        )
    return sorted(rows, key=lambda row: (row["priority_rate"], row["atrisk_rate"]), reverse=True)


def _risk_signals(row: pd.Series) -> str:
    signals: list[str] = []
    if float(row.get("assessment_score_mean", 0) or 0) < 50.29:
        signals.append("low_assessment_score")
    if float(row.get("assessment_count", 0) or 0) < 2:
        signals.append("low_assessment_count")
    if float(row.get("vle_total_clicks", 0) or 0) < 142:
        signals.append("low_vle_clicks")
    if float(row.get("vle_active_days", 0) or 0) < 11:
        signals.append("low_vle_active_days")
    if int(float(row.get("has_unregistration", 0) or 0)) == 1:
        signals.append("has_unregistration")
    return "|".join(signals) if signals else "none"


def _priority_score(row: pd.Series) -> float:
    """Score that differentiates within risk levels using actual feature values."""
    base = {"High Risk": 0.60, "Medium Risk": 0.30, "Low Risk": 0.05}[row["knowledge_risk_level"]]
    # Use actual values to differentiate (lower values = higher risk score)
    assess_mean = float(row.get("assessment_score_mean", 0) or 0)
    assess_count = float(row.get("assessment_count", 0) or 0)
    vle_clicks = float(row.get("vle_total_clicks", 0) or 0)
    vle_days = float(row.get("vle_active_days", 0) or 0)
    has_unreg = int(float(row.get("has_unregistration", 0) or 0))

    # Each factor adds up to a portion, with diminishing scale
    score_pen = max(0, (60 - assess_mean) / 60) * 0.10
    count_pen = max(0, (5 - assess_count) / 5) * 0.08
    click_pen = max(0, (500 - vle_clicks) / 500) * 0.08
    days_pen = max(0, (30 - vle_days) / 30) * 0.07
    unreg_pen = 0.07 if has_unreg else 0
    return round(min(base + score_pen + count_pen + click_pen + days_pen + unreg_pen, 0.99), 2)


def _priority_students(df: pd.DataFrame) -> list[dict[str, object]]:
    priority = df[df["knowledge_risk_level"].isin(["High Risk", "Medium Risk"])].copy()
    priority["priority_score"] = priority.apply(_priority_score, axis=1)
    risk_order = {"High Risk": 0, "Medium Risk": 1, "Low Risk": 2}
    priority["risk_order"] = priority["knowledge_risk_level"].map(risk_order)
    # Secondary sort: fewer VLE active days = more urgent
    priority = priority.sort_values(
        ["risk_order", "priority_score", "vle_last_activity_day"],
        ascending=[True, False, True],
    )
    # Sample diversity: mix modules, include varied signal patterns
    sampled = []
    high = priority[priority["knowledge_risk_level"] == "High Risk"]
    medium = priority[priority["knowledge_risk_level"] == "Medium Risk"]
    for _, group in high.groupby("code_module"):
        sampled.append(group.head(2))
    for _, group in medium.groupby("code_module"):
        if len(group) >= 2:
            mid_idx = len(group) // 2
            sampled.append(group.iloc[[0, mid_idx]])
        else:
            sampled.append(group.head(1))
    result = pd.concat(sampled).sort_values(
        ["risk_order", "priority_score", "vle_last_activity_day"],
        ascending=[True, False, True],
    ).head(30)
    columns = [
        "code_module",
        "code_presentation",
        "id_student",
        "priority_score",
        "knowledge_risk_level",
        "knowledge_risk_signals",
        "vle_last_activity_day",
    ]
    return result[columns].to_dict(orient="records")


def _trend_data(df: pd.DataFrame) -> list[dict[str, object]]:
    """AtRisk rate per presentation (time series)."""
    pres_order = ["2013B", "2013J", "2014B", "2014J"]
    rows = []
    for pres in pres_order:
        subset = df[df["code_presentation"] == pres]
        if len(subset) == 0:
            continue
        atrisk_rate = round((subset["risk_label"] == "AtRisk").mean() * 100, 1)
        rows.append({"presentation": pres, "atrisk_rate": atrisk_rate, "total": len(subset)})
    return rows


def _signal_cooccurrence(df: pd.DataFrame) -> list[dict[str, object]]:
    """How many students have N simultaneous risk signals."""
    counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for signals in df["knowledge_risk_signals"]:
        parts = [p for p in str(signals).split("|") if p and p != "none"]
        n = min(len(parts), 5)
        counts[n] += 1
    return [{"signals": k, "count": v} for k, v in counts.items() if v > 0]


def _success_metrics(df: pd.DataFrame) -> dict[str, object]:
    """Counterbalance: success cohort stats."""
    successful = df[df["risk_label"] == "Successful"]
    distinction = df[df["final_result"] == "Distinction"]
    low_risk = df[df["knowledge_risk_level"] == "Low Risk"]
    return {
        "successful_count": len(successful),
        "successful_pct": round(len(successful) / len(df) * 100, 1),
        "distinction_count": len(distinction),
        "distinction_pct": round(len(distinction) / len(df) * 100, 1),
        "low_risk_count": len(low_risk),
        "avg_vle_clicks_successful": round(successful["vle_total_clicks"].mean(), 0),
        "avg_assessment_score_successful": round(successful["assessment_score_mean"].mean(), 1),
    }


def build_dashboard_data() -> dict[str, object]:
    df = pd.read_csv(DATASET_PATH)
    for col in [
        "assessment_count",
        "assessment_score_mean",
        "assessment_score_max",
        "assessment_score_min",
        "vle_total_clicks",
        "vle_active_days",
        "vle_site_count",
        "vle_last_activity_day",
        "has_unregistration",
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["knowledge_risk_level"] = df.apply(apply_knowledge_risk_layer, axis=1)
    df["knowledge_risk_signals"] = df.apply(_risk_signals, axis=1)
    experiment_summary = run_experiment(DATASET_PATH)
    high_risk = int((df["knowledge_risk_level"] == "High Risk").sum())
    medium_risk = int((df["knowledge_risk_level"] == "Medium Risk").sum())
    low_risk = int((df["knowledge_risk_level"] == "Low Risk").sum())
    unreg_rate = round(df["has_unregistration"].mean() * 100, 1)

    signal_counts: defaultdict[str, int] = defaultdict(int)
    for signals in df["knowledge_risk_signals"]:
        for signal in str(signals).split("|"):
            if signal and signal != "none":
                signal_counts[signal] += 1

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "kpis": {
            "rows": len(df),
            "modules": int(df["code_module"].nunique()),
            "presentations": int(df["code_presentation"].nunique()),
            "atrisk": int((df["risk_label"] == "AtRisk").sum()),
            "atrisk_rate": round((df["risk_label"] == "AtRisk").mean() * 100, 2),
            "high_risk": high_risk,
            "medium_risk": medium_risk,
            "low_risk": low_risk,
            "unreg_rate": unreg_rate,
        },
        "trend": _trend_data(df),
        "signalCooccurrence": _signal_cooccurrence(df),
        "successMetrics": _success_metrics(df),
        "labelDistribution": _counter_to_items(Counter(df["risk_label"])),
        "finalResultDistribution": _counter_to_items(Counter(df["final_result"])),
        "knowledgeDistribution": _counter_to_items(Counter(df["knowledge_risk_level"])),
        "moduleSummary": _module_summary(df),
        "presentationSummary": _presentation_summary(df),
        "signalCounts": sorted(
            [{"label": k, "value": v} for k, v in signal_counts.items()],
            key=lambda x: x["value"],
            reverse=True,
        ),
        "modelResults": experiment_summary["model_results"],
        "bestModel": experiment_summary["best_model"],
        "priorityStudents": _priority_students(df),
    }


HTML_TEMPLATE = r"""<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dashboard Monitoring Risiko Akademik</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f7f9;
      --panel: #ffffff;
      --line: #d8dee8;
      --text: #17202a;
      --muted: #667085;
      --blue: #2563eb;
      --teal: #0f766e;
      --amber: #d97706;
      --red: #dc2626;
      --green: #16a34a;
      --ink: #263548;
      --active-filter: #dbeafe;
    }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); }
    header { background: #102033; color: white; padding: 22px 28px 18px; border-bottom: 4px solid var(--teal); }
    header h1 { margin: 0 0 4px; font-size: clamp(22px, 3vw, 32px); font-weight: 750; }
    header p { margin: 0; color: #c8d3df; max-width: 960px; line-height: 1.45; font-size: 14px; }
    .header-meta { display: flex; gap: 18px; margin-top: 8px; font-size: 12px; color: #94a3b8; }
    main { padding: 22px 28px 32px; max-width: 1440px; margin: 0 auto; }
    .toolbar { display: flex; gap: 12px; align-items: center; justify-content: space-between; margin-bottom: 18px; flex-wrap: wrap; padding: 12px 16px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; }
    .toolbar select { border: 1px solid var(--line); background: white; min-height: 38px; padding: 8px 12px; border-radius: 6px; font: inherit; color: var(--text); cursor: pointer; min-width: 160px; }
    .toolbar select:focus { outline: 2px solid var(--blue); border-color: var(--blue); }
    .toolbar label { color: var(--muted); font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
    .filter-status { font-size: 13px; color: var(--blue); font-weight: 600; display: none; padding: 4px 10px; background: var(--active-filter); border-radius: 4px; }
    .filter-status.active { display: inline-block; }
    .kpis { display: grid; grid-template-columns: repeat(5, minmax(130px, 1fr)); gap: 12px; margin-bottom: 18px; }
    .kpi, .panel { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; box-shadow: 0 1px 2px rgba(16,32,51,.04); }
    .kpi { padding: 14px; min-height: 96px; position: relative; }
    .kpi .label { color: var(--muted); font-size: 11px; text-transform: uppercase; font-weight: 700; letter-spacing: 0.02em; }
    .kpi .value { font-size: clamp(22px, 2.8vw, 32px); font-weight: 780; margin-top: 6px; color: var(--ink); }
    .kpi .note { color: var(--muted); font-size: 11px; margin-top: 2px; }
    .kpi .trend { position: absolute; top: 12px; right: 14px; font-size: 11px; font-weight: 700; }
    .kpi .trend.up { color: var(--red); }
    .kpi .trend.down { color: var(--green); }
    .kpi .trend.flat { color: var(--muted); }
    .sparkline { display: flex; align-items: flex-end; gap: 2px; height: 24px; margin-top: 6px; }
    .sparkline .bar { width: 16px; background: var(--blue); border-radius: 2px; opacity: 0.6; }
    .sparkline .bar:last-child { opacity: 1; }
    .grid { display: grid; grid-template-columns: 1.1fr .9fr; gap: 14px; margin-bottom: 14px; }
    .grid-3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-bottom: 14px; }
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }
    .panel { padding: 16px; overflow: hidden; }
    .panel h2 { margin: 0 0 12px; font-size: 15px; line-height: 1.25; font-weight: 700; }
    .bar-row { display: grid; grid-template-columns: 150px 1fr 80px; gap: 10px; align-items: center; margin: 10px 0; }
    .bar-label { color: var(--ink); font-size: 13px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .bar-track { height: 18px; background: #e8edf3; border-radius: 5px; overflow: hidden; }
    .bar-fill { height: 100%; border-radius: 5px; transition: width 0.3s ease; }
    .bar-value { color: var(--muted); font-variant-numeric: tabular-nums; text-align: right; font-size: 12px; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th, td { border-bottom: 1px solid var(--line); padding: 9px 8px; text-align: left; vertical-align: top; }
    th { color: var(--muted); font-size: 11px; font-weight: 750; background: #f9fafb; position: sticky; top: 0; text-transform: uppercase; letter-spacing: 0.02em; }
    .scroll { max-height: 390px; overflow: auto; border: 1px solid var(--line); border-radius: 6px; }
    .pill { display: inline-block; padding: 3px 7px; border-radius: 999px; font-size: 11px; font-weight: 700; white-space: nowrap; }
    .pill-high { background: #fee2e2; color: #991b1b; }
    .pill-medium { background: #fef3c7; color: #92400e; }
    .pill-low { background: #dcfce7; color: #166534; }
    .legend { display: flex; gap: 12px; flex-wrap: wrap; color: var(--muted); font-size: 12px; margin-top: 10px; }
    .legend i { width: 10px; height: 10px; display: inline-block; border-radius: 2px; margin-right: 4px; vertical-align: middle; }
    .muted { color: var(--muted); }
    .decision-note { border-left: 4px solid var(--teal); background: #eef7f5; padding: 12px 14px; border-radius: 6px; color: #164e45; line-height: 1.45; margin-bottom: 12px; font-size: 13px; }
    .success-note { border-left: 4px solid var(--green); background: #f0fdf4; padding: 12px 14px; border-radius: 6px; color: #166534; line-height: 1.45; font-size: 13px; }
    .action-list { display: grid; gap: 9px; }
    .action-item { border: 1px solid var(--line); border-radius: 6px; padding: 10px 12px; background: #fbfcfd; line-height: 1.4; }
    .action-item b { display: block; color: var(--ink); margin-bottom: 3px; font-size: 13px; }
    .action-item span { font-size: 12px; color: var(--muted); }
    .cooccurrence { display: flex; gap: 6px; align-items: flex-end; height: 90px; margin-top: 16px; }
    .cooccurrence .col { display: flex; flex-direction: column; align-items: center; flex: 1; }
    .cooccurrence .col-bar { width: 100%; max-width: 36px; background: var(--blue); border-radius: 3px 3px 0 0; opacity: 0.7; }
    .cooccurrence .col-label { font-size: 10px; color: var(--muted); margin-top: 4px; }
    .cooccurrence .col-value { font-size: 11px; color: var(--ink); font-weight: 700; margin-bottom: 2px; }
    .benchmark { display: flex; align-items: center; gap: 8px; margin-top: 10px; padding: 8px 12px; background: #fffbeb; border: 1px solid #fde68a; border-radius: 6px; font-size: 12px; color: #92400e; }
    footer { padding: 16px 28px; color: var(--muted); font-size: 12px; border-top: 1px solid var(--line); margin-top: 12px; }
    footer .note-box { background: #f9fafb; border: 1px solid var(--line); border-radius: 6px; padding: 12px 14px; line-height: 1.5; }
    @media (max-width: 1100px) { .kpis { grid-template-columns: repeat(3, minmax(0, 1fr)); } .grid, .grid-3, .grid-2 { grid-template-columns: 1fr; } }
    @media (max-width: 680px) { header, main { padding-left: 16px; padding-right: 16px; } .kpis { grid-template-columns: 1fr 1fr; } .bar-row { grid-template-columns: 110px 1fr 52px; } }
  </style>
</head>
<body>
  <header>
    <h1>Dashboard Monitoring Risiko Akademik</h1>
    <p>Membantu pengelola akademik memantau mahasiswa berisiko, menentukan prioritas intervensi, dan membaca alasan risiko berdasarkan aktivitas belajar.</p>
    <div class="header-meta">
      <span>Dataset: Open University Learning Analytics Dataset (OULAD) 2013–2014</span>
      <span>|</span>
      <span id="generatedAt"></span>
    </div>
  </header>
  <main>
    <section class="toolbar">
      <div style="display:flex; align-items:center; gap:12px;">
        <label>Filter Module
          <select id="moduleFilter"><option value="all">Semua Module</option></select>
        </label>
        <span class="filter-status" id="filterStatus"></span>
      </div>
      <div class="muted" style="font-size:12px;">Kode module telah dianonimisasi oleh penyedia dataset</div>
    </section>

    <section class="kpis" id="kpis"></section>

    <section class="grid">
      <div class="panel">
        <h2>Segmentasi Risiko Mahasiswa</h2>
        <div class="decision-note">Kelompok <b>High Risk</b> = prioritas kontak akademik. <b>Medium Risk</b> = observasi berkala. <b>Low Risk</b> = monitoring reguler.</div>
        <div id="knowledgeBars"></div>
        <div class="legend">
          <span><i style="background:var(--red)"></i>High Risk</span>
          <span><i style="background:var(--amber)"></i>Medium Risk</span>
          <span><i style="background:var(--green)"></i>Low Risk</span>
        </div>
      </div>
      <div class="panel">
        <h2>Ringkasan Keputusan</h2>
        <div id="decisionSummary" class="action-list"></div>
      </div>
    </section>

    <section class="grid-3">
      <div class="panel">
        <h2>Prioritas Tindakan</h2>
        <div id="actionPlan" class="action-list"></div>
      </div>
      <div class="panel">
        <h2>Ko-Occurensi Sinyal Risiko</h2>
        <p class="muted" style="font-size:12px;margin:0 0 16px;">Jumlah mahasiswa berdasarkan banyaknya sinyal risiko yang aktif bersamaan.</p>
        <div class="cooccurrence" id="cooccurrence"></div>
      </div>
      <div class="panel">
        <h2>Module: Risiko vs Volume</h2>
        <div id="moduleBars"></div>
      </div>
    </section>

    <section class="grid-2">
      <div class="panel">
        <h2>Tren Risiko per Periode</h2>
        <p class="muted" style="font-size:12px;margin:0 0 12px;">AtRisk rate di setiap presentation.</p>
        <div id="trendChart"></div>
        <div class="benchmark" id="benchmark"></div>
      </div>
      <div class="panel">
        <h2>Profil Mahasiswa Berhasil</h2>
        <div class="success-note" id="successPanel"></div>
      </div>
    </section>

    <section class="grid">
      <div class="panel">
        <h2>Area Akademik Prioritas</h2>
        <div class="scroll">
          <table>
            <thead><tr><th>Module</th><th>Presentation</th><th>Jumlah</th><th>AtRisk Rate</th><th>High</th><th>Medium</th></tr></thead>
            <tbody id="presentationRows"></tbody>
          </table>
        </div>
      </div>
      <div class="panel">
        <h2>Daftar Prioritas Intervensi</h2>
        <div class="scroll">
          <table>
            <thead><tr><th>ID Mahasiswa (anonim)</th><th>Module</th><th>Level Risiko</th><th>Skor</th><th>Hari Terakhir Aktif</th><th>Alasan Utama</th><th>Rekomendasi</th></tr></thead>
            <tbody id="priorityRows"></tbody>
          </table>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="note-box">
      <b>Catatan Metodologis:</b> Dashboard ini menggunakan model <b id="bestModel"></b> sebagai scoring engine dan knowledge-based risk layer sebagai penjelas risiko.
      Metrik teknis model tidak ditampilkan di sini karena dashboard ditujukan untuk keputusan monitoring akademik.
      Kode module (AAA–GGG) merupakan anonimisasi dari penyedia dataset OULAD dan tidak merepresentasikan nama mata kuliah sebenarnya.
    </div>
  </footer>

  <script>
    const DATA = __DASHBOARD_DATA__;
    const colors = {"High Risk":"#dc2626","Medium Risk":"#d97706","Low Risk":"#16a34a"};
    const fmt = new Intl.NumberFormat("id-ID");
    const pct = v => `${Number(v).toFixed(1)}%`;
    const signalLabels = {
      low_assessment_score: "Skor assessment rendah",
      low_assessment_count: "Partisipasi assessment rendah",
      low_vle_clicks: "Aktivitas VLE rendah",
      low_vle_active_days: "Hari aktif VLE rendah",
      has_unregistration: "Sinyal unregistration"
    };
    let currentModule = "all";

    function getFilteredData() {
      if (currentModule === "all") return DATA;
      const mod = currentModule;
      const modSummary = DATA.moduleSummary.filter(r => r.module === mod);
      const ms = modSummary[0] || {};
      return {
        ...DATA,
        kpis: { rows: ms.total||0, modules: 1, presentations: DATA.presentationSummary.filter(r=>r.module===mod).length, atrisk: ms.atrisk||0, atrisk_rate: ms.atrisk_rate||0, high_risk: ms.high||0, medium_risk: ms.medium||0, low_risk: ms.low||0, unreg_rate: DATA.kpis.unreg_rate },
        knowledgeDistribution: [{label:"Low Risk",value:ms.low||0},{label:"High Risk",value:ms.high||0},{label:"Medium Risk",value:ms.medium||0}],
        moduleSummary: modSummary,
        presentationSummary: DATA.presentationSummary.filter(r=>r.module===mod),
        priorityStudents: DATA.priorityStudents.filter(r=>r.code_module===mod),
      };
    }

    function trendArrow() {
      const t = DATA.trend;
      if (t.length < 2) return {text:"", cls:"flat"};
      const last = t[t.length-1].atrisk_rate;
      const prev = t[t.length-2].atrisk_rate;
      const diff = last - prev;
      if (Math.abs(diff) < 0.5) return {text:"→ stabil", cls:"flat"};
      return diff > 0 ? {text:`↑ +${diff.toFixed(1)}%`, cls:"up"} : {text:`↓ ${diff.toFixed(1)}%`, cls:"down"};
    }

    function renderKpis(data) {
      const k = data.kpis;
      const arrow = trendArrow();
      const items = [
        ["Mahasiswa Dipantau", fmt.format(k.rows), `${k.presentations} presentation`, ""],
        ["Prediksi AtRisk", fmt.format(k.atrisk), pct(k.atrisk_rate)+" dari total", `<span class="trend ${arrow.cls}">${arrow.text}</span>`],
        ["High Risk", fmt.format(k.high_risk), "prioritas kontak", ""],
        ["Medium Risk", fmt.format(k.medium_risk), "observasi berkala", ""],
        ["Unregistration Rate", pct(k.unreg_rate), "sinyal early dropout", ""],
      ];
      document.getElementById("kpis").innerHTML = items.map(([label, value, note, extra]) => `
        <article class="kpi">${extra}<div class="label">${label}</div><div class="value">${value}</div><div class="note">${note}</div></article>
      `).join("");
    }

    function renderBars(target, items, valueKey="value") {
      const max = Math.max(...items.map(i=>Number(i[valueKey])),1);
      document.getElementById(target).innerHTML = items.map(item => {
        const value = Number(item[valueKey]);
        const width = value/max*100;
        const label = item.label??item.module;
        const displayLabel = signalLabels[label]||label;
        const color = colors[label]||"#2563eb";
        return `<div class="bar-row"><div class="bar-label" title="${displayLabel}">${displayLabel}</div><div class="bar-track"><div class="bar-fill" style="width:${width}%;background:${color}"></div></div><div class="bar-value">${typeof value==="number"&&value<100?pct(value):fmt.format(value)}</div></div>`;
      }).join("");
    }

    function renderModuleBars(data) {
      // Show rate + volume context
      const el = document.getElementById("moduleBars");
      const items = data.moduleSummary;
      const maxRate = Math.max(...items.map(i=>i.atrisk_rate),1);
      el.innerHTML = items.map(item => {
        const width = item.atrisk_rate/maxRate*100;
        return `<div class="bar-row"><div class="bar-label">${item.module} <span class="muted" style="font-size:11px;">(${fmt.format(item.total)})</span></div><div class="bar-track"><div class="bar-fill" style="width:${width}%;background:${item.atrisk_rate>55?'var(--red)':item.atrisk_rate>45?'var(--amber)':'var(--green)'}"></div></div><div class="bar-value">${pct(item.atrisk_rate)}</div></div>`;
      }).join("");
    }

    function renderCooccurrence() {
      const items = DATA.signalCooccurrence;
      const max = Math.max(...items.map(i=>i.count),1);
      document.getElementById("cooccurrence").innerHTML = items.map(item => {
        const h = Math.max(item.count/max*50, 4);
        return `<div class="col"><div class="col-value">${fmt.format(item.count)}</div><div class="col-bar" style="height:${h}px;${item.signals>=4?'background:var(--red)':item.signals>=2?'background:var(--amber)':'background:var(--green)'}"></div><div class="col-label">${item.signals} sinyal</div></div>`;
      }).join("");
    }

    function renderTrend() {
      const items = DATA.trend;
      const max = Math.max(...items.map(i=>i.atrisk_rate),100);
      const el = document.getElementById("trendChart");
      el.innerHTML = `<div style="display:flex;align-items:flex-end;gap:12px;height:100px;padding:16px 0 8px;">` +
        items.map(item => {
          const h = Math.max(item.atrisk_rate/max*70, 8);
          return `<div style="display:flex;flex-direction:column;align-items:center;flex:1;"><span style="font-size:12px;font-weight:700;color:var(--ink);">${pct(item.atrisk_rate)}</span><div style="width:100%;max-width:48px;height:${h}px;background:${item.atrisk_rate>55?'var(--red)':item.atrisk_rate>45?'var(--amber)':'var(--blue)'};border-radius:4px 4px 0 0;margin:4px 0;"></div><span style="font-size:11px;color:var(--muted);">${item.presentation}</span><span style="font-size:10px;color:var(--muted);">${fmt.format(item.total)} mhs</span></div>`;
        }).join("") + `</div>`;
      // Benchmark
      document.getElementById("benchmark").innerHTML = `<span>⚠️</span><span>Referensi: rata-rata dropout rate pendidikan tinggi UK ~25–30% (HESA). AtRisk rate OULAD lebih tinggi karena mencakup Fail + Withdrawn.</span>`;
    }

    function renderSuccess() {
      const s = DATA.successMetrics;
      document.getElementById("successPanel").innerHTML = `
        <b style="display:block;margin-bottom:8px;color:#166534;">${fmt.format(s.successful_count)} mahasiswa berhasil (${s.successful_pct}%)</b>
        <div style="font-size:13px;line-height:1.6;">
          • <b>${fmt.format(s.distinction_count)}</b> meraih Distinction (${s.distinction_pct}%)<br>
          • Rata-rata klik VLE mahasiswa berhasil: <b>${fmt.format(s.avg_vle_clicks_successful)}</b><br>
          • Rata-rata skor assessment: <b>${s.avg_assessment_score_successful}</b><br>
          • <b>${fmt.format(s.low_risk_count)}</b> mahasiswa dalam kategori Low Risk
        </div>
        <div style="margin-top:10px;font-size:12px;color:#15803d;">Indikator ini dapat dijadikan target engagement minimum untuk mahasiswa berisiko.</div>
      `;
    }

    function renderDecisionPanels(data) {
      const k = data.kpis;
      const topMod = data.moduleSummary[0];
      const summaryItems = [
        [`${fmt.format(k.high_risk)} mahasiswa High Risk`, "Perlu kontak akademik dan counselling segera."],
        [`${fmt.format(k.medium_risk)} mahasiswa Medium Risk`, "Masukkan ke daftar observasi berkala, cek engagement."],
      ];
      if (topMod) summaryItems.push([`Module ${topMod.module}: AtRisk rate ${pct(topMod.atrisk_rate)}`, `${fmt.format(topMod.atrisk)} dari ${fmt.format(topMod.total)} mahasiswa berisiko.`]);
      document.getElementById("decisionSummary").innerHTML = summaryItems.map(([t,b])=>`<div class="action-item"><b>${t}</b><span>${b}</span></div>`).join("");
      document.getElementById("actionPlan").innerHTML = [
        ["Hubungi High Risk","Mahasiswa dengan unregistration + aktivitas rendah + assessment lemah."],
        ["Periksa module merah","Lihat area dengan AtRisk rate tertinggi untuk fokus tutor."],
        ["Pantau engagement","Gunakan sinyal VLE dan assessment sebagai indikator awal."]
      ].map(([t,b])=>`<div class="action-item"><b>${t}</b><span>${b}</span></div>`).join("");
    }

    function riskPill(level) {
      const cls = level==="High Risk"?"pill-high":level==="Medium Risk"?"pill-medium":"pill-low";
      return `<span class="pill ${cls}">${level}</span>`;
    }
    function explainSignals(signals) {
      const parts = String(signals||"none").split("|").filter(p=>p&&p!=="none");
      if (!parts.length) return "<span class='muted'>—</span>";
      return parts.map(p=>signalLabels[p]||p).join(", ");
    }
    function suggestAction(row) {
      if (row.knowledge_risk_level==="High Risk") return "Kontak segera";
      if (String(row.knowledge_risk_signals).includes("low_assessment")) return "Review assessment";
      if (String(row.knowledge_risk_signals).includes("low_vle")) return "Dorong engagement";
      return "Observasi berkala";
    }

    function renderTables(data) {
      document.getElementById("presentationRows").innerHTML = data.presentationSummary.map(row=>`
        <tr><td>${row.module}</td><td>${row.presentation}</td><td>${fmt.format(row.total)}</td><td>${pct(row.atrisk_rate)}</td><td>${fmt.format(row.high)}</td><td>${fmt.format(row.medium)}</td></tr>
      `).join("");
      const priorities = data.priorityStudents;
      document.getElementById("priorityRows").innerHTML = priorities.length
        ? priorities.map(row=>`<tr><td>${row.id_student}</td><td>${row.code_module}-${row.code_presentation}</td><td>${riskPill(row.knowledge_risk_level)}</td><td>${Number(row.priority_score).toFixed(2)}</td><td>${row.vle_last_activity_day!=null?`Hari ke-${Math.round(row.vle_last_activity_day)}`:'<span class="muted">—</span>'}</td><td>${explainSignals(row.knowledge_risk_signals)}</td><td>${suggestAction(row)}</td></tr>`).join("")
        : `<tr><td colspan="7" class="muted" style="text-align:center;padding:20px">Tidak ada data untuk filter ini</td></tr>`;
    }

    function renderAll() {
      const data = getFilteredData();
      renderKpis(data);
      renderBars("knowledgeBars", data.knowledgeDistribution);
      renderModuleBars(data);
      renderDecisionPanels(data);
      renderTables(data);
    }

    function initFilter() {
      const select = document.getElementById("moduleFilter");
      DATA.moduleSummary.forEach(row=>{
        const opt=document.createElement("option");
        opt.value=row.module;
        opt.textContent=`${row.module} (${fmt.format(row.total)} mhs)`;
        select.appendChild(opt);
      });
      select.addEventListener("change",e=>{
        currentModule=e.target.value;
        const status=document.getElementById("filterStatus");
        if(currentModule==="all"){status.classList.remove("active");}
        else{status.textContent=`Menampilkan: Module ${currentModule}`;status.classList.add("active");}
        renderAll();
      });
    }

    function init() {
      document.getElementById("bestModel").textContent=DATA.bestModel;
      document.getElementById("generatedAt").textContent="Dashboard dibuat: "+DATA.generated_at;
      initFilter();
      renderAll();
      // Static panels (not affected by filter)
      renderCooccurrence();
      renderTrend();
      renderSuccess();
    }
    init();
  </script>
</body>
</html>
"""


def build_dashboard(output_path: str | Path = DASHBOARD_PATH) -> Path:
    data = build_dashboard_data()
    html = HTML_TEMPLATE.replace("__DASHBOARD_DATA__", json.dumps(data, ensure_ascii=False))
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path


if __name__ == "__main__":
    path = build_dashboard()
    print(f"Wrote dashboard to {path}")
