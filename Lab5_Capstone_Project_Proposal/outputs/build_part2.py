#!/usr/bin/env python3
"""Part 2: HEADER + INTRO + INTERACTIVE MAP section HTML"""

PART2 = r"""
<!-- HEADER -->
<header class="header">
  <div class="header-inner">
    <span class="course-pill">GE.338 &middot; Geographic Data Science</span>
    <h1>
      <span data-i18n-en>Mars Analog Site Suitability in Northeastern Thailand</span>
      <span data-i18n-th>การหาพื้นที่ที่คล้ายดาวอังคารในภาคตะวันออกเฉียงเหนือของประเทศไทย</span>
    </h1>
    <div class="subtitle">
      <span data-i18n-en>A multi-criteria remote sensing study using Landsat 8, NASADEM, and ESA WorldCover.</span>
      <span data-i18n-th>การศึกษาเชิงรีโมตเซนซิงแบบหลายเกณฑ์ โดยใช้ Landsat 8, NASADEM และ ESA WorldCover</span>
    </div>
    <p class="overview">
      <span data-i18n-en>This dashboard presents the Mars analog suitability analysis over the Isan region. By combining spectral indices (Iron Oxide, NDVI, BSI) with topographic slope and land cover masks, the analysis highlights arid, iron-rich, low-vegetation landscapes with potential as terrestrial analogs for Martian surface studies. Explore the interactive map below — zoom down to the tambon (sub-district) level.</span>
      <span data-i18n-th>แดชบอร์ดนี้นำเสนอการวิเคราะห์ความเหมาะสมของพื้นที่ที่คล้ายดาวอังคารในภาคอีสาน โดยใช้ดัชนีเชิงสเปกตรัม (Iron Oxide, NDVI, BSI) ร่วมกับความลาดชันและชั้นข้อมูลสิ่งปกคลุมดิน เพื่อคัดเลือกพื้นที่ที่แห้งแล้ง มีธาตุเหล็กสูง และพืชพรรณเบาบาง ซึ่งเหมาะเป็นพื้นที่จำลองดาวอังคารบนโลก สำรวจแผนที่แบบโต้ตอบด้านล่าง — สามารถซูมถึงระดับตำบลได้</span>
    </p>
  </div>
</header>

<main class="container">

  <!-- INTERACTIVE LEAFLET MAP -->
  <section id="interactive-map-section">
    <div class="section-title"><span class="num">★</span>
      <h2>
        <span data-i18n-en>Interactive Suitability Map — Isan</span>
        <span data-i18n-th>แผนที่ความเหมาะสมแบบโต้ตอบ — ภาคอีสาน</span>
      </h2>
    </div>
    <p class="section-sub">
      <span data-i18n-en>Colored provinces show <b>mean Mars-analog suitability</b>. Click any province for its statistics. Toggle raster overlays (Suitability, Iron Oxide, NDVI, BSI, Slope, Candidate Sites, Very-High Sites). Zoom supports up to level 18 — tambon (sub-district) scale.</span>
      <span data-i18n-th>จังหวัดถูกลงสีตามค่า<b>ความเหมาะสมเฉลี่ย</b> คลิกจังหวัดเพื่อดูสถิติ เปิด/ปิดชั้นข้อมูล (Suitability, Iron Oxide, NDVI, BSI, Slope, พื้นที่เสนอ, พื้นที่เหมาะสมสูงมาก) ซูมได้ถึงระดับ 18 — ระดับตำบล</span>
    </p>

    <div class="zoom-hint">
      🛰️
      <span data-i18n-en><b>Zoom down to tambon level</b> — scroll or use the ＋ control. Satellite basemap supports zoom level 18.</span>
      <span data-i18n-th><b>ซูมได้ถึงระดับตำบล</b> — เลื่อนเมาส์หรือกดปุ่ม ＋ แผนที่ดาวเทียมรองรับ zoom level 18</span>
    </div>

    <div class="map-toolbar">
      <label><input type="checkbox" id="tglProvinces" checked>
        <span data-i18n-en>Provinces (Choropleth)</span>
        <span data-i18n-th>ขอบเขตจังหวัด (Choropleth)</span>
      </label>
      <label><input type="checkbox" id="tglSuitability">
        <span data-i18n-en>Suitability Raster</span>
        <span data-i18n-th>แผนที่ความเหมาะสม (Raster)</span>
      </label>
      <label><input type="checkbox" id="tglIronOxide">
        <span data-i18n-en>Iron Oxide</span>
        <span data-i18n-th>ธาตุเหล็กออกไซด์</span>
      </label>
      <label><input type="checkbox" id="tglNDVI">
        <span data-i18n-en>NDVI</span>
        <span data-i18n-th>NDVI</span>
      </label>
      <label><input type="checkbox" id="tglBSI">
        <span data-i18n-en>BSI</span>
        <span data-i18n-th>BSI</span>
      </label>
      <label><input type="checkbox" id="tglSlope">
        <span data-i18n-en>Slope</span>
        <span data-i18n-th>ความลาดชัน</span>
      </label>
      <label><input type="checkbox" id="tglCandidates" checked>
        <span data-i18n-en>Candidate Sites</span>
        <span data-i18n-th>พื้นที่เสนอ</span>
      </label>
      <label><input type="checkbox" id="tglVeryHigh" checked>
        <span data-i18n-en>Very-High Suitability</span>
        <span data-i18n-th>เหมาะสมสูงมาก</span>
      </label>
      <label style="margin-left:auto;">
        <span data-i18n-en>Basemap:</span>
        <span data-i18n-th>แผนที่ฐาน:</span>
        <select id="basemapSelect">
          <option value="satellite" data-en="Satellite (ESRI)" data-th="ดาวเทียม (ESRI)">Satellite (ESRI)</option>
          <option value="osm" data-en="OpenStreetMap" data-th="OpenStreetMap">OpenStreetMap</option>
          <option value="terrain" data-en="Terrain (OpenTopo)" data-th="ภูมิประเทศ (OpenTopo)">Terrain (OpenTopo)</option>
          <option value="dark" data-en="Dark (Carto)" data-th="มืด (Carto)">Dark (Carto)</option>
        </select>
      </label>
      <button id="btnFit">
        <span data-i18n-en>Fit to Isan</span>
        <span data-i18n-th>จัดเต็มอีสาน</span>
      </button>
    </div>

    <div class="leaflet-map-wrap">
      <div id="isanMap"></div>
      <div class="map-legend" id="mapLegend">
        <h4>
          <span data-i18n-en>Mean Suitability</span>
          <span data-i18n-th>ความเหมาะสมเฉลี่ย</span>
        </h4>
        <div class="row"><span class="sw" style="background:#7a1e1e"></span>
          <span data-i18n-en>0.70 – 0.75 Very High</span>
          <span data-i18n-th>0.70 – 0.75 สูงมาก</span>
        </div>
        <div class="row"><span class="sw" style="background:#b5502c"></span>
          <span data-i18n-en>0.65 – 0.70 High</span>
          <span data-i18n-th>0.65 – 0.70 สูง</span>
        </div>
        <div class="row"><span class="sw" style="background:#d07a4c"></span>
          <span data-i18n-en>0.60 – 0.65 Mod-High</span>
          <span data-i18n-th>0.60 – 0.65 ค่อนข้างสูง</span>
        </div>
        <div class="row"><span class="sw" style="background:#e9b888"></span>
          <span data-i18n-en>0.55 – 0.60 Moderate</span>
          <span data-i18n-th>0.55 – 0.60 ปานกลาง</span>
        </div>
        <div class="row"><span class="sw" style="background:#f6ecdb"></span>
          <span data-i18n-en>&lt; 0.55 Lower</span>
          <span data-i18n-th>&lt; 0.55 ต่ำ</span>
        </div>
        <hr style="border:none; border-top:1px solid var(--mars-border); margin:8px 0;">
        <div class="row"><span class="sw" style="background:#ff2d2d; border-radius:50%; width:10px; height:10px;"></span>
          <span data-i18n-en>Very High Site</span>
          <span data-i18n-th>จุดเหมาะสมสูงมาก</span>
        </div>
        <div class="row"><span class="sw" style="background:#ffb000; border-radius:50%; width:10px; height:10px;"></span>
          <span data-i18n-en>Candidate Site</span>
          <span data-i18n-th>จุดเสนอ</span>
        </div>
      </div>
    </div>
  </section>
"""

out = "/sessions/intelligent-youthful-babbage/part2.html"
with open(out,"w",encoding="utf-8") as f:
    f.write(PART2)
print("OK", len(PART2), "chars")
