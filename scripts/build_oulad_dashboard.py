from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_PATH = ROOT / "assets" / "dashboard" / "oulad-risk-dashboard.html"


def build_dashboard_data() -> dict[str, object]:
    """Final dashboard data synchronized with the day-28 notebook/article."""
    high_risk = 1795
    medium_risk = 1994
    low_risk = 2682
    total_rows = high_risk + medium_risk + low_risk
    priority_count = high_risk + medium_risk

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "scope": {
            "dataset": "Open University Learning Analytics Dataset (OULAD)",
            "unit": "student-module-presentation",
            "horizon": "Day 28 / week 4",
            "split": "20% hold-out test grouped by id_student",
            "model": "Random Forest",
        },
        "kpis": {
            "holdout_rows": total_rows,
            "unique_students": 5757,
            "atrisk_actual": 3398,
            "successful_actual": 3073,
            "priority_queue": priority_count,
            "priority_rate": round(priority_count / total_rows * 100, 1),
            "high_risk": high_risk,
            "medium_risk": medium_risk,
            "low_risk": low_risk,
        },
        "knowledgeDistribution": [
            {"label": "High Risk", "value": high_risk, "pct": 27.7},
            {"label": "Medium Risk", "value": medium_risk, "pct": 30.8},
            {"label": "Low Risk", "value": low_risk, "pct": 41.4},
        ],
        "thresholds": [
            {"label": "Assessment score", "value": 0},
            {"label": "Assessment count", "value": 0},
            {"label": "VLE clicks", "value": 47},
            {"label": "VLE active days", "value": 4},
        ],
        "signals": [
            {"label": "Skor assessment rendah", "value": 2341},
        ],
        "modelMetrics": [
            {"metric": "Accuracy", "rf": 0.7592, "combined": 0.7136},
            {"metric": "Precision AtRisk", "rf": 0.8032, "combined": 0.7039},
            {"metric": "Recall AtRisk", "rf": 0.7172, "combined": 0.7849},
            {"metric": "F1 AtRisk", "rf": 0.7578, "combined": 0.7422},
        ],
        "modelComparison": [
            {"model": "Logistic Regression", "accuracy": 0.7476, "precision": 0.8040, "recall": 0.6869, "f1": 0.7408},
            {"model": "Random Forest", "accuracy": 0.7592, "precision": 0.8032, "recall": 0.7172, "f1": 0.7578},
            {"model": "XGBoost", "accuracy": 0.7633, "precision": 0.8186, "recall": 0.7054, "f1": 0.7578},
        ],
        "confusionMatrix": {
            "labels": ["Successful", "AtRisk"],
            "values": [[2476, 597], [961, 2437]],
        },
        "featureImportance": [
            {"feature": "VLE total clicks", "value": 0.096883},
            {"feature": "VLE last activity day", "value": 0.088235},
            {"feature": "VLE active days", "value": 0.083810},
            {"feature": "VLE site count", "value": 0.079148},
            {"feature": "Assessment score mean", "value": 0.068352},
            {"feature": "Date registration", "value": 0.064697},
            {"feature": "Assessment score min", "value": 0.063415},
        ],
        "modulePriority": [
            {"module": "GGG", "presentation": "2014J", "priority_rate": 100.0, "note": "Proporsi High/Medium Risk tertinggi pada hold-out test"},
        ],
        "insights": [
            "Total antrean intervensi: 3.789 student-module-presentation.",
            "Sinyal risiko paling dominan: skor assessment rendah dengan 2.341 kasus.",
            "Module GGG presentation 2014J memiliki 100,0% kasus High/Medium Risk pada hold-out test.",
            "Knowledge layer meningkatkan recall AtRisk dari 0,7172 menjadi 0,7849 dengan konsekuensi precision turun.",
        ],
        "priorityStudents": [
            {"id_student": 87604, "module": "BBB", "presentation": "2013B", "probability": "100.0%", "level": "High Risk", "signals": 4, "reasons": "Skor assessment rendah; Partisipasi assessment rendah; Total klik VLE rendah; Hari aktif VLE rendah", "action": "pengingat dan monitoring akses VLE; pendampingan assessment; konseling atau tindak lanjut dosen wali"},
            {"id_student": 88580, "module": "BBB", "presentation": "2013B", "probability": "100.0%", "level": "High Risk", "signals": 4, "reasons": "Skor assessment rendah; Partisipasi assessment rendah; Total klik VLE rendah; Hari aktif VLE rendah", "action": "pengingat dan monitoring akses VLE; pendampingan assessment; konseling atau tindak lanjut dosen wali"},
            {"id_student": 185240, "module": "BBB", "presentation": "2013B", "probability": "100.0%", "level": "High Risk", "signals": 4, "reasons": "Skor assessment rendah; Partisipasi assessment rendah; Total klik VLE rendah; Hari aktif VLE rendah", "action": "pengingat dan monitoring akses VLE; pendampingan assessment; konseling atau tindak lanjut dosen wali"},
            {"id_student": 230348, "module": "BBB", "presentation": "2013B", "probability": "100.0%", "level": "High Risk", "signals": 4, "reasons": "Skor assessment rendah; Partisipasi assessment rendah; Total klik VLE rendah; Hari aktif VLE rendah", "action": "pengingat dan monitoring akses VLE; pendampingan assessment; konseling atau tindak lanjut dosen wali"},
            {"id_student": 258402, "module": "BBB", "presentation": "2013B", "probability": "100.0%", "level": "High Risk", "signals": 4, "reasons": "Skor assessment rendah; Partisipasi assessment rendah; Total klik VLE rendah; Hari aktif VLE rendah", "action": "pengingat dan monitoring akses VLE; pendampingan assessment; konseling atau tindak lanjut dosen wali"},
            {"id_student": 269289, "module": "BBB", "presentation": "2013B", "probability": "100.0%", "level": "High Risk", "signals": 4, "reasons": "Skor assessment rendah; Partisipasi assessment rendah; Total klik VLE rendah; Hari aktif VLE rendah", "action": "pengingat dan monitoring akses VLE; pendampingan assessment; konseling atau tindak lanjut dosen wali"},
            {"id_student": 323914, "module": "BBB", "presentation": "2013B", "probability": "100.0%", "level": "High Risk", "signals": 4, "reasons": "Skor assessment rendah; Partisipasi assessment rendah; Total klik VLE rendah; Hari aktif VLE rendah", "action": "pengingat dan monitoring akses VLE; pendampingan assessment; konseling atau tindak lanjut dosen wali"},
            {"id_student": 353918, "module": "BBB", "presentation": "2013B", "probability": "100.0%", "level": "High Risk", "signals": 4, "reasons": "Skor assessment rendah; Partisipasi assessment rendah; Total klik VLE rendah; Hari aktif VLE rendah", "action": "pengingat dan monitoring akses VLE; pendampingan assessment; konseling atau tindak lanjut dosen wali"},
            {"id_student": 357038, "module": "BBB", "presentation": "2013B", "probability": "100.0%", "level": "High Risk", "signals": 4, "reasons": "Skor assessment rendah; Partisipasi assessment rendah; Total klik VLE rendah; Hari aktif VLE rendah", "action": "pengingat dan monitoring akses VLE; pendampingan assessment; konseling atau tindak lanjut dosen wali"},
            {"id_student": 372624, "module": "BBB", "presentation": "2013B", "probability": "100.0%", "level": "High Risk", "signals": 4, "reasons": "Skor assessment rendah; Partisipasi assessment rendah; Total klik VLE rendah; Hari aktif VLE rendah", "action": "pengingat dan monitoring akses VLE; pendampingan assessment; konseling atau tindak lanjut dosen wali"},
        ],
    }


