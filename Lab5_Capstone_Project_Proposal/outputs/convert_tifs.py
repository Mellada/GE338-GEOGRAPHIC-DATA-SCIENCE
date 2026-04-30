#!/usr/bin/env python3
"""Convert each Isan GeoTIFF into a colorized PNG (and a smaller display version)
that matches the same WGS84 bounds. Also computes the dataset bounds for use as
a Leaflet imageOverlay.
"""
import os, json
import numpy as np
import imageio.v3 as iio
from PIL import Image

UPLOADS = "/sessions/intelligent-youthful-babbage/mnt/uploads"
OUT_DIR = "/sessions/intelligent-youthful-babbage/mnt/outputs/images"
os.makedirs(OUT_DIR, exist_ok=True)

# Georeferencing (read from GeoTIFF tags) — same for every layer
ORIGIN_LON = 100.83549257163781   # top-left lon
ORIGIN_LAT = 18.44909983682905    # top-left lat
PX = 0.0010779783409434257        # degrees / pixel

# ---------- Colormaps (linear interpolation between stops) ----------
def lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i]-c1[i])*t) for i in range(3))

def make_cmap(stops):
    """stops = list of (pos, (r,g,b)). Returns 256-entry LUT."""
    lut = np.zeros((256,3), dtype=np.uint8)
    n = len(stops)
    for i in range(256):
        t = i/255.0
        for k in range(n-1):
            p0, c0 = stops[k]; p1, c1 = stops[k+1]
            if p0 <= t <= p1:
                tt = (t - p0)/(p1 - p0) if p1>p0 else 0
                lut[i] = lerp(c0, c1, tt)
                break
    return lut

# Mars / dashboard palette
CMAP_IRON = make_cmap([(0.0,(246,236,219)),(0.5,(208,122,76)),(0.85,(181,80,44)),(1.0,(122,30,30))])
CMAP_SUIT = make_cmap([(0.0,(246,236,219)),(0.45,(233,184,136)),(0.6,(208,122,76)),(0.8,(181,80,44)),(1.0,(122,30,30))])
CMAP_NDVI = make_cmap([(0.0,(233,214,184)),(0.35,(168,191,136)),(0.7,(106,140,90)),(1.0,(56,90,43))])
CMAP_BSI  = make_cmap([(0.0,(246,236,219)),(0.5,(201,162,106)),(1.0,(122,69,32))])
CMAP_SLOPE= make_cmap([(0.0,(246,236,219)),(0.5,(201,162,106)),(0.85,(122,69,32)),(1.0,(74,48,32))])

def colorize(arr, cmap, vmin=None, vmax=None, mask_zero=False):
    """Return RGBA uint8 image. NaN -> transparent. Optional 0 -> transparent."""
    arr = np.asarray(arr, dtype=np.float32)
    valid = np.isfinite(arr)
    if mask_zero:
        valid &= (arr != 0)
    if vmin is None: vmin = np.nanpercentile(arr[valid], 2) if valid.any() else 0
    if vmax is None: vmax = np.nanpercentile(arr[valid], 98) if valid.any() else 1
    if vmax <= vmin: vmax = vmin + 1e-9
    norm = (arr - vmin) / (vmax - vmin)
    norm = np.clip(norm, 0, 1)
    idx = (norm * 255).astype(np.uint8)
    rgb = cmap[idx]                            # (H,W,3)
    alpha = (valid * 255).astype(np.uint8)     # transparent where invalid
    rgba = np.dstack([rgb, alpha])
    return rgba, float(vmin), float(vmax)

def colorize_binary(arr, color):
    """0/1 raster -> transparent / colored RGBA."""
    arr = np.asarray(arr)
    rgba = np.zeros(arr.shape + (4,), dtype=np.uint8)
    sel = (arr > 0)
    rgba[sel,0] = color[0]; rgba[sel,1] = color[1]; rgba[sel,2] = color[2]; rgba[sel,3] = 230
    return rgba

def downsample(rgba, factor):
    if factor <= 1: return rgba
    h, w = rgba.shape[:2]
    img = Image.fromarray(rgba, "RGBA")
    new_w, new_h = w//factor, h//factor
    img = img.resize((new_w, new_h), Image.LANCZOS)
    return np.array(img)

def save_png(rgba, path, factor=4):
    rgba = downsample(rgba, factor)
    Image.fromarray(rgba, "RGBA").save(path, optimize=True, compress_level=9)
    print(f"  saved {os.path.basename(path)}  size={rgba.shape}  KB={os.path.getsize(path)//1024}")

# ---------- Process each TIF ----------
specs = [
    ("01_Isan_IronOxide.tif",          "01_Isan_IronOxide.png",     "iron",   CMAP_IRON,  None,  None,  False),
    ("01_Isan_NDVI.tif",               "01_Isan_NDVI.png",          "ndvi",   CMAP_NDVI,  -0.1,  0.9,   False),
    ("01_Isan_BSI.tif",                "01_Isan_BSI.png",           "bsi",    CMAP_BSI,   None,  None,  False),
    ("01_Isan_Slope.tif",              "01_Isan_Slope.png",         "slope",  CMAP_SLOPE, 0.0,   25.0,  False),
    ("02_Isan_Suitability.tif",        "02_Isan_Suitability.png",   "suit",   CMAP_SUIT,  0.4,   1.0,   True),
]

stats = {}
suitability_arr = None
for src, dst, key, cmap, vmin, vmax, mask_zero in specs:
    print(src)
    arr = iio.imread(os.path.join(UPLOADS, src))
    rgba, lo, hi = colorize(arr, cmap, vmin=vmin, vmax=vmax, mask_zero=mask_zero)
    save_png(rgba, os.path.join(OUT_DIR, dst), factor=4)
    stats[key] = {"min":lo, "max":hi, "shape":list(arr.shape)}
    if key == "suit":
        suitability_arr = arr  # keep for sampling

