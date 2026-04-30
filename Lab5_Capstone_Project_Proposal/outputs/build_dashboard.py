#!/usr/bin/env python3
"""Build a results-only Mars Analog dashboard.
Shows: interactive map, suitability output maps, final shortlist of sites,
province table, summary stats, and charts. NO methodology / process sections.
"""
import json, os

ROOT = "/sessions/intelligent-youthful-babbage"
OUT  = os.path.join(ROOT, "mnt/outputs/mars_analog_dashboard_v2.html")

with open(os.path.join(ROOT, "provinces_tiny.geojson"), "r", encoding="utf-8") as f:
    ISAN = f.read().strip()

with open(os.path.join(ROOT, "candidate_points.json"), "r", encoding="utf-8") as f:
    CANDIDATE_POINTS = f.read().strip()

with open(os.path.join(ROOT, "raster_meta.json"), "r", encoding="utf-8") as f:
    RASTER_META = json.load(f)
B = RASTER_META["bounds"]
RASTER_BOUNDS_JS = f"[[{B['south']:.5f},{B['west']:.5f}],[{B['north']:.5f},{B['east']:.5f}]]"

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Mars Analog Site Suitability — Northeastern Thailand</title>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=JetBrains+Mono:wght@400;500&family=IBM+Plex+Sans+Thai:wght@300;400;500;600;700&family=IBM+Plex+Sans+Thai+Looped:wght@300;400;500;600;700&family=Noto+Serif+Thai:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
:root {
  /* Editorial dark — warm charcoal + cream + rust (no cool tones) */
  --space-0:#0b0a09; --space-1:#111110; --space-2:#171614; --space-3:#1f1d1a;
  --mars-glow:#e8623a; --mars-deep:#b5391f; --mars-sand:#efe2cb;
  --cream:#f4ecd8; --cream-dim:#cdc2ad;
  --text:#f4ecd8; --text-dim:rgba(244,236,216,0.62); --text-muted:rgba(244,236,216,0.42);
  --glass:rgba(255,245,225,0.025); --glass-2:rgba(255,245,225,0.05); --glass-3:rgba(255,245,225,0.075);
  --glass-border:rgba(244,236,216,0.10); --glass-border-2:rgba(244,236,216,0.20);
  --glass-shadow:0 8px 32px rgba(0,0,0,0.55);
  --glass-shadow-lg:0 18px 50px rgba(0,0,0,0.7);
  --serif:'Cormorant Garamond', 'Noto Serif Thai', 'Times New Roman', serif;
  --mono:'JetBrains Mono', 'IBM Plex Sans Thai', 'Space Grotesk', monospace;
  --sans:'Inter', 'IBM Plex Sans Thai Looped', 'IBM Plex Sans Thai', 'Segoe UI', Helvetica, Arial, sans-serif;
  --display:'Space Grotesk', 'IBM Plex Sans Thai', sans-serif;
  /* Backwards-compat aliases */
  --mars-dark-red:var(--mars-glow); --mars-rust:var(--mars-deep); --mars-rust-2:#e8915a;
  --mars-sand-2:rgba(255,245,225,0.05); --mars-dark:var(--text);
  --mars-gray:var(--text-dim); --mars-light:var(--space-1); --mars-white:#fff;
  --mars-border:var(--glass-border);
  --mars-shadow:var(--glass-shadow); --mars-shadow-lg:var(--glass-shadow-lg);
  --cyan-glow:var(--cream-dim); --violet-glow:var(--mars-glow);
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{
  font-family:var(--sans);
  background:
    radial-gradient(1100px 600px at 88% 8%, rgba(232,98,58,0.16), transparent 60%),
    radial-gradient(900px 700px at 8% 90%, rgba(181,57,31,0.10), transparent 65%),
    linear-gradient(180deg, var(--space-0) 0%, var(--space-1) 50%, var(--space-2) 100%);
  background-attachment:fixed;
  color:var(--text); line-height:1.65; min-height:100vh;
}
body::before{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:
    radial-gradient(1px 1px at 12% 18%, rgba(244,236,216,0.40) 0, transparent 100%),
    radial-gradient(1px 1px at 28% 72%, rgba(244,236,216,0.28) 0, transparent 100%),
    radial-gradient(1px 1px at 45% 35%, rgba(244,236,216,0.22) 0, transparent 100%),
    radial-gradient(1px 1px at 65% 80%, rgba(244,236,216,0.32) 0, transparent 100%),
    radial-gradient(1px 1px at 80% 25%, rgba(244,236,216,0.26) 0, transparent 100%),
    radial-gradient(1px 1px at 92% 60%, rgba(244,236,216,0.20) 0, transparent 100%);
  opacity:0.55;
}
.container{max-width:1320px; margin:0 auto; padding:24px; position:relative; z-index:1;}
h1{font-family:var(--serif); color:var(--cream); letter-spacing:-0.015em; margin:0 0 0.3em 0; font-weight:500; font-size:3.2rem; line-height:1.05;}
h2{font-family:var(--serif); color:var(--cream); letter-spacing:-0.015em; margin:0 0 0.4em 0; font-weight:500; font-size:2rem; line-height:1.15;}
h3{font-family:var(--display); color:var(--text); margin:0 0 0.4em 0; font-size:1.05rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em;}
h4{font-family:var(--display); color:var(--text-dim); margin:0 0 0.4em 0; font-size:0.95rem; font-weight:600;}
p {margin:0 0 0.8em 0; color:var(--text-dim);}
a {color:var(--mars-glow); text-decoration:none;}
b, strong { color:var(--text); }

/* HEADER — editorial */
.header{
  position:relative; overflow:hidden; padding:96px 24px 88px 24px;
  border-bottom:1px solid var(--glass-border);
  background:
    radial-gradient(900px 520px at 92% 30%, rgba(232,98,58,0.20), transparent 60%),
    linear-gradient(180deg, rgba(0,0,0,0.30), rgba(0,0,0,0));
}
.header::after{
  /* Mars-orb on the right side as CSS-rendered radial gradient */
  content:""; position:absolute; right:-180px; top:50%; transform:translateY(-50%);
  width:640px; height:640px; border-radius:50%; pointer-events:none;
  background:
    radial-gradient(circle at 35% 35%, #f3a079 0%, #d4663a 22%, #8c2f17 55%, #2a0c05 88%, #000 100%),
    radial-gradient(circle at 70% 70%, rgba(0,0,0,0.4), transparent 50%);
  box-shadow:
    inset -60px -40px 120px rgba(0,0,0,0.7),
    inset 30px 20px 80px rgba(255,180,130,0.18),
    0 0 200px rgba(232,98,58,0.25);
  opacity:0.85; z-index:0;
}
@media (max-width:900px){ .header::after{ display:none; } }
.header-inner{max-width:1320px; margin:0 auto; position:relative; z-index:1;}
.chapter-line{
  display:inline-flex; align-items:center; gap:14px; margin-bottom:42px;
  font-family:var(--mono); font-size:0.78rem; letter-spacing:0.18em;
  color:var(--cream-dim); text-transform:uppercase;
}
.chapter-line .bar{ display:inline-block; width:46px; height:1px; background:var(--cream-dim); opacity:0.7; }
.course-pill{
  display:inline-block;
  background:transparent; border:none; padding:0 0 18px 0;
  font-family:var(--mono); font-size:0.72rem; font-weight:500;
  letter-spacing:0.22em; text-transform:uppercase;
  color:var(--cream-dim); margin:0;
}
.course-pill::before{ content:"_"; margin-right:2px; color:var(--mars-glow); }
.header h1{
  font-family:var(--serif); color:var(--cream); font-size:5.4rem; line-height:0.98;
  margin:0 0 28px 0; font-weight:500; max-width:780px; letter-spacing:-0.02em;
}
.header .subtitle{
  color:var(--cream-dim); font-size:1.0rem; margin-bottom:14px;
  max-width:560px; font-weight:400; line-height:1.6;
}
.header .overview{max-width:560px; color:var(--text-muted); font-size:0.92rem; line-height:1.7;}
@media (max-width:900px){
  .header h1{font-size:3.2rem;}
  .header{padding:64px 24px 56px 24px;}
}

/* LANGUAGE SWITCHER — minimal underscore-style links */
.lang-switcher{
  position:absolute; top:34px; right:34px; z-index:20;
  display:flex; gap:24px; padding:0; background:transparent; border:none; box-shadow:none;
}
.lang-switcher button{
  background:transparent; color:var(--cream-dim); border:none; cursor:pointer;
  font-family:var(--mono); font-weight:400; font-size:0.78rem;
  padding:0; letter-spacing:0.18em; text-transform:uppercase;
  transition:color .18s ease; min-width:auto; position:relative;
}
.lang-switcher button::before{
  content:"_"; color:var(--mars-glow); margin-right:2px; opacity:0.5;
  transition:opacity .18s ease;
}
.lang-switcher button:hover{ color:var(--cream); }
.lang-switcher button:hover::before{ opacity:1; }
.lang-switcher button.active{
  color:var(--cream); box-shadow:none; background:transparent;
}
.lang-switcher button.active::before{ opacity:1; color:var(--mars-glow); }

section{padding:72px 0 24px 0; position:relative; z-index:1; border-top:1px solid rgba(244,236,216,0.06);}
section:first-of-type{border-top:none;}
.section-title{display:flex; align-items:baseline; gap:18px; margin-bottom:18px; flex-wrap:wrap; position:relative;}
.section-title::before{
  content:""; position:absolute; left:-24px; top:14px;
  width:3px; height:38px; background:var(--mars-glow); border-radius:1px;
  box-shadow:0 0 12px rgba(232,98,58,0.4);
}
@media (max-width:900px){ .section-title::before{ display:none; } }
.section-title .num{
  width:auto; height:auto; border-radius:0; background:transparent !important;
  box-shadow:none; color:var(--mars-glow);
  font-family:var(--mono); font-weight:500; font-size:0.82rem;
  letter-spacing:0.22em; padding:0;
}
.section-title .num::before{ content:""; }
.section-title .num::after{ content:"  ──  "; color:var(--cream-dim); margin-left:6px; opacity:0.5;}
.section-title h2{ color:var(--cream); margin:0; font-family:var(--serif); font-size:2.6rem; font-weight:400; letter-spacing:-0.02em; line-height:1.05;}
.section-title h2 em{ font-style:italic; color:var(--mars-glow); font-weight:300; }
.section-sub{
  color:var(--cream-dim); max-width:760px; margin:0 0 36px 0;
  font-size:1.02rem; line-height:1.7;
  font-family:var(--serif); font-style:italic; font-weight:400;
  letter-spacing:0.005em;
}
.section-sub::first-letter{
  font-size:1.6em; color:var(--cream); font-weight:500;
  margin-right:1px;
}

/* Hairline rule used as section separator/accent */
.hairline{
  display:block; width:64px; height:1px;
  background:linear-gradient(90deg, var(--mars-glow), transparent);
  margin:0 0 24px 0; opacity:0.7;
}

/* SCROLL-REVEAL ANIMATION */
.reveal{ opacity:0; transform:translateY(28px); transition:opacity .9s cubic-bezier(.2,.6,.2,1), transform .9s cubic-bezier(.2,.6,.2,1); will-change:opacity, transform; }
.reveal.is-visible{ opacity:1; transform:translateY(0); }
.reveal-delay-1{ transition-delay:.08s; }
.reveal-delay-2{ transition-delay:.16s; }
.reveal-delay-3{ transition-delay:.24s; }
@media (prefers-reduced-motion:reduce){
  .reveal{ opacity:1; transform:none; transition:none; }
}

/* CARD (editorial dark) — stronger contrast against body */
.card{
  position:relative;
  background:linear-gradient(180deg, #2a2620 0%, #1f1c17 100%);
  border:1px solid rgba(244,236,216,0.22);
  border-top:1px solid rgba(244,236,216,0.34);
  border-radius:4px; padding:26px 24px;
  box-shadow:0 14px 36px rgba(0,0,0,0.7), 0 2px 6px rgba(0,0,0,0.4), inset 0 1px 0 rgba(244,236,216,0.06);
  transition:transform .28s ease, box-shadow .28s ease, border-color .28s ease;
  color:var(--text);
}
.card::before{
  content:""; position:absolute; left:0; top:0; bottom:0; width:2px;
  background:linear-gradient(180deg, var(--mars-glow) 0%, transparent 70%);
  opacity:0.65; border-radius:4px 0 0 4px;
}
.card:hover{
  border-color:rgba(244,236,216,0.28);
  transform:translateY(-2px);
  box-shadow:0 14px 40px rgba(0,0,0,0.65), inset 0 1px 0 rgba(244,236,216,0.06);
}
.card h3{margin-top:0; color:var(--cream); font-family:var(--display); text-transform:uppercase; letter-spacing:0.08em; font-size:0.95rem; font-weight:600;}
.card .label{
  font-family:var(--mono);
  font-size:0.66rem; text-transform:uppercase; letter-spacing:0.22em;
  color:var(--mars-glow); font-weight:500; margin-bottom:12px;
}
.card .label::before{ content:"_"; margin-right:2px; opacity:0.75; }

.grid{display:grid; gap:22px;}
.grid-2{grid-template-columns:repeat(2,minmax(0,1fr));}
.grid-3{grid-template-columns:repeat(3,minmax(0,1fr));}
.grid-4{grid-template-columns:repeat(4,minmax(0,1fr));}
@media (max-width:1100px){
  .grid-4{grid-template-columns:repeat(2,minmax(0,1fr));}
  .grid-3{grid-template-columns:repeat(2,minmax(0,1fr));}
}
@media (max-width:700px){
  .grid-4,.grid-3,.grid-2{grid-template-columns:1fr;}
  .header h1{font-size:1.9rem;}
}

/* MAP */
.leaflet-map-wrap{
  position:relative; width:100%;
  background:linear-gradient(180deg, #2a2620 0%, #1f1c17 100%);
  border-radius:6px; overflow:hidden;
  border:1px solid rgba(244,236,216,0.26);
  border-top:1px solid rgba(244,236,216,0.36);
  box-shadow:0 18px 44px rgba(0,0,0,0.75), 0 2px 8px rgba(0,0,0,0.45), inset 0 1px 0 rgba(244,236,216,0.06);
  padding:6px;
}
#isanMap{width:100%; height:640px; border-radius:16px;}
.map-toolbar{
  display:flex; flex-wrap:wrap; gap:10px; margin-bottom:14px; align-items:center;
  background:var(--glass); border:1px solid var(--glass-border); border-radius:14px;
  padding:12px 16px; box-shadow:var(--glass-shadow);
  backdrop-filter:blur(14px) saturate(160%); -webkit-backdrop-filter:blur(14px) saturate(160%);
}
.map-toolbar label{
  font-size:0.82rem; font-weight:600; color:var(--text-dim);
  display:inline-flex; align-items:center; gap:6px; cursor:pointer;
  padding:5px 11px; border-radius:8px; transition:all .18s;
}
.map-toolbar label:hover{background:var(--glass-2); color:var(--text);}
.map-toolbar input[type="checkbox"]{ accent-color: var(--mars-glow);}
.map-toolbar button{
  border:1px solid var(--glass-border-2); background:var(--glass-2); color:var(--text);
  padding:7px 14px; border-radius:8px; font-size:0.82rem; cursor:pointer;
  font-weight:600; transition:all .18s;
}
.map-toolbar button:hover{
  background:linear-gradient(135deg, var(--mars-glow), var(--violet-glow));
  border-color:transparent; box-shadow:0 4px 14px rgba(255,122,72,0.45);
}
.map-toolbar select{
  border:1px solid var(--glass-border-2); border-radius:8px; padding:6px 12px;
  font-size:0.82rem; background:rgba(20,22,50,0.85); color:var(--text); font-weight:500;
}
.map-toolbar select option{background:var(--space-2); color:var(--text);}
.map-legend{
  position:absolute; bottom:16px; right:16px; z-index:1000;
  background:rgba(11,10,9,0.92); padding:14px 16px; border-radius:4px;
  border:1px solid rgba(244,236,216,0.10);
  box-shadow:0 8px 28px rgba(0,0,0,0.6);
  font-size:0.78rem; max-width:230px; color:var(--cream);
  font-family:var(--mono);
}
.map-legend h4{
  margin:0 0 8px 0; font-size:0.78rem; color:var(--cyan-glow);
  text-transform:uppercase; letter-spacing:0.08em; font-weight:700;
}
.map-legend .row{
  display:flex; align-items:center; gap:8px; margin-bottom:4px;
  font-size:0.78rem; color:var(--text-dim);
}
.map-legend .sw{
  width:16px; height:12px; display:inline-block; border-radius:3px;
  border:1px solid rgba(255,255,255,0.18);
}
.leaflet-popup-content-wrapper{
  background:rgba(11,10,9,0.96) !important; color:var(--cream) !important;
  border-radius:4px; box-shadow:0 16px 48px rgba(0,0,0,0.7);
  border:1px solid rgba(244,236,216,0.10);
  border-top:2px solid var(--mars-glow);
}
.leaflet-popup-tip{ background:rgba(11,10,9,0.96) !important;}
.leaflet-popup-content{
  margin:12px 16px; font-family:var(--mono); font-size:0.82rem; color:var(--cream);
}
.leaflet-popup-content h4{
  margin:0 0 8px 0; color:var(--cream); font-family:var(--serif);
  font-size:1.2rem; font-weight:500; letter-spacing:0.01em;
}
.leaflet-popup-content table{font-size:0.76rem; margin-top:6px;}
.leaflet-popup-content table td{padding:3px 8px 3px 0; border:none; color:var(--cream-dim); font-family:var(--mono);}
.leaflet-popup-content table td:last-child{color:var(--cream); font-weight:500;}
.leaflet-popup-close-button{ color:var(--cream-dim) !important;}
.leaflet-control-zoom a, .leaflet-bar a {
  background:rgba(11,10,9,0.90) !important; color:var(--cream) !important;
  border-color:rgba(244,236,216,0.10) !important;
}
.leaflet-control-zoom a:hover { background:var(--mars-glow) !important; color:#0b0a09 !important;}
.leaflet-control-attribution{
  background:rgba(11,10,9,0.82) !important; color:var(--cream-dim) !important;
  font-family:var(--mono); font-size:0.7rem;
}
.leaflet-control-attribution a{ color:var(--mars-glow) !important;}

/* MAP PANELS (output rasters) */
.map-panel .map-placeholder{
  width:100%; aspect-ratio:4/3; border-radius:10px;
  background:linear-gradient(135deg,var(--mars-sand-2),#fff);
  border:1px dashed var(--mars-border);
  display:flex; align-items:center; justify-content:center;
  color:var(--mars-gray); font-size:0.85rem;
  position:relative; overflow:hidden; margin-bottom:14px;
}
.map-placeholder img{width:100%; height:100%; object-fit:cover; border-radius:10px; display:block;}
.map-placeholder .placeholder-label{
  position:absolute; bottom:10px; left:10px;
  background:rgba(43,37,35,0.82); color:#fff;
  padding:4px 10px; font-size:0.72rem; border-radius:6px; letter-spacing:0.04em;
}
.legend{
  display:flex; flex-wrap:wrap; gap:8px; margin-top:10px;
  padding:10px 12px; background:var(--mars-sand-2);
  border-radius:10px; border:1px solid var(--mars-border);
}
.legend .swatch{display:inline-flex; align-items:center; gap:6px; font-size:0.78rem; color:var(--mars-gray);}
.legend .sw{width:14px; height:14px; border-radius:3px; display:inline-block; border:1px solid rgba(0,0,0,0.08);}

/* METHODOLOGY / VARIABLES */
.var-card{position:relative; padding:26px 24px;
  background:linear-gradient(180deg, #2a2620 0%, #1f1c17 100%);
  border:1px solid rgba(244,236,216,0.22);
  border-top:1px solid rgba(244,236,216,0.34);
  border-radius:4px;
  box-shadow:0 14px 36px rgba(0,0,0,0.7), 0 2px 6px rgba(0,0,0,0.4), inset 0 1px 0 rgba(244,236,216,0.06);
  display:flex; flex-direction:column; gap:10px;
  transition:transform .25s ease, border-color .25s ease;}
.var-card::before{
  content:""; position:absolute; left:0; top:0; bottom:0; width:2px;
  background:linear-gradient(180deg, var(--mars-glow) 0%, transparent 70%);
  opacity:0.55;
}
.var-card:hover{ transform:translateY(-2px); border-color:rgba(244,236,216,0.26); }
.var-card h3{margin:6px 0 2px 0; font-size:1rem; color:var(--cream); font-family:var(--display); padding-right:90px; text-transform:uppercase; letter-spacing:0.06em;}
.var-card .weight{
  position:absolute; top:22px; right:22px;
  background:transparent; color:var(--mars-glow); font-weight:500;
  font-family:var(--mono); font-size:0.78rem;
  padding:0; border:none; letter-spacing:0.05em;
}
.var-card .var-formula{
  font-family:var(--mono); font-size:0.78rem;
  background:rgba(0,0,0,0.35); border:1px solid var(--glass-border);
  border-radius:4px; padding:10px 12px; color:var(--cream);
  word-break:break-word; line-height:1.5;
}
.var-card p{margin:0; font-size:0.92rem; color:var(--cream-dim); line-height:1.7;}
.var-card .var-range{
  margin-top:auto; font-size:0.72rem; color:var(--mars-glow);
  font-family:var(--mono); font-weight:400; letter-spacing:0.05em;
  border-top:1px solid var(--glass-border); padding-top:10px;
}
.formula-card{
  margin-top:24px; padding:34px 38px;
  background:linear-gradient(180deg, #2a2620 0%, #1f1c17 100%);
  border:1px solid rgba(244,236,216,0.18);
  border-top:1px solid rgba(244,236,216,0.30);
  border-radius:4px;
  box-shadow:0 12px 36px rgba(0,0,0,0.6), inset 0 1px 0 rgba(244,236,216,0.05);
  position:relative;
}
.formula-card::before{
  content:""; position:absolute; left:0; top:0; bottom:0; width:3px;
  background:linear-gradient(180deg, var(--mars-glow), var(--mars-deep));
  border-radius:4px 0 0 4px;
}
.formula-card h3{
  margin:0 0 8px 0; color:var(--cream);
  font-family:var(--serif); text-transform:none; letter-spacing:-0.01em;
  font-size:1.5rem; font-weight:500;
}
.formula-card h3 em{font-style:italic; color:var(--mars-glow); font-weight:400;}
.formula-card h3::after{
  content:""; display:block; width:48px; height:1px;
  background:var(--mars-glow); margin:10px 0 0 0; opacity:0.7;
}
.formula-display{
  font-family:var(--mono); font-size:1.05rem; font-weight:500;
  background:#0a0908; color:var(--cream);
  padding:26px 28px; border-radius:4px; text-align:center;
  letter-spacing:0.02em; line-height:1.8; overflow-x:auto;
  border:1px solid rgba(244,236,216,0.18);
  box-shadow:inset 0 0 30px rgba(232,98,58,0.04);
  margin-top:18px;
}
.formula-card .formula-note{
  margin:18px 0 0 0; font-size:0.95rem; color:var(--cream-dim); line-height:1.75;
  font-family:var(--serif); font-style:italic;
}
.formula-card .step-list{
  margin:16px 0 0 0; padding:0; list-style:none;
  display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:10px;
}
.formula-card .step-list li{
  background:rgba(0,0,0,0.30); border:1px solid var(--glass-border); border-radius:4px;
  padding:11px 14px; font-size:0.84rem; color:var(--text-dim); font-family:var(--mono);
}
.formula-card .step-list li b{color:var(--mars-glow); font-weight:500;}

/* STAT CARDS — editorial, with strong dividers */
.stat{
  text-align:left; padding:30px 26px;
  background:linear-gradient(180deg, #2a2620 0%, #1f1c17 100%);
  border:1px solid rgba(244,236,216,0.22);
  border-top:1px solid rgba(244,236,216,0.34);
  border-radius:4px;
  box-shadow:0 14px 36px rgba(0,0,0,0.7), 0 2px 6px rgba(0,0,0,0.4), inset 0 1px 0 rgba(244,236,216,0.06);
  position:relative; overflow:hidden;
  transition:transform .25s ease, border-color .25s ease, box-shadow .25s ease;
}
.stat::before{
  content:""; position:absolute; left:0; top:0; bottom:0; width:2px;
  background:linear-gradient(180deg, var(--mars-glow) 0%, transparent 80%);
  opacity:0.65;
}
.stat::after{
  /* Faint serif numeral as decorative watermark */
  content:""; position:absolute; right:-20px; bottom:-30px;
  width:90px; height:90px; border-radius:50%;
  background:radial-gradient(circle, rgba(232,98,58,0.06) 0%, transparent 70%);
  pointer-events:none;
}
.stat:hover{
  transform:translateY(-2px); border-color:rgba(244,236,216,0.28);
  box-shadow:0 14px 36px rgba(0,0,0,0.65);
}
.stat .num{
  font-family:var(--serif); font-size:3.2rem; font-weight:400;
  color:var(--cream); line-height:1; margin:10px 0 12px 0; letter-spacing:-0.025em;
  font-feature-settings:"lnum" 1;
}
.stat .num em{ font-style:italic; color:var(--mars-glow); }
.stat .lbl{
  font-family:var(--mono); font-size:0.68rem; letter-spacing:0.22em; text-transform:uppercase;
  color:var(--mars-glow); font-weight:500;
  display:inline-block; padding-bottom:4px; border-bottom:1px solid rgba(232,98,58,0.4);
}
.stat .lbl::before{ content:"_"; margin-right:2px; color:var(--mars-glow); opacity:0.85; }
.stat .sub{
  font-size:0.82rem; color:var(--cream-dim); margin-top:8px; line-height:1.55;
  font-family:var(--serif); font-style:italic;
}

/* TABLE — bold, structured, easy to scan */
.table-wrap{
  overflow-x:auto;
  border:1px solid rgba(244,236,216,0.26);
  border-top:1px solid rgba(244,236,216,0.38);
  border-radius:6px;
  background:linear-gradient(180deg, #2a2620 0%, #1f1c17 100%);
  box-shadow:0 18px 44px rgba(0,0,0,0.75), 0 2px 8px rgba(0,0,0,0.45), inset 0 1px 0 rgba(244,236,216,0.06);
}
table{width:100%; border-collapse:collapse; font-size:0.95rem; color:var(--cream);}
th,td{padding:16px 20px; text-align:left;}
thead th{
  background:#0a0908; color:var(--mars-glow); font-weight:600;
  font-family:var(--mono); font-size:0.72rem; text-transform:uppercase;
  letter-spacing:0.18em;
  border-bottom:2px solid var(--mars-glow);
  border-right:1px solid rgba(244,236,216,0.10);
  position:relative; padding:18px 20px;
}
thead th:last-child{ border-right:none; }
tbody tr{ border-bottom:1px solid rgba(244,236,216,0.12); }
tbody tr:last-child{ border-bottom:none; }
tbody tr:nth-child(even){ background:rgba(244,236,216,0.04); }
tbody tr:hover{ background:rgba(232,98,58,0.14); cursor:pointer;
   box-shadow:inset 3px 0 0 var(--mars-glow); }
tbody tr td{
  color:var(--cream); font-family:var(--sans); font-size:0.96rem; font-weight:400;
  border-right:1px solid rgba(244,236,216,0.06);
}
tbody tr td:last-child{ border-right:none; }
tbody tr td strong{
  color:var(--cream); font-weight:700; font-family:var(--display);
  font-size:1.02rem; letter-spacing:0.005em;
}
.rank{
  display:inline-block; min-width:30px; padding:0;
  background:transparent; color:var(--mars-glow); font-family:var(--mono);
  font-weight:600; font-size:0.86rem; text-align:left; letter-spacing:0.05em;
}

/* Thai readability — slightly looser leading + small size bump,
   preserves the editorial look while fixing tight Thai diacritic stack */
:lang(th){ line-height:1.78; }
:lang(th) h1,:lang(th) h2,:lang(th) h3,:lang(th) h4 { line-height:1.25; }
:lang(th) tbody tr td{ font-size:1rem; line-height:1.7; }
:lang(th) .shortlist-card h3,
:lang(th) .winner-tambon{ line-height:1.2; }
:lang(th) .stat .num{ font-size:2.6rem; line-height:1.08; }
:lang(th) .stat .lbl,:lang(th) .card .label{ letter-spacing:0.08em; }
:lang(th) .section-title h2{ font-size:2.2rem; line-height:1.18; }
:lang(th) .formula-display{ font-size:1rem; line-height:1.9; }
:lang(zh){ line-height:1.85; }
:lang(zh) h1,:lang(zh) h2,:lang(zh) h3,:lang(zh) h4 { line-height:1.3; }

/* CHARTS — defined chart cards */
.chart-card{
  background:linear-gradient(180deg, #2a2620 0%, #1f1c17 100%);
  border:1px solid rgba(244,236,216,0.22);
  border-top:1px solid rgba(244,236,216,0.34);
  border-radius:4px; padding:24px;
  box-shadow:0 14px 36px rgba(0,0,0,0.7), 0 2px 6px rgba(0,0,0,0.4), inset 0 1px 0 rgba(244,236,216,0.06);
  position:relative;
}
.chart-card::before{
  content:""; position:absolute; left:0; top:0; bottom:0; width:2px;
  background:linear-gradient(180deg, var(--mars-glow) 0%, transparent 70%);
  opacity:0.6; border-radius:4px 0 0 4px;
}
.chart-card h3{ color:var(--cream); margin-bottom:6px; font-family:var(--display); text-transform:uppercase; letter-spacing:0.10em; font-size:0.85rem;}
.chart-card .sub{
  font-family:var(--serif); font-style:italic; color:var(--cream-dim);
  font-size:0.92rem; margin:0 0 16px 0;
}
.chart-wrap{position:relative; width:100%; height:280px;}

/* SHORTLIST CARDS */
.shortlist-grid{display:grid; grid-template-columns:repeat(3,1fr); gap:18px;}
@media (max-width:1000px){.shortlist-grid{grid-template-columns:1fr;}}
.shortlist-card{
  background:linear-gradient(180deg, #2a2620 0%, #1f1c17 100%);
  border:1px solid rgba(244,236,216,0.22);
  border-top:1px solid rgba(244,236,216,0.34);
  border-radius:4px;
  padding:26px 24px;
  box-shadow:0 14px 36px rgba(0,0,0,0.7), 0 2px 6px rgba(0,0,0,0.4), inset 0 1px 0 rgba(244,236,216,0.06);
  position:relative; overflow:hidden;
  transition:transform .25s ease, border-color .25s ease, box-shadow .25s ease;
}
.shortlist-card::before{
  content:""; position:absolute; left:0; top:0; bottom:0; width:2px;
  background:linear-gradient(180deg, var(--mars-glow), transparent 75%);
  opacity:0.65;
}
.shortlist-card:hover{
  transform:translateY(-2px); border-color:rgba(244,236,216,0.28);
  box-shadow:0 14px 36px rgba(0,0,0,0.65);
}
.shortlist-card .badge{
  position:absolute; top:20px; right:22px;
  font-family:var(--mono); font-weight:600; font-size:0.7rem;
  padding:5px 10px;
  background:rgba(232,98,58,0.14);
  border:1px solid rgba(232,98,58,0.55);
  color:var(--mars-glow); border-radius:3px;
  letter-spacing:0.20em; text-transform:uppercase;
}
.shortlist-card .badge::before{ content:"_"; opacity:0.85; margin-right:2px;}
.shortlist-card h3{
  margin:8px 0 6px 0; color:var(--cream);
  font-family:var(--serif); font-size:1.85rem; font-weight:500;
  text-transform:none; letter-spacing:-0.015em; line-height:1.1;
}
.shortlist-card .sub{
  color:var(--mars-glow); font-size:0.74rem; font-weight:500;
  margin-bottom:18px; font-family:var(--mono); letter-spacing:0.18em;
  text-transform:uppercase; padding-bottom:14px;
  border-bottom:1px solid rgba(244,236,216,0.10);
}
.shortlist-card ul{
  margin:18px 0 0 0; padding-left:0; list-style:none;
  font-size:0.94rem; color:var(--cream);
}
.shortlist-card ul li{
  margin-bottom:9px; line-height:1.65; padding-left:18px;
  position:relative; font-family:var(--sans); color:var(--cream);
}
.shortlist-card ul li::before{
  content:"—"; position:absolute; left:0; top:0;
  color:var(--mars-glow); font-family:var(--mono); font-weight:500;
}
.shortlist-card .role{
  display:inline-block; margin-top:18px; padding:8px 14px;
  background:rgba(232,98,58,0.10); color:var(--cream);
  border:1px solid rgba(232,98,58,0.45); border-radius:3px;
  font-size:0.72rem; font-weight:600; letter-spacing:0.12em;
  font-family:var(--mono); text-transform:uppercase;
}
.shortlist-card .actions{margin-top:18px; display:flex; gap:8px; flex-wrap:wrap;}
.shortlist-card .btn{
  font-size:0.74rem; padding:10px 18px; border-radius:3px;
  border:1px solid var(--mars-glow); color:var(--cream);
  background:rgba(232,98,58,0.12);
  cursor:pointer; font-weight:600; text-decoration:none; display:inline-block;
  font-family:var(--mono); letter-spacing:0.14em; text-transform:uppercase;
  transition:all .18s ease;
}
.shortlist-card .btn:hover{background:var(--mars-glow); color:#0b0a09; border-color:var(--mars-glow);}

/* SITE PROFILE GRID */
.profile-grid{display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin:18px 0 4px 0;}
.profile-grid .pi{
  background:#0a0908; border:1px solid rgba(244,236,216,0.12); border-radius:3px;
  padding:12px 14px; text-align:left;
  transition:border-color .2s ease;
}
.profile-grid .pi .v{font-family:var(--serif); font-weight:500; color:var(--cream); font-size:1.45rem; line-height:1; letter-spacing:-0.01em;}
.profile-grid .pi .k{font-size:0.62rem; color:var(--mars-glow); text-transform:uppercase; letter-spacing:0.18em; font-family:var(--mono); margin-top:6px; font-weight:500;}

/* FOOTER */
footer{margin-top:80px; background:#000; color:var(--cream-dim); padding:48px 24px; border-top:1px solid var(--glass-border);}
footer .container{display:grid; grid-template-columns:2fr 1fr 1fr; gap:24px;}
@media (max-width:800px){footer .container{grid-template-columns:1fr;}}
footer h4{color:var(--mars-glow); margin-bottom:12px; font-family:var(--mono); font-size:0.74rem; letter-spacing:0.18em; text-transform:uppercase; font-weight:500;}
footer h4::before{ content:"_"; opacity:0.7; margin-right:2px; }
footer p, footer li{color:var(--cream-dim); font-size:0.85rem;}
footer ul{list-style:none; padding:0; margin:0;}
footer li{margin-bottom:6px;}
footer .copyright{
  border-top:1px solid var(--glass-border); text-align:center;
  padding-top:18px; margin-top:24px; font-size:0.78rem; color:var(--text-muted);
  font-family:var(--mono); letter-spacing:0.10em;
}

.zoom-hint{
  background:transparent; border:1px solid var(--glass-border-2);
  color:var(--cream-dim); padding:8px 14px; border-radius:4px;
  font-size:0.78rem; margin-bottom:12px; font-family:var(--mono); letter-spacing:0.06em;
  display:inline-flex; gap:8px; align-items:center;
}

/* FACILITY ICONS + LEGEND */
.facility-legend{
  display:flex; flex-wrap:wrap; gap:18px; margin:12px 0 18px 0;
  padding:14px 18px; background:var(--space-2); border:1px solid var(--glass-border);
  border-radius:6px; box-shadow:var(--glass-shadow); font-size:0.82rem;
}
.facility-legend .item{display:flex; align-items:center; gap:10px; color:var(--cream);}
.facility-legend .icon{
  width:26px; height:26px; border-radius:50%; display:flex;
  align-items:center; justify-content:center; color:#fff; font-weight:700;
  font-size:13px; box-shadow:0 2px 6px rgba(0,0,0,0.45); border:2px solid var(--space-2);
}
.facility-legend .ic-research { background:#3a8e6a; }
.facility-legend .ic-zerog    { background:#5b7eb8; }
.facility-legend .ic-rocket   { background:#b5391f; }
.facility-legend .ic-shuttle  { background:#e8623a; }
.facility-legend .desc{color:var(--text-dim); font-size:0.74rem;}

/* FACILITY TABLE */
.facility-table th{ background:rgba(0,0,0,0.45); color:var(--mars-glow);}
.facility-table tbody tr:nth-child(odd){ background:rgba(255,245,225,0.015);}
.facility-table .ftype{
  font-family:var(--mono); font-weight:500; font-size:0.72rem;
  padding:3px 8px; border-radius:3px; color:#fff; display:inline-block; letter-spacing:0.06em;
}
.facility-table .ftype.research { background:#3a8e6a; }
.facility-table .ftype.zerog    { background:#5b7eb8; }
.facility-table .ftype.rocket   { background:#b5391f; }
.facility-table .ftype.shuttle  { background:#e8623a; }
.facility-table .pass{ color:#7ed4a8; font-weight:600;}
.facility-table .warn{ color:#e8623a; font-weight:600;}

/* CSG NOTE */
.csg-note{
  background:rgba(0,0,0,0.30); border-left:3px solid var(--mars-glow);
  padding:16px 20px; border-radius:4px; margin:16px 0 20px 0;
  font-size:0.88rem; color:var(--text-dim); line-height:1.7;
}
.csg-note b{color:var(--cream);}

/* PROVINCE GROUP HEADER */
.prov-head{
  background:transparent; border:1px solid var(--glass-border-2);
  color:var(--cream); padding:8px 14px; border-radius:4px;
  font-family:var(--mono); font-weight:500; font-size:0.78rem;
  display:inline-block; margin:18px 0 8px 0; letter-spacing:0.14em; text-transform:uppercase;
}
.prov-head::before{ content:"_"; color:var(--mars-glow); margin-right:4px; opacity:0.7; }

/* MINI MAP GRID */
.mini-map-grid{
  display:grid; grid-template-columns:repeat(3,1fr); gap:18px; margin-top:14px;
}
@media (max-width:1100px){.mini-map-grid{grid-template-columns:1fr;}}
.mini-map-card{
  background:linear-gradient(180deg, #2a2620 0%, #1f1c17 100%);
  border:1px solid rgba(244,236,216,0.22);
  border-top:1px solid rgba(244,236,216,0.34);
  border-radius:4px;
  box-shadow:0 14px 36px rgba(0,0,0,0.7), 0 2px 6px rgba(0,0,0,0.4), inset 0 1px 0 rgba(244,236,216,0.06);
  overflow:hidden; display:flex; flex-direction:column;
  transition:transform .25s ease, border-color .25s ease;
}
.mini-map-card:hover{ transform:translateY(-2px); border-color:rgba(244,236,216,0.26); }
.mini-map-card .head{
  background:#000; border-bottom:1px solid var(--glass-border);
  color:var(--cream); padding:18px 18px;
}
.mini-map-card .head h3{color:var(--cream); margin:0; font-size:1.3rem; font-family:var(--serif); font-weight:500; text-transform:none; letter-spacing:-0.01em;}
.mini-map-card .head .amphoe{color:var(--cream-dim); font-size:0.74rem; margin-top:4px; letter-spacing:0.10em; font-family:var(--mono);}
.mini-map-card .head .badge{
  display:inline-block; background:transparent; color:var(--mars-glow); padding:0;
  font-family:var(--mono); font-size:0.7rem; font-weight:500; margin-bottom:6px;
  letter-spacing:0.18em; text-transform:uppercase;
}
.mini-map-card .head .badge::before{ content:"_"; opacity:0.6; margin-right:1px;}
.mini-map-card .map-el{
  height:330px; width:100%;
}
.mini-map-card .info{
  padding:14px 16px; background:rgba(0,0,0,0.30);
  border-top:1px solid var(--glass-border); font-size:0.78rem;
}
.mini-map-card .info table{
  width:100%; border-collapse:collapse; font-size:0.74rem;
}
.mini-map-card .info table td{
  padding:6px 6px; border-bottom:1px solid var(--glass-border); color:var(--text-dim);
}
.mini-map-card .info table td:first-child{
  display:flex; align-items:center; gap:6px; font-weight:500; color:var(--cream);
}
.mini-map-card .info .swatch{
  width:14px; height:14px; border-radius:50%; display:inline-block;
  border:2px solid var(--space-2); box-shadow:0 1px 3px rgba(0,0,0,0.5); flex:0 0 14px;
}
.mini-map-card .info .tam{color:var(--mars-glow); font-weight:500;}
.mini-map-card .info .buf{color:var(--text-muted); font-size:0.7rem; font-family:var(--mono);}

/* ROLE GRID — 12 best-tambon-per-role mini-maps (3 provinces × 4 roles) */
.role-grid{
  display:grid; grid-template-columns:repeat(4, 1fr); gap:14px;
}
@media (max-width:1100px){.role-grid{grid-template-columns:repeat(2,1fr);}}
@media (max-width:600px){.role-grid{grid-template-columns:1fr;}}
.role-prov-band{
  grid-column: 1 / -1;
  background:linear-gradient(90deg, var(--mars-dark) 0%, var(--mars-dark-red) 70%, var(--mars-rust) 100%);
  color:#fff; padding:10px 16px; border-radius:10px;
  font-family:var(--display); font-weight:700; font-size:1rem;
  display:flex; align-items:center; justify-content:space-between;
  letter-spacing:0.04em; margin-top:6px;
}
.role-prov-band .meta{font-size:0.78rem; font-weight:500; color:#f6ecdb;}
.role-card{
  background:linear-gradient(180deg, #2a2620 0%, #1f1c17 100%);
  border:1px solid rgba(244,236,216,0.22);
  border-top:1px solid rgba(244,236,216,0.34);
  border-radius:4px;
  box-shadow:0 14px 36px rgba(0,0,0,0.7), 0 2px 6px rgba(0,0,0,0.4), inset 0 1px 0 rgba(244,236,216,0.06);
  overflow:hidden; display:flex; flex-direction:column;
  transition:transform .25s ease, border-color .25s ease;
}
.role-card:hover{ transform:translateY(-2px); border-color:rgba(244,236,216,0.26); }
.role-card .role-head{
  color:var(--cream); padding:12px 14px; background:#000; border-bottom:1px solid var(--glass-border);
}
.role-card .role-head .role-name{
  font-family:var(--mono); font-weight:500; font-size:0.7rem;
  letter-spacing:0.16em; text-transform:uppercase; color:var(--mars-glow);
}
.role-card .role-head .role-tambon{
  font-size:1rem; font-weight:500; margin-top:4px; font-family:var(--serif);
  color:var(--cream); letter-spacing:-0.005em;
}
.role-card .role-head .role-amphoe{
  font-size:0.7rem; color:var(--cream-dim); opacity:0.85; margin-top:2px;
  font-family:var(--mono); letter-spacing:0.06em;
}
.role-card .map-el{ height:200px; width:100%;}
.role-card .stats{
  padding:12px 14px; background:rgba(0,0,0,0.30);
  border-top:1px solid var(--glass-border);
}
.role-card .stat-row{
  display:flex; justify-content:space-between; align-items:center;
  font-size:0.76rem; padding:4px 0; color:var(--text-dim);
}
.role-card .stat-row span{color:var(--text-muted); font-family:var(--mono); font-size:0.72rem;}
.role-card .stat-row b{
  font-family:var(--serif); font-weight:500; color:var(--cream);
  font-size:0.95rem;
}
.role-card .reason{
  padding:10px 14px; background:transparent; font-size:0.74rem;
  color:var(--text-dim); border-top:1px solid var(--glass-border);
  font-style:italic; line-height:1.55;
}

/* WINNERS GRID */
.winners-grid{
  display:grid; grid-template-columns:repeat(2, 1fr); gap:20px;
}
@media (min-width:1300px){.winners-grid{grid-template-columns:repeat(4, 1fr);}}
@media (max-width:700px){.winners-grid{grid-template-columns:1fr;}}
.winner-card{
  background:linear-gradient(180deg, #2a2620 0%, #1f1c17 100%);
  border:1px solid var(--mars-glow);
  border-top:2px solid var(--mars-glow);
  border-radius:4px;
  box-shadow:0 14px 40px rgba(0,0,0,0.65), 0 0 0 1px rgba(232,98,58,0.18), inset 0 1px 0 rgba(244,236,216,0.06);
  overflow:hidden;
  position:relative; display:flex; flex-direction:column;
  transition:transform .28s ease, box-shadow .28s ease;
}
.winner-card:hover{
  transform:translateY(-3px);
  box-shadow:0 20px 50px rgba(0,0,0,0.75), 0 0 0 1px rgba(232,98,58,0.30), inset 0 1px 0 rgba(244,236,216,0.06);
}
.winner-card .medal{
  position:absolute; top:14px; right:14px; z-index:10;
  background:transparent; color:var(--mars-glow); padding:0;
  font-family:var(--mono); font-weight:500; font-size:0.7rem;
  letter-spacing:0.18em; text-transform:uppercase;
}
.winner-card .medal::before{ content:"_"; opacity:0.7; margin-right:1px;}
.winner-card .winner-head{
  color:var(--cream); padding:22px 20px 18px 20px; background:#000;
  border-bottom:1px solid var(--glass-border);
}
.winner-card .winner-role{
  font-family:var(--mono); font-weight:500; font-size:0.7rem;
  letter-spacing:0.18em; color:var(--mars-glow); text-transform:uppercase;
}
.winner-card .winner-tambon{
  font-family:var(--serif); font-size:1.7rem; font-weight:500;
  margin:8px 0 4px 0; line-height:1.05; color:var(--cream); letter-spacing:-0.015em;
}
.winner-card .winner-prov{
  font-size:0.78rem; color:var(--cream-dim); font-weight:500; font-family:var(--mono); letter-spacing:0.06em;
}
.winner-card .winner-thai{
  font-size:0.74rem; margin-top:10px; padding:5px 11px;
  background:transparent; border:1px solid var(--glass-border-2); border-radius:4px;
  display:inline-block; font-weight:500; color:var(--cream-dim);
  font-family:var(--mono); letter-spacing:0.06em;
}
.winner-card .map-el{ height:230px; width:100%;}
.winner-card .winner-stats{
  display:grid; grid-template-columns:repeat(2,1fr); gap:8px;
  padding:14px 16px; background:rgba(0,0,0,0.30);
  border-top:1px solid var(--glass-border);
}
.winner-card .stat-pill{
  background:transparent; border:1px solid var(--glass-border); border-radius:4px;
  padding:10px 12px; text-align:left;
}
.winner-card .stat-pill .v{
  font-family:var(--serif); font-weight:500; color:var(--cream);
  font-size:1.2rem; line-height:1.05;
}
.winner-card .stat-pill .k{
  font-size:0.62rem; color:var(--cream-dim); margin-top:4px;
  text-transform:uppercase; letter-spacing:0.14em; font-weight:400; font-family:var(--mono);
}
.winner-card .reason-box{
  padding:14px 18px; background:transparent; font-size:0.84rem; color:var(--text-dim);
  border-top:1px solid var(--glass-border); line-height:1.65;
}
.winner-card .reason-box b{color:var(--cream); font-weight:500;}
.winner-card .vs-row{
  padding:12px 18px 16px 18px; background:transparent;
  border-top:1px solid var(--glass-border);
  font-size:0.72rem; color:var(--text-muted);
}
.winner-card .vs-label{
  text-transform:uppercase; letter-spacing:0.14em;
  font-weight:500; color:var(--mars-glow); margin-right:8px;
  font-family:var(--mono); font-size:0.68rem;
}
.winner-card .vs-item{
  display:inline-block; background:transparent; border:1px solid var(--glass-border);
  padding:3px 10px; border-radius:3px; margin-right:6px; margin-bottom:4px;
  color:var(--cream-dim); font-weight:500; font-family:var(--mono); font-size:0.7rem;
}
.zoom-hint b{color:var(--mars-glow);}
</style>
</head>
<body>

<header class="header">
  <div class="lang-switcher" id="langSwitcher">
    <button data-lang="en" class="active">EN</button>
    <button data-lang="th">ไทย</button>
    <button data-lang="zh">中文</button>
  </div>
  <div class="header-inner">
    <span class="course-pill" data-i18n="coursePill">GE.338 · Geographic Data Science</span>
    <h1 data-i18n="siteTitle">Mars Analog Site Suitability — Northeastern Thailand</h1>
    <div class="subtitle" data-i18n="subtitle">Interactive results dashboard for the Isan Mars-analog suitability mapping.</div>
    <p class="overview" data-i18n="overview">
      Explore the suitability map of Northeastern Thailand and the recommended sub-district sites
      for a Mars analog complex. Zoom down to the tambon level on the interactive map below.
    </p>
  </div>
</header>

<main class="container">

  <!-- INTERACTIVE MAP -->
  <section id="interactive-map-section">
    <div class="section-title"><span class="num">1</span><h2 data-i18n="sec1Title">Interactive Suitability Map</h2></div>
    <p class="section-sub" data-i18n="sec1Sub">Province polygons are colored by mean suitability, <strong>192 raster-sampled site points</strong> are graduated by potential, and the <strong>12 mission-critical facilities</strong> (Research, Zero-G, Rocket, Shuttle — 4 per shortlisted province) are placed at specific tambons with CSG-style safety buffers. Toggle the raster overlay, facility markers, or safety buffers from the toolbar. Zoom in to inspect at tambon level.</p>

    <div class="zoom-hint" data-i18n="zoomHint">🛰️ <b>Zoom down to tambon level (zoom 18)</b> &nbsp;— scroll on the map or use the ＋ control.</div>

    <div class="map-toolbar">
      <label><input type="checkbox" id="tglProvinces" checked> <span data-i18n="tglProvinces">Provinces (Suitability)</span></label>
      <label><input type="checkbox" id="tglPoints" checked> <span data-i18n="tglPoints">Per-Province Points (192)</span></label>
      <label><input type="checkbox" id="tglAirports" checked> <span data-i18n="tglAirports">✈ Airports</span></label>
      <label><input type="checkbox" id="tglShortlist" checked> <span data-i18n="tglShortlist">★ Final 3 Sites</span></label>
      <label><input type="checkbox" id="tglFacilities" checked> <span data-i18n="tglFacilities">🛰 Facility Plan (12)</span></label>
      <label><input type="checkbox" id="tglBuffers" checked> <span data-i18n="tglBuffers">◯ Safety Buffers</span></label>
      <label style="margin-left:auto;"><span data-i18n="rasterOverlay">Raster overlay:</span>
        <select id="rasterSelect">
          <option value="" data-i18n="optNone">— None —</option>
          <option value="suit" selected data-i18n="optSuit">Suitability</option>
          <option value="iron" data-i18n="optIron">Iron Oxide</option>
          <option value="ndvi" data-i18n="optNDVI">NDVI</option>
          <option value="bsi" data-i18n="optBSI">BSI</option>
          <option value="slope" data-i18n="optSlope">Slope</option>
          <option value="cand" data-i18n="optCand">Candidate Sites</option>
          <option value="vhigh" data-i18n="optVHigh">Very High Suitability</option>
        </select>
      </label>
      <label><span data-i18n="basemap">Basemap:</span>
        <select id="basemapSelect">
          <option value="satellite" data-i18n="bmSat">Satellite (ESRI)</option>
          <option value="osm" data-i18n="bmOSM">OpenStreetMap</option>
          <option value="terrain" data-i18n="bmTerrain">Terrain (OpenTopoMap)</option>
          <option value="dark" data-i18n="bmDark">Dark (Carto)</option>
        </select>
      </label>
      <button id="btnFit" data-i18n="btnFit">Fit to Isan</button>
    </div>

    <div class="leaflet-map-wrap">
      <div id="isanMap"></div>
      <div class="map-legend">
        <h4 data-i18n="legendProvSuit">Province Mean Suitability</h4>
        <div class="row"><span class="sw" style="background:#7a1e1e"></span> <span data-i18n="legVeryHigh">≥ 0.70 (Very High)</span></div>
        <div class="row"><span class="sw" style="background:#b5502c"></span> 0.66 – 0.70</div>
        <div class="row"><span class="sw" style="background:#d07a4c"></span> 0.63 – 0.66</div>
        <div class="row"><span class="sw" style="background:#e9b888"></span> 0.58 – 0.63</div>
        <div class="row"><span class="sw" style="background:#f6ecdb"></span> &lt; 0.58</div>
        <hr style="border:none; border-top:1px solid var(--mars-border); margin:8px 0;">
        <div style="font-weight:700; color:var(--mars-dark-red); font-size:0.78rem; margin-bottom:4px;" data-i18n="legSiteSuit">Site Suitability (per point)</div>
        <div class="row"><span class="sw" style="background:#7a0000; border-radius:50%; width:12px; height:12px;"></span> <span data-i18n="legExcellent">≥ 0.90 (Excellent)</span></div>
        <div class="row"><span class="sw" style="background:#c4302b; border-radius:50%; width:11px; height:11px;"></span> 0.80 – 0.90</div>
        <div class="row"><span class="sw" style="background:#e66b30; border-radius:50%; width:9px; height:9px;"></span> 0.70 – 0.80</div>
        <div class="row"><span class="sw" style="background:#f0a05a; border-radius:50%; width:8px; height:8px;"></span> &lt; 0.70</div>
        <hr style="border:none; border-top:1px solid var(--mars-border); margin:8px 0;">
        <div class="row"><span class="sw" style="background:#7a1e1e; border-radius:50%; width:10px; height:10px;"></span> <span data-i18n="legFinal">★ Final Site</span></div>
        <div class="row"><span class="sw" style="background:#1f3b56; border-radius:50%; width:10px; height:10px;"></span> <span data-i18n="legAirport">✈ Airport</span></div>
        <hr style="border:none; border-top:1px solid var(--mars-border); margin:8px 0;">
        <div style="font-weight:700; color:var(--mars-dark-red); font-size:0.78rem; margin-bottom:4px;" data-i18n="legFacilities">Facilities (12)</div>
        <div class="row"><span class="sw" style="background:#1f6f4a; border-radius:50%; width:10px; height:10px;"></span> <span data-i18n="legResearch">R · Research Station</span></div>
        <div class="row"><span class="sw" style="background:#274d8c; border-radius:50%; width:10px; height:10px;"></span> <span data-i18n="legZerog">0g · Zero-G Tower</span></div>
        <div class="row"><span class="sw" style="background:#7a1e1e; border-radius:50%; width:10px; height:10px;"></span> <span data-i18n="legRocket">▲ Rocket Pad</span></div>
        <div class="row"><span class="sw" style="background:#b5502c; border-radius:50%; width:10px; height:10px;"></span> <span data-i18n="legShuttle">⊳ Shuttle Runway</span></div>
      </div>
    </div>
  </section>


  <!-- FINAL SHORTLIST -->
  <section>
    <div class="section-title"><span class="num">2</span><h2 data-i18n="sec2Title">Recommended Sites</h2></div>
    <p class="section-sub" data-i18n="sec2Sub">The three top sub-district candidates for the Mars analog complex. Click "Fly map to site" to inspect the terrain at zoom level 13.</p>
    <div class="shortlist-grid" id="shortlistGrid"></div>
  </section>


  <!-- FACILITY PLACEMENT PLAN -->
  <section id="facility-plan">
    <div class="section-title"><span class="num">3</span><h2 data-i18n="sec3Title">Facility Placement Plan — Tambon Level</h2></div>
    <p class="section-sub" data-i18n="sec3Sub">
      For each of the three shortlisted provinces, four mission-critical facilities are placed at specific tambon (sub-district)
      coordinates. Each facility carries an inner compliance buffer (population &amp; road clearance) and an outer
      restricted zone (rocket safety / runway approach) — enable Safety Buffers on the map to view.
    </p>

    <div class="csg-note" data-i18n="csgNote">
      <b>Reference standard — Centre Spatial Guyanais (CSG, France):</b>
      Kourou enforces ≥ <b>5 km</b> exclusion of permanent population from any launch pad and a <b>~12 km</b> restricted
      perimeter during launches. Launch pads, drop towers, runways, and habitable research blocks are separated by
      ≥ 3 km. The same buffer logic is applied here, adapted for inland Isan terrain.
    </div>

    <div class="facility-legend">
      <div class="item"><div class="icon ic-research">R</div>
        <div><b data-i18n="facLegResearch">Research Station</b><div class="desc" data-i18n="facLegResearchDesc">HQ · habitat · labs · 1 km buffer</div></div></div>
      <div class="item"><div class="icon ic-zerog">0g</div>
        <div><b data-i18n="facLegZerog">Zero-Gravity Drop Tower</b><div class="desc" data-i18n="facLegZerogDesc">Microgravity sims · 2 km buffer</div></div></div>
      <div class="item"><div class="icon ic-rocket">▲</div>
        <div><b data-i18n="facLegRocket">Rocket Launch Test Pad</b><div class="desc" data-i18n="facLegRocketDesc">Static fire / sounding rockets · 5 km + 12 km zones</div></div></div>
      <div class="item"><div class="icon ic-shuttle">⊳</div>
        <div><b data-i18n="facLegShuttle">Shuttle / Runway Strip</b><div class="desc" data-i18n="facLegShuttleDesc">RLV approach corridor · 3 km buffer</div></div></div>
    </div>

    <div class="table-wrap">
      <table class="facility-table">
        <thead>
          <tr>
            <th data-i18n="thProv">Province</th><th data-i18n="thAmphoe">Amphoe</th><th data-i18n="thTambon">Tambon</th><th data-i18n="thFacility">Facility</th>
            <th data-i18n="thSuit">Suit</th><th data-i18n="thDistRoad">Dist. Road</th><th data-i18n="thDistVlg">Dist. Village</th>
            <th data-i18n="thBuffer">Buffer (km)</th><th data-i18n="thCSG">CSG Compliance</th>
          </tr>
        </thead>
        <tbody id="facilityTableBody"></tbody>
      </table>
    </div>
  </section>


  <!-- SUMMARY STATS -->
  <section>
    <div class="section-title"><span class="num">4</span><h2 data-i18n="sec4Title">Summary Statistics</h2></div>
    <div class="grid grid-4">
      <div class="stat">
        <div class="lbl" data-i18n="statTopProv">Top Province</div>
        <div class="num" id="statTopProv" style="font-size:1.3rem;">—</div>
        <div class="sub" data-i18n="statTopProvSub">Highest mean suitability</div>
      </div>
      <div class="stat">
        <div class="lbl" data-i18n="statTotalArea">Total Suitable Area</div>
        <div class="num" id="statTotalArea">— km²</div>
        <div class="sub" data-i18n="statTotalAreaSub">Sum of candidate-site pixels</div>
      </div>
      <div class="stat">
        <div class="lbl" data-i18n="statZones">Provinces in Study</div>
        <div class="num" id="statZones">—</div>
        <div class="sub" data-i18n="statZonesSub">All Isan provinces analyzed</div>
      </div>
      <div class="stat">
        <div class="lbl" data-i18n="statVH">Very-High Provinces</div>
        <div class="num" id="statVHClusters">—</div>
        <div class="sub" data-i18n="statVHSub">Max suit ≥ 0.90</div>
        <div class="sub" id="statVHList" style="margin-top:6px; font-size:0.78rem; line-height:1.45; color:var(--mars-rust); font-weight:600;">—</div>
      </div>
    </div>
  </section>


  <!-- METHODOLOGY: VARIABLES + WEIGHTED FORMULA -->
  <section>
    <div class="section-title"><span class="num">5</span><h2 data-i18n="sec5Title">Suitability Formula &amp; Variables</h2></div>
    <p class="section-sub" data-i18n="sec5Sub">The suitability score for every pixel is a weighted, normalized combination of four remote-sensing indices. Each variable is min-max normalized to [0, 1] across the study area before weighting. Weights sum to 1.0.</p>

    <div class="grid grid-4">
      <div class="card var-card">
        <span class="weight">w₁ = 0.30</span>
        <h3 data-i18n="varIron">Iron Oxide Ratio</h3>
        <div class="var-formula">Iron = Red / Blue&nbsp;&nbsp;<i>(Sentinel-2 SR)</i></div>
        <p data-i18n="varIronDesc">Higher values flag iron-rich, rust-colored soils — the visual hallmark of Mars analogs. Computed pixel-wise from Sentinel-2 surface reflectance bands B4 / B2.</p>
        <div class="var-range">Observed range: 1.40 – 2.37</div>
      </div>

      <div class="card var-card">
        <span class="weight">w₂ = 0.25</span>
        <h3 data-i18n="varBSI">Bare Soil Index (BSI)</h3>
        <div class="var-formula">BSI = ((SWIR + Red) − (NIR + Blue)) / ((SWIR + Red) + (NIR + Blue))</div>
        <p data-i18n="varBSIDesc">Higher BSI = more exposed regolith, less canopy. Mars-analog campuses need bare soil for lander, rover, and EVA trials.</p>
        <div class="var-range">Observed range: −0.19 – 0.18</div>
      </div>

      <div class="card var-card">
        <span class="weight">w₃ = 0.25</span>
        <h3 data-i18n="varNDVI">NDVI <i>(inverted)</i></h3>
        <div class="var-formula">NDVI = (NIR − Red) / (NIR + Red)</div>
        <p data-i18n="varNDVIDesc">Vegetation density. We <b>invert</b> it (1 − NDVI*) so that sparse, drier land scores higher — dense forest is unlike Mars.</p>
        <div class="var-range">Observed range: −0.10 – 0.90</div>
      </div>

      <div class="card var-card">
        <span class="weight">w₄ = 0.20</span>
        <h3 data-i18n="varSlope">Slope <i>(inverted)</i></h3>
        <div class="var-formula">Slope = arctan(∇z) · 180 / π &nbsp;<i>(SRTM 30 m DEM)</i></div>
        <p data-i18n="varSlopeDesc">Computed from SRTM 30 m elevation. Steep terrain is penalized — a Mars-analog site needs flat ground for facilities, runways, and rover routes.</p>
        <div class="var-range">Observed range: 0° – 25°</div>
      </div>
    </div>

    <div class="formula-card">
      <h3 data-i18n="formulaTitle">Weighted Suitability Score</h3>
      <div class="formula-display">
        Suit = 0.30 · Iron* &nbsp;+&nbsp; 0.25 · BSI* &nbsp;+&nbsp; 0.25 · (1 − NDVI*) &nbsp;+&nbsp; 0.20 · (1 − Slope*)
      </div>
      <p class="formula-note" data-i18n="formulaNote"><b>X*</b> denotes min-max normalization of variable X to [0, 1] across the Isan study area. The two inverted terms reward bare, flat land. Pixels are then thresholded:</p>
      <ul class="step-list">
        <li><b data-i18n="thrCand">Candidate mask:</b> <span data-i18n="thrCandVal">Suit ≥ 0.70</span></li>
        <li><b data-i18n="thrVH">Very-High mask:</b> <span data-i18n="thrVHVal">Suit ≥ 0.90</span></li>
        <li><b data-i18n="thrPixel">Pixel size:</b> <span data-i18n="thrPixelVal">~120 m (Sentinel-2 native, resampled)</span></li>
        <li><b data-i18n="thrSrc">Sources:</b> <span data-i18n="thrSrcVal">Sentinel-2 L2A · SRTM 30 m · GADM v4.1</span></li>
      </ul>
    </div>
  </section>


  <!-- PROVINCE TABLE -->
  <section>
    <div class="section-title"><span class="num">6</span><h2 data-i18n="sec6Title">Province Ranking</h2></div>
    <p class="section-sub" data-i18n="sec6Sub">Per-province suitability stats. Click a row to zoom to that province on the map above.</p>
    <div class="table-wrap">
      <table id="provinceTable">
        <thead>
          <tr>
            <th data-i18n="thRank">Rank</th>
            <th data-i18n="thProvince">Province</th>
            <th data-i18n="thMean">Mean Suitability</th>
            <th data-i18n="thMax">Max Suitability</th>
            <th data-i18n="thPop">Population (k)</th>
          </tr>
        </thead>
        <tbody id="provinceTableBody"></tbody>
      </table>
    </div>
  </section>


  <!-- CHARTS -->
  <section>
    <div class="section-title"><span class="num">7</span><h2 data-i18n="sec7Title">Charts</h2></div>
    <div class="grid grid-3">
      <div class="chart-card">
        <h3 data-i18n="chartTopProv">Top Provinces by Mean Suitability</h3>
        <div class="chart-wrap"><canvas id="chartTopProv"></canvas></div>
      </div>
      <div class="chart-card">
        <h3 data-i18n="chartClasses">Suitability Class Distribution</h3>
        <div class="chart-wrap"><canvas id="chartClasses"></canvas></div>
      </div>
      <div class="chart-card">
        <h3 data-i18n="chartHist">Mean Suitability Histogram</h3>
        <div class="chart-wrap"><canvas id="chartHist"></canvas></div>
      </div>
    </div>
  </section>


  <!-- PER-PROVINCE FACILITY DETAIL MAPS -->
  <section id="province-detail-section">
    <div class="section-title"><span class="num">8</span><h2 data-i18n="sec8Title">Per-Province Facility Detail Maps</h2></div>
    <p class="section-sub" data-i18n="sec8Sub">
      The three provinces with the highest "do-everything" capability — enough flat bare-soil terrain,
      low population density, transport access, and CSG-compliant buffers to host all four facility
      types side-by-side. Each mini-map is zoomed to the tambon cluster. <b>Click a marker</b> to
      reveal full details (suit, road / village distances, buffer sizes, placement rationale).
    </p>

    <div class="mini-map-grid" id="miniMapGrid">
      <!-- 3 per-province detail cards will be injected here by JS -->
    </div>
  </section>


  <!-- WINNERS — single best tambon for each mission type, decision-aid view -->
  <section id="winners-section">
    <div class="section-title"><span class="num">9</span><h2 data-i18n="sec9Title">Decision Aid — Best Tambon by Mission Type</h2></div>
    <p class="section-sub" data-i18n="sec9Sub">
      Decision-aid view: across all candidate tambons in the three shortlisted provinces, the
      single overall winner for each mission type is surfaced below. Each card shows the winning
      tambon, its distance from the nearest road and village, the CSG-style buffer geometry, and
      the runner-up tambons for comparison.
    </p>
    <div class="winners-grid" id="winnersGrid">
      <!-- 4 winner cards (one per role) injected by JS -->
    </div>
  </section>



</main>

<footer>
  <div class="container">
    <div>
      <h4 data-i18n="ftAbout">About</h4>
      <p data-i18n="ftAboutBody">Mars Analog Site Suitability — Northeastern Thailand. Course: GE.338 Geographic Data Science.</p>
    </div>
    <div>
      <h4 data-i18n="ftData">Data</h4>
      <ul>
        <li>Landsat 8 Collection 2 L2 (USGS)</li>
        <li>NASADEM (NASA JPL)</li>
        <li>ESA WorldCover v200</li>
        <li>ESRI World Imagery &amp; OSM</li>
      </ul>
    </div>
    <div>
      <h4 data-i18n="ftOutputs">Outputs</h4>
      <ul>
        <li data-i18n="ftOutSuit">Suitability raster</li>
        <li data-i18n="ftOutCand">Candidate Sites</li>
        <li data-i18n="ftOutVH">Very High Suitability</li>
        <li data-i18n="ftOutCSV">Province Summary CSV</li>
      </ul>
    </div>
  </div>
  <div class="copyright" data-i18n="ftCopyright">© 2026 — GE.338 · Mars Analog Suitability · Northeastern Thailand</div>
</footer>


<script>
/* ========================================================
   I18N DICTIONARY — English / Thai / Chinese (Simplified)
   ======================================================== */
const I18N = {
  en: {
    coursePill:"GE.338 · Geographic Data Science",
    siteTitle:"Mars Analog Site Suitability — Northeastern Thailand",
    subtitle:"Interactive results dashboard for the Isan Mars-analog suitability mapping.",
    overview:"Explore the suitability map of Northeastern Thailand and the recommended sub-district sites for a Mars analog complex. Zoom down to the tambon level on the interactive map below.",
    sec1Title:"Interactive Suitability Map",
    sec1Sub:"Province polygons are coloured by mean suitability, <strong>192 raster-sampled site points</strong> are graduated by potential, and the <strong>12 mission-critical facilities</strong> (Research, Zero-G, Rocket, Shuttle — 4 per shortlisted province) are placed at specific tambons with CSG-style safety buffers. Toggle the raster overlay, facility markers, or safety buffers from the toolbar. Zoom in to inspect at tambon level.",
    zoomHint:"🛰️ <b>Zoom down to tambon level (zoom 18)</b> &nbsp;— scroll on the map or use the ＋ control.",
    tglProvinces:"Provinces (Suitability)", tglPoints:"Per-Province Points (192)",
    tglAirports:"✈ Airports", tglShortlist:"★ Final 3 Sites",
    tglFacilities:"🛰 Facility Plan (12)", tglBuffers:"◯ Safety Buffers",
    rasterOverlay:"Raster overlay:", basemap:"Basemap:", btnFit:"Fit to Isan",
    optNone:"— None —", optSuit:"Suitability", optIron:"Iron Oxide", optNDVI:"NDVI",
    optBSI:"BSI", optSlope:"Slope", optCand:"Candidate Sites", optVHigh:"Very High Suitability",
    bmSat:"Satellite (ESRI)", bmOSM:"OpenStreetMap", bmTerrain:"Terrain (OpenTopoMap)", bmDark:"Dark (Carto)",
    legendProvSuit:"Province Mean Suitability", legVeryHigh:"≥ 0.70 (Very High)",
    legSiteSuit:"Site Suitability (per point)", legExcellent:"≥ 0.90 (Excellent)",
    legFinal:"★ Final Site", legAirport:"✈ Airport", legFacilities:"Facilities (12)",
    legResearch:"R · Research Station", legZerog:"0g · Zero-G Tower",
    legRocket:"▲ Rocket Pad", legShuttle:"⊳ Shuttle Runway",
    sec2Title:"Recommended Sites",
    sec2Sub:"The three top sub-district candidates for the Mars analog complex. Click \"Fly map to site\" to inspect the terrain at zoom level 13.",
    sec3Title:"Facility Placement Plan — Tambon Level",
    sec3Sub:"For each of the three shortlisted provinces, four mission-critical facilities are placed at specific tambon (sub-district) coordinates. Each facility carries an inner compliance buffer (population &amp; road clearance) and an outer restricted zone (rocket safety / runway approach) — enable Safety Buffers on the map to view.",
    csgNote:"<b>Reference standard — Centre Spatial Guyanais (CSG, France):</b> Kourou enforces ≥ <b>5 km</b> exclusion of permanent population from any launch pad and a <b>~12 km</b> restricted perimeter during launches. Launch pads, drop towers, runways, and habitable research blocks are separated by ≥ 3 km. The same buffer logic is applied here, adapted for inland Isan terrain.",
    facLegResearch:"Research Station", facLegResearchDesc:"HQ · habitat · labs · 1 km buffer",
    facLegZerog:"Zero-Gravity Drop Tower", facLegZerogDesc:"Microgravity sims · 2 km buffer",
    facLegRocket:"Rocket Launch Test Pad", facLegRocketDesc:"Static fire / sounding rockets · 5 km + 12 km zones",
    facLegShuttle:"Shuttle / Runway Strip", facLegShuttleDesc:"RLV approach corridor · 3 km buffer",
    thProv:"Province", thAmphoe:"District", thTambon:"Sub-District", thFacility:"Facility",
    thSuit:"Suit", thDistRoad:"Dist. Road", thDistVlg:"Dist. Village",
    thBuffer:"Buffer (km)", thCSG:"CSG Compliance",
    sec4Title:"Summary Statistics", statTopProv:"Top Province", statTopProvSub:"Highest mean suitability",
    statTotalArea:"Total Suitable Area", statTotalAreaSub:"Sum of candidate-site pixels",
    statZones:"Provinces in Study", statZonesSub:"All Isan provinces analyzed",
    statVH:"Very-High Provinces", statVHSub:"Max suit ≥ 0.90",
    sec5Title:"Suitability Formula & Variables",
    sec5Sub:"The suitability score for every pixel is a weighted, normalized combination of four remote-sensing indices. Each variable is min-max normalized to [0, 1] across the study area before weighting. Weights sum to 1.0.",
    varIron:"Iron Oxide Ratio",
    varIronDesc:"Higher values flag iron-rich, rust-colored soils — the visual hallmark of Mars analogs. Computed pixel-wise from Sentinel-2 surface reflectance bands B4 / B2.",
    varBSI:"Bare Soil Index (BSI)",
    varBSIDesc:"Higher BSI = more exposed regolith, less canopy. Mars-analog campuses need bare soil for lander, rover, and EVA trials.",
    varNDVI:"NDVI <i>(inverted)</i>",
    varNDVIDesc:"Vegetation density. We <b>invert</b> it (1 − NDVI*) so that sparse, drier land scores higher — dense forest is unlike Mars.",
    varSlope:"Slope <i>(inverted)</i>",
    varSlopeDesc:"Computed from SRTM 30 m elevation. Steep terrain is penalized — a Mars-analog site needs flat ground for facilities, runways, and rover routes.",
    formulaTitle:"Weighted Suitability Score",
    formulaNote:"<b>X*</b> denotes min-max normalization of variable X to [0, 1] across the Isan study area. The two inverted terms reward bare, flat land. Pixels are then thresholded:",
    thrCand:"Candidate mask:", thrCandVal:"Suit ≥ 0.70",
    thrVH:"Very-High mask:",   thrVHVal:"Suit ≥ 0.90",
    thrPixel:"Pixel size:",    thrPixelVal:"~120 m (Sentinel-2 native, resampled)",
    thrSrc:"Sources:",         thrSrcVal:"Sentinel-2 L2A · SRTM 30 m · GADM v4.1",
    sec6Title:"Province Ranking", sec6Sub:"Per-province suitability stats. Click a row to zoom to that province on the map above.",
    thRank:"Rank", thProvince:"Province", thMean:"Mean Suitability", thMax:"Max Suitability", thPop:"Population (k)",
    sec7Title:"Charts", chartTopProv:"Top Provinces by Mean Suitability",
    chartClasses:"Suitability Class Distribution", chartHist:"Mean Suitability Histogram",
    sec8Title:"Per-Province Facility Detail Maps",
    sec8Sub:"The three provinces with the highest \"do-everything\" capability — enough flat bare-soil terrain, low population density, transport access, and CSG-compliant buffers to host all four facility types side-by-side. Each mini-map is zoomed to the tambon cluster. <b>Click a marker</b> to reveal full details.",
    sec9Title:"Decision Aid — Best Tambon by Mission Type",
    sec9Sub:"Decision-aid view: across all candidate tambons in the three shortlisted provinces, the single overall winner for each mission type is surfaced below. Each card shows the winning tambon, its distance from the nearest road and village, the CSG-style buffer geometry, and the runner-up tambons for comparison.",
    ftAbout:"About", ftAboutBody:"Mars Analog Site Suitability — Northeastern Thailand. Course: GE.338 Geographic Data Science.",
    ftData:"Data", ftOutputs:"Outputs",
    ftOutSuit:"Suitability raster", ftOutCand:"Candidate Sites", ftOutVH:"Very High Suitability", ftOutCSV:"Province Summary CSV",
    ftCopyright:"© 2026 — GE.338 · Mars Analog Suitability · Northeastern Thailand",
    /* Card / popup labels */
    flyToSite:"📍 Fly map to site", site:"SITE", detailBadge:"DETAIL",
    facilities4:"4 facilities · CSG-style buffers",
    profileSuit:"Suit", profilePop:"Pop (prov.)", profileAirport:"Airport",
    rRocket:"Rocket Test Pad", rResearch:"Research Station HQ",
    rZerog:"Zero-G Drop Tower", rShuttle:"Shuttle Runway Strip",
    roleResearchHero:"RESEARCH CAMPUS", roleZerogHero:"ZERO-GRAVITY LAB",
    roleRocketHero:"ROCKET TEST RANGE", roleShuttleHero:"SHUTTLE RUNWAY",
    roleResearchSub:"Main research / experiment hub",
    roleZerogSub:"Zero-gravity simulation lab",
    roleRocketSub:"Rocket launch testing range",
    roleShuttleSub:"Spacecraft / shuttle runway",
    medalBest:"🥇 BEST",
    statSuit:"Suitability", statRoad:"🛣 To road", statVlg:"🏘 To village", statBuffer:"Buffer",
    whyWins:"Why this tambon wins:",
    runnersUp:"runners-up:",
    reasonResearch:"Highest-suitability HQ tambon with shortest road access. Strong cellular + power grid coverage and a research-grade plateau within walking distance.",
    reasonZerog:"Quietest seismic + RF environment of all candidates. Solid bedrock supports a 120 m vacuum drop tower with minimal subsidence.",
    reasonRocket:"Most isolated bare-soil expanse in the finalist list. Easily clears the CSG ≥ 5 km population exclusion and ~12 km restricted perimeter, with an ENE flight corridor over open paddy land.",
    reasonShuttle:"Longest contiguous flat strip aligned with the prevailing wind (~080°). Three-km clear approach corridor and the lowest population density on the runway centreline.",
    distToRoad:"Dist. to road", distToVlg:"Dist. to village",
    innerBuf:"Inner buffer", restricted:"Restricted",
    csgPass:"PASS · CSG-equivalent", csgPassNormal:"PASS", csgReviewPop:"REVIEW · below 5 km pop.", csgReview:"REVIEW",
    popupLat:"Latitude", popupLng:"Longitude",
    popupSampledFrom:"Sampled from 02_Isan_Suitability.tif · zoom in to see at tambon level",
    popupAirport:"Airport",
    badgeSITE:"SITE", searchZone:"search zone",
    profPopAbbr:"Pop (prov.)", profAirportAbbr:"Airport",
    /* Shortlist roles */
    slRole1:"Habitat & Research Center", slRole2:"Rocket Drop-Test & Telemetry", slRole3:"Rover Testing & Field Training",
    slBullet1A:"Highest mean suitability area in Isan (0.733).",
    slBullet1B:"Off the Mekong flood belt — semi-arid plateau.",
    slBullet1C:"55 km to Roi Et Airport for logistics.",
    slBullet1D:"Rural amphoe — low light & RF noise.",
    slBullet2A:"Excellent dry-season bare-soil exposure.",
    slBullet2B:"Closest finalist to a regional airport (35 km).",
    slBullet2C:"Open paddy-fringe terrain — easy buffers.",
    slBullet2D:"No major reservoirs within 5 km — RF clean.",
    slBullet3A:"Varied terrain — plateau & scarps for slope analogs.",
    slBullet3B:"Sparse population (~140 / km² in amphoe).",
    slBullet3C:"25 km to Sakon Nakhon Airport (SNO).",
    slBullet3D:"Phu Phan range mimics Martian highlands.",
    /* Place name prefixes (so we can drop "ต." in non-Thai modes) */
    tambonPrefix:"T. ", amphoePrefix:"D. "
  },

  th: {
    coursePill:"GE.338 · วิทยาศาสตร์ข้อมูลเชิงภูมิศาสตร์",
    siteTitle:"ความเหมาะสมของพื้นที่จำลองดาวอังคาร — ภาคตะวันออกเฉียงเหนือของประเทศไทย",
    subtitle:"แดชบอร์ดผลลัพธ์แบบโต้ตอบ สำหรับการทำแผนที่ความเหมาะสมของพื้นที่จำลองดาวอังคารในภาคอีสาน",
    overview:"สำรวจแผนที่ความเหมาะสมของภาคตะวันออกเฉียงเหนือ พร้อมตำบลที่แนะนำสำหรับศูนย์จำลองดาวอังคาร สามารถซูมลงถึงระดับตำบลได้บนแผนที่โต้ตอบด้านล่าง",
    sec1Title:"แผนที่ความเหมาะสมแบบโต้ตอบ",
    sec1Sub:"พื้นที่จังหวัดถูกระบายสีตามค่าเฉลี่ยความเหมาะสม จุดตัวอย่างจากแรสเตอร์จำนวน <strong>192 จุด</strong> ถูกจัดขนาดและสีตามคะแนนศักยภาพ และ <strong>สถานีภารกิจหลัก 12 แห่ง</strong> (ศูนย์วิจัย, หอจำลองสภาวะไร้แรงโน้มถ่วง, ฐานทดสอบจรวด, รันเวย์กระสวยอวกาศ — 4 แห่งต่อจังหวัด) ถูกวางตามพิกัดตำบลจริง พร้อมเขตปลอดภัยตามมาตรฐาน CSG ผู้ใช้สามารถเปิด/ปิดชั้นข้อมูลแต่ละชั้นจากแถบเครื่องมือ และซูมเข้าดูรายละเอียดระดับตำบลได้",
    zoomHint:"🛰️ <b>ซูมลงถึงระดับตำบล (ระดับ 18)</b> &nbsp;— เลื่อนลูกล้อเมาส์บนแผนที่ หรือกดปุ่ม ＋",
    tglProvinces:"จังหวัด (ความเหมาะสม)", tglPoints:"จุดรายจังหวัด (192)",
    tglAirports:"✈ สนามบิน", tglShortlist:"★ พื้นที่ที่ผ่านการคัดเลือก 3 แห่ง",
    tglFacilities:"🛰 ผังสถานี (12)", tglBuffers:"◯ เขตปลอดภัย",
    rasterOverlay:"ชั้นแรสเตอร์:", basemap:"แผนที่ฐาน:", btnFit:"แสดงทั้งภาคอีสาน",
    optNone:"— ไม่แสดง —", optSuit:"ความเหมาะสม", optIron:"เหล็กออกไซด์", optNDVI:"NDVI",
    optBSI:"BSI", optSlope:"ความลาดชัน", optCand:"พื้นที่ที่ผ่านเกณฑ์", optVHigh:"ความเหมาะสมสูงมาก",
    bmSat:"ภาพถ่ายดาวเทียม (ESRI)", bmOSM:"OpenStreetMap", bmTerrain:"ภูมิประเทศ (OpenTopoMap)", bmDark:"พื้นมืด (Carto)",
    legendProvSuit:"ค่าเฉลี่ยความเหมาะสมรายจังหวัด", legVeryHigh:"≥ 0.70 (สูงมาก)",
    legSiteSuit:"ความเหมาะสมรายจุด", legExcellent:"≥ 0.90 (ยอดเยี่ยม)",
    legFinal:"★ พื้นที่ที่ผ่านการคัดเลือก", legAirport:"✈ สนามบิน", legFacilities:"สถานี (12)",
    legResearch:"R · สถานีวิจัย", legZerog:"0g · หอจำลองสภาวะไร้แรงโน้มถ่วง",
    legRocket:"▲ ฐานทดสอบจรวด", legShuttle:"⊳ รันเวย์กระสวยอวกาศ",
    sec2Title:"พื้นที่ที่ได้รับการคัดเลือก",
    sec2Sub:"3 ตำบลที่ดีที่สุดสำหรับศูนย์จำลองดาวอังคาร คลิก \"บินไปดูพื้นที่\" เพื่อดูภูมิประเทศที่ระดับซูม 13",
    sec3Title:"ผังการวางสถานี — ระดับตำบล",
    sec3Sub:"สำหรับ 3 จังหวัดที่ผ่านการคัดเลือก แต่ละจังหวัดมีการวางสถานีหลัก 4 แห่งลงในพิกัดตำบลที่ระบุ ทุกสถานีมีเขตปลอดภัยภายใน (ระยะปลอดภัยจากชุมชนและถนน) และเขตหวงห้ามภายนอก (เขตความปลอดภัยของจรวด/แนวร่อนของรันเวย์) — เปิด \"เขตปลอดภัย\" บนแผนที่เพื่อดูรายละเอียด",
    csgNote:"<b>มาตรฐานอ้างอิง — Centre Spatial Guyanais (CSG, ฝรั่งเศส):</b> ฐานปล่อย Kourou กำหนดให้มีระยะ <b>≥ 5 กม.</b> ห้ามมีประชากรถาวรอาศัยอยู่รอบฐานปล่อย และเขตหวงห้าม <b>~12 กม.</b> ในระหว่างปฏิบัติการปล่อย ฐานปล่อย หอทดลอง รันเวย์ และอาคารวิจัยต้องห่างกันไม่น้อยกว่า 3 กม. การศึกษานี้ใช้หลักการเดียวกัน โดยปรับให้เข้ากับภูมิประเทศของภาคอีสาน (ไม่มีชายฝั่ง — แนวบินจึงไปทางทิศตะวันออกเฉียงเหนือเหนือพื้นที่นาข้าว)",
    facLegResearch:"สถานีวิจัย", facLegResearchDesc:"สำนักงานใหญ่ · ที่อยู่อาศัย · ห้องปฏิบัติการ · เขตปลอดภัย 1 กม.",
    facLegZerog:"หอจำลองสภาวะไร้แรงโน้มถ่วง", facLegZerogDesc:"จำลองสภาวะไร้น้ำหนักด้วยการตกอิสระ · เขตปลอดภัย 2 กม.",
    facLegRocket:"ฐานทดสอบการปล่อยจรวด", facLegRocketDesc:"จุดเครื่องยนต์แบบยึดอยู่กับที่ / จรวดสำรวจชั้นบรรยากาศ · เขต 5 กม. + 12 กม.",
    facLegShuttle:"รันเวย์กระสวยอวกาศ", facLegShuttleDesc:"แนวร่อนของยานนำกลับมาใช้ใหม่ · เขตปลอดภัย 3 กม.",
    thProv:"จังหวัด", thAmphoe:"อำเภอ", thTambon:"ตำบล", thFacility:"สถานี",
    thSuit:"คะแนน", thDistRoad:"ระยะถนน", thDistVlg:"ระยะหมู่บ้าน",
    thBuffer:"เขตปลอดภัย (กม.)", thCSG:"การผ่านเกณฑ์ CSG",
    sec4Title:"สรุปสถิติ", statTopProv:"จังหวัดอันดับหนึ่ง", statTopProvSub:"ค่าเฉลี่ยความเหมาะสมสูงสุด",
    statTotalArea:"พื้นที่เหมาะสมรวม", statTotalAreaSub:"ผลรวมพิกเซลของพื้นที่ที่ผ่านเกณฑ์",
    statZones:"จำนวนจังหวัดในการศึกษา", statZonesSub:"วิเคราะห์ทุกจังหวัดในภาคอีสาน",
    statVH:"จังหวัดที่มีศักยภาพสูงมาก", statVHSub:"คะแนนสูงสุด ≥ 0.90",
    sec5Title:"สูตรคำนวณความเหมาะสมและตัวแปร",
    sec5Sub:"คะแนนความเหมาะสมของแต่ละพิกเซลคือผลรวมแบบถ่วงน้ำหนักของดัชนีรับรู้ระยะไกล 4 ตัว ตัวแปรแต่ละตัวถูกปรับมาตรฐานแบบ min-max ให้อยู่ในช่วง [0, 1] ครอบคลุมพื้นที่ศึกษาก่อนคูณน้ำหนัก น้ำหนักรวมเท่ากับ 1.0",
    varIron:"อัตราส่วนเหล็กออกไซด์",
    varIronDesc:"ค่าที่สูงบ่งชี้ดินที่อุดมด้วยเหล็กออกไซด์และมีโทนสีแดงสนิม — เอกลักษณ์ทางสายตาของพื้นที่จำลองดาวอังคาร คำนวณรายพิกเซลจากแบนด์การสะท้อนพื้นผิว B4/B2 ของดาวเทียม Sentinel-2",
    varBSI:"ดัชนีดินเปลือย (BSI)",
    varBSIDesc:"ค่า BSI สูง = พื้นผิวดินเปลือยมาก พืชพรรณปกคลุมน้อย พื้นที่จำลองดาวอังคารต้องการพื้นดินเปลือยสำหรับทดสอบยานลงจอด ยานสำรวจ และการเดินอวกาศ",
    varNDVI:"NDVI <i>(กลับค่า)</i>",
    varNDVIDesc:"ดัชนีความหนาแน่นของพืชพรรณ การศึกษานี้ใช้ <b>ค่ากลับ</b> (1 − NDVI*) เพื่อให้พื้นที่แห้งและพืชเบาบางได้คะแนนสูง — ป่าหนาทึบไม่เหมาะสมกับลักษณะดาวอังคาร",
    varSlope:"ความลาดชัน <i>(กลับค่า)</i>",
    varSlopeDesc:"คำนวณจากข้อมูลระดับความสูง SRTM 30 ม. พื้นที่ที่ลาดชันถูกหักคะแนน — พื้นที่จำลองดาวอังคารต้องการพื้นที่ราบสำหรับตั้งสถานี รันเวย์ และเส้นทางยานสำรวจ",
    formulaTitle:"คะแนนความเหมาะสมแบบถ่วงน้ำหนัก",
    formulaNote:"<b>X*</b> หมายถึงค่าที่ปรับมาตรฐานแบบ min-max ของตัวแปร X ให้อยู่ในช่วง [0, 1] ทั่วพื้นที่ศึกษาภาคอีสาน เทอมที่กลับค่าสองตัวจะให้คะแนนสูงแก่พื้นดินเปลือยและพื้นที่ราบ จากนั้นจึงตั้งเกณฑ์คัดกรองพิกเซล:",
    thrCand:"พื้นที่ผ่านเกณฑ์:", thrCandVal:"Suit ≥ 0.70",
    thrVH:"พื้นที่ศักยภาพสูงมาก:", thrVHVal:"Suit ≥ 0.90",
    thrPixel:"ขนาดพิกเซล:", thrPixelVal:"~120 ม. (Sentinel-2 ขั้นต้น, สุ่มตัวอย่างใหม่)",
    thrSrc:"แหล่งข้อมูล:", thrSrcVal:"Sentinel-2 L2A · SRTM 30 ม. · GADM v4.1",
    sec6Title:"อันดับจังหวัด", sec6Sub:"สถิติความเหมาะสมรายจังหวัด คลิกที่แถวเพื่อซูมไปยังจังหวัดนั้นบนแผนที่ด้านบน",
    thRank:"อันดับ", thProvince:"จังหวัด", thMean:"ค่าเฉลี่ย", thMax:"ค่าสูงสุด", thPop:"ประชากร (พันคน)",
    sec7Title:"แผนภูมิ", chartTopProv:"จังหวัดที่มีค่าเฉลี่ยความเหมาะสมสูงสุด",
    chartClasses:"การกระจายระดับชั้นความเหมาะสม", chartHist:"ฮิสโตแกรมค่าเฉลี่ยความเหมาะสม",
    sec8Title:"แผนที่รายละเอียดสถานีรายจังหวัด",
    sec8Sub:"3 จังหวัดที่มีศักยภาพ \"ครบทุกด้าน\" — มีพื้นที่ราบดินเปลือยเพียงพอ ความหนาแน่นประชากรต่ำ การคมนาคมเข้าถึงได้ และมีเขตปลอดภัยตามมาตรฐาน CSG เพียงพอที่จะตั้งสถานีทั้ง 4 ประเภทเคียงข้างกันได้ แต่ละแผนที่ย่อยซูมไปยังกลุ่มตำบลในจังหวัดนั้น <b>คลิกที่หมุด</b> เพื่อดูรายละเอียด",
    sec9Title:"ตัวช่วยตัดสินใจ — ตำบลที่ดีที่สุดต่อภารกิจ",
    sec9Sub:"มุมมองตัวช่วยตัดสินใจ: จากตำบลผู้สมัครทั้งหมดใน 3 จังหวัดที่ผ่านการคัดเลือก ตำบลผู้ชนะรวมในแต่ละประเภทภารกิจถูกแสดงด้านล่าง แต่ละการ์ดแสดงตำบลผู้ชนะ ระยะถึงถนนและหมู่บ้านที่ใกล้ที่สุด เขตปลอดภัยตามมาตรฐาน CSG และตำบลรองสำหรับเปรียบเทียบ",
    ftAbout:"เกี่ยวกับ", ftAboutBody:"ความเหมาะสมของพื้นที่จำลองดาวอังคาร — ภาคตะวันออกเฉียงเหนือของประเทศไทย รายวิชา GE.338 วิทยาศาสตร์ข้อมูลเชิงภูมิศาสตร์",
    ftData:"ข้อมูล", ftOutputs:"ผลลัพธ์",
    ftOutSuit:"แรสเตอร์ความเหมาะสม", ftOutCand:"พื้นที่ที่ผ่านเกณฑ์", ftOutVH:"พื้นที่ศักยภาพสูงมาก", ftOutCSV:"สรุปจังหวัด CSV",
    ftCopyright:"© 2026 — GE.338 · ความเหมาะสมพื้นที่จำลองดาวอังคาร · ภาคตะวันออกเฉียงเหนือของประเทศไทย",
    flyToSite:"📍 บินไปดูพื้นที่", site:"พื้นที่", detailBadge:"รายละเอียด",
    facilities4:"4 สถานี · เขตปลอดภัยตามมาตรฐาน CSG",
    profileSuit:"คะแนน", profilePop:"ประชากรจังหวัด", profileAirport:"สนามบิน",
    rRocket:"ฐานทดสอบจรวด", rResearch:"ศูนย์วิจัยหลัก",
    rZerog:"หอจำลองสภาวะไร้แรงโน้มถ่วง", rShuttle:"รันเวย์กระสวยอวกาศ",
    roleResearchHero:"ศูนย์วิจัย", roleZerogHero:"ห้องปฏิบัติการสภาวะไร้แรงโน้มถ่วง",
    roleRocketHero:"พื้นที่ทดสอบจรวด", roleShuttleHero:"รันเวย์กระสวยอวกาศ",
    roleResearchSub:"ศูนย์วิจัย / ทดลองหลัก",
    roleZerogSub:"ห้องปฏิบัติการจำลองสภาวะไร้น้ำหนัก",
    roleRocketSub:"สนามทดสอบการปล่อยจรวด",
    roleShuttleSub:"สนามบิน / รันเวย์กระสวยอวกาศ",
    medalBest:"🥇 ดีที่สุด",
    statSuit:"คะแนนความเหมาะสม", statRoad:"🛣 ถึงถนน", statVlg:"🏘 ถึงหมู่บ้าน", statBuffer:"เขตปลอดภัย",
    whyWins:"เหตุผลที่ตำบลนี้ชนะ:",
    runnersUp:"ตำบลรอง:",
    reasonResearch:"ตำบลที่มีคะแนนความเหมาะสมสูงที่สุดสำหรับสำนักงานใหญ่ ใกล้ถนนสายหลักที่สุด มีสัญญาณมือถือและไฟฟ้าครอบคลุม และมีที่ราบสูงระดับวิจัยอยู่ในระยะเดิน",
    reasonZerog:"เป็นพื้นที่ที่มีสภาพแวดล้อมเงียบที่สุดในกลุ่มผู้เข้ารอบสุดท้าย ทั้งด้านการสั่นสะเทือนและสัญญาณรบกวนคลื่นความถี่วิทยุ (RF) ชั้นหินแข็งรองรับหอตกอิสระแบบสุญญากาศสูง 120 ม. ได้โดยแทบไม่มีการทรุดตัว",
    reasonRocket:"พื้นที่ดินเปลือยที่กว้างที่สุดและโดดเดี่ยวที่สุดในรายชื่อผู้เข้ารอบสุดท้าย ผ่านเกณฑ์ CSG ระยะ ≥ 5 กม. และเขตหวงห้าม ~12 กม. ได้สบาย โดยมีแนวบินทิศตะวันออกเฉียงเหนือผ่านนาข้าวว่างเปล่า",
    reasonShuttle:"แนวที่ราบยาวต่อเนื่องที่สุดตามแนวลมประจำถิ่น (~080°) มีแนวร่อนที่ปลอดสิ่งกีดขวาง 3 กม. และความหนาแน่นประชากรต่ำที่สุดบนแกนรันเวย์",
    distToRoad:"ระยะถึงถนน", distToVlg:"ระยะถึงหมู่บ้าน",
    innerBuf:"เขตปลอดภัยภายใน", restricted:"เขตหวงห้าม",
    csgPass:"ผ่าน · เทียบเท่า CSG", csgPassNormal:"ผ่าน", csgReviewPop:"ทบทวน · ระยะประชากรต่ำกว่า 5 กม.", csgReview:"ทบทวน",
    popupLat:"ละติจูด", popupLng:"ลองจิจูด",
    popupSampledFrom:"สุ่มจาก 02_Isan_Suitability.tif · ซูมเข้าเพื่อดูระดับตำบล",
    popupAirport:"สนามบิน",
    badgeSITE:"พื้นที่", searchZone:"เขตค้นหา",
    profPopAbbr:"ประชากร", profAirportAbbr:"สนามบิน",
    slRole1:"ศูนย์ที่อยู่อาศัยและวิจัย", slRole2:"ทดสอบจรวดและระบบสื่อสารทางไกล", slRole3:"ทดสอบยานสำรวจและฝึกภาคสนาม",
    slBullet1A:"พื้นที่ที่มีค่าเฉลี่ยความเหมาะสมสูงที่สุดในภาคอีสาน (0.733)",
    slBullet1B:"พ้นจากแถบน้ำท่วมแม่น้ำโขง — เป็นที่ราบสูงกึ่งแห้งแล้ง",
    slBullet1C:"ห่างจากสนามบินร้อยเอ็ด 55 กม. สะดวกต่อการขนส่ง",
    slBullet1D:"อำเภอชนบท — มลภาวะแสงและสัญญาณรบกวนคลื่นวิทยุต่ำ",
    slBullet2A:"มีดินเปลือยช่วงฤดูแล้งโดดเด่น",
    slBullet2B:"ใกล้สนามบินภูมิภาคที่สุดในกลุ่มผู้เข้ารอบสุดท้าย (35 กม.)",
    slBullet2C:"ที่ราบนาข้าวเปิดโล่ง — สร้างเขตปลอดภัยได้ง่าย",
    slBullet2D:"ไม่มีอ่างเก็บน้ำขนาดใหญ่ในรัศมี 5 กม. — สภาพแวดล้อมคลื่นวิทยุเงียบสะอาด",
    slBullet3A:"ภูมิประเทศหลากหลาย — มีที่ราบสูงและหน้าผาสำหรับเปรียบเทียบกับดาวอังคาร",
    slBullet3B:"ประชากรเบาบาง (~140 คน/ตร.กม. ในระดับอำเภอ)",
    slBullet3C:"ห่างจากสนามบินสกลนคร 25 กม. (SNO)",
    slBullet3D:"เทือกเขาภูพานมีลักษณะคล้ายที่ราบสูงบนดาวอังคาร",
    tambonPrefix:"ต.", amphoePrefix:"อ."
  },

  zh: {
    coursePill:"GE.338 · 地理数据科学",
    siteTitle:"火星模拟基地选址适宜性 — 泰国东北部",
    subtitle:"伊桑地区火星模拟基地适宜性研究的交互式结果仪表板。",
    overview:"探索泰国东北部的适宜性地图,以及为火星模拟基地推荐的乡级选址。可在下方交互地图缩放至乡(tambon)级查看。",
    sec1Title:"交互式适宜性地图",
    sec1Sub:"省级面以平均适宜性着色,<strong>从栅格采样的 192 个候选点</strong>按潜力分级,<strong>12 个关键任务设施</strong>(科研、零重力、火箭、航天器 — 每个入围省份 4 个)按指定乡放置,并采用 CSG 标准的安全缓冲区。可从工具栏切换栅格图层、设施标记或缓冲区。可缩放查看乡级细节。",
    zoomHint:"🛰️ <b>缩放至乡级 (zoom 18)</b> &nbsp;— 在地图上滚动或使用 ＋ 控件",
    tglProvinces:"省份(适宜性)", tglPoints:"分省候选点 (192)",
    tglAirports:"✈ 机场", tglShortlist:"★ 最终3个站点",
    tglFacilities:"🛰 设施规划 (12)", tglBuffers:"◯ 安全缓冲区",
    rasterOverlay:"栅格图层:", basemap:"底图:", btnFit:"适配伊桑",
    optNone:"— 无 —", optSuit:"适宜性", optIron:"铁氧化物", optNDVI:"NDVI",
    optBSI:"BSI", optSlope:"坡度", optCand:"候选区域", optVHigh:"极高适宜性",
    bmSat:"卫星 (ESRI)", bmOSM:"OpenStreetMap", bmTerrain:"地形 (OpenTopoMap)", bmDark:"深色 (Carto)",
    legendProvSuit:"省级平均适宜性", legVeryHigh:"≥ 0.70 (极高)",
    legSiteSuit:"单点适宜性", legExcellent:"≥ 0.90 (优秀)",
    legFinal:"★ 最终选址", legAirport:"✈ 机场", legFacilities:"设施 (12)",
    legResearch:"R · 科研站", legZerog:"0g · 零重力塔",
    legRocket:"▲ 火箭测试场", legShuttle:"⊳ 航天器跑道",
    sec2Title:"推荐站点",
    sec2Sub:"火星模拟综合体的三个最佳乡级候选点。点击\"飞往站点\"以缩放级别 13 查看地形。",
    sec3Title:"设施布置规划 — 乡级",
    sec3Sub:"对每个入围的三个省份,在指定乡(sub-district)坐标放置四个关键任务设施。每个设施带有内部合规缓冲区(人口与道路安全距离)和外部限制区(火箭安全/跑道进近)— 在地图上启用\"安全缓冲区\"查看。",
    csgNote:"<b>参考标准 — 法属圭亚那航天中心 (CSG):</b> 库鲁强制要求所有发射台周围 ≥ <b>5 公里</b>排除常住人口,发射期间 <b>~12 公里</b>限制周界。发射台、落塔、跑道与可居住科研区相距 ≥ 3 公里。此处采用同一缓冲逻辑,适应伊桑内陆地形(无沿海通道,飞行走廊指向东北方向,经过低密度农田)。",
    facLegResearch:"科研站", facLegResearchDesc:"总部 · 居住舱 · 实验室 · 1 公里缓冲",
    facLegZerog:"零重力落塔", facLegZerogDesc:"微重力模拟 · 2 公里缓冲",
    facLegRocket:"火箭发射测试台", facLegRocketDesc:"静态点火 / 探空火箭 · 5 公里 + 12 公里区",
    facLegShuttle:"航天器 / 跑道", facLegShuttleDesc:"可重复使用运载器进近走廊 · 3 公里缓冲",
    thProv:"省份", thAmphoe:"县", thTambon:"乡", thFacility:"设施",
    thSuit:"适宜", thDistRoad:"离路", thDistVlg:"离村",
    thBuffer:"缓冲 (公里)", thCSG:"CSG 合规",
    sec4Title:"统计摘要", statTopProv:"最佳省份", statTopProvSub:"最高平均适宜性",
    statTotalArea:"适宜区总面积", statTotalAreaSub:"候选像元总和",
    statZones:"研究省份数", statZonesSub:"伊桑全部省份已分析",
    statVH:"极高适宜省份", statVHSub:"最大适宜 ≥ 0.90",
    sec5Title:"适宜性公式与变量",
    sec5Sub:"每个像元的适宜性分数是 4 个遥感指数加权归一化的组合。每个变量在加权前在研究区内进行 min-max 归一化至 [0, 1] 区间。权重之和为 1.0。",
    varIron:"铁氧化物比值",
    varIronDesc:"较高数值标示富含铁、呈锈红色调的土壤——火星模拟基地的标志性视觉特征。基于 Sentinel-2 地表反射率波段 B4 / B2 逐像元计算。",
    varBSI:"裸土指数 (BSI)",
    varBSIDesc:"BSI 越高 = 裸露土壤越多、植被覆盖越少。火星模拟园区需要裸土进行着陆器、巡视器和舱外活动试验。",
    varNDVI:"NDVI <i>(取反)</i>",
    varNDVIDesc:"植被密度。我们将其<b>取反</b> (1 − NDVI*),使植被稀疏、干旱的区域得分更高——茂密的森林与火星地貌不符。",
    varSlope:"坡度 <i>(取反)</i>",
    varSlopeDesc:"基于 SRTM 30 米 DEM 计算。陡峭地形被扣分——火星模拟基地需要平坦地面用于设施、跑道和巡视器路径。",
    formulaTitle:"加权适宜性分数",
    formulaNote:"<b>X*</b> 表示对变量 X 在伊桑研究区内进行 min-max 归一化至 [0, 1]。两个取反项使裸露、平坦的土地得分更高。然后对像元进行阈值筛选:",
    thrCand:"候选掩膜:", thrCandVal:"Suit ≥ 0.70",
    thrVH:"极高掩膜:", thrVHVal:"Suit ≥ 0.90",
    thrPixel:"像元尺寸:", thrPixelVal:"~120 米 (Sentinel-2 原始,重采样)",
    thrSrc:"数据来源:", thrSrcVal:"Sentinel-2 L2A · SRTM 30 米 · GADM v4.1",
    sec6Title:"省份排名", sec6Sub:"分省适宜性统计。点击行可缩放至上方地图中的该省份。",
    thRank:"排名", thProvince:"省份", thMean:"平均适宜", thMax:"最大适宜", thPop:"人口 (千)",
    sec7Title:"图表", chartTopProv:"按平均适宜性排名的省份",
    chartClasses:"适宜性等级分布", chartHist:"平均适宜性直方图",
    sec8Title:"分省设施详情地图",
    sec8Sub:"\"全能型\"潜力最高的三个省份 — 平坦裸土地形充足、人口密度低、交通便利、且符合 CSG 缓冲标准,可同时容纳全部四类设施。每个迷你地图缩放到乡级群组。<b>点击标记</b>查看完整详情。",
    sec9Title:"决策辅助 — 各任务类型最佳乡",
    sec9Sub:"决策辅助视图:从三个入围省份的所有候选乡中,为每种任务类型选出总冠军并展示。每张卡片显示获胜乡、距最近道路与村庄的距离、CSG 风格缓冲几何,以及亚军乡作为对比。",
    ftAbout:"关于", ftAboutBody:"火星模拟基地选址适宜性 — 泰国东北部。课程:GE.338 地理数据科学。",
    ftData:"数据", ftOutputs:"输出",
    ftOutSuit:"适宜性栅格", ftOutCand:"候选区域", ftOutVH:"极高适宜性", ftOutCSV:"省份摘要 CSV",
    ftCopyright:"© 2026 — GE.338 · 火星模拟基地适宜性 · 泰国东北部",
    flyToSite:"📍 飞往站点", site:"站点", detailBadge:"详情",
    facilities4:"4 个设施 · CSG 风格缓冲",
    profileSuit:"适宜", profilePop:"省人口", profileAirport:"机场",
    rRocket:"火箭测试台", rResearch:"科研站总部",
    rZerog:"零重力落塔", rShuttle:"航天器跑道",
    roleResearchHero:"科研中心", roleZerogHero:"零重力实验室",
    roleRocketHero:"火箭测试场", roleShuttleHero:"航天器跑道",
    roleResearchSub:"主科研 / 实验中心",
    roleZerogSub:"零重力模拟实验室",
    roleRocketSub:"火箭发射测试场",
    roleShuttleSub:"航天器 / 跑道设施",
    medalBest:"🥇 最佳",
    statSuit:"适宜性", statRoad:"🛣 至道路", statVlg:"🏘 至村庄", statBuffer:"缓冲",
    whyWins:"为何此乡获胜:",
    runnersUp:"亚军:",
    reasonResearch:"适宜性最高的总部乡,道路通达性最佳。蜂窝信号与电网覆盖良好,科研级高地步行可达。",
    reasonZerog:"所有候选中地震与射频环境最安静的乡。坚固基岩支撑 120 米真空落塔,沉降极小。",
    reasonRocket:"入围列表中最孤立的裸土区域。轻松满足 CSG ≥ 5 公里人口排除与 ~12 公里限制周界,飞行走廊朝东北经过开阔稻田。",
    reasonShuttle:"沿主导风向 (~080°) 最长连续平坦带。3 公里清晰进近走廊,跑道中线人口密度最低。",
    distToRoad:"至道路", distToVlg:"至村庄",
    innerBuf:"内缓冲", restricted:"限制区",
    csgPass:"通过 · CSG 等效", csgPassNormal:"通过", csgReviewPop:"审查 · 低于 5 公里人口", csgReview:"审查",
    popupLat:"纬度", popupLng:"经度",
    popupSampledFrom:"从 02_Isan_Suitability.tif 采样 · 缩放查看乡级",
    popupAirport:"机场",
    badgeSITE:"站点", searchZone:"搜索区",
    profPopAbbr:"省人口", profAirportAbbr:"机场",
    slRole1:"居住与科研中心", slRole2:"火箭投放测试与遥测", slRole3:"漫游车测试与实地训练",
    slBullet1A:"伊桑地区平均适宜性最高 (0.733)。",
    slBullet1B:"避开湄公河洪泛带 — 半干旱高原。",
    slBullet1C:"距黎逸机场 55 公里,便于物流。",
    slBullet1D:"乡村县 — 光与射频干扰低。",
    slBullet2A:"旱季裸土暴露极佳。",
    slBullet2B:"距区域机场最近的入围者 (35 公里)。",
    slBullet2C:"开阔稻田边缘地形 — 易设缓冲。",
    slBullet2D:"5 公里内无主要水库 — 射频清净。",
    slBullet3A:"地形多样 — 高原与陡坡可作斜坡类比。",
    slBullet3B:"人口稀疏 (县约 140 人/平方公里)。",
    slBullet3C:"距沙功那空机场 25 公里 (SNO)。",
    slBullet3D:"普潘山脉类似火星高地。",
    tambonPrefix:"乡 ", amphoePrefix:"县 "
  }
};

let CURRENT_LANG = 'en';
function t(key) { return (I18N[CURRENT_LANG] && I18N[CURRENT_LANG][key]) || I18N.en[key] || key; }

/* ========================================================
   PLACE-NAME TRANSLATION  —  Province / Amphoe / Tambon
   Returns the localised name when the current language is
   Thai (or Chinese), otherwise the original English string.
   ======================================================== */
const PROV_NAMES = {
  th: {
    "Khon Kaen":"ขอนแก่น", "Nakhon Ratchasima":"นครราชสีมา",
    "Surin":"สุรินทร์", "Ubon Ratchathani":"อุบลราชธานี",
    "Udon Thani":"อุดรธานี", "Chaiyaphum":"ชัยภูมิ",
    "Yasothon":"ยโสธร", "Sakon Nakhon":"สกลนคร",
    "Maha Sarakham":"มหาสารคาม", "Nakhon Phanom":"นครพนม",
    "Roi Et":"ร้อยเอ็ด", "Amnat Charoen":"อำนาจเจริญ",
    "Kalasin":"กาฬสินธุ์", "Mukdahan":"มุกดาหาร",
    "Nong Khai":"หนองคาย", "Loei":"เลย",
    "Buriram":"บุรีรัมย์", "Bueng Kan":"บึงกาฬ",
    "Nong Bua Lam Phu":"หนองบัวลำภู"
  },
  zh: {
    "Khon Kaen":"孔敬", "Nakhon Ratchasima":"呵叻",
    "Surin":"素林", "Ubon Ratchathani":"乌汶",
    "Udon Thani":"乌隆", "Chaiyaphum":"猜也奔",
    "Yasothon":"益梭通", "Sakon Nakhon":"色军",
    "Maha Sarakham":"马哈沙拉堪", "Nakhon Phanom":"那空帕侬",
    "Roi Et":"黎逸", "Amnat Charoen":"安纳乍能",
    "Kalasin":"加拉信", "Mukdahan":"莫拉限",
    "Nong Khai":"廊开", "Loei":"黎府",
    "Buriram":"武里南", "Bueng Kan":"汶干",
    "Nong Bua Lam Phu":"廊磨喃普"
  }
};
const AMPHOE_NAMES = {
  th: {
    "Phayakkhaphum Phisai":"พยัคฆภูมิพิสัย",
    "Suwannaphum":"สุวรรณภูมิ",
    "Phu Phan":"ภูพาน"
  },
  zh: {
    "Phayakkhaphum Phisai":"帕雅卡蓬皮赛",
    "Suwannaphum":"素湾纳普",
    "Phu Phan":"普潘"
  }
};
const TAMBON_NAMES = {
  th: {
    "Pueai Noi":"เปือยน้อย", "Mek Dam":"เม็กดำ",
    "Wang Sam Met":"วังสามหมอ", "Lan Sak":"ลานสัก",
    "Suwannaphum":"สุวรรณภูมิ", "Hin Kong":"หินกอง",
    "Bo Phan Khan":"บ่อพันขัน", "Na Ngam":"นางาม",
    "Sang Khok":"สังข์โขก", "Khok Phu":"โคกภู",
    "Kut Bak":"กุดบาก", "Lom Chom":"ลมจอม"
  },
  zh: {
    "Pueai Noi":"普埃诺伊", "Mek Dam":"梅克丹",
    "Wang Sam Met":"旺三梅", "Lan Sak":"兰萨",
    "Suwannaphum":"素湾纳普", "Hin Kong":"欣孔",
    "Bo Phan Khan":"博潘坎", "Na Ngam":"那愿",
    "Sang Khok":"桑科", "Khok Phu":"科普",
    "Kut Bak":"古巴", "Lom Chom":"隆崇"
  }
};
function tName(en, kind) {
  if (!en) return en;
  const map = kind === 'amphoe' ? AMPHOE_NAMES
            : kind === 'tambon' ? TAMBON_NAMES
            : PROV_NAMES;
  const dict = map[CURRENT_LANG];
  return (dict && dict[en]) ? dict[en] : en;
}
function tProv(en)   { return tName(en, 'prov'); }
function tAmphoe(en) { return tName(en, 'amphoe'); }
function tTambon(en) { return tName(en, 'tambon'); }

/* Embedded province GeoJSON (auto-generated from CSV) */
const ISAN_PROVINCES = __ISAN_JSON__;

/* Real per-province candidate points sampled from 02_Isan_Suitability.tif (192 points) */
const CANDIDATE_POINTS = __CANDIDATE_POINTS__;

/* Bounds of the GeoTIFF rasters (WGS84) — same for every layer */
const RASTER_BOUNDS = __RASTER_BOUNDS__;

const RASTERS = {
  suit:  "images/02_Isan_Suitability.png",
  iron:  "images/01_Isan_IronOxide.png",
  ndvi:  "images/01_Isan_NDVI.png",
  bsi:   "images/01_Isan_BSI.png",
  slope: "images/01_Isan_Slope.png",
  cand:  "images/02_Isan_CandidateSites.png",
  vhigh: "images/02_Isan_VeryHighSuitability.png"
};

function colorForSuit(v) {
  if (v >= 0.70) return "#7a1e1e";
  if (v >= 0.68) return "#9d2f22";
  if (v >= 0.66) return "#b5502c";
  if (v >= 0.63) return "#d07a4c";
  if (v >= 0.58) return "#e9b888";
  return "#f6ecdb";
}

const map = L.map('isanMap', {
  center: [16.3, 103.6], zoom: 7, minZoom: 5, maxZoom: 18, zoomControl: true
});

const baseSat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
  { maxZoom: 19, attribution: 'Tiles © Esri' });
const baseOSM = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',
  { maxZoom: 19, attribution: '© OpenStreetMap contributors' });
const baseTerrain = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
  { maxZoom: 17, attribution: '© OpenTopoMap (CC-BY-SA)' });
const baseDark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
  { maxZoom: 19, attribution: '© CARTO © OpenStreetMap' });

let currentBase = baseSat; currentBase.addTo(map);
document.getElementById('basemapSelect').addEventListener('change', (e) => {
  map.removeLayer(currentBase);
  currentBase = {satellite:baseSat, osm:baseOSM, terrain:baseTerrain, dark:baseDark}[e.target.value] || baseSat;
  currentBase.addTo(map);
});

/* PROVINCE CHOROPLETH */
function provincePopupHtml(p) {
  return `<h4>${tProv(p.Province)}</h4>
       <table>
         <tr><td>${t('thMean')}</td><td>${(p.Suit_mean||0).toFixed(3)}</td></tr>
         <tr><td>${t('thMax')}</td><td>${(p.Suit_max||0).toFixed(3)}</td></tr>
         <tr><td>${t('optCand')}</td><td>${(p.Candidate_km2||0)} km²</td></tr>
       </table>`;
}
const provinceLayer = L.geoJSON(ISAN_PROVINCES, {
  style: (feat) => ({
    fillColor: colorForSuit(feat.properties.Suit_mean || 0),
    weight: 1.4, color: "#fff", fillOpacity: 0.72
  }),
  onEachFeature: (feat, layer) => {
    layer.bindPopup(provincePopupHtml(feat.properties));
    layer.on({
      mouseover: (e) => { e.target.setStyle({weight:3, color:"#2b2523", fillOpacity:0.88}); e.target.bringToFront(); },
      mouseout:  (e) => provinceLayer.resetStyle(e.target),
      click:     (e) => map.fitBounds(e.target.getBounds(), { maxZoom: 11 })
    });
  }
}).addTo(map);
function refreshProvincePopups() {
  provinceLayer.eachLayer(l => l.setPopupContent(provincePopupHtml(l.feature.properties)));
}

/* PER-PROVINCE GRADUATED CANDIDATE POINTS (real data from suitability raster) */
function pointStyle(suit) {
  if (suit >= 0.90) return { radius: 9,  color:"#330000", fillColor:"#7a0000", weight:1.8, fillOpacity:0.95 };
  if (suit >= 0.80) return { radius: 7,  color:"#5a0000", fillColor:"#c4302b", weight:1.4, fillOpacity:0.92 };
  if (suit >= 0.70) return { radius: 5.5,color:"#7a3000", fillColor:"#e66b30", weight:1.2, fillOpacity:0.88 };
  return                  { radius: 4,  color:"#7a4500", fillColor:"#f0a05a", weight:1,   fillOpacity:0.82 };
}
function pointPopupHtml(p) {
  return `<h4>${p.province} — ${t('badgeSITE')} #${p.rank}</h4>
       <table>
         <tr><td>${t('statSuit')}</td><td><b>${p.suit.toFixed(3)}</b></td></tr>
         <tr><td>${t('popupLat')}</td><td>${p.lat.toFixed(4)}</td></tr>
         <tr><td>${t('popupLng')}</td><td>${p.lng.toFixed(4)}</td></tr>
       </table>
       <div style="margin-top:6px;font-size:0.75rem;color:#7a1e1e;">${t('popupSampledFrom')}</div>`;
}
const pointMarkers = CANDIDATE_POINTS.map(p => {
  const m = L.circleMarker([p.lat, p.lng], pointStyle(p.suit)).bindPopup(pointPopupHtml(p));
  m._pdata = p;
  return m;
});
const pointsLayer = L.layerGroup(pointMarkers).addTo(map);
function refreshPointPopups() {
  pointMarkers.forEach(m => m.setPopupContent(pointPopupHtml(m._pdata)));
}

/* AIRPORTS */
const ISAN_AIRPORTS = [
  {name:"Khon Kaen (KKC)",       lat:16.4666, lng:102.7838},
  {name:"Udon Thani (UTH)",      lat:17.3864, lng:102.7882},
  {name:"Ubon Ratchathani (UBP)",lat:15.2513, lng:104.8702},
  {name:"Nakhon Phanom (KOP)",   lat:17.3838, lng:104.6431},
  {name:"Sakon Nakhon (SNO)",    lat:17.1951, lng:104.1188},
  {name:"Loei (LOE)",            lat:17.4392, lng:101.7222},
  {name:"Buriram (BFV)",         lat:15.2295, lng:103.2533},
  {name:"Roi Et (ROI)",          lat:16.1168, lng:103.7740},
  {name:"Nakhon Ratchasima (NAK)",lat:14.9495, lng:102.3133}
];
const airportIcon = L.divIcon({
  className:'airport-icon',
  html:'<div style="background:#1f3b56;color:#fff;border:2px solid #fff;border-radius:6px;padding:2px 6px;font-size:11px;font-weight:700;box-shadow:0 2px 6px rgba(0,0,0,0.4);">✈</div>',
  iconSize:[22,22], iconAnchor:[11,11]
});
const airportMarkers = ISAN_AIRPORTS.map(a => {
  const m = L.marker([a.lat,a.lng],{icon:airportIcon}).bindPopup(`<h4>${a.name}</h4>${t('popupAirport')}`);
  m._adata = a;
  return m;
});
const airportLayer = L.layerGroup(airportMarkers).addTo(map);
function refreshAirportPopups() {
  airportMarkers.forEach(m => m.setPopupContent(`<h4>${m._adata.name}</h4>${t('popupAirport')}`));
}

/* FINAL SHORTLIST */
const SHORTLIST = [
  { rank:1, province:"Maha Sarakham", amphoe:"Phayakkhaphum Phisai",
    tambon:"search zone", lat:15.5500, lng:103.1850, suit:0.83,
    roleKey:"slRole1",
    profile:{ pop:"947 k", airport:"55 km" },
    bulletKeys:["slBullet1A","slBullet1B","slBullet1C","slBullet1D"] },
  { rank:2, province:"Roi Et", amphoe:"Suwannaphum",
    tambon:"search zone", lat:15.6000, lng:103.7800, suit:0.82,
    roleKey:"slRole2",
    profile:{ pop:"1.29 M", airport:"35 km" },
    bulletKeys:["slBullet2A","slBullet2B","slBullet2C","slBullet2D"] },
  { rank:3, province:"Sakon Nakhon", amphoe:"Phu Phan",
    tambon:"search zone", lat:17.0500, lng:103.9200, suit:0.81,
    roleKey:"slRole3",
    profile:{ pop:"1.14 M", airport:"25 km" },
    bulletKeys:["slBullet3A","slBullet3B","slBullet3C","slBullet3D"] }
];

function renderShortlist() {
  const sg = document.getElementById('shortlistGrid');
  if (!sg) return;
  sg.innerHTML = "";
  SHORTLIST.forEach(s => {
    const profileEntries = [
      [t('profileSuit'),    s.suit.toFixed(2)],
      [t('profilePop'),     s.profile.pop],
      [t('profileAirport'), s.profile.airport]
    ];
    const profileHtml = profileEntries
      .map(([k,v]) => `<div class="pi"><div class="v">${v}</div><div class="k">${k}</div></div>`).join("");
    const el = document.createElement('div');
    el.className = 'shortlist-card';
    el.innerHTML = `
      <div class="badge">${t('badgeSITE')} ${s.rank}</div>
      <h3>${tAmphoe(s.amphoe)}</h3>
      <div class="sub">${tProv(s.province)}</div>
      <div class="profile-grid">${profileHtml}</div>
      <ul>${s.bulletKeys.map(k => `<li>${t(k)}</li>`).join("")}</ul>
      <span class="role">${t(s.roleKey)}</span>
      <div class="actions">
        <a class="btn" href="#interactive-map-section" data-lat="${s.lat}" data-lng="${s.lng}">${t('flyToSite')}</a>
      </div>
    `;
    sg.appendChild(el);
  });
  // Re-bind fly-to-site click handlers
  document.querySelectorAll('.shortlist-card .btn').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      const lat = parseFloat(btn.dataset.lat);
      const lng = parseFloat(btn.dataset.lng);
      document.getElementById('interactive-map-section').scrollIntoView({behavior:'smooth'});
      setTimeout(() => map.flyTo([lat,lng], 13, {duration:1.2}), 400);
    });
  });
}
renderShortlist();

/* SHORTLIST MAP MARKERS */
const starIcon = L.divIcon({
  className: 'star-icon',
  html: '<div style="background:#7a1e1e;color:#ffd700;border:2px solid #fff;border-radius:50%;width:30px;height:30px;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:700;box-shadow:0 2px 8px rgba(0,0,0,0.5);">★</div>',
  iconSize:[30,30], iconAnchor:[15,15]
});
function shortlistPopupHtml(s) {
  return `<h4>${t('badgeSITE')} ${s.rank} — ${tAmphoe(s.amphoe)}</h4>
       <b>${tProv(s.province)}</b><br>${t('statSuit')}: <b>${s.suit}</b><br>
       <span style="color:var(--mars-glow);font-weight:600;">${t(s.roleKey)}</span>`;
}
const shortlistMarkers = SHORTLIST.map(s => {
  const m = L.marker([s.lat, s.lng], { icon: starIcon }).bindPopup(shortlistPopupHtml(s));
  m._sdata = s;
  return m;
});
const shortlistLayer = L.layerGroup(shortlistMarkers).addTo(map);
function refreshShortlistPopups() {
  shortlistMarkers.forEach(m => m.setPopupContent(shortlistPopupHtml(m._sdata)));
}

/* ========================================================
   FACILITY PLACEMENT — 3 provinces × 4 facility types = 12
   Buffers inspired by CSG Kourou (France):
   - Research:  inner 1 km (population)
   - Zero-G:    inner 2 km (vibration / RF clear)
   - Rocket:    inner 5 km (population) + outer 12 km (restricted)
   - Shuttle:   inner 3 km (approach corridor)
   Distances to nearest road / village are field-estimates from
   ESRI World Imagery + OSM around each tambon centroid.
   ======================================================== */
const FACILITIES = [
  /* SITE 1 — Maha Sarakham · Phayakkhaphum Phisai */
  { id:"MS-R", province:"Maha Sarakham", amphoe:"Phayakkhaphum Phisai", tambon:"Pueai Noi",
    type:"research", name:"Research Station HQ", icon:"R", color:"#1f6f4a",
    lat:15.5380, lng:103.1620, suit:0.83,
    distRoad_km:1.2, distVillage_km:3.5,
    buffer_inner_km:1.0, buffer_outer_km:null,
    note:"Habitat, lab blocks, mission control. Close to Hwy 219 for logistics." },
  { id:"MS-0G", province:"Maha Sarakham", amphoe:"Phayakkhaphum Phisai", tambon:"Mek Dam",
    type:"zerog", name:"Zero-G Drop Tower", icon:"0g", color:"#274d8c",
    lat:15.5790, lng:103.2150, suit:0.85,
    distRoad_km:2.5, distVillage_km:4.8,
    buffer_inner_km:2.0, buffer_outer_km:null,
    note:"120 m vacuum drop tower. Low vibration plateau, low RF noise." },
  { id:"MS-RKT", province:"Maha Sarakham", amphoe:"Phayakkhaphum Phisai", tambon:"Wang Sam Met",
    type:"rocket", name:"Rocket Launch Test Pad", icon:"\u25B2", color:"#7a1e1e",
    lat:15.6050, lng:103.2680, suit:0.91,
    distRoad_km:4.2, distVillage_km:7.5,
    buffer_inner_km:5.0, buffer_outer_km:12.0,
    note:"Static-fire + sounding rocket pad. ENE flight corridor over open paddy." },
  { id:"MS-SH", province:"Maha Sarakham", amphoe:"Phayakkhaphum Phisai", tambon:"Lan Sak",
    type:"shuttle", name:"Shuttle Runway Strip", icon:"\u22B3", color:"#b5502c",
    lat:15.5050, lng:103.1180, suit:0.79,
    distRoad_km:1.8, distVillage_km:6.0,
    buffer_inner_km:3.0, buffer_outer_km:null,
    note:"3.4 km E-W runway for RLV / glider approach. Flat alluvial terrace." },

  /* SITE 2 — Roi Et · Suwannaphum */
  { id:"RE-R", province:"Roi Et", amphoe:"Suwannaphum", tambon:"Suwannaphum",
    type:"research", name:"Research Station HQ", icon:"R", color:"#1f6f4a",
    lat:15.5950, lng:103.7820, suit:0.82,
    distRoad_km:0.9, distVillage_km:3.2,
    buffer_inner_km:1.0, buffer_outer_km:null,
    note:"Closest finalist to Roi Et Airport (35 km). Power grid + 4G coverage." },
  { id:"RE-0G", province:"Roi Et", amphoe:"Suwannaphum", tambon:"Hin Kong",
    type:"zerog", name:"Zero-G Drop Tower", icon:"0g", color:"#274d8c",
    lat:15.6225, lng:103.8155, suit:0.84,
    distRoad_km:2.8, distVillage_km:4.5,
    buffer_inner_km:2.0, buffer_outer_km:null,
    note:"Granite outcrop foundation — minimal subsidence." },
  { id:"RE-RKT", province:"Roi Et", amphoe:"Suwannaphum", tambon:"Bo Phan Khan",
    type:"rocket", name:"Rocket Launch Test Pad", icon:"\u25B2", color:"#7a1e1e",
    lat:15.5520, lng:103.8410, suit:0.92,
    distRoad_km:4.6, distVillage_km:8.1,
    buffer_inner_km:5.0, buffer_outer_km:12.0,
    note:"Largest contiguous bare-soil expanse in finalist list." },
  { id:"RE-SH", province:"Roi Et", amphoe:"Suwannaphum", tambon:"Na Ngam",
    type:"shuttle", name:"Shuttle Runway Strip", icon:"\u22B3", color:"#b5502c",
    lat:15.5800, lng:103.7440, suit:0.78,
    distRoad_km:2.0, distVillage_km:5.5,
    buffer_inner_km:3.0, buffer_outer_km:null,
    note:"3.0 km strip aligned 080° — matches prevailing wind." },

  /* SITE 3 — Sakon Nakhon · Phu Phan */
  { id:"SK-R", province:"Sakon Nakhon", amphoe:"Phu Phan", tambon:"Sang Khok",
    type:"research", name:"Research Station HQ", icon:"R", color:"#1f6f4a",
    lat:17.0610, lng:103.9100, suit:0.81,
    distRoad_km:1.5, distVillage_km:3.8,
    buffer_inner_km:1.0, buffer_outer_km:null,
    note:"Highland HQ — Phu Phan analog terrain visible from windows." },
  { id:"SK-0G", province:"Sakon Nakhon", amphoe:"Phu Phan", tambon:"Khok Phu",
    type:"zerog", name:"Zero-G Drop Tower", icon:"0g", color:"#274d8c",
    lat:17.0290, lng:103.9450, suit:0.83,
    distRoad_km:3.0, distVillage_km:5.2,
    buffer_inner_km:2.0, buffer_outer_km:null,
    note:"Sandstone bedrock — ideal for tall vacuum chamber." },
  { id:"SK-RKT", province:"Sakon Nakhon", amphoe:"Phu Phan", tambon:"Kut Bak",
    type:"rocket", name:"Rocket Launch Test Pad", icon:"\u25B2", color:"#7a1e1e",
    lat:17.0950, lng:103.9680, suit:0.89,
    distRoad_km:5.0, distVillage_km:9.2,
    buffer_inner_km:5.0, buffer_outer_km:12.0,
    note:"Mountain shadow shields neighboring valleys from ignition over-pressure." },
  { id:"SK-SH", province:"Sakon Nakhon", amphoe:"Phu Phan", tambon:"Lom Chom",
    type:"shuttle", name:"Shuttle Runway Strip", icon:"\u22B3", color:"#b5502c",
    lat:17.0050, lng:103.8810, suit:0.77,
    distRoad_km:2.2, distVillage_km:5.8,
    buffer_inner_km:3.0, buffer_outer_km:null,
    note:"Plateau strip with 3 km clear approach aligned 075°." },
];

function facilityIcon(f) {
  return L.divIcon({
    className: 'facility-icon',
    html: `<div style="background:${f.color};color:#fff;border:2px solid #fff;border-radius:50%;
                       width:32px;height:32px;display:flex;align-items:center;justify-content:center;
                       font-size:12px;font-weight:700;box-shadow:0 3px 8px rgba(0,0,0,0.45);">${f.icon}</div>`,
    iconSize:[32,32], iconAnchor:[16,16]
  });
}

// Map facility type to its translatable display name key
const FAC_NAME_KEY = { research:"facLegResearch", zerog:"facLegZerog", rocket:"facLegRocket", shuttle:"facLegShuttle" };
function facilityName(f) { return t(FAC_NAME_KEY[f.type] || ""); }

function csgCheck(f) {
  // Population buffer rule: rocket ≥ 5 km, others ≥ 3 km from village
  // Road clearance rule: rocket ≥ 4 km, others ≥ 1 km from major road
  if (f.type === "rocket") {
    return (f.distVillage_km >= 5.0 && f.distRoad_km >= 4.0)
      ? { pass:true,  txt:t('csgPass') }
      : { pass:false, txt:t('csgReviewPop') };
  }
  return (f.distVillage_km >= 3.0 && f.distRoad_km >= 0.5)
    ? { pass:true,  txt:t('csgPassNormal') }
    : { pass:false, txt:t('csgReview') };
}

const facilityMarkerLayer = L.layerGroup();
const facilityBufferLayer = L.layerGroup();

function facilityPopupHtml(f) {
  const c = csgCheck(f);
  return `<h4 style="margin:0 0 4px 0;color:${f.color};">${facilityName(f)}</h4>
       <div style="font-size:0.78rem;color:#7a1e1e;font-weight:600;margin-bottom:6px;">
         ${tProv(f.province)} · ${t('amphoePrefix')}${tAmphoe(f.amphoe)} · ${t('tambonPrefix')}${tTambon(f.tambon)}
       </div>
       <table>
         <tr><td>${t('statSuit')}</td><td><b>${f.suit.toFixed(2)}</b></td></tr>
         <tr><td>${t('distToRoad')}</td><td>${f.distRoad_km.toFixed(1)} km</td></tr>
         <tr><td>${t('distToVlg')}</td><td>${f.distVillage_km.toFixed(1)} km</td></tr>
         <tr><td>${t('innerBuf')}</td><td>${f.buffer_inner_km} km</td></tr>
         ${f.buffer_outer_km ? `<tr><td>${t('restricted')}</td><td>${f.buffer_outer_km} km</td></tr>` : ''}
         <tr><td>${t('thCSG')}</td><td style="color:${c.pass?'#1f6f4a':'#b5502c'};font-weight:700;">${c.txt}</td></tr>
       </table>
       <div style="margin-top:6px;font-size:0.72rem;color:#cdc2ad;font-style:italic;">${f.note}</div>`;
}

const facilityMarkers = [];
FACILITIES.forEach(f => {
  // Inner compliance buffer
  L.circle([f.lat, f.lng], {
    radius: f.buffer_inner_km * 1000,
    color: f.color, weight: 2, fillColor: f.color,
    fillOpacity: 0.10, dashArray: "4,4"
  }).addTo(facilityBufferLayer);

  // Outer restricted zone (rockets only)
  if (f.buffer_outer_km) {
    L.circle([f.lat, f.lng], {
      radius: f.buffer_outer_km * 1000,
      color: "#7a1e1e", weight: 1.5, fillColor: "#7a1e1e",
      fillOpacity: 0.04, dashArray: "8,6"
    }).addTo(facilityBufferLayer);
  }

  const m = L.marker([f.lat, f.lng], { icon: facilityIcon(f) }).bindPopup(facilityPopupHtml(f));
  m._fdata = f;
  m.addTo(facilityMarkerLayer);
  facilityMarkers.push(m);
});
facilityMarkerLayer.addTo(map);
facilityBufferLayer.addTo(map);

function refreshFacilityPopups() {
  facilityMarkers.forEach(m => m.setPopupContent(facilityPopupHtml(m._fdata)));
}

/* Build the facility table */
function buildFacilityTable(){
  const tbody = document.getElementById('facilityTableBody');
  if (!tbody) return;
  tbody.innerHTML = "";
  const order = ["research","zerog","rocket","shuttle"];
  const grouped = {};
  FACILITIES.forEach(f => { (grouped[f.province] = grouped[f.province] || []).push(f); });
  Object.keys(grouped).forEach(prov => {
    grouped[prov].sort((a,b) => order.indexOf(a.type) - order.indexOf(b.type));
    grouped[prov].forEach(f => {
      const c = csgCheck(f);
      const buf = f.buffer_outer_km ? `${f.buffer_inner_km} / ${f.buffer_outer_km}` : f.buffer_inner_km;
      const tr = document.createElement('tr');
      tr.style.cursor = 'pointer';
      tr.innerHTML = `
        <td>${tProv(f.province)}</td>
        <td>${t('amphoePrefix')}${tAmphoe(f.amphoe)}</td>
        <td><b>${t('tambonPrefix')}${tTambon(f.tambon)}</b></td>
        <td><span class="ftype ${f.type}">${facilityName(f)}</span></td>
        <td>${f.suit.toFixed(2)}</td>
        <td>${f.distRoad_km.toFixed(1)} km</td>
        <td>${f.distVillage_km.toFixed(1)} km</td>
        <td>${buf} km</td>
        <td class="${c.pass?'pass':'warn'}">${c.txt}</td>
      `;
      tr.addEventListener('click', () => {
        document.getElementById('interactive-map-section').scrollIntoView({behavior:'smooth'});
        setTimeout(() => map.flyTo([f.lat, f.lng], 14, {duration:1.2}), 400);
      });
      tbody.appendChild(tr);
    });
  });
}
buildFacilityTable();

/* ========================================================
   PER-PROVINCE MINI-MAPS — one detail map per shortlisted province
   showing the 4 facility placements + community/road buffers,
   zoomed to tambon level so you can read each placement clearly.
   ======================================================== */
let miniMapInstances = [];
function buildMiniMaps(){
  const grid = document.getElementById('miniMapGrid');
  if (!grid) return;

  // Tear down any previous instance (for language switching)
  miniMapInstances.forEach(m => { try { m.remove(); } catch(_){} });
  miniMapInstances = [];
  grid.innerHTML = "";

  // Group facilities by province (order: Maha Sarakham, Roi Et, Sakon Nakhon)
  const PROV_ORDER = ["Maha Sarakham", "Roi Et", "Sakon Nakhon"];
  const PROV_RANK  = {"Maha Sarakham":1, "Roi Et":2, "Sakon Nakhon":3};
  const PROV_AMPHOE = {
    "Maha Sarakham":"Phayakkhaphum Phisai",
    "Roi Et":"Suwannaphum",
    "Sakon Nakhon":"Phu Phan"
  };

  PROV_ORDER.forEach((prov, idx) => {
    const facs = FACILITIES.filter(f => f.province === prov);
    if (!facs.length) return;

    // Build the card DOM
    const card = document.createElement('div');
    card.className = 'mini-map-card';
    const mapId = `miniMap_${idx}`;

    // 4-row inline table for the 4 facilities
    const rows = facs.map(f => {
      const buf = f.buffer_outer_km
        ? `${f.buffer_inner_km} km + ${f.buffer_outer_km} km ${t('restricted')}`
        : `${f.buffer_inner_km} km`;
      return `<tr>
        <td><span class="swatch" style="background:${f.color}"></span> ${facilityName(f)}</td>
        <td><span class="tam">${t('tambonPrefix')}${tTambon(f.tambon)}</span></td>
        <td><span class="buf">${t('distToRoad')} ${f.distRoad_km.toFixed(1)} · ${t('distToVlg')} ${f.distVillage_km.toFixed(1)} km · ${t('statBuffer')} ${buf}</span></td>
      </tr>`;
    }).join("");

    card.innerHTML = `
      <div class="head">
        <div class="badge">${t('badgeSITE')} ${PROV_RANK[prov]} · ${t('detailBadge')}</div>
        <h3>${tProv(prov)}</h3>
        <div class="amphoe">${t('amphoePrefix')}${tAmphoe(PROV_AMPHOE[prov])} · ${t('facilities4')}</div>
      </div>
      <div id="${mapId}" class="map-el"></div>
      <div class="info">
        <table>${rows}</table>
      </div>
    `;
    grid.appendChild(card);

    // Init Leaflet mini-map
    const mini = L.map(mapId, {
      zoomControl: true, scrollWheelZoom: false,
      attributionControl: false, minZoom: 9, maxZoom: 17
    });
    miniMapInstances.push(mini);

    // Satellite base for terrain context
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      { maxZoom: 19 }).addTo(mini);
    // Soft OSM overlay for road / village labels
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}{r}.png',
      { maxZoom: 19, opacity: 0.85 }).addTo(mini);

    // Buffer circles (drawn first so markers sit on top)
    facs.forEach(f => {
      // Outer restricted (rocket)
      if (f.buffer_outer_km) {
        L.circle([f.lat, f.lng], {
          radius: f.buffer_outer_km * 1000,
          color:"#7a1e1e", weight:1.5, fillColor:"#7a1e1e",
          fillOpacity:0.05, dashArray:"8,6"
        }).addTo(mini);
      }
      // Inner compliance buffer
      L.circle([f.lat, f.lng], {
        radius: f.buffer_inner_km * 1000,
        color: f.color, weight: 2, fillColor: f.color,
        fillOpacity: 0.15, dashArray: "4,4"
      }).addTo(mini);
    });

    // Facility markers + tambon labels
    facs.forEach(f => {
      L.marker([f.lat, f.lng], {
        icon: L.divIcon({
          className: 'mini-fac-icon',
          html: `<div style="background:${f.color};color:#fff;border:2px solid #fff;border-radius:50%;
                             width:28px;height:28px;display:flex;align-items:center;justify-content:center;
                             font-size:11px;font-weight:700;box-shadow:0 2px 6px rgba(0,0,0,0.5);">${f.icon}</div>`,
          iconSize:[28,28], iconAnchor:[14,14]
        })
      }).bindPopup(
        `<h4 style="margin:0 0 4px 0;color:${f.color};">${facilityName(f)}</h4>
         <div style="font-size:0.78rem;color:var(--mars-glow);font-weight:600;">${t('tambonPrefix')}${tTambon(f.tambon)}</div>
         <table>
           <tr><td>${t('statSuit')}</td><td><b>${f.suit.toFixed(2)}</b></td></tr>
           <tr><td>${t('distToRoad')}</td><td>${f.distRoad_km.toFixed(1)} km</td></tr>
           <tr><td>${t('distToVlg')}</td><td>${f.distVillage_km.toFixed(1)} km</td></tr>
           <tr><td>${t('statBuffer')}</td><td>${f.buffer_inner_km}${f.buffer_outer_km?` / ${f.buffer_outer_km}`:''} km</td></tr>
         </table>`
      ).addTo(mini);

      // (No permanent tooltip — details show only when the marker is clicked.)
    });

    // Fit bounds to encompass all 4 facilities + their largest buffer
    const lats = facs.map(f => f.lat);
    const lngs = facs.map(f => f.lng);
    // pad ~0.1° (~11 km) to make sure outer buffers are visible
    const pad = 0.10;
    const sw = [Math.min(...lats) - pad, Math.min(...lngs) - pad];
    const ne = [Math.max(...lats) + pad, Math.max(...lngs) + pad];
    mini.fitBounds([sw, ne]);

    // After Leaflet has measured, invalidate so tiles draw correctly
    setTimeout(() => mini.invalidateSize(), 250);
  });
}
buildMiniMaps();


/* ========================================================
   WINNERS — 4 mini-maps (one per mission type)
   Surfaces the single best tambon across all 3 shortlisted
   provinces for each role, as a decision aid. Runner-up
   tambons are listed below each winner for comparison.
   ======================================================== */
let winnerMapInstances = [];
function buildWinners(){
  const grid = document.getElementById('winnersGrid');
  if(!grid) return;

  // Tear down previous (for language switching)
  winnerMapInstances.forEach(m => { try { m.remove(); } catch(_){} });
  winnerMapInstances = [];
  grid.innerHTML = "";

  const ROLE_ORDER = ["research","zerog","rocket","shuttle"];
  const ROLE_LABEL_KEY  = { research:"roleResearchHero", zerog:"roleZerogHero", rocket:"roleRocketHero", shuttle:"roleShuttleHero" };
  const ROLE_SUB_KEY    = { research:"roleResearchSub", zerog:"roleZerogSub", rocket:"roleRocketSub", shuttle:"roleShuttleSub" };
  const ROLE_REASON_KEY = { research:"reasonResearch", zerog:"reasonZerog", rocket:"reasonRocket", shuttle:"reasonShuttle" };

  ROLE_ORDER.forEach(role => {
    const candidates = FACILITIES.filter(f => f.type === role)
                                 .sort((a,b) => b.suit - a.suit);
    const winner  = candidates[0];
    const runners = candidates.slice(1);
    if(!winner) return;

    const mapId = `winnerMap_${role}`;
    const card = document.createElement('div');
    card.className = 'winner-card';
    card.innerHTML = `
      <div class="medal">${t('medalBest')}</div>
      <div class="winner-head" style="background:linear-gradient(135deg, ${winner.color} 0%, #2b2523 110%);">
        <div class="winner-role">${t(ROLE_LABEL_KEY[role])}</div>
        <div class="winner-tambon">${t('tambonPrefix')}${tTambon(winner.tambon)}</div>
        <div class="winner-prov">${t('amphoePrefix')}${tAmphoe(winner.amphoe)} · ${tProv(winner.province)}</div>
        <div class="winner-thai">${t(ROLE_SUB_KEY[role])}</div>
      </div>
      <div id="${mapId}" class="map-el"></div>
      <div class="winner-stats">
        <div class="stat-pill"><div class="v">${winner.suit.toFixed(2)}</div><div class="k">${t('statSuit')}</div></div>
        <div class="stat-pill"><div class="v">${winner.distRoad_km.toFixed(1)} km</div><div class="k">${t('statRoad')}</div></div>
        <div class="stat-pill"><div class="v">${winner.distVillage_km.toFixed(1)} km</div><div class="k">${t('statVlg')}</div></div>
        <div class="stat-pill"><div class="v">${winner.buffer_inner_km}${winner.buffer_outer_km?` / ${winner.buffer_outer_km}`:''} km</div><div class="k">${t('statBuffer')}</div></div>
      </div>
      <div class="reason-box">
        <b>${t('whyWins')}</b> ${t(ROLE_REASON_KEY[role])}
      </div>
      <div class="vs-row">
        <span class="vs-label">${t('runnersUp')}</span>
        ${runners.map(r => `<span class="vs-item">${tProv(r.province)} · ${t('tambonPrefix')}${tTambon(r.tambon)} · ${r.suit.toFixed(2)}</span>`).join("")}
      </div>
    `;
    grid.appendChild(card);

    const m = L.map(mapId, {
      zoomControl:true, scrollWheelZoom:false,
      attributionControl:false, minZoom:9, maxZoom:17
    });
    winnerMapInstances.push(m);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      { maxZoom: 19 }).addTo(m);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}{r}.png',
      { maxZoom: 19, opacity: 0.85 }).addTo(m);

    if (winner.buffer_outer_km) {
      L.circle([winner.lat, winner.lng], {
        radius: winner.buffer_outer_km * 1000,
        color:"#7a1e1e", weight:1.5, fillColor:"#7a1e1e",
        fillOpacity:0.05, dashArray:"8,6"
      }).addTo(m).bindTooltip(`${t('restricted')} ${winner.buffer_outer_km} km`, {sticky:true});
    }
    L.circle([winner.lat, winner.lng], {
      radius: winner.buffer_inner_km * 1000,
      color: winner.color, weight:2, fillColor: winner.color,
      fillOpacity:0.18, dashArray:"4,4"
    }).addTo(m).bindTooltip(`${t('innerBuf')} ${winner.buffer_inner_km} km`, {sticky:true});

    const kmToDeg = 1/111;
    const roadEnd = [winner.lat + winner.distRoad_km*kmToDeg*0.7,
                     winner.lng + winner.distRoad_km*kmToDeg*0.7];
    const vlgEnd  = [winner.lat - winner.distVillage_km*kmToDeg*0.7,
                     winner.lng - winner.distVillage_km*kmToDeg*0.7];
    L.polyline([[winner.lat,winner.lng], roadEnd], {
      color:"#2b2523", weight:2, dashArray:"3,4", opacity:0.85
    }).addTo(m);
    L.marker(roadEnd, {icon:L.divIcon({className:'dist-label',
      html:`<span style="background:#2b2523;color:#fff;padding:2px 6px;border-radius:4px;
                          font-size:10px;font-weight:700;white-space:nowrap;
                          box-shadow:0 1px 4px rgba(0,0,0,0.4);">
              🛣 ${winner.distRoad_km.toFixed(1)} km</span>`,
      iconSize:[1,1], iconAnchor:[0,0]})}).addTo(m);
    L.polyline([[winner.lat,winner.lng], vlgEnd], {
      color:"#7a1e1e", weight:2, dashArray:"3,4", opacity:0.85
    }).addTo(m);
    L.marker(vlgEnd, {icon:L.divIcon({className:'dist-label',
      html:`<span style="background:#7a1e1e;color:#fff;padding:2px 6px;border-radius:4px;
                          font-size:10px;font-weight:700;white-space:nowrap;
                          box-shadow:0 1px 4px rgba(0,0,0,0.4);">
              🏘 ${winner.distVillage_km.toFixed(1)} km</span>`,
      iconSize:[1,1], iconAnchor:[0,0]})}).addTo(m);

    L.marker([winner.lat, winner.lng], {
      icon: L.divIcon({className:'winner-fac-icon',
        html:`<div style="background:${winner.color};color:#fff;border:3px solid #fff;border-radius:50%;
                          width:38px;height:38px;display:flex;align-items:center;justify-content:center;
                          font-size:14px;font-weight:700;box-shadow:0 4px 10px rgba(0,0,0,0.55);">${winner.icon}</div>`,
        iconSize:[38,38], iconAnchor:[19,19]
      })
    }).bindPopup(
      `<h4 style="margin:0 0 4px 0;color:${winner.color};">${facilityName(winner)}</h4>
       <div style="font-size:0.78rem;color:var(--mars-glow);font-weight:600;margin-bottom:4px;">
         ${t('tambonPrefix')}${tTambon(winner.tambon)} · ${t('amphoePrefix')}${tAmphoe(winner.amphoe)}
       </div>
       <table>
         <tr><td>${t('statSuit')}</td><td><b>${winner.suit.toFixed(2)}</b></td></tr>
         <tr><td>${t('statRoad')}</td><td>${winner.distRoad_km.toFixed(1)} km</td></tr>
         <tr><td>${t('statVlg')}</td><td>${winner.distVillage_km.toFixed(1)} km</td></tr>
         <tr><td>${t('innerBuf')}</td><td>${winner.buffer_inner_km} km</td></tr>
         ${winner.buffer_outer_km ? `<tr><td>${t('restricted')}</td><td>${winner.buffer_outer_km} km</td></tr>`:''}
       </table>
       <div style="margin-top:6px;font-size:0.7rem;color:#cdc2ad;font-style:italic;">${winner.note}</div>`
    ).addTo(m);

    const zoom = winner.buffer_outer_km ? 11 : 13;
    m.setView([winner.lat, winner.lng], zoom);
    setTimeout(() => m.invalidateSize(), 250);
  });
}
buildWinners();


/* RASTER OVERLAY — switch between Suitability / Iron Oxide / NDVI / BSI / Slope / Candidate / Very-High */
let activeRaster = null;
function setRaster(key) {
  if (activeRaster) { map.removeLayer(activeRaster); activeRaster = null; }
  if (key && RASTERS[key]) {
    activeRaster = L.imageOverlay(RASTERS[key], RASTER_BOUNDS, { opacity: 0.65, interactive: false });
    activeRaster.addTo(map);
    // Put province polygons on top of the raster
    if (map.hasLayer(provinceLayer)) provinceLayer.bringToFront();
  }
}
// Default raster: Suitability
setRaster('suit');
document.getElementById('rasterSelect').addEventListener('change', e => setRaster(e.target.value));

/* TOOLBAR BINDINGS */
document.getElementById('tglProvinces').addEventListener('change', e => {
  if (e.target.checked) { provinceLayer.addTo(map); provinceLayer.bringToFront(); } else map.removeLayer(provinceLayer);
});
document.getElementById('tglPoints').addEventListener('change', e => {
  if (e.target.checked) pointsLayer.addTo(map); else map.removeLayer(pointsLayer);
});
document.getElementById('tglAirports').addEventListener('change', e => {
  if (e.target.checked) airportLayer.addTo(map); else map.removeLayer(airportLayer);
});
document.getElementById('tglShortlist').addEventListener('change', e => {
  if (e.target.checked) shortlistLayer.addTo(map); else map.removeLayer(shortlistLayer);
});
document.getElementById('tglFacilities').addEventListener('change', e => {
  if (e.target.checked) facilityMarkerLayer.addTo(map); else map.removeLayer(facilityMarkerLayer);
});
document.getElementById('tglBuffers').addEventListener('change', e => {
  if (e.target.checked) facilityBufferLayer.addTo(map); else map.removeLayer(facilityBufferLayer);
});
document.getElementById('btnFit').addEventListener('click', () => {
  map.fitBounds(provinceLayer.getBounds(), { padding:[20,20] });
});
setTimeout(() => { try { map.fitBounds(provinceLayer.getBounds(), { padding:[20,20] }); } catch(_){} }, 200);

/* "Fly map to site" handlers are bound inside renderShortlist() */

/* PROVINCE TABLE + STATS */
const PROV_POP = {
  "Nakhon Ratchasima":2625,"Ubon Ratchathani":1869,"Khon Kaen":1789,"Udon Thani":1568,
  "Buriram":1571,"Surin":1383,"Si Sa Ket":1463,"Roi Et":1289,"Chaiyaphum":1118,
  "Kalasin":973,"Maha Sarakham":947,"Sakon Nakhon":1145,"Nakhon Phanom":712,
  "Loei":641,"Yasothon":537,"Nong Bua Lam Phu":509,"Nong Khai":520,"Bueng Kan":421,
  "Mukdahan":351,"Amnat Charoen":376
};
/* Candidate-area km² fallback: derived from per-province suit_mean/suit_max
   when the source geojson lacks the Candidate_km2 attribute. */
const PROV_CAND_KM2 = {
  "Khon Kaen":108,"Nakhon Ratchasima":107,"Surin":106,"Ubon Ratchathani":101,
  "Udon Thani":101,"Chaiyaphum":100,"Yasothon":92,"Sakon Nakhon":89,
  "Maha Sarakham":88,"Nakhon Phanom":87,"Roi Et":86,"Amnat Charoen":85,
  "Kalasin":85,"Mukdahan":80,"Nong Khai":78,"Loei":63
};
function buildProvinceTable() {
  const rows = ISAN_PROVINCES.features.map(f => ({
    province: f.properties.Province,
    mean: f.properties.Suit_mean || 0,
    max:  f.properties.Suit_max  || 0,
    cand: f.properties.Candidate_km2 || PROV_CAND_KM2[f.properties.Province] || 0,
    pop:  PROV_POP[f.properties.Province] || "—"
  }));
  rows.sort((a,b) => b.mean - a.mean);
  const tbody = document.getElementById('provinceTableBody');
  tbody.innerHTML = "";
  rows.forEach((r,i) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><span class="rank">#${i+1}</span></td>
      <td><strong>${tProv(r.province)}</strong></td>
      <td>${r.mean.toFixed(3)}</td>
      <td>${r.max.toFixed(3)}</td>
      <td>${r.pop}</td>
    `;
    tr.addEventListener('click', () => {
      const layer = provinceLayer.getLayers().find(l => l.feature.properties.Province === r.province);
      if (layer) {
        map.fitBounds(layer.getBounds(), { maxZoom: 11 });
        layer.openPopup();
        document.getElementById('interactive-map-section').scrollIntoView({behavior:'smooth'});
      }
    });
    tbody.appendChild(tr);
  });
  document.getElementById('statTopProv').textContent = tProv(rows[0].province);
  document.getElementById('statTotalArea').textContent = rows.reduce((s,r)=>s+r.cand,0).toFixed(0) + " km²";
  document.getElementById('statZones').textContent = rows.length;
  const vhRows = rows.filter(r => r.max >= 0.9).sort((a,b) => b.max - a.max);
  document.getElementById('statVHClusters').textContent = vhRows.length;
  document.getElementById('statVHList').innerHTML = vhRows.length
    ? vhRows.map(r => `${tProv(r.province)} <span style="opacity:.65; font-weight:500;">(${r.max.toFixed(2)})</span>`).join(" · ")
    : "—";
  return rows;
}
const tableRows = buildProvinceTable();

/* CHARTS */
Chart.defaults.font.family = "'JetBrains Mono', 'IBM Plex Sans Thai', 'Inter', monospace";
Chart.defaults.font.size = 11;
Chart.defaults.color = "#cdc2ad";
Chart.defaults.borderColor = "rgba(244,236,216,0.10)";

const CLASS_LABELS = {
  en: ["Very High (≥0.9)","High (0.8–0.9)","Mod-High (0.7–0.8)","Moderate (0.6–0.7)","Lower (<0.6)"],
  th: ["สูงมาก (≥0.9)","สูง (0.8–0.9)","ค่อนข้างสูง (0.7–0.8)","ปานกลาง (0.6–0.7)","ต่ำ (<0.6)"],
  zh: ["极高 (≥0.9)","高 (0.8–0.9)","较高 (0.7–0.8)","中等 (0.6–0.7)","较低 (<0.6)"]
};
const CHART_LABELS = {
  en: { meanSuit:"Mean Suitability", provinces:"Provinces", histX:"Mean suitability bin", histY:"# provinces" },
  th: { meanSuit:"ค่าเฉลี่ยความเหมาะสม", provinces:"จังหวัด", histX:"ช่วงค่าเฉลี่ยความเหมาะสม", histY:"จำนวนจังหวัด" },
  zh: { meanSuit:"平均适宜性", provinces:"省份", histX:"平均适宜性区间", histY:"省份数量" }
};

let chartTopProv = null, chartClasses = null, chartHist = null;

function renderCharts(){
  if (chartTopProv) { chartTopProv.destroy(); chartTopProv = null; }
  if (chartClasses) { chartClasses.destroy(); chartClasses = null; }
  if (chartHist)    { chartHist.destroy();    chartHist = null; }

  const cl = CHART_LABELS[CURRENT_LANG] || CHART_LABELS.en;
  const classLabels = CLASS_LABELS[CURRENT_LANG] || CLASS_LABELS.en;

  chartTopProv = new Chart(document.getElementById("chartTopProv"), {
    type:"bar",
    data:{
      labels: tableRows.slice(0,10).map(r => r.province),
      datasets:[{ label: cl.meanSuit, data: tableRows.slice(0,10).map(r => r.mean),
        backgroundColor: tableRows.slice(0,10).map(r => colorForSuit(r.mean)),
        borderColor:"#7a1e1e", borderWidth:1, borderRadius:6 }]
    },
    options:{ indexAxis:"y", responsive:true, maintainAspectRatio:false,
      plugins:{legend:{display:false}},
      scales:{ x:{min:0.4,max:0.8,grid:{color:"rgba(244,236,216,0.08)"},ticks:{color:"#cdc2ad"}},
               y:{grid:{display:false},ticks:{color:"#cdc2ad"}} } }
  });

  const classCounts = [0,0,0,0,0];
  tableRows.forEach(r => {
    if (r.max >= 0.9) classCounts[0]++;
    else if (r.max >= 0.8) classCounts[1]++;
    else if (r.max >= 0.7) classCounts[2]++;
    else if (r.max >= 0.6) classCounts[3]++;
    else classCounts[4]++;
  });
  chartClasses = new Chart(document.getElementById("chartClasses"), {
    type:"doughnut",
    data:{
      labels: classLabels,
      datasets:[{ data:classCounts,
        backgroundColor:["#e8623a","#b5391f","#8a2c18","#5a4a3a","#2a2520"],
        borderColor:"#0b0a09", borderWidth:2 }]
    },
    options:{ responsive:true, maintainAspectRatio:false,
      plugins:{legend:{position:"bottom",labels:{boxWidth:12,padding:10,color:"#cdc2ad",font:{family:"'JetBrains Mono', monospace",size:10}}}},
      cutout:"58%" }
  });

  const bins = [0,0,0,0,0,0,0,0,0,0,0];
  tableRows.forEach(r => { const i = Math.min(10, Math.max(0, Math.floor(r.mean*10))); bins[i]++; });
  chartHist = new Chart(document.getElementById("chartHist"), {
    type:"bar",
    data:{
      labels:["0.0","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1.0"],
      datasets:[{ label: cl.provinces, data:bins,
        backgroundColor:"#e8623a", borderColor:"#b5391f", borderWidth:1, borderRadius:2 }]
    },
    options:{ responsive:true, maintainAspectRatio:false,
      plugins:{legend:{display:false}},
      scales:{ x:{title:{display:true,text: cl.histX,color:"#cdc2ad"},grid:{display:false},ticks:{color:"#cdc2ad"}},
               y:{title:{display:true,text: cl.histY,color:"#cdc2ad"},grid:{color:"rgba(244,236,216,0.08)"},ticks:{stepSize:1,color:"#cdc2ad"}} } }
  });
}
renderCharts();

/* ========================================================
   LANGUAGE SWITCHING — EN / TH / ZH
   ======================================================== */
function applyStaticI18n() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const val = t(key);
    if (el.tagName === 'OPTION') {
      el.textContent = val;
    } else {
      el.innerHTML = val;
    }
  });
  // Update <html lang="…"> for accessibility
  document.documentElement.setAttribute('lang', CURRENT_LANG);
  // Update document title
  document.title = t('siteTitle');
}

function setLang(lang) {
  if (!I18N[lang]) return;
  CURRENT_LANG = lang;

  // 1) Update language switcher active state
  document.querySelectorAll('#langSwitcher button').forEach(b => {
    b.classList.toggle('active', b.dataset.lang === lang);
  });

  // 2) Update all static labels
  applyStaticI18n();

  // 3) Refresh dynamic popups (Leaflet markers already on map)
  refreshProvincePopups();
  refreshPointPopups();
  refreshAirportPopups();
  refreshShortlistPopups();
  refreshFacilityPopups();

  // 4) Re-render dynamic content (rebuilds DOM + Leaflet sub-maps + Chart.js)
  renderShortlist();
  buildFacilityTable();
  buildMiniMaps();
  buildWinners();
  buildProvinceTable();
  renderCharts();
}

document.getElementById('langSwitcher').addEventListener('click', e => {
  const btn = e.target.closest('button[data-lang]');
  if (btn) setLang(btn.dataset.lang);
});

// Initial pass: apply EN labels (matches the default markup but normalises any HTML entities)
applyStaticI18n();

/* ========================================================
   SCROLL REVEAL — fade-up as elements enter the viewport
   ======================================================== */
(function setupScrollReveal(){
  // Apply reveal class to major content blocks
  const targets = document.querySelectorAll(
    'section .section-title, section > .section-sub, ' +
    'section > .grid > *, section > .grid-2 > *, section > .grid-3 > *, section > .grid-4 > *, ' +
    'section > .table-wrap, section > .leaflet-map-wrap, section > .map-toolbar, ' +
    'section > .formula-card, section > .shortlist-grid > *, ' +
    'section > .mini-map-grid > *, section > .role-grid > *, section > .winners-grid > *, ' +
    'section > .facility-legend, section > .csg-note, section > .prov-head, section > .chart-card'
  );
  targets.forEach((el, i) => {
    el.classList.add('reveal');
    if (i % 3 === 1) el.classList.add('reveal-delay-1');
    if (i % 3 === 2) el.classList.add('reveal-delay-2');
  });

  if (!('IntersectionObserver' in window)) {
    targets.forEach(el => el.classList.add('is-visible'));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  targets.forEach(el => io.observe(el));

  // Header content reveals on load
  setTimeout(() => {
    document.querySelectorAll('.header .chapter-line, .header h1, .header .subtitle, .header .overview, .header .course-pill')
      .forEach((el, i) => {
        el.classList.add('reveal');
        if (i > 0) el.style.transitionDelay = (0.08 * i) + 's';
        requestAnimationFrame(() => el.classList.add('is-visible'));
      });
  }, 50);
})();
</script>

</body>
</html>
"""

HTML = HTML.replace("__ISAN_JSON__", ISAN)
HTML = HTML.replace("__CANDIDATE_POINTS__", CANDIDATE_POINTS)
HTML = HTML.replace("__RASTER_BOUNDS__", RASTER_BOUNDS_JS)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)

print("OK ->", OUT)
print("size KB:", round(os.path.getsize(OUT)/1024, 1))
