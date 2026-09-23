import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOGO_PATH = ROOT / "SMJaleel Logo and Tagline_FAW_2.svg"
OUT_PATH = ROOT / "fleet-dashboard.html"
ROADS_PATH = ROOT / "roads_4326.geojson"

# SimpleMaps Barbados country boundary, WGS84, CC BY 4.0.
BARBADOS_BOUNDARY = [
    [-59.426909968852904, 13.160386589200625],
    [-59.43004309534556, 13.125921903135804],
    [-59.45571855984968, 13.100043121825795],
    [-59.47577877724313, 13.086493263943751],
    [-59.48753821676761, 13.078558686975065],
    [-59.50885983495788, 13.057318499976091],
    [-59.516713027879256, 13.056382669971066],
    [-59.523101355892514, 13.056463785252348],
    [-59.529286261313594, 13.055405981899861],
    [-59.536122196376056, 13.051174167653413],
    [-59.545969201138675, 13.06769434625819],
    [-59.56444250825684, 13.07802963506683],
    [-59.58690344635365, 13.08319727953415],
    [-59.60024979749031, 13.084133109578525],
    [-59.60814368294176, 13.084662161491861],
    [-59.621571417644944, 13.09398020480346],
    [-59.63312741480577, 13.115912276404366],
    [-59.64606686988558, 13.160386589200625],
    [-59.65420487523193, 13.295111297864155],
    [-59.65221106085918, 13.310614236993825],
    [-59.64513098373112, 13.323716463575346],
    [-59.63093015147467, 13.337958210481858],
    [-59.612863736679344, 13.344549881711671],
    [-59.594471805582415, 13.334784198087766],
    [-59.58071856205332, 13.314520690512628],
    [-59.575917124327766, 13.304388786782575],
    [-59.56895910883352, 13.28965884670589],
    [-59.54979408366389, 13.2491723931133],
    [-59.53661048268799, 13.231390716424144],
    [-59.5180558017038, 13.217515493137917],
    [-59.491810686029545, 13.19794357268718],
    [-59.476673958482344, 13.18939852655596],
    [-59.45710200725774, 13.183172777204444],
    [-59.43862871973718, 13.1748722788806],
    [-59.426909968852904, 13.160386589200625],
]

LOCALITY_ANCHORS = [
    ["westbury", 13.1068, -59.6215],
    ["roebuck", 13.0997, -59.6152],
    ["hindsbury", 13.1080, -59.6150],
    ["hamlet road", 13.1080, -59.6150],
    ["wilkinson", 13.1160, -59.6090],
    ["prerogative", 13.1160, -59.6090],
    ["black rock", 13.1175, -59.6330],
    ["st. stephen", 13.1190, -59.6290],
    ["st stephen", 13.1190, -59.6290],
    ["kensington", 13.1050, -59.6260],
    ["monroe", 13.1120, -59.6170],
    ["broad st", 13.0960, -59.6150],
    ["james st", 13.0960, -59.6150],
    ["church village", 13.0975, -59.6156],
    ["bridgetown", 13.0969, -59.6145],
    ["cgi tower", 13.1490, -59.6180],
    ["warrens industrial", 13.1500, -59.6140],
    ["warrens", 13.1480, -59.6170],
    ["hothersal", 13.1420, -59.5940],
    ["prior park", 13.1530, -59.6270],
    ["thorpes", 13.1550, -59.6330],
    ["taitt hill", 13.1340, -59.5860],
    ["lears business", 13.1260, -59.5830],
    ["lears rd", 13.1240, -59.5840],
    ["dayrells commercial", 13.1180, -59.6030],
    ["salters", 13.1290, -59.5530],
    ["highway 3b", 13.1270, -59.5460],
    ["six cross roads", 13.1350, -59.4620],
    ["highway 5, bridgetown", 13.0910, -59.5900],
    ["highway 7, bridgetown", 13.0770, -59.5930],
    ["sheraton", 13.0750, -59.5660],
    ["kingsland", 13.0790, -59.5540],
    ["oistins", 13.0660, -59.5460],
    ["pilgrim", 13.0780, -59.5200],
    ["inch marlow", 13.0500, -59.5090],
    ["coverly", 13.0800, -59.4960],
    ["coverley", 13.0800, -59.4960],
    ["tom adams", 13.0840, -59.4920],
    ["prospect", 13.1350, -59.6360],
    ["highway 1, bb24009", 13.1880, -59.6370],
    ["sunset crest", 13.1830, -59.6360],
    ["holetown", 13.1850, -59.6370],
    ["mullins", 13.2350, -59.6430],
    ["speightstown", 13.2500, -59.6440],
    ["maynards", 13.2550, -59.6250],
    ["mile and a quarter", 13.2550, -59.6250],
    ["retreat", 13.2550, -59.6250],
    ["windy hill", 13.2520, -59.5780],
    ["ermy bourne", 13.3100, -59.5660],
    ["belleplaine", 13.3210, -59.5660],
    ["workmans", 13.2050, -59.5350],
    ["waverley cot", 13.2030, -59.5470],
    ["belair", 13.1190, -59.4790],
    ["jackmans", 13.1600, -59.5320],
    ["highway 2", 13.1340, -59.6090],
]

LABELS = [
    {"name": "Speightstown", "lat": 13.2500, "lon": -59.6440},
    {"name": "Holetown", "lat": 13.1850, "lon": -59.6370},
    {"name": "Warrens", "lat": 13.1480, "lon": -59.6170},
    {"name": "Bridgetown", "lat": 13.0969, "lon": -59.6145},
    {"name": "Oistins", "lat": 13.0660, "lon": -59.5460},
    {"name": "Belleplaine", "lat": 13.3210, "lon": -59.5660},
]


def load_roads():
    if not ROADS_PATH.exists():
        return []

    road_data = json.loads(ROADS_PATH.read_text(encoding="utf-8"))
    crs_name = road_data.get("crs", {}).get("properties", {}).get("name", "")
    if crs_name and not crs_name.endswith(("::4326", ":4326")):
        raise ValueError(f"Road data must use EPSG:4326 coordinates, got {crs_name}")
    roads = []
    for feature in road_data.get("features", []):
        props = feature.get("properties", {})
        road_type = props.get("Type", "")
        if road_type not in {"Highway", "Secondary Highway"}:
            continue

        geometry = feature.get("geometry", {})
        if geometry.get("type") == "MultiLineString":
            line_groups = geometry.get("coordinates", [])
        elif geometry.get("type") == "LineString":
            line_groups = [geometry.get("coordinates", [])]
        else:
            continue

        for line in line_groups:
            if len(line) < 2:
                continue
            compact_line = [[round(point[0], 5), round(point[1], 5)] for point in line]
            roads.append(
                {
                    "name": props.get("NAME") or road_type,
                    "type": road_type,
                    "coords": compact_line,
                }
            )
    return roads