# Binary rasters
print("02_Isan_CandidateSites.tif")
cand = iio.imread(os.path.join(UPLOADS, "02_Isan_CandidateSites.tif"))
save_png(colorize_binary(cand, (255,176,0)), os.path.join(OUT_DIR, "02_Isan_CandidateSites.png"), factor=4)

print("02_Isan_VeryHighSuitability.tif")
vh = iio.imread(os.path.join(UPLOADS, "02_Isan_VeryHighSuitability.tif"))
save_png(colorize_binary(vh, (255,45,45)), os.path.join(OUT_DIR, "02_Isan_VeryHighSuitability.png"), factor=4)

# Bounds for Leaflet imageOverlay
H, W = suitability_arr.shape
bounds = {
    "north": ORIGIN_LAT,
    "west":  ORIGIN_LON,
    "south": ORIGIN_LAT - H*PX,
    "east":  ORIGIN_LON + W*PX,
    "px": PX
}
print("Bounds:", bounds)

# ---------- Sample real candidate points per province from suitability raster ----------
# Load province GeoJSON
GEOJSON = "/sessions/intelligent-youthful-babbage/provinces_tiny.geojson"
with open(GEOJSON, "r", encoding="utf-8") as f:
    gj = json.load(f)

def point_in_ring(x, y, ring):
    inside = False
    j = len(ring)-1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi):
            inside = not inside
        j = i
    return inside

def point_in_polygon(x, y, polygon_coords):
    """polygon_coords = list of rings (first = outer)"""
    if not polygon_coords: return False
    if not point_in_ring(x, y, polygon_coords[0]): return False
    for hole in polygon_coords[1:]:
        if point_in_ring(x, y, hole): return False
    return True

def feature_polygons(feat):
    g = feat["geometry"]
    if g["type"] == "Polygon":
        return [g["coordinates"]]
    elif g["type"] == "MultiPolygon":
        return g["coordinates"]
    return []

def feature_bbox(feat):
    polys = feature_polygons(feat)
    xs, ys = [], []
    for poly in polys:
        for ring in poly:
            for pt in ring:
                xs.append(pt[0]); ys.append(pt[1])
    return min(xs), min(ys), max(xs), max(ys)

def lonlat_to_pixel(lon, lat):
    col = int((lon - ORIGIN_LON) / PX)
    row = int((ORIGIN_LAT - lat) / PX)
    return row, col

def pixel_to_lonlat(row, col):
    return ORIGIN_LON + (col+0.5)*PX, ORIGIN_LAT - (row+0.5)*PX

# Sample candidates per province
candidate_points = []  # list of {province, lat, lng, suit, rank}
N_PER_PROV = 12        # how many candidate points per province

H, W = suitability_arr.shape
for feat in gj["features"]:
    province = feat["properties"]["Province"]
    polys = feature_polygons(feat)
    if not polys: continue
    minx, miny, maxx, maxy = feature_bbox(feat)
    # Pixel bbox
    r_top    = max(0, int((ORIGIN_LAT - maxy) / PX))
    r_bot    = min(H-1, int((ORIGIN_LAT - miny) / PX))
    c_left   = max(0, int((minx - ORIGIN_LON) / PX))
    c_right  = min(W-1, int((maxx - ORIGIN_LON) / PX))
    if r_bot <= r_top or c_right <= c_left: continue

    # Stride to keep computation cheap: ~10000 sample candidates
    region = suitability_arr[r_top:r_bot+1, c_left:c_right+1]
    rh, rw = region.shape
    stride_r = max(1, rh // 100)
    stride_c = max(1, rw // 100)

    pts = []  # (suit, lat, lng)
    for rr in range(0, rh, stride_r):
        for cc in range(0, rw, stride_c):
            v = region[rr, cc]
            if not np.isfinite(v) or v <= 0: continue
            row = r_top + rr; col = c_left + cc
            lon, lat = pixel_to_lonlat(row, col)
            # Check polygon membership
            inside = False
            for poly in polys:
                if point_in_polygon(lon, lat, poly):
                    inside = True; break
            if not inside: continue
            pts.append((float(v), lat, lon))

    if not pts: continue
    # Sort by suit descending
    pts.sort(key=lambda x: -x[0])
    # Spatial thinning to spread points: greedy with min distance ~0.05° (≈5 km)
    MIN_DEG = 0.06
    chosen = []
    for v, lat, lng in pts:
        ok = True
        for cv, clat, clng in chosen:
            if abs(lat - clat) < MIN_DEG and abs(lng - clng) < MIN_DEG:
                ok = False; break
        if ok:
            chosen.append((v, lat, lng))
        if len(chosen) >= N_PER_PROV: break

    for rank, (v, lat, lng) in enumerate(chosen, start=1):
        candidate_points.append({
            "province": province,
            "lat": round(lat, 4),
            "lng": round(lng, 4),
            "suit": round(v, 3),
            "rank": rank
        })
    print(f"  {province}: {len(chosen)} points (max suit {chosen[0][0]:.3f})")

# Save outputs
with open("/sessions/intelligent-youthful-babbage/raster_meta.json", "w") as f:
    json.dump({"bounds": bounds, "stats": stats}, f, indent=2)

with open("/sessions/intelligent-youthful-babbage/candidate_points.json", "w") as f:
    json.dump(candidate_points, f, separators=(",", ":"))

print(f"\nTotal candidate points: {len(candidate_points)}")
print("DONE.")
