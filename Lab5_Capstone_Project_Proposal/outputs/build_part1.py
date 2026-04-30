#!/usr/bin/env python3
"""Part 1: Build HEAD + CSS + opening body."""
import os

PART1 = r"""<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Mars Analog Site Suitability in Northeastern Thailand</title>

<!-- Leaflet (interactive map with zoom down to sub-district / tambon level) -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<!-- Fonts: Inter for EN, Sarabun for Thai -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
:root {
  --mars-dark-red:#7a1e1e; --mars-rust:#b5502c; --mars-rust-2:#d07a4c;
  --mars-sand:#e9d6b8; --mars-sand-2:#f6ecdb; --mars-dark:#2b2523;
  --mars-gray:#4a4340; --mars-light:#f9f6f1; --mars-white:#ffffff;
  --mars-border:#e4d9c6; --mars-shadow:0 4px 16px rgba(60,30,15,0.08);
  --mars-shadow-lg:0 10px 30px rgba(60,30,15,0.12);
  --mars-accent:#c45a2a; --mars-green:#6a8c5a; --mars-blue:#3d6b89;
}
* { box-sizing:border-box; }
html, body { margin:0; padding:0; }
body {
  font-family:'Inter','Segoe UI',Helvetica,Arial,sans-serif;
  background:
    radial-gradient(1200px 600px at 85% -10%, rgba(181,80,44,0.08), transparent 70%),
    radial-gradient(1000px 500px at -10% 110%, rgba(122,30,30,0.06), transparent 70%),
    var(--mars-light);
  color:var(--mars-dark); line-height:1.6;
}
html[data-lang="th"] body { font-family:'Sarabun','Inter',sans-serif; }
h1,h2,h3,h4 { font-family:'Space Grotesk','Inter',sans-serif; color:var(--mars-dark); letter-spacing:-0.01em; margin:0 0 0.4em 0; }
html[data-lang="th"] h1,
html[data-lang="th"] h2,
html[data-lang="th"] h3,
html[data-lang="th"] h4 { font-family:'Sarabun',sans-serif; font-weight:700; }
h1 { font-size:2.2rem; font-weight:700; }
h2 { font-size:1.5rem; font-weight:600; }
h3 { font-size:1.15rem; font-weight:600; }
h4 { font-size:1rem; font-weight:600; color:var(--mars-gray); }
p  { margin:0 0 0.8em 0; color:var(--mars-gray); }
a  { color:var(--mars-dark-red); text-decoration:none; }
.container { max-width:1280px; margin:0 auto; padding:24px; }

/* language visibility */
[data-i18n-th], [data-i18n-en] { }
html[data-lang="en"] [data-i18n-th] { display:none !important; }
html[data-lang="th"] [data-i18n-en] { display:none !important; }

/* Language toggle (fixed top-right) */
.lang-toggle {
  position:fixed; top:16px; right:16px; z-index:2000;
  display:flex; background:rgba(43,37,35,0.92); padding:4px; border-radius:999px;
  box-shadow:var(--mars-shadow-lg); border:1px solid rgba(255,255,255,0.12);
  backdrop-filter:blur(8px);
}
.lang-toggle button {
  background:transparent; border:none; color:#f6ecdb; padding:6px 14px;
  font-weight:600; font-size:0.82rem; border-radius:999px; cursor:pointer;
  transition:all 0.2s; letter-spacing:0.04em;
}
.lang-toggle button.active {
  background:linear-gradient(135deg, var(--mars-dark-red), var(--mars-rust));
  color:#fff; box-shadow:0 2px 6px rgba(0,0,0,0.3);
}
.lang-toggle button:hover:not(.active) { color:#fff; }

/* HEADER */
.header {
  background: linear-gradient(135deg, #3a1818 0%, #7a1e1e 45%, #b5502c 100%);
  color:var(--mars-white); padding:48px 24px 56px 24px;
  position:relative; overflow:hidden; border-bottom:4px solid var(--mars-rust-2);
}
.header::before {
  content:""; position:absolute; inset:0;
  background-image:
    radial-gradient(circle at 20% 30%, rgba(255,255,255,0.08) 0 2px, transparent 3px),
    radial-gradient(circle at 70% 60%, rgba(255,255,255,0.05) 0 2px, transparent 3px),
    radial-gradient(circle at 50% 80%, rgba(255,255,255,0.06) 0 2px, transparent 3px);
  background-size:120px 120px, 180px 180px, 90px 90px; opacity:0.6; pointer-events:none;
}
.header-inner { max-width:1280px; margin:0 auto; position:relative; z-index:1; }
.course-pill {
  display:inline-block; background:rgba(255,255,255,0.14); border:1px solid rgba(255,255,255,0.3);
  padding:6px 14px; border-radius:999px; font-size:0.8rem; font-weight:500;
  letter-spacing:0.06em; text-transform:uppercase; margin-bottom:14px;
}
.header h1 { color:var(--mars-white); font-size:2.6rem; margin-bottom:8px; }
.header .subtitle { color:var(--mars-sand); font-size:1.1rem; font-weight:400; margin-bottom:18px; }
.header .overview { max-width:820px; color:rgba(255,255,255,0.92); font-size:0.98rem; }

section { padding:48px 0 12px 0; }
.section-title { display:flex; align-items:center; gap:12px; margin-bottom:6px; }
.section-title .num {
  width:34px; height:34px; border-radius:10px; background:var(--mars-dark-red); color:white;
  display:inline-flex; align-items:center; justify-content:center;
  font-family:'Space Grotesk'; font-weight:700; font-size:0.95rem;
}
.section-sub { color:var(--mars-gray); max-width:820px; margin-bottom:24px; }
.card {
  background:var(--mars-white); border:1px solid var(--mars-border);
  border-radius:14px; padding:22px; box-shadow:var(--mars-shadow);
  transition:transform .2s ease, box-shadow .2s ease;
}
.card:hover { transform:translateY(-2px); box-shadow:var(--mars-shadow-lg); }
.card h3 { margin-top:0; }
.card .label {
  font-size:0.72rem; text-transform:uppercase; letter-spacing:0.1em;
  color:var(--mars-rust); font-weight:600; margin-bottom:8px;
}
.grid { display:grid; gap:22px; }
.grid-2 { grid-template-columns:repeat(2, minmax(0, 1fr)); }
.grid-3 { grid-template-columns:repeat(3, minmax(0, 1fr)); }
.grid-4 { grid-template-columns:repeat(4, minmax(0, 1fr)); }
@media (max-width:1100px){
  .grid-4{grid-template-columns:repeat(2,minmax(0,1fr));}
  .grid-3{grid-template-columns:repeat(2,minmax(0,1fr));}
}
@media (max-width:700px){
  .grid-4,.grid-3,.grid-2{grid-template-columns:1fr;}
  .header h1{font-size:1.9rem;}
}
.workflow { display:flex; flex-wrap:wrap; align-items:center; gap:10px; margin-top:14px; }
.wf-step {
  flex:1 1 160px; background:linear-gradient(180deg, #fff, var(--mars-sand-2));
  border:1px solid var(--mars-border); border-radius:12px; padding:14px 12px;
  text-align:center; min-width:140px; box-shadow:var(--mars-shadow);
}
.wf-step .ic {
  width:34px; height:34px; margin:0 auto 6px auto; background:var(--mars-dark-red); color:white;
  border-radius:10px; display:flex; align-items:center; justify-content:center;
  font-weight:700; font-family:'Space Grotesk';
}
.wf-step strong { display:block; font-size:0.92rem; color:var(--mars-dark); }
.wf-step small  { color:var(--mars-gray); font-size:0.78rem; }
.wf-arrow { color:var(--mars-rust); font-weight:bold; font-size:1.3rem; }
@media (max-width:700px){ .wf-arrow{transform:rotate(90deg);} }
.formula {
  background:var(--mars-dark); color:var(--mars-sand);
  padding:16px 20px; border-radius:12px;
  font-family:'Space Grotesk', monospace; font-size:1rem;
  margin-top:14px; border-left:4px solid var(--mars-rust-2); overflow-x:auto;
}
.formula .weight { color:var(--mars-rust-2); font-weight:700; }
.variables { display:flex; flex-wrap:wrap; gap:10px; margin-top:10px; }
.var-chip {
  display:inline-flex; align-items:center; gap:6px; padding:6px 12px; border-radius:999px;
  background:var(--mars-sand-2); border:1px solid var(--mars-border);
  font-size:0.85rem; color:var(--mars-dark); font-weight:500;
}
.var-dot { width:8px; height:8px; border-radius:50%; display:inline-block; }

/* Colored TIFF panel */
.map-panel .tiff-img {
  width:100%; aspect-ratio:4/3; border-radius:10px;
  background:linear-gradient(135deg, #fff, var(--mars-sand-2));
  border:1px solid var(--mars-border);
  display:block; object-fit:cover; margin-bottom:14px;
}
.legend {
  display:flex; flex-wrap:wrap; gap:8px; margin-top:10px;
  padding:10px 12px; background:var(--mars-sand-2);
  border-radius:10px; border:1px solid var(--mars-border);
}
.legend .swatch { display:inline-flex; align-items:center; gap:6px; font-size:0.78rem; color:var(--mars-gray); }
.legend .sw { width:14px; height:14px; border-radius:3px; display:inline-block; border:1px solid rgba(0,0,0,0.08); }
.legend .gradient-bar {
  width:100%; height:12px; border-radius:6px; margin-bottom:4px;
}
.legend-labels {
  display:flex; justify-content:space-between; font-size:0.72rem; color:var(--mars-gray);
}
.callout {
  margin-top:12px; padding:10px 12px; border-left:3px solid var(--mars-rust);
  background:#fff7ee; color:var(--mars-dark); border-radius:6px; font-size:0.88rem;
}
.compare-box {
  background:linear-gradient(135deg, #fff, var(--mars-sand-2));
  border:1px solid var(--mars-border); border-radius:14px;
  padding:20px 22px; margin-top:22px;
}
.compare-grid { display:grid; grid-template-columns:repeat(3, 1fr); gap:18px; }
@media (max-width:800px){ .compare-grid{grid-template-columns:1fr;} }
.compare-item h4 { color:var(--mars-dark-red); margin-bottom:6px; }
.stat {
  text-align:left; padding:22px;
  background:linear-gradient(140deg, #fff 60%, var(--mars-sand-2));
  border:1px solid var(--mars-border); border-radius:14px; box-shadow:var(--mars-shadow);
}
.stat .num {
  font-family:'Space Grotesk'; font-size:2.1rem; font-weight:700;
  color:var(--mars-dark-red); line-height:1; margin:4px 0 6px 0;
}
.stat .lbl {
  font-size:0.82rem; letter-spacing:0.06em; text-transform:uppercase;
  color:var(--mars-gray); font-weight:600;
}
.stat .sub { font-size:0.8rem; color:var(--mars-gray); margin-top:4px; }
.table-wrap {
  overflow-x:auto; border:1px solid var(--mars-border);
  border-radius:14px; background:white; box-shadow:var(--mars-shadow);
}
table { width:100%; border-collapse:collapse; font-size:0.9rem; }
th, td { padding:12px 14px; text-align:left; border-bottom:1px solid var(--mars-border); }
th {
  background:var(--mars-sand-2); color:var(--mars-dark); font-weight:600;
  font-size:0.78rem; text-transform:uppercase; letter-spacing:0.06em;
}
tbody tr:hover { background:#fff9ef; cursor:pointer; }
.rank {
  display:inline-block; min-width:26px; padding:2px 8px; border-radius:6px;
  background:var(--mars-dark-red); color:white; font-weight:600; font-size:0.78rem; text-align:center;
}
.chart-card { background:white; border:1px solid var(--mars-border); border-radius:14px; padding:20px; box-shadow:var(--mars-shadow); }
.chart-wrap { position:relative; width:100%; height:260px; }
.rq-block {
  padding:18px; background:white; border:1px solid var(--mars-border);
  border-left:4px solid var(--mars-dark-red); border-radius:10px; box-shadow:var(--mars-shadow);
}
.rq-block h4 { color:var(--mars-dark-red); margin-bottom:6px; }
footer {
  margin-top:50px; background:var(--mars-dark);
  color:var(--mars-sand); padding:36px 24px;
}
footer .container { display:grid; grid-template-columns:2fr 1fr 1fr; gap:24px; }
@media (max-width:800px){ footer .container{grid-template-columns:1fr;} }
footer h4 { color:var(--mars-sand-2); margin-bottom:8px; }
footer p, footer li { color:rgba(255,255,255,0.75); font-size:0.85rem; }
footer ul { list-style:none; padding:0; margin:0; }
footer li { margin-bottom:4px; }
footer .copyright {
  border-top:1px solid rgba(255,255,255,0.1); text-align:center;
  padding-top:14px; margin-top:20px; font-size:0.8rem; color:rgba(255,255,255,0.5);
}

/* Leaflet map */
.leaflet-map-wrap {
  position:relative; width:100%;
  background:#222; border-radius:14px; overflow:hidden;
  border:1px solid var(--mars-border); box-shadow:var(--mars-shadow-lg);
}
#isanMap { width:100%; height:640px; border-radius:14px; }
.map-toolbar {
  display:flex; flex-wrap:wrap; gap:10px; margin-bottom:14px; align-items:center;
  background:white; border:1px solid var(--mars-border); border-radius:12px; padding:10px 14px;
  box-shadow:var(--mars-shadow);
}
.map-toolbar label {
  font-size:0.82rem; font-weight:600; color:var(--mars-gray);
  display:inline-flex; align-items:center; gap:6px; cursor:pointer;
  padding:4px 10px; border-radius:6px; transition:background 0.15s;
}
.map-toolbar label:hover { background:var(--mars-sand-2); }
.map-toolbar button {
  border:1px solid var(--mars-border); background:white; color:var(--mars-dark);
  padding:6px 12px; border-radius:6px; font-size:0.82rem; cursor:pointer;
  font-weight:600; transition:all 0.15s;
}
.map-toolbar button:hover { background:var(--mars-dark-red); color:white; border-color:var(--mars-dark-red); }
.map-toolbar select {
  border:1px solid var(--mars-border); border-radius:6px; padding:5px 10px;
  font-size:0.82rem; background:white; color:var(--mars-dark); font-weight:500;
}
.map-legend {
  position:absolute; bottom:16px; right:16px; z-index:1000;
  background:rgba(255,255,255,0.96); padding:12px 14px; border-radius:10px;
  border:1px solid var(--mars-border); box-shadow:var(--mars-shadow);
  font-size:0.8rem; max-width:230px;
}
.map-legend h4 {
  margin:0 0 8px 0; font-size:0.82rem; color:var(--mars-dark-red);
  text-transform:uppercase; letter-spacing:0.06em; font-weight:700;
}
.map-legend .row {
  display:flex; align-items:center; gap:8px; margin-bottom:4px;
  font-size:0.78rem; color:var(--mars-gray);
}
.map-legend .sw {
  width:16px; height:12px; display:inline-block; border-radius:3px;
  border:1px solid rgba(0,0,0,0.1);
}
.leaflet-popup-content-wrapper {
  border-radius:10px; box-shadow:var(--mars-shadow-lg);
  border-top:3px solid var(--mars-dark-red);
}
.leaflet-popup-content { margin:12px 16px; font-size:0.88rem; color:var(--mars-dark); }
.leaflet-popup-content h4 { margin:0 0 6px 0; color:var(--mars-dark-red); font-family:'Space Grotesk'; font-size:1rem; }
.leaflet-popup-content table { font-size:0.82rem; margin-top:4px; }
.leaflet-popup-content table td { padding:2px 6px 2px 0; border:none; color:var(--mars-gray); }
.leaflet-popup-content table td:last-child { color:var(--mars-dark); font-weight:600; }

.zoom-hint {
  background:linear-gradient(90deg, var(--mars-dark-red), var(--mars-rust));
  color:#fff; padding:8px 14px; border-radius:8px;
  font-size:0.8rem; margin-bottom:12px;
  display:inline-flex; gap:8px; align-items:center;
}
.zoom-hint b { color:var(--mars-sand-2); }
</style>
</head>
<body>

<!-- LANGUAGE TOGGLE (fixed top-right) -->
<div class="lang-toggle" role="group" aria-label="Language switcher">
  <button id="btnLangEN" class="active" onclick="setLang('en')">EN</button>
  <button id="btnLangTH" onclick="setLang('th')">ไทย</button>
</div>
"""

out = "/sessions/intelligent-youthful-babbage/part1.html"
with open(out,"w",encoding="utf-8") as f:
    f.write(PART1)
print("OK", len(PART1), "chars")