def inline_logo():
    logo = LOGO_PATH.read_text(encoding="utf-8")
    return re.sub(r"<\?xml[^>]*>\s*", "", logo)


def build_html():
    static_json = json.dumps(
        {
            "boundary": BARBADOS_BOUNDARY,
            "anchors": LOCALITY_ANCHORS,
            "labels": LABELS,
            "roads": load_roads(),
        },
        ensure_ascii=True,
        separators=(",", ":"),
    )
    template = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>S.M. Jaleel Fleet Trip Review - C 3493</title>
<style>
:root {
  --navy: #004182;
  --blue: #134395;
  --cyan: #00aeef;
  --ink: #14213d;
  --muted: #5d6b7d;
  --line: #d8e0ea;
  --paper: #f6f8fb;
  --panel: #ffffff;
  --soft-blue: #e8f5fc;
  --soft-green: #e9f6ef;
  --soft-amber: #fff3d9;
  --green: #22754a;
  --amber: #a46600;
  --red: #b3261e;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  color: var(--ink);
  background: var(--paper);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.45;
}
button { font: inherit; }
.topbar {
  background: var(--navy);
  color: #fff;
  padding: 24px clamp(16px, 4vw, 44px);
}
.topbar-inner, .wrap {
  max-width: 1440px;
  margin: 0 auto;
}
.topbar-inner {
  display: grid;
  grid-template-columns: minmax(150px, 230px) 1fr;
  gap: 24px;
  align-items: center;
}
.brand-logo {
  background: #fff;
  border-radius: 8px;
  padding: 10px 12px;
  min-height: 72px;
  display: grid;
  align-items: center;
}
.brand-logo svg { width: 100%; height: auto; display: block; }
h1 {
  margin: 0;
  font-size: 44px;
  line-height: 1.05;
  font-weight: 760;
  letter-spacing: 0;
}
.headline p {
  margin: 10px 0 0;
  color: rgba(255,255,255,.84);
}
.wrap {
  padding: 24px clamp(16px, 4vw, 44px) 44px;
}
.source-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}
.status {
  color: var(--muted);
  font-size: 13px;
}
.btn {
  appearance: none;
  border: 1px solid var(--line);
  background: var(--panel);
  color: var(--ink);
  border-radius: 8px;
  min-height: 38px;
  padding: 8px 12px;
  cursor: pointer;
}
.btn.primary {
  background: var(--navy);
  border-color: var(--navy);
  color: #fff;
}
.summary-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(150px, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}
.card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 39, 82, 0.04);
}
.metric {
  padding: 16px;
  min-height: 112px;
}
.metric-label {
  color: var(--muted);
  font-size: 13px;
  font-weight: 650;
}
.metric-value {
  margin-top: 8px;
  font-size: 34px;
  line-height: 1;
  font-weight: 760;
  letter-spacing: 0;
}
.metric-note {
  margin-top: 8px;
  color: var(--muted);
  font-size: 13px;
}
.toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin: 20px 0 14px;
}
.segmented, .control-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}
.chip {
  appearance: none;
  border: 1px solid var(--line);
  background: var(--panel);
  color: var(--ink);
  border-radius: 8px;
  min-height: 38px;
  padding: 8px 12px;
  cursor: pointer;
}
.chip[aria-pressed="true"] {
  background: var(--navy);
  border-color: var(--navy);
  color: #fff;
}
.map-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 16px;
  align-items: stretch;
}
.map-card {
  min-height: 640px;
  overflow: hidden;
  position: relative;
}
#fleetMap {
  width: 100%;
  height: clamp(420px, 56vh, 640px);
  display: block;
  background: linear-gradient(180deg, #f8fbfe 0%, #edf5fa 100%);
  touch-action: none;
}
.map-note {
  position: absolute;
  left: 16px;
  bottom: 16px;
  background: rgba(255,255,255,.92);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 10px 12px;
  color: var(--muted);
  font-size: 12px;
  max-width: min(520px, calc(100% - 32px));
}
.map-legend {
  position: absolute;
  right: 16px;
  top: 16px;
  display: grid;
  gap: 7px;
  background: rgba(255,255,255,.94);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 10px 12px;
  color: var(--muted);
  font-size: 12px;
}
.legend-row {
  display: grid;
  grid-template-columns: 24px 1fr;
  gap: 8px;
  align-items: center;
}
.legend-swatch {
  width: 24px;
  height: 0;
  border-top: 3px solid var(--navy);
}
.legend-swatch.road { border-top-color: #b6c3cf; border-top-width: 2px; }
.legend-swatch.zero { border-top-color: var(--muted); border-top-style: dashed; }
.legend-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--navy);
  justify-self: center;
}
.legend-dot.locality { background: var(--amber); }
.legend-pin {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--green);
  color: #fff;
  font-weight: 760;
  font-size: 11px;
  justify-self: center;
}
.legend-pin.end { background: var(--red); }
.side-panel {
  padding: 18px;
  min-height: 640px;
}
.side-panel h2, .section-title {
  margin: 0 0 12px;
  font-size: 20px;
  line-height: 1.2;
}
.detail-row {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 10px;
  padding: 9px 0;
  border-bottom: 1px solid var(--line);
}
.detail-row span:first-child {
  color: var(--muted);
  font-size: 13px;
}
.confidence {
  display: inline-flex;
  width: fit-content;
  border-radius: 999px;
  padding: 4px 9px;
  font-size: 12px;
  font-weight: 700;
}
.confidence.precise { background: var(--soft-green); color: var(--green); }
.confidence.mixed { background: var(--soft-amber); color: var(--amber); }
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 16px;
}
.panel, .risk {
  padding: 18px;
}
.bars {
  display: grid;
  gap: 13px;
}
.bar-row {
  display: grid;
  grid-template-columns: 72px 1fr 70px;
  gap: 12px;
  align-items: center;
}
.bar-track {
  height: 16px;
  background: #eaf0f6;
  border-radius: 999px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  min-width: 2px;
  background: var(--cyan);
}
.bar-value {
  text-align: right;
  font-variant-numeric: tabular-nums;
  color: var(--muted);
  font-size: 13px;
}
.stop-list {
  display: grid;
  gap: 11px;
}
.stop-item {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  align-items: center;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--line);
}
.stop-name { font-weight: 650; }
.stop-visits {
  color: var(--muted);
  font-variant-numeric: tabular-nums;
}
.risk-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 16px;
}
.risk strong {
  display: block;
  margin-bottom: 8px;
}
.risk p {
  margin: 0;
  color: var(--muted);
}
.table-card {
  margin-top: 16px;
  overflow: hidden;
}
.table-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  padding: 16px 18px;
  border-bottom: 1px solid var(--line);
}
.table-head p {
  margin: 4px 0 0;
  color: var(--muted);
  font-size: 13px;
}
.table-wrap {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
table {
  width: 100%;
  border-collapse: collapse;
  background: var(--panel);
}
th, td {
  text-align: left;
  vertical-align: top;
  padding: 11px 12px;
  border-bottom: 1px solid var(--line);
  font-size: 13px;
}
th {
  color: var(--muted);
  font-size: 12px;
  font-weight: 750;
  background: #fbfcfe;
}
td.num, th.num {
  text-align: right;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}
.zero { color: var(--muted); }
.footer {
  margin-top: 16px;
  color: var(--muted);
  font-size: 12px;
}
.coast { fill: #eef7fb; stroke: #9ecadf; stroke-width: 1.5; }
.road-line { fill: none; stroke: #9cabb8; stroke-width: 1; stroke-linecap: round; opacity: .72; }
.road-line.secondary { stroke: #b1beca; stroke-width: .8; opacity: .57; }
.route { fill: none; stroke-width: 2.5; stroke-linecap: round; opacity: .78; }
.route.zero { stroke-dasharray: 3 5; opacity: .28; }
.route-arrow { opacity: .9; pointer-events: none; }
.stop { stroke: #fff; stroke-width: 1.5; cursor: pointer; }
.stop.precise { fill: var(--navy); }
.stop.locality { fill: var(--amber); }
.stop.selected { fill: var(--red); stroke-width: 3; }
.scope-pin { stroke: #fff; stroke-width: 2; pointer-events: none; }
.scope-pin.start { fill: var(--green); }
.scope-pin.end { fill: var(--red); }
.scope-pin.same { fill: var(--navy); }
.scope-pin-label {
  fill: #fff;
  font-size: 12px;
  font-weight: 760;
  text-anchor: middle;
  dominant-baseline: central;
  pointer-events: none;
}
.scope-pin-label.same { font-size: 9px; }
.map-label {
  fill: var(--muted);
  font-size: 11px;
  paint-order: stroke;
  stroke: rgba(255,255,255,.82);
  stroke-width: 3px;
}
@media (max-width: 1100px) {
  .summary-grid { grid-template-columns: repeat(3, minmax(150px, 1fr)); }
  .map-layout { grid-template-columns: 1fr; }
  .side-panel, .map-card { min-height: auto; }
}
@media (max-width: 760px) {
  .topbar { padding: 18px 16px; }
  .topbar-inner { grid-template-columns: 1fr; }
  .brand-logo { max-width: 240px; }
  h1 { font-size: 34px; }
  .headline p { font-size: 14px; }
  .wrap { padding: 16px 14px 32px; }
  .source-row {
    flex-direction: column;
    align-items: stretch;
  }
  .status { width: 100%; }
  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
  }
  .metric {
    min-height: 106px;
    padding: 14px;
  }
  .metric-value { font-size: 28px; }
  .dashboard-grid, .risk-grid { grid-template-columns: 1fr; }
  #fleetMap { height: min(72vh, 430px); }
  .map-legend {
    position: static;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px 4px;
    margin: 0 12px 12px;
    padding: 0;
    border: 0;
    background: transparent;
  }
  .map-note {
    position: static;
    max-width: none;
    margin: 0 12px 12px;
    padding: 0;
    border: 0;
    background: transparent;
  }
  .toolbar, .source-row { align-items: stretch; }
  .control-group, .segmented { width: 100%; }
  .chip, .btn { flex: 1 1 auto; justify-content: center; }
}
@media (max-width: 560px) {
  .brand-logo { max-width: 210px; }
  h1 { font-size: 30px; }
  .summary-grid { grid-template-columns: 1fr; }
  .control-group, .segmented {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
  .source-row .control-group { grid-template-columns: 1fr; }
  .chip, .btn {
    width: 100%;
    min-width: 0;
  }
  .map-layout { gap: 12px; }
  #fleetMap { height: 340px; }
  .side-panel, .panel, .risk { padding: 14px; }
  .detail-row {
    grid-template-columns: 1fr;
    gap: 3px;
  }
  .bar-row {
    grid-template-columns: 1fr;
    gap: 6px;
  }
  .bar-value { text-align: left; }
  .table-head {
    align-items: flex-start;
    flex-direction: column;
    padding: 14px;
  }
  .table-wrap { overflow-x: visible; }
  table, thead, tbody, tr, td {
    display: block;
    width: 100%;
  }
  thead {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0 0 0 0);
  }
  tbody {
    display: grid;
    gap: 10px;
    padding: 12px;
  }
  tr {
    border: 1px solid var(--line);
    border-radius: 8px;
    background: var(--panel);
    overflow: hidden;
  }
  td {
    display: grid;
    grid-template-columns: minmax(92px, 36%) 1fr;
    gap: 10px;
    align-items: start;
    padding: 9px 10px;
  }
  td::before {
    content: attr(data-label);
    color: var(--muted);
    font-size: 12px;
    font-weight: 750;
  }
  td.num {
    text-align: left;
    white-space: normal;
  }
}
</style>
</head>
<body>
<div class="page">
  <header class="topbar">
    <div class="topbar-inner">
      <div class="brand-logo" aria-label="S.M. Jaleel">__LOGO__</div>
      <div class="headline">
        <h1>Fleet Trip Review</h1>
        <p><span id="deviceName">Truck</span> | Barbados service activity | <span id="dateRange">Loading</span></p>
      </div>
    </div>
  </header>

  <main class="wrap">
    <section class="source-row" aria-label="Data source controls">
      <div class="status" id="sourceStatus" aria-live="polite">Loading ServiceTruckCSV.csv...</div>
    </section>

    <section class="summary-grid" aria-label="Executive summary">
      <article class="card metric"><div class="metric-label">Total distance</div><div class="metric-value" id="totalDistance"></div><div class="metric-note">Across filtered trips</div></article>
      <article class="card metric"><div class="metric-label">Trips recorded</div><div class="metric-value" id="tripCount"></div><div class="metric-note" id="nearZero"></div></article>
      <article class="card metric"><div class="metric-label">Driving time</div><div class="metric-value" id="drivingTime"></div><div class="metric-note">Engine-on movement</div></article>
      <article class="card metric"><div class="metric-label">Idling time</div><div class="metric-value" id="idlingTime"></div><div class="metric-note" id="idleRatio"></div></article>
      <article class="card metric"><div class="metric-label">Peak speed</div><div class="metric-value" id="maxSpeed"></div><div class="metric-note">Maximum recorded</div></article>
    </section>

    <section class="toolbar" aria-label="Map filters">
      <div class="segmented" id="dayFilters"></div>
      <div class="control-group" aria-label="Map controls">
        <button class="btn" type="button" id="zoomIn" aria-label="Zoom in">+</button>
        <button class="btn" type="button" id="zoomOut" aria-label="Zoom out">-</button>
        <button class="btn primary" type="button" id="resetView">Reset view</button>
      </div>
    </section>

    <section class="map-layout">
      <article class="card map-card">
        <svg id="fleetMap" role="img" aria-labelledby="mapTitle mapDesc">
          <title id="mapTitle">Barbados trip map</title>
          <desc id="mapDesc">Trip routes and stop concentrations by day.</desc>
        </svg>
        <div class="map-legend" aria-label="Map legend">
          <div class="legend-row"><span class="legend-swatch road"></span><span>Roads</span></div>
          <div class="legend-row"><span class="legend-swatch"></span><span>Trip path</span></div>
          <div class="legend-row"><span class="legend-swatch zero"></span><span>Near-zero leg</span></div>
          <div class="legend-row"><span class="legend-dot"></span><span>Plus Code stop</span></div>
          <div class="legend-row"><span class="legend-dot locality"></span><span>Locality anchor</span></div>
          <div class="legend-row"><span class="legend-pin">S</span><span>First start</span></div>
          <div class="legend-row"><span class="legend-pin end">E</span><span>Final stop</span></div>
        </div>
        <div class="map-note">Roads provide geographic context; paths connect recorded starts and stops, not driven road routes. Select a day for direction arrows.</div>
      </article>
      <aside class="card side-panel" aria-live="polite">
        <h2 id="detailTitle">Selected Activity</h2>
        <div id="detailPanel"></div>
      </aside>
    </section>

    <section class="dashboard-grid">
      <article class="card panel"><h2 class="section-title">Daily Distance</h2><div class="bars" id="distanceBars"></div></article>
      <article class="card panel"><h2 class="section-title">Most Frequent Stops</h2><div class="stop-list" id="topStops"></div></article>
    </section>

    <section class="risk-grid" aria-label="Management considerations">
      <article class="card risk"><strong>Idle time concentration</strong><p id="idleInsight"></p></article>
      <article class="card risk"><strong>Near-zero trip records</strong><p id="zeroInsight"></p></article>
      <article class="card risk"><strong>Location confidence</strong><p id="confidenceInsight"></p></article>
    </section>

    <section class="card table-card">
      <div class="table-head">
        <div><h2 class="section-title">Trip Log</h2><p id="tableSubhead"></p></div>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Start</th><th>Origin</th><th>Destination</th>
              <th class="num">Km</th><th class="num">Drive h</th><th class="num">Idle h</th>
              <th class="num">Stop h</th><th class="num">Max speed</th><th>Zones</th>
            </tr>
          </thead>
          <tbody id="tripRows"></tbody>
        </table>
      </div>
    </section>
    <p class="footer">Prepared from the active CSV. Boundary: SimpleMaps Barbados WGS84 GeoJSON, Creative Commons Attribution 4.0. Road context: Caribbean Marine Atlas road network. Locality-anchor coordinates should be validated before operational routing decisions.</p>
  </main>
</div>

<script>
const STATIC = __STATIC_JSON__;
const BRIDGETOWN_REF = [13.0975, -59.6167];
const OLC_ALPHABET = "23456789CFGHJMPQRVWX";
const OLC_PAIR_RESOLUTIONS = [20, 1, 0.05, 0.0025, 0.000125];
const PLUS_RE = /\b[23456789CFGHJMPQRVWX]{2,8}\+[23456789CFGHJMPQRVWX]{2,3}\b/i;
let DATA = null;

const state = { day: "all", selectedStop: null, viewBox: null, baseViewBox: null, isDragging: false, dragStart: null };
const dayColors = ["#004182", "#00aeef", "#22754a", "#a46600", "#7d4ab7", "#b3261e"];
const svg = document.getElementById("fleetMap");

function byId(id) { return document.getElementById(id); }
function fmt(value, digits = 1) { return Number(value || 0).toLocaleString(undefined, { maximumFractionDigits: digits, minimumFractionDigits: digits }); }
function fmtCompact(value) { return Number(value || 0).toLocaleString(undefined, { maximumFractionDigits: 0 }); }
function esc(value) { return String(value ?? "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char])); }
function setStatus(message, isError = false) {
  const status = byId("sourceStatus");
  status.textContent = message;
  status.style.color = isError ? "var(--red)" : "var(--muted)";
}
function parseCSV(text) {
  const rows = [];
  let row = [], field = "", inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const char = text[i], next = text[i + 1];
    if (char === '"') {
      if (inQuotes && next === '"') { field += '"'; i++; }
      else { inQuotes = !inQuotes; }
    } else if (char === "," && !inQuotes) {
      row.push(field); field = "";
    } else if ((char === "\n" || char === "\r") && !inQuotes) {
      if (char === "\r" && next === "\n") i++;
      row.push(field); field = "";
      if (row.some(cell => cell.length)) rows.push(row);
      row = [];
    } else {
      field += char;
    }
  }
  row.push(field);
  if (row.some(cell => cell.length)) rows.push(row);
  const headers = rows.shift().map(h => h.replace(/^\uFEFF/, "").trim());
  return rows.map(values => Object.fromEntries(headers.map((h, i) => [h, values[i] ?? ""])));
}
function encodeOlc(lat, lon, length = 10) {
  let latVal = Math.min(Math.max(lat, -90), 90 - 1e-12) + 90;
  let lonVal = ((lon + 180) % 360);
  let chars = "";
  for (const res of OLC_PAIR_RESOLUTIONS) {
    const latDigit = Math.floor(latVal / res);
    const lonDigit = Math.floor(lonVal / res);
    chars += OLC_ALPHABET[latDigit] + OLC_ALPHABET[lonDigit];
    latVal -= latDigit * res;
    lonVal -= lonDigit * res;
    if (chars.length >= length) break;
  }
  return `${chars.slice(0, 8)}+${chars.slice(8, length)}`;
}
function recoverShortCode(code) {
  const plusIndex = code.indexOf("+");
  if (plusIndex >= 8) return code;
  const shortClean = code.replace("+", "");
  const missing = 8 - plusIndex;
  const refFull = encodeOlc(BRIDGETOWN_REF[0], BRIDGETOWN_REF[1], 10).replace("+", "");
  const recovered = refFull.slice(0, missing) + shortClean;
  return `${recovered.slice(0, 8)}+${recovered.slice(8)}`;
}
function decodeOlc(code) {
  const fullCode = recoverShortCode(code.toUpperCase());
  const full = fullCode.replace("+", "").slice(0, 10);
  let lat = -90, lon = -180;
  OLC_PAIR_RESOLUTIONS.forEach((res, i) => {
    lat += OLC_ALPHABET.indexOf(full[i * 2]) * res;
    lon += OLC_ALPHABET.indexOf(full[i * 2 + 1]) * res;
  });
  lat += OLC_PAIR_RESOLUTIONS[Math.floor(full.length / 2) - 1] / 2;
  lon += OLC_PAIR_RESOLUTIONS[Math.floor(full.length / 2) - 1] / 2;
  return { lat: Number(lat.toFixed(6)), lon: Number(lon.toFixed(6)), fullCode };
}
function excelDate(value) {
  const ms = (Number(value) - 25569) * 86400 * 1000;
  return new Date(ms);
}
function dateLabel(date) {
  return date.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}
function dateKey(date) {
  return date.toISOString().slice(0, 10);
}
function dateTimeLabel(date) {
  return `${dateKey(date)} ${date.toTimeString().slice(0, 5)}`;
}
function hours(value) {
  return Number(value || 0) * 24;
}
function shortPlace(address) {
  let text = address || "";
  if (text.includes(":")) text = text.split(":").slice(1).join(":");
  text = text.replace(/^\d{5,6},\s*/, "").replace(PLUS_RE, "").replace(/,\s*Barbados/gi, "");
  return text.replace(/\s+/g, " ").replace(/^[\s,-]+|[\s,-]+$/g, "") || address;
}
function coordinateFor(address) {
  const match = String(address).match(PLUS_RE);
  if (match) {
    const decoded = decodeOlc(match[0]);
    return { lat: decoded.lat, lon: decoded.lon, confidence: "precise", method: `Plus Code ${decoded.fullCode}` };
  }
  const lowered = String(address).toLowerCase();
  for (const [key, lat, lon] of STATIC.anchors) {
    if (lowered.includes(key)) return { lat, lon, confidence: "locality", method: `Locality anchor: ${key}` };
  }
  return { lat: BRIDGETOWN_REF[0], lon: BRIDGETOWN_REF[1], confidence: "locality", method: "Locality anchor: Barbados fallback" };
}
function validateRows(rawRows) {
  const required = ["Device", "Start Date", "Stop Date", "Distance", "Driving Duration", "Stop Duration", "Origin", "Destination", "Idling Duration", "Maximum Speed"];
  const missing = required.filter(col => !(col in (rawRows[0] || {})));
  if (missing.length) throw new Error(`CSV is missing required columns: ${missing.join(", ")}`);
}
function buildDataset(csvText, sourceName) {
  const rawRows = parseCSV(csvText).filter(row => row["Start Date"] && row.Origin && row.Destination);
  validateRows(rawRows);
  const addressSet = new Set();
  rawRows.forEach(row => { addressSet.add(row.Origin); addressSet.add(row.Destination); });
  const locations = {};
  [...addressSet].sort().forEach(address => {
    locations[address] = { name: shortPlace(address), address, ...coordinateFor(address) };
  });
  const rows = rawRows.map((row, index) => {
    const start = excelDate(row["Start Date"]);
    const stop = excelDate(row["Stop Date"]);
    const origin = locations[row.Origin];
    const destination = locations[row.Destination];
    return {
      id: index + 1,
      device: row.Device,
      date: dateKey(start),
      start: dateTimeLabel(start),
      stop: dateTimeLabel(stop),
      origin: origin.name,
      destination: destination.name,
      originFull: row.Origin,
      destinationFull: row.Destination,
      originLat: origin.lat,
      originLon: origin.lon,
      destLat: destination.lat,
      destLon: destination.lon,
      distance: Number(row.Distance || 0),
      drivingHours: hours(row["Driving Duration"]),
      stopHours: hours(row["Stop Duration"]),
      idlingHours: hours(row["Idling Duration"]),
      maxSpeed: Number(row["Maximum Speed"] || 0),
      zoneTypes: row["Stop Zone Types"] || "Unclassified",
      nearZero: Number(row.Distance || 0) < 0.05
    };
  }).sort((a, b) => a.start.localeCompare(b.start));
  const days = [...new Set(rows.map(row => row.date))].sort();
  const daily = days.map(date => {
    const dayRows = rows.filter(row => row.date === date);
    return {
      date,
      label: dateLabel(new Date(`${date}T12:00:00`)),
      trips: dayRows.length,
      distance: dayRows.reduce((sum, row) => sum + row.distance, 0),
      drivingHours: dayRows.reduce((sum, row) => sum + row.drivingHours, 0),
      idlingHours: dayRows.reduce((sum, row) => sum + row.idlingHours, 0),
      stopHours: dayRows.reduce((sum, row) => sum + row.stopHours, 0),
      maxSpeed: dayRows.reduce((max, row) => Math.max(max, row.maxSpeed), 0),
      nearZero: dayRows.filter(row => row.nearZero).length
    };
  });
  const confidenceCounts = Object.values(locations).reduce((acc, loc) => {
    acc[loc.confidence] = (acc[loc.confidence] || 0) + 1;
    return acc;
  }, {});
  const topStopCounts = {};
  rows.forEach(row => {
    topStopCounts[row.origin] = (topStopCounts[row.origin] || 0) + 1;
    topStopCounts[row.destination] = (topStopCounts[row.destination] || 0) + 1;
  });
  const topStops = Object.entries(topStopCounts).sort((a, b) => b[1] - a[1]).slice(0, 6).map(([name, visits]) => ({ name, visits }));
  const totalDriving = rows.reduce((sum, row) => sum + row.drivingHours, 0);
  const totalIdling = rows.reduce((sum, row) => sum + row.idlingHours, 0);
  const highestIdleDay = daily.reduce((best, day) => day.idlingHours > best.idlingHours ? day : best, daily[0]);
  return {
    sourceName,
    rows,
    locations,
    days,
    daily,
    boundary: STATIC.boundary,
    roads: STATIC.roads || [],
    labels: STATIC.labels,
    summary: {
      device: rows[0]?.device || "Truck",
      dateRange: days.length ? `${days[0]} to ${days[days.length - 1]}` : "No dates",
      tripCount: rows.length,
      locationCount: Object.keys(locations).length,
      totalDistance: rows.reduce((sum, row) => sum + row.distance, 0),
      totalDrivingHours: totalDriving,
      totalIdlingHours: totalIdling,
      totalStopHours: rows.reduce((sum, row) => sum + row.stopHours, 0),
      maxSpeed: rows.reduce((max, row) => Math.max(max, row.maxSpeed), 0),
      nearZeroCount: rows.filter(row => row.nearZero).length,
      idlingToDriving: totalDriving ? (totalIdling / totalDriving) * 100 : 0,
      confidenceCounts,
      topStops,
      highestIdleDay
    }
  };
}
function loadCsv(csvText, sourceName) {
  DATA = buildDataset(csvText, sourceName);
  state.day = "all";
  state.selectedStop = null;
  state.viewBox = null;
  state.baseViewBox = null;
  renderAll();
  setStatus(`Loaded ${sourceName}: ${DATA.rows.length} trips, ${DATA.summary.locationCount} locations.`);
}
async function loadPublishedCsv() {
  try {
    const response = await fetch(`ServiceTruckCSV.csv?refresh=${Date.now()}`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    loadCsv(await response.text(), "ServiceTruckCSV.csv");
  } catch (error) {
    setStatus(`Could not load ServiceTruckCSV.csv (${error.message}). Keep it beside the HTML and redeploy the site.`, true);
  }
}
function filteredRows() { return state.day === "all" ? DATA.rows : DATA.rows.filter(row => row.date === state.day); }
function currentStats() {
  const rows = filteredRows();
  return {
    trips: rows.length,
    distance: rows.reduce((sum, row) => sum + row.distance, 0),
    driving: rows.reduce((sum, row) => sum + row.drivingHours, 0),
    idling: rows.reduce((sum, row) => sum + row.idlingHours, 0),
    stop: rows.reduce((sum, row) => sum + row.stopHours, 0),
    nearZero: rows.filter(row => row.nearZero).length,
    maxSpeed: rows.reduce((max, row) => Math.max(max, row.maxSpeed), 0)
  };
}
function setViewBox(box) {
  state.viewBox = box;
  svg.setAttribute("viewBox", box.join(" "));
}
function projectFactory(width, height) {
  const coords = [...DATA.boundary, ...Object.values(DATA.locations).map(loc => [loc.lon, loc.lat])];
  const meanLat = coords.reduce((sum, coord) => sum + coord[1], 0) / coords.length;
  const cos = Math.cos(meanLat * Math.PI / 180);
  const xs = coords.map(coord => coord[0] * cos);
  const ys = coords.map(coord => coord[1]);
  const minX = Math.min(...xs), maxX = Math.max(...xs);
  const minY = Math.min(...ys), maxY = Math.max(...ys);
  const pad = 42;
  return (lon, lat) => {
    const x = pad + ((lon * cos - minX) / (maxX - minX || 1)) * (width - pad * 2);
    const y = pad + ((maxY - lat) / (maxY - minY || 1)) * (height - pad * 2);
    return [x, y];
  };
}
function aggregateStops(rows) {
  const stops = new Map();
  rows.forEach(row => {
    [
      { name: row.origin, full: row.originFull, lat: row.originLat, lon: row.originLon },
      { name: row.destination, full: row.destinationFull, lat: row.destLat, lon: row.destLon }
    ].forEach(stop => {
      const loc = DATA.locations[stop.full];
      if (!stops.has(stop.full)) stops.set(stop.full, { ...stop, confidence: loc.confidence, method: loc.method, visits: 0 });
      stops.get(stop.full).visits += 1;
    });
  });
  return [...stops.values()].sort((a, b) => b.visits - a.visits);
}
function drawMap() {
  const width = 960, height = 680, project = projectFactory(width, height), rows = filteredRows(), stops = aggregateStops(rows);
  svg.innerHTML = `<title id="mapTitle">Barbados trip map</title><desc id="mapDesc">Roads, trip connections, stops, and first start and final stop for the selected dates.</desc>`;
  svg.setAttribute("width", width);
  svg.setAttribute("height", height);
  if (!state.baseViewBox) {
    state.baseViewBox = [0, 0, width, height];
    setViewBox([...state.baseViewBox]);
  }
  const coastPath = DATA.boundary.map((coord, index) => {
    const [x, y] = project(coord[0], coord[1]);
    return `${index === 0 ? "M" : "L"} ${x.toFixed(1)} ${y.toFixed(1)}`;
  }).join(" ") + " Z";
  const coast = document.createElementNS("http://www.w3.org/2000/svg", "path");
  coast.setAttribute("d", coastPath);
  coast.setAttribute("class", "coast");
  svg.appendChild(coast);
  const roadsLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
  roadsLayer.setAttribute("aria-label", "Road network");
  DATA.roads.forEach(road => {
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", road.coords.map((coord, index) => {
      const [x, y] = project(coord[0], coord[1]);
      return `${index ? "L" : "M"} ${x.toFixed(1)} ${y.toFixed(1)}`;
    }).join(" "));
    path.setAttribute("class", `road-line ${road.type === "Secondary Highway" ? "secondary" : ""}`);
    roadsLayer.appendChild(path);
  });
  svg.appendChild(roadsLayer);
  const dayIndex = new Map(DATA.days.map((date, index) => [date, index]));
  rows.forEach(row => {
    const [x1, y1] = project(row.originLon, row.originLat);
    const [x2, y2] = project(row.destLon, row.destLat);
    const line = document.createElementNS("http://www.w3.org/2000/svg", "path");
    const cx = (x1 + x2) / 2;
    const cy = (y1 + y2) / 2 - Math.min(26, Math.max(8, row.distance * 0.7));
    line.setAttribute("d", `M ${x1.toFixed(1)} ${y1.toFixed(1)} Q ${cx.toFixed(1)} ${cy.toFixed(1)} ${x2.toFixed(1)} ${y2.toFixed(1)}`);
    line.setAttribute("class", `route ${row.nearZero ? "zero" : ""}`);
    const color = dayColors[dayIndex.get(row.date) % dayColors.length];
    line.setAttribute("stroke", color);
    const tip = document.createElementNS("http://www.w3.org/2000/svg", "title");
    tip.textContent = `${row.start} | ${row.origin} to ${row.destination} | ${fmt(row.distance)} km`;
    line.appendChild(tip);
    svg.appendChild(line);
    if (state.day !== "all" && !row.nearZero && Math.hypot(x2 - x1, y2 - y1) > 22) {
      const at = t => [(1-t)*(1-t)*x1 + 2*(1-t)*t*cx + t*t*x2, (1-t)*(1-t)*y1 + 2*(1-t)*t*cy + t*t*y2];
      const [ax, ay] = at(.63), [bx, by] = at(.67);
      const angle = Math.atan2(by - ay, bx - ax);
      const arrow = document.createElementNS("http://www.w3.org/2000/svg", "path");
      arrow.setAttribute("d", `M ${ax + 5*Math.cos(angle)} ${ay + 5*Math.sin(angle)} L ${ax - 5*Math.cos(angle) + 4*Math.sin(angle)} ${ay - 5*Math.sin(angle) - 4*Math.cos(angle)} L ${ax - 5*Math.cos(angle) - 4*Math.sin(angle)} ${ay - 5*Math.sin(angle) + 4*Math.cos(angle)} Z`);
      arrow.setAttribute("class", "route-arrow");
      arrow.setAttribute("fill", color);
      svg.appendChild(arrow);
    }
  });
  stops.forEach(stop => {
    const [x, y] = project(stop.lon, stop.lat);
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", x.toFixed(1));
    circle.setAttribute("cy", y.toFixed(1));
    circle.setAttribute("r", Math.max(4.5, Math.min(15, 4 + Math.sqrt(stop.visits) * 2.1)).toFixed(1));
    circle.setAttribute("class", `stop ${stop.confidence} ${state.selectedStop === stop.full ? "selected" : ""}`);
    circle.setAttribute("tabindex", "0");
    circle.setAttribute("role", "button");
    circle.setAttribute("aria-label", `${stop.name}, ${stop.visits} visits`);
    circle.addEventListener("click", () => selectStop(stop));
    circle.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === " ") { event.preventDefault(); selectStop(stop); }
    });
    const tip = document.createElementNS("http://www.w3.org/2000/svg", "title");
    tip.textContent = `${stop.name} | ${stop.visits} visits | ${stop.confidence}`;
    circle.appendChild(tip);
    svg.appendChild(circle);
  });
  DATA.labels.forEach(label => {
    const [x, y] = project(label.lon, label.lat);
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", x.toFixed(1));
    text.setAttribute("y", y.toFixed(1));
    text.setAttribute("class", "map-label");
    text.textContent = label.name;
    svg.appendChild(text);
  });
  if (rows.length) {
    const first = rows[0], last = rows[rows.length - 1];
    const [sx, sy] = project(first.originLon, first.originLat);
    let [ex, ey] = project(last.destLon, last.destLat);
    const samePlace = Math.hypot(ex - sx, ey - sy) < 1;
    if (!samePlace && Math.hypot(ex - sx, ey - sy) < 22) { ex += 22; ey -= 20; }
    const pins = samePlace
      ? [["S/E", sx, sy, "same", `First start and final stop: ${first.origin} (${first.start} to ${last.stop})`]]
      : [["S", sx, sy, "start", `First start: ${first.origin} (${first.start})`],
         ["E", ex, ey, "end", `Final stop: ${last.destination} (${last.stop})`]];
    pins.forEach(([letter, x, y, kind, description]) => {
      const pin = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      pin.setAttribute("cx", x.toFixed(1));
      pin.setAttribute("cy", y.toFixed(1));
      pin.setAttribute("r", "11");
      pin.setAttribute("class", `scope-pin ${kind}`);
      const tip = document.createElementNS("http://www.w3.org/2000/svg", "title");
      tip.textContent = description;
      pin.appendChild(tip);
      svg.appendChild(pin);
      const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("x", x.toFixed(1));
      label.setAttribute("y", y.toFixed(1));
      label.setAttribute("class", `scope-pin-label ${kind}`);
      label.textContent = letter;
      svg.appendChild(label);
    });
  }
}
function selectStop(stop) {
  state.selectedStop = stop.full;
  drawMap();
  renderDetail(stop);
}
function renderDetail(stop = null) {
  const panel = byId("detailPanel"), stats = currentStats(), rows = filteredRows();
  if (!stop) {
    byId("detailTitle").textContent = "Selected Activity";
    panel.innerHTML = `
      <div class="detail-row"><span>Scope</span><strong>${state.day === "all" ? "All service days" : state.day}</strong></div>
      <div class="detail-row"><span>First start</span><strong>${rows.length ? esc(rows[0].origin) : "n/a"}</strong></div>
      <div class="detail-row"><span>Final stop</span><strong>${rows.length ? esc(rows[rows.length - 1].destination) : "n/a"}</strong></div>
      <div class="detail-row"><span>Distance</span><strong>${fmt(stats.distance)} km</strong></div>
      <div class="detail-row"><span>Driving</span><strong>${fmt(stats.driving, 2)} hours</strong></div>
      <div class="detail-row"><span>Idling</span><strong>${fmt(stats.idling, 2)} hours</strong></div>
      <div class="detail-row"><span>Stops</span><strong>${fmt(stats.stop, 2)} hours</strong></div>
      <div class="detail-row"><span>Peak speed</span><strong>${fmtCompact(stats.maxSpeed)}</strong></div>`;
    return;
  }
  byId("detailTitle").textContent = stop.name;
  const related = filteredRows().filter(row => row.originFull === stop.full || row.destinationFull === stop.full);
  const distance = related.reduce((sum, row) => sum + row.distance, 0);
  panel.innerHTML = `
    <div class="detail-row"><span>Visits</span><strong>${stop.visits}</strong></div>
    <div class="detail-row"><span>Related km</span><strong>${fmt(distance)} km</strong></div>
    <div class="detail-row"><span>Coordinate</span><strong>${stop.lat.toFixed(5)}, ${stop.lon.toFixed(5)}</strong></div>
    <div class="detail-row"><span>Confidence</span><strong><span class="confidence ${stop.confidence === "precise" ? "precise" : "mixed"}">${stop.confidence === "precise" ? "Precise" : "Locality anchor"}</span></strong></div>
    <div class="detail-row"><span>Method</span><strong>${esc(stop.method)}</strong></div>
    <div class="detail-row"><span>Address</span><strong>${esc(stop.full)}</strong></div>`;
}
function renderFilters() {
  const filters = byId("dayFilters");
  const buttons = [{ date: "all", label: "All days" }, ...DATA.daily.map(day => ({ date: day.date, label: day.label }))];
  filters.innerHTML = buttons.map(item => `<button class="chip" type="button" aria-pressed="${state.day === item.date}" data-day="${item.date}">${item.label}</button>`).join("");
  filters.querySelectorAll("button").forEach(button => {
    button.addEventListener("click", () => {
      state.day = button.dataset.day;
      state.selectedStop = null;
      renderAll();
    });
  });
}
function renderSummary() {
  const stats = currentStats();
  byId("deviceName").textContent = DATA.summary.device;
  byId("dateRange").textContent = DATA.summary.dateRange;
  byId("totalDistance").textContent = `${fmt(stats.distance)} km`;
  byId("tripCount").textContent = fmtCompact(stats.trips);
  byId("nearZero").textContent = `${stats.nearZero} near-zero records`;
  byId("drivingTime").textContent = `${fmt(stats.driving, 1)} h`;
  byId("idlingTime").textContent = `${fmt(stats.idling, 1)} h`;
  byId("idleRatio").textContent = `${stats.driving ? fmtCompact((stats.idling / stats.driving) * 100) : 0}% of driving time`;
  byId("maxSpeed").textContent = fmtCompact(stats.maxSpeed);
}
function renderBars() {
  const maxDistance = Math.max(...DATA.daily.map(day => day.distance), 1);
  byId("distanceBars").innerHTML = DATA.daily.map(day => `
    <div class="bar-row">
      <strong>${day.label}</strong>
      <div class="bar-track" aria-label="${day.label} distance ${fmt(day.distance)} kilometers">
        <div class="bar-fill" style="width:${Math.max(2, (day.distance / maxDistance) * 100).toFixed(1)}%"></div>
      </div>
      <div class="bar-value">${fmt(day.distance)} km</div>
    </div>`).join("");
}
function renderStops() {
  byId("topStops").innerHTML = DATA.summary.topStops.map(stop => `
    <div class="stop-item"><div class="stop-name">${esc(stop.name)}</div><div class="stop-visits">${stop.visits} visits</div></div>`).join("");
}
function renderInsights() {
  const s = DATA.summary;
  byId("idleInsight").textContent = `${fmt(s.totalIdlingHours, 1)} idle hours were recorded, equal to about ${fmtCompact(s.idlingToDriving)}% of total driving time. Highest idle day: ${s.highestIdleDay?.label || "n/a"}.`;
  byId("zeroInsight").textContent = `${s.nearZeroCount} legs were under 0.05 km and are visually de-emphasized as likely parked/GPS-jitter records.`;
  byId("confidenceInsight").textContent = `${s.confidenceCounts.precise || 0} locations decoded from Plus Codes; ${s.confidenceCounts.locality || 0} use named locality anchors and should be validated for operational routing.`;
}
function renderTable() {
  const rows = filteredRows();
  byId("tableSubhead").textContent = `${rows.length} records shown from ${DATA.sourceName}`;
  byId("tripRows").innerHTML = rows.map(row => `
    <tr class="${row.nearZero ? "zero" : ""}">
      <td data-label="Start">${esc(row.start)}</td><td data-label="Origin">${esc(row.origin)}</td><td data-label="Destination">${esc(row.destination)}</td>
      <td class="num" data-label="Km">${fmt(row.distance, 2)}</td><td class="num" data-label="Drive h">${fmt(row.drivingHours, 2)}</td>
      <td class="num" data-label="Idle h">${fmt(row.idlingHours, 2)}</td><td class="num" data-label="Stop h">${fmt(row.stopHours, 2)}</td>
      <td class="num" data-label="Max speed">${fmtCompact(row.maxSpeed)}</td><td data-label="Zones">${esc(row.zoneTypes)}</td>
    </tr>`).join("");
}
function renderAll() {
  renderFilters();
  renderSummary();
  drawMap();
  renderDetail();
  renderBars();
  renderStops();
  renderInsights();
  renderTable();
}
function zoom(factor) {
  const [x, y, w, h] = state.viewBox;
  const nw = w * factor, nh = h * factor;
  setViewBox([x + (w - nw) / 2, y + (h - nh) / 2, nw, nh]);
}
byId("zoomIn").addEventListener("click", () => zoom(0.78));
byId("zoomOut").addEventListener("click", () => zoom(1.22));
byId("resetView").addEventListener("click", () => setViewBox([...state.baseViewBox]));
svg.addEventListener("pointerdown", event => {
  state.isDragging = true;
  state.dragStart = { x: event.clientX, y: event.clientY, box: [...state.viewBox] };
  svg.setPointerCapture(event.pointerId);
});
svg.addEventListener("pointermove", event => {
  if (!state.isDragging) return;
  const rect = svg.getBoundingClientRect();
  const scaleX = state.viewBox[2] / rect.width;
  const scaleY = state.viewBox[3] / rect.height;
  const dx = (event.clientX - state.dragStart.x) * scaleX;
  const dy = (event.clientY - state.dragStart.y) * scaleY;
  setViewBox([state.dragStart.box[0] - dx, state.dragStart.box[1] - dy, state.dragStart.box[2], state.dragStart.box[3]]);
});
svg.addEventListener("pointerup", () => state.isDragging = false);
svg.addEventListener("pointercancel", () => state.isDragging = false);

loadPublishedCsv();
</script>
</body>
</html>
'''
    return (
        template.replace("__LOGO__", inline_logo())
        .replace("__STATIC_JSON__", static_json)
    )


def main():
    OUT_PATH.write_text(build_html(), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
