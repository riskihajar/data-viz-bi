from __future__ import annotations

import json
from collections import Counter, defaultdict
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
    base_score = {"High Risk": 0.85, "Medium Risk": 0.55, "Low Risk": 0.2}[row["knowledge_risk_level"]]
    signal_count = 0 if row["knowledge_risk_signals"] == "none" else len(row["knowledge_risk_signals"].split("|"))
    return min(base_score + (signal_count * 0.03), 0.99)


def _priority_students(df: pd.DataFrame) -> list[dict[str, object]]:
    priority = df[df["knowledge_risk_level"].isin(["High Risk", "Medium Risk"])].copy()
    priority["priority_score"] = priority.apply(_priority_score, axis=1)
    risk_order = {"High Risk": 0, "Medium Risk": 1, "Low Risk": 2}
    priority["risk_order"] = priority["knowledge_risk_level"].map(risk_order)
    priority = priority.sort_values(["risk_order", "priority_score"], ascending=[True, False])
    columns = [
        "code_module",
        "code_presentation",
        "id_student",
        "priority_score",
        "knowledge_risk_level",
        "knowledge_risk_signals",
    ]
    return priority[columns].head(30).to_dict(orient="records")


def build_dashboard_data() -> dict[str, object]:
    df = pd.read_csv(DATASET_PATH)
    for col in [
        "assessment_count",
        "assessment_score_mean",
        "vle_total_clicks",
        "vle_active_days",
        "has_unregistration",
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["knowledge_risk_level"] = df.apply(apply_knowledge_risk_layer, axis=1)
    df["knowledge_risk_signals"] = df.apply(_risk_signals, axis=1)
    experiment_summary = run_experiment(DATASET_PATH)
    high_risk = int((df["knowledge_risk_level"] == "High Risk").sum())
    medium_risk = int((df["knowledge_risk_level"] == "Medium Risk").sum())

    signal_counts: defaultdict[str, int] = defaultdict(int)
    for signals in df["knowledge_risk_signals"]:
        for signal in str(signals).split("|"):
            if signal and signal != "none":
                signal_counts[signal] += 1

    return {
        "kpis": {
            "rows": len(df),
            "modules": int(df["code_module"].nunique()),
            "presentations": int(df["code_presentation"].nunique()),
            "atrisk": int((df["risk_label"] == "AtRisk").sum()),
            "atrisk_rate": round((df["risk_label"] == "AtRisk").mean() * 100, 2),
            "high_risk": high_risk,
            "intervention_queue": high_risk + medium_risk,
            "medium_risk": medium_risk,
        },
        "labelDistribution": _counter_to_items(Counter(df["risk_label"])),
        "finalResultDistribution": _counter_to_items(Counter(df["final_result"])),
        "knowledgeDistribution": _counter_to_items(Counter(df["knowledge_risk_level"])),
        "moduleSummary": _module_summary(df),
        "presentationSummary": _presentation_summary(df),
        "signalCounts": _counter_to_items(Counter(signal_counts)),
        "modelResults": experiment_summary["model_results"],
        "bestModel": experiment_summary["best_model"],
        "priorityStudents": _priority_students(df),
    }


HTML_TEMPLATE = r"""<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Academic Risk Intervention Dashboard</title>
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
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
      letter-spacing: 0;
    }
    header {
      background: #102033;
      color: white;
      padding: 22px 28px 18px;
      border-bottom: 4px solid var(--teal);
    }
    header h1 {
      margin: 0 0 6px;
      font-size: clamp(24px, 3vw, 36px);
      font-weight: 750;
      letter-spacing: 0;
    }
    header p { margin: 0; color: #c8d3df; max-width: 960px; line-height: 1.45; }
    main { padding: 22px 28px 32px; max-width: 1440px; margin: 0 auto; }
    .toolbar {
      display: flex;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 18px;
      flex-wrap: wrap;
    }
    .toolbar select, .toolbar input {
      border: 1px solid var(--line);
      background: white;
      min-height: 38px;
      padding: 8px 10px;
      border-radius: 6px;
      font: inherit;
      color: var(--text);
    }
    .toolbar label { color: var(--muted); font-size: 13px; display: grid; gap: 4px; }
    .kpis {
      display: grid;
      grid-template-columns: repeat(6, minmax(130px, 1fr));
      gap: 12px;
      margin-bottom: 18px;
    }
    .kpi, .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 1px 2px rgba(16, 32, 51, .04);
    }
    .kpi { padding: 14px; min-height: 96px; }
    .kpi .label { color: var(--muted); font-size: 12px; text-transform: uppercase; font-weight: 700; }
    .kpi .value { font-size: clamp(22px, 2.8vw, 34px); font-weight: 780; margin-top: 8px; color: var(--ink); }
    .kpi .note { color: var(--muted); font-size: 12px; margin-top: 2px; }
    .grid {
      display: grid;
      grid-template-columns: 1.1fr .9fr;
      gap: 14px;
      margin-bottom: 14px;
    }
    .grid-3 {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 14px;
    }
    .panel { padding: 16px; overflow: hidden; }
    .panel h2 {
      margin: 0 0 12px;
      font-size: 16px;
      line-height: 1.25;
    }
    .bar-row { display: grid; grid-template-columns: 130px 1fr 70px; gap: 10px; align-items: center; margin: 10px 0; }
    .bar-label { color: var(--ink); font-size: 13px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .bar-track { height: 18px; background: #e8edf3; border-radius: 5px; overflow: hidden; }
    .bar-fill { height: 100%; border-radius: 5px; }
    .bar-value { color: var(--muted); font-variant-numeric: tabular-nums; text-align: right; font-size: 12px; }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }
    th, td {
      border-bottom: 1px solid var(--line);
      padding: 9px 8px;
      text-align: left;
      vertical-align: top;
    }
    th { color: var(--muted); font-size: 12px; font-weight: 750; background: #f9fafb; position: sticky; top: 0; }
    .scroll { max-height: 390px; overflow: auto; border: 1px solid var(--line); border-radius: 6px; }
    .pill {
      display: inline-block;
      padding: 3px 7px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
    }
    .pill-high { background: #fee2e2; color: #991b1b; }
    .pill-medium { background: #fef3c7; color: #92400e; }
    .pill-low { background: #dcfce7; color: #166534; }
    .pill-atrisk { background: #e0e7ff; color: #3730a3; }
    .stack { display: flex; width: 100%; height: 18px; overflow: hidden; border-radius: 5px; background: #e8edf3; }
    .stack span { height: 100%; display: block; }
    .legend { display: flex; gap: 12px; flex-wrap: wrap; color: var(--muted); font-size: 12px; margin-top: 10px; }
    .legend i { width: 10px; height: 10px; display: inline-block; border-radius: 2px; margin-right: 4px; }
    .muted { color: var(--muted); }
    .decision-note {
      border-left: 4px solid var(--teal);
      background: #eef7f5;
      padding: 12px 14px;
      border-radius: 6px;
      color: #164e45;
      line-height: 1.45;
      margin-bottom: 12px;
    }
    .action-list { display: grid; gap: 9px; }
    .action-item {
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px 12px;
      background: #fbfcfd;
      line-height: 1.4;
    }
    .action-item b { display: block; color: var(--ink); margin-bottom: 3px; }
    @media (max-width: 1100px) {
      .kpis { grid-template-columns: repeat(3, minmax(0, 1fr)); }
      .grid, .grid-3 { grid-template-columns: 1fr; }
    }
    @media (max-width: 680px) {
      header, main { padding-left: 16px; padding-right: 16px; }
      .kpis { grid-template-columns: 1fr 1fr; }
      .bar-row { grid-template-columns: 96px 1fr 52px; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Academic Risk Intervention Dashboard</h1>
    <p>Dashboard DVBI untuk membantu pengelola akademik memantau mahasiswa berisiko, menentukan prioritas intervensi, dan membaca alasan risiko dari aktivitas belajar.</p>
  </header>
  <main>
    <section class="toolbar">
      <div class="muted">Audience: pimpinan akademik, program studi, dan tim counselling</div>
      <label>Module
        <select id="moduleFilter"><option value="all">All modules</option></select>
      </label>
    </section>

    <section class="kpis" id="kpis"></section>

    <section class="grid">
      <div class="panel">
        <h2>Segmentasi Risiko Mahasiswa</h2>
        <div class="decision-note">Gunakan kelompok High Risk sebagai prioritas kontak akademik, Medium Risk sebagai observasi berkala, dan Low Risk sebagai monitoring reguler.</div>
        <div id="knowledgeBars"></div>
        <div class="legend">
          <span><i style="background: var(--red)"></i>High Risk</span>
          <span><i style="background: var(--amber)"></i>Medium Risk</span>
          <span><i style="background: var(--green)"></i>Low Risk</span>
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
        <h2>Penyebab Risiko Dominan</h2>
        <div id="signalBars"></div>
      </div>
      <div class="panel">
        <h2>Module dengan Risiko Tertinggi</h2>
        <div id="moduleBars"></div>
      </div>
    </section>

    <section class="grid">
      <div class="panel">
        <h2>Area Akademik Prioritas</h2>
        <div class="scroll">
          <table>
            <thead><tr><th>Module</th><th>Presentation</th><th>Mahasiswa</th><th>AtRisk Rate</th><th>Intervention Rate</th><th>High</th><th>Medium</th></tr></thead>
            <tbody id="presentationRows"></tbody>
          </table>
        </div>
      </div>
      <div class="panel">
        <h2>Daftar Prioritas Intervensi</h2>
        <div class="scroll">
          <table>
            <thead><tr><th>Student</th><th>Module</th><th>Status</th><th>Risk Score</th><th>Alasan Utama</th><th>Aksi</th></tr></thead>
            <tbody id="priorityRows"></tbody>
          </table>
        </div>
      </div>
    </section>
    <section class="panel">
      <h2>Catatan Metodologis</h2>
      <p class="muted">Dashboard ini memakai model <b id="bestModel"></b> sebagai scoring engine dan rule-based risk layer sebagai penjelas risiko. Metrik model tidak ditampilkan sebagai panel utama karena dashboard ini ditujukan untuk keputusan monitoring akademik, bukan evaluasi teknis eksperimen.</p>
    </section>
  </main>

  <script>
    const DATA = __DASHBOARD_DATA__;
    const colors = {
      "High Risk": "#dc2626",
      "Medium Risk": "#d97706",
      "Low Risk": "#16a34a",
      "AtRisk": "#2563eb",
      "Successful": "#0f766e",
      "Fail": "#dc2626",
      "Withdrawn": "#d97706",
      "Pass": "#0f766e",
      "Distinction": "#16a34a"
    };

    const fmt = new Intl.NumberFormat("id-ID");
    const pct = value => `${Number(value).toFixed(2)}%`;
    const signalLabels = {
      low_assessment_score: "Skor assessment rendah",
      low_assessment_count: "Partisipasi assessment rendah",
      low_vle_clicks: "Aktivitas VLE rendah",
      low_vle_active_days: "Hari aktif VLE rendah",
      has_unregistration: "Ada sinyal unregistration"
    };

    function renderKpis(data) {
      const items = [
        ["Mahasiswa Dipantau", fmt.format(data.kpis.rows), "rekaman mahasiswa per module"],
        ["AtRisk", fmt.format(data.kpis.atrisk), pct(data.kpis.atrisk_rate)],
        ["High Risk", fmt.format(data.kpis.high_risk), "kontak prioritas"],
        ["Medium Risk", fmt.format(data.kpis.medium_risk), "observasi berkala"],
        ["Intervention Queue", fmt.format(data.kpis.intervention_queue), "perlu ditinjau tim akademik"],
        ["Module", fmt.format(data.kpis.modules), "area pembelajaran"]
      ];
      document.getElementById("kpis").innerHTML = items.map(([label, value, note]) => `
        <article class="kpi"><div class="label">${label}</div><div class="value">${value}</div><div class="note">${note}</div></article>
      `).join("");
    }

    function renderBars(target, items, valueKey = "value") {
      const max = Math.max(...items.map(item => Number(item[valueKey])), 1);
      document.getElementById(target).innerHTML = items.map(item => {
        const value = Number(item[valueKey]);
        const width = value / max * 100;
        const label = item.label ?? item.module ?? item.signal;
        const displayLabel = signalLabels[label] || label;
        const color = colors[label] || "#2563eb";
        return `<div class="bar-row">
          <div class="bar-label" title="${displayLabel}">${displayLabel}</div>
          <div class="bar-track"><div class="bar-fill" style="width:${width}%;background:${color}"></div></div>
          <div class="bar-value">${fmt.format(value)}</div>
        </div>`;
      }).join("");
    }

    function renderDecisionPanels() {
      const high = DATA.kpis.high_risk;
      const medium = DATA.kpis.medium_risk;
      const queue = DATA.kpis.intervention_queue;
      const topModule = DATA.moduleSummary[0];
      document.getElementById("decisionSummary").innerHTML = [
        [`${fmt.format(high)} mahasiswa High Risk`, "Prioritaskan kontak akademik dan counselling pada kelompok ini."],
        [`${fmt.format(medium)} mahasiswa Medium Risk`, "Masukkan ke daftar observasi berkala dan cek perkembangan engagement."],
        [`${topModule.module} memiliki AtRisk rate tertinggi`, `${pct(topModule.atrisk_rate)} dari ${fmt.format(topModule.total)} mahasiswa pada module ini masuk label AtRisk.`]
      ].map(([title, body]) => `<div class="action-item"><b>${title}</b>${body}</div>`).join("");

      document.getElementById("actionPlan").innerHTML = [
        ["Hubungi High Risk", "Prioritaskan mahasiswa dengan unregistration, aktivitas VLE rendah, dan assessment lemah."],
        ["Cek module-presentation merah", "Lihat area akademik dengan intervention rate tertinggi untuk menentukan fokus dosen wali atau tutor."],
        ["Pantau engagement mingguan", "Gunakan sinyal VLE dan assessment sebagai indikator awal sebelum hasil akhir diketahui."]
      ].map(([title, body]) => `<div class="action-item"><b>${title}</b>${body}</div>`).join("");
    }

    function riskPill(level) {
      const klass = level === "High Risk" ? "pill-high" : level === "Medium Risk" ? "pill-medium" : "pill-low";
      return `<span class="pill ${klass}">${level}</span>`;
    }

    function labelPill(label) {
      return `<span class="pill pill-atrisk">${label}</span>`;
    }

    function explainSignals(signals) {
      const parts = String(signals || "none").split("|").filter(part => part && part !== "none");
      if (!parts.length) return "Tidak ada sinyal dominan";
      return parts.map(part => signalLabels[part] || part).join(", ");
    }

    function suggestAction(row) {
      if (row.knowledge_risk_level === "High Risk") return "Kontak segera";
      if (String(row.knowledge_risk_signals).includes("low_assessment")) return "Review assessment";
      if (String(row.knowledge_risk_signals).includes("low_vle")) return "Dorong engagement";
      return "Observasi berkala";
    }

    function renderTables(module = "all") {
      const presentations = DATA.presentationSummary.filter(row => module === "all" || row.module === module);
      document.getElementById("presentationRows").innerHTML = presentations.map(row => `
        <tr>
          <td>${row.module}</td><td>${row.presentation}</td><td>${fmt.format(row.total)}</td>
          <td>${pct(row.atrisk_rate)}</td><td>${pct(row.priority_rate)}</td>
          <td>${fmt.format(row.high)}</td><td>${fmt.format(row.medium)}</td>
        </tr>
      `).join("");

      const priorities = DATA.priorityStudents.filter(row => module === "all" || row.code_module === module);
      document.getElementById("priorityRows").innerHTML = priorities.map(row => `
        <tr>
          <td>${row.id_student}</td><td>${row.code_module}-${row.code_presentation}</td>
          <td>${riskPill(row.knowledge_risk_level)}</td>
          <td>${Number(row.priority_score).toFixed(2)}</td>
          <td>${explainSignals(row.knowledge_risk_signals)}</td>
          <td>${suggestAction(row)}</td>
        </tr>
      `).join("");
    }

    function renderModuleFilter() {
      const select = document.getElementById("moduleFilter");
      DATA.moduleSummary.forEach(row => {
        const option = document.createElement("option");
        option.value = row.module;
        option.textContent = row.module;
        select.appendChild(option);
      });
      select.addEventListener("change", event => renderTables(event.target.value));
    }

    function init() {
      document.getElementById("bestModel").textContent = DATA.bestModel;
      renderKpis(DATA);
      renderBars("knowledgeBars", DATA.knowledgeDistribution);
      renderBars("signalBars", DATA.signalCounts);
      renderBars("moduleBars", DATA.moduleSummary.map(row => ({ label: row.module, value: row.atrisk_rate })));
      renderDecisionPanels();
      renderModuleFilter();
      renderTables();
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