HTML_TEMPLATE = r"""<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dashboard Early Warning OULAD Minggu Ke-4</title>
  <style>
    :root { color-scheme: light; --bg:#f6f7f9; --panel:#fff; --line:#d8dee8; --text:#17202a; --muted:#667085; --blue:#2563eb; --teal:#0f766e; --amber:#d97706; --red:#dc2626; --green:#16a34a; --ink:#263548; }
    * { box-sizing: border-box; }
    body { margin:0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif; background:var(--bg); color:var(--text); }
    header { background:#102033; color:#fff; padding:22px 28px 18px; border-bottom:4px solid var(--teal); }
    header h1 { margin:0 0 4px; font-size:clamp(22px,3vw,32px); font-weight:760; }
    header p { margin:0; color:#c8d3df; max-width:980px; line-height:1.45; font-size:14px; }
    .header-meta { display:flex; gap:14px; flex-wrap:wrap; margin-top:8px; font-size:12px; color:#94a3b8; }
    main { padding:22px 28px 32px; max-width:1440px; margin:0 auto; }
    .kpis { display:grid; grid-template-columns:repeat(5,minmax(130px,1fr)); gap:12px; margin-bottom:16px; }
    .kpi, .panel { background:var(--panel); border:1px solid var(--line); border-radius:8px; box-shadow:0 1px 2px rgba(16,32,51,.04); }
    .kpi { padding:14px; min-height:96px; }
    .label { color:var(--muted); font-size:11px; text-transform:uppercase; font-weight:750; letter-spacing:.02em; }
    .value { font-size:clamp(22px,2.8vw,32px); font-weight:780; margin-top:6px; color:var(--ink); }
    .note { color:var(--muted); font-size:11px; margin-top:2px; line-height:1.35; }
    .grid { display:grid; grid-template-columns:1.05fr .95fr; gap:14px; margin-bottom:14px; }
    .grid-3 { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; margin-bottom:14px; }
    .grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:14px; }
    .panel { padding:16px; overflow:hidden; }
    .panel h2 { margin:0 0 12px; font-size:15px; line-height:1.25; font-weight:720; }
    .decision-note { border-left:4px solid var(--teal); background:#eef7f5; padding:12px 14px; border-radius:6px; color:#164e45; line-height:1.45; margin-bottom:12px; font-size:13px; }
    .bar-row { display:grid; grid-template-columns:170px 1fr 88px; gap:10px; align-items:center; margin:10px 0; }
    .bar-label { color:var(--ink); font-size:13px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    .bar-track { height:18px; background:#e8edf3; border-radius:5px; overflow:hidden; }
    .bar-fill { height:100%; border-radius:5px; }
    .bar-value { color:var(--muted); font-variant-numeric:tabular-nums; text-align:right; font-size:12px; }
    .action-list { display:grid; gap:9px; }
    .action-item { border:1px solid var(--line); border-radius:6px; padding:10px 12px; background:#fbfcfd; line-height:1.4; }
    .action-item b { display:block; color:var(--ink); margin-bottom:3px; font-size:13px; }
    .action-item span { font-size:12px; color:var(--muted); }
    table { width:100%; border-collapse:collapse; font-size:13px; }
    th, td { border-bottom:1px solid var(--line); padding:9px 8px; text-align:left; vertical-align:top; }
    th { color:var(--muted); font-size:11px; font-weight:750; background:#f9fafb; position:sticky; top:0; text-transform:uppercase; letter-spacing:.02em; }
    .scroll { max-height:390px; overflow:auto; border:1px solid var(--line); border-radius:6px; }
    .pill { display:inline-block; padding:3px 7px; border-radius:999px; font-size:11px; font-weight:700; white-space:nowrap; }
    .pill-high { background:#fee2e2; color:#991b1b; }
    .pill-medium { background:#fef3c7; color:#92400e; }
    .pill-low { background:#dcfce7; color:#166534; }
    .matrix { display:grid; grid-template-columns:100px repeat(2,1fr); gap:6px; align-items:stretch; }
    .matrix div { padding:12px; border-radius:6px; background:#f8fafc; text-align:center; font-size:13px; }
    .matrix .head { background:#e8edf3; font-weight:700; color:var(--ink); }
    .matrix .hot { background:#dbeafe; font-size:20px; font-weight:780; color:#1e3a8a; }
    footer { padding:16px 28px; color:var(--muted); font-size:12px; border-top:1px solid var(--line); margin-top:12px; }
    footer .note-box { background:#f9fafb; border:1px solid var(--line); border-radius:6px; padding:12px 14px; line-height:1.5; }
    @media (max-width:1100px) { .kpis { grid-template-columns:repeat(3,minmax(0,1fr)); } .grid,.grid-3,.grid-2 { grid-template-columns:1fr; } }
    @media (max-width:680px) { header, main { padding-left:16px; padding-right:16px; } .kpis { grid-template-columns:1fr 1fr; } .bar-row { grid-template-columns:118px 1fr 56px; } }
  </style>
</head>
<body>
  <header>
    <h1>Dashboard Early Warning OULAD — Minggu Ke-4</h1>
    <p>Dashboard ini mengikuti kondisi final notebook: fitur dibatasi sampai hari ke-28, Random Forest dipilih karena recall AtRisk tertinggi, dan knowledge-based risk layer memakai empat indikator perilaku awal tanpa sinyal unregistration.</p>
    <div class="header-meta">
      <span>Dataset: OULAD 2013-2014</span>
      <span>Unit: student-module-presentation</span>
      <span>Split: hold-out test by id_student</span>
      <span id="generatedAt"></span>
    </div>
  </header>
  <main>
    <section class="kpis" id="kpis"></section>

    <section class="grid">
      <div class="panel">
        <h2>Segmentasi Risiko Hold-Out Test</h2>
        <div class="decision-note">High Risk dan Medium Risk membentuk antrean intervensi. Low Risk tetap dipantau reguler. Level ini berasal dari gabungan prediksi Random Forest dan empat sinyal knowledge layer.</div>
        <div id="knowledgeBars"></div>
      </div>
      <div class="panel">
        <h2>Insight Business Intelligence</h2>
        <div id="insights" class="action-list"></div>
      </div>
    </section>

    <section class="grid-3">
      <div class="panel">
        <h2>Threshold Knowledge Layer</h2>
        <div id="thresholdBars"></div>
      </div>
      <div class="panel">
        <h2>Sinyal Risiko Dominan dari Notebook</h2>
        <div id="signalBars"></div>
      </div>
      <div class="panel">
        <h2>Feature Importance Random Forest</h2>
        <div id="featureBars"></div>
      </div>
    </section>

    <section class="grid-2">
      <div class="panel">
        <h2>Random Forest vs RF + Knowledge Layer</h2>
        <div id="metricBars"></div>
      </div>
      <div class="panel">
        <h2>Perbandingan Model Hold-Out</h2>
        <div class="scroll">
          <table>
            <thead><tr><th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1</th></tr></thead>
            <tbody id="modelRows"></tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="grid">
      <div class="panel">
        <h2>Confusion Matrix Random Forest</h2>
        <div id="confusionMatrix" class="matrix"></div>
      </div>
      <div class="panel">
        <h2>Area Akademik Prioritas</h2>
        <div class="scroll">
          <table>
            <thead><tr><th>Module</th><th>Presentation</th><th>High + Medium Risk</th><th>Catatan</th></tr></thead>
            <tbody id="moduleRows"></tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="panel">
      <h2>Sample Daftar Prioritas Intervensi dari Notebook</h2>
      <div class="scroll">
        <table>
          <thead><tr><th>ID Mahasiswa</th><th>Module</th><th>Probabilitas</th><th>Level</th><th>Jumlah Sinyal</th><th>Alasan Risiko</th><th>Rekomendasi</th></tr></thead>
          <tbody id="priorityRows"></tbody>
        </table>
      </div>
    </section>
  </main>
  <footer>
    <div class="note-box">
      <b>Catatan Metodologis:</b> Dashboard ini merepresentasikan hasil final notebook OULAD early warning pada cut-off hari ke-28. Kolom `date_unregistration` dan `has_unregistration` tidak digunakan sebagai fitur maupun sinyal risiko karena merupakan informasi masa depan untuk skenario intervensi dini.
    </div>
  </footer>
  <script>
    const DATA = __DASHBOARD_DATA__;
    const fmt = new Intl.NumberFormat("id-ID");
    const pct = v => `${(Number(v) * 100).toFixed(2).replace(".", ",")}%`;
    const pctRaw = v => `${Number(v).toFixed(1).replace(".", ",")}%`;
    const colors = {"High Risk":"#dc2626","Medium Risk":"#d97706","Low Risk":"#16a34a"};

    function renderKpis() {
      const k = DATA.kpis;
      const items = [
        ["Hold-out Rows", fmt.format(k.holdout_rows), "baris evaluasi final"],
        ["Mahasiswa Unik", fmt.format(k.unique_students), "grouped split by id_student"],
        ["Priority Queue", fmt.format(k.priority_queue), `${pctRaw(k.priority_rate)} High/Medium Risk`],
        ["High Risk", fmt.format(k.high_risk), "prioritas kontak"],
        ["Recall Gabungan", "78,49%", "RF + Knowledge Layer"],
      ];
      document.getElementById("kpis").innerHTML = items.map(([label, value, note]) => `<article class="kpi"><div class="label">${label}</div><div class="value">${value}</div><div class="note">${note}</div></article>`).join("");
    }

    function renderBars(target, items, opts = {}) {
      const valueKey = opts.valueKey || "value";
      const labelKey = opts.labelKey || "label";
      const max = Math.max(...items.map(i => Number(i[valueKey])), 1);
      document.getElementById(target).innerHTML = items.map(item => {
        const value = Number(item[valueKey]);
        const width = value / max * 100;
        const label = item[labelKey];
        const color = item.color || colors[label] || opts.color || "#2563eb";
        const valueText = opts.percent ? pct(value) : fmt.format(value);
        return `<div class="bar-row"><div class="bar-label" title="${label}">${label}</div><div class="bar-track"><div class="bar-fill" style="width:${width}%;background:${color}"></div></div><div class="bar-value">${valueText}</div></div>`;
      }).join("");
    }

    function renderMetrics() {
      document.getElementById("metricBars").innerHTML = DATA.modelMetrics.map(row => {
        const rf = row.rf * 100;
        const combined = row.combined * 100;
        return `<div style="margin:12px 0;"><div class="bar-label" style="margin-bottom:6px;">${row.metric}</div><div class="bar-track"><div class="bar-fill" style="width:${rf}%;background:#457b9d"></div></div><div class="note">Random Forest: ${pct(row.rf)}</div><div class="bar-track" style="margin-top:5px;"><div class="bar-fill" style="width:${combined}%;background:#e76f51"></div></div><div class="note">RF + Knowledge Layer: ${pct(row.combined)}</div></div>`;
      }).join("");
    }

    function renderTables() {
      document.getElementById("modelRows").innerHTML = DATA.modelComparison.map(row => `<tr><td><b>${row.model}</b></td><td>${pct(row.accuracy)}</td><td>${pct(row.precision)}</td><td>${pct(row.recall)}</td><td>${pct(row.f1)}</td></tr>`).join("");
      document.getElementById("moduleRows").innerHTML = DATA.modulePriority.map(row => `<tr><td>${row.module}</td><td>${row.presentation}</td><td>${pctRaw(row.priority_rate)}</td><td>${row.note}</td></tr>`).join("");
      document.getElementById("priorityRows").innerHTML = DATA.priorityStudents.map(row => `<tr><td>${row.id_student}</td><td>${row.module}-${row.presentation}</td><td>${row.probability}</td><td><span class="pill pill-high">${row.level}</span></td><td>${row.signals}</td><td>${row.reasons}</td><td>${row.action}</td></tr>`).join("");
    }

    function renderConfusionMatrix() {
      const v = DATA.confusionMatrix.values;
      document.getElementById("confusionMatrix").innerHTML = `
        <div></div><div class="head">Pred Successful</div><div class="head">Pred AtRisk</div>
        <div class="head">Actual Successful</div><div class="hot">${fmt.format(v[0][0])}</div><div>${fmt.format(v[0][1])}</div>
        <div class="head">Actual AtRisk</div><div>${fmt.format(v[1][0])}</div><div class="hot">${fmt.format(v[1][1])}</div>`;
    }

    function init() {
      document.getElementById("generatedAt").textContent = "Dashboard dibuat: " + DATA.generated_at;
      renderKpis();
      renderBars("knowledgeBars", DATA.knowledgeDistribution.map(x => ({...x, value:x.value})));
      renderBars("thresholdBars", DATA.thresholds, {color:"#0f766e"});
      renderBars("signalBars", DATA.signals, {color:"#d97706"});
      renderBars("featureBars", DATA.featureImportance, {color:"#2563eb"});
      document.getElementById("insights").innerHTML = DATA.insights.map((text, i) => `<div class="action-item"><b>Insight ${i + 1}</b><span>${text}</span></div>`).join("");
      renderMetrics();
      renderConfusionMatrix();
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
